# APP 53/21/0/-/Pyzdry Gr.115

One document on one page: the head of a table of the parish of Trąbczyn,
page 543 of the Relationes [protocollon] of 1791-1792. Added on 2026-10-26 at
the editor's word, built from the editor's own transcription
(`intake/table.csv`); the editor's rulings of the day were given in chat,
while they were away from this PC. The model is APP 53/64/0/-/Kalisz Tab.21
(`units/app53640kalisztab21/intake/holding.py`).

## Provenance

Archiwum Państwowe w Poznaniu, fond "Księgi sądu i urzędu grodzkiego w
Pyzdrach", unit "Relationes [protocollon] 1791-1792" (szukajwarchiwach.gov.pl,
jednostka 984641). The archive's description of the fonds and its account of
the creator, as the editor pasted them, are in
`reference/sources/app_ksiegi_sadu_i_urzedu_grodzkiego_w_pyzdrach.md` and on
the holding's page.

- **Images.** The folder holds `543_trim.jpg` (the editor's own trim of page
  543 of the register, 2659×4410) and `542v-543.jpg` (the spread). **Only
  543_trim.jpg is used** - the editor's word (2026-10-26): page 543 is the
  page of the unit in focus. `crop_scans.py` is not run; `intake/holding.py
  --crop` copies the one page whole as `0543_a.jpg` (`courtbook.cut`, the
  Kalisz Tab.21 way; a single page has no fold to place). The scans block's
  `raw_glob` is `*.jpg` because that is what `stage_pages.py` takes its stem
  from; the folder's other image never enters `processed/`.
- **Part of a page.** Only the first half of the page is transcribed - the
  editor's word: the relevant information is the table, and the rest of the
  page belongs to the entry after it.

## The transcription

The editor's CSV ("Relationes [protocollon] 1791-1792 (53_21_0_-_Pyzdry
Gr.115) - Sheet1.csv"), kept as `intake/table.csv` as received: one heading
row and seven rows of the parish of Trąbczyn, five cells each - parish,
name, dymy rolne, gara zyta, gara owcza. Written into `corpus.txt` as a
table (`doc_type: register`, `tables: ["1"]`), the heading row as the
table's head.

- **The one change: "Parofie" → "Parafie"** in the heading - the editor ruled
  it in chat (2026-10-26: "It should be Parafie"), applied by `--correct` and
  logged in `transcription_decisions.csv`. Everything else stays as the
  editor typed it, diacritics included where they gave them: Kuznia (no ź),
  Luzne (no ł), Nowawieś (with ś), Wies (no ś).
- **The document carries no date in the transcription**; `rulings.yml` puts
  it under `no_date`. The holding's `date_span` is 1791-1792, the archive's
  title. The editor's word of 2026-10-26 ("use my transcription, which is
  correct") settles it: no dated heading is carried, and the document stays
  undated.

## The figures

In six of the seven rows the figures double from column to column (h, 2h,
4h): Plebania 4-8-16, Nowawieś 5-10-20, Osiny 6-12-24, Łazy 5-10-20, Kuznia
Maryantów 1-2-4, the Hollendry 31-62-124. The village's own row reads 21,
**22**, 84, where the doubling would give 42 in the middle column. Figures
are never corrected from arithmetic (docs/EDITORIAL_RULES.md): the row
stands as written, and the editor said (2026-10-26) they will resolve it
later. It is in NEEDS_CONFIRMATION.

## Rulings given in chat (2026-10-26, the editor away from this PC)

- **"It should be Parafie"** - the heading's first cell; applied and logged.
- **"Yes, Maryantow is Marianton"** - Kuznia Maryantów is the Marianton of
  the edition: the place named among the parish's villages in the visitation
  of 1791 (adwl85, document 1, "Maryanton") and the seat of the Hohenlohe
  patrimonial court for Trąbczyn ("Actum Marianton", app5371057). Worked
  into `reference/places.yml` (`mariantow`, the match now also takes
  "Maryantów"), and the entry's comment records that the ruling supports
  reading the unclear "Marianton" of 9454 letter 136 as this place.
