# BK PAN Kodeks Dyplomatyczny Wielkopolski

**Set up, waiting for the editor's entries (2026-10-16). Not on the site:**
the settings are `unit.yml.draft`, so the build does not see the holding.
Rename it to `unit.yml` when the first entries go in.

## What the editor decided (2026-10-16)

- **One holding** for every entry the edition uses, whatever its volume;
  **each entry is its own document**. Volumes named: 1, 2, 3, 5, 6, 7, 8,
  11, all from the Kórnik Library (PAN Biblioteka Kórnicka) in the
  Wielkopolska Digital Library (WBC).
- **Text only.** The WBC has the Kodeks only as a proofed electronic text,
  one HTML file a volume, with no page images and no printed page numbers.
  Each document's page shows its text, its citation (volume, number) linked
  to the volume in the WBC, and "From the electronic text of a printed
  edition: there is no page image."
- **The whole entry is the transcription**: the Kodeks's number, the
  editors' heading (place and date, volumes 6 to 11), their summary (Latin
  in 1 to 5, Polish in 6 to 11), their sources, the text, their notes.
- **A new era**, working name `medieval` ("Trąbczyn in the Middle Ages"),
  first in order. Written and tried, held back as `intake/add_era.py` until
  there are documents (an empty era would show on the site).

## The sources

`intake/kdw_source.py` has the eight volumes (VOLUMES: WBC id, year,
title, years, numbers) and reads any entry by volume and number. The
volumes' texts are saved in the editor's references folder, `Kodeks
Dyplomatyczny Wielkopolski/KDW_T<vv>_wbc<id>.html`, downloaded 2026-10-16
from `https://www.wbc.poznan.pl/Content/<id>/download/`. The WBC answers a
burst of requests with a "High Load" page of 1.7 KB: fetch one volume at a
time and check the size (volume 3 needed a second try).

Entries found per file: vol. 1: 612 (nos. 1-616), 2: 674 (617-1292),
3: 761 (1293-2053), 5: 738 (1-738), 6: 400 (1-400), 7: 379 (401-773),
8: 304 (774-1074), 11: 324 (1700-2023). Numbers restart in volume 5 and in
volume 6, so an entry is always named by volume and number.

In volumes 6 to 11 "[s. 443]" in a text is the page of the manuscript the
editors printed from, not of the Kodeks. Some entries of volume 5 are only
a summary ("R." at the start).

## How a document is made

`intake/holding.py`: add `(document number, volume, Kodeks number)` to
ENTRIES, then `--write` (page file, corpus, and the `citation:` block and
`by_paragraph` list of rulings.yml), and by hand in rulings.yml each
document's date (`dates: read:` from the heading or dateline), place,
language and `doc_type`. Page id `NNNN_a`, NNNN the document number; no
image. Tried end to end with volume 6, no. 198 on 2026-10-16 (built,
verified, then taken out again).

## Open

- The name of the era (working name `medieval`).
- The page images of the modern volumes are not used (text only), but
  their text is: volumes 6 to 11 were published 1982 to 1999, and the WBC
  names the Kórnik Library as rights holder. Before the site is shared
  widely (NEEDS_CONFIRMATION).
