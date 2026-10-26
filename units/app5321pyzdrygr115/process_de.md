Der Bestand kam fertig übertragen: die eigene Lesung des Herausgebers, als
Tabellenexport gegeben („Relationes [protocollon] 1791-1792 (53_21_0_-_Pyzdry
Gr.115) - Sheet1.csv“), eine Kopfzeile und sieben Zeilen, je fünf Zellen. Die
Datei liegt als `intake/table.csv` vor, wie empfangen, und alles andere wird
aus ihr gemacht.

Der Ordner enthält zwei Photographien: den eigenen Zuschnitt des
Herausgebers der Seite 543 (`543_trim.jpg`) und die Doppelseite
(`542v-543.jpg`). Benutzt wird nur der Zuschnitt, auf des Herausgebers Wort:
die Seite 543 ist die Seite der Einheit im Blick. Der Zuschnitt ist bereits
eine einzelne Seite, also wird keine Falte gesetzt und kein Schnitt gemacht;
das Intake-Skript (`intake/holding.py`) kopiert die eine Seite ganz unter der
Seitenkennung `0543_a`, auf die Weise des Rauchfangsteuerregisters (APP
53/64/0/-/Kalisz Tab.21).

Die Übertragung deckt die Tabelle in der ersten Hälfte der Seite, auf des
Herausgebers Wort; der Rest der Seite gehört zum Eintrag nach der Tabelle.
Das Dokument hat daher eine Seite und neun Zeilen des Korpus: die
Kopfzeile, die die Tabelle eröffnet, und die sieben Zeilen der Pfarrei.

Eine Lesung wurde geändert, auf des Herausgebers im Chat gegebenes Wort
(2026-10-26): die erste Zelle der Kopfzeile, „Parofie“, ist „Parafie“. Die
Änderung wird von `--correct` des Intake-Skripts angewendet und in
`transcription_decisions.csv` vermerkt; alles andere steht, wie der
Herausgeber es tippte, die diakritischen Zeichen nur, wo er sie gab.

Die Tabelle hat keine Spalte der Eintragsnummern: die Pfarrei steht in der
ersten Zelle, gefüllt in der Zeile des Dorfes selbst und leer unter ihr, und
die Zahlen folgen. Die Tabellen-Maschinerie der Edition sortierte eine
Tabelle nach den Nummern ihrer ersten Spalte und blieb bei einer Tabelle
ohne solche stehen. Sie wurde erweitert, und die Erweiterung wurde geprüft,
wie geprüft wird, wenn gemeinsam genutzter Code geändert wird: die Version
vor der Änderung, aus dem Repository genommen, und die neue wurden über
jede Tabelle geführt, die die Edition schon trägt, und die beiden Ausgaben
stimmen genau überein (`pipeline/review/verify_table_of_diff.py`; 12
Tabellendokumente in 5 Einheiten).

Die Zahlen von sechs der sieben Zeilen verdoppeln sich von Spalte zu Spalte;
die Zeile des Dorfes selbst folgt der Verdoppelung in ihrer mittleren Zahl
nicht und steht als geschrieben, der Herausgeber wird sie entscheiden.
