# -*- coding: utf-8 -*-
"""0140 r17 c10 pair: 7-vs-5 and 2 refs; 0141 r31 date '1746' supplies
a verified full-size 7; 0142 r53's 2@0.97 supplies a verified 2."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()
ims = {}
for n in ('0140', '0141', '0142'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = (im, im.load())


def gridof(n, xa, xb, ya, yb):
    return digit_read.grid(ims[n][1], (xa, xb, ya, yb, 0))


def show(g, tag):
    print('=== %s' % tag)
    for row in g:
        print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                              for v in row))


# r17 c10 pair
g1 = gridof('0140', 5203, 5242, 904, 964)
g2 = gridof('0140', 5240, 5279, 904, 964)
show(g1, 'r17 c10 g1 (x5207)')
show(g2, 'r17 c10 g2 (x5244)')

# verified 7 from 0141 r31's rok 1746 (c4 zone)
im, px = ims['0141']
rules = RULES['0141']
y0, y1 = at['0141']['rows']['31']['y']
bl = digit_read.blobs(px, rules[4] + 4, rules[5] - 4, y0 - 16, y1 + 30,
                      minpx=60)
print('0141 r31 c4 blobs (rok 1746):')
for b in sorted(bl, key=lambda t: t[0]):
    print('   x%d-%d y%d-%d w%d h%d n%d'
          % (b[0], b[1], b[2], b[3], b[1] - b[0], b[3] - b[2], b[4]))
# digit order 1,7,4,6 -> second blob = 7
blobs = [b for b in sorted(bl, key=lambda t: t[0])
         if 20 <= b[3] - b[2] <= 70 and b[1] - b[0] >= 8]
if len(blobs) >= 2:
    g7 = gridof('0141', blobs[1][0] - 2, blobs[1][1] + 2,
                blobs[1][2] - 4, blobs[1][3] + 4)
    show(g7, 'REF 7 (0141 r31 rok 1746, 2nd digit)')
    print('corr(r17g1, 7ref) = %.2f' % digit_read.corr(g1, g7))

# verified 2 from 0142 r53 c8 first digit
im2, px2 = ims['0142']
rules2 = RULES['0142']
y02, y12 = at['0142']['rows']['53']['y']
bl2 = digit_read.blobs(px2, rules2[8] + 4, rules2[9] - 4, y02 - 16,
                       y12 + 30, minpx=60)
blobs2 = [b for b in sorted(bl2, key=lambda t: t[0])
          if 20 <= b[3] - b[2] <= 70 and b[1] - b[0] >= 8]
print('0142 r53 c8 blobs (25):', [(b[0], b[1]) for b in blobs2])
if blobs2:
    gb = gridof('0142', blobs2[0][0] - 2, blobs2[0][1] + 2,
                blobs2[0][2] - 4, blobs2[0][3] + 4)
    print('corr(r17g2, 2ref) = %.2f' % digit_read.corr(g2, gb))
    # also 5-ref corr for g1 (5 = flat top bar, r73)
    g5 = gridof('0151', 4690, 4730, 2305, 2364)
    with open(os.path.join(SRC, 'tom5_0151.tif'), 'rb') as fh:
        im5 = Image.open(io.BytesIO(fh.read())).convert('L')
    im5.load()
    g5 = digit_read.grid(im5.load(), (4690, 4730, 2305, 2364, 0))
    print('corr(r17g1, 5ref) = %.2f' % digit_read.corr(g1, g5))
