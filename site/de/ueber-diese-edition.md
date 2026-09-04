---
layout: page
title: Über diese Edition
standfirst: Wie der Text erstellt wurde, was die editorischen Zeichen bedeuten und was noch offen ist.
permalink: /de/ueber-diese-edition/
lang: de
alt_url: /reading-this-edition/
---

## Die Quelle

Die Dokumente liegen im **Hohenloher Zentralarchiv Neuenstein (HZAN)**. Der hier
dargebotene Text wurde nach den Originalhandschriften transkribiert, geschrieben in
*Kurrentschrift*, der deutschen Schreibschrift der Zeit, schwer zu lesen und leicht falsch
zu lesen.

**Die Transkription wurde von einem KI-System angefertigt, nicht von einem Paläographen.**
Das ist von Bedeutung, und die Edition verschweigt es nicht. Die maschinelle Transkription
von Kurrentschrift macht einen eigenen Fehlertyp: neben gewöhnlichen Verwechslungen
ähnlicher Buchstabenformen kann sie Text hervorbringen, der plausibles Deutsch ist, aber
nicht das, was auf der Seite steht. Jede editorische Entscheidung wurde mit diesem Wissen
getroffen, und Lesarten, die sich nicht aus Belegen klären ließen, blieben unangetastet,
statt erraten zu werden.

## Seiten

Die Briefe werden Seite für Seite dargeboten, so wie sie im Archiv liegen. Jede
Handschriftenseite erscheint als eigener Block, bezeichnet mit dem Zeilenbereich, den sie
im Archivtext einnimmt. Nichts läuft über einen Seitenumbruch hinweg. Ein Brief bleibt
dennoch als Ganzes lesbar; die Seiten sind Gliederung darin, und neben ihnen stehen die
Digitalisate.

Auf die 318 Dokumente entfallen **869 Handschriftenseiten**.

## Vier Ansichten jedes Dokuments

Der Umschalter über dem Text wechselt zwischen ihnen.

**Transkription** ist die Grundeinstellung. Sie behält die Zeilenumbrüche der Handschrift
bei, eine Zeile je Zeile der Seite, gezählt nach der Archivdatei, sodass eine Stelle
zeilenweise zitiert werden kann. Sie ist jedoch *bearbeitet*, nicht roh. Wo ein Wort
tatsächlich über die Zeile gebrochen ist, trägt es einen einfachen Bindestrich; wo die
Transkription einen Umbruch markierte, der keiner ist, ist das Zeichen entfernt.
Wiederkehrende Namen sind vereinheitlicht. Das ist, was die Briefe sagen, dargeboten so,
wie die Herausgeber sie gelesen haben.

**Lesefassung** nimmt denselben Text und führt die Zeilen zu fortlaufender Prosa zusammen.

### Was geändert wurde, und warum

Diese Edition bietet keine strenge diplomatische Umschrift, und der Grund ist ein
bestimmter: die Transkription stammt von einem KI-System, nicht von einem Paläographen.
Das meiste, was wie eine Eigenheit des Schreibers aussah, erwies sich als Maschinenfehler.
Diese Fehler getreu wiederzugeben, bewahrte nichts von der Handschrift und führte die
Leserschaft in die Irre.

Drei Arten von Eingriffen wurden vorgenommen, jede aufgrund von Belegen statt aufgrund von
Eindrücken:

- **Trennzeichen am Zeilenende.** Von 1.317 Zeichen am Zeilenende verbanden nur 826
  tatsächlich ein Wort. 483 waren überflüssig, 5 waren Kustoden, und 3 hatten nichts, worin
  sie sich hätten fortsetzen können. Jedes wurde an diesem Korpus und am historischen
  deutschen Sprachgebrauch geprüft, und jede Entscheidung ist mit ihrem Beleg verzeichnet.
- **Wiederkehrende Namen.** Mehrfach unterschiedlich transkribierte Personen und Orte
  wurden auf eine Schreibung vereinheitlicht, nur am Wortstamm, sodass deutsche und
  polnische Flexionsendungen erhalten bleiben. Wo sich eine Variante als *andere* Person
  herausstellte, blieb sie bewusst stehen.
- **Nachweisbare Verschreibungen**, wo dasselbe Wort anderswo im Korpus richtig
  geschrieben ist oder die Lesart einer zweiten Abschrift desselben Dokuments widerspricht.

Die Orthographie der Zeit wird nicht berichtigt. Formen wie *laßen*, *seyn*, *nöthig*,
*Ewr* und *dero* sind die Schreibweise der Verfasser und bleiben stehen. Ebenso die
Zweifelszeichen des Transkribenten.

Der unbearbeitete Text besteht weiter. Die Archivdatei
(`von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt`) enthält die Transkription genau so,
wie sie erzeugt wurde, und jede editorische Schicht wird gegen sie geprüft: eine Änderung,
die keine verzeichnete Entscheidung deckt, lässt den Build scheitern.

**Englisch** enthält die Übersetzung, Seite für Seite ergänzt. Wo noch keine vorliegt, sagt
die Ansicht das, statt nichts zu zeigen.

