# Słowo, 4 January 1892: "Sprzedaże dóbr" — notes

A sale notice under the rubric "Sprzedaże dóbr" in the "Kronika ekonomiczna"
of Słowo, R. XI, nr 2 (4 January 1892), p. 3, digitised by Crispa, the
University of Warsaw's digital library
(https://crispa.uw.edu.pl/object/files/30152/display/PDF).

## How it came in (2026-10-22)

The editor: add the item, the image in Downloads (`3-DPI300.jpg`, a crop of
the page at 300 dpi — a column of the "Kronika ekonomiczna", the notice with
the column's opening note above it), and "only this snippet of the article
is needed"; Tesseract may be used.

- **What is transcribed**: the "Sprzedaże dóbr" notice only — five printed
  lines, two sales. The column's opening note above it (the spiritus trade
  in Warsaw, quoting „Wiest. Finan.") is not part of the item and is not
  transcribed; it shows in the crop.
- **How it was read**: Tesseract 5.5.3, pol (tessdata_best), the page as it
  is (psm 6 and psm 4) and upscaled ×2 (psm 6); word-level zooms of the
  doubtful spots at ×6 to ×14. The passes agree on almost everything; five
  spots went to the editor on the spot sheet
  (`scratch/slowo1892_sheet.py`, answers in
  `review/slowo18920104/query_answers.json`, on the working machine).
- **The rulings of the sheet** (2026-10-22):
  - `zas` → **za** — the print has no acute over the s; the line reads
    "Władysławowa Wielopolska za 225,000 rs."
  - `wladyslawowa` → **Władysławowa** — the longer form, the married form
    (the wife of a Władysław), stands.
  - `peckiu` → **peckim,** — the print is grammatical ("w pow. słupeckim");
    the draft's "peckiu" was the zoom's misreading of the m.
  - `mark159` → the editor read the crop's words as "**peckim, 150 włók**"
    — the number is **150**, not the draft's 159 (the last digit a 9 only
    to two OCR passes and the first zoom), and nothing printed stands
    between the comma and "150": the vertical streak before the number is
    the digitisation's, left out.
  - `edge` → **leave out** — the sliver at the foot of the image is left
    out; the notice reads complete without it.
- **Line division**: as printed, five lines, with "¬" at "Luto¬/stański"
  and "słu¬/peckim," (the Kuryer Polski convention).
- **Kept as printed**: the rubric's leading "—" stands. "rs." stands (the
  ruble in silver, rubli srebrnych), as do "31,000" and "225,000" with the
  comma as the print sets the thousands, and "150 włók" as the editor read
  the figure on the sheet (two OCR passes and the first zoom had said 159;
  the x2 upscale's "150" was the reading that held).
- **Left out**: the vertical streak before "150" on the fourth line and the
  sliver at the foot of the image — the digitisation's, not the print's
  (the editor's rulings on the sheet).

## What it bears on

- **What the index takes.** The item's one hit is Trąbczyn ("Trąbczyn",
  ruled in `newspapers/index.yml`); the box "In the newspapers" shows it on
  the estate's page on /places/. The notice's "hr. Miączyńskiego" is not
  matched by the edition's patterns (the genitive after "hr." is outside
  the Miączyński entries' forms, and Włodzimierz's own pattern is pinned to
  one document of the lawsuit by `only_in`); the reading lives in the
  transcription and this notes file. Repphan, Lutostański, Tomisławice and
  the buyer's "Wielopolska" have no patterns.
- **The estate's transfer out of the Miączyński family.** The era's
  ownership line (`reference/eras.yml`, the wlodzimierz era) has Count
  Włodzimierz Miączyński holding Trąbczyn to his death in 1879, "then his
  nephew Władysław Miączyński, and by 1892 Countess Maria Wielopolska".
  This notice of 4 January 1892 is the press witness of the transfer: the
  count selling is the Miączyński of the years between, Władysław; the
  countess buying is the one the line ends with.
- **The buyer's name.** The press names the buyer "hr. Władysławowa
  Wielopolska" — by her husband's name (the wife of a Władysław
  Wielopolski) — where the era's ownership line has "Countess Maria
  Wielopolska". If Maria is the wife the married form points to, the two
  name one woman. Open (NEEDS_CONFIRMATION, "The newspapers").
- **The servitude buy-out of 1892.** The era's account has the Łazińsk
  colony's rights in the forest Studzianka given up in 1892 for 393 Morgen
  of manor land. This notice shows the ownership changing hands in the
  same months; whether the sale and the buy-out are one transaction's two
  sides is not said by either source, and the item does not say so.
- **150 włók → the draft's 159.** The draft read "159 włók" (two OCR
  passes, the first zoom); the editor read the figure "150" on the sheet,
  and the x2 upscale's pass had said the same. "150 włók" stands in the
  transcription. The edition's documents measure in Morgen; no conversion
  is attempted here.
- **Tomisławice** (powiat turecki, 17 włók, Repphan → Lutostański,
  31,000 rs.) is not the edition's; it stands in the notice and nowhere in
  the corpus.

## Open

- The spot sheet's five rulings (2026-10-22, above) — all worked in.
- The buyer's name: whether "Władysławowa Wielopolska" of the press and
  "Countess Maria Wielopolska" of the era's ownership line name one woman
  (NEEDS_CONFIRMATION, "The newspapers").
- Publishing at the editor's word, as always.
