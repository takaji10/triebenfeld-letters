# -*- coding: utf-8 -*-
"""r88 middle digit: top-5 matcher + corr vs verified full-size 3."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()
ims = {}
for n in ('0143', '0145'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = (im, im.load())

px = ims['0145'][1]
g88 = digit_read.grid(px, (5163, 5200, 1497, 1555, 0))
ds = sorted(((max(digit_read.corr(g88, rg) for rg in gs), d)
             for d, gs in lib.items()), reverse=True)[:5]
print('r88 mid top-5:', ' '.join('%s@%.2f' % (d, s) for s, d in ds))

# verified full-size 3: 0143 r73 c8 second digit (value 13)
im, px3 = ims['0143']
rules = RULES['0143']
y0, y1 = at['0143']['rows']['73']['y']
bl = digit_read.blobs(px3, rules[8] + 4, rules[9] - 4, y0 - 16, y1 + 30,
                      minpx=25)
print('0143 r73 c8 blobs:')
b3 = None
for b in sorted(bl, key=lambda t: t[0]):
    w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
    print('   x%d-%d y%d-%d w%d h%d n%d' % (b[0], b[1], b[2], b[3], w, h, ink))
    if w >= 25 and h >= 40:
        b3 = b
if b3:
    g3 = digit_read.grid(px3, b3)
    print('corr(r88mid, 3ref) = %.2f' % digit_read.corr(g88, g3))
    print('=== 3-ref grid')
    for row in g3:
        print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                              for v in row))
