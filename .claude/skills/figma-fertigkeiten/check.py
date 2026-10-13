#!/usr/bin/env python3
"""Prüft die Sektionen "## Figma-Fertigkeiten" in _lehrveranstaltungen/.

Aufruf (aus dem Repo-Root):
  python3 .claude/skills/figma-fertigkeiten/check.py                 Vollständige Prüfung
  python3 .claude/skills/figma-fertigkeiten/check.py --offline       Ohne Netzwerkprüfungen
  python3 .claude/skills/figma-fertigkeiten/check.py --stand-aktualisieren
                                    Prüfen und aktuellen Stand als "abgeglichen" speichern
  python3 .claude/skills/figma-fertigkeiten/check.py suche-hilfe <Begriff>...
  python3 .claude/skills/figma-fertigkeiten/check.py suche-video <Begriff>...
  python3 .claude/skills/figma-fertigkeiten/check.py pruefe-video <YouTube-ID>...

Nur Standardbibliothek, damit es ohne Installation läuft.
"""
import concurrent.futures
import datetime as dt
import difflib
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# --- Konfiguration -----------------------------------------------------------

REPO = Path(__file__).resolve().parents[3]
LV_DIR = REPO / "_lehrveranstaltungen"
AS_DIR = REPO / "_assignments"
STAND = Path(__file__).resolve().parent / "stand.json"
BASEURL = "/mi-bachelor-screendesign"

SECTION = "## Figma-Fertigkeiten"
HINWEIS = "Für diese Übungen werden keine neuen Figma-Fertigkeiten benötigt."
PFLEGE_KOMMENTAR = "{% comment %}Gepflegt mit dem Claude-Code-Skill /figma-fertigkeiten, siehe README.md{% endcomment %}"
TYPEN = {"workshop", "training"}
FIGMA_CHANNEL = "https://www.youtube.com/@figma"

# Videos außerhalb der Sektion, die bleiben dürfen (eigene Kursinhalte).
ERLAUBTE_KANAELE = {"mikoeln", "Christian Noss"}
# help.figma.com-Links außerhalb der Sektion, die bleiben dürfen (Einrichtung, keine Tutorials).
ERLAUBTE_HILFE_LINKS = {"360041061214"}  # Education Plan

VIDEO_MAX_JAHRE = 5
STIL_WARNUNGEN = {
    " – ": "Gedankenstrich im Text wirkt schnell generiert",
    "Rechtsklick-Menü": "lieber „mit der rechten Maustaste …“",
    "nahtlos": "Floskel",
    "mühelos": "Floskel",
    "Das spart": "Floskel",
}

UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}

# --- Hilfsfunktionen ---------------------------------------------------------


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # Timeout, DNS …
        return None, str(e)


def http_json(url):
    status, body = http_get(url)
    if status == 200:
        try:
            return status, json.loads(body)
        except json.JSONDecodeError:
            return status, None
    return status, None


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return {}, text, text
    fm, body = {}, m.group(2)
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"([A-Za-z0-9_-]+):\s?(.*)$", line)
        if km and not line.startswith((" ", "\t")):
            key, val = km.group(1), km.group(2).strip()
            fm[key] = "" if val in ("|", ">") else val
        elif key is not None:
            fm[key] += line + "\n"
    return fm, body, text


def erste_termin(termine):
    daten = re.findall(r"(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}:\d{2}))?", termine or "")
    if not daten:
        return None
    return min(dt.datetime.fromisoformat(f"{d} {t or '00:00'}") for d, t in daten)


def semester_zeitraum():
    cfg = (REPO / "_config.yml").read_text(encoding="utf-8")
    m = re.search(r"^semester:\s*((Wintersemester|Sommersemester)\s*(\d{4})\S*)", cfg, re.M)
    if not m:
        sys.exit("semester in _config.yml nicht gefunden")
    name, jahr = m.group(1), int(m.group(3))
    if m.group(2) == "Wintersemester":
        return name, dt.datetime(jahr, 9, 1), dt.datetime(jahr + 1, 3, 31, 23, 59)
    return name, dt.datetime(jahr, 4, 1), dt.datetime(jahr, 8, 31, 23, 59)


