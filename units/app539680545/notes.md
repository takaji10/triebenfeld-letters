# APP 53/968/0/-/545

Albert Breyer's research sheets on the Polonisation of surnames in the gmina
Zagórów ("Polonisierta Namen [gmina Zagórów - nazwiska mieszkańców]"): ten
photographed sheets of his own notes, German and Polish. Added on
2026-10-25 at the editor's request. **The transcription is a draft, waiting
on the editor's answers to the sheet "Readings in Breyer's sheets 1".**

## The images

Image00024 to Image00034 in the editor's folder of that name on J:.
Image00024 is the photograph of the folder itself and is left out (the
editor, 2026-10-25). Image00025 to Image00034 are ten photographed sheets,
each one page, no fold: `intake/build_pages.py` copies them into
`processed/` as `Image00025_a.jpg` ... `Image00034_a.jpg`.

What each sheet carries (from the machine reading of 2026-10-25):

- **0025** — a short list headed "P. Winkler Polonisiert Namen": pairs of a
  German surname and its Polonised form, with years (7. 1855; 1843).
- **0026** — a list headed "Poloniatura"(?), numbered 1-19: German surname -
  Polonised form (Mittmann - Nowak ... Brodel - Brudel).
- **0027** — an alphabetical list A-Z of Polonised surnames (Arminski ...
  Wilmański), the letters C, E, T, U, V and Z apparently empty.
- **0028** — Breyer's excerpt in his own hand of a Breslau print of 1741:
  "deutsche Briefe von George Schlag, Morgenprediger zu St. Hieronymi u.
  der polnischen Schule verordneter Moderator. Breslau, den 18. September
  1741", with nine pairs of a Polish name and its German form (Wojciech
  Wilkotek - Albrecht ...). The editor ruled that every page of this holding
  is Breyer's own notes, so this is his copy, not a photographed print.
- **0029-0030** — one continuous numbered list of Polonised surnames,
  1 to 53, running across three columns of 0029 and onto 0030; the top of
  0029 has a heading read as "Polonisazja techniczna"(?) and a block of
  pairs of a German name and its Polonised translation (Gross - Grosz(?),
  Erdmann - Zieminski(?), Hoppe - Chmielewski).
- **0031-0034** — dense handwritten German prose, Breyer's discussion of the
  Polonisation of names. **Not yet transcribed**: see below.

## How the reading was made

The session that made this draft could not see the images: the scans were
read only through the lunaroute document converter (the reader of Kraus 2001
and Werner 1904), whole page first, then in overlapping bands cut with PIL
at 2 to 3 times the size, then single lines and blocks where the bands
disagreed. Tesseract 5.5.3 was tried first and produced nothing on these
pages: the hand is handwriting, not print. The list sheets (0025-0030) came
out well enough to draft; the prose sheets (0031-0034) defeated it — the
band readings there contradict one another and invent German where the hand
defeats them, so nothing of those pages is in the transcription.

Every doubtful reading is marked `[?]` in the draft and asked on the sheet:
`python units/app539680545/intake/spot_sheet1.py` (port 4103), answers to
`review/app539680545/readings1_answers.json`, 31 rows, one per strip that
carries a doubtful reading. The strip pictures are the band crops of the
reading pass, copied into `review/app539680545/spot_img/`. A script-order
bug in the generated page (the shared `ANSWERS` object declared after the
per-row handler setup, so the first row threw and no button was wired)
silently killed every button on 2026-10-25; fixed the same day by moving the
declaration to the top of the script. Any later edit to the script keeps the
`var ANSWERS` line above the `querySelectorAll` loop. The strip pictures
were first cut at the band boundaries of the reading pass and sliced through
lines (the editor, 2026-10-25: "Some of the crops are too tight"); they are
now cut from the raw images by `build_strips()` with explicit generous
rects, and every row links the whole sheet besides.

## The editor's answers (2026-10-25, 30 of 32 rows)

Applied to the transcriptions the same day. How the answers were read:

- A row answered "Something else" carries the page's reading in its text;
  a row answered only in the note box carries the corrections there
  (a note in a row without a choice is an answer too, WORKING_NOTES).
  Names the editor gave replace the draft's; names of a corrected line the
  editor did not retype keep the draft's reading.
- A row answered "As drafted" settles the whole strip, so its `[?]` marks
  drop (p26b5, p27b4, p28b3). Where the editor typed a `[?]` themselves it
  stays (Jursowski[?], Tarnamm[?]). A doubtful name a note-only row does
  not mention keeps its `[?]` (Nowaczyński, Micklewski, Sekerowski).
