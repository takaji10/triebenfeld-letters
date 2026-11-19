# I. HA GR, Rep. 7 C, Nr. 3067

One document of 16 February 1797 on six pages: the Grand Chancellor
Goldbeck's promemoria to King Friedrich Wilhelm II on the outcome of the
proceedings against the insurgents of 1794 in South Prussia and on a further
pardon (pages 1 to 3), the King's own-hand decision written beneath it,
refusing any reduction (page 3), and the list the promemoria encloses, of the
31 rebels sentenced to death, to the fortress for life or for long terms
(pages 4 to 6). Added
2026-11-19 at the editor's word, branch `trampczynski-family`.

The archive's title, as the editor gave it: "Promemoria Goldbecks mit Angaben
über das Ergebnis des Rechtsverfahrens gegen die Insurgenten und Anfragen
wegen deren Begnadigung sowie eine eigenhändige ablehnende Entscheidung des
Königs".

## Provenance

GStA PK. The editor gave the reference as "I. HA Rep. 7 C, Nr. 3067"; it is
written "I. HA GR, Rep. 7 C, Nr. 3067" with the series' GR, as its siblings
Nr. 1414, 3570, 3705 and 3709 are (the scans' file names omit GR for all of
them). Slug `ihagrrep7cnr3067`. NEEDS_CONFIRMATION asks.

Four scans as the editor gave them (Downloads\74344_Lacko\I_HA_Rep_7_C_Nr_3067\Process),
0005 to 0008, the archive's pencil folios 3 to 6; scans 0001-0004 were not
supplied (presumably the folder). 0005 and 0007 the editor had cut to the
leaf; 0006 and 0008 are openings, cut at the fold on the binding thread by
`intake/build_pages.py --crop` (the boxes are in its CROPS). Page ids: 0005_a,
0006_a1, 0006_a2, 0007_a, 0008_a1, 0008_a2.

## The document

**One document, a memorandum** (the editor, 2026-11-19: "Do not split this
into three documents - it is a single document"). It was first built as
three: 1 the promemoria, 2 the King's decision (a new kind,
`royal_resolution`, since withdrawn with its labels), 3 the list (a
`register`, its date inferred from the promemoria). Made one the same day:
the boundaries (`build_pages.py` SPEC), the rulings (one date, read; the
relations "transmits" and "answers" gone), the English (`doc1.yml`, six
pages; the King's note joins page 3), the summaries joined, the index's
`not_in`/`issued_in` moved to document 1, the timeline's two sources made
one; the paragraph ruling of the King's date ("d 16 Februariy / 1797",
joined) carried over, and a break set by hand before his note. The old
addresses /documents/ihagrrep7cnr3067/2/ and /3/ were never published.

- **Pages 1 to 3** (0005_a to 0006_a2): Goldbeck's promemoria, "Berlin den
  16ten Februar 1797". The date "d. 16 Feb. 1797" at the head of the first page
  is in another hand (a docket); kept where the editor put it. On page 3,
  under Goldbeck's signature, the King's decision, "Fr. Wilhelm / d 16
  Februariy 1797".