def section_bounds(body):
    m = re.search(rf"^{re.escape(SECTION)}\n(.*?)(?=^## |^<!--|\Z)", body, re.S | re.M)
    return m


ENTRY_RE = re.compile(r"^- \*\*(?P<label>.+?):\*\* (?P<text>.+)\n  (?P<links>.+)$", re.M)
ARTIKEL_RE = re.compile(r"\[Figma-Hilfe(?P<en> \(englisch\))?\]\((?P<url>https://help\.figma\.com/hc/(?P<loc>[a-z-]+)/articles/(?P<id>\d+)[^)]*)\)")
VIDEO_RE = re.compile(r"\[Video\]\((?P<url>https://www\.youtube\.com/watch\?v=(?P<id>[A-Za-z0-9_-]{11})[^)]*)\)")
ZULETZT_RE = re.compile(rf"\(zuletzt: \[(?P<titel>[^\]]+)\]\({re.escape(BASEURL)}/lehrveranstaltungen/(?P<slug>[^/)]+)/?\)\)")
YT_ANY_RE = re.compile(r"(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/)([A-Za-z0-9_-]{11})")
HILFE_ANY_RE = re.compile(r"https?://help\.figma\.com/[^\s)\"'>]+")


def assignments_von(fm, body):
    links = re.findall(rf"{re.escape(BASEURL)}/assignments/([A-Za-z0-9_.-]+?)/?\)", fm.get("assignments", ""))
    links += re.findall(rf"{re.escape(BASEURL)}/assignments/([A-Za-z0-9_.-]+?)/?\)", strip_comments(body))
    return list(dict.fromkeys(links))


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# --- Datenmodell -------------------------------------------------------------


def lade_workshops():
    sem, start, ende = semester_zeitraum()
    alle = []
    for p in sorted(LV_DIR.glob("*.md")):
        fm, body, text = parse_frontmatter(p)
        termin = erste_termin(fm.get("termine"))
        relevant = (
            fm.get("typ", "").strip() in TYPEN
            and fm.get("published", "").strip().lower() == "true"
            and termin is not None
            and start <= termin <= ende
        )
        sec = section_bounds(body)
        sec_text = sec.group(1) if sec else None
        entries = []
        if sec_text:
            for m in ENTRY_RE.finditer(sec_text):
                art = ARTIKEL_RE.search(m.group("links"))
                vid = VIDEO_RE.search(m.group("links"))
                entries.append({
                    "label": m.group("label").strip(),
                    "text": m.group("text").strip(),
                    "artikel": art.groupdict() if art else None,
                    "video": vid.groupdict() if vid else None,
                })
        ausserhalb = body if not sec else body[: sec.start()] + body[sec.end():]
        alle.append({
            "datei": p.name,
            "slug": p.stem,
            "titel": fm.get("titel", "").strip(),
            "typ": fm.get("typ", "").strip(),
            "termin": termin,
            "relevant": relevant,
            "section": sec_text,
            "entries": entries,
            "zuletzt": ZULETZT_RE.search(sec_text).groupdict() if sec_text and ZULETZT_RE.search(sec_text) else None,
            "hinweis": bool(sec_text and HINWEIS in sec_text),
            "assignments": assignments_von(fm, body),
            "ausserhalb": strip_comments(ausserhalb) + "\n" + fm.get("material", ""),
            "inhalt_hash": sha(text.replace(sec_text or "", "")),
        })
    relevant = sorted((w for w in alle if w["relevant"]), key=lambda w: w["termin"])
    return sem, relevant, [w for w in alle if not w["relevant"] and w["section"]]


# --- Prüfungen ---------------------------------------------------------------


class Bericht:
    def __init__(self):
        self.fehler, self.warnungen, self.hinweise, self.inhalt = [], [], [], []

    def f(self, w, msg): self.fehler.append(f"**{w}**: {msg}")
    def w(self, w, msg): self.warnungen.append(f"**{w}**: {msg}")
    def h(self, w, msg): self.hinweise.append(f"**{w}**: {msg}")


