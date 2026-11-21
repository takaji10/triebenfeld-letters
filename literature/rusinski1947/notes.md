# Rusiński (1947): how it came in

## The source

Władysław Rusiński, *Osady tzw. „olędrów" w dawnym województwie poznańskim*,
Prace Komisji Atlasu Historycznego Polski, zeszyt V. Poznań 1939 – Kraków
1947, Nakładem Polskiej Akademii Umiejętności; printed by Drukarnia
Uniwersytetu Jagiellońskiego w Krakowie (imprint scan tom5_0007: "pod
zarządem Karola Kiecia", M - 14707); "wydano z zasiłku Wydziału Nauki
Ministerstwa Oświaty"; "z mapą". Rusiński (1906-2007), the economic
historian of Greater Poland; the book was ready in 1939 and printed only
after the war. The editor's scans: `C:/Users/Tersnaus/Downloads/tom5/`,
170 TIFFs (tom5_0006-tom5_0175), 3999x5936 or rotated.

The book is the foundation study of the Olęder settlement of the whole
former voivodeship of Poznań; the edition's own literature cites it
(Chodyła 2015 passim; Szwiec 2009 bibliography no. 28; Słowiński and
Połom 2024, notes 34 and 41). Its bearing on the edition: Łazińsk (the
Trąbczyńskie Stare Olędry), the Łukomskie Olędry, and the whole
Zagórów-Trąbczyn ring appear in its tables and its founding-lists.

## The editor's rulings (2026-11-05, in chat)

- The whole book is brought in, **except the four plates** at the end
  (tom5_0172-0175: the settlement plans and the map, the contents' last
  two items "Plany osad" and "Mapa") - recorded, not transcribed.
- **"It's fine to display the entire contents on the site (in relation to
  rights)."** Recorded here and in work.yml (`visible: true`), the editor's
  word: Rusiński died in 2007, so the print is formally in copyright in
  Poland; the ruling stands like the Kraus 2001 exception (CLAUDE.md,
  "the third full-text exception").
- Footnote labels in original.md are **page-prefixed** (`[^13-2]`): the
  print restarts its footnote numbering on every printed page, and markdown
  footnote labels must be unique across the work. The label's first number
  is the printed page, the second the note's own number on that page.
- **First the OCR to an acceptable state, then the translation** ("we'll
  have to focus first on getting the OCR to an acceptable state before
  translating it"). English comes on the editor's word, after this state.

## How it was read

- Tesseract 5.5.3 (`C:\Program Files\Tesseract-OCR\tesseract.exe`), models
  `pol` (tessdata_best) and `pol-std` (the standard model) from
  `%LOCALAPPDATA%\Tesseract\tessdata`, through `pipeline/ocr.py`, psm 3,
  at the scans' own resolution (about 400 dpi). The book's type is Polish
  antiqua; no Fraktur pass needed (the German titles of the bibliography
  and the sigla list read well enough in both Polish models to be
  corrected by sense).
- **Two passes as witnesses**: every page read with `pol` (the primary)
  and `pol-std` (the witness), plus the word-level TSV of the `pol` pass
  (boxes and confidences). Raw OCR stays out of the repository
  (`Temp/opencode/tom5_ocr/`); the scripts that made it are in
  `scratch/rusinski1947/` (committed).
- **Every body line re-read at 2.5x** (`full_lines.py`): each body line
  cropped from the scan, upscaled, read with both models at psm 7 - a
  line-level third and fourth witness, and the way the superscript
  footnote markers (which the page passes lose almost entirely - they
  glue to the previous word or vanish) are recovered. Lines whose every
  word read at conf >= 80 (or the conf-0 quirk) and that carry no
  digit-tailed token are skipped: the re-read's yield there would be nil.
- **The doubtful-word candidates** (`quality.py`): the words inside
  difflib-changed blocks between the two page passes (the Dorow 1843
  alignment method; v2's excess-counting was wrong and is recorded below),
  plus the best pass's words of conf 1..75. About 3,000 candidates for the
  book; the band and line re-reads settle most of them.
- **The annex tables** (Aneks I, scans 0139-0159): the sheets are
  landscape TIFFs whose orientations vary **per sheet** - probed in four
  orientations each (`orient_map.py`, `orient_probe.py`); the ones proved
  sideways get a rotate(-90) read. Rows are anchored on the row-number
  column (L.b.); the row-major text's `|` cell marks split each row into
  cells; the even sheets' direct full-page reads are column-major and
  serve as the per-column cross-check of the numbers. The weak sheets'
  rows come from strip-band reads (`strip_rows.py`, psm 6 per band).

## Findings and traps

- **Tesseract conf 0.0 is not a badness signal.** The psm 3 pass emits
  0.000000 for words it reads perfectly (one word in several lines;
  'demograficzne' on scan 0008 read 0.0 and was right). Confidence 0 must
  be treated as "unknown"; the doubtful set is conf 1..75 plus the
  pass-vs-pass disagreements.
- **The running heads' digits are unreliable** (7 reads as 1 on the 70s,
  5 as 0, 3 as 0): the printed-page labels come from the offset
  (scan - 15 for the arabic body, scan - 5 for the roman front matter),
  verified at the chapter anchors: ROZDZIAŁ I scan 0027 = p. 12, II 0037
  = p. 22, III 0052 = p. 37, IV 0070 = p. 55, V 0126 = p. 111, Uwagi
  końcowe 0136 = p. 121, ANEKS II 0160 = p. 145, ANEKS III 0166 = p. 151 -
  all scan - 15; front matter: title = I (0006), contents III-IV
  (0008-0009), Wykaz skrótów V-X (0010-0015).
- **The annex sheets' orientations vary per sheet** (not by scan parity):
  the four-orientation probe (`orient_map.py`) scores every sheet's stored
  orientation highest - 0140 included, whose rotate(-90) PNG is a true
  rotation of the stored TIFF (pixel-identical, checked) and whose direct
  strip read is also fine. **No annex sheet's full-page psm 3 read is
  trustworthy for row order** (Tesseract segments the ruled grid by its
  columns); the reading order comes from psm 4 (rows, variable sizes) and
  the strip reads, not from psm 3.
- **The even sheets' direct full-page reads are column-major** (Tesseract
  blocks the table by its columns): kept as the numbers' cross-check, not
  as the primary.
- **The in-text footnote markers are lost by the page passes**: they glue
  to the previous word ('zupełnie*?', 'intere1') or vanish. **The 2.5x
  line re-reads recover them** (proved on scan 0042: the page pass read
  'Charłub 4, OIL. Chromiec' with two markers lost; the line pass read
  'Charłub 4 (O Chromiec 5' - both present). They are reconstructed
  order-based (the page's nth marker = the page's nth note), with the line
  pass as the marker's own witness.
- **Aneks II and III are printed sources** (the privilege of the Kicin
  key, 1781; the wilkierz of the Kotusz Olęders, old Polish, "pisownia
  poprawiona" - Rusiński's note that the spelling is corrected, scan 0166
  reads 'bobrawiona' for 'poprawiona'). They read at 93-95 mean
  confidence: the easiest text in the book.
- The lunaroute document converter was tried as a third engine (the
  Werner/Kraus precedent) and is unreachable this session (the tool takes
  a URL or base64; the local fetch failed as in the Dorow sitting). The
  witnesses are the two Polish models and the line re-reads.

## What is still to do (this work)

1. The word-level settlement: settle.py v2 ran (2,295 candidates:
   2,214 resolved with the near-spelling guard, 813 to the spot list) -
   the spot words still have to be gone through with crops.
2. The footnote anchors: 498 of 593 markers placed (proximity-matched
   to the rebuilt lines); 95 definitions lack their in-text label and
   go to the spot sheet with their line crops.
3. The footnote inventory is CLOSED (2026-11-05, third pass - see "The
   note parse, v4-v6" below): 593 notes, 589 strip+page verified, the
   two v2-era SPOT cases (0096-5, 0099-5) resolved by the new
   witnesses. The annex tables' trailing notes (about 15, text captured
   in the strip reads) go to the spot sheet - the warped sheets' row
   anchors and note digits are geometrically entangled.
4. The annex rows: 147 tier A (geometric cells), 47 tier B (chunk
   parse), 107 tier C (raw text only) of 287 - the C rows are read and
   in the draft, but not yet column-split; the tables' totals check
   against the book's own sums is open.
5. The front matter composed into front_matter.md (title page,
   contents); the Wykaz skrótów still to compose (sources read).
6. The spot sheet last, with the crops: the marker anchors, the
   annex-table notes, the tier-C annex rows, the words the witnesses
   cannot settle.

## The note parse, v4-v6 (2026-11-05, the third inventory pass)

The v2 inventory (549 notes) was chain-consistent but INCOMPLETE in
both directions, which the editor's "try them yourself first" pushed
into the open:

- **It under-counted**: v2's block started at the foot's largest gap
  and stopped at the last digit it could read - 0103 has 17 notes in
  the print (the printed numbers 8..17 sit in the note texts) and v2
  had found 5; 0020 has 13 and v2 had found 4. Whole trailing runs of
  notes were outside the parsed block.
- **It swallowed body**: 0075's '2. Skład społeczny' section heading
  (digit-led, big gap above, body-size type) parsed as a note, with
  the paragraph after it; 0077/0079's table rows likewise.

