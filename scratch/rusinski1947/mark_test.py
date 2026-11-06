# -*- coding: utf-8 -*-
"""The raised-mark experiment: sum ALL digits found in a-series dymy
(c8) and ludn (c10) cells - main figures and small raised marks alike -
and compare against the print's RAZEM (2386 / 12967). Tests both
interpretations (marks counted vs ignored)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
cur = None
AS = {'0139', '0140', '0141', '0142', '0143', '0144', '0145', '0146'}
rows = []
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur in AS:
        c = [x.strip() for x in ln.split('|')][1:-1]
        if len(c) < 11:
            continue
        rows.append((cur, int(c[0]), c[8], c[10]))

def digits(v):
    return [int(d) for d in re.findall(r'\d+', v)]

for ci, name, want in ((2, 'dymy', 2386), (3, 'ludn', 12967)):
    strict = 0      # only single-number cells
    marks = 0       # every digit group counted
    marked_cells = []
    for sh, num, dym, lud in rows:
        v = (dym, lud)[ci - 2]
        ds = digits(v)
        if not ds:
            continue
        if len(ds) == 1:
            strict += ds[0]
            marks += ds[0]
        else:
            marks += sum(ds)
            marked_cells.append('%s r%d %s=%r -> %d'
                                % (sh, num, name, v, sum(ds)))
    print('%s: strict(1st num only)=%d  all-digits=%d  want=%d'
          % (name, strict, marks, want))
    print('  strict residue: %d   all-digits residue: %d'
          % (want - strict, want - marks))
    for mc in marked_cells:
        print('  marked:', mc)
