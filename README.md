# Infos rund um das Modul "Screendesign" im Studiengang Medieninformatik Bachelor

- Verantwortlicher Dozent: Christian Noss // http://www.christiannoss.de
- https://th-koeln.github.io/mi-bachelor-screendesign

# Figma-Fertigkeiten pflegen

Jeder Workshop und jedes Training des laufenden Semesters (`_lehrveranstaltungen/`) hat eine Sektion **„Figma-Fertigkeiten“**. Dort stehen die Figma-Fertigkeiten, die für die verknüpften Assignments neu dazukommen, jeweils mit einem Link zur Figma-Hilfe und einem Video vom offiziellen Figma-YouTube-Kanal. Die Sektionen bauen chronologisch aufeinander auf, und keine Fertigkeit wird wiederholt.

Gepflegt werden die Sektionen mit dem Claude-Code-Skill **`/figma-fertigkeiten`**. Er liegt unter [`.claude/skills/figma-fertigkeiten/`](.claude/skills/figma-fertigkeiten/).

**Aufruf:** Claude Code im Repo starten und `/figma-fertigkeiten` eingeben (oder „Aktualisiere die Figma-Fertigkeiten“). Claude prüft alles, schlägt Änderungen vor und committet erst nach Freigabe.

**Wann:**
- nach Änderungen an Workshops oder Assignments
- bei neuen oder verschobenen Terminen
- zum Semesterwechsel (`semester:` in `_config.yml`)
- ab und zu, um tote Links zu finden

**Was geprüft wird:**
- welche Workshops und Assignments sich seit dem letzten Abgleich geändert haben
- ob Figma-Hilfe-Artikel und Videos noch existieren, vom Kanal @Figma stammen und aktuell sind
- ob die Fertigkeiten aufeinander aufbauen, ohne Doppelungen

**Ohne Claude:** Den Prüfbericht gibt es auch direkt im Terminal (Python 3, keine Installation nötig):

```bash
python3 .claude/skills/figma-fertigkeiten/check.py            # Prüfbericht
python3 .claude/skills/figma-fertigkeiten/check.py --offline  # ohne Link-Prüfung
```

**Dateien im Skill-Ordner:**

| Datei | Inhalt |
|---|---|
| `SKILL.md` | Ablauf und alle Regeln (Umfang, Platzierung, Format, Quellen, Stil der Texte) |
| `check.py` | Prüfskript und Suche in Figma-Hilfe und auf dem Kanal @Figma (`check.py suche <Begriffe>`) |
| `stand.json` | Prüfsummen vom letzten Abgleich, wird vom Skript geschrieben (nicht von Hand bearbeiten) |
