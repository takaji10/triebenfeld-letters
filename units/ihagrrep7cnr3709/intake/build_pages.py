# -*- coding: utf-8 -*-
"""How the editor's 20 transcription files became this unit's page files.

    python units/ihagrrep7cnr3709/intake/build_pages.py            # check only
    python units/ihagrrep7cnr3709/intake/build_pages.py --write

A record as much as a tool: it is the one place that says which lines of which
source file went where, and it was run once (2026-10-04). The editor's files, one
per scan, stay untouched in <raw_dir>/transcription/. The same method as
units/iiihamdaiiinr12765/intake/build_pages.py.

Two things happen to them here, both decided against the scans:

  * Each page is cut into the documents on it (the editor ruled one document
    per letter). A page here is a scan: an opening with writing on both sides
    was not split in this unit, so no source file is divided between pages.
  * Text the receiving office wrote on someone else's letter (received marks,
    journal numbers, the decree for the reply, paraphs) is moved to the end of
    that document's part of the page and listed in office_notes.yml, so the site
    can set it apart. No line is changed, added or dropped: the script checks
    that every source line lands in the page files exactly once.

SPEC rows: (scan, side, [(document, kind, [source line ranges])]). Ranges are
1-based and inclusive, in the order the lines are to stand; ALL is the whole
file. Document 0 is the front matter.
"""
import csv
import io
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PREFIX = 'I_HA_Rep_7_C_Nr_3709_'
T, O = 'text', 'office'
ALL = [(1, None)]
SPEC = [
    ('0001', 'a',  [(0,  T, ALL)]),
    # The Poznań government's report of 18 June 1800. The ministry's: the date
    # at the head, "ad acta" with the paraph, and the mark at the foot.
    ('0002', 'a2', [(1,  T, [(2, 4), (8, 33)]), (1, O, [(1, 1), (5, 7), (34, 34)])]),
    ('0003', 'a2', [(2,  T, ALL)]),
    # Its report of 10 July 1800. The ministry's: the date at the head, "ad
    # Acta" with the paraph, the mark beside the signatures, the journal numbers.
    ('0004', 'a2', [(3,  T, [(2, 7), (11, 24), (26, 37)]),
                    (3,  O, [(1, 1), (8, 10), (25, 25), (38, 39)])]),
    ('0005', 'a2', [(4,  T, ALL)]),
    # The Prince's petition to the Grand Chancellor, with the date it came in
    # and the journal number.
    ('0007', 'a2', [(5,  T, [(2, 17)]), (5, O, [(1, 1), (18, 19)])]),
    # The petition ends on the left; his covering letter begins on the right.
    ('0008', 'a',  [(5,  T, [(1, 7)]), (6, T, [(8, 19)])]),
    ('0009', 'a',  [(6,  T, ALL)]),
    ('0010', 'a',  [(6,  T, ALL)]),
    ('0011', 'a2', [(7,  T, ALL)]),
    # Three rescripts drafted one under another, parted by "# # #".
    ('0012', 'a2', [(8,  T, [(1, 28)]), (9, T, [(29, 43)])]),
    ('0013', 'a',  [(9,  T, [(1, 8), (10, 19)]), (10, T, [(20, 48)])]),
    ('0014', 'a2', [(11, T, ALL)]),
    ('0015', 'a1', [(11, T, ALL)]),
    # The Poznań government's report of 18 December 1800, with the decree for
    # the answer written at its head and the journal number at its foot.
    ('0016', 'a2', [(12, T, [(7, 37)]), (12, O, [(1, 6), (38, 38)])]),
    ('0017', 'a2', [(13, T, ALL)]),
    ('0018', 'a2', [(14, T, ALL)]),
    ('0019', 'a1', [(14, T, ALL)]),
    # Prusimska's petition to the King. Above it: the Cabinet's remittal to the
    # minister, the received mark, and the minister's decree.
    ('0020', 'a2', [(15, T, [(16, 24)]), (15, O, [(1, 15)])]),
    ('0021', 'a1', [(15, T, ALL)]),
]