def pruefe_struktur(ws, sonstige, b):
    vorher_mit_eintraegen = None
    for i, w in enumerate(ws):
        n = w["datei"]
        if w["section"] is None:
            b.f(n, f"Sektion `{SECTION}` fehlt.")
            b.inhalt.append(f"{n}: Sektion neu anlegen")
            continue
        if PFLEGE_KOMMENTAR not in w["section"]:
            b.w(n, f"Kommentar unter der Überschrift fehlt: `{PFLEGE_KOMMENTAR}`")
        if not w["entries"] and not w["hinweis"]:
            b.f(n, "Sektion hat weder Einträge noch den Hinweis „keine neuen Figma-Fertigkeiten“.")
        if w["entries"] and w["hinweis"]:
            b.f(n, "Sektion hat Einträge **und** den Hinweis „keine neuen Figma-Fertigkeiten“.")
        roh = len(re.findall(r"^- \*\*", w["section"], re.M))
        if roh != len(w["entries"]):
            b.f(n, f"{roh - len(w['entries'])} Eintrag/Einträge entsprechen nicht dem Format "
                   "`- **Name:** Text` + eingerückte Linkzeile.")
        if w["entries"]:
            if vorher_mit_eintraegen is None:
                if w["zuletzt"]:
                    b.w(n, "Erste Veranstaltung mit Fertigkeiten, sollte keinen „zuletzt“-Verweis haben.")
            else:
                soll = vorher_mit_eintraegen
                if not w["zuletzt"]:
                    b.f(n, f"Verweis auf vorherige Veranstaltung fehlt (soll: {soll['datei']}).")
                elif w["zuletzt"]["slug"] != soll["slug"]:
                    b.f(n, f"Verweis zeigt auf `{w['zuletzt']['slug']}`, soll `{soll['slug']}` sein.")
                elif w["zuletzt"]["titel"] != soll["titel"]:
                    b.w(n, f"Linktext „{w['zuletzt']['titel']}“ ≠ Titel „{soll['titel']}“.")
            vorher_mit_eintraegen = w
            if not (3 <= len(w["entries"]) <= 7) and i > 0:
                b.h(n, f"{len(w['entries'])} Fertigkeiten (Richtwert 3–7).")
        for e in w["entries"]:
            if not e["artikel"]:
                b.f(n, f"„{e['label']}“: Link zur Figma-Hilfe fehlt.")
            elif (e["artikel"]["loc"] == "de") == bool(e["artikel"]["en"]):
                b.f(n, f"„{e['label']}“: Linktext passt nicht zur Sprache ({e['artikel']['loc']}).")
            ohne_abk = re.sub(r"\b(?:z\. B\.|d\. h\.|u\. a\.|o\. Ä\.|bzw\.|ca\.|etc\.|ggf\.)", "", e["text"])
            saetze = len(re.findall(r"[.!?](?:\s|$)", ohne_abk))
            if saetze > 2:
                b.w(n, f"„{e['label']}“: {saetze} Sätze (Vorgabe 1–2).")
            for muster, grund in STIL_WARNUNGEN.items():
                if muster in e["text"]:
                    b.w(n, f"„{e['label']}“: „{muster.strip()}“ ({grund}).")
    for w in sonstige:
        b.h(w["datei"], "hat eine Figma-Sektion, gehört aber nicht zu den aktuellen Veranstaltungen "
                        "(unveröffentlicht, anderer Typ oder anderes Semester).")


def pruefe_aufbau(ws, b):
    gesehen = {}
    videos, artikel = {}, {}
    for w in ws:
        for e in w["entries"]:
            key = e["label"].lower()
            if key in gesehen:
                b.f(w["datei"], f"„{e['label']}“ steht schon in {gesehen[key]}.")
            else:
                for alt, wo in gesehen.items():
                    if difflib.SequenceMatcher(None, key, alt).ratio() > 0.8:
                        b.w(w["datei"], f"„{e['label']}“ ähnelt „{alt}“ aus {wo}. Wiederholung oder echte Vertiefung?")
                gesehen[key] = w["datei"]
            if e["video"]:
                vid = e["video"]["id"]
                if vid in videos and videos[vid] != w["datei"]:
                    b.w(w["datei"], f"„{e['label']}“: Video {vid} wird schon in {videos[vid]} verwendet.")
                videos.setdefault(vid, w["datei"])
            if e["artikel"]:
                aid = e["artikel"]["id"]
                if aid in artikel and artikel[aid] != w["datei"]:
                    b.h(w["datei"], f"„{e['label']}“: Artikel {aid} wird auch in {artikel[aid]} verlinkt.")
                artikel.setdefault(aid, w["datei"])


