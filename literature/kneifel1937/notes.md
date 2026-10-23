# Kneifel (1937): the Kalischer Diözese parish monographs, the excerpt

Eduard Kneifel, *Die evangelisch-augsburgischen Gemeinden der Kalischer
Diözese*, Verlag Günther Wolff, Plauen im Vogtland 1937 ("Forschungen zur
Geschichte der evangelisch-augsburgischen Kirche in Polen, 1. Band"). Added
2026-10-23 as a sitting of its own, on branch `kneifel1937`; the English
translation is a later sitting. The work is the forerunner of the sibling
*kneifel1964* (the same author revisits several of these parishes there),
and parts of its Kalisch, Grodziec, Konin and Zagórów material bear
directly on the edition's ground (Trąbczyn, Łazińsk, Zagórów, the
Lissewo-Pyzdry filial).

## The source

`J:\Documents\Archive\Genealogy\References\Books\Eduard Kneifel - [1937]
Die evangelisch-augsburgischen Gemeinden der Kalischer Diözese.pdf` — a PDF
of the book, 298 PDF pages (not kept). No editor's transcription exists for
the whole book; the editor's own .md on J: covers only the Kalisch chapter
(PDF 60-72) and supplied the text for those pages, with its correct Polish
diacritics. Everything else was read from the page images: Tesseract 5.5.3
(deu) at 300 dpi against the PDF's own text layer, the two checked against
each other page by page (word multisets), doubtful spots settled at zoom or
on the spot sheet (`review/kneifel1937/query_answers.json`).

## The excerpt

PDF pages 1-2 (library slip and title page), 6-17 (chapter I, the
introduction, printed 7-16, with the two unnumbered portrait plates PDF
10/11 bound in), 60-85 (3. Kalisch and 4. Grodziec, printed 55-79), 171-190
(12. Konin with a) Maślaki, printed 163-182), 256-274 (17. Zagórów with
a) Das Filial Lissewo-Pyzdry, printed 248-266). The printed page number at
the page foot is the anchor of every `[p. N]` mark; the PDF page and the
printed page drift apart inside the excerpt (the two portrait plates after
printed p. 10; the unnumbered Kalisch page bound in between printed 60 and
61), and the drift continues outside it (printed 55 is PDF 60, printed
163 is PDF 171). The mapping that the finals
record: PDF 6-9 → printed 7-10, PDF 10/11 plates, PDF 12-17 → 11-16,
PDF 60-65 → 55-60, PDF 66 unnumbered, PDF 67-85 → 61-79, PDF 171-190 →
163-182, PDF 256-274 → 248-266.

## How it was read

Per page: the PDF text layer (structural witness, umlauts damaged) and a
full-page Tesseract pass were reduced to word multisets and compared
(`scratch/kneifel1937_wordcheck.py`); pages where full-page OCR lost blocks
(the letter-spaced STATISTIK headings, the "Zahlenmäßige Entwicklung"
tables, the Ortschaften lists) were re-run in horizontal bands
(`scratch/kneifel1937_bands.py`, `cache/kneifel1937/bands/`). For Kalisch
PDF 60-72 the editor's .md was the base text, cut at the page openings and
stripped of its wrappers (`~~***`, `**`), soft hyphens and drop-cap
placeholders; the layer located the cuts. Footnote markers are printed as
superscript "N)", restart within each parish entry (and again in the
Maślaki and Lissewo sub-entries), and the notes are defined at the foot of
their own page as `[^p<N>-n]` with the printed number kept in the
definition text — the kneifel1964 convention.

## Print's slips and doubtful readings, kept as printed

- p. 9 (PDF 8): "Anfänge" — the layer's "Anlänge" is wrong.
- p. 58 (PDF 63): "Nach Pastor Modls Tode" stands beside "Pastor Modl
  († 22. April 1860)" — the print's own inconsistency, kept.
- p. 58 (PDF 63): "bey ändern feyerlichen Handlungen" — kept (print's
  ä/ai type slip for "andern").
