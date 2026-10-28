#!/usr/bin/env python3
"""Prüft die Sektionen „## Figma-Fertigkeiten“ in _lehrveranstaltungen/.

Aufruf aus dem Repo-Root:
  python3 .claude/skills/figma-fertigkeiten/check.py                        Prüfbericht
  python3 .claude/skills/figma-fertigkeiten/check.py --offline              ohne Link- und Videoprüfung
  python3 .claude/skills/figma-fertigkeiten/check.py --stand-aktualisieren  Abgleich als erledigt speichern
  python3 .claude/skills/figma-fertigkeiten/check.py suche <Begriffe>       Figma-Hilfe und Kanal @Figma durchsuchen
"""
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
STAND = Path(__file__).with_name("stand.json")
HINWEIS = "Für diese Übungen werden keine neuen Figma-Fertigkeiten benötigt."
KOMMENTAR = "{% comment %}Gepflegt mit dem Claude-Code-Skill /figma-fertigkeiten, siehe README.md{% endcomment %}"
FIGMA_KANAL = "https://www.youtube.com/@figma"
VIDEO_MAX_JAHRE = 5

SEKTION_RE = re.compile(r"^## Figma-Fertigkeiten\n.*?(?=^## |^<!--|\Z)", re.S | re.M)
EINTRAG_RE = re.compile(r"^- \*\*(.+?):\*\* .+\n  (.+)$", re.M)
ARTIKEL_RE = re.compile(r"\[Figma-Hilfe( \(englisch\))?\]\(https://help\.figma\.com/hc/([a-z-]+)/articles/(\d+)")
VIDEO_RE = re.compile(r"\[Video\]\(https://www\.youtube\.com/watch\?v=([\w-]{11})")

BERICHT = {"Inhaltlich zu prüfen": [], "Fehler": [], "Warnungen": [], "Hinweise": []}


def melde(art, datei, text):
    BERICHT[art].append(f"**{datei}**: {text}")


def get(url):
    """Lädt eine URL. Gibt (HTTP-Status, Text) zurück, Status None bei Netzwerkfehler."""
    anfrage = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(anfrage, timeout=30) as antwort:
            return antwort.status, antwort.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as fehler:
        return fehler.code, ""
    except OSError:
        return None, ""


