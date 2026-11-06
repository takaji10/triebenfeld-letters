# -*- coding: utf-8 -*-
"""y-coordinate scans for the ambiguous ludn cells + 0/9-ref corr for
0145 r92's second digit."""
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

for n, nums in (('0143', (63, 65, 70)), ('0145', (92, 93))):
    im, px = ims[n]
    rules = RULES[n]
    for num in nums:
        y0, y1 = at[n]['rows'][str(num)]['y']
        bl = digit_read.blobs(px, rules[0] + 4, rules[1] - 4,
                              y0 - 60, y1 + 60, minpx=100)
        anch = [(b[2] + b[3]) // 2 for b in bl if 25 <= b[3] - b[2] <= 75]
        x0, x1 = rules[10] + 4, rules[11] - 4
        bl = digit_read.blobs(px, x0, x1, y0 - 16, y1 + 34, minpx=40)
        print('=== %s r%d band %s Lpmid%s' % (n, num, (y0, y1), anch))
        for b in sorted(bl, key=lambda t: t[0]):
            w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
            info = ''
            if 16 <= h <= 66 and ink >= 80 and w >= 8:
                g = digit_read.grid(px, b)
                ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)[:3]
                info = ' '.join('%s@%.2f' % (d, s) for s, d in ds)
            print('   x%d-%d y%d-%d w%d h%d n%d  %s'
                  % (b[0], b[1], b[2], b[3], w, h, ink, info))

# direct 0/9-ref corr for 0145 r92's digits
im, px = ims['0145']
y0, y1 = at['0145']['rows']['92']['y']
print('r92 band', (y0, y1))
