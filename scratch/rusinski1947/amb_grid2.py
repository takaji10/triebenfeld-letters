# -*- coding: utf-8 -*-
"""Reference grids: strip-verified 5 (0151 r73) and 9 (0153 r93)
vs the 9@0.9x suspect family."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

ims = {}
for n in ('0151', '0153', '0156'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = im.load()

px = ims['0151']
# 0151 r73: 9@0.95(w31h51 y2309-2360) per junkdec
g = digit_read.grid(px, (4690, 4730, 2305, 2364, 0))
print('=== REF 0151 r73 (strip=5, matcher 9@0.95)')
for row in g:
    print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                          for v in row))
px = ims['0153']
# 0153 r93: 9@0.82(w31h48 y1322-1370) strip=9
g = digit_read.grid(px, (4690, 4730, 1318, 1374, 0))
print('=== REF 0153 r93 (strip=9, matcher 9@0.82)')
for row in g:
    print('   ' + ''.join('#' if v > 0.35 else ('+' if v > 0.12 else '.')
                          for v in row))