def pruefe_assignments(ws, b):
    for w in ws:
        for slug in w["assignments"]:
            if not (AS_DIR / f"{slug}.md").exists():
                b.f(w["datei"], f"Assignment `{slug}` existiert nicht in _assignments/.")


def pruefe_aenderungen(ws, b, sem):
    stand = json.loads(STAND.read_text(encoding="utf-8")) if STAND.exists() else {}
    alt = stand.get("workshops", {})
    if stand and stand.get("semester") != sem:
        b.inhalt.append(f"Semesterwechsel ({stand.get('semester')} → {sem}): komplette Kette neu ableiten")
        alt = {}
    if not stand:
        b.h("Stand", "Noch kein gespeicherter Abgleich. Nach der Prüfung mit `--stand-aktualisieren` speichern.")
    for w in ws:
        s = alt.get(w["datei"])
        if s is None:
            if stand:
                b.inhalt.append(f"{w['datei']}: neu im Semester, Fertigkeiten anhand der Assignments festlegen")
            continue
        gruende = []
        if s.get("inhalt") != w["inhalt_hash"]:
            gruende.append("Workshopseite geändert")
        alt_as = s.get("assignments", {})
        for slug in w["assignments"]:
            p = AS_DIR / f"{slug}.md"
            h = sha(p.read_text(encoding="utf-8")) if p.exists() else None
            if slug not in alt_as:
                gruende.append(f"Assignment `{slug}` neu verknüpft")
            elif alt_as[slug] != h:
                gruende.append(f"Assignment `{slug}` geändert")
        for slug in set(alt_as) - set(w["assignments"]):
            gruende.append(f"Assignment `{slug}` nicht mehr verknüpft")
        if gruende:
            b.inhalt.append(f"{w['datei']}: " + "; ".join(gruende))
    for datei in set(alt) - {w["datei"] for w in ws}:
        b.inhalt.append(f"{datei}: nicht mehr im aktuellen Semester. Prüfen, ob Fertigkeiten in eine andere Veranstaltung wandern müssen")
    letzter = stand.get("geprueft_am")
    return stand, letzter


def speichere_stand(ws, sem, netz):
    data = {
        "semester": sem,
        "geprueft_am": dt.date.today().isoformat(),
        "workshops": {
            w["datei"]: {
                "inhalt": w["inhalt_hash"],
                "assignments": {
                    s: sha((AS_DIR / f"{s}.md").read_text(encoding="utf-8")) if (AS_DIR / f"{s}.md").exists() else None
                    for s in w["assignments"]
                },
            }
            for w in ws
        },
        "artikel_stand": netz.get("artikel_stand", {}),
    }
    STAND.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --- Netzwerkprüfungen -------------------------------------------------------


def hilfe_artikel(loc, aid):
    status, data = http_json(f"https://help.figma.com/api/v2/help_center/{loc}/articles/{aid}.json")
    return status, (data or {}).get("article")


