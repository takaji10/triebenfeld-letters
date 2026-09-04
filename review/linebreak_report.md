# Line-break resolution

Every line-end wrap mark in the corpus, decided on evidence. The canonical archival text is unchanged — these decisions drive the generated *reading* copy only.

## Why this was needed

The transcription's continuation marks cannot be taken at face value. `die¬` + `serhalb` really is one word (*dieserhalb*), but `die¬` + `nöthigsten` is two, and the mark is simply an error. Roughly a third of the marks turn out not to join anything.

## Evidence

1. **This corpus** — period-appropriate; it knows that `laßen` and `nöthigsten` are ordinary words.
2. **DWDS frequency API** — lemma-aware, so inflected forms resolve (`Mitgliedern` → *Mitglied*), and its corpora include historical German. A form is treated as real at ≥1,000 hits; below that, the returns are proper-name noise.

## Results

| Outcome | Count |
|---|---|
| join | 826 |
| split | 483 |
| catchword | 5 |
| orphan | 3 |
| **total** | **1317** |

| Confidence | Count |
|---|---|
| high | 1298 |
| review | 19 |

| Reason | Count |
|---|---|
| joined form occurs elsewhere in this corpus | 536 |
| joined form unattested; both halves are real words | 470 |
| head is not a word on its own | 173 |
| crosses a page break - check by hand | 19 |
| fragment repeats the next page opening | 5 |
| nothing to continue into - the next line holds no words | 3 |
| joined form attested in DWDS (1,366 hits) | 3 |
| joined form attested in DWDS (3,181 hits) | 2 |
| joined form attested in DWDS (1,701 hits) | 1 |
| joined form attested in DWDS (2,983 hits) | 1 |
| joined form attested in DWDS (1,416,004 hits) | 1 |
| joined form attested in DWDS (96,646 hits) | 1 |
| joined form attested in DWDS (12,034,956 hits) | 1 |
| joined form attested in DWDS (1,430 hits) | 1 |
| joined form attested in DWDS (20,353 hits) | 1 |
| joined form attested in DWDS (324,313 hits) | 1 |
| joined form attested in DWDS (36,875 hits) | 1 |
| joined form attested in DWDS (28,146 hits) | 1 |
| joined form attested in DWDS (12,643 hits) | 1 |
| joined form attested in DWDS (16,446 hits) | 1 |
| joined form attested in DWDS (1,659 hits) | 1 |
| joined form attested in DWDS (184,034 hits) | 1 |
| joined form attested in DWDS (2,267 hits) | 1 |
| joined form attested in DWDS (59,881 hits) | 1 |
| joined form attested in DWDS (2,183 hits) | 1 |
| joined form attested in DWDS (65,712 hits) | 1 |
| joined form attested in DWDS (1,973 hits) | 1 |
| joined form attested in DWDS (37,345 hits) | 1 |
| joined form attested in DWDS (18,086 hits) | 1 |
| joined form attested in DWDS (2,556,573 hits) | 1 |
| joined form attested in DWDS (1,849 hits) | 1 |
| joined form attested in DWDS (6,400,337 hits) | 1 |
| joined form attested in DWDS (441,375 hits) | 1 |
| joined form attested in DWDS (17,525 hits) | 1 |
| joined form attested in DWDS (106,339 hits) | 1 |
| joined form attested in DWDS (79,073 hits) | 1 |
| joined form attested in DWDS (1,006,399 hits) | 1 |
| joined form attested in DWDS (1,040,958 hits) | 1 |
| joined form attested in DWDS (115,684 hits) | 1 |
| joined form attested in DWDS (4,305 hits) | 1 |
| joined form attested in DWDS (469,466 hits) | 1 |
| joined form attested in DWDS (4,875,601 hits) | 1 |
| joined form attested in DWDS (208,917 hits) | 1 |
| joined form attested in DWDS (10,331 hits) | 1 |
| joined form attested in DWDS (11,311 hits) | 1 |
| joined form attested in DWDS (342,694 hits) | 1 |
| joined form attested in DWDS (104,427 hits) | 1 |
| joined form attested in DWDS (460,070 hits) | 1 |
| joined form attested in DWDS (1,386,539 hits) | 1 |
| joined form attested in DWDS (343,834 hits) | 1 |
| joined form attested in DWDS (17,090 hits) | 1 |
| joined form attested in DWDS (451,216 hits) | 1 |
| joined form attested in DWDS (17,926 hits) | 1 |
| joined form attested in DWDS (2,660 hits) | 1 |
| joined form attested in DWDS (7,816 hits) | 1 |
| joined form attested in DWDS (13,464 hits) | 1 |
| joined form attested in DWDS (2,766,591 hits) | 1 |
| joined form attested in DWDS (183,499 hits) | 1 |
| joined form attested in DWDS (49,174 hits) | 1 |
| joined form attested in DWDS (259,432 hits) | 1 |
| joined form attested in DWDS (8,057,421 hits) | 1 |
| joined form attested in DWDS (2,144 hits) | 1 |
| joined form attested in DWDS (26,355,418 hits) | 1 |
| joined form attested in DWDS (97,942 hits) | 1 |
| joined form attested in DWDS (77,161 hits) | 1 |
| joined form attested in DWDS (22,506 hits) | 1 |
| joined form attested in DWDS (3,012,789 hits) | 1 |
| joined form attested in DWDS (60,650 hits) | 1 |
| joined form attested in DWDS (120,555 hits) | 1 |
| joined form attested in DWDS (200,644 hits) | 1 |
| joined form attested in DWDS (33,627 hits) | 1 |
| joined form attested in DWDS (908,791 hits) | 1 |
| joined form attested in DWDS (13,570 hits) | 1 |
| joined form attested in DWDS (2,694 hits) | 1 |
| joined form attested in DWDS (3,296,640 hits) | 1 |
| joined form attested in DWDS (81,100 hits) | 1 |
| joined form attested in DWDS (480,807 hits) | 1 |
| joined form attested in DWDS (595,843 hits) | 1 |
| joined form attested in DWDS (45,658 hits) | 1 |
| joined form attested in DWDS (1,293 hits) | 1 |
| joined form attested in DWDS (242,644 hits) | 1 |
| joined form attested in DWDS (1,631,054 hits) | 1 |
| joined form attested in DWDS (649,531 hits) | 1 |
| joined form attested in DWDS (89,995 hits) | 1 |
| joined form attested in DWDS (5,081 hits) | 1 |
| joined form attested in DWDS (41,868 hits) | 1 |
| joined form attested in DWDS (760,869 hits) | 1 |
| joined form attested in DWDS (11,883 hits) | 1 |
| joined form attested in DWDS (4,140,751 hits) | 1 |
| joined form attested in DWDS (2,280,615 hits) | 1 |
| joined form attested in DWDS (845,018 hits) | 1 |
| joined form attested in DWDS (3,839 hits) | 1 |
| joined form attested in DWDS (47,390,276 hits) | 1 |
| joined form attested in DWDS (1,848,861 hits) | 1 |
| joined form attested in DWDS (3,479 hits) | 1 |
| joined form attested in DWDS (5,731 hits) | 1 |
| joined form attested in DWDS (2,000 hits) | 1 |
| joined form attested in DWDS (59,215 hits) | 1 |
| joined form attested in DWDS (36,877 hits) | 1 |
| joined form attested in DWDS (85,594 hits) | 1 |
| joined form attested in DWDS (2,021,977 hits) | 1 |
| joined form attested in DWDS (162,925 hits) | 1 |
| joined form attested in DWDS (819,410 hits) | 1 |
| joined form attested in DWDS (4,854,247 hits) | 1 |
| joined form attested in DWDS (5,345 hits) | 1 |
| joined form attested in DWDS (29,219 hits) | 1 |
| joined form attested in DWDS (115,238 hits) | 1 |
| joined form attested in DWDS (1,411,740 hits) | 1 |
| joined form attested in DWDS (134,169 hits) | 1 |
| joined form attested in DWDS (351,293 hits) | 1 |
| joined form attested in DWDS (2,345,412 hits) | 1 |
| joined form attested in DWDS (322,270 hits) | 1 |
| joined form attested in DWDS (1,479,072 hits) | 1 |
| joined form attested in DWDS (8,569 hits) | 1 |

