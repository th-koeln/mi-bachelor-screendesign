---
name: figma-fertigkeiten
description: Prüft und aktualisiert die Sektionen „## Figma-Fertigkeiten“ in den Workshops und Trainings unter _lehrveranstaltungen. Gleicht sie mit Workshopinhalten und Assignments ab, prüft Figma-Hilfe-Artikel und YouTube-Videos auf Verfügbarkeit und Aktualität und kontrolliert, ob die Fertigkeiten von Workshop zu Workshop aufeinander aufbauen. Verwenden bei „Figma-Fertigkeiten aktualisieren/prüfen“, nach Änderungen an Workshops oder Assignments, bei neuen Terminen oder zum Semesterwechsel.
---

# Figma-Fertigkeiten pflegen

Jede Veranstaltung des laufenden Semesters hat eine Sektion `## Figma-Fertigkeiten`. Dort stehen nur die Figma-Fertigkeiten, die für ihre Assignments **neu** dazukommen. Die Sektionen bauen chronologisch aufeinander auf.

Das Prüfskript `check.py` erledigt die mechanischen Prüfungen:
- Reihenfolge der Veranstaltungen im Semester
- Sektion vorhanden, Format korrekt, keine Verweise auf andere Veranstaltungen, keine doppelten Fertigkeitsnamen
- Artikel und Videos noch vorhanden, Videos vom Kanal @Figma, Alter der Videos, neue deutsche Fassungen
- welche Workshopseiten und Assignments sich seit dem letzten Abgleich geändert haben

Deine Aufgabe ist alles, was Urteilsvermögen braucht: Fertigkeiten aus den Assignments ableiten, den Aufbau inhaltlich prüfen und die Texte schreiben.

```bash
python3 .claude/skills/figma-fertigkeiten/check.py                       # Prüfbericht (ca. 10 s, mit Netzwerk)
python3 .claude/skills/figma-fertigkeiten/check.py --offline             # ohne Link- und Videoprüfung
python3 .claude/skills/figma-fertigkeiten/check.py --stand-aktualisieren # Abgleich als erledigt speichern
python3 .claude/skills/figma-fertigkeiten/check.py suche <Begriffe>      # Figma-Hilfe (de + en) und Kanal @Figma durchsuchen
```

`stand.json` speichert Prüfsummen der Workshopseiten (ohne die Figma-Sektion) und ihrer Assignments vom letzten Abgleich. Daraus erzeugt der Bericht die Liste **„Inhaltlich zu prüfen“**.

## Ablauf

1. **Bericht erzeugen** mit `check.py` und dem Nutzer die Übersicht der Fehler, Warnungen und „Inhaltlich zu prüfen“ zeigen.
2. **Inhaltlich prüfen**, für jeden Eintrag unter „Inhaltlich zu prüfen“ und jede Datei ohne Sektion:
   - Workshopseite und alle verknüpften Assignments lesen. Verknüpft sind sie über `assignments:` im Frontmatter, manchmal auch über Links im Body.
   - Ermitteln, welche Figma-Fertigkeiten die Assignments brauchen oder spürbar erleichtern.
   - Mit der Übersichtstabelle abgleichen: Was schon früher vorkommt, entfällt. Was fehlt, kommt in die **früheste** Veranstaltung, in der es sinnvoll ist. Dafür darf eine Fertigkeit auch in einen früheren Workshop verschoben werden.
   - Ändert sich die Reihenfolge oder kommt eine Veranstaltung hinzu bzw. fällt weg, die ganze Kette ab dieser Stelle neu durchgehen.
   - Material-Liste und Body der Workshopseite auf Figma-Tutorials und help.figma.com-Links außerhalb der Sektion prüfen (siehe Regeln unter „Quellen“).
3. **Aufbau prüfen**, auch wenn das Skript nichts meldet. Die Übersichtstabelle chronologisch durchgehen und fragen:
   - Braucht ein späteres Assignment eine Fertigkeit, die nirgends vorher eingeführt wird?
   - Kommt eine Fertigkeit unter anderem Namen doppelt vor?
   - Steht etwas zu spät, obwohl es früher schon helfen würde? Beispiel: Ebenen benennen gehört in Figma Basics, weil der Frame-Name beim Export zum Dateinamen wird.
   - Ergebnisse dem Nutzer als Vorschlag vorlegen, bevor du Fertigkeiten verschiebst.
4. **Fehler und Warnungen beheben:**
   - Defekte oder fremde Links durch Treffer aus `suche` ersetzen. Neue Links werden beim nächsten Lauf von `check.py` mitgeprüft.
   - Meldet das Skript eine deutsche Fassung, den Link auf `hc/de/…` umstellen und das „(englisch)“ im Linktext streichen.
5. **Hinweise auf alte Videos:** Nur ersetzen, wenn es ein neueres @Figma-Video zum selben Thema gibt. Sonst bleibt das alte Video stehen.
6. **Stil prüfen:** Das Skript prüft den Stil nicht. Alle neuen und geänderten Texte selbst gegen die Regeln unter „Stil der Texte“ lesen.
7. **Abschließen:**
   - `check.py` erneut ausführen, bis keine Fehler mehr da sind.
   - `jekyll build -d <Scratchpad>/site` muss fehlerfrei durchlaufen.
   - Dem Nutzer die Änderungen zusammenfassen und den Diff zur Freigabe vorlegen.
   - Nach der Freigabe `--stand-aktualisieren` ausführen und `stand.json` mitcommitten. Commit nach Conventional Commits, z. B. `docs(lehrveranstaltungen): Figma-Fertigkeiten aktualisieren`.

