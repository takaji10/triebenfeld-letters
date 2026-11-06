# How the nmpol work came in

## What is here

Only the 23 entries the gazetteer cites (the editor's match-sheet
decisions of 2026-10-26), not the works whole - a deliberate exception to
the plan's whole-work rule, recorded here. The works' full texts live in
the private place-name repository (Igor's), which is where they belong.

## The text

Each entry is the citation text of `review/place_name_sources/citations_pass1.json`,
corrected on 2026-10-27: for the scanned volumes by three OCR witnesses
(whole-page tesseract with the Polish model, a zoomed single-line crop
re-read, and a document-conversion OCR of the same crops), for the
born-digital volumes against the publisher PDFs' own text layer. The
fixes are logged in `data/matches/` of that repository.

## The English

`english.md` is a SUMMARY of each entry (type, location, size, date range
of the forms), not a translation; the Polish original is the record. When
the work becomes visible the summaries should be replaced by real
translations.

## Visibility

`visible: false`, like seidel2018 and dabrowska1976: in the corpus,
searchable when questions are put to the edition, no page on the site.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> In the corrected text of 2026-10-27. Brought in so the citations can be
> checked against the works' own words without opening the volumes; not a
> republication of the dictionaries, which stay whole in the private place-
> name repository. No page of text on the site: the works are reference, not
> narrative, and the gazetteer's footnotes stay unresolved until the editor
> decides otherwise.

## The Drzewce entry re-read from the page image (2026-11-06)

The editor supplied the page image of vol. 2, p. 443 (the entry's locator in
the edition's records, p. 444, was a page off). The three-witness OCR text
of 2026-10-27 had garbled the entry's special characters — d with a dot
below (ḑ), z with a caron (ž), v with an accent (ṽ), k with an accent (ḱ) —
which is where the gazetteer's "Drzevvyc7a" and "VCe" came from: the OCR's
Drzevvyc7a was **Drzewycza** (de Drzewycza 1418 AC II nr 117) and its
DrLe\VCe was **Drzewce** (1881 SG II 182). The section in `original.md` is
re-read from the image (the (6) fragment of the next Drzewce, gm. Poniec,
kept as the citation text ran to the page's end there); the gazetteer's
drzewce.yml carries the corrected forms. The dialect line
("gw. ḑžyfće, -cuf, ḑžyṽecḱi") is the editor's correction of Claude's
first take (2026-11-06: ṽ → f in the first two forms, -ḱi for -ḱ), settled.

## The locator shift, confirmed systematic (2026-11-06)

A second page image from the editor (Czarnybród, **vol. 2, p. 196**, against
the records' p. 197) confirms what Drzewce showed (444 → 443): the place-name
repository's page counting is **one page off against the printed pages**. Per
the editor's word, every NMP locator was shifted −1 — the 23 headings here
and in `english.md`, and the gazetteer's 23 footnote texts and nmpol
locators (drzewce exempt, already image-corrected). **The basis**: the two
t. 2 entries are image-confirmed; the rest ride the systematic inference.
The caveat: vols 1-6 came from the clean transcription and vols 7-18 from
RCIN — the two groups' offsets could differ, so the non-t.-2 shifts
(including t. 14 and t. 15 from RCIN) are to be verified against the
sources when images come to hand. The Czarnybród section was also re-read
from its image: the leading «BCz» was the previous entry's signature glued
on by the OCR (off the record), the 1980 pair carries its comma, and the
dialect line is «gw. čorny brut, -ygo -du, čornobrocḱi.» — the editor saw
the c with a caron and the k with an accent, the same ḱi ending as
Drzewce's. The other 22 entries' locators may carry the same
page-number shift (NEEDS_CONFIRMATION).
