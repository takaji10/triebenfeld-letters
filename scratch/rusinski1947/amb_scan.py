# -*- coding: utf-8 -*-
"""Precise x-positioned blob scans for the last ambiguous junk cells."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()
ims = {}


def get(n):
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = (im, im.load())
    return ims[n]


# (sheet, row, col, ya, yb) - scan window chosen around the band top
JOBS = [
    ('0151', 78, 8, 3130, 3230),
    ('0154', 105, 8, 380, 470),
    ('0154', 112, 8, 1790, 1880),
    ('0156', 134, 8, 575, 665),
    ('0156', 137, 8, 1040, 1130),
    ('0156', 144, 8, 2510, 2600),
    ('0157', 146, 8, 1480, 1560),   # the disputed 2,7 vs 4,7 line
    ('0158', 3, 8, 860, 950),
    ('0158', 4, 8, 1055, 1145),
    ('0158', 6, 8, 1465, 1560),
    ('0158', 7, 8, 1625, 1720),
    ('0158', 8, 8, 1865, 1960),
]
for n, num, ci, ya, yb in JOBS:
    im, px = get(n)
    rules = RULES[n]
    x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
    bl = digit_read.blobs(px, x0, x1, ya, yb, minpx=25)
    print('=== %s r%d c%d y%d-%d' % (n, num, ci, ya, yb))
    for b in sorted(bl, key=lambda t: t[0]):
        w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
        info = ''
        if w >= 38 and h <= 20 and ink <= 1100:
            info = 'DASH'
        elif h > 66 or w <= 3:
            info = 'TALL'
        elif h >= 16 and ink >= 80:
            g = digit_read.grid(px, b)
            ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                         for d, gs in lib.items()), reverse=True)[:3]
            info = ' '.join('%s@%.2f' % (d, s) for s, d in ds)
        else:
            info = '.'
        print('   x%d-%d y%d-%d w%d h%d n%d  %s'
              % (b[0], b[1], b[2], b[3], w, h, ink, info))