**Digitalisate** zeigen die Seite selbst. Jedes Bild wurde einzeln und von Auge seiner
Seite zugeordnet; ein Klick öffnet es in voller Größe. Von den 872 aufgenommenen Bildern
stehen 865 neben einer transkribierten Seite. Die übrigen sieben sind das Titelblatt der
Serie, fünf Blätter, die keine Handschriftenseiten sind, und eine Seite mit
Rechenaufstellungen, die bewusst nicht transkribiert wurde.

Die hier veröffentlichten Bilder sind auf 1100 Pixel Breite verkleinert, was zum Lesen der
Hand genügt. Die Originale in voller Auflösung, rund 1 GB, liegen offline als
Archivmaster.

## Warum die Trennzeichen geprüft werden mussten

Die Transkription bezeichnet ein gebrochenes Wort mit `¬`, doch dieses Zeichen ist nicht
für bare Münze zu nehmen, denn der Transkribent hat es sehr häufig falsch gesetzt. Von den
1.317 Zeichen am Zeilenende im Korpus verbinden **483 (37 %) gar nichts**:

| | |
|---|---|
| `die¬` + `serhalb` | *dieserhalb*, eine wirkliche Fügung. **Verbunden** |
| `die¬` + `nöthigsten` | *dienöthigsten* ist kein Wort. **Getrennt gelassen** |
| `auf¬` + `Übrigens` | zwei eigene Wörter. **Getrennt gelassen** |

