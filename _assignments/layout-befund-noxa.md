---
titel: "Vom Wireframe zum Layout: Befund-Seite für NOXA Analytik"
tags: 
  - Layout
  - Wireframes
  - Variantenbildung
  - WS2627
published: true
---

Heute entwickeln Sie ein echtes Layout, und zwar in vier Stufen: von der groben Skizze über Grayscale-Wireframes bis zum fertigen Entwurf. Nach jeder Stufe tragen wir die Ergebnisse zusammen, dann geht es auf die nächste. Den Input dazu gibt es jeweils kurz vor der Stufe, in der Sie ihn brauchen.

---

## Kontext

NOXA Analytik kennen Sie schon: ein Labor, das Wasser, Böden und Lebensmittel untersucht. Kundinnen und Kunden schicken Wasserproben ein und bekommen den Befund in ihrem Kundenportal. Die Seite soll präzise und sachlich wirken, aber nicht kalt. Die genaue Richtung finden Sie unten unter »Gestaltungsrichtung«.

Ihre Aufgabe: Gestalten Sie die **Befund-Seite** im Kundenportal. Wer sie öffnet, will vor allem eines wissen: Ist mein Wasser in Ordnung? Und wenn nicht: Was muss ich tun?

## Formate

| Format | Breite | Raster |
|---|---|---|
| **Desktop** | 1440 px | 12 Spalten, Rand 80 px, Spaltenabstand 24 px |
| **Smartphone** | 390 px | 4 Spalten, Rand 20 px, Spaltenabstand 16 px |

Die Höhe ergibt sich aus dem Inhalt. Im Workshop arbeiten Sie am Desktop, die Smartphone-Fassung kommt in der Hausaufgabe.

## Vorlage und Schrift

