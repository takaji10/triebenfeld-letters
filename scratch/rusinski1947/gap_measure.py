# -*- coding: utf-8 -*-
"""Measure the text-band gaps per sheet: which gaps contain an editor
separator line (between-row gaps) vs which do not (within-row line
gaps) - to derive the split threshold."""
import os, io, json, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
rowlines = json.load(open(os.path.join(OCR, 'rowlines.json'),
                          encoding='utf-8'))
X0, X1 = 350, 3700

def bands(n):
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    W, H = im.size
    px = im.load()
    step = 10
    on = []
    for y in range(250, H - 40):
        dark = sum(1 for x in range(X0, X1, step) if px[x, y] < 130)
        on.append(dark >= 3)
    out = []
    y0 = None
    for i, v in enumerate(on):
        y = 250 + i
        if v and y0 is None:
            y0 = y
        elif not v and y0 is not None:
            if y - y0 >= 12:
                out.append((y0, y))
            y0 = None
    if y0 is not None:
        out.append((y0, H - 40))
    return out

for n in (sys.argv[1:] or ['0139', '0140', '0148']):
    bs = bands(n)
    els = rowlines[n]
    print('===', n, '| text bands:', len(bs), '| editor lines:', len(els))
    marked, unmarked = [], []
    for i in range(len(bs) - 1):
        g0, g1 = bs[i][1], bs[i + 1][0]
        c = (g0 + g1) // 2
        hit = any(g0 - 20 <= e <= g1 + 20 for e in els)
        (marked if hit else unmarked).append((g0, g1, g1 - g0))
    print(' MARKED gaps:', [(g1 - g0) for g0, g1, _ in marked])
    print(' UNMARKED gaps:', [(g1 - g0) for g0, g1, _ in unmarked])
