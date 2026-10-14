# APP 53/968/0/-/669

Albert Breyer's pencil notebook of July 1936 on Łazińsk and Emilienheim,
German settlements of the commune of Trąbczyn: one document of 35 pages
with its covers, in German. Added on 2026-10-14 at the editor's request:
read from the scans in session (there was no transcription), translated,
summarised in both languages and claim-checked, with its page. **Built and
published at the editor's word on 2026-10-14.** The editor answered the spot sheet of ten
readings (2026-10-14); the rest of the reading is unchecked.

Everything about how the holding was made is in the docstring of
`intake/holding.py`; the English is `intake/english.py`.

## Document 2, "V. Grodziec Juli 1936" (added 2026-10-14)

At the editor's request, after the holding was published, the notebook of
the raw photos IMG_5192 to IMG_5205 was added as document 2 (the editor had
first chosen the archive's scans only; this is the second notebook of the
four, the one their English notes render). Not published.

- **Images**: `intake/photos.py` takes the camera's full-size JPEG out of
  each CR2 and cuts it to the notebook (BOXES) into `photos_V_Grodziec/`
  under the scans folder; `holding.py --crop2` cuts them at the fold into
  `processed/` like the scans. Page ids `5192_a` (the cover), `5193_a2` to
  `5205_a1`; the blank inside covers `5193_a1` and `5205_a2` are left out.
- **IMG_5205** carries the EXIF orientation 6, so viewers show it on its
  side, which is why the editor asked for it turned; the preview inside the
  file is stored unturned and is upright. Nothing to turn.
- **Reading**: `intake/notebook2.py` (TEXT2, and the English ENGLISH2),
  25 pages, 329 lines, 33 marks of doubt. Read in three strips a page at
  about four times the size. One page in Kurrent (5199_a1) is the weakest.
  The editor's "Breyer Notes.md" was compared after the reading and agrees.
- **Summary**: `S[2]` in `holding.py`, claim-checked in
  `intake/claim_check.yml` (15 statements, three weakened).
- **Spot sheet** "Readings in Breyer's second notebook", 15 rows
  (`intake/spot_sheet4.py`, rows in `intake/readings4.csv`, port 4102).
- **Index**: Koppe, Küster and Stanisław Miączyński shut out of document 2
  ("Koppen" is sheaf stacks, the Küster is the sexton of Józefów, the Count
  of about 1911 is a later, unidentified Miączyński); Holland as for
  document 1. The surname-only "Lipski" of the name list is found twice:
  once the owner of the Chocz estate about 1790, once "Lipski" as the new
  name of Nowo-Lipsk; neither is the 9454 Lipski. Left: the name list has
  no way to shut a document out.
- The glossary entry Morgen now also takes "Mor." after a figure.

## Provenance

Archiwum Państwowe w Poznaniu, fonds 968 (Albert Breyer - spuścizna), unit
669, "Grodziec [Notatki dotyczące Grodźca, Józefowa Zamentu, Łazińska]": a
bundle of Breyer's field notebooks. The third holding from these papers,
after 53/968/0/-/801 and -/783.

- **Which notebook.** The editor photographed four notebooks of the unit in
  April 2023 (raw files IMG_5181 to IMG_5210 in the unit's folder) and has
  the archive's scans of one (Image00001 to Image00018, folder "Notes on
  Łazińsk"). **The holding is that one notebook only** (editor,
  2026-10-14). The others: a notebook of church-book extracts, Grodziec
  1938 (IMG_5182 to 5191); "V. Grodziec Juli 1936" (IMG_5192 to 5205); one
  on Białobłoty and Dembe (IMG_5206 to 5210).
- **The editor's "Breyer Notes.md"** in the scans folder is a partial
  English rendering of "V. Grodziec Juli 1936", not of this notebook. Not
  used.
- **Images.** Image00001 the front cover; Image00002 to Image00018
  openings, cut at the fold (proposals from `courtbook.find_fold`; the
  editor has not placed them). Page ids `0001_a`, `0002_a1` ... `0018_a2`.
  Page n of the document: 1 the cover, 2 inside the front cover, then in
  order; 35 inside the back cover.

## What the notebook is

Written from the front in Łazińsk and Emilienheim (cover: "Juli 1936",
"Łazinsk", "Emilienheim"). The back pages, written from the other end, are
a log of his photographs (exposure number, subject, aperture "Bl.", filter
"Gf." or "Ohne", time, hour); page 33 is headed "Juli 1935" and names
Gostynin, Leonberg and Grabie, another district. Whether the log was
written a year before the notes, in the same book, the page does not say.
On page 10 the stamp of the village mayor of the colony ("GROMADA
ŁAZIŃSKA KOLONJA / SOŁTYS / GMINA Trąbczyn") stands under "Kolonja
Łazińsk", and is transcribed. Sketches of houses, barns and grave boards
(pages 5, 9, 30) are not.

## The reading (2026-10-14)

All 35 pages read in session from the archive's scans, in strips at about
twice the size; the lilac inside covers in the red channel. 88 marks of
doubt; the two inside covers (pages 2 and 35) are barely legible and carry
about a third of them. Field names and a few notes are in Kurrent (pages
8, 9, 22, 23). The settlers' Low German is quoted as written ("ick war do",
"er hud", "jejen").

