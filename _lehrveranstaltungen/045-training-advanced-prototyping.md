---
titel: Advanced Prototyping
kuerzel: t-ld
verantwortlich: vs
typ: training
pflicht: false
termine: 2026-12-11 11:00
empfohlene-voraussetzungen: 
check-in-frage: 
published: true
dauer: 300
raum: hybrid-mutabor
info: Wie können wir Prototypen mit Figma systematisch aufbauen?
assignments: |
  - [Advanced Prototyping](/mi-bachelor-screendesign/assignments/training-002-advanced-prototyping/)

---

## Worum geht es?

In diesem Training befassen wir uns mit der systematisch Erstellung von Prototypen in Figma. Sobald die Kompexität der Screens und damit die Anzahl der benutzten Elemente zu nimmt, steigt auch die Gefahr, dass die Struktur des Projektes sich verschlechtert und irgendwann die Übersicht verloren geht.

Verstärkt wird die Problematik noch, wenn viele unterschiedliche Screens in dem Projekt hinzukommen und zu jedem Screen noch angepasste Screens für unterschiedliche Endgeräte oder Varianten.

Wir werden uns mit Konzepten, Techniken und Funktionen von Figma beschäftigen, die uns dabei helfen systematische, gut strukturierte und konsistente Prototypen zu erstellen. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/A_bdqGcjuBo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Was muss ich mitbringen?
- sicherer Umgang in Figma

## Figma-Fertigkeiten
{% comment %}Gepflegt mit dem Claude-Code-Skill /figma-fertigkeiten, siehe README.md{% endcomment %}

Hier stehen nur die Figma-Fertigkeiten, die neu dazukommen. Alles andere kennen Sie bereits aus den vorherigen Veranstaltungen (zuletzt: [Verschiedene Übungen zu Fläche und Typographie](/mi-bachelor-screendesign/lehrveranstaltungen/050-training-misc/)).

- **Variables:** In Variables legen Sie Farben, Zahlen und Schriftwerte einmal zentral an und verknüpfen sie mit Ihren Ebenen. Ändern Sie später einen Wert, ändert sich der ganze Podcast Player mit.
  [Figma-Hilfe](https://help.figma.com/hc/de/articles/15339657135383-Leitfaden-zu-Variablen-in-Figma) · [Video](https://www.youtube.com/watch?v=1ONxxlJnvdM)
- **Text Styles:** Ein Text Style fasst Schrift, Größe, Schnitt und Zeilenabstand zusammen. Verknüpfen Sie diese Werte mit Ihren Typographie-Variablen, bleiben alle Texte einheitlich.
  [Figma-Hilfe (englisch)](https://help.figma.com/hc/en-us/articles/360039957034-Create-and-apply-text-styles) · [Video](https://www.youtube.com/watch?v=APNWWhXIg04)
- **Variants:** Mit Variants packen Sie verschiedene Zustände einer Komponente in ein Component Set, etwa Play und Pause. In der Instanz schalten Sie dann rechts in der Seitenleiste zwischen den Zuständen um.
  [Figma-Hilfe (englisch)](https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants) · [Video](https://www.youtube.com/watch?v=y29Xwt9dET0)
- **Component Properties:** Mit Properties für Text, Sichtbarkeit und Instance Swap passen Sie Instanzen an, ohne für jede Abwandlung eine neue Komponente zu bauen. Titel oder Icon ändern Sie dann direkt in der Seitenleiste.
  [Figma-Hilfe](https://help.figma.com/hc/de/articles/5579474826519-Komponenteneigenschaften-untersuchen) · [Video](https://www.youtube.com/watch?v=iIq8FLt1hUY)
- **Auto Layout:** Auto Layout (<kbd>Shift</kbd> + <kbd>A</kbd>) ordnet Elemente in einem Frame neben- oder untereinander an, mit festen Abständen und Innenabständen. Kommt ein Eintrag in der Playlist dazu oder fällt einer weg, rutscht der Rest von selbst nach.
  [Figma-Hilfe](https://help.figma.com/hc/de/articles/360040451373-Leitfaden-zum-Auto-Layout) · [Video](https://www.youtube.com/watch?v=Aik8tMRdI90)
- **Constraints:** Constraints bestimmen, was mit einer Ebene passiert, wenn ihr Frame breiter oder schmaler wird: ob sie am Rand bleibt oder mitwächst. Das brauchen Sie, um aus den Hochformat-Screens die Querformat-Versionen zu machen.
  [Figma-Hilfe (englisch)](https://help.figma.com/hc/en-us/articles/360039957734-Apply-constraints-to-define-how-layers-resize) · [Video](https://www.youtube.com/watch?v=JZyUE5dY1Wk)
- **Plugins nutzen:** Plugins rüsten Funktionen nach, die Figma selbst nicht hat. Für die Playlist nutzen Sie Google Sheets Sync, das die Einträge aus einer Tabelle in Ihr Design holt.
  [Figma-Hilfe (englisch)](https://help.figma.com/hc/en-us/articles/360042532714-Use-plugins-in-files)

## Readings

- [How to construct a design system](https://www.freecodecamp.org/news/how-to-construct-a-design-system-864adbf2a117/)
- [Was ist ein Design Token](https://ux-ui-design.de/design-token/)
- [Naming Tokens in Design Systems](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676)
- [Atomic Design](https://atomicdesign.bradfrost.com)
- [Extending Atomic Design](https://bradfrost.com/blog/post/extending-atomic-design/)

## Tools
- [Figma Plugin - Color Shades & Tints Generator](https://www.figma.com/community/plugin/1221190866182222979/color-shades-tints-generator)
- [Figma Plugin - Google Sheets Sync](https://www.figma.com/de-de/community/plugin/735770583268406934/google-sheets-sync)
- [Color Designer](https://colordesigner.io)

## Video Tutorial

In diesem Figma-Video wird Schritt für Schritt ein dynamisches Veranstaltungs-/Stundenplan-Layout aufgebaut. Zunächst wird eine Colorcode-Komponente inklusive Varianten erstellt. Anschließend werden mithilfe von Auto Layout strukturierte Textfelder für Wochentage und Uhrzeiten sowie für Veranstaltung und Lehrende angelegt. Danach werden Colorcode-Komponente und Haarlinie integriert, ein Profilbild der Lehrperson eingefügt und eine Veranstaltungsliste erstellt. Zum Schluss wird gezeigt, wie die Elemente automatisch mit Inhalten aus Google Sheets befüllt werden, sodass Aktualisierungen schnell übernommen werden können.
<br><br>

<iframe width="560" height="315" src="https://www.youtube.com/embed/ljn_-YS4Zrw?si=iRfl_Wc7nZTUCi8M" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
