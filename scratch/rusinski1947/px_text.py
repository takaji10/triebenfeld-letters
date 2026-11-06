# -*- coding: utf-8 -*-
"""Render suspect TEXT cells (rok/char/zrodlo) at high zoom for reading.
One panel per cell: crop the column x-range around the row band, 5x."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
ims = {}


def get(n):
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = (im, im.load())
    return ims[n]


# (sheet, row, ci, tag)
JOBS = [
    ('0147', 5, 5, '0147 r5 char'),
    ('0148', 18, 4, '0148 r18 rok'),
    ('0148', 24, 4, '0148 r24 rok'),
    ('0148', 24, 5, '0148 r24 char'),
    ('0151', 68, 6, '0151 r68 zr'),
    ('0154', 105, 6, '0154 r105 zr'),
    ('0154', 111, 6, '0154 r111 zr'),
    ('0154', 115, 5, '0154 r115 char'),
    ('0154', 115, 6, '0154 r115 zr'),
    ('0154', 116, 5, '0154 r116 char'),
    ('0157', 146, 4, '0157 r146 rok'),
    ('0157', 146, 6, '0157 r146 zr'),
    ('0158', 1, 5, '0158 r1 char'),
    ('0158', 1, 6, '0158 r1 zr'),
    ('0158', 2, 6, '0158 r2 zr'),
    ('0158', 5, 5, '0158 r5 char'),
    ('0159', 10, 4, '0159 r10 rok'),
]
panels = []
for n, num, ci, tag in JOBS:
    im, px = get(n)
    rules = RULES[n]
    y0, y1 = at[n]['rows'][str(num)]['y']
    ya, yb = max(0, y0 - 16), min(im.size[1], y1 + 34)
    c = im.crop((rules[ci] + 2, ya, rules[ci + 1] - 2, yb))
    sc = min(1420.0 / c.size[0], 500.0 / c.size[1], 5.0)
    c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
    panels.append((tag, c))
per = 4
for pi in range(0, len(panels), per):
    chunk = panels[pi:pi + per]
    W = max(p.size[0] for _, p in chunk) + 220
    H = sum(p.size[1] + 12 for _, p in chunk) + 10
    out = Image.new('L', (W, H), 255)
    d = ImageDraw.Draw(out)
    yy = 5
    for tag, p in chunk:
        out.paste(p, (215, yy))
        d.text((5, yy + p.size[1] // 2), tag, fill=0)
        yy += p.size[1] + 12
    out.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tx_%d.png'
             % (pi // per))
    print('saved tx_%d.png' % (pi // per), out.size,
          [t for t, _ in chunk])
