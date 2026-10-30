# AGAD 1/169/0/1/1745

One document on six pages: part of a table of the villages of a district of
South Prussia, with the houses, churches and inhabitants of each. Added on
2026-10-12 and 13 at the editor's request: the pages cut from three scans,
the table read from the scans in the working session (there was no
transcription), built as a table, summarised in both languages, given an
English version and its page. **Checked by the editor line by line and
published at their word on 2026-10-13.**

Everything about how the holding was made is in the docstring of
`intake/holding.py`. The reading itself is `intake/table.csv`. The clean
spreadsheet of the table, to keep, is `AGAD_1_169_0_1_1745_table.xlsx` in
this folder (`holding.py --archive`): the table as written, the table in
English, and a sheet on the source and the conventions.

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
- **Folds** (3122, 2625, 2632) were read off strips of the gutter. The
  editor looked at them on the fold page and let them stand (2026-10-13:
  "The folds look fine as you set them"). There is no `intake/folds.json`;
  the numbers in `holding.py` are the ones in use.

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
  spreadsheets keep them in two columns so each can be checked.
- **Figures.** The stop after each figure and number is left out. The
  clerk's dash in an empty column is "—".
- **The tailed stroke.** The clerk ends a shortened name with a stroke that
  drops below the line, like a z with a tail, mostly followed by a colon or
  a period: "Grab" + stroke + colon, "Szyman" + stroke + period. It is an
  abbreviation sign and not a letter. It is given as a period, or as the
  colon where he set one: "Kurow Grab:", "dito Szyman.", "Police Kramsk.".
  The editor was asked whether they wanted it shown another way; they
  checked the table with it and changed nothing about it, and their own
  corrections follow it ("Groi."). It stands.
- **"Szyman." is short for Szymanowice** (the editor, 2026-10-13). "dito
  Szyman." (193) is the Nowa wieś of Szymanowice, which is itself entry
  280. The text keeps the short form; the note on the line says what it
  stands for.
- **Diacritics** are given where a mark is on the page and not supplied
  where there is none. The editor's check added the marks the first reading
  had missed or doubted (Kuźnica, Koźmin, Łomow, Myżakow, Ołszyny, Ośiek,
  Ośiecza, Pępoćin, Rudźica, Sługoćin, Wardężynek): the clerk marks a c, s
  or z before an i, which modern Polish does not, and it is kept.
- **No mark of doubt is left.** The notes still in the last column of
  `table.csv` describe the page (a name shortened with the tailed sign, a
  name entered twice); the editor cleared every note that was a doubt.

## The editor's check (2026-10-13)

The editor went through `review/agad1169011745/table_check.xlsx` (each line
beside a picture of the same line of the scan), corrected 25 names, took
away the six "[?]" and cleared 24 notes of doubt. No figure was changed. It
came back with `holding.py --take <file> --apply`.

| No. | First reading | The editor |
|---|---|---|
| 143 | Kuznica Janisz: | Kuźnica Janisz: |
| 144 | d° Kozmin: | d° Koźmin: |
| 156 | Leysce[?]. | Leysce. |
| 158 | Lęzec. | Lęka. |
| 166 | Lomow. | Łomow. |
| 168 | Lubinia[?] wielka | Lubinia wielka |
| 182 | d° Bienna[?]. | d° Bienna. |
| 184 | Mokre Groice[?] | Mokre Groice |
| 188 | Myzakow. | Myżakow. |
| 189 | Myzakowskie | Myżakowskie |
| 194 | dito Trąmpcz. | dito Trąmpczyn. |
| 204 | Olszyny. | Ołszyny. |
| 205 | Osiek mały. | Ośiek mały. |
| 207 | Osiecza. | Ośiecza. |
| 217 | Pępocin | Pępoćin |
| 221 | Piskoszew[?]. | Piskoszew. |
| 229 | d° wsrzednie[?] | d° wsrzednie |
| 246 | Rudzica | Rudźica |
| 254 | Sięszyce. | Siąszyce. |
| 255 | Siekierzyn. | Siekierszyn. |
| 256 | Sięszew. | Sierszew. |
| 261 | Sługocin | Sługoćin |
| 262 | Sługocinek | Sługoćinek |
| 282 | d° d° Grod. | d° d° Groi. |
| 297 | Wardęzynek. | Wardężynek. |

Three things about it that a later session should know:

- **Two periods were put back from the scan.** The editor's cells for 156
  and 158 came back as "Leysce" and "Lęka", without the period that stands
  after both names on the page; it went with the "[?]" when the cell was
  retyped. They are "Leysce." and "Lęka.". The editor was told.
