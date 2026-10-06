# -*- coding: utf-8 -*-
"""How the scans and the editor's transcription of APP 53/6/0/-/40 became this
unit's page images, page files and corpus.

    python units/app536040/intake/build_pages.py            # check only
    python units/app536040/intake/build_pages.py --crop     # cut the page images
    python units/app536040/intake/build_pages.py --sheet    # the fold page for the editor
    python units/app536040/intake/build_pages.py --write    # page files and corpus.txt (once)

The images. Five from the archive, named by the editor after the leaves:

    368.jpg        leaf 368 recto, one page: the heading of the court's sitting
                   at the top, then the beginning of another entry
    372.jpg        leaf 372 recto, one page: the end of another entry, then
                   our entry under its heading
    372v-373.jpg   an opening: leaf 372 verso | leaf 373 recto
    373v.jpg       leaf 373 verso, one page: the last nine lines of our
                   entry, then another entry ("Chwałkoska ...")
    Image00001.jpg the label on the cover of the volume, "Z. KONIN 43": not
                   a page, not used

Page ids follow the edition's rule for these books: leaf N recto is <N>_a2,
leaf N verso is <N+1>_a1. Only the opening is cut; the three single pages are
copied whole. Every page is kept whole, with the other entries on it, which
are not transcribed.

The text. The editor's file marks each page by its leaf: "[368]" the
heading of the sitting, "[372]" to "[373v]" the entry. One document of five
pages: the heading is its first page, because it dates the entry.

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

SLUG = 'app536040'
REF = 'APP 53/6/0/-/40'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Decreta [inducta] 1722-1780 (53.6.0.-.40)"

# (file, x of the fold or None for a single page, left page or the page, right
# page). The fold is a first proposal: where the editor has moved it on the
# fold page and saved it, folds.json beside this script is used instead
# (courtbook.placed).
SCANS = [
    ('368.jpg', None, '0368_a2', None),
    ('372.jpg', None, '0372_a2', None),
    ('372v-373.jpg', 2650, '0373_a1', '0373_a2'),
    ('373v.jpg', None, '0374_a1', None),
]
SKIP = ()
LEAF = {'0368_a2': '368 recto', '0372_a2': '372 recto', '0373_a1': '372 verso', '0373_a2': '373 recto',
        '0374_a1': '373 verso'}
PAGE_OF = {'368': '0368_a2', '372': '0372_a2', '372v': '0373_a1', '373': '0373_a2', '373v': '0374_a1'}
DOCS = [(1, ['0368_a2', '0372_a2', '0373_a1', '0373_a2', '0374_a1'])]


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head, head
    assert [l for l, _ in leaves] == ['368', '372', '372v', '373', '373v'], [l for l, _ in leaves]
    return {PAGE_OF[leaf]: paras for leaf, paras in leaves}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    pages = read_source()
    print(len(pages), 'pages,', sum(len(' '.join(p).split()) for p in pages.values()), 'words')
    if '--crop' in sys.argv:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS), SKIP)
    if '--sheet' in sys.argv:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS), SKIP, LEAF,
                             note='Three of the four images are single pages and are not cut. Other entries stand on '
                                  'every page; the pages are kept whole.')
    if '--write' in sys.argv:
        courtbook.write_pages(UNIT_DIR, DOCS, pages)


if __name__ == '__main__':
    main()
