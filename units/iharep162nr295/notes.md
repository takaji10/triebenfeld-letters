# I. HA Rep. 162, Nr. 295 (GStA PK)

The cover and eleven pages of copies, papers of 28 January to 13 March 1805,
from the head of a file the Prussian state treasury kept from 1820 to March
1827 on the 50,000 thalers that Peter Friedrich von Triebenfeld had borrowed
from the Invalids' Fund and secured on the Zagórów estates. Scaffolded on
2026-10-05: the page images are made; nothing is transcribed yet, so the
holding is `draft` and the build skips it.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, I. HA Rep. 162
Verwaltung des Staatsschatzes, Nr. 295. Older marks on the cover: "Rep 162",
"Sectio III Pars. 26. No: 1", "Vol. I, cont. Vol. 2", "1820 bis med: Maerz
1827", and the numbers 295 (blue pencil) and 281 (red, struck through). The
printed heading is "Central-Activa", with "Pohlen" written under it. The
editor's folder calls it "Capital on the Zagorow estates, now owned by
Trzcinski".

- **Photographs.** 23 images taken by the editor at the archive on 28 July
  2023 with a telephone (`PXL_20230728_*.jpg`, 3072 by 4080 pixels), the file
  lying on a table and a hand holding the page flat. The first is the cover.
  The other 22 are eleven pages, each photographed twice: the top of the page,
  then the bottom, overlapping by more than half the page.
- **Page images.** `intake/build_pages.py --crop` joins each pair into one
  image of the whole page and cuts the page out, into
  `<raw_dir>/processed/I_HA_Rep_162_Nr_295_<page id>.jpg`. `0001_a` is the
  cover, `0002_a` to `0012_a` the eleven pages in the order photographed. How
  the join is made, and what was checked, is in that script's heading; the
  numbers are in `intake/stitch.json`.
  - Above the seam a page image is the top photograph unchanged; below it,
    the bottom photograph laid onto the top one. The seam runs through the
    gap between two lines of writing, so no line is doubled, lost, or made of
    two photographs. On pages 0003, 0005, 0007 and 0009 the seam crosses the
    tail of a letter in a few places (under 2 in 100 of its length); the two
    photographs agree there to within about two pixels.
  - Outside the written area the two photographs do not always agree, because
    the page was not lying the same way in both: a small step can be seen at
    the fold on 0005 and at the edge of the leaves on 0006 and 0009. No
    writing is affected.
  - The hand holding the page is in the right or left margin of most images.
- **What is not there.** The pages carry no leaf numbers in the photographs.
  The last page (0012) ends with the opening words of a further mortgage
  certificate ("Die in der Provinz Südpreußen und deren Ko-"), which was not
  photographed. Nothing from the file's own years, 1820 to 1827, was
  photographed.

## What the pages are

Read from the page images on 2026-10-05, before any transcription, to write
`unit.yml`; to be checked against the text.

| Page | Content |
|---|---|
| 0001 | Cover |
| 0002-0004 | "Abschrift". Triebenfeld's bond for 50,000 thalers to the General Invalids' Fund, Berlin, 28 January 1805, pledging the Prince of Hohenlohe-Ingelfingen's bond of 1 June 1804 for 250,000 thalers |
| 0004-0005 | "Actum Berlin, den 28. Januar 1805": the bond acknowledged before a court at Berlin, signed Wilmanns |
| 0005-0007 | "Wir Friedrich Wilhelm ...": the South Prussian Regierung's certificate of the acknowledgement at Kalisz, with the record of 27 February 1805; given at Kalisz, 5 March 1805 |
| 0007-0008 | "Vigore decreti de 5. hujus ...": the note of the entry in the mortgage book of the Konin district, on Zagórów, Drzewce and Kopojno; Kalisz, 13 March 1805 |
| 0008-0012 | The mortgage certificate for Zagórów, Kalisz, 13 March 1805, headed at its end "Hypotheken-Schein ... No. 1179" |
| 0012 | The first line of a further certificate |

The marks in brackets in the margin beside the opening of a piece (0002,
0005, 0008, 0012) note the stamped paper of the original, for example
"(6 ggr. Stempel)".

## Transcription

None yet. The editor transcribes from the page images in
`<raw_dir>/processed/`, one text file per image. Named like the images
(`I_HA_Rep_162_Nr_295_0002_a.txt`) and put in `units/iharep162nr295/
transcriptions/`, they are read by `import_pages.py` as they are
(`unit.yml`, `transcriptions:`).

How the pages divide into documents is to be settled then. By the edition's
rule a deed and its acknowledgements are one document, so the likely division
is two: the bond with its acknowledgements and registry note (0002 to the
middle of 0008), and the mortgage certificate (from the middle of 0008).

## Quirks worth knowing

- Everything is a copy made for the file, in one clerk's hand: signatures are
  "gez.", seals "L. S.".
- The file is of 1820 to 1827, the papers copied into it of 1805;
  `date_span` gives 1805, the years of what was photographed.
- This is the "Invalids' Fund loan of 1805" named in section III of the era
  essay, and the loan of 250,000 thalers on Zagórów is also in Oe 1 Bü 14525.

## Damage

None recorded.