- **Page 4** (0007_a): the list's title page, "Liste / dererjenigen
  Südpreußischen Rebellen, ...", text line by line. It was first built as
  the table's first rows, which drew it as a caption over the column heads
  of page 5, with its line ends lost; the editor (2026-11-19): page 4 "has
  weird styling on the text and is not showing the text separated by its
  original lines. I also see table headings that don't belong there". In
  the reading, "Liste" stands as its own paragraph (a hand row in
  `paragraph_decisions.csv`), and "Vestungs¬ / Strafe" stays two words (a
  held `split` in `linebreak_decisions.csv`, as the list's cells have it).
- **Pages 5 and 6** (0008_a1, 0008_a2): the list, **a table since
  2026-11-19** (`documents: tables` with `table_pages: [5, 6]`: the
  document is a table on those pages only, the others are text). Where a
  brace joins two entries on the page, their cell is one cell reaching over
  both rows (`documents: table_merged_cells:`; the editor, 2026-11-19): the
  offence of A 1 and 2 (Wittwicki, Retznowski), and the offence and the
  month of beginning of C 20 and 21 (Czimay, Ruba), each of whom keeps his
  own length; the English the same. At first it was kept line by line, as the editor's text file
  has it, because `render_table` set every cell after the name as a figure;
  the editor then pointed to their own table of it,
  `Downloads\I_HA_Rep_7_C_Nr_3067_tables.xlsx` ("It should already be in
  table format"), which the first session had not looked for. Now:
  `intake/table_from_xlsx.py` turns the spreadsheet into `intake/table.csv`
  (one sheet per block of 0008; A and B, written there as running text, split
  into number, name and offence; C 20 and 21, one row there, two here), and
  `build_pages.py` (TABLE) fills each cell with the corrected words of the
  page, every word placed exactly once. In a cell the line ends are spaces and
  a word broken at a line end is joined without its "¬" ("Geistlichen"; the
  editor: "you don't need to do this"), two words where the next part is
  capitalised ("Krieg Commission", "Vestungs Strafe"); the list's line-end
  decisions lapsed. The braces of the page (A 1 and 2 share one offence; C 20
  and 21 one offence and one month) are given once, in the first row. Columns
  3 to 5 (offence, length, month) are text columns (`table_text_columns` in
  rulings.yml), the short two kept on one line; the column heads repeated on
  0008_a2 are shown once over each page. The English is the same table
  (`intake/translation/doc3_table.py`). Its date is inferred from the
  promemoria, whose enclosure it is ("nach der beyliegenden Liste").

The promemoria counts 3 sentenced to death and 2 for life; the list has 2
under A (death) and 3 under B (life), Nowicki among B with "zum Galgen
verurtheilt; ist aber ... pardonnirt worden". The promemoria counts him with
the death sentences ("wovon aber einer unter dem Galgen Pardon erhalten"). The
figures 307 + 49 + 26 + 2 + 3 = 387 add up; the list's C has 26 entries.

## The transcription checked

The transcription is the editor's. At the editor's word ("examine the
transcripts to see if there are any transcription errors ... use Sonnet
subagents where possible") four Sonnet readers checked it against the page
images, two independently for each part (promemoria and the King's note;
the list), each given the page in overlapping strips at full resolution and a
list of suspect spots without the suspected answer; reader 2 read the King's
lines from the image before opening the transcription, reader 4 the names and
dates of 0008_a2. Claude then looked at every disputed word on an enlarged
crop. 23 corrections, each with its witness, in `intake/build_pages.py`
(CORRECTIONS): among them "zufürtzerer" → "zu kürtzerer", "größtintheils" →
"größtentheils" (the same word six lines below), "ge¬ / geldet" →
"ge¬ / meldet", "Straf E[w?][r?][m?]¬pel" → "Straf Exem¬pel" (the fixed
formula), "Mnewski" → "Mniewski", "Höym" → "Hoym", "Weiler" → "Weil er"
(three times), "Ausgleicher" → "Aus gleicher" (twice), "des Insurrektion" →
"der", "December" → "Dezember" (entry 14), "4 Jahre" → "4 Jahr" (entry 26).
In the King's hand: "binnen" → "keinen" (the one reading of the sentence:
"finde keinen der Condemnirten einer Minderung der Strafe würdig"),
"erkennen[?]" → "erlegung" (confirmed by the editor),
"am[e?]st" → "arest", and the struck word "straffe" taken out (struck-out text
is not transcribed: EDITORIAL_RULES, 2026-10-05; two words on that line are
struck, the editor had transcribed one of them).

The editor's spot sheet (`intake/spot_sheet.py`; as one self-contained
page, `intake/spot_sheet_html.py` -> `review/ihagrrep7cnr3067/spot_sheet.html`),
eight rows, answered 2026-11-19: "befreyt", "dererjenigen", "Pistrzkowski" and
entry 23's "Mißbrauch" stand as transcribed; **"Betrachtung" stands, the
editor's own reading**, against reader 1's and Claude's "Untersuchung[?]" and
reader 2's "Erwegung" (Claude's correction withdrawn; the English reads "After
close consideration"); "erlegung" confirmed, its [?] removed; "verbrach[en?]"
and "da[?]" the editor could not tell either, and they stay doubtful.

Not transcribed, as in the editor's text: the "# #" marks above "Sollten Sr
Königliche Majestät" (0005_a), above "Es schweben noch einige wenige
Untersuchungen" (0006_a1) and above "auf obige Vorschläge" (0006_a2); a small
brown-ink mark at the foot of 0005_a, read "v. Sh." by one reader; the pencil
folio numbers; the underlining of "nach der beyliegenden Liste" and "nach
eben dieser Liste"; in the list, the filler dots and dashes after the names
and the lengths (only entry 16's "6 Jahre -" is in the transcription), the
full stops after the column heads of 0008_a1, and the braces that join the
reason of A 1 and 2, and the reason and the date "März 1796" of C 20 and 21
(the transcription gives the reason and the date once).

Goldbeck's signature stands on the page at the right edge, in a thin
red-brown ink, underlined, level with the King's sixth and seventh lines,
which run round it; the transcription puts it after his date, where it
belongs to document 1.

Line ends: the resolver's "split" of lebens wie¬rige, Posen¬schen, be¬freyt,
exten¬diren, exa¬miniren and Con¬foederation set to `join` by hand;
"Krieg¬ / Commission" left split. Paragraph breaks set by hand (`hand` rows):
the docket, "Promemoria", "Bey allen diesen", "Die Haupträdelsführer", "Daher
ist es", "= 387.", "Sollten Sr.", the dateline; the King's date joined.

## Translation and summaries

Translated in session (2026-11-19), no paid run: `intake/translation/doc1-3.yml`,
written to the cache by `write_cache.py`; check_translations.py raised
nothing. The English uses Poznań, Włocławek, Wieluń, Łęczyca, Kalisz;
"Ostrzewo" kept as written (Ostrzeszów, which lay in the Wieluń land, is a
thought only). Summaries written in session (`intake/write_summaries.py`),
claim-checked by a Sonnet sub-agent (`intake/claim_check.yml`: 58 statements,
6 overstated, 4 cut or weakened and 2 kept with the reason given there).

## Index

- Goldbeck: `only_in` extended to document 1. Friedrich Wilhelm II: his
  signature "Fr. Wilhelm" added to his `issuer_match`, this document to
  `issued_in` (which only says where that pattern may match). Hoym matched.
- Wybicki and Niemojewski (document 1) are matched to the existing entries,
  whose confiscated estates were returned in 1807: Claude's identification,
  noted in both entries and in NEEDS_CONFIRMATION.
- Shut out: the minister Sobolewski of 1820 (not Joseph Sobolewski, documents
  1 and 3), Grand Duke Constantin (not Constantin v. Mielewski), the creditor
  Magnuski of 1805 (not shown to be Vincent von Magnuski; `seed_not_in`).
- Places: Włocławek now matches "Wraclawec" (the pattern hit only this list
  and the existing "Wraclawek" of Oe 1 Bü 14525-28); Łęczyca matches
  "Lenczyc..."; Rypin added as a place. B 2's "Wrac¬lawek", broken at a line
  end, is "Wraclawek" in the table and matched since 2026-11-19.
- "Prudzinski" (document 1, among the fled ringleaders; the page plainly
  has the d) is Antoni Prusimski: the editor's identification, 2026-11-19.
  Matched to `prusimski` by its own alternative in the `match` (not a
  `variants` entry, which would make check_translations demand the full
  "Antoni Prusimski" in a list of surnames); the English writes "Prusimski"
  (reference/english_forms.yml, name-prusimski), the transcription keeps
  "Prudzinski".
- No person entries for the 31 names of the list or the other ringleaders
  (the editor, 2026-11-19).

## Connections and the timeline

Three cross-holding connections (reference/connections.yml, 2026-11-19, at
the editor's word), the candidates (37 documents sharing a name or a term)
read whole by a Sonnet reader and the quotes checked by Claude:
`goldbeck-confiscated-estates-disposed` (with Nr. 3570, 1: the disposal of
August 1796, whose deeds of gift Goldbeck laid before the King with Hoym),
`prusimski-venice-goldbeck` (with Nr. 1414, 1: the Venice report sent to
Goldbeck five weeks before), `fled-ringleaders-restitution-1807` (with AGAD
1/174/0/1/6, 2 and III. HA MdA, III. Nr. 12366, 2: Wybicki, Niemoiewski and
Prusimski's daughter regain their estates; rests on Claude's identification
of Wybicki and Niemoiewski). Read and not connected (a shared name only):
the Kalisz president Goldbeck of the Prince's letters, the other Dombrowskis,
the later papers of 1809-1815 on the estates. Possible further members,
not written: the gift of 19 June 1797 (Oe 1 Bü 14525, 10 and its copies),
which adds the church estates because the confiscated Prusimski estates were
heavily indebted; the Kalisz judgment of 1827 (12366, 6).

Timeline: "The King refuses the insurgents a further pardon", 16 February
1797, era `insurgency` (beside Prusimski at Venice), its source the
document.

## Era

`hohenlohe`, as Nr. 1414: the insurgency era's own blurb says the Prussian
files of these years stand in the era of the estate's Prussian years. The
editor left it to Claude ("The date is 1797, so you figure out the era",
2026-11-19).

## Damage

None recorded.
