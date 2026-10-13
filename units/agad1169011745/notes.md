# AGAD 1/169/0/1/1745

One document on six pages: part of a table of the villages of a district of
South Prussia, with the houses, churches and inhabitants of each. Added on
2026-10-12 and 13 at the editor's request: the pages cut from three scans,
the table read from the scans in the working session (there was no
transcription), built as a table, summarised in both languages, given an
English version and its page. **Not yet published, and not yet checked by
the editor**: their check is on the spreadsheet
`review/agad1169011745/table_check.xlsx`.

Everything about how the holding was made is in the docstring of
`intake/holding.py`. The reading itself is `intake/table.csv`.

## Provenance

Archiwum Główne Akt Dawnych, Warsaw, fonds 169 (Generalne Dyrektorium.
Departament Prus Południowych), series 1, unit 1745: "Die neuesten
topografischen Nachrichten von Südpreussen". The editor gave the reference,
the title, the fonds and the archive's description of the fonds
(`reference/sources/agad_generalne_dyrektorium_prus_poludniowych.md`); the
year 1797 is in the name of their folder and is taken as the archive's date
for the volume. Nothing on the six pages gives a date or names the district.

- **Images.** Three, each an opening: `401-402.jpg`, `403-404.jpg`,
  `404-405.jpg`. The third shows pages 405 and 406, whatever its name says.
- **Pages.** Numbered in pencil 401 to 406. Page ids: `0401_a1`, `0402_a2`,
  `0403_a1`, `0404_a2`, `0405_a1`, `0406_a2` (the pencil number and the
  side of the opening).
- **The heading** is printed and stands on a taller leaf behind the written
  leaves (pencil "397" on its left half, a struck-out "408" on its right),
  showing above each of them. The editor: "the headers stay the same on
  each page". It is transcribed once, at the head of the first page; the
  site repeats it over every page of the table.
- **Folds** are first proposals (3122, 2625, 2632), read off strips of the
  gutter. The fold page is `review/agad1169011745/folds/index.html`; the
  editor has not placed them yet.

## The table

Entries 140 to 303, 164 of them, alphabetical from Kurow to Wierzbna, and
the six page totals "Latus 6." to "Latus 11.". Columns: No.; Nahmen der
Dörfer; Anzahl der Häuser; Anzahl der Kirchen; Menschen-Zahl, Christen
(männlichen Geschlechts, weiblichen Geschlechts, Summa Christen); Juden
(männlichen Geschlechts, weiblichen Geschlechts, Summa); Summa aller
Menschen. On the page "männlichen" and "weiblichen" share the one word
"Geschlechts", printed across both columns; each column is given the whole
phrase.

The district is not named. The places are those of the country round Konin
(Kurow Koninsk., Ląd, Lądek, Rzgow, Stare miasto, Rychwał, Tuliszkow), and
Konin was a district of the Kalisz chamber; that it is the Konin district
is an inference and is written as one wherever it is said.

## How it is written down

- **Kind of place and name in one cell.** On the page they stand in one
  ruled column, the kind in German script (Dorf, Haul., Mühle, Vorw.,
  Kloster, Krug, Alt Haul.), the name in Latin script. `table.csv` and the
  spreadsheet keep them in two columns so each can be checked.
- **Figures.** The stop after each figure and number is left out. The
  clerk's dash in an empty column is "—".
- **The tailed stroke.** The clerk ends a shortened name with a stroke that
  drops below the line, like a z with a tail, mostly followed by a colon or
  a period: "Grab" + stroke + colon, "Szyman" + stroke + period. It is an
  abbreviation sign and not a letter (Grabieński, Szymanowski and Kramski
  have no z there). It is given as a period, or as the colon where he set
  one: "Kurow Grab:", "dito Szyman.", "Police Kramsk.". In "d° d° Grod."
  and "Tarnowa Brud." the same stroke could be read as the letter z
  (Grodz., Brudz.); they are given like the rest. **One question for the
  editor**, on the spreadsheet: whether they want the stroke shown some
  other way.
- **Diacritics** are given where a mark is on the page (Ląd, Małoszyn,
  Myśliborz, Trąpczyn) and not supplied where there is none (Lagiewniki,
  Krolewska, Lomow).
- **Doubt.** Six names carry "[?]": Leysce (156), Lubinia (168), Bienna
  (182), Groice (184), Piskoszew (221), wsrzednie (229). `table.csv` has a
  note on these and on 29 other lines (a letter that could be one of two, a
  figure written over another). The notes are in the spreadsheet beside
  each line.

## The check of the figures

`holding.py` with no argument checks that in every line men and women add
up to the sum, the two sums to the total, and the lines of each page to its
Latus in all nine columns. All hold. This is the witness for the figures:
a misread digit breaks a sum. On the first reading nothing had to be
corrected for it. Figures written over others, which the sums confirm: the
sum of 149, the women of 213, the sum of 281, the total of 166.

## Worth knowing from the reading

- Trąbczyn is "Trąpczyn" (291): 32 houses, 1 church, 51 male and 114
  female. More than twice as many women as men is unusual in this table
  and is what the page has; the sums of the line and of the page agree
  with it.
- "Haul. dito." (292) after it is the Trąbczyn Hollander settlement: 34
  houses, 271 people, larger than the village.
- Two entries are both "Międzylesie." (176 and 177), with different
  figures.
- "Nowa wieś" has four entries (192 to 195), told apart by a shortened
  second word: "Bru.", "Szyman.", "Trąmpcz.", "Wierzchy". The edition's
  Nowawies (the place entry `nowawies-trabczyn`) is 194. The index finds
  the place through the words "Nowa wieś" on line 192, which is another
  village; the document does name the edition's one two lines on.
- "Stara Huta" has three (281 to 283): "Lukom.", "Grod.", "Trąpcz.".
- Places of the edition found by the index: Trąbczyn, Łukom, Szetlewek
  (which also takes Szetlew), Świątniki, Oleśnica, Swięcia, Osiny, Skokum,
  Lądek, Nowawies. "Kurow Koninsk." is not the town of Konin and the
  village "Ostrow" not the town of Ostrów: both entries are shut out of
  this document in `reference/places.yml`.

## What the site needed

A table with a heading of three levels and with a total at the foot of
every page was new. `unitlib.render_table` now takes a row for each level
of a heading and sets off a row without a number between the entries (a
page's total); `publish_translations.py` accepts an English table whose
heading is translated. Oe 1 Bü 9454, document 303, the only other table,
comes out as before.

## Still to do

1. **The editor's check** of the spreadsheet. Their corrections come back
   with `holding.py --take <file> --apply`, then `--write --english
   --cache`, `publish_translations.py`, the summary and `about` texts if a
   figure or name they cite changed, and a rebuild. The count of "[?]" is
   given by hand in `process.md`, `process_de.md` and these notes.
2. **The folds**, on the fold page.
3. **Publishing**, at the editor's word.
4. Not done, and for the editor to say whether they want them: the modern
   name of each village (nothing here identifies the 164 places), and a
   sentence on the table in the era essay.
