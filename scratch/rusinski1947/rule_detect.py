# -*- coding: utf-8 -*-
"""Detect the print's horizontal row rules on an annex sheet and
compare with the editor's separator lines."""
import os, io, json, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
rowlines = json.load(open(os.path.join(OCR, 'rowlines.json'),
                          encoding='utf-8'))

n = sys.argv[1] if len(sys.argv) > 1 else '0139'
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
W, H = im.size
px = im.load()
# sample the central span (the table's width)
X0, X1 = 400, 3600
step = 12
prof = []
for y in range(300, H - 60):
    dark = sum(1 for x in range(X0, X1, step) if px[x, y] < 128)
    prof.append((y, dark / ((X1 - X0) // step)))
# rules: sustained dark fraction
rules = []
run = []
for y, f in prof:
    if f > 0.45:
        run.append(y)
    else:
        if len(run) >= 3:
            rules.append(sum(run) // len(run))
        run = []
if len(run) >= 3:
    rules.append(sum(run) // len(run))
print('sheet', n, '| editor lines:', len(rowlines[n]))
print('detected rules (%d):' % len(rules), rules)
print('editor lines:', rowlines[n])
# agreement
matched = []
for el in rowlines[n]:
    best = min(rules, key=lambda r: abs(r - el)) if rules else None
    matched.append((el, best, abs(best - el) if best is not None else None))
print('editor -> nearest rule:')
for el, r, d in matched:
    print('  %5d -> %5s (d=%s)' % (el, r, d))
unmatched_rules = [r for r in rules
                   if all(abs(r - el) > 25 for el in rowlines[n])]
print('rules NOT near an editor line:', unmatched_rules)