- p. 62 (PDF 68): after "der im Kriege beschlagnahmten" the superscript
  note number is printed as a bare ")" (digit lost in the print or in the
  scan); transcribed as printed. The mark before "sehr" on the same page
  (a stray stroke read "isehr" by the editor's file, as a raised comma by
  Tesseract) was dropped as printer's ink.
- p. 62 (PDF 68): "die später von ihm Nitsche gekauft hat" — kept (the
  print's syntax; "von ihm" for "von").
- p. 63 (PDF 69): the marker after "Gesangchor" is a damaged "16)" — the
  editor's .md read "18)", but note 18 (the Zwiastun piece on the
  Greisenheim jubilee) belongs to the Greisenheim sentence on p. 64, while
  note 16 (Otto, Geschichte der Christlichen Gemeinschaft in Polen)
  otherwise has no marker at all.
- p. 63 (PDF 69): "Cepelli" among the Gesangverein conductors (also
  "iseiner" → "seiner" above it); "Gottlieb Lucae" on p. 58 where the
  layer reads "Lticae".
- p. 69 (PDF 75): "Spleszyński" and "Spleczyński" alternate within one
  page (the print's own inconsistency; the editor's file has
  "Spleszyniski" for the first) — both kept as printed.
- p. 70 (PDF 76): currency signs alternate between "Zł." and "Zt." line
  by line; kept as printed.
- p. 72 (PDF 78): "Reich aus Pleschen" — the layer offers "Pieschen";
  kept "Pleschen" (both witnesses of the letter o/ie ambiguous, the form
  as printed stands).
- p. 165 (PDF 173): the note marker after "Szyszyner Hol. zu übertragen"
  is damaged; both witnesses show a stray mark, and the note sequence on
  the page foot (5, 6, 7) fits a second "5)" (both statements rest on the
  same Witkowo archive file) — transcribed "5)".
- p. 249 (PDF 257): "Emilienheim (Michalinów gmina Oleśnica)" — the .md's
  "Michalinow" corrected to the print's ń per the layer.
- p. 259 (PDF 267): "33 Fleischer"" — the print's stray closing quote
  after "Fleischer kept as printed; "Bürger- und Garnisonsschule" (layer
  "Garnisonschule").
- p. 260 (PDF 268): "unsere eigenen Mitte" read as "unserer eigenen
  Mitte" per both witnesses.

## The portrait plates

PDF 10 and 11 are unnumbered portrait plates bound in between printed
pages 10 and 11: Pastor Herzberg and Pastor Ernst Johann August v. Modl.
Per the sitting's rule (no images in the output) only the typeset caption
lines are transcribed; the captions continue in engraved script
(Kurrentschrift) that neither pass could read, marked `[…]`. On the Modl
plate the line "Nach … jähriger Wirksamkeit" is damaged in the print (29?
39? — unresolved, left under the `[…]`).

## What the pages bear on

- Kalisch (printed 55-79): the parish from which the Kalischer Diözese
  takes its name; Sup. Modl appears throughout the neighbouring parishes'
  accounts; the Greisenheim and the Gesangverein matters.
- Grodziec (printed 67-79): the parish that administered Zagórów
  1843-1856 and again 1878-1892; Pastor Orive, Erdmann, Buse; the
  Kantorate Orlina, Obory, Białobłoty, Gadow.
- Konin and Maślaki (printed 163-182): Maślaki (Butterholland) is the
  filial nearest the edition's ground; its 1842 founding, the Kantorat
  Bolesławowo/Genowefa matters, and the list of Ortschaften includes the
  Trąbczyn-area villages (Dębowiec, Świętno, Wola Spławiecka).
- Zagórów and Lissewo-Pyzdry (printed 248-266): the parish of the
  edition's ground itself — Łazińsk (founded 1746, the oldest Siedlung),
  Trąbczyn, Huta Trąbczyńska, Ciemierów, Wrąbczynkowska Kolonia, the
  pastors Winkler, Biedermann, Erdmann, Groß, and the long
  Zagórów-Peisern-Kantorate conflict that produced the filial
  Lissewo-Pyzdry.
- Chapter I (printed 7-16): the framework — the diocese's parish and
  filial list as of 1936, the school statistics, the Kirchenkreis
  Bojanowo/Kalisch history with the two Konsistorialrat portraits.
