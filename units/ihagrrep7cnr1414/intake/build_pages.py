# -*- coding: utf-8 -*-
"""How the scans and the editor's transcriptions of I. HA GR, Rep. 7 C, Nr. 1414
became this unit's page images and page files.

    python units/ihagrrep7cnr1414/intake/build_pages.py            # check only
    python units/ihagrrep7cnr1414/intake/build_pages.py --crop     # cut the page images
    python units/ihagrrep7cnr1414/intake/build_pages.py --write    # write the page files

A record as much as a tool: it is the one place that says which part of which
scan is a page, and which source line went where. Follows
units/ihagrrep7cnr3709/intake/build_pages.py and
units/agad11740273/intake/build_pages.py.

The scans. Seven, of which the editor wants four (2026-10-05: "only pages
0002-0005 are relevant; the rest can be ignored"): 0001 is the modern folder,
0006 a blank opening with the archive's slip, 0007 a blank leaf. Of the four,
0002 is a single page and is copied as it is. 0003, 0004 and 0005 are openings
whose left side is blank; the editor asked for the blank pages to be cut away.
CROPS gives the written side as a box in pixels (left, top, right, bottom),
placed on a gridded view of each scan. On 0003 the written side is a slip
smaller than the leaf beneath it, and the box is the slip. Page ids: `_a` the
whole scan, `_a2` the right side of an opening.

The text. The editor's four files in <raw_dir>/txt/, one per scan, line by
line. SPEC says, for each page, which source lines it takes and in what order.
The order differs from the source in one respect only: what the department
wrote on a paper it received (the mark of receipt, the journal number, the
routing to an official, "Ad acta") is set at the end of that page and listed
in office_notes.yml, as in Nr. 3709 and Nr. 12765 (docs/NEW_UNIT.md, "A file
the office wrote on"). The slip on 0003 is such a direction as a whole. The
draft on 0002 is the department's own paper and keeps its marks where the
editor put them. The script checks that every source line is used exactly once.

Readings corrected against the scans are in corrections.py; office_notes.yml
is written there, after the corrections, because it quotes corrected lines.
"""
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'ihagrrep7cnr1414'
PREFIX = 'I_HA_Rep_7_C_Nr_1414_'

# scan -> (page id, box or None for the whole scan)
CROPS = [
    ('0002', '0002_a', None),                          # the draft of 11 January 1797
    ('0003', '0003_a2', (2480, 1480, 4660, 4100)),     # the slip: the direction of 8 January
    ('0004', '0004_a2', (2390, 60, 4930, 4350)),       # the extract of the dispatch from Venice
    ('0005', '0005_a2', (2530, 40, 5010, 4400)),       # Schrötter's letter of 29 January
]

# page id -> (document number or None to continue, [(first line, last line), ...]
# of the source file for that scan, in the order the page file takes them)
SPEC = [
    ('0002_a', 1, [(1, 23)]),
    ('0003_a2', 2, [(1, 6)]),
    ('0004_a2', None, [(4, 14), (1, 3)]),
    ('0005_a2', 3, [(4, 14), (18, 20), (1, 3), (15, 17)]),
]


def source(raw_dir):
    out = {}
    d = os.path.join(raw_dir, 'txt')
    for f in sorted(os.listdir(d)):
        scan = os.path.splitext(f)[0].rsplit('_', 1)[1]
        out[scan] = io.open(os.path.join(d, f), encoding='utf-8-sig').read().replace('\r\n', '\n').rstrip('\n').split('\n')
    return out


def crop(unit):
    from PIL import Image
    pdir = os.path.join(unit.raw_dir, 'processed')
    os.makedirs(pdir, exist_ok=True)
    manifest = {}
    for scan, pid, box in CROPS:
        src = PREFIX + scan + '.jpg'
        im = Image.open(os.path.join(unit.raw_dir, src)).convert('RGB')
        box = box or (0, 0) + im.size
        out = PREFIX + pid + '.jpg'
        im.crop(box).save(os.path.join(pdir, out), quality=95)
        manifest[src] = [{'file': out, 'bbox_original': list(box),
                          'size': [box[2] - box[0], box[3] - box[1]], 'fold_confidence': 'manual'}]
        print(f'  {src} -> processed/{out}  {box}')
    with open(os.path.join(pdir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


def main():
    unit = unitlib.one_unit(SLUG)
    if '--crop' in sys.argv:
        crop(unit)
        return
    src = source(unit.raw_dir)
    pages, bounds, problems = [], [], []
    for pid, doc, ranges in SPEC:
        scan = pid.split('_')[0]
        lines, used = [], []
        for a, b in ranges:
            lines.extend(src[scan][a - 1:b])
            used.extend(range(a, b + 1))
        if sorted(used) != list(range(1, len(src[scan]) + 1)):
            problems.append(f'{pid}: the source has {len(src[scan])} lines, SPEC uses {sorted(used)}')
        if any(not l.strip() for l in lines):
            problems.append(f'{pid}: a blank line')
        pages.append((pid, lines))
        if doc:
            bounds.append((doc, pid, 1))
    if sorted(src) != sorted(p.split('_')[0] for p, _, _ in SPEC):
        problems.append('the source files and SPEC do not name the same scans')
    if problems:
        sys.exit('NOT WRITTEN\n' + '\n'.join(problems))
    print(f'{len(src)} source files -> {len(pages)} pages, {len(bounds)} documents; '
          'every source line placed exactly once')
    for pid, lines in pages:
        print(f'  {pid:<8} {len(lines):>2} lines  {lines[0][:36]!r} ... {lines[-1][-30:]!r}')
    if '--write' not in sys.argv:
        return
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    for pid, lines in pages:
        with open(os.path.join(tdir, PREFIX + pid + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
    rdir = unitlib.review_dir(unit.slug)
    os.makedirs(rdir, exist_ok=True)
    for d in (rdir, HERE):
        with open(os.path.join(d, 'document_boundaries.csv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(['letter_id', 'first_page', 'first_line'])
            w.writerows(bounds)
    print('wrote transcriptions/ and document_boundaries.csv')


if __name__ == '__main__':
    main()
