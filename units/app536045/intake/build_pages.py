# -*- coding: utf-8 -*-
"""How the scan and the editor's transcription of APP 53/6/0/-/45 became this
unit's page images, page files and corpus.

    python units/app536045/intake/build_pages.py            # check only
    python units/app536045/intake/build_pages.py --crop     # cut the page images
    python units/app536045/intake/build_pages.py --sheet    # the fold sheet for the editor
    python units/app536045/intake/build_pages.py --write    # page files and corpus.txt (once)

The image. One scan from the archive, 673.jpg: an opening of the book of
decrees of the land court at Konin, leaf 653 verso on the left and leaf 654
recto on the right. It is cut at the fold into two whole pages, 0673_a1 and
0673_a2. The upper half of leaf 653 verso is the end of the entry before
(no. 16, another matter); the page is kept whole and that part is not
transcribed.

The text. The editor's file marks each page by its leaf. It has three parts:

- "[638]", the heading of the court's sitting: "Actum in Judiciis
  Terrestribus ... Anno Domini Millesimo Septingentesimo Sexagesimo Tertio in
  Conin". Leaf 638 is not among the scans, so the heading is not a page of
  the edition. It is kept here (HEADING), quoted on the holding's page, and
  is the ground for the document's year.
- "[653v]" and "[654]", entry no. 17: the document.

Do not run --write again after corrections.py --write: it would put the
uncorrected text back.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app536045'
REF = 'APP 53/6/0/-/45'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Decreta [protocollon] 1750-1765 (53.6.0.-.45) (Konin)"

# (file, x of the fold, left page, right page). A first proposal: where the
# editor has moved a fold on the fold page and saved it, folds.json beside
# this script is used instead (courtbook.placed). The fold is the gutter between
# the two leaves, looked at on a strip, 2026-10-06.
SCANS = [('673.jpg', 1728, '0673_a1', '0673_a2')]
SKIP = ()
LEAF = {'0673_a1': '653 verso', '0673_a2': '654 recto'}
PAGE_OF = {'653v': '0673_a1', '654': '0673_a2'}
DOCS = [(1, ['0673_a1', '0673_a2'])]

HEADING_LEAF = '638'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head, head
    assert [l for l, _ in leaves] == ['638', '653v', '654'], [l for l, _ in leaves]
    heading = leaves[0][1]
    pages = {PAGE_OF[leaf]: paras for leaf, paras in leaves[1:]}
    return heading, pages


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    heading, pages = read_source()
    print('heading of the sitting (leaf %s, no scan): %s' % (HEADING_LEAF, ' '.join(heading)))
    print(len(pages), 'pages,', sum(len(' '.join(p).split()) for p in pages.values()), 'words')
    if '--crop' in sys.argv:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS), SKIP)
    if '--sheet' in sys.argv:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS), SKIP, LEAF,
                             note='The upper half of the left page is the end of the entry before; the page is kept whole.')
    if '--write' in sys.argv:
        courtbook.write_pages(UNIT_DIR, DOCS, pages)


if __name__ == '__main__':
    main()
