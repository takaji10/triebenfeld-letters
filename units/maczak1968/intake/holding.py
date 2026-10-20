# -*- coding: utf-8 -*-
"""Mączak 1968, Export of Grain: from the editor's PDF to the edition.

    python units/maczak1968/intake/holding.py            # check only
    ... --crop        render the map (p. 81) and the chart (p. 97) from the PDF
                      into raw_dir/processed/0081_a.jpg and 0097_a.jpg
    ... --write       page files and corpus.txt from intake/text/
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding (2026-10-20). The
steps are those of courtbook.holding_main (pipeline/intake/courtbook.py). There
is no --english: the article is printed in English (rulings.yml, language).

The second holding of published literature (unit.yml, kind: literature). The
editor gave the PDF "Antoni Mączak - Export of Grain 1550-1650.pdf" (J:\\...\\
References\\Books), the digital copy in RCIN of the Institute of History of the
Polish Academy of Sciences (ABBYY FineReader, 2012; every page stamped
http://rcin.org.pl): 24 pages, the whole article, pp. 75 to 98 of Acta
Poloniae Historica 18 (1968). The editor wants it as "supporting material for
the agricultural activities of the Olęders"; how useful it is will be judged
later (the editor, 2026-10-20).

The PDF has a text layer (OCR), with the usual faults: spaced-out surnames
("M ałow ist"), "com" for "corn", lost diacritics, the sideways Table 2 in
pieces. It was not taken over. Every page was read from the page images,
rendered at 300 dpi and cut in three bands, and the reading was then compared
word by word with the OCR to catch anything left out (nothing was). The
figures of Tables 2 and 4 were checked by their own sums: every column of
Table 2 adds up to 100, and the totals and yearly averages of Table 4 are those
of its rows.

How it is written down (intake/text/<page>.txt, one file per printed page):
- by paragraph: each line is a paragraph, a heading, a footnote, a caption or
  a row of a table. The running heads, page numbers and the printer's
  signature marks (6 on p. 81, 7 on p. 97) are left out, and so is RCIN's
  stamp;
- the footnote marks as raised figures (¹ to ⁴³), each page's notes at its
  foot (footnotes.yml sets them apart). The marks of Table 3's notes are raised
  letters (ᵃ, ᵇ);
- the tables as rows, "| cell | cell |", a cell set across two columns given
  as "<" in the column it covers (Table 5's figures for Warsaw, the heads of
  Tables 1, 4, 6 and 7). The reading view draws them as tables
  (build_site_data.text_table_html). Italics are not marked, also in Table 2,
  where they set the percentages apart from the lasts: the note under the
  table says which is which, and the figures show it;
- the print as it stands, its slips included: "wirtschafliche" (n. 1), "von
  Bath" beside "van Bath" (p. 77), "cummulative", "statical", "differenciated"
  (twice), "landlors" (twice), "achievments", "the sale or rye" (Table 3),
  "rythm" (n. 12), "according the figures" (Table 1), "Lustrácja" (n. 18),
  "oligarchial", "elswhere", "contituted" (n. 25), "Transilvanian",
  "cristalizing", "heberdashery", "The questions is", "quater", "consited",
  "nean", "200 Rdl." (for 200 thousand), "merchants’profits", "cautios",
  "enetered", "a sometimes mason’s", "Krakowie a latach" (n. 42),
  "discused" (map), "Ellehoj", "22 thous," and the year 1663 in Table 6,
  which the text gives as 1653;
- what the print has damaged is read as the word it is: a comma half lost
  after "granen" (n. 6), "be" with a broken e ("bs" in the OCR, p. 90);
- the ł of Polish names and titles in the small type of the notes (Małowist,
  Wrocław, Biała Góra, połowie, wołami, kapitałem, Małopolska) does not
  always show its stroke at this resolution; it is given as the body text
  prints it;
- the notes of p. 88 seem not to answer their marks (note 23 speaks of credit,
  the mark 23 of Kula on terms of trade; note 24 of the shares of land, the
  mark 24 of the magnates as bankers). They are given as printed;
- typographic quotes and apostrophes, "—" for the dash, the print's spaced
  hyphen in spans of years ("1550 - 1650"); "1°" and "2°" as printed (p. 95);
- a word that runs over the end of a page is given whole on the page where
  it begins, and the next page starts after it (PAGE_ENDS below); a
  paragraph that runs on (no word broken) simply continues on the next page;
- pages 81 and 97 are the map and the chart: their images, and their words
  (caption, legend, the titles of the chart's six panels) as text.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402

SLUG = 'maczak1968'
REF = 'Mączak 1968, Export of Grain'
PDF = r"J:\Documents\Archive\Genealogy\References\Books\Antoni Mączak - Export of Grain 1550-1650.pdf"
RAW = r"J:\Documents\Archive\Genealogy\References\Mączak 1968, Export of Grain"

# The two pages that are pictures: (page of the PDF, page id, box at 300 dpi
# (left, top, right, bottom)). The box holds the figure and its caption, without
# the running head above or the signature mark and RCIN's stamp below; a margin
# of 40 pixels round the printed area.
FIGURES = [(7, '0081_a', (215, 444, 1783, 2344)),
           (23, '0097_a', (176, 440, 1749, 2445))]
SCANS = [('0081_a.jpg', None, '0081_a', None), ('0097_a.jpg', None, '0097_a', None)]
LEAF = {'0081_a': 'page 81, the map', '0097_a': 'page 97, the chart of prices and wages'}

PAGES = ['%04d_a' % n for n in range(75, 99)]
DOCS = [(1, PAGES)]
ROWS = []

# What was moved across a page end (in the reading, in session): (page where the
# word begins, what it reads whole).
PAGE_ENDS = [
    ('0077_a', 'prosperous (p. 78 "perous")'),
    ('0086_a', 'constituted (p. 87 "stituted")'),
    ('0089_a', 'especially (p. 90 "cially")'),
    ('0094_a', 'existence (p. 95 "istence")'),
]


def crop():
    """Render the map and the chart from the PDF into RAW/processed/ (grey, 300 dpi)."""
    import fitz
    from PIL import Image
    out = os.path.join(RAW, 'processed')
    os.makedirs(out, exist_ok=True)
    doc = fitz.open(PDF)
    for n, pid, box in FIGURES:
        pix = doc[n - 1].get_pixmap(dpi=300, colorspace=fitz.csGRAY)
        im = Image.frombytes('L', (pix.width, pix.height), pix.samples)
        im.crop(box).save(os.path.join(out, pid + '.jpg'), quality=92)
        print('wrote', pid, box)


def read_source():
    out = {}
    for pid in PAGES:
        lines = io.open(os.path.join(HERE, 'text', pid[:4] + '.txt'), encoding='utf-8').read().rstrip('\n').split('\n')
        assert all(l.strip() for l in lines), pid
        assert not any('¬' in l for l in lines), pid
        out[(1, pid)] = lines
    return out


def english():
    raise SystemExit('the article is printed in English: there is no translation to write')


def _summaries():
    import summaries as M
    return M.S


S = None
HOW = ('written in the working session from the English of the article as read\n# (intake/holding.py, 2026-10-20).')

if __name__ == '__main__':
    if '--crop' in sys.argv:
        crop()
    if '--summaries' in sys.argv:
        S = _summaries()
    sys.argv = [a for a in sys.argv if a != '--crop']
    courtbook.holding_main(globals())
