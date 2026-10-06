# -*- coding: utf-8 -*-
"""How the scan and the editor's transcription of APP 53/6/0/-/36 became this
unit's page images, page files and corpus.

    python units/app536036/intake/build_pages.py            # check only
    python units/app536036/intake/build_pages.py --crop     # cut the page images
    python units/app536036/intake/build_pages.py --sheet    # the fold sheet for the editor
    python units/app536036/intake/build_pages.py --write    # page files and corpus.txt (once)

The image. One scan from the archive, 53_6_0_-_36_91328209.jpg: an opening of
the book of decrees of the land court at Konin, leaf 641 verso on the left
and leaf 642 recto on the right. It is cut at the fold into two whole pages,
named after the leaf on the right: 0642_a1 and 0642_a2. The top third of leaf
641 verso is the end of another entry, and the lower half of leaf 642 has two
more ("Strzałkowsky", "Kurowsky"); the pages are kept whole and those parts
are not transcribed.

The text. The editor's file marks each page by its leaf:

- "[612]", the heading of the court's sitting, 1644. Leaf 612 is not among
  the scans, so the heading is not a page of the edition. It is kept here
  (printed by this script), quoted on the holding's page, and is the ground
  for the documents' year.
- "[641v]": the first entry, with its heading.
- "[642]": the last line of the first entry, then the second entry.

Two documents, one for each entry (the editor's ruling of 2026-10-06). Page
0642_a2 carries the end of the first and the whole of the second.

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

SLUG = 'app536036'
REF = 'APP 53/6/0/-/36'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Decreta [inducta] 1641-1644 (53.6.0.-.36)"

# (file, x of the fold, left page, right page). The fold is the gutter between
# the two leaves, looked at on the scan, 2026-10-06.
SCANS = [('53_6_0_-_36_91328209.jpg', 1803, '0642_a1', '0642_a2')]
SKIP = ()
LEAF = {'0642_a1': '641 verso', '0642_a2': '642 recto'}
DOCS = [(1, ['0642_a1', '0642_a2']), (2, ['0642_a2'])]


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head, head
    assert [l for l, _ in leaves] == ['612', '641v', '642'], [l for l, _ in leaves]
    heading = leaves[0][1]
    verso, recto = leaves[1][1], leaves[2][1]
    assert len(verso) == 2 and len(recto) == 2, (len(verso), len(recto))
    assert recto[1].startswith('Similis Contra Eosdem'), recto[1][:40]
    parts = {(1, '0642_a1'): verso, (1, '0642_a2'): [recto[0]], (2, '0642_a2'): [recto[1]]}
    return heading, parts


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    heading, parts = read_source()
    print('heading of the sitting (leaf 612, no scan): %s' % ' '.join(heading))
    print(len(parts), 'parts of pages,', sum(len(' '.join(p).split()) for p in parts.values()), 'words')
    if '--crop' in sys.argv:
        courtbook.cut(RAW, SCANS, SKIP)
    if '--sheet' in sys.argv:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, SCANS, SKIP, LEAF,
                             note='Both pages carry other entries as well; they are kept whole.')
    if '--write' in sys.argv:
        courtbook.write_pages(UNIT_DIR, DOCS, parts)


if __name__ == '__main__':
    main()
