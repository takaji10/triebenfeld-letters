# -*- coding: utf-8 -*-
"""ASCII ink grids of the ambiguous glyphs - shape-level reading."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
ims = {}
for n in ('0151', '0154', '0156', '0158'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = im.load()

JOBS = [
    ('0151', 4688, 4727, 3152, 3209, 'r78 g1'),
    ('0151', 4736, 4769, 3153, 3191, 'r78 g2'),
    ('0154', 4699, 4738, 367, 421, 'r105 g1'),
    ('0154', 4696, 4735, 1788, 1846, 'r112 g1'),
    ('0156', 4724, 4767, 587, 646, 'r134 g1'),
    ('0156', 4714, 4754, 1054, 1102, 'r137 g1'),
    ('0156', 4704, 4742, 2523, 2579, 'r144 g1'),
    ('0156', 4752, 4787, 2524, 2561, 'r144 g2'),
    ('0158', 4696, 4735, 859, 917, 'r3 g1'),
    ('0158', 4666, 4687, 1054, 1111, 'r4 g1'),
    ('0158', 4692, 4731, 1053, 1111, 'r4 g2'),
    ('0158', 4689, 4729, 1868, 1926, 'r8 g1'),
]
for n, xa, xb, ya, yb, tag in JOBS:
    px = ims[n]
    g = digit_read.grid(px, (xa, xb, ya, yb, 0))
    print('=== %s  x%d-%d y%d-%d' % (tag, xa, xb, ya, yb))
    for row in g:
        print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                              for v in row))