The fix that held (**structure2.py v6**): the page's own lines are
1:1 with the print's lines (TSV reading-order grouping - the earlier
top-sort orphaned first words on warped pages: 0018's 'we
wcześniejszym' lost its 'we'); the wide strip (the whole foot at 3x,
**psm 4** - psm 6 collapsed dense note blocks into one paragraph) is
read line by line and its lines are ALIGNED to the page's lines. A
strip line matching a page line's prefix begins a note iff its leading
token is a 1-2 digit number (requiring footnote-size type - a numbered
section heading is body-size), a strong artifact glyph ('!%*+$§£|?'
- the print's ornamental small digits misread), or a digit-1 lookalike
('l Przywilej'); a strip line inside a page line is a psm-4 split
artifact. Every alignment pair must earn ratio >= 0.55 and orphaned
real lines are reassigned to unclaimed page lines (debris strip lines
used to consume page lines and leave real note lines homeless,
0116). The strip is used only within its true coverage (y >= y0).
Marker-less notes (the OCR dropped the marker entirely, 0061's note 4)
come from the psm4 paragraph break + previous sentence end + citation
opener. Garbled-strip pages (0036, 0052, 0136 - warped sheets) fall
back to the v1 geometry parse with debris lines dropped.

Result: **593 notes**; 589 verified by strip-vs-page first-word
agreement; the 2 low-ratio residues are false alarms (a junk prefix,
fraction-glyph variance); per-note crops polish 7 garbled texts
(lexicon-validity arbitrated). Downstream: markers matched to the
rebuilt lines by PROXIMITY (the v1-lineation marker tops never
equal-matched: label placement had silently collapsed to 45 labels);
the paragraphs' hyphen join now REPLACES the fragment (the old code
appended the joined word after it - 'zna- znanej' duplication
throughout; the old 415 kB draft carried ~70 kB of such debris).

Traps worth keeping:

- **psm 6 cannot segment dense footnote blocks** - it reflows them
  into one paragraph; psm 4 preserves the print's line and paragraph
  breaks.
- **A page's last body line often ends mid-sentence** (the paragraph
  runs over the leaf) - a body/note boundary check that demands
  sentence-final punctuation flags ~56 innocent pages.
- **An abbreviation period is not a sentence end** ('C.', 'fol.',
  'AW. A. 1—4.' end mid-citation lines); the first attempt wrote the
  abbreviation list as a character class ([fol|s|nr]) which matches one
  character - it never worked until rewritten as alternation.
- **Tesseract TSV word order IS the line membership** - sorting words
  by top before grouping breaks on warped baselines.
- **A witness built from a wrong boundary cannot witness that
  boundary** (the v2-crop notestrips began at v2's first-note top and
  'confirmed' 0075's swallowed heading; the wide strips - whole foot -
  were needed).

## Spanning notes and the small-type lead-ins (the editor's S01 hypothesis)

The print continues a long note set in solid small type from the bottom
of page N across to the TOP of page N+1's note block (before N+1's own
note 1, no marker). The v6 parse left such continuations in the body.

Confirmed and repaired (span_repair.py; each join verified against the
print at 3-8x):

- runover continuations moved into the previous page's last note:
  0048->0047 (p. 32->33, the Daleszyno lustracja note), 0054->0053
  (p. 38->39, the Essenwalde petition + outcome), 0065->0064 (p. 49->50,
  the editor's S01 wilkierz quotation), 0119->0118 (p. 103->104, the
  German petition of the Ujskie Ol.), 0132->0131 (p. 116->117, the
  'metryki protestanckie Lwowka' runover - its receiving line survived
  only as a faint band, y~3130-3200, pixel-density verified).
- missed FIRST notes absorbed into the body (class b): 0064 (print
  note 1 'Przywilej dla Ol. Karpicko...', lines 2415-3298; stored notes
  renumbered, they were the print's 2-4), 0114 (print note 1
  'Prawdopodobnie wyrokiem sądowym...', crafted from the 3x read -
  the strip had lost 'tylko' and 'robocizn'; stored 'pod owa Bede'
  corrected to the print's 'pod słowami Bede'), 0133 (print note 1
  'AW. Krosna, A. 1: Bakałarza...', crafted), 0035 (print note 1
  'Zagadnienie etymologii...'), 0031 (the Wymysłowo sigla block merged
  into note 1 - the print's 'I.' is the marker '1.', pol-std 8x; the
  two 'examples' of 'dwóch przykładach:' ARE notes 1 and 2, and
  'Dalszy przykład:' closes note 1).

Survey (span_survey.py): small-type lines above a page's first stored
note top, contiguous tail. 49 pages flagged initially, 43 remain; every
one adjudicated by the seam test - if the lead flows MID-WORD or
MID-PHRASE from the body line above (wykar-|czowanej, obli-|czenia,
ze-|zwalał, wiado-|mością, mły-|nów, Miło-|stowo...), it is the same
paragraph: body. The line-height difference that flags them (h~65-72
above h~80-86) is bounding-box noise (ascender/descender), not a type
change - a word split across a type change is impossible. Class (c)
pages: 0017 0018 0019 0022 0023 0034 0037 0038 0043 0047 0049 0055
0056 0058 0059 0060 0061 0069 0070 0071 0081 0090 0093 0099 0102 0104
0105 0107 0109 0110 0113 0121 0127 0130 (+ sliver-only 0056 0058 0072
0128). No action.

Side effects of the repair:

- 7 note texts had absorbed the running footer ('Prace Komisji Atlasu
  hist. Polski, z. 5' + stray glyphs); stripped (FOOTER_RE in
  span_repair.py).
- markers3 re-ran with the new note tops: the sigla block's false
  '89' markers (16-1/16-2, citation years) fell into the excluded
  note region and dropped; net labels 543 -> 546 (the want-count trim
  now keeps 3 more of the pre-existing dual-model duplicate
  detections on the renumbered pages - the stacked-label quirk is
  markers3's known class, to be settled in the print-verification
  pass).
- notetexts/ crop files renamed to the new numbering (a stale crop
  must not overwrite a renumbered note on a future polish run);
  0031_1.json retired (.pre-repair.bak).
- note_apply/note_polish NOT re-run (they would clobber the repairs);
  the chain resumed at markers3 -> marked_lines -> compose.

New residue (spot items S23a-f): six 1-3-line degraded zones where the
body breaks mid-word/mid-sentence and every OCR setting fails:
0064 y2240-2430 ('Testamenty...sporzą-'), 0114 y3560-3780 ('do 200'),
0116 y4060-4280 ('podwyż-'), 0123 y3260-3470 ('przywileje'),
0124 y4160-4400 ('rów-'), 0132 y2600-2860 ('względnie'). Editor's call
(supply readings from a clean copy, or the breaks stand).

State: original.md recomposed (422.3 kB), all repairs verified
(verify_span2.py, 25/25 PASS), SPOT_SHEET.html regenerated (26 items;
S01 marked RESOLVED), CSVs refreshed (orphans 123, numctx 206,
shorts 35). SPOT_SHEET.md not re-synced (secondary twin; the HTML is
authoritative).

## The spot-answer round: marker audit + join/label machinery rebuilt

The editor's answers (S02-S23) exposed the systemic marker problem and
confirmed the spanning-note class. Applied:

Editor rulings applied to the text: S03 13.915 kept with [sic]; S05
60[^68-6] morgów; S06 Tabela V rebuilt (the absolute rows 44|20|3|21,
78|17|3|58, 122|37|6|79 - the editor's reading; 20+3+21=44 confirms;
percents 45,5/6,8/47,7 - the 41,7 was a 47,7 transposition; the header
reconstructed); S08 r. 1653; S10a 2½ razy; S10b 88½ zł; S11 od
30[^86-1] do 70[^86-2]; S12 121½ garnca wódki; S13 4,58 litra[^78-2];
S15 5 2/5 / 4 3/5 włóki[^98-4]; S16 5% sumy; S17 10% kwoty; S18 44
lata[^43-3] / 60 lat[^43-4]; S19 the 1782 Bracknitzer Holl. petition
re-read at 3x and rewritten (ö/ü/ä restored, '8 Ellen' restored - the
auto label had eaten the 8 -, the date '22 maja' restored - the auto
label had eaten the 22 -, markers 2/3 anchored at Brandenburger²/Koerth³
per the defs); S02 confirmed the note 14-1 extent (no change needed).

S23a-f RESOLVED - no lacunae: pixel-density profiling of all six
'lost line' zones shows blank + the footnote separator rule; every
sentence continues overleaf (sporzą-|dzane, 200|talarów, podwyż-|szył,
przywileje|wystawione, rów-|nież, rzeczy|przyczynił, względnie|lektora,
inter e-|sującego, bądź nad|brzegami). The compose cross-page join was
REWRITTEN: the old code duplicated page A's whole last paragraph into
page B (frag[:-1]+pb[0]); now only the fragment word (with its parked
labels) moves, and a plain mid-sentence page break (no terminal punct,
lowercase continuation, not a quote) moves the whole paragraph to page
B. Sliver lines (single-letter warp junk) are dropped before assembly
(111 lines; they had poisoned the hyphen joins: 'sporzą-'+'z' ->
'sporząz', 'materia-'+'w pracy' -> 'materiaw').