- Replaced lines take the editor's punctuation; uncorrected lines keep the
  draft's.

What changed, by sheet:

- **0025**: heading "P. Winkler Polonisierte Namen."; "Bobel" (not Bobbe);
  the line under the first pair is "Gem. Zagórów" (not Lagiewniki);
  "Grüning - Zielinski"; "Schwirschke - Smierczyski"; "Schmeckel -
  Szmigielski"; "Betke - Bedtka"; "Stange - Sztanga"; "Gutschke - Gucz";
  "1843. Szuberski". The draft's phantom last line ("1873. Universal." /
  "1893. Gruberstr.") is dropped: the editor read the page tail as two
  lines only (Waldowski / 1843. Szuberski), and row p25b7 went unanswered.
- **0026**: heading "Polonisirte / Deutsche Namen." over two lines; 1
  "Niemann - Nowak" (not Mittmann); 4 "Nachtigall - Słowiński" (the whole
  pair replaced); 5 "Fuhrmański"; 10 German "Pidd"; 11 "Schienke -
  Stodulski"; 16 "Hahn - Koguciński" (not Nahr or Mahn).
- **0027**: B "Bartmański" (with ń); F all three doubtful names settled
  (Festerkiewicz, Frydrychowski, Feterowski); H "Hedszelewski";
  K "Kurzmanowski"; S "Schmidecki, Szmidowicz, Szulborski" (not
  Sendowrz/Sulborski). J keeps "Jursowski[?]" (the editor's own bracket).
- **0028**: heading "Polnisch-deutsche" (hyphenated); "Bärwolff" (double
  f); "Thomas Kraut" (not Erzont); "Tomas Złotomeski"; the German of the
  fifth pair is "Tarnamm[?]" (not Tannon). The rest confirmed as drafted,
  brackets dropped.
- **0029**: heading "Polonisirte Deutsche Namen" (not "Polonisazja
  techniczna"). The pairs block, in the page's order down the third
  column: Zech - Czech; Rolle - Rola; Sack - Zak; Rietschel - Rycsel;
  Pahl - Pal; Grosz - Grosz; Rosin - Rosyn; Hahnisch - Hanuś; Brich -
  Bych; Borde - Borda; Maron - Maronowski; Gänsler - Gąsiorowski; Blum -
  Kwiatkowska; Erdmann - Ziemiecki; Hoppe - Chmielewski; Semrau -
  Semroch; Born - Borna. In the numbered list: 1 "Barmański" (the
  alphabet's B line has "Bartmański" - both as read); 2 "Schmidecki";
  4 "Szulborski"; 5 confirmed a pair "Riewe - Riwa"; 8 "Kassewicz";
  20 "Mystelkowski"; 21 "Mystkowski" (not Mlyptkowski); 26
  "Kurzmanowski"; 27 "Hendelewski"; 28 "Folkierski" (the draft's 28
  "Hirzowski" was a misassignment - 29 is Hirszowski); 31
  "Henschelewski"; 35 "Feterowski" (not Retelewski); 41 "Hornowski";
  46 "Kuncewicz"; 48 "Fęglerski" (as the editor typed it, with ę);
  51 "Karlowski"; 52 "Madaliński - Mude" (a pair); 53 "Melerowicz".
  The machine's "Ruck/Rieck = Rozy" pair is dropped as a misread; the
  "Borckl - Boryl / Brill - Boryl" question of the sheet is taken to
  have been the same line the editor read as "Borde - Borda".
- **0030**: 51 "Karlowski"; 52 "Madaliński - Mude"; 53 "Melerowicz";
  under the list "Bohrer - Swiderski" (a translation pair: Bohrer,
  świder, a drill).

## Still open from the sheet

- **Row p25b7** went unanswered: the editor read the tail of 0025 as two
  lines (Waldowski / 1843. Szuberski), so the draft's extra last line is
  taken to have been the machine's misread of "1843. Szuberski". Say so if
  there is a further line.

## The difficult column of 0030 (the editor's readings, 2026-10-25)

The sheet's row p30c2 asked what stands at the foot of 0030's third
column. The editor read it twice in the reply; the second reading stands
and is in the transcription:

    Themen:
    Geschichtskrankheiten
    Polacy-ewangelicy.
    Erste deutsche Einwand
    (Verschlungen
    hat ihr
    der pronihige[?] Münd")

The first reading ("Geschichts Pr_the[s?]hen", "Erste deutsch Eimwand[?]",
"(Wer[t?]s..gen ... der gr...igen Münd")") is kept here as the record of
what was read before. "Themen:" answers the earlier question about the
Kurrent lines below "Bohrer - Swiderski": the block is a list of topics
under that head, not separate Kurrent lines. The machine's readings of the
region ("sirdorfki", "motzungen") are dropped as confabulation.

**The one uncertain word, "pronihige[?]"** — Claude's reading from the
context (2026-10-25, put to the editor): the sentence almost certainly
reads "(Verschlungen hat ihr der **polnische** Mund" — "the Polish mouth
has swallowed (it)": the German name gone under in Polish speech, which is
the subject of the whole holding and of the essay of document 7 ("nothing
is left such people but their German name"). "Hat ihr" then reads as the
dative ("swallowed her [name] from her") or may itself be "ihn". How the
shapes could produce "pronihige": the "ol" of polnische read as "ro" (the
round-bellied minims of pencil Kurrent), and the Kurrent "sch" ligature —
a run of tall strokes — read as "hi" with the "h" of the true "ch"
carried to "g". The check that settles it is in Breyer's own hand: he
writes "polnischen" on 0028 (der polnischen Schule) and "Polonisirte" on
0026 and 0029, so the shapes of his "ol" and his "sch" can be compared
directly on the same pages. A 4x picture of the phrase is at
`review/app539680545/spot_img/p30_word4x.jpg` (served at
/spot_img/p30_word4x.jpg), beside the earlier 3x one. The alternatives
from the metaphor of swallowing — "gefräßige", "hungrige", "gierige" —
fit the "-ige" tail better but lose on the first letters and on the
theme; "provinzielle" was considered and dropped. If the shapes refuse
"polnische", the word keeps its bracket.

## Still open, after the answers

- **"pronihige[?]"**, above: "polnische" is the proposed reading, to be
  confirmed against Breyer's own hand.
- **The prose sheets 0031-0034**: 0031-0033 are transcribed (the editor's
  own transcription, 2026-10-25); 0034 stays without a transcription (the
  editor's word).

## The corpus and the documents (2026-10-25)

Seven documents on the ten pages, `review/app539680545/document_boundaries.csv`:

1. 0025, the "P. Winkler" list — `register`.
2. 0026, the numbered list of 19 pairs — `register`.
3. 0027, the alphabetical list — `register`.
4. 0028, the 1741 excerpt — `note`.
5. 0029-0030, the numbered list of 53 with its heading, pairs and the
   "Themen:" block — `register`, two pages.
6. 0031, the essay on the German middle schools — `note`.
7. 0032-0033 (with 0034) — the essay on the surnames in the towns — `note`,
   three pages, its last page 0034 shown but not transcribed: its text in
   the corpus is `(skipped)`, the pipeline's marker, so the image is paired
   and shown with the document while the text is not invented.

No document is dated (all in `no_date:`); no place of writing (the
overrides leave every document's place empty, since Breslau, Lodz and
Warschau stand in quoted matter, not datelines). All seven keep the
holding's era `twentieth-century`. The transcriptions of 0031-0033 are the
editor's own, kept as typed; the prose carries Breyer's spellings and
slips, and its unreadable words are listed in `intake/unresolved.md`.

The page ids are four digits (`0025_a`), the grammar the pipeline's scan
matcher parses; the first staging used the archive's five digits
(`00025_a`) and paired nothing until the copy script, the transcriptions
and the boundaries were all moved to four digits.

## Documents (draft, to confirm with the editor)

1. 0025, the "P. Winkler" list.
2. 0026, the numbered list of 19 pairs.
3. 0027, the alphabetical list.
4. 0028, the 1741 excerpt.
5. 0029-0030, the numbered list of 53 with its heading and pairs.
6. (0031-0034, the prose — not built yet.)

The corpus has not been assembled: `transcriptions/` holds the six list
pages only, and the prose pages wait on a reading that can see the pages.

That was the state of 2026-10-25 morning; the same day the editor supplied
transcriptions of 0031-0033, ruled 0034 image-only, and the holding was
assembled (seven documents, above), translated in session, its summaries
written and claim-checked in both languages (`intake/write_summaries.py`,
`intake/claim_check.yml`: 33 statements, two corrected in the draft), the
holding's page written in both languages (`about.md`, `process.md`, and the
German), the glossary gate run (0 candidates), and the edition guide's
counts corrected (626 documents, 2,021 pages). Status `translated`, on the
branch, not published. TODO, docs/TODO.md section 35.
