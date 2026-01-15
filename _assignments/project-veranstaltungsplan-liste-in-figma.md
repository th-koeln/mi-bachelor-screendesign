---
titel: Veranstaltungsliste in Figma aufbauen
tags: 
  - Layout
published: true
---

## Ziel der Übung
Sie bauen in Figma eine funktionale, dynamisch befüllbare **Veranstaltungsliste** als **Organism** – unter Verwendung von [Komponenten](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma), [Auto Layout](https://help.figma.com/hc/de/articles/360040451373-Leitfaden-zum-Auto-Layout) und dem [Google Sheets Sync Plugin](https://www.figma.com/de-de/community/plugin/735770583268406934/google-sheets-sync).

Diese Übung ist technisch und methodisch ausgerichtet – der Fokus liegt auf **Struktur, Modularität und Datenhandling**, nicht auf finalem Look & Feel.

--- 

## Material
- [Google Sheets Sync Plugin](https://www.figma.com/de-de/community/plugin/735770583268406934/google-sheets-sync)
- [Google Sheets Sync Plugin Doku](https://docs.sheetssync.app)
- [Tabelle mit Veranstaltungen](https://docs.google.com/spreadsheets/d/1m-zY9TQf1zGWPPyYnxvrrzNeAYLqd8THYcUGQqy_uvA/edit?usp=sharing)

### Figma Template
<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/design/QjeSJhbGUXoVFdKBugOP0Q/Vorlage-f%C3%BCr-Layoutworkshop-2025-26?node-id=0-1&embed-host=share" allowfullscreen></iframe>

<br>
### Kleines Video zur Nutzung des Google Sheets Sync Plugins
<iframe width="560" height="315" src="https://www.youtube.com/embed/aaugAwZU1hQ?si=TDkNTM4fpxgeGrVf" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


---

## Schritt 1: Komponentenstruktur aufbauen

#### Aufgabe:

* Erstellen Sie eine **Komponente für einen Veranstaltungseintrag**.
* Überlegen Sie, ob und welche **Sub-Komponenten** sinnvoll sind (z. B. Zeitangabe, Titel, Raum, Dozent*in, etc.).
* Bauen Sie die Komponenten [reaktionsfähig](https://help.figma.com/hc/en-us/articles/360039957734-Apply-constraints-to-define-how-layers-resize) auf, sodass sie gut über Auto Layout organisiert und später dynamisch befüllt werden können.

#### Hinweise:

* Arbeiten Sie mit **Auto Layout** innerhalb der Komponente(n).
* Achten Sie auf sauberes **Spacing**, konsistente Typografie, Wiederverwendbarkeit.
* Nutzen Sie die Vorlage und die darin enthaltenen Styles
* Ziehen Sie bei Bedarf die Ergebnisse des [Workshops «Gestaltungsrichtlinien und Spielräume»](https://miro.com/app/board/uXjVGckv1pM=/?share_link_id=772751485323) zu rate. Passwort *screendesign*


## Schritt 2: Google Sheets Sync Plugin integrieren

#### Aufgabe:

* Verwenden Sie das Plugin [Google Sheets Sync Plugin](https://www.figma.com/de-de/community/plugin/735770583268406934/google-sheets-sync), um Ihre Komponenten dynamisch mit Daten zu befüllen.
* Erstellen Sie dazu das bereitgestellte Google Sheet mit relevanten Spalten (z. B. Titel, Uhrzeit, Ort, etc.).
* Verbinden Sie das Sheet mit Ihrer Figma-Datei und mappen Sie die Inhalte auf die Komponenten-Felder.

#### Hinweise:

* Testen Sie, ob mehrere Einträge automatisch generiert werden.
* Prüfen Sie, ob Formatierungen konsistent übernommen werden.


## Optionaler Schritt 3: Responsives Verhalten gestalten

* Bauen Sie das Layout so um, dass es sich an **verschiedene Bildschirmgrößen** anpassen kann.
* Nutzen Sie **Auto Layout + Constraints**, um das Verhalten bei Größenänderung zu testen (z. B. Smartphone vs. Desktop).


## Ergebnis am Ende:

* Eine in Figma aufgebaute Veranstaltungsliste,
* modular als Organism strukturiert,
* befüllbar mit dynamischen Daten,
* optional responsive.

---

## Upload

Ein Upload von gehaltvollen Ergebnissen bringt bis zu 5 Bonuspunkte für das Abschlussprojekt. 
Laden Sie Ihre Ergebnisse im [ILU](https://ilu.th-koeln.de/ilias.php?baseClass=ilexercisehandlergui&cmdNode=cw:nq:4i&cmdClass=ilAssignmentPresentationGUI&ref_id=770941&mode=future&from_overview=1&ass_id=27791) hoch.

Verwenden Sie beim Dateinamen bitte die folgende Nomenklatur:

> `sd-veranstaltungsliste-NACHNAME.png` 
