# -*- coding: utf-8 -*-
"""The page on which the editor sees and moves the folds of APP 53/17/0/-/Konin Gr.145.

    python units/app53170koningr145/intake/fold_sheet.py

Writes review/app53170koningr145/folds/index.html: every scan, with the line
it is cut at. The editor clicks where a fold should be and saves the folds;
`python pipeline/intake/courtbook.py folds app53170koningr145 <the saved file>`
then copies them to folds.json beside this script and cuts the pages again
(build_pages.py reads that file). The first folds are in build_pages.py.

The editor's rule (2026-10-06): pages are whole pages cut at the fold, and the
editor approves the folds before a holding is published. On 2026-10-07 they
found the first lines crossing the ends of the left pages' lines on many
scans and asked for a page on which to move them: this one.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import build_pages as B  # noqa: E402
import courtbook  # noqa: E402


def main():
    scans, leaf = courtbook.Scans(), {}
    scans.angles = B.ANGLES
    scans.mine = set(B.ANGLES) | ({'%d.jpg' % n for n in B.FOLDS} if os.path.isfile(B._MINE) else set())
    for n in range(B.FIRST, B.LAST + 1):
        left, right = '%04d_a1' % n, '%04d_a2' % n
        scans.append(('%d.jpg' % n, B.FOLDS[n], left, right))
        leaf[left], leaf[right] = '%d verso' % (n - 1), '%d recto' % n
    assert courtbook.OVERLAP == B.OVERLAP
    courtbook.fold_sheet(ROOT, 'app53170koningr145', 'APP 53/17/0/-/Konin Gr.145', B.RAW, scans, B.SKIP, leaf)


if __name__ == '__main__':
    main()
