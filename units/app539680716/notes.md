# APP 53/968/0/-/716

Albert Breyer's notebook "Łazińsk, Emilienheim, Ликвидац. табель" (archive's
title "Łazińsk [pow. słupecki, woj. poznańskie - notatki, statystyka]
1937"), with a loose sheet of 1858 laid in it: thirteen documents, 1858 to
1936, on 34 pages of the notebook and the sheet (40 document pages, as a
page holding the end of one document and the start of the next stands
under both), with the archive's title page and the cover in front. Russian,
German and Polish; six documents are tables. Added on 2026-10-14 at the
editor's request: read from the editor's photos in session (there was no
transcription), translated, summarised in both languages and
claim-checked, with its page, a timeline entry (29 June 1868) and a
paragraph in the story. **Built and committed; not published.** Waits for
the editor's look at the folds, the spot sheet and their word.

Everything about how the holding was made is in the docstrings of
`intake/holding.py` (the steps), `intake/photos.py` (the images),
`intake/text716.py` (the reading and its conventions) and
`intake/english716.py` (the English).

## Division (the editor's choice, 2026-10-14: by content)

1 the sheet of 1858 (table); 2 the Emilienheim liquidation table of 1868
(table); 3 Breyer's extracts on Emilienheim, 1870 and 1892; 4 the Łazińsk
liquidation table, Słupca, 29 June 1868 (table), with Breyer's pencil of
1875; 5 the Łazińsk servitudes (copy); 6 Breyer's counts 1875 to 1914; 7
farmers and Morgen of (by its figures) Łazińsk, 1840 to 1935 (table); 8
notes of July 1935, Huta Trąbczyńska, Orlin, Józefów and the morals of the
settlers; 9 the farmers of the Orlin Hauland Biskupice (table); 10 notes on
Orlin, July 1936; 11 the Orliny liquidation table (table, undated); 12
Breyer's notes on the separation; 13 the Orliny servitudes (copy, undated).
Places and dates: `rulings.yml`.

**A copy takes the date and era of what it copies** (editor, 2026-10-14:
"a copy of an 1828 document from 1939 should not belong to the 20th
century"). The holding was first built as eleven documents, two of which
held a copy and Breyer's own notes together; they were divided the same
day (old 5 into 5 and 6, old 11 into 12 and 13; numbers from 6 on moved).
Documents 1 to 5, 11 and 13 stand in the era `wlodzimierz` (per-document
`era:` in `rulings.yml`), the rest in the holding's `twentieth-century`.
Document 3 is dated by its first entry (26 November 1870), 5 to 1868 (the
year of the table it follows), 11 and 13 are undated.

## Images

The editor's raw photos IMG_5159 to IMG_5180 (CR2) in the unit's folder.
`intake/photos.py` takes the camera's full-size JPEG out of each and cuts
it to the paper (BOXES; IMG_5160 turned 90°) into `photos/`;
`holding.py --crop` cuts the openings at the fold (FOLDS, placed in
session) into `processed/`. IMG_5159: only the archive's title page is
taken (editor). IMG_5168 repeats IMG_5169 and is not used; the blank
inside front cover (5163_a1) is left out. The fold page is
`review/app539680716/folds/index.html` (`holding.py --sheet`); the editor
has not yet looked at it.

## The reading

68 marks of doubt. The tables follow the edition's convention (number
first, name second; abbreviated numbers in full; the copyist's dash after
a name dropped; a heading repeated on a page given once). In the Łazińsk
table Breyer's pencil of 1875 stands in the name cell after " — ".

- **Breyer's sum on 5176_a2** (document 10) is 1157.69 Morgen; his figures
  (17 + 370 + 464.69 + 300) make 1151.69. The photo shows the figures as
  read. The summary says so; the text is not corrected.
- **The heading of document 9** (5174_a2) is four lines of Kurrent. Read
  first as "[?] von dem Orliner Hauland Biskupice [?] [?] [?] [?] [?]";
  read again on a closer picture (2026-10-14) as "... gehörig, sämtlich auf
  das Buch ...". Not put into the text: offered on the spot sheet.
- **Spot sheet** "Readings in Breyer's Łazińsk notebook": 17 rows
  (`intake/spot_sheet.py`, port 4102), the readings a name, a place, a
  heading or the sense rests on. Not asked: the doubtful names of the
  Russian tables (documents 2, 4, 11) and the pencil of 1875, which the
  editor may not read in Cyrillic; the rest of document 8's marks.

## The English

`intake/english716.py`. In the tables only names and words are translated
and every figure keeps its cell; Russian names are transliterated letter by
letter (Shults Gotfr.), without the final hard sign. A cell holding a
figure of four digits inside words ("4420 roubles") is written quoted, as
the house forms group it (4,420) and an unquoted comma would split the
cell (`holding.py`, `english()`).

## Summaries

`intake/summaries716.py`, claim-checked in `intake/claim_check.yml`: 86
statements, 16 weakened or cut (the first draft told what the tables do
not say, counted rows wrongly where numbers are skipped or doubled, and
named people from the Russian tables in German forms).

## Index and checks

- People: `kuh` shut out of document 8 ("Kuh", a cow), `neumann` out of
  document 9 (a farmer of Orlin, not the edition's Neumann).
- Glossary: Kl., Wirte and dt. (after "geb.") ruled out.
- The translation check raises "Schenk" in document 8: it is "schenkte"
  (gave), not the name. Nothing to do.

## Open

- The editor's look at the folds and their answers on the spot sheet.
- Whether 1858 already falls in Włodzimierz's years or still in his
  mother Michalina's: the edition knows only that he held the estate in
  1860. The sheet stands in `wlodzimierz`, the nearest era.

## Damage

None recorded.
