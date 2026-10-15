# -*- coding: utf-8 -*-
"""ADWł 85: from the editor's photographs and transcript to the edition.

    python units/adwl85/intake/holding.py            # check only
    ... --crop        copy the nine page images into raw_dir/processed/ under their page ids
    ... --write       page files and corpus.txt from intake/text85.py
    ... --english     write translation/doc<N>.yml from intake/english85.py
    ... --cache       put them into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding. The steps are
those of courtbook.holding_main (pipeline/intake/courtbook.py).

The unit is the volume of the visitation of the Konin deanery of 1790 and
1791 in the Diocesan Archive in Włocławek, sygn. 85. The editor has fifty
photographs of it, one page each, named by leaf (Wizytacja_0385_k_24.jpg,
..._k_24v.jpg, ..._k_25_v.jpg), and a transcript of parts of nine pages
(intake/editor_transcript.md, copied from their folder). Only those nine
pages are in the edition (the editor, 2026-10-15). Two documents, at the
editor's word the same day: the parish of Trąbczyn (leaves 23v to 25v and
28v to 29v) and the table of the souls of the parish of Zagórów (leaf 34a).

The text. The editor's transcript left out parts of the pages it covers:
the foot of leaf 24 and the head of 24v (the souls of the parish and the
baptisms, marriages and burials of 1790), the small table of 1790 on 24v,
the second half of 25 (from the measurements of the porch) and of 25v (the
bells, the ossuary, the patronage, the altars), the head of 28v, the second
half of 29 and the head of 29v (the foundations of 1668 to 1694 and the
decree of 1692), the end of 29v (the parsonage), and the margin note beside
the Zagórów table. The editor asked for these to be transcribed in session
(2026-10-15), and they were. Every page was then read against the scans,
the editor's text with it, and the edition's text is intake/text85.py,
which says what is left out and how the text is written. The editor's
expansions of the abbreviations are not kept: "JWo Mści" is not "Jego
Wysokość Magnifici" but Jaśnie Wielmożnego Mości, and the edition gives the
abbreviation as written (EDITORIAL_RULES). What changed is listed in
intake/changes.yml for the page of changes.

Not transcribed: the leaf numbers in the top right corners (in pencil and
ink) and the pencil 34 a on leaf 34a.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
import text85  # noqa: E402

SLUG = 'adwl85'
REF = 'ADWł 85'
RAW = r"J:\Documents\Archive\Genealogy\References\Archiwum Diecezjalne we Włocławku\Wizytacja"

# (file, fold, page id, -): every photograph is one page.
SCANS = [
    ('Wizytacja_0385_k_23v.jpg', None, '0023_b', None),
    ('Wizytacja_0385_k_24.jpg', None, '0024_a', None),
    ('Wizytacja_0385_k_24v.jpg', None, '0024_b', None),
    ('Wizytacja_0385_k_25.jpg', None, '0025_a', None),
    ('Wizytacja_0385_k_25_v.jpg', None, '0025_b', None),
    ('Wizytacja_0385_k_28_v.jpg', None, '0028_b', None),
    ('Wizytacja_0385_k_29.jpg', None, '0029_a', None),
    ('Wizytacja_0385_k_29_v.jpg', None, '0029_b', None),
    ('Wizytacja_0385_k_34a.jpg', None, '0034_c', None),
]
LEAF = {'0023_b': 'leaf 23 verso', '0024_a': 'leaf 24', '0024_b': 'leaf 24 verso', '0025_a': 'leaf 25',
        '0025_b': 'leaf 25 verso', '0028_b': 'leaf 28 verso', '0029_a': 'leaf 29', '0029_b': 'leaf 29 verso',
        '0034_c': 'leaf 34a'}
DOCS = text85.DOCS
ROWS = []          # the text is read whole against the scans: text85.py is the record


def read_source():
    return {(n, pid): text85.TEXT[pid] for n, ids in DOCS for pid in ids}


def english():
    import english85
    return {n: [english85.ENGLISH[pid] for pid in ids] for n, ids in DOCS}


def _summaries():
    try:
        import english85
        return english85.S, english85.HOW
    except ImportError:
        return {}, ''


S, HOW = _summaries()

if __name__ == '__main__':
    courtbook.holding_main(globals())
