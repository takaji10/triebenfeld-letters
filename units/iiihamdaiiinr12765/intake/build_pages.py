# -*- coding: utf-8 -*-
"""How the editor's 37 transcription files became this unit's page files.

    python units/iiihamdaiiinr12765/intake/build_pages.py            # check only
    python units/iiihamdaiiinr12765/intake/build_pages.py --write

A record as much as a tool: it is the one place that says which lines of which
source file went where, and it was run once (2026-10-01). The editor's files, one
per scan, stay untouched in <raw_dir>/transcription/.

Three things happen to them here, all decided against the scans:

  * A scan is an opening. Each written side becomes a page: `_a1` the left,
    `_a2` the right, as split_spreads.py names the halves. The source marks the
    change of side with a blank line on six scans; on five more (0019, 0022,
    0023, 0027, 0029) both sides are written with no blank line, and the point
    where the text crosses the fold was read off the scan.
  * Each page is cut into the documents on it (the editor ruled one document
    per letter). A reply drafted on a petitioner's letter is a document of its
    own, starting partway down that page.
  * Text the receiving office wrote on someone else's letter (received marks,
    journal numbers, directions, paraphs) is moved to the end of that
    document's part of the page and listed in office_notes.yml, so the site can
    set it apart. No line is changed, added or dropped: the script checks that
    every source line lands in the page files exactly once.

SPEC rows: (scan, side, [(document, kind, [source line ranges])]). Ranges are
1-based and inclusive, in the order the lines are to stand. Document 0 is the
front matter.
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

T, O = 'text', 'office'
SPEC = [
    ('0001', 'a',  [(0,  T, [(1, 7)])]),
    # Triebenfeld to Hardenberg, 25 Oct 1814, with the reply drafted beneath it.
    # The two paraphs the source gives after the salutation stand under the draft.
    ('0003', 'a2', [(1,  T, [(1, 2), (6, 13), (16, 19)]), (1, O, [(3, 5)]),
                    (2,  T, [(20, 30), (14, 15)])]),
    ('0004', 'a2', [(3,  T, [(1, 16)])]),
    ('0005', 'a2', [(4,  T, [(4, 48)]), (4, O, [(1, 3)])]),
    ('0006', 'a2', [(5,  T, [(1, 32)])]),
    ('0007', 'a2', [(6,  T, [(2, 6)]), (6, O, [(1, 1)])]),
    ('0008', 'a1', [(6,  T, [(1, 3)])]),
    ('0008', 'a2', [(6,  T, [(5, 13)])]),
    ('0010', 'a2', [(7,  T, [(1, 9)])]),
    ('0011', 'a2', [(8,  T, [(1, 21)])]),
    ('0012', 'a1', [(8,  T, [(1, 20)])]),
    ('0012', 'a2', [(9,  T, [(22, 50)]), (10, T, [(51, 63)])]),
    ('0013', 'a1', [(10, T, [(1, 10)])]),
    ('0013', 'a2', [(11, T, [(12, 39)])]),
    ('0014', 'a1', [(11, T, [(1, 11)])]),
    ('0015', 'a2', [(12, T, [(1, 19)])]),
    ('0016', 'a2', [(13, T, [(1, 6)])]),
    # Zerboni's report; the opinion written down its margin is office text.
    ('0018', 'a2', [(14, T, [(1, 29)]), (14, O, [(30, 53)])]),
    ('0019', 'a1', [(14, T, [(1, 32)])]),
    ('0019', 'a2', [(14, T, [(33, 52)])]),
    ('0020', 'a2', [(15, T, [(1, 16)])]),
    ('0021', 'a2', [(16, T, [(1, 37)])]),
    ('0022', 'a1', [(16, T, [(1, 6)])]),
    ('0022', 'a2', [(17, T, [(7, 50)])]),
    ('0023', 'a1', [(17, T, [(1, 21)])]),
    ('0023', 'a2', [(17, T, [(22, 25)])]),
    ('0025', 'a2', [(18, T, [(1, 8)])]),
    ('0026', 'a2', [(19, T, [(24, 34)]), (19, O, [(1, 23)])]),
    ('0027', 'a1', [(19, T, [(1, 15)])]),
    ('0027', 'a2', [(19, T, [(16, 31)])]),
    ('0028', 'a2', [(20, T, [(1, 15)])]),
    ('0029', 'a1', [(20, T, [(1, 16)])]),
    ('0029', 'a2', [(20, T, [(17, 27)])]),
    ('0030', 'a2', [(21, T, [(1, 34)]), (22, T, [(35, 47)])]),
    ('0031', 'a1', [(22, T, [(1, 26)])]),
    ('0032', 'a2', [(23, T, [(21, 42)]), (23, O, [(1, 20)])]),
    ('0033', 'a2', [(24, T, [(1, 35)])]),
    ('0036', 'a2', [(25, T, [(4, 13), (17, 18)]), (25, O, [(1, 3), (14, 16)])]),
    ('0037', 'a2', [(26, T, [(1, 22)])]),
    ('0039', 'a2', [(27, T, [(3, 5)]), (27, O, [(1, 2)])]),
    ('0040', 'a1', [(27, T, [(1, 4)])]),
    ('0040', 'a2', [(27, T, [(6, 9)])]),
    ('0041', 'a1', [(27, T, [(1, 7)])]),
    ('0041', 'a2', [(28, T, [(9, 12)])]),
    ('0042', 'a1', [(28, T, [(1, 3)])]),
    ('0042', 'a2', [(29, T, [(6, 40)])]),
    ('0043', 'a1', [(29, T, [(1, 31)])]),
    ('0044', 'a2', [(30, T, [(4, 21), (23, 23), (26, 28)]),
                    (30, O, [(1, 3), (22, 22), (24, 25)])]),
]


def source_lines(src_dir):
    out = {}
    for fn in sorted(os.listdir(src_dir)):
        if not fn.lower().endswith('.txt'):
            continue
        scan = os.path.splitext(fn)[0][-4:]
        with open(os.path.join(src_dir, fn), encoding='utf-8-sig') as f:
            out[scan] = [l.rstrip('\r') for l in f.read().split('\n')]
    return out


def main():
    write = '--write' in sys.argv
    unit = unitlib.one_unit('iiihamdaiiinr12765')
    src = source_lines(os.path.join(unit.raw_dir, 'transcription'))

    pages, bounds, office, used = [], [], [], Counter()
    seen_docs = set()
    for scan, side, parts in SPEC:
        pid = f'{scan}_{side}'
        lines = []
        for doc, kind, ranges in parts:
            got = []
            for a, b in ranges:
                for n in range(a, b + 1):
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
        with open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
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
