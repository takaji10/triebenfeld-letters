# -*- coding: utf-8 -*-
"""Profile 0124's top region (does the 0123 'przywileje' sentence
continue there, dropped by the lineation?) and 0131's bottom gap."""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
for n, a, b in (('0124', 470, 700), ('0131', 3540, 3770)):
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    W, H = im.size
    px = im.load()
    print('=== %s  %d-%d' % (n, a, b))
    line = []
    for y in range(a, min(H, b), 10):
        vals = [px[x, y] for x in range(250, 3700, 25)]
        dark = sum(1 for v in vals if v < 120)
        line.append('%4d:%-3d' % (y, dark))
    for i in range(0, len(line), 6):
        print('   ' + ' '.join(line[i:i + 6]))
    print()