Ändert sich `semester:` in `_config.yml`, ist das ein **Semesterwechsel**. Dann sind alle Veranstaltungen neu, und die komplette Kette wird von vorne abgeleitet.

## Regeln

### Umfang
- Betroffen sind veröffentlichte Lehrveranstaltungen (`published: true`) mit `typ: workshop` oder `typ: training`, deren früheste Angabe in `termine` im Semester aus `_config.yml` liegt. Das Wintersemester reicht von September bis März, das Sommersemester von April bis August.
- Die Reihenfolge ergibt sich aus dem frühesten Termin.
- Gezählt wird nur Figma Design, FigJam und Miro zählen nicht.
- Veranstaltungen ohne neue Fertigkeiten bekommen trotzdem die Sektion, und zwar nur mit dem Satz:
  `Für diese Übungen werden keine neuen Figma-Fertigkeiten benötigt.`

### Auswahl
- Eine Fertigkeit entspricht ungefähr einem Help-Center-Artikel. Richtwert sind 3–7 neue Fertigkeiten pro Veranstaltung, Figma Basics darf mehr haben.
- Jede Fertigkeit steht genau einmal. Eine Vertiefung ist nur bei einem wirklich neuen Aspekt erlaubt und braucht einen eigenen, unterscheidbaren Namen.
- Eine Fertigkeit kommt dorthin, wo sie zum ersten Mal **sinnvoll** ist, nicht erst dorthin, wo sie zwingend gebraucht wird.

### Platzierung und Format
- Die Sektion `## Figma-Fertigkeiten` steht im Markdown-Body direkt nach `## Was muss ich mitbringen?`. Fehlt dieser Abschnitt, steht sie vor `## Upload`/`## Uploads`, sonst am Ende vor auskommentierten Blöcken.
- Direkt unter der Überschrift steht immer dieser Liquid-Kommentar. Er wird nicht gerendert und weist Bearbeiter:innen auf den Skill hin:
  ```
  {% comment %}Gepflegt mit dem Claude-Code-Skill /figma-fertigkeiten, siehe README.md{% endcomment %}
  ```
- Einleitung ab der zweiten Veranstaltung mit Fertigkeiten, **ohne** Link auf vorherige Veranstaltungen:
  ```
  Hier stehen nur die Figma-Fertigkeiten, die neu dazukommen. Alles andere kennen Sie bereits aus den vorherigen Veranstaltungen.
  ```
- Eintrag:
  ```
  - **Name der Fertigkeit:** Ein bis zwei Sätze.
    [Figma-Hilfe](https://help.figma.com/hc/de/articles/…) · [Video](https://www.youtube.com/watch?v=…)
  ```
  Bei englischen Artikeln lautet der Linktext `[Figma-Hilfe (englisch)]`. Gibt es kein passendes Video, entfällt ` · [Video](…)`.

### Quellen
- Artikel stammen ausschließlich aus `help.figma.com`, und zwar die deutsche Fassung (`hc/de`), wenn es sie gibt, sonst die englische (`hc/en-us`).
- Videos stammen ausschließlich vom YouTube-Kanal **@Figma**. Verlinkt wird immer ein einzelnes Video, nie eine Playlist. Zeitstempel (`&t=…`) sind erlaubt.
- Außerhalb der Sektion haben Figma-Tutorials (YouTube) und help.figma.com-Links nichts zu suchen. Sinnvolle Figma-Quellen wandern in die Sektion, Fremd-Tutorials werden entfernt.
- Erlaubt bleiben außerhalb der Sektion:
  - eigene Kursvideos (Kanäle `mikoeln`, `Christian Noss`)
  - Plugin-Links und Figma-Dateien/Vorlagen
  - der Link zum Education Plan
- Assignments werden nicht verändert.

### Stil der Texte
Die Texte sollen nach den Lehrenden klingen und nicht generiert wirken.
- Die Studierenden werden gesiezt, wie auf der übrigen Seite.
- Ein bis zwei kurze Sätze in Alltagsdeutsch, möglichst mit konkretem Bezug zum Assignment, z. B. „bei bis zu 120 Linien pro Zelle …“.
- Funktionsnamen bleiben englisch wie in der Figma-Oberfläche: Auto Layout, Fills, Smart Animate.
- Vermeiden:
  - Gedankenstriche im Text
  - Floskeln wie „nahtlos“ oder „Das spart Zeit“
  - Handbuchdeutsch wie „Rechtsklick-Menü“, besser „mit der rechten Maustaste“
  - gleichförmige Satzanfänge wie „So …“ oder „Damit …“
- Tastenkürzel nur angeben, wenn sie in der Figma-Hilfe stehen oder sicher bekannt sind. Format: `<kbd>Cmd</kbd>/<kbd>Strg</kbd> + <kbd>D</kbd>`.