## Catchwords

The scribal habit of writing the next page's first word at the foot of the current page. Not broken words — joining them would manufacture nonsense ("ConContract"). Kept in the diplomatic view, dropped from the reading copy.

| Letter | Line | Fragment | Next page opens | Context |
|---|---|---|---|---|
| 133 | 9463 | `Con¬` | `Contract` | it Glenck eingeschrittenen Societeets Con¬ || Contract beym Betscher Verkauf auf gehoben |
| 140 | 10228 | `Vor-` | `Vorwerk` |  in Händen hätte nach welchen sie das Vor- || Vorwerk Abre und den grösten Theil der Wal |
| 168 | 11854 | `Win¬` | `Winnickischen` | So haben zum Beispiel die Win¬ || Winnickischen Erben dermalen wieder |
| 177 | 12464 | `be¬` | `benennung` | e. Geld Marschall Mollendorf soll Haus be¬ || benennung der neuen Dörfer die durch die D |
| 235 | 17181 | `ver-` | `verliehren` | was den verlohren geht unß Stössel ver- || verliehren der Ewr Durchlaucht mehr alt zu |

## For your review

Cases with no decisive evidence, plus every wrap that crosses a page break. The `decision` column in `linebreak_decisions.csv` is hand-editable — change a cell and regenerate.

