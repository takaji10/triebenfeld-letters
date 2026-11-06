# -*- coding: utf-8 -*-
"""Zone render with Lp-row guide lines: finds the Lp digit groups in the
Lp column (their y-centres = the print rows' anchor lines) and draws a
horizontal rule at each anchor on the figure-zone crop.

usage: python junk_eyes2.py <sheet> <y0> <y1> <tag> [coli colhi]
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

n = sys.argv[1]
ya, yb = int(sys.argv[2]), int(sys.argv[3])
tag = sys.argv[4]
coli = int(sys.argv[5]) if len(sys.argv) > 5 else 7
chi = int(sys.argv[6]) if len(sys.argv) > 6 else 11

with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
rules = RULES[n]
# Lp anchors: blobs in the Lp column with digit-like size
lx0, lx1 = rules[0] + 4, rules[1] - 4
bl = digit_read.blobs(px, lx0, lx1, max(0, ya - 40), yb + 40, minpx=200)
anch = []
for b in bl:
    h = b[3] - b[2]
    if 30 <= h <= 75 and (b[1] - b[0]) <= 60:
        anch.append((b[2] + b[3]) // 2)
# merge anchors closer than 30px
anch.sort()
merged = []
for y in anch:
    if merged and y - merged[-1][-1] < 30:
        merged[-1].append(y)
    else:
        merged.append([y])
lines = [sum(g) // len(g) for g in merged]
print('Lp anchors:', lines)

x0, x1 = rules[coli] + 2, rules[chi] - 2
c = im.crop((x0, ya, x1, yb)).convert('L')
sc = min(1420.0 / c.size[0], 1350.0 / c.size[1], 3.2)
c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
d = ImageDraw.Draw(c)
for y in lines:
    yy = int((y - ya) * sc)
    if 0 <= yy < c.size[1]:
        d.line([(0, yy), (c.size[0], yy)], fill=128, width=2)
c.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\junk_%s.png' % tag)
print('saved junk_%s.png' % tag, c.size)
