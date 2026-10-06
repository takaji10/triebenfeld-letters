# -*- coding: utf-8 -*-
"""How the scans and the editor's transcription of APP 53/6/0/-/17 became this
unit's page images, page files and corpus.

    python units/app536017/intake/build_pages.py            # check only
    python units/app536017/intake/build_pages.py --crop     # cut the page images
    python units/app536017/intake/build_pages.py --sheet    # the fold page for the editor
    python units/app536017/intake/build_pages.py --write    # page files and corpus.txt (once)

The images. Three scans from the archive, each an opening of the book of the
land court at Konin for 1589:

    53_6_0_-_17_76256864.jpg   leaf 26 verso | leaf 27 recto
    53_6_0_-_17_76256865.jpg   leaf 27 verso | leaf 28 recto
    53_6_0_-_17_76256866.jpg   leaf 28 verso | leaf 29 recto

The one entry the editor transcribed begins under its heading on leaf 27 and
ends at the top of leaf 27 verso. So two pages are pages of the edition,
named after the leaf on the right of their scan: 0027_a2 (leaf 27) and
0028_a1 (leaf 27 verso). The other halves of those two scans are cut and set
apart (SKIP); the third scan is not cut. The pages are kept whole.

What else is on the scans and is NOT transcribed (for the editor to decide):
three more entries about the same people. On leaf 27 verso and leaf 28, a
second "Lukomski Visionem expediet", Albertus Thrampczinski Otha against
Stanislaus Łukomski, in nearly the same words as ours. On leaves 28 and 28
verso, "Thrampczinskich Visio", Nicolaus and Joannes Thrampczinski against
Albertus, over a pond and a mill between Trąbczyn and Szetlewo. On leaves 28
verso and 29, "Eorundem Visio", the same against Albertus.

The text. The editor's file marks each page by its leaf and has four parts:

- "[2]", the heading of the court's sitting, 1589. Leaf 2 is not among the
  scans: not a page; printed by this script, quoted on the holding's page,
  the ground for the document's year.
- "[22]", an entry headed "Thrampczinski Liber" which the editor marks "not
  relevant - about Szetlewo and a mill". Leaf 22 is not among the scans and
  the text is a first reading that cannot be checked: left out.
- "[27]", our entry with its heading.
- "[27v]", its end, given TWICE: two readings of the same lines. The first
  is taken; the second is left out (the editor, 2026-10-07: "obviously
  don't import duplicate pages").

Do not run --write again after corrections.py --write.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app536017'
REF = 'APP 53/6/0/-/17'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Inscriptiones, relationes, decreta [inducta] 1589 (53.6.0.-.17)"

# (file, x of the fold, left page, right page). A first proposal: where the
# editor has moved a fold on the fold page and saved it, folds.json beside
# this script is used instead (courtbook.placed).
SCANS = [
    ('53_6_0_-_17_76256864.jpg', 1749, '0027_a1', '0027_a2'),
    ('53_6_0_-_17_76256865.jpg', 1752, '0028_a1', '0028_a2'),
]
SKIP = ('0027_a1', '0028_a2')
LEAF = {'0027_a1': '26 verso', '0027_a2': '27 recto', '0028_a1': '27 verso', '0028_a2': '28 recto'}
DOCS = [(1, ['0027_a2', '0028_a1'])]


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head, head
    assert [l for l, _ in leaves] == ['2', '22', '27', '27v'], [l for l, _ in leaves]
    heading = leaves[0][1]
    recto, verso = leaves[2][1], leaves[3][1]
    assert len(recto) == 2 and recto[0].startswith('# '), recto[0]
    assert len(verso) == 2 and verso[1].startswith('[...]'), 'the second reading of leaf 27 verso is expected last'
    parts = {(1, '0027_a2'): [recto[0][2:], recto[1]], (1, '0028_a1'): [verso[0]]}
    return heading, parts


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    heading, parts = read_source()
    print('heading of the sitting (leaf 2, no scan): %s' % ' '.join(heading))
    print(len(parts), 'pages,', sum(len(' '.join(p).split()) for p in parts.values()), 'words')
    if '--crop' in sys.argv:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS), SKIP)
    if '--sheet' in sys.argv:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS), SKIP, LEAF,
                             note='Two of the four halves carry the transcribed entry. A third scan (leaves 28 verso and 29) '
                                  'has none of it and is not used.')
    if '--write' in sys.argv:
        courtbook.write_pages(UNIT_DIR, DOCS, parts)


if __name__ == '__main__':
    main()
