# APP 53/968/0/-/716

Albert Breyer's notebook "Łazińsk, Emilienheim, Ликвидац. табель" (archive's
title "Łazińsk [pow. słupecki, woj. poznańskie - notatki, statystyka]
1937"), with a loose sheet of 1858 laid in it: eleven documents, 1858 to
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
(table); 3 Breyer's notes on Emilienheim, 1870 and 1892; 4 the Łazińsk
liquidation table, Słupca, 29 June 1868 (table), with Breyer's pencil of
1875; 5 the Łazińsk servitudes and Breyer's counts 1875 to 1914; 6 farmers
and Morgen of (by its figures) Łazińsk, 1840 to 1935 (table); 7 notes of
July 1935, Huta Trąbczyńska, Orlin, Józefów and the morals of the settlers;
8 the farmers of the Orlin Hauland Biskupice (table); 9 notes on Orlin,
July 1936; 10 the Orliny liquidation table (table, undated); 11 the
separation and the Orliny servitudes. Places and dates: `rulings.yml`.

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

- **Breyer's sum on 5176_a2** (document 9) is 1157.69 Morgen; his figures
  (17 + 370 + 464.69 + 300) make 1151.69. The photo shows the figures as
  read. The summary says so; the text is not corrected.
- **The heading of document 8** (5174_a2) is four lines of Kurrent. Read
  first as "[?] von dem Orliner Hauland Biskupice [?] [?] [?] [?] [?]";
  read again on a closer picture (2026-10-14) as "... gehörig, sämtlich auf
  das Buch ...". Not put into the text: offered on the spot sheet.
- **Spot sheet** "Readings in Breyer's Łazińsk notebook": 17 rows
  (`intake/spot_sheet.py`, port 4102), the readings a name, a place, a
  heading or the sense rests on. Not asked: the doubtful names of the
  Russian tables (documents 2, 4, 10) and the pencil of 1875, which the
  editor may not read in Cyrillic; the rest of document 7's marks.

## The English

`intake/english716.py`. In the tables only names and words are translated
and every figure keeps its cell; Russian names are transliterated letter by
letter (Shults Gotfr.), without the final hard sign. A cell holding a
figure of four digits inside words ("4420 roubles") is written quoted, as
the house forms group it (4,420) and an unquoted comma would split the
cell (`holding.py`, `english()`).

## Summaries

`intake/summaries716.py`, claim-checked in `intake/claim_check.yml`: 83
statements, 16 weakened or cut (the first draft told what the tables do
not say, counted rows wrongly where numbers are skipped or doubled, and
named people from the Russian tables in German forms).

## Index and checks

- People: `kuh` shut out of document 7 ("Kuh", a cow), `neumann` out of
  document 8 (a farmer of Orlin, not the edition's Neumann).
- Glossary: Kl., Wirte and dt. (after "geb.") ruled out.
- The translation check raises "Schenk" in document 7: it is "schenkte"
  (gave), not the name. Nothing to do.

## Open

- The editor's look at the folds and their answers on the spot sheet.
- The era: the holding stands under `twentieth-century` (Breyer's
  notebook, like 53/968/0/-/669). The sheet of 1858 and the tables of 1868
  are documents of Włodzimierz Miączyński's time copied or kept by Breyer;
  whether they should stand under `wlodzimierz` is the editor's to say.

## Damage

None recorded.
