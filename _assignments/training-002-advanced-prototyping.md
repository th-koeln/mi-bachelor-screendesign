---
titel: Advanced Prototyping
tags: 
  - Prototyping
  - Figma
  - WS2425
published: true

---

Heute beschäftigen wir uns mit dem Thema „Advanced Prototyping”. Hilfestellungen bekommen Sie in dem [dazu vorgesehenen Training](/mi-bachelor-screendesign/lehrveranstaltungen/045-training-advanced-prototyping/).

---

## Übung 1 - Variablen und Text Styles

Fügen Sie diese [Figma-Vorlage](https://www.figma.com/design/BQoZkTtpaeKOkojVgqguit/podcast-player?node-id=0-1&t=JoSAhbLOR8LBnbhu-1) ihrem Workspace hinzu. Sie ist die Ausgangsbasis für die folgenden Übungen.

* Erzeugen Sie Variablen für alle verwendeten Farben und weisen Sie diese den vorhandenen Elementen zu.
* Erzeugen Sie Variablen für alle verwendeten Schrifgrößen und -schnitte und der eingesetzen Schriftfamilie.
* Leiten Sie aus den zuvor definierten Variablen Text Styles ab und weisen Sie diesen den vorhandenen Textelementen zu.

## Übung 2 - Komponenten
* Erzeugen Sie Komponenten und Varianten von Komponenten für Elemente bei denen es sinnvoll ist. Diese helfen dabei ein konsistentes Layout, auch über mehrere Views hinaus, zu ermöglichen.  
* Sortieren Sie in diesem Zuge die Elemente in der Ebenenleiste nach einem System, welches Sie sich zuvor überlegt haben. Eine Möglichkeit ist es, die Elemente in der Reihenfolge, wie sie auf der Zeichenfläche vorkommen, zu sortieren und zwar von oben nach unten.  
* Achten Sie darauf, dass Sie den Elementen sprechende Namen geben. Überlegen Sie sich ein Schema, welches Sie für die Benamung verwenden.

## Übung 3 - Autolayout und Constraints

Für die bestehenden Screens soll ein Layout für das Querformat erzeugt werden.

Konfigurieren Sie die Elemente so, dass sie flexibel auf Größenänderungen der Frames oder der Elemente selbst reagieren.
Duplizieren Sie daraufhin die Frames, stellen Sie sie auf das Querformat ein und justieren Sie die darin enthaltenden Elemente entsprechend der neuen Ausrichtung.

## Übung 4 - Google Sheets Sync

Die Playlist soll nun dynamisch mit Inhalten aus einem Google Sheet befüllt werden.
* Installieren Sie das [Google Sheets Sync Plugin](https://www.figma.com/de-de/community/plugin/735770583268406934/google-sheets-sync).
* Verbinden Sie das Plugin mit dem folgenden [Google Sheet](https://docs.google.com/spreadsheets/d/1cNWdVcJ7_LBgH3YxF-VcbNx0RGr9kudf6qnl4rmFLR8/edit?gid=0#gid=0).
* Ordnen Sie die Datenfelder aus dem Sheet den entsprechenden Textelementen der Playlist zu (Datum, Titel, Größe).
* Achten Sie darauf, dass die Struktur der Komponenten so angelegt ist, dass dynamische Inhalte problemlos übernommen werden können (z. B. durch sauberes Autolayout).
* Aktualisieren Sie die Inhalte über das Plugin und prüfen Sie, ob alle Felder korrekt befüllt werden.


## Video Tutorial

In diesem Figma-Video wird Schritt für Schritt ein dynamisches Veranstaltungs-/Stundenplan-Layout aufgebaut. Zunächst wird eine Colorcode-Komponente inklusive Varianten erstellt. Anschließend werden mithilfe von Auto Layout strukturierte Textfelder für Wochentage und Uhrzeiten sowie für Veranstaltung und Lehrende angelegt. Danach werden Colorcode-Komponente und Haarlinie integriert, ein Profilbild der Lehrperson eingefügt und eine Veranstaltungsliste erstellt. Zum Schluss wird gezeigt, wie die Elemente automatisch mit Inhalten aus Google Sheets befüllt werden, sodass Aktualisierungen schnell übernommen werden können.
<br><br>

<iframe width="560" height="315" src="https://www.youtube.com/embed/ljn_-YS4Zrw?si=iRfl_Wc7nZTUCi8M" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>