# BK PAN Cz2271, Kuryer Polski 1754, nr 75

One document on one page: the report from Kalisz, 5 December 1754, on the
funeral of Paweł Prusimski at Trąbczyn, in the Warsaw newspaper Kuryer
Polski, no. 75 of 1754 (25 December). The first holding from print and
from a library (the editor, 2026-10-16: units "that might not necessarily
come from archives - think articles/announcements from newspapers").
Added 2026-10-16: read from the image in session, translated, summarised,
claim-checked, with its page. The editor looked at the one doubtful word
on the spot sheet and kept it as it stands; **published at their word on
2026-10-16**.

Everything about how the holding was made is in the docstring of
`intake/holding.py`.

## Provenance

The editor's folder `Kuryer Polski 1754, nr. 75` has the issue's three
images from the Wielkopolska Digital Library
(https://www.wbc.poznan.pl/dlibra/publication/85857/edition/99614/content),
openings of two pages at 300 dpi, and their crop of the left page of the
second (`..._0002_0001_crop.png`), which is page `0002_a`. The editor gave
the library (PAN Biblioteka Kórnicka), its shelfmark (Cz2271), the place of
printing (Warsaw) and the date of the issue. The page head of the first
image shows "Num. LXXV" and "Annô 1754"; the day is the editor's and the
digital library's.

- **Repository**: `bkpan-kornik` in `reference/repositories.yml` and the
  credits, "BK PAN"; a library, not an archive. The reference is
  "Cz2271, Kuryer Polski 1754, nr 75", so the site shows "BK PAN Cz2271,
  Kuryer Polski 1754, nr 75". Another issue of the same newspaper would be
  another holding with the same shelfmark and its own number (slug
  `kuryerpolski<year><number>`).
- **Document type** `newspaper` ("Newspaper report", "Zeitungsbericht").
- Dated by the report's dateline (5 December), placed at Kalisz.

## The text

- Line by line as printed, the printer's letters kept (ſ, ß, æ, á); "¬" at
  a broken line end. The line-break pass did not know words with the long
  s and split five of them ("Pru¬ſińſkich", "Gło¬wiecki"): ruled as joins
  by hand in `linebreak_decisions.csv`.
- One mark of doubt: "[Cleri?]" before "Sæcularis", faint print, kept by
  the editor on the spot sheet (2026-10-16). The summaries do not rest on it.
- "Łędzki" is Ląd, the Cistercian abbey (the editor, 2026-10-16). Kaźmierz
  is said on the holding's page to be probably Kazimierz Biskupi; not
  confirmed, and not in the place index.

## People and places

- Paweł, Antoni and Katarzyna Prusimski matched in the printer's spelling
  (the matcher reads ſ as s); Głowiecki, abbot of Ląd, new.
- Ląd new in `reference/places.yml`: it also finds "konwent Lądzki" in the
  boundary decree of 1775 (owner of Drzewce), "Kloster Ląd" in the Prussian
  table of about 1797 and in six contracts of Oe 1 Bü 14526. All read and
  right.

## Still to do

Nothing.
