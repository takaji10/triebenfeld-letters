# -*- coding: utf-8 -*-
"""Profile the six S23 gap zones: row darkness to count actual text
lines between the last body line and the first note line. A blank gap
(+ the thin separator rule) means the sentence continues overleaf; dark
bands mean physically damaged lines (lacuna)."""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
GAPS = [
    ('0064', 2280, 2440),
    ('0114', 3540, 3790),
    ('0116', 4050, 4300),
    ('0123', 3250, 3480),
    ('0124', 4150, 4410),
    ('0132', 2610, 2880),
]
for n, a, b in GAPS:
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    W, H = im.size
    px = im.load()
    print('=== %s  %d-%d' % (n, a, b))
    rows = []
    for y in range(a, min(H, b), 10):
        vals = [px[x, y] for x in range(250, 3700, 25)]
        dark = sum(1 for v in vals if v < 120)
        rows.append((y, dark))
    # print as compact bands
    line = []
    for y, d in rows:
        line.append('%4d:%-3d' % (y, d))
    for i in range(0, len(line), 6):
        print('   ' + ' '.join(line[i:i + 6]))
    print()
