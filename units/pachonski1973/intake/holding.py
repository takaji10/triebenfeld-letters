# -*- coding: utf-8 -*-
"""Pachoński 1973, Les Polonais dans la République de Venise: from the editor's scans to the edition.

    python units/pachonski1973/intake/holding.py            # check only
    ... --crop        cut the map (page 246) into raw_dir/processed/0246_a.jpg
    ... --write       page files and corpus.txt from intake/text/
    ... --english     write translation/doc1.yml from intake/english.py
    ... --cache       put it into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding (2026-10-20). The
steps are those of courtbook.holding_main (pipeline/intake/courtbook.py).

The first holding of published literature (unit.yml, kind: literature). The
editor scanned the book (600 dpi, black and white; the cover in colour) and
asked for Pachoński's article only, scans 2026-10-17-0001_2R.tif to
2026-10-17-0011_1L.tif, pages 237 to 256: "only the text needs to be
included", with the footnotes, an English translation, and the map. The
book's other scans (01.tif to 11.tif: cover, series page, title, imprint,
contents, presentation) gave its title and imprint and are not in the
edition.

There was no transcription. The article was read from the scans in session,
each page in five overlapping bands about 1700 pixels wide; doubtful words
were looked at again enlarged ("da grade", "contre-cadidat", the title).
Nothing was unreadable: the print is clean, and there is no mark of doubt.

How it is written down (intake/text/<page>.txt, one file per printed page):
- by paragraph: each line is a paragraph, a heading, a footnote, or a line of
  the map's legend. The running heads and page numbers are left out;
- the footnote marks as raised figures, as printed (¹ to ³¹), and each page's
  notes at its foot, after its text (footnotes.yml sets them apart);
- the print as it stands, its slips included ("da grade", "contre-cadidat",
  "Néanmois", "suiverent", "plusiers", "italiannes", "officieurs", "lietenant",
  "la Russe"); typographic apostrophes and the print's « » guillemets; roman
  numerals of months in capitals (7.II.1795; the print has small capitals);
  italics not marked;
- a word or note that runs over the end of a page is given whole on the page
  where it begins, and the next page starts after it (page_ends below). The
  pipeline would otherwise join the broken word to the footnote under it.
- page 246 is the map: its image, and its legend as text.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402

SLUG = 'pachonski1973'
REF = 'Pachoński 1973, Les Polonais dans la République de Venise'
RAW = r"D:\Pictures\Scans\Italia, Venezia e Polonia - Tra illuminismo e romanticismo (1973, Branca ed.)"

# The map only. The scan is the page turned on its side (5491 x 3336, the map
# printed across the page); the printed map and its frame lie between x 1384
# and 5160, y 260 and 3230. Cut at the sides with a margin of 40 pixels.
SCANS = [('2026-10-17-0006_1L.tif', None, '0246_a', None)]
EDGES = {'2026-10-17-0006_1L.tif': (1344, 5200)}
LEAF = {'0246_a': 'page 246, the map'}

# The book's pages, in order; the scan each was read from.
PAGES = ['%04d_a' % n for n in range(237, 257)]
SCAN_OF = {
    '0237_a': '2026-10-17-0001_2R.tif', '0238_a': '2026-10-17-0002_1L.tif', '0239_a': '2026-10-17-0002_2R.tif',
    '0240_a': '2026-10-17-0003_1L.tif', '0241_a': '2026-10-17-0003_2R.tif', '0242_a': '2026-10-17-0004_1L.tif',
    '0243_a': '2026-10-17-0004_2R.tif', '0244_a': '2026-10-17-0005_1L.tif', '0245_a': '2026-10-17-0005_2R.tif',
    '0246_a': '2026-10-17-0006_1L.tif', '0247_a': '2026-10-17-0006_2R.tif', '0248_a': '2026-10-17-0007_1L.tif',
    '0249_a': '2026-10-17-0007_2R.tif', '0250_a': '2026-10-17-0008_1L.tif', '0251_a': '2026-10-17-0008_2R.tif',
    '0252_a': '2026-10-17-0009_1L.tif', '0253_a': '2026-10-17-0009_2R.tif', '0254_a': '2026-10-17-0010_1L.tif',
    '0255_a': '2026-10-17-0010_2R.tif', '0256_a': '2026-10-17-0011_1L.tif',
}
DOCS = [(1, PAGES)]
ROWS = []

# What was moved across a page end (applied once to the reading, in session):
# (page where the word or note begins, what it reads whole).
PAGE_ENDS = [
    ('0237_a', 'gouvernement (p. 238 "vernement")'),
    ('0238_a', 'note 4, whose last line ("700 bateaux de commerce ... à désirer.") the print sets at the head of the notes of p. 239'),
    ('0241_a', 's’efforçait (p. 242 "çait")'),
    ('0242_a', 'Légion (p. 243 "gion")'),
    ('0243_a', 'apportés, (p. 244 "tés,")'),
    ('0245_a', '(contrada (p. 247 "trada", after the map)'),
    ('0249_a', 'attitude (p. 250 "tude")'),
    ('0254_a', 'défense (p. 255 "fense")'),
    ('0255_a', 'polono-italiannes (p. 256 "italiannes", the hyphen the compound’s own)'),
]


def read_source():
    out = {}
    for pid in PAGES:
        lines = io.open(os.path.join(HERE, 'text', pid[:4] + '.txt'), encoding='utf-8').read().rstrip('\n').split('\n')
        assert all(l.strip() for l in lines), pid
        assert not any('¬' in l for l in lines), pid
        out[(1, pid)] = lines
    return out


def english():
    import english as E
    return {1: [E.ENGLISH[pid] for pid in PAGES]}


def _summaries():
    import english as E
    return E.S


S = None
HOW = ('written in the working session from the French as read from the scans\n# (intake/holding.py, 2026-10-20).')

if __name__ == '__main__':
    if '--crop' in sys.argv:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS, EDGES))
    if '--summaries' in sys.argv:
        S = _summaries()
    sys.argv = [a for a in sys.argv if a != '--crop']
    courtbook.holding_main(globals())
