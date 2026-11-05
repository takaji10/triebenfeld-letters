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

1. The word-level settlement: the draft original.md is composed (415 kB)
   but its word layer still carries the page-passes' artifacts; the band
   re-reads (2,040 bands, read) and the line re-reads (166 pages, read)
   are the witnesses to settle them against, page by page, with the
   difflib alignment (quality.py's candidates).
2. The footnote anchors: 469 of 549 markers placed (line right, the
   anchor word can be a few words off); 80 definitions lack their
   in-text label and 24 pages' marker shortfalls go to the spot sheet
   with their line crops.
3. The footnote inventory is CLOSED (2026-11-05, second pass): the v1
   chain parser had silently dropped whole note blocks (213 notes
   recovered by structure2's geometric parse); the independent
   geometry gate runs at zero suspects. The annex tables' trailing
   notes (about 15, text captured in the strip reads) go to the spot
   sheet - the warped sheets' row anchors and note digits are
   geometrically entangled.
4. The annex rows: 147 tier A (geometric cells), 47 tier B (chunk
   parse), 107 tier C (raw text only) of 287 - the C rows are read and
   in the draft, but not yet column-split; the tables' totals check
   against the book's own sums is open.
5. The front matter composed into front_matter.md (title page,
   contents); the Wykaz skrótów still to compose (sources read).
6. The spot sheet last, with the crops: the marker anchors, the
   annex-table notes, the tier-C annex rows, the words the witnesses
   cannot settle.