- The Trąbczyn figure: "I'll resolve ... later" - left as written.
- **"No spot sheet is necessary - use my transcription, which is correct"**
  (2026-10-26, in chat): the transcription is the authority for the whole
  table, and the three questions the sheet was to ask are answered by it.
  The figures stand as transcribed - the village's row is 21, 22, 84; the
  doubling of the other rows is an observation of the table, recorded here
  and in the holding's account, and nothing is built on it. The two column
  headings "gara zyta" and "gara owcza" stand as written, and the English
  keeps the words. No dated heading is carried: the transcription is the
  entry's content, and the document stays undated (`no_date` in
  rulings.yml). The sheet was taken down and removed from the branch; the
  server was stopped.

## The machinery: a table with no entry numbers

`unitlib.table_of` sorted a table by its first column's numbers and crashed
(`StopIteration`) on a table that has none - the first crash of the build.
Extended (2026-10-26): where no row has a number in its first cell, the rows
that carry figures are the body and the rows above the first of them are the
head; no row is a page's total, and the first cell belongs with the name
(class `name`, not `no`). The check that no existing table changes:
`pipeline/review/verify_table_of_diff.py` runs the pristine `table_of` (git HEAD)
and the new one over every document `rulings.yml` lists under `tables:` -
12 documents in 5 units, the outputs identical.

## The index

Match extensions in `reference/places.yml`, each counted before it was made
(mistake 7 of docs/NEW_UNIT.md), every hit's line read:

- `mariantow` takes `Maryant[oó][nw]`: 4 hits in 3 documents - ours
  ("Kuznia Maryantów"), the Prussian table's "Maryantow." (agad1169011745,
  row 175, unmatched before, the same place), and the visitation's
  "Maryanton" (adwl85, already matched).
- `lazy-trabczyn` takes `(?<=,)Łazy(?=,)`: 2 hits - ours and the hearth-tax
  register's entry 180 (app53640kalisztab21), the same village by the
  entry's own note.
- both Olęder colony entries take `Hollendry(?= Luzne Stare i nowe)`: 1 hit,
  ours. One row of the table names both colonies together, as the
  visitation's "Olędry nowe i stare" does.

The other forms needed nothing: "Osiny" and "Nowawieś" already match their
entries; "Huta" (13 hits in 8 documents, the common noun) has no place entry
and gets none without the editor's word; "Kuznia", the smithy, is the
descriptor of the Mariantów row.

## What the site needed

`about.md`, `process.md`, and their German, with the fonds text; the glossary
run after the translation (0 candidates); the index extensions above.

## Open

- "z Hutą" in the row of the Hollander settlements: whether the Huta is a
  distinct place of the colonies or the colonies' smith, and so whether a
  place entry is wanted. No entry until the editor rules
  (NEEDS_CONFIRMATION).
- The rest of the page (the entry after the table) and the rest of the
  volume are not transcribed; the editor's five folders (docs/TODO.md,
  section 6) has this holding's text now only in part.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

The holding came ready transcribed: the editor's own reading of the table,
given as a spreadsheet, one heading row and seven rows of five cells each.
Everything on the holding's pages is made from it.

The folder holds two photographs: the editor's own trim of page 543 and the
spread of pages 542v and 543. Only the trim is used, at the editor's word:
page 543 is the page that holds the table. The trim is a single page
already, so it is shown whole, without cutting.

The transcription covers the table in the first half of the page, at the
editor's word; the rest of the page belongs to the entry after the table.
The document therefore has one page and eight lines: the heading row, which
opens the table, and the seven rows of the parish.

One reading was changed, at the editor's word on 26 October 2026: the
heading's first cell, "Parofie", is "Parafie". Everything else stands as
the editor typed it, diacritics included only where they gave them.

The table has no column of entry numbers: the parish stands in the first
cell, filled on the village's own row and empty under it, and the figures
follow.

The figures of six of the seven rows double from column to column; the
village's own row does not follow the doubling in its middle figure and
stands as written – the transcription is the editor's own and correct.