Jedes Zeichen wurde daher anhand von Belegen entschieden, nicht nach Annahme. Zwei Quellen
dienten dazu: dieses Korpus selbst, das die Orthographie der Zeit kennt, und die
Frequenzdaten der [DWDS](https://www.dwds.de), die lemmatisiert sind, sodass flektierte
Formen wie `Mitgliedern` aufgelöst werden, und die historisches Deutsch abdecken. Als
wirkliches Wort gilt eine Form ab tausend Korpustreffern; darunter kommt Rauschen aus
Eigennamen zurück.

Das Ergebnis: **826 echte Verbindungen, 483 Zeichen ohne Verbindung, 5 Kustoden** sowie 19
Fälle, die an den Originalen zu prüfen sind. Jede Entscheidung ist mit ihrem Beleg in
`linebreak_decisions.csv` verzeichnet, und jede lässt sich überstimmen.

## Kustoden

Fünf Seiten enden mit einer Kustode, dem alten Schreibbrauch, das erste Wort der nächsten
Seite unten auf die laufende zu setzen, damit die Blattfolge erkennbar bleibt:

| Brief | Seitenende | Anfang der nächsten Seite |
|---|---|---|
| 133 | `Con¬` | `Contract` |
| 140 | `Vor-` | `Vorwerk` |
| 168 | `Win¬` | `Winnickischen` |
| 177 | `be¬` | `benennung` |
| 235 | `ver-` | `verliehren` |

Das sind keine gebrochenen Wörter. Sie zu verbinden erzeugte „ConContract“. Sie bleiben in
der diplomatischen Ansicht, wo sie zur Seite gehören, und entfallen in der Lesefassung, wo
sie nicht zum Text gehören.

## Editorische Zeichen

| Zeichen | Bedeutung |
|---|---|
| `¬` | Das Worttrennungszeichen des Transkribenten. In der diplomatischen Ansicht beibehalten, gleichviel ob es sich als echt erwies, denn das Zeichen ist selbst ein Beleg; die Lesefassung folgt der geprüften Entscheidung. |
| `[?]` | Der Transkribent konnte das Wort überhaupt nicht lesen. |
| `[word?]` | Eine Vermutung zu einem Wort, das dem Transkribenten unklar war. |
| `(missing)` / `(skipped)` | Die Archivnummer besteht, doch unter ihr ist kein Text überliefert. |
| `ſ` | Das lange s, wie im Original geschrieben. |

Im Korpus sind **150** unsichere Lesarten verzeichnet: 98 Wörter, die niemand entziffern
konnte, und 52 als Vermutung angebotene. Sie bleiben im Text jedes betroffenen Dokuments
sichtbar, statt geglättet zu werden. Fünf beschädigte Stellen sind noch an den Originalen
zu prüfen.

## Datierung

Etwa sieben von acht Dokumenten tragen ein Datum im Brief selbst. Die übrigen sind auf eine
von vier Weisen datiert, und jedes Dokument nennt die für es zutreffende:

- **aus dem Brief gelesen**, die Datumszeile, wie sie geschrieben steht
- **von der Forschung ergänzt**, anhand der Originalhandschriften ermittelt
- **aus den Nachbarbriefen erschlossen**, eingegrenzt durch die Briefe davor und danach,
  wobei die Begründung beim Dokument verzeichnet ist
- **der Doppelüberlieferung entnommen**, wo ein Dokument in zwei Abschriften vorliegt

Sechs Dokumente bleiben undatiert und stehen am Ende der chronologischen Folge.

Zu beachten ist, dass die Zählung des Archivs nicht chronologisch ist. Die Briefe 1 bis 74
bilden einen ungeordneten Block über die Jahre 1806 bis 1815; 75 bis 301 laufen von 1798 an
der Reihe nach. Die Nummern 302 und 303 stehen außerhalb dieser Folge. Beide Ordnungen sind
begehbar, und die Archivnummer ist der feste Zitierschlüssel.

## Geld

Beträge stehen im preußischen System, das bis 1821 galt: **1 Reichsthaler = 24 Groschen;
1 Groschen = 12 Pfennig**, hier geschrieben als `Rthl`, `g` und `d`. Das Korpus hält diese
Grenzen genau ein, und eben das machte es möglich, die vielen uneinheitlichen Abkürzungen
des Originals ohne Raterei in eine einzige Schreibweise aufzulösen. Das `d` für Pfennig ist
kein Fehler. Es ist die historische Abkürzung für *denarius*, dieselbe Übung, die hinter
den britischen Pence vor der Dezimalumstellung steht.

## Zusammengefasste und doppelt überlieferte Dokumente

Mehrere Archivnummern enthielten mehr als ein Dokument. Diese wurden in Teilaufnahmen
zerlegt, Brief 72 in 72a bis 72f, Brief 74 in 74a bis 74e und so fort, jede mit einer
Verknüpfung zurück zum übergeordneten Stück. Dabei wurde nichts entfernt.

Drei Dokumente sind in zwei Abschriften überliefert: die Briefe **48 und 302** sind
derselbe Brief vom 7. März 1809, zweimal transkribiert, ebenso 72d/72e (deutsch und
polnisch) sowie 118b/118c. Die Doppelüberlieferungen sind ungewöhnlich wertvoll, denn der
Vergleich zweier unabhängiger Transkriptionen derselben Seite zeigt genau, wo
Transkription fehlgeht, und beide Abschriften stehen unverändert nebeneinander.

## Was noch offen ist

- Eine Geldsumme weicht zwischen den beiden Abschriften des Briefes vom 7. März 1809
  voneinander ab (23.000 gegen 32.000 Rthl). Beide Transkriptionen sind ihrer jeweiligen
  Seite treu, die Abweichung gehört also dem ursprünglichen Abschreiber, nicht dieser
  Edition.
- 150 unsichere Lesarten und fünf beschädigte Stellen sind an den Originalen zu prüfen.
- Manche Identifizierungen beruhen allein auf dem Zusammenhang. Die Personenseiten nennen
  jeweils den Beleg.

## Englische Übersetzungen

Die Übersetzungen werden Dokument für Dokument ergänzt. Wo eine vorliegt, erscheint sie
unter dem deutschen Text mit ihrem Status; wo noch keine vorliegt, ist der deutsche Text
unterdessen vollständig und durchsuchbar. Keine Übersetzung gilt als maßgeblich, bevor sie
von Hand geprüft wurde. Eine als **draft** bezeichnete Übersetzung hat die hier
beschriebenen maschinellen Prüfungen durchlaufen, ist aber noch nicht gegen die Handschrift
gelesen; **reviewed** heißt, dass eine Person jede dazu erhobene Rückfrage durchgegangen
ist.

**Das Englische zeigt eine Lücke, wo das Deutsche eine hat.** Das ist Absicht, und es ist
das Wichtigste am Lesen der Übersetzung. Eine Übersetzerin oder ein Übersetzer, ob Mensch
oder Maschine, kann fast jeden beschädigten Satz in glattes Englisch bringen, und glattes
Englisch lässt die Leserschaft nicht erkennen, was gesicherter Text ist und was Vermutung.
Darum gehen die Zweifelszeichen mit über:

| Im Deutschen | Im Englischen | Bedeutung |
|---|---|---|
| `[?]` | `[illegible]` | in der Handschrift nichts Lesbares |
| `[word?]` | `[uncertain: word]` | eine Lesart angeboten, aber unsicher |
| `[...]` | `[text lost]` | eine Lücke oder ein beschädigter Seitenrand |

Sie finden `[uncertain: …]` im Englischen mitunter auch dort, wo das Deutsche gar kein
Zeichen trägt. Das heißt, dass die Transkription sich wie gewöhnliches Deutsch liest, im
Zusammenhang aber keinen Sinn ergibt, eine Stelle also, an der die Handschrift
wahrscheinlich unbemerkt falsch gelesen wurde. Diese Stellen sind zur Prüfung am Original
gesammelt.

Wo sich erschließen ließ, was die Handschrift *wahrscheinlich* sagte, bleibt dieser
Vorschlag bewusst aus dem Englischen heraus und wird gesondert verzeichnet. Die
Transkription zu berichtigen ist etwas anderes, als sie zu übersetzen, und es geschieht an
der Handschrift, nicht am Sinn des Satzes. Zahlen und Eigennamen werden genau so
wiedergegeben, wie sie transkribiert sind, niemals nebenbei berichtigt, auch dort nicht, wo
sie offenkundig falsch sind. Eine stillschweigend verbesserte Zahl zerstörte den Beleg
dafür, dass sie je falsch war.