def feld(text, name):
    """Liest ein einzeiliges Feld wie „typ: workshop“ aus Frontmatter oder _config.yml."""
    m = re.search(rf"^{name}:[ \t]*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def pruefsumme(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def semester():
    """Name und Zeitraum des Semesters aus _config.yml (WS: Sep–Mär, SS: Apr–Aug)."""
    name = feld((REPO / "_config.yml").read_text(encoding="utf-8"), "semester")
    jahr = int(re.search(r"\d{4}", name).group())
    if name.startswith("Winter"):
        return name, dt.date(jahr, 9, 1), dt.date(jahr + 1, 3, 31)
    return name, dt.date(jahr, 4, 1), dt.date(jahr, 8, 31)


def lade_veranstaltungen():
    """Liest alle Lehrveranstaltungen mit frühestem Termin, Figma-Sektion und Assignments."""
    alle = []
    for pfad in sorted((REPO / "_lehrveranstaltungen").glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        termine = re.findall(r"(\d{4}-\d{2}-\d{2})(?: (\d{1,2}:\d{2}))?", feld(text, "termine"))
        sektion = SEKTION_RE.search(text)
        sektion = sektion.group() if sektion else None
        # Assignments stehen im Frontmatter-Feld „assignments“, selten auch als Link im Body.
        block = re.search(r"^assignments: \|\n((?:[ \t]+.*\n)*)", text, re.M)
        body = re.sub(r"<!--.*?-->", "", text.split("\n---\n", 1)[-1], flags=re.S)
        links = re.findall(r"/assignments/([\w.-]+?)/?\)", (block.group(1) if block else "") + body)
        alle.append({
            "datei": pfad.name,
            "typ": feld(text, "typ"),
            "published": feld(text, "published") == "true",
            "termin": min((dt.datetime.fromisoformat(f"{d} {(t or '0:00').zfill(5)}") for d, t in termine),
                          default=None),
            "text": text,
            "sektion": sektion,
            "eintraege": [(m.group(1), ARTIKEL_RE.search(m.group(2)), VIDEO_RE.search(m.group(2)))
                          for m in EINTRAG_RE.finditer(sektion or "")],
            "assignments": list(dict.fromkeys(links)),
        })
    return alle


def pruefe_sektionen(aktuell, sonstige):
    """Sektion vorhanden, Format korrekt, keine Verweise, keine doppelten Fertigkeiten."""
    gesehen = {}
    for v in aktuell:
        d, s = v["datei"], v["sektion"]
        for slug in v["assignments"]:
            if not (REPO / "_assignments" / f"{slug}.md").exists():
                melde("Fehler", d, f"Assignment `{slug}` existiert nicht.")
        if s is None:
            melde("Fehler", d, "Sektion „Figma-Fertigkeiten“ fehlt.")
            continue
        if KOMMENTAR not in s:
            melde("Warnungen", d, "Kommentar mit dem Hinweis auf den Skill fehlt unter der Überschrift.")
        if bool(v["eintraege"]) == (HINWEIS in s):
            melde("Fehler", d, "Sektion braucht entweder Einträge oder den Hinweis „keine neuen Figma-Fertigkeiten“.")
        if len(re.findall(r"^- \*\*", s, re.M)) != len(v["eintraege"]):
            melde("Fehler", d, "Ein Eintrag hat nicht das Format `- **Name:** Text` mit eingerückter Linkzeile.")
        if "/lehrveranstaltungen/" in s:
            melde("Fehler", d, "Sektion verlinkt auf eine andere Veranstaltung. Solche Verweise entfernen.")
        for name, artikel, _ in v["eintraege"]:
            if not artikel:
                melde("Fehler", d, f"„{name}“: Link zur Figma-Hilfe fehlt.")
            elif (artikel.group(2) == "de") == bool(artikel.group(1)):
                melde("Fehler", d, f"„{name}“: Linktext passt nicht zur Sprache des Artikels.")
            if name.lower() in gesehen:
                melde("Fehler", d, f"„{name}“ steht schon in {gesehen[name.lower()]}.")
            gesehen.setdefault(name.lower(), d)
    for v in sonstige:
        melde("Hinweise", v["datei"], "Hat eine Figma-Sektion, gehört aber nicht (mehr) zu den Veranstaltungen des Semesters.")


def pruefsummen(aktuell):
    """Prüfsummen der Workshopseiten (ohne Figma-Sektion) und ihrer Assignments."""
    summen = {}
    for v in aktuell:
        summen[f"_lehrveranstaltungen/{v['datei']}"] = pruefsumme(SEKTION_RE.sub("", v["text"]))
        for slug in v["assignments"]:
            pfad = REPO / "_assignments" / f"{slug}.md"
            if pfad.exists():
                summen[f"_assignments/{slug}.md"] = pruefsumme(pfad.read_text(encoding="utf-8"))
    return summen


def pruefe_aenderungen(aktuell, sem):
    """Vergleicht mit dem Stand des letzten Abgleichs aus stand.json."""
    if not STAND.exists():
        melde("Hinweise", "stand.json", "Noch kein Abgleich gespeichert.")
        return
    stand = json.loads(STAND.read_text(encoding="utf-8"))
    if stand.get("semester") != sem:
        melde("Inhaltlich zu prüfen", "Semesterwechsel", f"{stand.get('semester')} → {sem}: alle Fertigkeiten neu ableiten.")
        return
    alt, neu = stand.get("pruefsummen", {}), pruefsummen(aktuell)
    for v in aktuell:
        seite = f"_lehrveranstaltungen/{v['datei']}"
        gruende = ["neu im Semester"] if seite not in alt else ["Workshopseite geändert"] if alt[seite] != neu[seite] else []
        gruende += [f"Assignment `{s}` geändert oder neu verknüpft" for s in v["assignments"]
                    if alt.get(f"_assignments/{s}.md") != neu.get(f"_assignments/{s}.md")]
        if gruende:
            melde("Inhaltlich zu prüfen", v["datei"], "; ".join(gruende))


def speichere_stand(aktuell, sem):
    stand = {"semester": sem, "abgeglichen_am": dt.date.today().isoformat(), "pruefsummen": pruefsummen(aktuell)}
    STAND.write_text(json.dumps(stand, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def artikel_info(schluessel):
    """HTTP-Status eines Artikels und, falls er englisch ist, die URL einer deutschen Fassung."""
    sprache, nr = schluessel
    status, _ = get(f"https://help.figma.com/api/v2/help_center/{sprache}/articles/{nr}.json")
    deutsch = None
    if status == 200 and sprache != "de":
        s, text = get(f"https://help.figma.com/api/v2/help_center/de/articles/{nr}.json")
        deutsch = json.loads(text)["article"]["html_url"] if s == 200 else None
    return status, deutsch


def video_info(nr):
    """HTTP-Status, Kanal, Titel und Upload-Datum eines YouTube-Videos."""
    status, text = get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={nr}&format=json")
    if status != 200:
        return status, None, None, None
    oembed = json.loads(text)
    _, seite = get(f"https://www.youtube.com/watch?v={nr}")
    datum = re.search(r'"(?:uploadDate|publishDate)":"(\d{4}-\d{2}-\d{2})', seite)
    return status, oembed["author_url"].lower(), oembed["title"], datum and datum.group(1)


def pruefe_links(aktuell):
    """Figma-Hilfe-Artikel und Videos: noch vorhanden, von Figma, aktuell."""
    artikel, videos = {}, {}
    for v in aktuell:
        for name, a, vid in v["eintraege"]:
            if a:
                artikel.setdefault((a.group(2), a.group(3)), []).append((v["datei"], name))
            if vid:
                videos.setdefault(vid.group(1), []).append((v["datei"], name))
    with ThreadPoolExecutor(8) as pool:
        a_info = dict(zip(artikel, pool.map(artikel_info, artikel)))
        v_info = dict(zip(videos, pool.map(video_info, videos)))
    for schluessel, stellen in artikel.items():
        status, deutsch = a_info[schluessel]
        for d, name in stellen:
            if status is None:
                melde("Warnungen", d, f"„{name}“: Figma-Hilfe nicht erreichbar.")
            elif status != 200:
                melde("Fehler", d, f"„{name}“: Artikel nicht mehr vorhanden (HTTP {status}).")
            elif deutsch:
                melde("Warnungen", d, f"„{name}“: Deutsche Fassung verfügbar: {deutsch}")
    for nr, stellen in videos.items():
        status, kanal, titel, datum = v_info[nr]
        for d, name in stellen:
            if status is None:
                melde("Warnungen", d, f"„{name}“: YouTube nicht erreichbar.")
            elif status != 200:
                melde("Fehler", d, f"„{name}“: Video {nr} nicht mehr verfügbar (HTTP {status}).")
            elif kanal != FIGMA_KANAL:
                melde("Fehler", d, f"„{name}“: Video {nr} stammt nicht vom Kanal @Figma.")
            elif "older version" in titel.lower():
                melde("Warnungen", d, f"„{name}“: Figma hat das Video „{titel}“ als veraltet markiert.")
            elif datum and (dt.date.today() - dt.date.fromisoformat(datum)).days > VIDEO_MAX_JAHRE * 365:
                melde("Hinweise", d, f"„{name}“: Video „{titel}“ ist von {datum[:4]}. Gibt es ein neueres?")


def finde(daten, schluessel):
    """Sucht rekursiv alle Werte zu einem Schlüssel in verschachteltem JSON."""
    if isinstance(daten, dict):
        if schluessel in daten:
            yield daten[schluessel]
        for wert in daten.values():
            yield from finde(wert, schluessel)
    elif isinstance(daten, list):
        for wert in daten:
            yield from finde(wert, schluessel)


def suche(begriffe):
    """Durchsucht die Figma-Hilfe (deutsch und englisch) und den YouTube-Kanal @Figma."""
    q = " ".join(begriffe)
    for sprache in ("de", "en-us"):
        _, text = get("https://help.figma.com/api/v2/help_center/articles/search.json?"
                      + urllib.parse.urlencode({"query": q, "locale": sprache, "per_page": 6}))
        print(f"## Figma-Hilfe ({sprache}): {q}")
        for a in json.loads(text or "{}").get("results", []):
            eingebettet = sorted(set(re.findall(r"youtube(?:-nocookie)?\.com/embed/([\w-]{11})", a["body"] or "")))
            print(f"- {a['title']}: {a['html_url']}" + (f" (Video: {', '.join(eingebettet)})" if eingebettet else ""))
    _, seite = get("https://www.youtube.com/@Figma/search?" + urllib.parse.urlencode({"query": q}))
    daten = re.search(r"var ytInitialData = (\{.*?\});</script>", seite)
    print(f"## Kanal @Figma: {q}")
    for v in list(finde(json.loads(daten.group(1)) if daten else {}, "videoRenderer"))[:10]:
        titel = "".join(r["text"] for r in v["title"]["runs"])
        print(f"- {v['videoId']}: {titel} ({v.get('publishedTimeText', {}).get('simpleText', '?')})")


def ausgabe(sem, aktuell, offline):
    print(f"# Figma-Fertigkeiten: {sem}" + (" (ohne Link-Prüfung)" if offline else "") + "\n")
    print("| Termin | Datei | Neue Fertigkeiten |\n|---|---|---|")
    for v in aktuell:
        if v["sektion"] is None:
            inhalt = "**Sektion fehlt**"
        elif not v["eintraege"]:
            inhalt = "keine (Hinweis)"
        else:
            inhalt = ", ".join(name for name, _, _ in v["eintraege"])
        print(f"| {v['termin']:%d.%m.%Y} | {v['datei']} | {inhalt} |")
    for art, zeilen in BERICHT.items():
        print(f"\n## {art} ({len(zeilen)})\n")
        print("\n".join(f"- {z}" for z in zeilen) or "Keine.")


def main(args):
    if args[:1] == ["suche"]:
        return suche(args[1:])
    sem, start, ende = semester()
    alle = lade_veranstaltungen()
    aktuell = sorted((v for v in alle if v["typ"] in ("workshop", "training") and v["published"]
                      and v["termin"] and start <= v["termin"].date() <= ende), key=lambda v: v["termin"])
    pruefe_sektionen(aktuell, [v for v in alle if v["sektion"] and v not in aktuell])
    pruefe_aenderungen(aktuell, sem)
    if "--offline" not in args:
        pruefe_links(aktuell)
    ausgabe(sem, aktuell, "--offline" in args)
    if "--stand-aktualisieren" in args:
        speichere_stand(aktuell, sem)
        print(f"\nStand gespeichert: {STAND.relative_to(REPO)}")
    return 1 if BERICHT["Fehler"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
