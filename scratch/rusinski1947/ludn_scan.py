# -*- coding: utf-8 -*-
"""Precise scans of the a-ludn Delta-57 suspect rows."""
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


JOBS = [
    ('0140', 17), ('0142', 53), ('0142', 54), ('0142', 55),
    ('0144', 75), ('0144', 76), ('0144', 83),
    ('0145', 88), ('0145', 93), ('0146', 99),
]
for n, num in JOBS:
    im, px = get(n)
    rules = RULES[n]
    y0, y1 = at[n]['rows'][str(num)]['y']
    bl = digit_read.blobs(px, rules[0] + 4, rules[1] - 4,
                          y0 - 60, y1 + 60, minpx=100)
    anch = [(b[2], b[3]) for b in bl if 25 <= b[3] - b[2] <= 75]
    print('=== %s r%d band %s Lp%s' % (n, num, (y0, y1), anch))
    for ci in (8, 9, 10):
        x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
        bl = digit_read.blobs(px, x0, x1, y0 - 16, y1 + 30, minpx=25)
        parts = []
        for b in sorted(bl, key=lambda t: (t[2], t[0])):
            w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
            if w >= 38 and h <= 20 and ink <= 1100:
                parts.append('DASH(y%d)' % b[2])
            elif h > 66 or w <= 3:
                parts.append('TALL(y%d)' % b[2])
            elif h >= 16 and ink >= 80:
                g = digit_read.grid(px, b)
                ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)[:2]
                parts.append('%s@%.2f(x%d w%dh%d y%d)'
                             % (ds[0][1], ds[0][0], b[0], w, h, b[2]))
            else:
                parts.append('.(w%dh%d y%d)' % (w, h, b[2]))
        print('  c%d: %s' % (ci, ' '.join(parts) if parts else 'EMPTY'))