def source_lines(src_dir):
    out = {}
    for fn in sorted(os.listdir(src_dir)):
        if not fn.lower().endswith('.txt'):
            continue
        scan = os.path.splitext(fn)[0][-4:]
        with open(os.path.join(src_dir, fn), encoding='utf-8-sig') as f:
            ls = [l.rstrip('\r') for l in f.read().split('\n')]
        while ls and not ls[-1].strip():
            ls.pop()
        out[scan] = ls
    return out


def main():
    write = '--write' in sys.argv
    unit = unitlib.one_unit('ihagrrep7cnr3709')
    src = source_lines(os.path.join(unit.raw_dir, 'transcription'))

    pages, bounds, office, used = [], [], [], Counter()
    seen_docs = set()
    for scan, side, parts in SPEC:
        pid = f'{scan}_{side}'
        lines = []
        for doc, kind, ranges in parts:
            got = []
            for a, b in ranges:
                for n in range(a, (b or len(src[scan])) + 1):
                    if not src[scan][n - 1].strip():
                        continue
                    got.append(src[scan][n - 1])
                    used[(scan, n)] += 1
            if doc and doc not in seen_docs:
                seen_docs.add(doc)
                bounds.append((doc, pid, len(lines) + 1))
            if kind == O:
                office.append((doc, pid, got[0], len(got)))
            lines.extend(got)
        pages.append((pid, lines))

    # Nothing lost, nothing doubled: every non-blank source line exactly once.
    bad = []
    for scan, ls in src.items():
        for n, l in enumerate(ls, 1):
            want = 1 if l.strip() else 0
            if used[(scan, n)] != want:
                bad.append(f'{scan} line {n}: used {used[(scan, n)]} time(s), want {want}')
    missing = sorted(set(src) - {s for s, _, _ in SPEC})
    if bad or missing:
        sys.exit('NOT WRITTEN\n' + '\n'.join(bad + [f'scan {m} has no SPEC row' for m in missing]))
    print(f'{len(src)} source files -> {len(pages)} pages, {len(bounds)} documents, '
          f'{len(office)} office blocks; every source line placed exactly once')
    if not write:
        return

    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    for pid, lines in pages:
        with open(os.path.join(tdir, PREFIX + pid + '.txt'), 'w', encoding='utf-8',
                  newline='\n') as f:
            f.write('\n'.join(lines) + '\n')

    rdir = unitlib.review_dir(unit.slug)
    os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, 'document_boundaries.csv'), 'w', encoding='utf-8',
              newline='') as f:
        w = csv.writer(f)
        w.writerow(['letter_id', 'first_page', 'first_line'])
        w.writerows(bounds)

    def q(s):
        return "'" + s.replace("'", "''") + "'"
    with open(os.path.join(UNIT_DIR, 'office_notes.yml'), 'w', encoding='utf-8',
              newline='\n') as f:
        f.write(
            "# Text the receiving office wrote on someone else's letter: received marks,\n"
            "# journal numbers, directions for the reply, paraphs. The lines are ordinary\n"
            "# text in corpus.txt; this file only says which they are, so the site can set\n"
            "# them apart. Each block stands at the end of its document's part of the page\n"
            "# (editor, 2026-10-01), wherever it is written on the sheet.\n"
            "#   first: the block's first line exactly as it stands in corpus.txt\n"
            "#   lines: how many lines the block has\n"
            "# A first line that is edited must be edited here too; build_db.py stops if a\n"
            "# block cannot be found. A reply drafted on the page is not listed here: it is a\n"
            "# document of its own.\n"
            "blocks:\n")
        for doc, pid, first, n in office:
            f.write(f"  - letter: '{doc}'\n    page: '{pid}'\n"
                    f"    first: {q(first)}\n    lines: {n}\n")
    print('wrote transcriptions/, office_notes.yml and', os.path.join(rdir, 'document_boundaries.csv'))


if __name__ == '__main__':
    main()
