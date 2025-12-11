---
titel: Struktur und Daten – Die Anatomie von Veranstaltungen
tags: 
  - Analyse
  - WS2526
raum: 3.109
icon: 🎨
published: true
---

<div class="is-important">

Ziel dieses Workshops ist es, die inhaltliche und technische Struktur von Lehrveranstaltungen und ihrer Datenmodelle zu verstehen. Die Teilnehmenden sollen erarbeiten, welche Daten hinter dem System stehen, wie diese miteinander verknüpft sind und welche Auswirkungen dies auf die Gestaltung des Interfaces hat.

Im Zentrum stehen Fragen wie: Was ist eine Veranstaltung? Wie setzt sich eine Veranstaltung zusammen? Welche Bestandteile (z. B. Vorlesung, Übung, Praktikum) sind unterscheidbar, wie werden sie dargestellt? Wie hängen Veranstaltungen mit Modulen, Räumen, Zeiten, Formaten oder Lehrpersonen zusammen?

Darüber hinaus wird thematisiert, welche Funktionen sich aus diesen Strukturen ergeben (z. B. Terminwahl, Filterbarkeit, Pinnen) und welche Begriffe im Interface verwendet werden sollten, um das System nachvollziehbar zu kommunizieren.

</div>

<div class="is-medium">


### Erforderliche Schritte

#### Erarbeitung eines strukturellen Grundverständnisses
Zu Beginn werden gemeinsam zentrale Begriffe definiert: Was versteht das System unter einer Veranstaltung, einem Modul, einem Termin, einem Format? Welche Datenfelder gibt es typischerweise? Was ist ein Pflichtbestandteil, was optional?

#### Entwicklung eines vereinfachten Datenmodells
Die Teilnehmenden modellieren die grundlegende Datenstruktur anhand realer Beispiele oder typischer Kombinationen: Eine Veranstaltung kann aus mehreren Terminen bestehen, Termine können verschiedenen Formaten zugeordnet sein, Räume sind verbunden mit Zeitfenstern etc. Ziel ist ein visuell verständliches Modell, das die Systematik nachvollziehbar macht.

#### Mapping der Daten auf Interface-Komponenten
Die modellierten Datenstrukturen werden exemplarisch auf UI-Elemente übertragen: Welche Informationen gehören in eine Wochenansicht, welche in eine Detailansicht? Wo werden Daten aktiv verändert (z. B. Terminwahl), wo passiv rezipiert?

#### Funktionsrahmen klären
Aus der Datenstruktur und den identifizierten Nutzungsszenarien leiten die Gruppen mögliche Funktionen ab. Diese werden priorisiert (z. B. notwendig, optional) und hinsichtlich ihrer Umsetzbarkeit diskutiert.

#### Begriffsarbeit und Benennung
Zum Abschluss wird diskutiert, wie Daten und Funktionen im Interface sprachlich bezeichnet werden sollen. Begriffe wie „Veranstaltung“, „Termin“, „Block“ oder „Übersicht“ werden auf Verständlichkeit und Konsistenz geprüft. Ziel ist eine erste Sammlung von benutzerzentrierten Bezeichnungen.

### Ergebnis

* Visualisierte Datenstruktur (vereinfachtes Veranstaltungsmodell)
* Zuordnung der Daten zu typischen UI-Komponenten (z. B. Listen, Kalender, Detailansichten)
* Priorisierte Funktionsliste als Grundlage für die Konzeptionsphase
* Erste Version eines projektspezifischen Vokabulars zur Beschreibung von Daten und Funktionen
* Reflektion über die Grenzen des Systems: Welche Informationen sind verfügbar, welche nicht?

Diese Ergebnisse dienen als technische und semantische Grundlage für den weiteren Entwurfsprozess. Sie schaffen Klarheit über Daten, Funktionen und sprachliche Strukturen und bilden eine Schnittstelle zwischen Analyse und Gestaltung.

### Material

- [Aktuelle Prod Version](https://hops.gm.th-koeln.de/hops/modules/timetable/)
- [Aktuelle Dev Version](http://lwivs49.gm.fh-koeln.de:8080) Hinweis: Stundenplandaten liegen aktuell im Zeitraum vom 15.04.- 19.07.2024 vor.
- [Miro Board zur Sicherung der Ergebnisse](https://miro.com/app/board/uXjVGcl-pBI=/?share_link_id=919341261382)

</div>