Marker audit (the editor's 'look critically' instruction). The markers
are inline full-size digits; OCR fuses them forward ('60⁶'->'608',
'70²'->'70?', '³'->'%', '⁴'->'*'/'\$') or the parse skipped the line.
markers3 v4: (a) skipped lines now contribute standalone+artifact
candidates; (b) isolated artifact glyphs (*, \$, ?, £) are marker
candidates; (c) '|' excluded (line art); (d) both models' duplicate
detections deduped by (top, token) - the old count-trim had been
padding pages with dual-model pairs, DISPLACING real markers; (e) a
MANUAL_ADD/MANUAL_DROP layer for the print-verified markers (all
semantically confirmed against the def contents), with audit-authored
token replacements ('608'->'60[^..]', 'cm2'->'cm[^..]', '17732,'->
'1773[^..],'), protected from the count-trim; (f) MANUAL_DROP_RANGES
for table regions (Tabela V's digits are data, not markers). Short
pages 67 -> 31; labels 546 -> 577; the insert_marks glued matcher now
requires the word base to EQUAL the token base (a prefix match ate
'iniciatywy'->'ini'), standalone placements keep their trailing
punctuation, artifact placements must match the glyph token.

Fully audited pages (markers 1..N placed, def-pairing restored):
p. 6? no - the FIVE editor pages: 43 (9), 68 (10), 78 (9), 86 (10),
98 (6 - the note block rebuilt: the print has SIX notes, the strip
merged 3-6 into one stored note; texts from the 3x band read) + 66
(Tabela V region cleaned) + 97 (the petition page). The audit dump
(audit_dump.py) covers all short pages; ~27 pages remain (the
unanchored 113 defs concentrate there) - next round.

Deliverables: LINES_SHEET.html (the editor draws row separators on
Tabela V + the 21 ANEKS I sheets, Collect outputs scan-pixel y-JSON);
SPOT_SHEET.html regenerated with ONLY the 4 open items (S04/S07/S09/
S14, crops re-done at 2x so the numbers are legible; S07/S09/S14 carry
my applied readings pending confirmation). The confusing section C
tables are gone, replaced by the audit-status note + residual list.

Chain: structure2/4 -> markers3 (v4) -> marked_lines -> spot_fixes
(idempotent: BODY_FIXES line-addressed, DROP_LINES/DROP_RANGES,
LINE_TEXT rewrites incl. the S19 German + Tabela V, structure4 note
fixes) -> compose (join v2 + the label-space polish 'word [^x]' ->
'word[^x]'). Draft 408.9 kB; 534 body labels all def-paired, 0
dangling, 0 duplicates; 113 defs unanchored (audit residue). The four
unruled number items stay open with fixed crops.

## The annex rebuild from the editor's separator lines (rowlines.json)

The editor drew the row separators on Tabela V + the 21 ANEKS I sheets;
their y-coordinates (scan pixels) drove the row rebuild
(annex_rows2.py, v10). What the sheets actually are:

- The print's rows are NOT spaced apart - a new row is a text line in
  the number/name column. Boundaries: number lines (NUMHINT, left <
  1300) + name-column candidates (the sheet's own number/name
  separator rule x + 35..95, gap above >= 55, uppercase start) +
  editor-line repairs (the lines repair rows whose numbers OCR lost).
- The annex has THREE numbering series (each from 1): a = sheets
  0139-0146 (rows 1-111), b = 0147-0157 (1-156), c = 0158-0159
  ('Osady typu przejściowego', 1-9 + 10-11) plus a 4-row sub-table
  (Janikowo/Jasień/Łoskońskie Nowe/Tuczno, numbered 1-4) - the old
  table's 'row identity faults' (S20-22) were largely artifacts of
  not knowing this.
- Numbering: COUNT within the series; the print's hints validate.
  Repairs in the loop: phantom drops (hint == counted-1 -> the
  preceding start), drift-k drops (hintless/dup-hinted predecessors),
  the systematic-shift fix (a constant hint-count offset over >= 3
  disputes - 0145/0146 -2, the 0159 sub-table -11), the cross-sheet
  tail trim, the in-band rescue, cell-arbitration of misread hints
  (the zoomed number-cell read outranks the line read: 87 Not '81',
  102 Połajewskie Not the 'doubled 103' - the print has NO numbering
  defect there), the note filter (a hard-backward hint whose text is
  prose - 2nd token lowercase - is a footnote, cut from the rows;
  the sheet-bottom notes no longer pose as rows), sliver/junk row
  drops, and OVERRIDES for series c (eyeball-verified starts; the
  sub-table's restart handled by hint-aware numbering for overrides).

RESULT: all 21 sheets' row spans now match the print exactly
(0139: 1-13 ... 0146: 99-111; 0147: 1-13 ... 0157: 146-156; 0158: 1-9;
0159: 10-11 + the sub-table 1-4). compose emits one line per row
(numbered; totals/unnumbered rows after). Known residue: on 4 sheets
(0144, 0152, 0154, 0156) one row boundary could not be recovered (the
lineation has no line there and no editor mark) - the affected band's
text carries two rows' content; the numbering is unaffected. Column
splitting into cells remains open (the vertical rules are
row-inconsistent in OCR).

Also this round: S09 marked [sic] per the editor (the book's own
1889/1890 error); the S04 crop rebuilt as three stacked 3x line
fragments (the previous crops kept missing the '514' line at y 3293);
SPOT_SHEET.html = the single open item.

## S04 resolved - the spot sheet is empty

The editor read the print: 514 and 3.122 are what the page shows; the
discrepancy (514 x 6.05 = 3.110.7) is the book's own arithmetic slip.
The draft already carried both numbers unchanged (faithful
transcription); no [sic] was requested (contrast S09, where the
impossible dates 1889/1890 were marked). If the editor wants a [sic]
there, it is a one-token edit.

SPOT_SHEET.html regenerated with zero items (a 'no open items' banner;
the audit tables stay). All 23+ spot items from the three review
rounds are now applied.


## Marker audit wave 2 complete - methods, traps and the systemic findings

The label/def pairing check (body label Counter vs def Counter, both
directions) is the real completeness gate; 'short: 0' on all 115 body
pages is necessary but not sufficient. Final state: 651 body labels
<-> 651 defs, zero orphans both ways; verify_round/round2/span2 ALL
PASS.

New machinery this wave:
- audit_page.py - per-page report (body lines + markers + note
  one-liners); the working view for every page audit.
- raise_sweep.py - ascender-zone ink with empty x-height beneath, per
  structure line: finds raised markers the models missed (used on 0031,
  0061, 0084, 0120/0121).
- diag_unplaced.py - lists unplaced defs with the structure line text
  at their tops.
- digit_audit.py (annex) - the print's own number column (ink bands
  between the first two rules) as ground truth for row bounds: a data
  span must hold exactly one band; orphan bands = missed rows, 2-band
  spans = missed boundaries. Found and fixed: 0139 (header pseudo-row +
  missed row 1), 0142 (swallowed row 61), 0143 (repeated header), 0147
  (header + missed row 2), 0159 (rows 10/11 boundary + the totals row
  and the sub-table title as furniture).

Traps hit this wave (all now guarded):
- The insert_marks 'out' template must carry the caret: '[{label}]'
  NOT '[{label}' - 15+ entries were authored caret-less and placed
  caret-less labels (54 defs unplaced until the bulk fix). A caret-fix
  pass runs after every edit batch.
- MANUAL_ADD now SKIPS (not stacks) auto candidates it covers (same
  norm(tok), +-80px) - the re-dedup key inside prot is the EXACT
  (top, raw tok) pair so distinct digit-shape pairs like '!1'/'1?'
  (the raised 11/12 on p. 94) never merge.
- MANUAL_DROP with an artifact tok kills every artifact candidate
  +-80px on the page (norm('') matching) - used to clear whole junk
  clusters, re-adding needed markers as manual entries.
- A manual marker's top may need a nudge to order two same-line
  markers (0108: the \$ before zlodziejami must sort before the ?)
  pozare; insertion order breaks top-ties in the cands sort).
- The strip's note-block misfirings catalogue grew: notes merged into
  the next (0073's quote tail, 0109's 9+10, 0134's German quote), one
  note shredded into two blocks (0084 x2, 0085), body headings/list
  items filed as notes (0080 'I. Rolnictwo', 0044 'Wszystkie
  wspomniane'), real notes missed entirely (0085 notes 8/10, 0109 note
  1 'J. w.' - the strip read the note line as body text '17. w.'), and
  a note glued onto the previous note's tail (0108 note 7 'AW. Stare
  Loskonkskie' inside note 6).

Systemic strip artifact (editor question pending): the print's
lowercase 'l' was read as capital 'I' throughout - 'Kl.' (Klassifi-
kationsanschlaege) as 'KI.', 'Ol.' (Olendry) as 'OI.' - hundreds of
tokens. One note fix (0113 #2) already restored 'Kl. XII 7 fol.' per
the print. Normalizing the whole draft (KI.->Kl., OI.->Ol.) is a
one-pass mechanical change awaiting the editor's ruling.

Open items noted for the editor (all in the new front matter):
- 'Tp. - Topographisches Verzeichniss...' (p. VII): the siglum glyph
  reads TV/Tp ambiguously at pixel level; transcribed 'Tp.'
- 'T 1769' (p. VI): the last digit 6/9 is marginal; two OCR reads and
  the strip say 1769 (the imprint inside the entry says impressa
  1766).
- 'Tb.' (p. VI): strip read 'TB'; transcribed 'Tb.'.
- Ludkiewicz title (p. VIII): 'na nizinie sartawicko-noteckiej' - the
  strip read 'sartawicko-nowskiej'; the compound is barely legible.
- VO entry (p. VII): 'znanych pod nazwą wizytacyj Okęckiego' - the
  strip lost the inflection ('wizytacyjami'?).
- Gebhardt's 'Das Posener Haulaenderhaus' citation (p. IX): a stray
  'nr' fragment could not be placed ('Provinzialblaetter 26, nr ?,
  Poznan').
- The body note (p. 26 def 2) cites 'Tp. 72' - the Wykaz has no
  Tp. 72; TKS. 72 (the 1772 wypis) is the likely intended siglum.
  Left as printed pending the editor.

Front matter now complete: [p. I] title + imprint, [p. III] SPIS
TRESCI (the print's TOC numbers cross-checked against the body's
actual pagination; the transposed '3. Inne objazlenia/4. Robocizny'
pair restored to the print's order: 3. Robocizny 90, 4. Inne
obciazenia 93 - pixel-read), [pp. V-X] Wykaz skrotow (sources A +
literature B), composed from the strip with per-entry print reads.
The annex column parse (annex_cells.json, residuals <= 0.009, RULES_
SHEET.html for eyeball check) is available; the draft keeps the
editor-reviewed raw-row rendering (the dim dash-cells OCR as junk - a
cell-table rendering would need hundreds of spot answers).


## Editor rulings applied (the post-QA round)

1. The systemic l->I artifact: NORMALIZED. compose.py now runs a
   final pass restoring the print's sigla: KI.->Kl. (62), OIL->Ol.
   (11), OI.->Ol. (376) - word-boundary guarded, single-letter Roman
   numerals untouched.
2. The 'Tp. 72' body citation (p. 26 note 2): marked per the editor's
   convention - 'Tp. 72 [sic; TKS. 72]' (the [sic] plus the correction
   in square brackets; TKS. 72 = the 1772 wypis, Wykaz p. VI).
3. The small Wykaz uncertainties (Tp./TV siglum, T 1769, Tb.,
   sartawicko-noteckiej, wizytacyj inflection, Gebhardt's stray nr):
   no editor action needed - transcribed per the print reads already
   taken; they stay as-is.
4. ANEKS I NOW RENDERS AS REAL MARKDOWN TABLES (the editor's ruling;
   replaces the raw-row compromise). Pipeline: annex_cells.py (rule
   ladders, template fit generalized - every detection pair x every
   template pair, so sheets with a faint outer rule like 0152 pair
   correctly) -> annex_md.py (per-cell PIXEL classification: EMPTY /
   DASH / TEXT - the print's dash is ~70x8px, killing the junk OCR on
   the dim dash cells; text cells hyphen-joined and cleaned) ->
   compose.py renders one Markdown table per sheet (the print repeats
   its header on every sheet; the transcription follows). Known
   residue: the prose cells (Zrodlo/Data columns) carry OCR noise
   (e.g. 'AW. B.99--GU' for 'AW. B. 99-60') - the numeric/name columns
   are clean; spot answers welcome on suspicious prose cells only.


## Editor rulings applied (the Markdown-table round)

1. l->I NORMALIZED in compose.py's final pass (KI.->Kl. x60,
   OIL->Ol. x11, OI.->Ol. x371; word-boundary guarded).
2. 'Tp. 72' body citation -> 'Tp. 72 [sic; TKS. 72]' per the editor's
   [sic]-plus-bracketed-correction convention.
3. Small Wykaz uncertainties: no action needed (transcribed per the
   print reads already taken).
4. ANEKS I = REAL MARKDOWN TABLES. annex_cells.py's fit generalized
   (every detection-pair x template-pair hypothesis; bounded spurious
   -run skips), 0152's faint outer rule now pairs correctly
   (resid 0.0088 -> 0.0009). annex_md.py pixel-classifies every cell:
   EMPTY (no ink), DASH (the print's ~70x8px dash strokes; 744+6
   classified), TEXT (cleaned OCR: hyphen joins, junk punct runs
   dropped). compose renders one table per sheet (22 headers - the
   print repeats its header per sheet, and 0159 carries the second
   table), furniture interleaved by y (0159: totals line + sub-table
   title + sub-rows), 0158's sołtys footnote block appended from
   structure4, and 0158 row 9's noise cells replaced with the strip's
   print-verified row text.

KNOWN RESIDUE in the table cells: the prose columns (Zrodlo/data)
carry OCR noise on multi-line cells (e.g. 0147 row 2 'AW. B.99--GU'
for 'AW. B. 99-60', '291V 1/40' for '29 IV 1748', 0152 row 90
'rel. Posn. nr 140, r. 1601/2, f 6591' for the wrap). The numeric and
name columns are clean. Suspicious prose cells can be listed for spot
answers on demand; the tier-C raw row text (the previous rendering,
still in annex_table.json) remains the cross-check source.

## The annex tables' footnote apparatus (discovered in the noise sweep)

The print attaches numbered footnotes to the ANEKS I tables - a layer
the first compose pass never captured (0158's block leaked in as
garbled furniture paragraphs; the other sheets' blocks were simply
missing). Structure, established by pixel work (mark_scan2.py,
note_inv2.py, per-glyph ASCII/OCR):

- Refs: superscript digits after the Nazwa cell's text (the draft's
  junk chars '!', '?', the quote marks, '$', 'S', stray digits were
  the misread marks). Blocks print below a sheet's table and are
  numbered from 1 EACH; a ref resolves to the nearest block below its
  own sheet. Duplicate refs are normal (0158: r2/r4 both -> note 3,
  r5/r8 both -> note 5).
- Blocks found: 0144 (n1 Pożegowskie), 0146 (n1 Sroczewskie, n2
  'Razem z Ol. Góry.'), 0152 (n1 'Jest rzeczą wątpliwą...', n2 the
  long Wielkokrobielewskie note), 0156 (n1 'odłączenie się od
  Budziszewskich Olędrów'), 0158 (n1-n7, the sołtys/samorząd block),
  0159 (n1-n6). Sheets 0139-0143, 0145, 0147-0151, 0153-0155, 0157
  have NO blocks (page bottoms verified empty by ink profiling).
- The mark on 0150 r52 (Kolędzin Olędry) and on 0148 r23
  (Dziewczastruga) both resolve to 0152's note 1 - the nearest block
  below is three sheets down (0149-0151 verified empty). Semantics
  fit: both are 'doubtful whether two separate settlements' cases.
- The Budziszewko offshoots (b-r52 Kolędzin? no - r122 Smolary,
  r141 Wiewierczyn, r143 Władyszyn; all par. Budziszewko) share
  0156's note 1. b-r33 Grudzianki's raw 'l' is junk (nazwa tail
  pixel-checked: no mark; the name's second line reads 'Razem z
  Ol.: Kolędzin, Wiewierczyn i Władyszyn.' - the a-series r33 merge
  covers the same group).
- The asterisks in the dymy cells (b-r48 4*, r84 10*, r85 5*, c-r1
  12* etc.) are NOT note refs: the body (p. 23-24) explains them
  (dymy given zbiorowo in Tp. 89, estimated per Tp. 90). They must
  survive in the cells (cell-fix pass item).
- Series totals rows: a-series 'Razem z poprzedn. 2.386 92 12.967'
  (below 0146), b-series 'Razem z poprzedn. 2.071 38 4.484' (below
  0157) - both were missing from the draft entirely; the label zones
  print faint (OCR-blind, ink profiled) - labels taken in parallel
  with the c-series' readable u0 'Razem z poprzedn.'. The c-series
  u0/u2 render as real table rows now (u0 2.178 38 4.514; u2 Ogółem
  2.216 38 4.514 - the leading '4.' of the Ludn figures
  pixel-verified; arithmetic self-certifies: 2.178 + 38 sub = 2.216).

SPOT items for the editor (apparatus):
1. a-series razem row: label reads faint; taken as 'Razem z
   poprzedn.' with the sup 2 ref to n2 'Razem z Ol. Góry.' - please
   confirm the label wording and the ref.
2. 0158's mark digits (r1=2, r2=3, r3=4, r4=3, r5=5, r6=6, r7=7,
   r8=5, r9=1): r4 and r8 duplicates of r2's/r5's notes; r9's '1'
   inferred (the mark glyph sits in a noisy multi-line cell; note 1
   'Razem z olędrem...' fits Trojanowskie alone).
3. 0159 sub-table: s1-s4 mapped to notes 3-6 in row order; r10/r11
   to notes 1-2 ('Trzydomy !'/'Wiorek *?' junk = the misread marks).
4. 0152 note 1's anchor: taken as the sup marks on r23/r52; r84/r85
   (Niewiemko Nowe/Stare) show no nazwa marks - their 10*/5* dymy
   asterisks are the body's zbiorowo convention.
5. 0144 note 1 details to eyeball: 'komornica Naganianka' (odd
   name), 'Sobestyan komornik' (Sebestyan appears twice), 'karczma,
   d. 9.', 'wskazywałyby na to, że być może, uczyniono'.
6. 0159 note 5: 'Zachowały się 2 przywileje indywidualne dla 2
   osadników' (the two 2s per the print reads) and 'jednak Tp. 90
   wykazuje dla tej osady 7 dymów'.

compose.py now: emits the refs into the Nazwa cells ([^page-n]
labels), renders the blocks as footnote defs after each sheet's
table, injects the a/b totals rows, renders u0/u2 as table rows,
and no longer leaks 0158's note lines as furniture paragraphs.
annex_notes.py holds NOTES/REFS/RAZEM.

## Data-layer regeneration + cell-fix round (in progress)

- annex_cells.json/annex_md.json REGENERATED from annex_table.json v10
  (0159 sub-table on the corrected row bands; cells_patch.py re-OCR'd
  0159's six rows in place). annex_md.json now carries the u2 furniture
  (OgolEm) and compose renders u0/u2 as real table rows appended to
  their tables (no extra headers; qa 'table headers 22' back to PASS).
- clean() in annex_md.py now PRESERVES a trailing '*' (the body
  p. 23-24 zbiorowo-dymy marker); stars_reocr.py re-OCR'd the 38
  starred rows (idempotent for unchanged bands; verified via a
  git-draft diff that the re-OCR introduced NO regressions - the diffs
  were mojibake fixes, the old draft had OT-CE-OD dash mojibake).
- 34 star fixes pinned in annex_fixes.py (digit + ' *' per the raws;
  star_find.py's blob scan used as cross-evidence). Stars whose digit
  or column stays uncertain -> SPOT: 0146 r102, 0149 r47 (Kaledek),
  0151 r78 (Meryn Stary 'Qg*'), 0154 r106/r107 (the '39 *' row
  attribution), 0154 r110/r111 (the '13 *' attribution), 0154 r113,
  0157 r154 ('1 *% 44').
- Date-cell fixes verified by pixel/high-zoom reads and added to
  annex_fixes.py: 0139 r7 '11 XI 1720', r9 '6 VII 1702' (NOT 1762),
  r11 '18 IV 1785'; 0140 r18 '10 X 1721', r21, r23 '11 X 1757', r26
  '13 X 1765' (a FALSE-CLEAN cell the triage missed - caught in the
  star-row re-OCR diff); 0141 r39 '20 XI 1729 20 I 1749', r44
  '14 X 1735' (the doubled-1 artifact '11735'->'1735', same as the
  verified '11757'->'1757'; the 8 full-height glyph groups explained);
  0144 r84; 0147 r13 '28 VII 1776'; 0148 r17 '1 IV 1781', r27
  '11 XI 1735 20 X 1744'; 0151 r68, r69 '9 VII 1701', r72
  '3 III 1614 1 V 1677' (Marianowo's 1614 privilege is real); 0152
  r83; 0156 r136 '1 XI 1751'.
- The date roadmap lives in df1.txt (94 strip-candidate cells + 45
  SPOT) and numart.txt (ASCII art of the 48 flagged numeric/name
  cells); the numeric pass (c8 28 / c10 13 / c9 6 / c4 15 / c5 4 /
  c1-c2 2) continues from these.
- qa_final's footnote check relaxed to KEY-SET equality (the annex
  reuses one def for several refs by design; the body's strict 1:1
  pairing stays in verify_round*). qa_final ALL PASS; verify_round,
  verify_round2, verify_span2 ALL PASS.

## Numeric-junk crack round (digit template matching)

Built digit_read.py: harvests digit-glyph blobs from the draft's
trusted pure-digit cells (labeled by value), matches target blobs by
normalized-grid correlation. Sanity checks on 0139 hit 1.00 on known
values (r1=60, r6=34, r7=23). line_read.py clusters a cell's blobs by
line (bands are 2-3 rows tall in places).

Fixes encoded (pixel-verified): 0139 r4=5, r5=5 (bar-iozena raws agree),
r8=51 (the third raised glyph is a mark, NOT a digit - the a-series
column sum REFUTED '511': 1827+198 would overshoot 2386 with 511);
0142 r54 c11 dash; 0143 r62 c11 dash, r65 ludn=120, r67 ludn=104
(SPORT hypotheses confirmed), r68=14, r71=19; 0145 r88 dymy=22 (the
classifier's 4/0.94 was a SCALE artifact - glyph art shows the 2-arc +
flat base, and 0146's note says d. 22), r92=10, r94 ludn=159 (middle
glyph = 5: top bar + bowl, not 9); 0148 r28 dymy=48 ludn=266 (raws),
r31 c10 dash, r33 c11 dash; 0149 r37=2, r45 c11 dash; 0150 r60 dash,
r61=24 (blob1=2 arc-top, blob2=4 crossbar); 0153 r94 dash, r99=14;
0140 r14 rok/char/zrodlo/data = dashes (tall parenthesis-like marks
beside them - SPOT).

STRUCTURAL find: 0140's r29 band had swallowed the sheet's NOTE line
(3 notes on one line below the table: '1 Razem z Mostowskimi Ol.'
'2 Razem z Ol. Szarki.' '3 Razem z Ol. Sosnowiec.'). r29's true band
re-read: nazwa 'Dymaczewskie Stare Ol.', parafia 'iOd', dzis
'St. Dymaczewo', rok 1751, char las, zrodlo 'Rel. Posn. nr 489,
fol. 69' (nr 489 CONFIRMED by the body's [^57-1]), data '13 V 1751';
dymyTp/ludn carry tall brace-like marks (SPOT). The note block itself
goes into annex_notes in the next round (refs unresolved - no
superscripts found on r29's cells).

Arithmetic census (sum_check.py): a col9 needs 559 more from 19 junk
rows; a col11 needs 2321 from 22; b col9 needs 1056 from 64; b col11
needs 4100 from 18 junk (+124 dashes - most b-rows' ludn = dash).
These targets VALIDATE each fix as it lands.

## Audit round: full numeric-column sweep + hidden reads

audit_cells.py: band-crop blob reads of c9/c10/c11 for all 250 rows
(rule x-ranges masked), diffed against the draft. Key structural
findings:

1. SERIES IDENTITY settled from the body arithmetic: a-series
   (0139-0146) = powiat KOSCIA NSKI (dymy 2386 + 92 = 2478 = body
   [^23-2]); b-series (0147-0157) = powiat POZNANSKI (2071 + 38 =
   2109 = body p. 26). The a-ludn total 12.967 = the body's number.
   The b-ludn RAZEM 4.484 is the print's own column sum (Tol.-recorded
   osady only); the body's 12.759 for Poznan = an ESTIMATE
   (2109 x 6.05 = 12.759), NOT the column sum. OPEN QUESTION: the
   b-c11 column as pixel-read holds only ~500 total (most cells are
   TRUE dashes: w~66 h<=7 n~300, verified en masse by dash_scan.py);
   the printed RAZEM says 4.484. Either the print's RAZEM aggregates
   something beyond the column, or many b-ludn values sit where the
   draft/pixels both read dash. SPOTTED for the editor.

2. The print mixes DIGIT SIZES within the a-series tail and the whole
   b-series (h 25-45). Size-mismatched template refs caused the
   2<->4/5<->3/0<->6 ties; resolved per-cell by strip-raw agreement,
   ratio checks (body avg 6.05 os./dym) and the column-sum laws.

3. Raised small glyphs after dymy values (0139 r8 =51+1, 0140 r17
   =11+3, 0146 r102 =29+3, 0151 r67 =28+1): distinct from stars
   (stars matcher-read ~4@0.35; these read >=0.8 as digits).
   Semantics unresolved (mlyn count? karczma? obl estimate?) ->
   SPOT. Transcribed as the plain digit value; the raised mark is
   documented here.

4. Column-sum law: a-col10 (szacunkowo) EXACTLY 92 after fixes.

Fixes this round (40+ cells): 0139 r3 ludn 87 (was 7);
0142 r49 dymy 44 (ratio-decisive), r59 dymy 13; 0143 r72 dymy 9,
r73 data 17 V 1746 + ludn 83; 0145 r90 dymy 45 + ludn 282,
r91 ludn 36, r94 dymy 31 + data 29 X 1738, r95 data 6 VIII 1724,
r96 dymy 16 + ludn 97 (ratio = the body's 6.05!), r97 obl 22 (SUM
LAW) + ludn 356, r98 data 5 VI 1712; 0146 r102 data 21 X 1744 +
ludn 206, r111 ludn 226 (draft 2206 was a glitch; 3 digit-blobs);
0149 r36 dymy 30, r39 dymy 16, r40 dymy 3, r41 dymy 24, r42 dymy 36,
r43 data 10 XII 1643 (the strip split 1643 as 16 43!) + dymy dash,
r46 ludn 14; 0150 r50 dymy 11, r58 obl dash, r59 dymy 17;
0152 r92 obl 6; 0153 r97 dymy 38, r102 dymy 6; 0154 r106 dymy 16,
r108 dymy 35, r113 dymy 28, r114 dymy 16 *, r117 dymy 43;
0157 r148 dymy 20, r149 dymy 16; 0159 r11 obl dash; plus dashes at
0142 r51/r60 obl, 0143 r62, 0144 r81, 0145 r87/r95, 0148 r19,
0150 r57, 0152 r90, 0153 r93/r100/r101, 0154 r106.

Census after: a col9 7 junk, col10 1 (the r29 mark), col11 5;
b col9 37, col10 6, col11 13. Remaining junk = mostly small-type
2/4-5/3-0/6 ties -> next round: max-zoom art + the SPOT sheet.

## Round: full noise-removal pass (figures + text), 2025 session 5

### The mark-sum law (decisive experiment)
mark_test.py summed the a-series dymy column two ways: strict
(single-number cells) = 2173; all-digits (raised marks counted) =
2387 vs the print's RAZEM 2386 (Delta 1). CONCLUSION: the print's
total COUNTS the raised small glyphs. The 3 marked cells are real
content: 0140 r14 `165 3`, 0140 r17 `11 3`, 0146 r102 `29 3`.
(0151 r67 `28 1` fixed earlier under the same law.) The 1-unit
residue is within rounding of the print's own arithmetic.

### Column laws after this round
- a-dymy: 2387 (all-digits) vs 2386 printed - Delta 1, law confirmed.
- a-obl: EXACTLY 92. Decisive fixes: 0140 r17 obl was a column-shift
  phantom of c10's 7 -> dash; 0140 r16 obl -> dash; 0145 r87 `17`
  (7-as-1); 0145 r97 `23` (3-as-2 tie). Pixel-verified @0.96-0.98.
- a-ludn: 12958 vs 12967 (Delta 9). Every cell pixel-verified via
  a_audit.py (Lp-anchor windows); unresolved Delta 9 -> SPOT.
- b-obl: EXACTLY 38.
- b-dymy: 2025 strict + 34 marks = 2059 vs 2071 (Delta 12) -> SPOT
  (b-ludn RAZEM anomaly already spotted; the two likely share cause).
- c: no printed totals; c9 pixel sum 88 (3 marked cells not counted -
  consistent with marks-uncounted in c? -> SPOT alongside).

### Figure-pass tooling (this round)
a_census.py (full a-series pixel census), row_zoom.py (per-row 5.5x
figure-column renders with Lp guides), a_audit.py (definitive
anchor-window diff of every a-series figure cell), amb_scan/amb_grid/
amb_corr (9-vs-5 shape arbitration: the true 5 has a FLAT top bar
(0151 r73 ref); the 9 family has ring + curled tail (0153 r93,
0146 r102 refs); corr-vs-ref settled 0151 r78, 0154 r105/r112,
0156 r134/r137, 0158 r3/r4/r8), mark_test.py (the sum experiment),
ludn_diff/ludn_scan (Delta-9 hunt), delta_hunt (obl/ludn trailing-0
audit), junk_scan now whitelists `\d+ \d` raised marks.

### Figure fixes this round (headline)
0140 r14/r15 brace-pair figures `165 3`/`1152` (x-order verified);
0141 r31 ludn 75 (15 absurd: 7-as-1), r35 277, r41 335, r43 37,
r44 26; 0142 r45 ludn 130 (x-order), r53 ludn 192, r55 ludn 9,
r61 dymy 8 + obl dash; 0143 r64 196, r69 115, r73 13; 0144 r74 rok/
char dashes + ludn 188; 0145 r89 25/154, r92 18/90, r98 44/265;
0146 r100 ludn 74 (strip '13 74'), r104 25/73, r110 ludn 71 (the 7
hid under a tall mark; 71/13 = 5.5); 0148 r28 obl dash (draft 7 =
glue phantom of the '640' signature); 0149 r42 obl dash (draft 4 =
phantom), r34/r35/r43/r47 ludn 25/11/16/17 (top-alignment);
0150 r49 7, r53 21, r55 6, r58 ludn 5, r59 obl dash, r60 ludn 71,
r63 51, r65 7; 0151 r70 obl 5, r78 `9 4` (small 4 mark);
0153 r94 obl 2, r96 77, r98 obl 4, r101 ludn 2; 0154 r105 9,
r107 obl 9, r112 9, r118 2; 0155 r120 9; 0156 r134 9, r136 obl dash,
r137 9, r144 `7 4` (small 4), r145 12 + obl dash; 0157 r146 17,
r146 obl dash, r147 27 (FULL-size 2,7 - r146's 1,7 was its own line),
r150 `9 1`, r151 dash, r153 7, r154 14 (r155's 1,3 = its own line),
r155 13, r156 dashes + 7; 0158 r2 11, r3 9, r4 19, r5 21 + dash,
r6 dashes, r7 10, r8 6 (diagonal sweep + bottom loop, not 9/0).

### Text pass (b/c-series rok/char/zrodlo)
text_scan.py (regex vocab + verified-phrase whitelist) drove 123
suspects -> 15 SPOT. Mechanical family: 'Rel. Posn. nr' garbled as
'Kel./Kepertorium/KXEI./IKei./Recl./IXCI. LUOSN. I/IXCil. KOSIi.'
(the latter two = full formula mangling, decoded via 0157 r148's
strip); 'Kl. XII 6 I/II/V' body-form restored (0150 r60/r65,
0153 r101, 0158 r4/r6); 'AGH. sad X' (0158 r7, cf. 0139 r9 'AGH sad
Jarocin'); 'Kl. M. i Dom. P. 8515' (0158 r8); dto rows (0154 r106);
AM. Sierakow C. 53 forms; 'razem z Wyszynkami' confirmed as the
print's dzisiejsza-column usage (3 rows). Knot cleanups: 0154
r108 Radusz, r109 Trzciel/Ransko, r110 Roznowko, r111 Roznowo/
'razem z Roznowem' - figures pixel-confirmed unchanged (35/15/21/
13*; the strip's '21'/'20 III 13 *' fragments were line-tails).

### Note-layer final-pass fixes (compose.py)
Nickiedy -> Niekiedy (1), Ilolendry -> Holendry (1). 'iest' left
alone: period orthography inside quoted passages.

### SPOT items after this round (true residue)
Figures/sums: a-ludn Delta 9; b-dymy Delta 12 + b-ludn RAZEM ~4.484
vs pixels ~500; raised-mark semantics (dymy marks counted per the
sum law - meaning?); 0139 r8 third glyph; 0140 note superscripts.
Text cells (15, strip-deep-garble): 0147 r5 char; 0148 r18/r24 rok;
0151 r68 zrodlo prefix; 0154 r105 zrodlo prefix, r111 zrodlo,
r115 char+zrodlo; 0157 r146 rok+zrodlo; 0158 r1 char+zrodlo,
r2 zrodlo, r5 char; 0159 r10 rok.

## SPOT ANSWERS round 1 applied (S23-S35, editor rulings)

- S23 ok: a-RAZEM stays 2.386/92/12.967 (a-ludn d9 residue documented).
- S24 other: the b-RAZEM ludn prints **484**, not 4.484 (annex_notes
  RAZEM fixed). New arithmetic: pixel b-ludn 538 vs printed 484
  (Delta -54, column over the total) - open.
- S25/S26 DECISIVE: the small raised digits after dymy values are
  FOOTNOTE REFERENCES, not values. Ruled: 0139 r8 `51[^125-1]`,
  0140 r14 `165[^125-2]` (note 2 = "Razem z Ol. Szarki." - matches
  the brace-pair: the brace spans r14/r15 and 1152 sits two columns
  over under the same brace). The other marks (0140 r17 `11 3`,
  0146 r102 `29 3`, 0151 r67 `28 1`) make no sense to the editor
  either - left inline, pending. NOTE: with refs removed the a-dymy
  value sum = 2338 (+11+29 if r17/r102 are refs = 2378) vs printed
  2386 - the old Delta-1 fit was coincidence of the ref digits.
- S27: the "Razem z..." block IS a footnote section (confirmed);
  refs 1/2 now wired, 125-3 still unwired (qa whitelist).
- S28: `szatyn"` is NOT on 0147 r5's line (glue) -> charakter `—`.
  The orphan fragment noted here; if it belongs to a neighbour row
  the editor will say so.
- S29 ok: 0148 r18/r24 rok -> `—`.
- S30: 0151 r68 zrodlo = `AGH. s. Wronki, maj. Pożarowo, vol. III`
  (the tail `rowo` was Pożarowo, not Lubowo!).
- S31: 0154 r105 zrodlo = `AGH. s. Pniewy, maj. Psarskie, Tax
  Acten, v. II, fol. 88—94`.
- S32: 0154 r110 ruled verbatim: `Rosnowskie Olędry | Komorniki |
  Rosnówko | — | — | — | — | 21 | — | —` (my `Rożnowskie` proposal
  REJECTED; dzisiejsza = Rosnówko; zrodlo = dash). Consequence:
  AW. B. 770 belongs to r111's print line -> r111 zrodlo = `AW. B.
  770` (strip-derived; flagged to the editor for veto). r115 NOT
  ruled - garbles left, re-asked.
- S33: 0157 r146 ruled verbatim: `Wysogotowo | — ... | 17 | — | —`
  (nazwa plain single-s; `al. Czarne Olędry`/`Skórzewko` were glue
  from r147; parafia AND dzisiejsza dashes).
- S34: 0158 r1 ruled verbatim: rok `ok. 1745`, char `—`, zrodlo
  `AW. B. 1a`, data `2 VIII 1747`. r2 nazwa = `Głębockie Olędry`
  (editor spelling; ref [^143-3] via REFS). All 0158 nazwas carry
  refs (verified r1-r9). r2 zrodlo / r5 charakter await the
  editor's offered rows.
- S35 ok: 0159 r10 rok -> `—`.

## SPOT ANSWERS round 4: the body tables + the p. 85 leaf repair

- tabele_body.xlsx corrected by the editor; all five body tables
  (TABELA I-V) rebuilt in the transcription as proper Markdown
  tables (TABLE_SPANS span-replacer in compose.py). Key corrections:
  TABELA I wschowski = dashes; TABELA II restructured (%-columns) +
  table-note refs wired (Karczmarze[^61-1], Mlynarze[^61-2],
  Hutnictwo[^61-3], Szkolni[^61-4]); TABELA III = the editor's FULL
  reconstruction (28 wsi 1773 / 8 wsi sierakowska / Razem blocks,
  the chałupnicy/komornicy/czeladź + Hodowla + Rzemiosło sub-rows)
  with refs wired (chałupnicy[^62-1]; the uboczne 60/13 = [^62-2];
  the sierakowska 5 = [^62-3]); TABELA IV confirmed; TABELA V
  headers per the print (gotowe/czescia zarosle/zarosle).
- The table-note defs RECOVERED from the two-column OCR scramble
  (note_recon.py): [^61-1] (karczmarze estimate - was missing
  entirely!), [^61-2] (mlyny), [^61-3] (hamer), [^61-4]
  (nauczyciele/140 dusz), [^62-1..3]. [^64-1] (Rusinski
  królewszczyzny) wired at 'królewszczyzn pruskich'.
- S50 RESOLVED: 'wyrosił 20 zł' AND the sentence is on print 85 -
  which exposed a REAL defect: the czynsz paragraph physically
  begins on scan 0100 (p. 85, y1617-3210) but our assembly had
  leaked the whole paragraph into the p. 86 block. The print breaks
  it mid-word after 'w zdewaluowanych' (p. 86 opens 'złotówkach
  tynfowych;'). REPAIRED: the leaf-split restored (p. 85 = head
  through 'w zdewaluowanych' + defs; p. 86 = tail). The refs split
  exactly at the leaf ([^85-2..8] head / [^86-1..4] tail) - the
  print's per-page numbering confirmed.
- BONUS find: the print's p. 85 note block has NINE notes; the OCR
  had fused notes 3+4 and mis-numbered 5-8 (the '9' visible in the
  note margin). Defs re-split/renumbered (85-4 = Rel. Posn. 638 =
  Róża; 85-5 = 36-złoty; 85-8 = Dłuskie; 85-9 = the talar-list) and
  refs re-wired (w. XVII[^85-5] - the marker 5 is VISIBLE in the
  scan at y2250; 36 zł z huby[^85-4]; (r. 1688)[^85-8];
  talarów[^85-9]-). The garbled '30—36. za - czynszu' word order
  repaired from the raw (y3000-3240): '8 zł za talar, i wtedy
  wartość czynszu wyrosiła jak poprzednio 30—36 zł (srebrnych),
  względnie 8—12 talarów'.
- Folio map (folio_map.py): the printed folios match our page
  labels on ALL body pages (0016-0137) and all annex bands - NO
  global drift; the p. 85/86 case was a local assembly leak, now
  fixed. (The 7->1 OCR ties at folios 70-78 resolved by context.)
- 'immuhnitetam1' -> 'immunitetami' (p. 97).
- verify_round2's S06 checks updated to the new table format.
- Final footnote state: 692 refs / 686 defs, zero orphans, zero
  unwired; mismatches = the 5 legitimate ditto refs.

## The footnote-marker audit (SPOT round 2 prep)

Three scanners built: sup_scan.py (letter+digit remnants in prose),
fused_scan.py ('. N Capital' = the next print note glued inside a
def), and the dup-tail check (def N's tail == def N+1's head = the
OCR duplicated the next note into this def). Global state after the
fixes: 680 refs / 676 defs; only 125-3 unwired (pending); the 4
count-mismatches = legitimate j.w. ditto refs (137-1, 141-1, 143-3,
143-5). No page has more print notes than transcribed defs
(markers.json vs structure4.json counts equal everywhere).

DECISIVE fixes applied (BODY_FIXES/NOTE_REBUILD/NOTE_FIXES in
compose.py, 56 replacements):
- p. 1: markers 1-6 located at their visible digits (Baranowski 1,
  Inglota?, Schmidta *, Maasa4, Schulza 5, Polski 6); the old
  pattern-guessed wirings (a wiec/Wschowska/dotyczacym/Prace) removed;
  def 1-1 split (print notes 1+2 fused: 'Wsie holenderskie. 2 Problem
  kolonizacji...'), defs renumbered 1..6.
- p. 2: 'akta gruntowe i hipoteczne' (i->1 garbles); [^2-2] -> the
  wschowska tabela 1789; new [^2-3] at 'spisu ludności %' (Korzon);
  def 2-2 split (note 3 = Korzon fused).
- p. 30: all five markers located: Ujskich1 / Nowe Dwory? (the ? =
  superscript 2) / osadników (note 3 = the settler lists, fused) /
  wieleńskiej4 / Niemcom 5; defs rebuilt 1..5; the old miswires
  (otrzymują/flamandzko-holenderskie/przeciwstawiając/gegeben) removed.
- p. 66: def 1 split (Maas / Zmiany krajobrazu = Hładyłowicz), defs
  renumbered 1..4; refs moved to nowozytna1/Hładyłowicza2/gruntów3/
  cudzy4 (the old stacking at Hładyłowicza unstacked).
- p. 70: markers 8/9 at their $/? remnants ('gruntów$' = the Jaracz
  opposite-case note; 'miedze?' = the Göździn/Karpicko note); the old
  miswires (kawałek/grunty osady) removed; defs 7/9 dup-tails trimmed.
- p. 85/86: the whole czynsz marker map decoded: polskie1 (the
  numismatics note), 30-morgowej? (Ujskie source), 60-morgowej%
  (Nowe Dwory + pomiar), Róża's czynsz = 36 RESTORED (forced by
  note 4's '36-zlotowy czynsz mamy w...' phrasing), w. XVII[4] (the
  5 = a 4-as-5 small-type tie), Dłuskich (r. 1688)[5], obniżką
  czynszu$ [6], dobrej monecie? [7], 8-12 talarów* [8]; the triple
  stack at 'zdewaluowanych' unstacked; 'od każdej huby płacono
  1 zł[86-10]' (the * sat inside 'każdej', I = 1); def 86-9 repaired
  (was a full duplicate of note 8 + the fused note 9 'AW. Zielonka...
  2 talary' - the print's own inline '9' label visible); def 86-8's
  'Rel. Gost.' -> 'Rel. Cost.'.
- p. 89: markers: opłat targowych[^89-1] (best-guess position, the
  cła note - SPOT-confirm), aktu*% [2], gruncie% [3] (the Anerkennung
  quote), nieporozumieniu f. [4] (the f = the superscript; note 4 =
  Maas's Entstehung), Wartę5 [5] (note 5 = Rel. Posn. nr 038/638 =
  the Róża privilege!); defs: 89-3+89-4 MERGED (the 'IV, fol. 1137'
  fragment = note 3's wrapped tail), renumbered 1..5; 'Entstchung' ->
  'Entstehung', 'Kytrzeby' -> 'Kutrzeby', Wertę -> Wartę.
- p. 107: markers: olędrzy1 [1], Kniata[2] (kept), katolickiego* [3],
  równocześnie 4 [4], wysokości 5 [5]; the value-wirings (7/42/30)
  removed - 'w dobrach duchownych 7 talarów 42 gr' = values; p. 30's
  Folsztyn 'gegeben[^30-4]' miswire removed.
- Three remnants sitting directly at their wired refs deleted
  (pola*[^82-5], przeciętna*[^100-5], charakteru$[^112-4]).

REMAINING (SPOT round 2): 22 superscript remnants whose NUMBERS need
the print (rem_class.py list - the OCR rendered the tiny digits as
* % $ glyphs); 6 missing amounts (p. 89 pobierał X tynfów / co X lat
Y zł; p. 107 państwowe X gr; p. 86 Ujskie wyrosił X zł; p. 86 note 4
Skrzydlewie X talarów w dukatach; p. 30 Folsztyn gegeben X
Reichstaler); TABELA III (p. 62) = a garbled table WITH an unlinked
note apparatus (notes 1-4 visible: chałupnicy1, '2 Karczmarze i
młynarze.', '3 nauczyciel, 4 lektorów (Vorleser)'); p. 1's odd note
4/5 texts (Patrz wykaz skrótów @Maas4? Tamże @Schulz5?).

## The rotated top-bands (the annex's page-top furniture) - DISCOVERY

The annex table pages are PORTRAIT pages with the table printed
SIDEWAYS (Querdruck); the scans are landscape, so each page's top
band (running head + folio + TABELA title + the column header + the
table's notes) sits ROTATED in the scan's right margin (x5290-5936;
rotate -90 to read). The first OCR never read these bands - the
transcription's annex section had NO running heads, NO table titles,
NO 'ciag dalszy' markers and was missing several NOTES.

Band inventory (all 21 sheets read; folios verified = our labels):
- EVERY page: running head 'Osady tzw. "oledrow" w dawnem
  wojewodztwie poznanskim' + the folio (= label(scan) - all 21
  verified by eye: 124-144, incl. 129 AND 130 on the spread).
- p. 124: TABELA VI + the a-table's title + the column header WITH
  the asterisk: 'L. dymow wg Tp. 89 lub 90*' (the '*' now added to
  our markdown header).
- p. 125: header + NOTES 1-3 (the 'Razem z...' notes - already
  transcribed; verified verbatim against the band).
- pp. 126-128: header only.
- p. 129: header + THE ASTERISK NOTE (the '*' explanation) - text
  marginal in the scan -> SPOT (S43 crop = the band).
- p. 130: '(ciag dalszy)'? + header -> SPOT-confirm.
- p. 131: header + NOTES 1-2 - text marginal -> SPOT (S44 crop).
- p. 132: TABELA VII + the b-table's title + header (S46 crop; exact
  title wording -> SPOT).
- pp. 133-142: header only.
- p. 143: the c-table's title line (S47 crop -> SPOT).
- p. 144: header only.

SHEET 0144 = A TWO-PAGE SPREAD (print pp. 129 + 130 side by side,
rotated): the upper block = p. 129's rows 74-86; the lower block =
p. 130 (its own repeated header, rows 87-98, no interior rules across
the gutter, denser pitch); sheet 0145 = p. 130 RE-PHOTOGRAPHED solo
(better quality - our rows 87-98 came from it, so no data loss and
no duplication; the 0144-lower copy simply went unused). The printed
folios in the bands (129 on the upper half, 130 on the lower half of
0144's band; 130 again on 0145's band) PROVE the mapping - our page
labels are correct as they stand.

## SPOT ANSWERS round 2 applied + the closing state

S36: 18 marker numbers wired at the ruled positions; the 4
"can't find" glyphs deleted (the print shows no marker there).
S37: 16 talarow (note 86-4), 11 tynfow + co 50 lat / 36 zl (p. 89 -
consistent with note 89-3's "nach Verlauf von finfzig Jahren, zwei
Dukaten zu achtzehn polnische Gulden" = 2x18 = 36 zl!), 19 gr
(p. 107), 18 Reichstaler (the Folsztyn quote). The Ujskie "wyrosil
___ zl" = NOT ON the editor's p. 86 -> our body page labels may
drift from the print's folios (S50 re-ask).
S39: the editor confirms note 4 = "Patrz wykaz skrotow." / note 5 =
"Tamze." = our rebuild exactly.
S40/S41: rows verbatim (0154 r115 Sąpolna + dashes; 0158 r2
Głebocko/AW. A. 1-2/dual date "2 XI 1743 i 11 X 1744"; r5
Krzyzewniki/rok dash/char dash/Kl. M.).
S42: 0140 r17 = 11[^125-3] - the footnote graph is now FULLY closed
(699 refs / 677 defs, zero unwired, zero orphans). The r21/r26
stars confirmed as estimate-markers. The r14/r15 brace + 1152
structure confirmed.
NEW DISCOVERY (this round's footnote audit extension): the annex
pages are portrait pages with the table printed sideways; the
page-top furniture (running heads, folios, TABELA VI/VII titles,
the column header's asterisk, the p. 129 asterisk-note) sat ROTATED
in the scan margins and was missing from the transcription. Added:
the two TABELA titles + the c-title (wording SPOT-pending), the
header's '*', and the p. 129 asterisk-note (wording SPOT-pending).
The "missing" p. 129/131 notes (Pożegowskie, Sroczewskie, Razem z
Ol. Gory) turned out to be ALREADY transcribed and wired (defs
129-1, 131-1, 131-2, 137-1, 137-2 from the earlier strip work).
Also: sheet 0144 = a two-page spread (print pp. 129+130); 0145 =
p. 130 re-photographed; folios read from the bands prove our page
labels.
DELIVERABLE: aneks_i.xlsx - ANEKS I laid out for the editor's
formatting pass (282 rows, the print's segment structure marked,
the annex notes on a second sheet).

## SPOT round 5: the footnote-page pass (the no-move ruling + the debris)

ROOT CAUSE of the whole miswiring class: compose's cross-page join
logic (the "plain mid-sentence page break" mover + the hyphen
joiner) moved WHOLE paragraphs across leaves, and in flowing sections
the moves CHAINED - print p. 27's confession text had migrated into
our p. 29 block, p. 85's czynsz paragraph into p. 86. REMOVED: the
per-page blocks from assemble_marked ARE the print's leaf-splits
(the approved p. 85/86 precedent). After the removal:
fn_closure = 0 CROSS (except the legitimate p. 123->annex), 0 DEAD,
0 ORDER; refphys = 197 OK refs, 0 SLOT, 0 MISWIRE (2 false positives
from duplicate-text artifacts), 0 SPAN.

The pp. 24-25 totals-notes rebuilt line-by-line (4-space indents).
p. 24 closes: 16.303-17=16.286, +92+15=16.393, -2.478=13.915.
p. 25 closes: 14.489-16-84=14.389; +42 (Iwno)=14.431; +247 (the
38:2216 proportion)=14.678; -2.216=12.462.

P. 25 DEEPER FIND (pixel-verified): the old [^25-1]/[^25-2] refs were
PHANTOMS - the print reads 'Tp. 89 względnie 90' / 'względne 90' with
'90' as INLINE text (glyph h63 = body height; a true superscript is
h30). The only real marker on p. 25 is the raised '1' after '12.462'
(bbox h38, top-aligned) -> wired as 12.462[^25-1]. The note block is
ONE note: the totals list PLUS its prose continuation ('Dochodzą 42
dymy ... ostatecznie 12.462 dymy.') - no '2' number glyph at the
continuation (ink-checked x540-960). The old def split had broken the
note mid-sentence ('aneksie I / rubryki'). The final figure is 12.462,
not 12.402 - the glyph render shows the wide-top-curl '6' (same shape
as the verified '6' elsewhere), and only 12.462 closes the arithmetic
AND matches the body.

P. 23 fixes (pixel-verified): 'Jaromierskich Nowych 1 Starych' ->
'i Starych' (raw token 'i'@x1690); note 4's total '24.067' ->
'24.667' (both OCR passes + the glyph render; the '6' shape again).

The single-letter debris (all merged by the raw x/y geometry, ten
STRAY_FIXES entries in compose.py):
- p. 38 'z' -> opens the print line 'z całkowitego majątku swego...';
- p. 49 'w' -> opens 'w trąktuje tę sprawę'; 'z' -> 'kto z nich';
  'z' -> 'którykolwiek z naszych Holendrów'; 'w' -> 'że w osądach
  wcześniej-';
- p. 99 'r.' -> 'krótko przed r. 1800'; 'gr w' -> the missing 'gr w'
  after the first fraction - the print reads '3030 zł 20½ gr w
  Nowych Dworach i 2349 zł 28½ gr w Folsztynie' (the blob after
  each figure decomposes into small-1/slash/small-2 = the fraction);
- p. 103 'uns' -> begins the 'uns auf Erbpacht überlassen' line;
- p. 116 'w' -> 'Nawet w aktach regulacyjnych'; 'z' -> 'część z nich'.
furn_scan now reports only the legitimate headings (TABELA I/V,
ANEKS I).

NEW DISCOVERY - the print's note-overflow continuations (two cases,
content complete, placement is the print's own quirk):
- note 38-3: the manifest quote fills p. 38's note block to the page
  bottom ('...Grunta za sumę tylko 2.300 talerów') and CONTINUES on
  print p. 39 as a note-size insert mid-page (y3024-3645: 'sprzedali,
  inwentarz zabrali ... s. Johann Bóhme"'), followed by the 'Na skutek
  pozwu...' narrative (y3726-4104, also note-size). Our [^38-3] holds
  the whole note (quote + narrative) on p. 38.
- note 116-5: the tail ('metryki protestanckie Lwówka ... nie umieli
  się podpisać.') prints on p. 117 mid-page (y2835-3105, note-size,
  before p. 117's own notes). Our [^116-5] holds the whole note.
A def-tail physical sweep (def_phys.py) + a note-size-insert sweep
found NO other cases and NO missing content (all 28 candidate runs
are block quotes, table text or small-word noise, all covered).

Phase-4 sweep: p. 30 note 3's settler list is RUNNING text in the
print (structure4/5 line-pass, no gaps) - no per-line formatting
needed; p. 23's computation notes are running prose too. Only
pp. 24-25 needed the ladder layout.

verify_round/verify_span2's join-expectation checks rewritten to the
leaf-split state (both ALL PASS).

## SPOT ANSWERS round 5 applied (S52-S54, editor rulings)

S52 (p. 23, the Δ9): editor agrees - keep both figures as the print
has them (note total 24.667, body 15.831; the discrepancy is the
author's own slip). No [sic], no correcting note.

S53 (pp. 38-39) and S54 (pp. 116-117): the editor asked whether the
mid-page note-size inserts on the receiving pages might be the
RECEIVING pages' own notes instead of continuations. Verified they
are continuations of the PREVIOUS page's notes - four independent
proofs each:
1. SEAMLESS TEXT across the leaf: p. 38's note block ends '...za
   sume tylko 2.300 talerow' and the p. 39 insert opens 'sprzedali,
   inwentarz zabrali...' (one sentence); p. 116's note 5 ends
   '...najwczesniejsze' and the p. 117 insert opens 'metryki
   protestanckie Lwowka...' (one phrase).
2. The receiving pages ALREADY have their own complete, numbered
   note blocks elsewhere on the page: p. 39's own notes 1-6 sit at
   y4185-5049 (numbers at x590-594: Rafacz, Kutrzeba, 'Ta ostatnia',
   Rel. Cost. 223/164/224 = exactly our [^39-1..6]); p. 117's own
   notes start at y3213 ('1'@x600 AW. Wielkokrobielewskie... = our
   [^117-1]). The inserts are OUTSIDE and BEFORE those blocks.
3. The inserts are UNNUMBERED: the word scans of the insert opening
   lines (0054 y2990-3060, 0132 y2820-2880) show NO ink left of the
   first token (x372/x388) - no note-number digit - and both open
   lowercase mid-sentence.
4. TYPE SIZE: note-size on the receiving page too (the 0054
   narrative's median glyph height 58 vs the body's 75-81).
Also: no other word in any p. 116 note could precede 'metryki
protestanckie'. RULING: keep both notes WHOLE on their referencing
page (the current state - no change needed).

Verification BONUS find (fixed): inside [^38-3], the 'Na skutek
pozwu...' narrative had a scrambled line ('patrywana' stranded after
'twier-'); the raw x-order reconstructs the true print lines:
'...gdzie byla roz- / patrywana w trzech terminach (Decr. Posn. nr
137, fol. 303, 485 i 597-600). Pozwani twier- / dzili, ze cala
kwote uzyskana ze sprzedazy obrócili na splacenie dlugów powoda,
których / zdaniem ich było znacznie wiecej, niz to powód podał. Jak
sprawa ostatecznie została roz- / strzygnieta, nie wiadomo, gdyz
dalsze zbiory dekretów nic dochowały się.' Fixed via STRAY_FIXES
(also 'gdzic' -> 'gdzie', the only occurrence). Battery re-run:
QA ALL PASS, closure 0/0/0, 45/45 spot checks.

SPOT sheet regenerated with zero open items (the review harness
state).
