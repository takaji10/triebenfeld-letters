# -*- coding: utf-8 -*-
"""More reference grids: verified 9s and 0s."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC
import digit_read
from PIL import Image

ims = {}
for n in ('0145', '0146', '0158'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = im.load()

JOBS = [
    ('0146', 4676, 4711, 906, 964, 'REF 9 @0146r102 (9@1.00)'),
    ('0145', 5155, 5195, 3398, 3456, 'REF 9 @0145r92 ludn=90 first'),
    ('0145', 5200, 5240, 3398, 3456, 'REF 0 @0145r92 ludn=90 second'),
    ('0158', 4686, 4727, 1623, 1681, 'REF 0 @0158r7 (0@0.95)'),
]
for n, xa, xb, ya, yb, tag in JOBS:
    px = ims[n]
    g = digit_read.grid(px, (xa, xb, ya, yb, 0))
    print('=== %s  x%d-%d y%d-%d' % (tag, xa, xb, ya, yb))
    for row in g:
        print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                              for v in row))