Each was read in context; the decision column below is what the generated reading copy currently does.

| Letter | Line | Wrap | Decision | Context | Note |
|---|---|---|---|---|---|
| 6 | 420 | `defach`+`Nur` | **split** | teht gut auf jeden Falle bitte ich defach¬ || Nur zählen Sie nichts auf St. Rechnung der |  |
| 28 | 1890 | `Interodie`+`ist` | **split** | Ew. Hochfürstliche Durchlaucht Interodie- || ist mein größtes Augenmerk, und traurig |  |
| 51 | 3797 | `Wort`+`Bethney` | **split** | urm von ferne merkt so hält er gewis Wort¬ || Bethney liegt bey sich in Malsdorff sehr e |  |
| 63 | 4783 | `Pensrats`+`Es` | **split** | lii und alle Teufel und heiligen Pensrats¬ || Es glang mir den Honrichs im so weit zu re |  |
| 64 | 4972 | `anbey`+`Erbarmen` | **split** | inzeßin am Heßen Rothenburg erfolgt anbey¬ || Erbarmen sich Erer Durchlaucht und schulen |  |
| 78 | 6417 | `Ver`+`führung` | **join** | nenselben nur bloß die unterthänigste Ver¬ || führung geben, daß ich alles was in meinen |  |
| 86 | 6865 | `Kro`+`teszyn` | **split** | iegesrath Nöldichen erstattet und von Kro¬ || teszyn jener hohe Ertrag ohne Grund angeno |  |
| 87 | 7015 | `Ge`+`such` | **join** | s dringendste dem guten Monarchen mein Ge¬ || such ans Herz zu legen, damit ich keine fe |  |
| 101 | 7840 | `Vor`+`wert` | **join** |  ganz andere Bewandung. Dies ist kein Vor¬ || wert, sondern 1 Holländer Hufe, welche der |  |
| 103 | 8071 | `an`+`ſtalt` | **join** | er reelle Nachricht erhalten, auch ist an¬ || ſtalt getroffen, daß ich die Documente weg |  |
| 107 | 8376 | `Selle`+`Ubrigens` | **split** | gewisser Hoym und der Professor Selle¬ || Ubrigens man in Publicum fast alles Haare  |  |
| 136 | 9897 | `Collo`+`Mitten` | **split** | n weil er schon viel Händel mit die Collo¬ || Mitten gehabt hatt. Den dieser Strich soll |  |
| 146 | 10582 | `könt`+`Die` | **split** | ermachen, damit die Sache aufs reine könt¬ || Die Dismembration wird auf alle Fälle glüc |  |
| 176 | 12389 | `Patente`+`angeschlagen` | **split** | fingischen Besitz-Ergreifungs Patente- || angeschlagen, auch da, wo man sich von der |  |
| 178 | 12596 | `aus`+`gemacht` | **join** | alles was das Heheelohischen angrenge aus¬ || gemacht werden sollte, ehe die Reiße ange¬ |  |
| 223 | 16110 | `ange`+`so` | **split** | Güter ange¬ || so wäre Ihr Plan vortreflich; ich bitte, i |  |
| 223 | 16175 | `ver`+`oder` | **split** | len für mich geführt wurden, entweder ver¬ || oder aufgegeben gesehen habe; nach dem weg |  |
| 240 | 17455 | `Frieden`+`Ich` | **split** | gewiß einen sehr vorteilhaften Frieden¬ || Ich habe hier das erſte wohl wieder ſagen  |  |
| 272 | 19331 | `be`+`obachtet` | **join** | vieles von den Formen ab, die man be¬ || obachtet. |  |

## How to override a decision

Edit the `decision` column in `linebreak_decisions.csv` (`join`, `split` or `catchword`) and re-run `build_db.py` then `build_site_data.py`. Nothing else needs changing, and the archival text is never touched.
