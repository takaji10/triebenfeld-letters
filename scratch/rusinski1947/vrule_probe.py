# -*- coding: utf-8 -*-
"""Probe vertical rules: column darkness over one row band."""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
n = sys.argv[1]
a, b = int(sys.argv[2]), int(sys.argv[3])
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
W, H = im.size
px = im.load()
cols = []
for x in range(150, W - 100):
    vals = [px[x, y] for y in range(a, b, 3)]
    frac = sum(1 for v in vals if v < 140) / len(vals)
    cols.append((x, frac))
# report columns with sustained darkness
runs = []
run = []
for x, f in cols:
    if f > 0.5:
        run.append(x)
    else:
        if len(run) >= 8:
            runs.append((run[0], run[-1]))
        run = []
if len(run) >= 8:
    runs.append((run[0], run[-1]))
print('vertical rules in band %d-%d:' % (a, b), runs)