**The spot sheet "Readings in Breyer's notebook"** (ten rows, each with a
picture of its place on the page) asks the editor about the readings a
name, a date or a number rests on: `python pipeline/review/queries.py
--unit app539680669 --sheet readings.csv` (port 4102), with the built site
on port 4000. Rows and pictures are made by `intake/spot_sheet.py`; a copy
of the rows is `intake/readings.csv`. The first button is what the text
has now. Worth the editor's eye beyond the sheet: the inside covers.

**The editor's answers** (2026-10-14, `readings_answers.json`), in TEXT
and the English: Wagelt[?] (not Wagels), 17. IV 1832, Halwege, Hormann[?]
(not Hossmann), Neumann L. 1889 – 1849 (as the editor reads it; the years
run backwards as written), Włodzimierow (the editor's reading of what was
read Wlodziemen), Bärwinkel. Gullat[?], 1928[?] and Wolwachówka[?] stand.
Three of the ten came out different from the first reading: the readings
still marked deserve the same look. 83 marks remain: 29 on the two inside
covers, 12 on the Kurrent page 8, 7 in the photograph log, 35 in the
rest.

**The second spot sheet, "More readings in Breyer's notebook"**
(2026-10-14, at the editor's request for the most uncertain): 29 rows,
made by `intake/spot_sheet2.py` (copy of the rows `intake/readings2.csv`),
served on port 4102. Left out: the inside covers and the photograph log.
The pictures were each looked at; a line's place on the page is worked out
at the pitch of the ruled lines and moved by `SHIFT` where the writing
does not keep to it.

**The editor's answers on the second sheet** (2026-10-14,
`readings2_answers.json`) are in TEXT and the English; the list is in the
docstring of `intake/holding.py`. Of 29 rows, 14 were settled outright and
eight more changed with some doubt left; seven could not be told. The ones
that change the sense: "Strażniki", a village, where Claude read the name
"Krainik"; "Noga", a field name that also stands on page 13, where Claude
read "Kroge"; "Swięcer" (of Swięcia, a place of the edition, matched),
where Claude read "Smięcer"; "St[?]pin", where Claude read "Sm…"; "Mühle"
for "Müller". 70 marks of doubt remain.

**The third sheet, "Sm or Sw in Breyer's notebook"** (three rows,
`intake/spot_sheet3.py`, port 4102): the two "Smięcia" on page 22, read
without doubt, which may be Swięcia (an estate with a farm Broniki; the
first field name there is "Bronikel"), and the second "[Sm…?]" on page 34.
Breyer's S before m or w, and before t, is not to be trusted to the first
reading. **Answered (2026-10-14):** Swięcia both times, and St[y?]pin;
Swięcia is now matched three times in the notebook.

## The English and the summary

Written in session (`intake/english.py`, `S` in `holding.py`). The
translation check's flags were followed: Pyzdry for Peisern, Poznań for
Posen, Wrocław for Breslau (given once as "Wrocław (Breslau) hymn books"),
village mayor for Schulze. Four flags remain by choice: "Neu-Warschau", a
field name kept in German with its gloss, and the bracketed "Breslau".
The summary's 16 statements were checked against the reading
(`intake/claim_check.yml`): two weakened, none rests on a doubtful word.

## People and places

- **Shut out of this document** (`not_in` in `reference/people.yml` and
  `places.yml`): Neumann (the teacher of Łazińsk is not the edition's
  Neumann), Geheimer Finanzrat Schulze ("der Schulze i. Drzewce" is a
  village mayor), Holland (the Olęder settlements, "Altes Holland"), and
  Warszawa ("Neu-Warschau" is a field name).
- **"Emilien¬heim"** was matched as the name Emilie by the name list made
  from the corpus; such a pattern now refuses a word followed by the
  line-break mark (`pipeline/build/entities.py`; nothing else in the
  edition changed).
- **Zelmer**: "Zelmer Ed.", teacher in Łazińsk for 34 years, is matched to
  the Zelmer family entry, which is right.
- Łazińsk, Emilienheim, Michalinów, Włodzimierów have no matching place
  entries here; "Łazińsk" of 1936 is not linked to either Łazińskie Olędry
  (a question for the editor).

## Era

**The twentieth century of the estate** (editor, 2026-10-14): era
`twentieth-century`, made that day in `reference/eras.yml` under a working
name, "The twentieth century"; the editor will name it.

## Still to do

1. **The editor's answers** on the spot sheet, and their look at the folds
   (`review/app539680669/folds/index.html`).
2. **The editor's word** on whether "Łazinsk" of 1936 is both colonies
   together, and the era's name.
3. Published 2026-10-14.
4. Not done: a timeline entry or a sentence in the era essay (the notebook
   bears on the settlers, not on the owners of the estate); the other three
   notebooks of the unit.