def video_info(vid):
    status, data = http_json(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json")
    info = {"status": status, "oembed": data, "datum": None}
    if status == 200:
        s, html = http_get(f"https://www.youtube.com/watch?v={vid}")
        m = re.search(r'"(?:uploadDate|publishDate)":"(\d{4}-\d{2}-\d{2})', html or "") or \
            re.search(r'itemprop="uploadDate" content="(\d{4}-\d{2}-\d{2})', html or "")
        info["datum"] = m.group(1) if m else None
    return info


def pruefe_netz(ws, b, stand):
    artikel, videos, fremd = {}, {}, {}
    for w in ws:
        for e in w["entries"]:
            if e["artikel"]:
                artikel.setdefault((e["artikel"]["loc"], e["artikel"]["id"]), []).append((w["datei"], e))
            if e["video"]:
                videos.setdefault(e["video"]["id"], []).append((w["datei"], e))
        for vid in set(YT_ANY_RE.findall(w["ausserhalb"])):
            fremd.setdefault(vid, []).append(w["datei"])
        for url in set(HILFE_ANY_RE.findall(w["ausserhalb"])):
            if not any(a in url for a in ERLAUBTE_HILFE_LINKS):
                b.w(w["datei"], f"Figma-Hilfe-Link außerhalb der Sektion: {url}. In die Sektion übernehmen oder entfernen.")

    alt_stand = stand.get("artikel_stand", {})
    neu_stand = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        a_res = dict(zip(artikel, ex.map(lambda k: hilfe_artikel(*k), artikel)))
        de_res = dict(zip(artikel, ex.map(lambda k: hilfe_artikel("de", k[1]) if k[0] != "de" else (None, None), artikel)))
        v_res = dict(zip(videos, ex.map(video_info, videos)))
        f_res = dict(zip(fremd, ex.map(lambda v: http_json(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json"), fremd)))

    for (loc, aid), wo in artikel.items():
        status, art = a_res[(loc, aid)]
        for datei, e in wo:
            if status is None:
                b.w(datei, f"„{e['label']}“: Figma-Hilfe nicht erreichbar ({art}).")
            elif status != 200 or not art:
                b.f(datei, f"„{e['label']}“: Artikel {aid} ({loc}) nicht mehr vorhanden (HTTP {status}).")
            else:
                edited = (art.get("edited_at") or art.get("updated_at") or "")[:10]
                neu_stand[f"{loc}/{aid}"] = edited
                vorher = alt_stand.get(f"{loc}/{aid}")
                if vorher and edited and edited > vorher:
                    b.h(datei, f"„{e['label']}“: Artikel „{art['title']}“ wurde am {edited} überarbeitet. Passt der Text noch?")
                d_status, d_art = de_res[(loc, aid)]
                if loc != "de" and d_status == 200 and d_art:
                    b.w(datei, f"„{e['label']}“: Deutsche Fassung jetzt verfügbar: {d_art['html_url']}")
    for vid, wo in videos.items():
        info = v_res[vid]
        oe = info["oembed"] or {}
        for datei, e in wo:
            if info["status"] is None:
                b.w(datei, f"„{e['label']}“: YouTube nicht erreichbar.")
            elif info["status"] != 200:
                b.f(datei, f"„{e['label']}“: Video {vid} nicht mehr verfügbar (HTTP {info['status']}).")
            elif (oe.get("author_url") or "").lower() != FIGMA_CHANNEL:
                b.f(datei, f"„{e['label']}“: Video {vid} stammt von „{oe.get('author_name')}“, nicht von Figma.")
            else:
                if re.search(r"older version|outdated|veraltet", oe.get("title", ""), re.I):
                    b.w(datei, f"„{e['label']}“: Video „{oe['title']}“ ist als veraltet markiert.")
                if info["datum"]:
                    jahre = (dt.date.today() - dt.date.fromisoformat(info["datum"])).days / 365.25
                    if jahre > VIDEO_MAX_JAHRE:
                        b.h(datei, f"„{e['label']}“: Video „{oe['title']}“ ist von {info['datum'][:4]} "
                                   f"({jahre:.0f} Jahre alt), die Oberfläche hat sich vermutlich verändert. Neueres Video suchen?")
    for vid, dateien in fremd.items():
        status, oe = f_res[vid]
        autor = (oe or {}).get("author_name")
        author_url = ((oe or {}).get("author_url") or "").lower()
        for datei in dateien:
            if status != 200:
                b.w(datei, f"Video {vid} außerhalb der Sektion ist nicht mehr verfügbar (HTTP {status}).")
            elif author_url == FIGMA_CHANNEL:
                b.w(datei, f"Figma-Video {vid} („{oe.get('title')}“) außerhalb der Sektion. In die Sektion übernehmen?")
            elif autor not in ERLAUBTE_KANAELE:
                b.w(datei, f"Fremdvideo {vid} von „{autor}“ („{oe.get('title')}“). Falls es ein Figma-Tutorial ist: entfernen.")
    return {"artikel_stand": {**alt_stand, **neu_stand}}


# --- Ausgabe -----------------------------------------------------------------


def ausgabe(sem, ws, b, letzter, offline):
    print(f"# Figma-Fertigkeiten: Prüfbericht\n")
    print(f"Semester: {sem} · letzter Abgleich: {letzter or '–'} · Netzwerkprüfung: {'aus' if offline else 'an'}\n")
    print("## Reihenfolge und Fertigkeiten\n")
    print("| Datum | Datei | Titel | Fertigkeiten |\n|---|---|---|---|")
    for w in ws:
        if w["section"] is None:
            f = "⚠️ keine Sektion"
        elif w["hinweis"]:
            f = "– (Hinweis)"
        else:
            f = ", ".join(e["label"] for e in w["entries"])
        print(f"| {w['termin']:%d.%m.%Y} | {w['datei']} | {w['titel']} | {f} |")
    for titel, liste in [("Inhaltlich zu prüfen", b.inhalt), ("Fehler", b.fehler),
                         ("Warnungen", b.warnungen), ("Hinweise", b.hinweise)]:
        print(f"\n## {titel} ({len(liste)})\n")
        print("\n".join(f"- {x}" for x in liste) if liste else "Keine.")


# --- Recherche-Helfer --------------------------------------------------------


def suche_hilfe(begriffe):
    q = " ".join(begriffe)
    for loc in ("de", "en-us"):
        status, data = http_json("https://help.figma.com/api/v2/help_center/articles/search.json?"
                                 + urllib.parse.urlencode({"query": q, "locale": loc, "per_page": 8}))
        print(f"## Figma-Hilfe ({loc}): {q}")
        for a in (data or {}).get("results", []):
            yt = sorted(set(YT_ANY_RE.findall(a.get("body") or "")))
            print(f"- {a['title']}\n  {a['html_url']}\n  eingebettete Videos: {', '.join(yt) or '–'}")
        print()


def suche_video(begriffe):
    q = " ".join(begriffe)
    status, html = http_get("https://www.youtube.com/@Figma/search?" + urllib.parse.urlencode({"query": q}))
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html or "")
    print(f"## Kanal @Figma: {q}")
    if not m:
        print("Keine Daten (YouTube-Seite hat sich ggf. geändert).")
        return

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                yield o["videoRenderer"]
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)
    for v in list(walk(json.loads(m.group(1))))[:12]:
        t = "".join(r.get("text", "") for r in v["title"].get("runs", []))
        print(f"- {v['videoId']} | {t} | {v.get('lengthText', {}).get('simpleText', '')} | "
              f"{v.get('publishedTimeText', {}).get('simpleText', '')}")


def pruefe_video(ids):
    for vid in ids:
        info = video_info(vid)
        oe = info["oembed"] or {}
        ok = (oe.get("author_url") or "").lower() == FIGMA_CHANNEL
        print(f"- {vid} | HTTP {info['status']} | {oe.get('author_name')} {'✓' if ok else '✗ nicht Figma'} | "
              f"{oe.get('title')} | {info['datum'] or 'Datum unbekannt'}")


# --- Main --------------------------------------------------------------------


def main(argv):
    if argv and argv[0] == "suche-hilfe":
        return suche_hilfe(argv[1:])
    if argv and argv[0] == "suche-video":
        return suche_video(argv[1:])
    if argv and argv[0] == "pruefe-video":
        return pruefe_video(argv[1:])
    offline = "--offline" in argv
    sem, ws, sonstige = lade_workshops()
    b = Bericht()
    pruefe_struktur(ws, sonstige, b)
    pruefe_aufbau(ws, b)
    pruefe_assignments(ws, b)
    stand, letzter = pruefe_aenderungen(ws, b, sem)
    netz = {"artikel_stand": stand.get("artikel_stand", {})} if offline else pruefe_netz(ws, b, stand)
    ausgabe(sem, ws, b, letzter, offline)
    if "--stand-aktualisieren" in argv:
        speichere_stand(ws, sem, netz)
        print(f"\nStand gespeichert: {STAND.relative_to(REPO)}")
    return 1 if b.fehler else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
