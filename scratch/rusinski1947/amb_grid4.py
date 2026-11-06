# -*- coding: utf-8 -*-
"""Disputed-digit grids (0145 r88 middle, r93 third) + 0140 r17
c9/c10 boundary scan and wide render data."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()
ims = {}
for n in ('0140', '0145'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = (im, im.load())


def show(n, xa, xb, ya, yb, tag):
    px = ims[n][1]
    g = digit_read.grid(px, (xa, xb, ya, yb, 0))
    print('=== %s' % tag)
    for row in g:
        print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                              for v in row))


# r88 c10 middle digit (draft 159, matcher 3@0.94)
show('0145', 5163, 5200, 1497, 1555, 'r88 mid (159 vs 139?)')
# r93 c10 third digit (draft 119, matcher 5@0.95)
show('0145', 5204, 5241, 2485, 2543, 'r93 3rd (119 vs 115?)')

# 0140 r17: scan the c9/c10 boundary and full c9 with low thresholds
im, px = ims['0140']
rules = RULES['0140']
print('0140 rules:', rules)
bl = digit_read.blobs(px, rules[9] - 40, rules[10] + 40, 890, 980, minpx=15)
print('r17 boundary zone x%d-%d y890-980:' % (rules[9] - 40, rules[10] + 40))
for b in sorted(bl, key=lambda t: t[0]):
    w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
    info = ''
    if 16 <= h <= 62 and ink >= 80:
        g = digit_read.grid(px, b)
        ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                     for d, gs in lib.items()), reverse=True)[:3]
        info = ' '.join('%s@%.2f' % (d, s) for s, d in ds)
    elif w >= 38 and h <= 20:
        info = 'DASH'
    print('   x%d-%d y%d-%d w%d h%d n%d  %s'
          % (b[0], b[1], b[2], b[3], w, h, ink, info))
