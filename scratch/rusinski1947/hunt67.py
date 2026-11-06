# -*- coding: utf-8 -*-
"""Zoom-read the two raised glyphs on 0105 line 2622 (after 30 / after 60)."""
import sys, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0105.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
# locate the '(30' .. 'zagonów' stretch: profile baseline zone for '('
# simpler: scan x2200-3000 word gaps in y2640-2700 (x-height zone)
runs = []
prev = False
for x in range(2100, 3100, 2):
    dark = sum(1 for y in range(2650, 2700) for xx in range(x, x+2) if px[xx, y] < 128)
    cur = dark > 6
    if cur and not prev:
        start = x
    if prev and not cur:
        runs.append((start, x))
    prev = cur
print('gaps/clusters (x-height zone):')
for a, b in runs:
    print('  cluster %d-%d w=%d' % (a, b, b - a))