Damit Sie direkt am Layout arbeiten können, bekommen Sie eine [Figma-Vorlage](https://www.figma.com/design/N3lJDLKBkLQozJPZICHPG6/SD-2026-%C2%B7-Befund-NOXA-%C2%B7-Vorlage?node-id=10-12&t=SzfwzerAav8qaZ42-1). Duplizieren Sie sie in Ihre Drafts (»Duplicate to your drafts«) und arbeiten Sie in Ihrer Kopie. Die Vorlage hat fünf Seiten:

- **Lies mich:** eine kurze Anleitung
- **Gestaltungsrichtung:** Farbfilm und semantisches Differential, siehe unten
- **Arbeitsfläche:** leere Frames für alle vier Stufen und für die Abgabe, die Raster sind schon eingestellt
- **Inhalt:** alle Texte der Befund-Seite zum Kopieren
- **Bausteine:** Wireframe-Bausteine für Stufe 2, zum Beispiel Textbalken, Bildfläche und Button

Außerdem sind Textstile (Desktop und Mobil), Graustufen, die Farben des Farbfilms und Abstände (4 bis 96 px) angelegt. Auf allen Frames liegen ein 8-px-Grid und ein Zeilenraster im 24-px-Rhythmus, dem Zeilenabstand des Fließtexts. **Nutzen Sie Textstile, Farben und Abstände der Vorlage, statt eigene Werte zu setzen.**

Ein Layout enthält die Vorlage bewusst nicht. Auch Messwerttabelle, Statusanzeige, Empfehlung, Navigation und Kopfbereich gestalten Sie selbst.

**Die Schrift ist vorgegeben:** IBM Plex Sans für alle Texte, IBM Plex Mono für Messwerte und die Probennummer. Die Ziffern der Mono-Schrift sind gleich breit, Werte stehen dadurch sauber untereinander. Heute geht es um Layout und Varianten, nicht um die Schriftwahl.

## Gestaltungsrichtung

Wie die Befund-Seite wirken soll, ist vorgegeben. Sie finden beides auch auf der Seite »Gestaltungsrichtung« der Vorlage.

**Semantisches Differential:** eher sachlich, sehr präzise, eher modern, deutlich wissenschaftlich, eher klar, deutlich innovativ.

![Semantisches Differential der Befund-Seite: nahbar gegen sachlich 4, präzise gegen spielerisch 1, modern gegen zeitlos 2, sinnlich gegen wissenschaftlich 5, klar gegen warm 2, bewährt gegen innovativ 5](../images/noxa-differential.png)

**Farbfilm:** fünf Farben. Die Breite der Streifen zeigt, wie viel Fläche eine Farbe ungefähr einnimmt.

![Farbfilm mit Nachtblau, Blau, Türkis, Grün und Hell, die Streifenbreite zeigt den Flächenanteil](../images/noxa-farbfilm.png)

| Farbe | Wert | Kontrast zu Weiß | Einsatz | Fläche |
|---|---|---|---|---|
| **Nachtblau** | #011140 | 18,2 : 1 | Text und Flächen | ca. 7 % |
| **Blau** | #0D6BA6 | 5,7 : 1 | Text, Links, Flächen | ca. 28 % |
| **Türkis** | #42BABF | 2,3 : 1 | nur Flächen, als Text nur auf Nachtblau | ca. 10 % |
| **Grün** | #A4DA71 | 1,6 : 1 | nur Flächen, als Text nur auf Nachtblau | ca. 5 % |
| **Hell** | #F8F8F8 | 1,1 : 1 | Hintergrund | ca. 50 % |

Die Farben kommen erst in Stufe 4 ins Spiel. Bis dahin arbeiten Sie in Graustufen.

**Grün ist keine Statusfarbe.** Das Grün gehört zum Farbfilm, es ist eine Markenfarbe. Achten Sie darauf, dass es nicht als »in Ordnung« missverstanden wird. Wie Sie den Status der Messwerte zeigen, zum Beispiel »über dem Grenzwert«, ist Teil der Aufgabe. Verlassen Sie sich dabei nicht allein auf Farbe.

## Inhalt

Alle Inhalte müssen auf die Seite. Wie Sie sie gewichten, gruppieren und anordnen, ist Ihre Entscheidung.

**Portal:** Logo NOXA Analytik, Navigation (Übersicht, Befunde, Proben bestellen, Rechnungen), Konto von Petra Albers

**Kopf des Befunds**
- Titel: Befund Trinkwasser
- Probennummer: NX-2026-04817
- Probenahme: 27.10.2026, Befund vom 06.11.2026
- Entnahmestelle: Küche, Hauptstraße 12, 51069 Köln

**Gesamtergebnis:** 1 Wert über dem Grenzwert. Kupfer in der ersten Probe (morgens, Wasser stand über Nacht in der Leitung).

**Messwerte**

| Parameter | Probe 1 (morgens) | Probe 2 (nach 3 Minuten) | Grenzwert | Bewertung |
|---|---|---|---|---|
| Kupfer | 2,4 mg/l | 0,3 mg/l | 2,0 mg/l | Probe 1 über dem Grenzwert |
| Blei | 0,004 mg/l | 0,001 mg/l | 0,010 mg/l | in Ordnung |
| Nickel | 0,006 mg/l | 0,002 mg/l | 0,020 mg/l | in Ordnung |
| Nitrat | 12 mg/l | 12 mg/l | 50 mg/l | in Ordnung |
| pH-Wert | 7,4 | 7,5 | 6,5 bis 9,5 | in Ordnung |
| Gesamthärte | 14,2 °dH | 14,1 °dH | kein Grenzwert | hart |

**Empfehlung:** Die Empfehlung gibt es in zwei Fassungen, kurz und ausführlich. Sie entscheiden, welche Sie verwenden oder wie Sie beide kombinieren, zum Beispiel die kurze Fassung sichtbar und die ausführliche zum Aufklappen.

*Empfehlung kurz*

> Empfehlung
>
> Lassen Sie morgens und nach längerer Abwesenheit das Wasser etwa drei Minuten laufen, bis es spürbar kühler ist. Nutzen Sie das erste Wasser für Blumen, nicht zum Trinken oder Kochen. Bei Kupfer sind vor allem neue Leitungen betroffen. Wir empfehlen eine Kontrollmessung in sechs Monaten.

*Empfehlung ausführlich*

> Empfehlung
>
> In Ihrer ersten Probe, morgens nach der Nacht entnommen, liegt der Kupferwert mit 2,4 mg/l über dem Grenzwert der Trinkwasserverordnung von 2,0 mg/l. In der zweiten Probe, nach drei Minuten Ablaufen, liegt er mit 0,3 mg/l deutlich darunter. Das zeigt: Das Kupfer stammt nicht aus dem Wasser Ihres Versorgers, sondern löst sich aus den Leitungen im Haus, während das Wasser darin steht.
>
> Besonders betroffen sind neue Kupferleitungen. Auf ihrer Innenseite bildet sich mit der Zeit eine Schutzschicht, die weniger Kupfer abgibt. Das dauert in der Regel einige Monate bis etwa zwei Jahre. Auch die Wasserchemie spielt eine Rolle: Ihr pH-Wert von 7,4 liegt an der unteren Grenze des Bereichs, für den Kupferleitungen als geeignet gelten.
>
> Was Sie tun können: Lassen Sie morgens und nach längerer Abwesenheit, etwa nach dem Urlaub, das Wasser laufen, bis es spürbar kühler ist. Das dauert meist zwei bis drei Minuten. Nutzen Sie dieses Wasser zum Blumengießen oder Putzen. Abkochen hilft nicht, das Kupfer bleibt dabei im Wasser. Nehmen Sie zum Trinken und Kochen nur kaltes Wasser, denn warmes Wasser löst mehr Kupfer aus der Leitung.
>
> Für Säuglinge ist erhöhtes Kupfer besonders bedenklich. Bereiten Sie Babynahrung nur mit abgelaufenem Wasser zu, bis eine Kontrollmessung den Wert unter dem Grenzwert bestätigt.
>
> Wohnen Sie zur Miete, informieren Sie bitte Ihre Vermieterin oder Ihren Vermieter über den Befund. Wir empfehlen eine Kontrollmessung in sechs Monaten. Liegt der Wert dann weiterhin über dem Grenzwert, beraten wir Sie gern zu den nächsten Schritten, zum Beispiel zu einer Prüfung der Hausinstallation durch einen Installationsbetrieb.

**Aktionen:** Befund als PDF herunterladen, Kontrollmessung bestellen, Beratung buchen

**Ansprechperson:** Dr. Jonas Riedel, Labor Köln, 0221 555 0148, j.riedel@noxa-analytik.de

**Hinweis:** Grenzwerte nach Trinkwasserverordnung. Analysiert im akkreditierten Labor nach DIN EN ISO/IEC 17025.

---

## Die vier Stufen

### Stufe 1: Skizzen

Skizzieren Sie auf Papier **6 bis 8 Thumbnails** der Desktop-Seite, jeweils nur mit groben Blöcken. Keine Details, kein Text, nur: Was steht wo, und was ist wie groß? Erst viele, dann gute. Fotos der Skizzen kommen später in den Frame »Skizzen« der Vorlage.

Danach Galerie: Skizzen auslegen, Rundgang, die stärkste fremde Skizze markieren. Gemeinsam halten wir fest, warum die stärksten Skizzen funktionieren. Diese **Kriterien** begleiten Sie durch alle weiteren Stufen.

### Stufe 2: Grayscale-Wireframes

Bauen Sie Ihre beste Skizze in der Vorlage als **Grayscale-Wireframe** auf dem Desktop-Raster: nur Grautöne, Text als graue Balken, Flächen als hellgraue Felder. Nutzen Sie dafür die Seite »Bausteine« und die Abstände der Vorlage. Eine Idee aus einer fremden Skizze zu übernehmen ist ausdrücklich erlaubt.

Entwickeln Sie dann **drei Varianten entlang einer Achse**, in den Frames »Variante A«, »Variante B« und »Variante C«. Es ändert sich jeweils nur eine Variable, zum Beispiel die Position des Gesamtergebnisses, die Darstellung der Messwerte oder das Gewicht der Empfehlung. Tragen Sie die Achse jeweils im Feld »Achse: …« über dem Frame ein. Wählen Sie mithilfe der Kriterien eine Variante aus.

### Stufe 3: Mid-Fi

Bringen Sie die gewählte Variante im Frame »Mid-Fi Desktop« auf Mid-Fi: Ersetzen Sie die Balken durch **echte Texte** von der Seite »Inhalt«, gesetzt mit den **Textstilen** der Vorlage, alles noch in Grau. Jetzt zeigt sich, ob das Layout den echten Inhalt aushält.

### Stufe 4: Hi-Fi

Bringen Sie den Entwurf im Frame »Hi-Fi Desktop« in Farbe, mit den Farben aus dem **Farbfilm** und ungefähr in ihren Flächenanteilen. Prüfen Sie den Kontrast, vor allem bei Türkis und Grün. Der Status darf nicht nur über Farbe erkennbar sein. Im Workshop legen Sie die Farbverteilung fest, fertig wird der Entwurf in der Hausaufgabe, zusammen mit der Fassung im Frame »Hi-Fi Smartphone«.

---

## Hausaufgabe

- Stellen Sie den Hi-Fi-Entwurf für den Desktop fertig.
- Übertragen Sie ihn auf das **Smartphone** (390 px, 4 Spalten).
- Legen Sie die ganze Reihe im Frame »Übersicht« (Section »Abgabe«) an: Skizzen, Variante A, B und C, Mid-Fi, Hi-Fi Desktop und Hi-Fi Smartphone, zusammen sieben Ergebnisse.
- Schreiben Sie im Frame »Erläuterung« eine kurze **Erläuterung** (ca. 150 Wörter): Welche Achse haben Sie variiert? Welche Variante haben Sie gewählt und warum, gemessen an den Kriterien aus der Galerie? Was hat sich von Stufe zu Stufe verändert?

## Abgabe

Laden Sie Ihre Ergebnisse bis zum **19.11.2026 23:55 Uhr** im [ILU](https://ilu.th-koeln.de/ilias.php?baseClass=ilexercisehandlergui&cmdNode=cw:nq&cmdClass=ilObjExerciseGUI&cmd=showOverview&ref_id=679333) hoch.

Exportieren Sie dafür vier Frames aus der Vorlage als PNG: »Übersicht«, »Hi-Fi Desktop«, »Hi-Fi Smartphone« und »Erläuterung«. Desktop und Smartphone geben Sie zusätzlich einzeln ab, weil sie in der Übersicht klein werden.

Verwenden Sie beim Dateinamen bitte die folgende Nomenklatur:

> `sd-layout-noxa-uebersicht-NACHNAME.png` \
`sd-layout-noxa-desktop-NACHNAME.png` \
`sd-layout-noxa-smartphone-NACHNAME.png` \
`sd-layout-noxa-erlaeuterung-NACHNAME.png`

Die Skizzen fotografieren oder scannen Sie und legen sie in den Frame »Skizzen«. Auf der Übersicht zeigen Sie sie ebenfalls, im Platzhalter »Skizzen«.
