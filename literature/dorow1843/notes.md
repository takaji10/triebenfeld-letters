# Dorow (1843): how it came in

## The source

Wilhelm Dorow, *Erlebtes aus den Jahren 1813-1820*, part II (Leipzig 1843).
The scan is the Staatsbibliothek zu Berlin's digitisation: PPN 167107372X,
Bibl. Varnhagen 936, PURL
http://resolver.staatsbibliothek-berlin.de/SBB000290D900020000,
Public Domain Mark 1.0, 239 pages. The editor's PDF is at
`C:/Users/Tersnaus/Downloads/"Erlebtes aus den Jahren 1813-1820 (Dorow, 1843).pdf"`
(245 MB, downloaded 2026-10-19, the day of the first literature sitting, and
left unprocessed until now); it is image-only (jsPDF assembly of the SBB page
images, no text layer), and its first page is the digitisation's own
metadata page, not part of the book - it is not brought in. The scan carries
no title page of the volume: it begins with the Vorwort's first page (the
Wellington/Baron v. Eben passage), so the volume's bibliographic record
rests on the digitisation's metadata page and the contents page.

The editor's word (2026-11-01): the memoir only - the piece the volume prints
from Triebenfeld's manuscript, not the whole part II.

## What the excerpt is

The part II contents list the piece as "Pohlen unter Friedrich II. und
Friedrich Wilhelm II. vom Kriegsrath v. T. ... Seite 11". In the volume's
counting the memoir's title leaf (the PDF's page 32) and its Goethe motto
leaf (PDF 33) are printed pp. 11-12 (unnumbered on the leaves themselves),
and the text runs printed pp. 13-24 (PDF 34-45), ending with Hardenberg's
verdict of November 1816; Reischach's piece begins at printed p. 25 (PDF 46).
The excerpt brings the two leaves (as the work's front) and pp. 13-24.
Dorow's cross-reference on the title leaf - "Siehe I. Theil Seite 19" - and
his telling of how the manuscript came to him (submitted to him in 1813 by
Triebenfeld, shown to Hardenberg in November 1816) belong to part I, which
this scan does not hold; the Materialien's note 152 sums that up.

The memoir's own title, on printed p. 13: "Skizze, wie Pohlen von Preußen
benutzt werden, und wie Preußen wenigstens seine Interessen für die dahin
geliehenen siebenundzwanzig Millionen Thaler erhalten kann." The memoir
speaks of its author in the third person and names him in parentheses - "Ein
biederer Mann (Kriegsrath v. Triebenfeld)", "der damaligen
Departementsrath, der dies Fach bearbeitete (Kriegsrath v. Triebenfeld)" -
which is what the Materialien's note 152 calls the source's own way
(the extract's "( )" pointers are the 1861 compiler's, but these two
parentheses are in the 1843 print).

## How it was read

- The PDF's pages 32-45 rendered at 300 dpi and read with Tesseract 5.5.3,
  `script/Fraktur` traineddata from tessdata_best fetched into
  `%LOCALAPPDATA%\Tesseract\tessdata` (that directory already held the deu
  and pol models of the newspaper work; deu does not read Fraktur, and the
  install's own tessdata carries English only). The model is recorded in
  WORKING_NOTES for the next Fraktur source.
- Every doubtful line re-read as a 900 dpi band in both the Fraktur and the
  deu models. The Fraktur model's standing noise: the long s comes through
  as `ſ` (transcribed `s` throughout; the capital `J` of the Fraktur face
  transcribed `I`, as the editor's own file of the Materialien does); the
  `ch` of `nicht`, `durch`, `beschützen` and friends is often dropped
  (`niht`, `durh`); the `tz` ligature is misread as `ß` (`benußt`,
  `Saß`, `Küß`) or `st` (`Eigennust`); stray quote marks, commas and
  hyphens appear at line ends. All settled by sense, by the deu pass and by
  the Materialien witness, except the nine readings on the spot sheet
  (`scratch/dorow1843_sheet.py`, answers in
  `review/dorow1843/query_answers.json`).
- The second engine planned was the lunaroute document converter (as for
  Kraus 2001), but the converter takes only a URL or base64, and this
  session could reach neither the SBB's IIIF nor a local server, so it was
  not used. The human witness in its place: the Materialien (1861) reprints
  this memoir in extract, pp. 205-216, in the editor's own file - read line
  against line with `difflib` after the draft was composed. The
  eng-model pass over the same 300 dpi pages was also made (for word-count
  checking) and stands in `C:/Users/Tersnaus/AppData/Local/Temp/opencode/dorow300/`.

## The spot sheet's answers (2026-11-01)

Eight of the nine rows answered (`review/dorow1843/query_answers.json`), all
worked into `original.md`:

- **9/5 Procent (p. 14): 5 Procent.** The editor read the digit with the
  deu pass and the Materialien's reprint; the Fraktur model's 9 was its
  error. The English follows ("5 per cent").
- **gebauset/gehauset (p. 15): gehauset.** The print's word is the
  reprint's; the Fraktur pass's b was its misreading of the h. The English
  follows ("had dwelt").
- **Offizcianten (p. 15): Officianten.** The broken word is the reprint's
  form; the Fraktur model read the ci as iz. Note the memoir's own whole-word
  occurrence on printed p. 17, read "Offizianten" by both passes and not
  ruled: it stands as read, and the two spellings stand as the print gives
  them (recorded here rather than silently mended).
- **Würkungskreis (p. 21): Würkungskreis.** The print's form stands against
  the reprint's "Wirkungskreis"; an attested older form of Wirkung.
- **bewürken (p. 21): bewürken.** The same ruling, against the reprint's
  "bewirken".
- **kukken (p. 23): kukken.** As the reprint has it.
- **Michelis (p. 22): Michelis.** The print's form stands against the
  reprint's "Michaelis".
- **Title leaf: Pohlen.** The display word confirmed.
- **Not answered: the cross-reference row.** The form of the numeral in
  "Siehe I. Theil Seite 19." stays as the draft has it ("Siehe I. Theil
  Seite 19.", the passes' "1r Theil"/"Ir Theil" both pointing to a roman I);
  open in NEEDS_CONFIRMATION ("The literature").

## The Materialien's reprint and this print

The Materialien (1861) reproduces the memoir from Dorow's printing "nur im
Auszuge, hie und da mit einem Fingerzeig in ( )" (its note 152). Read
against the 1843 print, its additions and omissions are:

- Added motto: the Vollgräff quotation (*Moderne Politik*, S. 652) follows
  the Goethe motto on the Materialien's p. 205. The scan's motto leaf shows
  the Goethe quotation only; the Vollgräff motto is presumably on the
  leaf's verso, which the recto-only scan does not carry.
- Added pointers, which the print does not have: "(—)" after "Conto fand."
  (p. 205), "(?—)" after "kaum 5 Procent ... betragen haben." (p. 206),
  "(Siehe S. 128)" after "weiter nichts" (p. 212), "(war der auch ein
  Pole?—)" after "Karl George von Hessen" (p. 214).
- Omissions, small: "auf 6 Jahr" before "à 5 Procent jährlich" (p. 215);
  the closing sentence in Dorow's own form ("diese waren die Worte des
  Fürsten v. Hardenberg, als D. demselben die Schrift ... mittheilte."),
  which the Materialien reformulates as its introduction to the quotation.
- Its own slips, kept unmarked where the print reads differently: "man
  rieth ihm, sich nur an diesen zu *werden*" (p. 215; the print reads
  "wenden"); the inserted table of the civil suits of 1790 (its note 153,
  from Holsche, *der Netzdistrikt*, p. 267) printed mid-sentence on its
  p. 208, interrupting "Hunderte von Prozessen gegen / ihre Herrschaften" -
  the table is the Materialien's own and stands in no way in the 1843
  print.
- Silent normalisations of spelling, which the 1861 print makes and the
  1843 print does not: *daß* for *dass*, *Große* for *Grosse*, *Preußen*
  for *Preussen* (the 1843 print reads *Preußen* with ß where the OCR shows
  it, and the vowel-length spellings are its own), *jetzigen* for the
  print's *jezigen*, *baten* for the print's *bathen*, *Wirkungskreis* for
  the print's *Würkungskreis* (both passes), *benutzt* (the print's tz
  ligature), *Officianten* (see the spot sheet), *Michaelis* (see the spot
  sheet), *etc.* for the print's *2c.*

Where the two differ, the 1843 print stands here (the scan is the source
brought in); the Materialien keeps its own text as printed.

## The print's own forms kept

- "mit das Haus Brandenburg verbunden" (the slip the Materialien marked
  [sic] on its p. 205) and "strebten sie nach das Vermögen der Gutsbesitzer"
  (unmarked there) stand as printed.
- The old orthography throughout: *Thlr.*, *2c.*, *quaest.*, *Mahl* (for
  Mal), *bathen*, *thaten*, *benuzt* forms as the sheet rules, *jezigen*,
  *beseelt*, *ney* forms of *sey*, "den vierten Groschen nach gegeben".
- The parenthesised self-identifications and the closing "D." (Dorow) are
  the print's own abbreviations.
- Punctuation follows the print as the passes show it, including the comma
  of "kaum 9 Procent gegen, den alten Satz" (both passes; the reprint has
  no comma) - read on the spot sheet's crop.

## The figures

The memoir is Triebenfeld's own account, and its figures are his: the 10 per
cent of the old classification and the 24 volunteered (with the Silesian 28
and Hoym's wished-for 5), the 36,000 thalers of the Kammergericht councillor
"Sch —" lent to "B—i" on Sulislawice, the 27 million thalers of the title,
the 2—3 and at most 4 per cent of the funds' papers, Prince Karl George of
Hessen's purchase for circa 230,000 and his valuation at 800,000, costing
him about 3500 thalers (the valuers Wildeganns, Korn and Schröter), the
200,000 asked of Heymann Ephraim at 5 per cent with the 30,000
proxeneticum. The memoir does NOT print the story of Triebenfeld's own
estate (bought 1797 for 50,000, sold to Prince George of Hessen-Darmstadt,
resold for 750,000) - that story is Łukasiewicz's (1997) telling of Dorow's
printing; the register's entry and the edition's letters (400,000 and
750,000) stand against both (the standing rule, docs/LITERATURE_PLAN.md
section 23). And Łukasiewicz's "the buying of the head of the valuation
commission cost him 35 000" is his figure, not the memoir's: the memoir
makes the valuation itself cost the prince "etwa 3500 Thlr." (p. 22) - a
figure ten times smaller.

## The conventions

- The transcription is the scan's text, never tidied: line breaks of the
  print reflowed into paragraphs (the house rule, as `kneifel1937`), the
  page marks `[p. N]` at the printed pages, the two unnumbered leaves before
  them as the work's front.
- Long s transcribed s, the Fraktur capital J transcribed I, ß kept where
  the print has it, the print's abbreviations and slips kept.
- The `[.]` elision mark (the Kneifel convention) is not needed: the excerpt
  is bounded by the volume's own pieces and nothing inside is cut.