- **194, "dito Trąmpczyn."** The page has "Trąmpczy" and the tailed sign;
  the first reading had missed the y. The editor writes the n the sign
  stands for. Their form is kept and the note on the line says what is on
  the page. The same sign in 283 follows "Trąpcz" and stays "Trąpcz.".
- **158, "Lęka."** The first reading saw more letters after the k
  ("Lęzec" or "Lękec"). The editor's reading stands.

## The check of the figures

`holding.py` with no argument checks that in every line men and women add
up to the sum, the two sums to the total, and the lines of each page to its
Latus in all nine columns. All hold. This is the witness for the figures:
a misread digit breaks a sum. On the first reading nothing had to be
corrected for it, and the editor's check changed no figure. Figures written
over others, which the sums confirm: the sum of 149, the women of 213, the
sum of 281, the total of 166.

## Worth knowing from the reading

- Trąbczyn is "Trąpczyn" (291): 32 houses, 1 church, 51 male and 114
  female. More than twice as many women as men is unusual in this table
  and is what the page has; the sums of the line and of the page agree
  with it.
- "Haul. dito." (292) after it is the Trąbczyn Hollander settlement: 34
  houses, 271 people, larger than the village.
- "Haul. Lazy." (150), 5 houses, is probably the Łazińskie Olędry, one of
  the two Olęder colonies of the Trąbczyn estate, and not the village of
  Łazy (editor, 2026-10-14). It names neither the old nor the new colony
  and is not matched to either place entry; the English keeps "Lazy." as
  written.
- Two entries are both "Międzylesie." (176 and 177), with different
  figures.
- "Nowa wieś" has four entries (192 to 195), told apart by a second word:
  "Bru.", "Szyman.", "Trąmpczyn.", "Wierzchy". The edition's Nowawies (the
  place entry `nowawies-trabczyn`) is 194. The index finds the place
  through the words "Nowa wieś" on line 192, which is another village; the
  document does name the edition's one two lines on. The English has
  "Nowawies" in 192 for the same reason (the edition's rule for the name).
- "Stara Huta" has three (281 to 283): "Lukom.", "Groi.", "Trąpcz.".
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

## A later correction

A name or figure is changed in `intake/table.csv`; then `holding.py --write
--english --cache --archive`, `publish_translations.py --unit
agad1169011745`, and a rebuild. The summary, `about.md` and
`intake/claim_check.yml` cite entries 151, 152, 171, 251, 278, 279, 291 and
292: change them with the table. `holding.py --xlsx` writes the checking
spreadsheet again and refuses while the editor's file is in `review/`.

## Still to do

Nothing waits on the editor. Offered on 2026-10-13 and not answered: the
modern name of each village (nothing here identifies the 164 places), and a
sentence on the table in the account of the Hohenlohe-Ingelfingen years.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The heading of the table is printed, in German. It stands on a taller leaf that lies behind the written leaves and shows above each of them, so that one heading serves every page. The entries are in one clerk's hand. He wrote the kinds of place in German script and the names in Latin script. The names are Polish, in his spelling, and a number of them are shortened ("Kurow Grab:", "dito Szyman."). In every line the men and women add up to the sum given, and the lines of each page add up to its total.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The editor supplied three images from the volume. Each shows two facing pages of the table; they were cut at the fold into six page images. The printed heading, which stands on a leaf behind the written ones, is at the top of each image.

### Transcription

There was no earlier transcription. An AI model (Claude) read the table from the scans, line by line, and the editor then checked that reading against the scans, line by line, on a sheet that shows each line of the table beside a picture of the same line; 25 names were corrected. The table is given as a table: one row for each line of the page, in the page's own columns. The printed heading is given once, above the first page.

The kind of place and the name stand in one column on the page and in one cell here. The stop that the clerk set after every figure is left out, and his dash in an empty column is kept. Where he shortened a name he ended it with a tailed stroke, often followed by a colon; the stroke is given as a period, or as the colon where he set one. The names are spelt as on the page, with the marks the clerk set on the letters and no others.

### Checking the figures

Every line of the table carries its own sums, and every page its total. As read, the men and women of each line add up to the sum beside them, the Christians and Jews to the total of the line, and the lines of each page to the page's total in all nine columns. A misread figure would break one of these sums; none is broken. The names have no such check and rest on the two readings.

### Summary and translation

The summary was written in German from the table and translated into English; each statement in it was then checked against the table. The English version of the table translates the heading and the kinds of place and leaves the names as the clerk wrote them, except that Trąbczyn and Świątniki take the spelling used everywhere.
