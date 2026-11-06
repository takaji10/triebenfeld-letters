# -*- coding: utf-8 -*-
"""Cross-correlate suspect grids against strip-verified reference digits."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC
import digit_read
from PIL import Image

ims = {}
for n in ('0140', '0142', '0151', '0153', '0154', '0156', '0158'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = im.load()

REF = {
    '5@0151r73': ('0151', 4690, 4730, 2305, 2364),
    '9@0153r93': ('0153', 4690, 4730, 1318, 1374),
    '8@0142r61': ('0142', 4700, 4742, 3014, 3072),
    '6@0140r14': ('0140', 4645, 4681, 567, 627),
    '0@0158r7': ('0158', 4686, 4727, 1623, 1681),
}
SUS = {
    '0151r78g1': ('0151', 4688, 4727, 3152, 3209),
    '0154r105': ('0154', 4699, 4738, 367, 421),
    '0154r112': ('0154', 4696, 4735, 1788, 1846),
    '0156r134': ('0156', 4724, 4767, 587, 646),
    '0156r137': ('0156', 4714, 4754, 1054, 1102),
    '0158r3': ('0158', 4696, 4735, 859, 917),
    '0158r4g2': ('0158', 4692, 4731, 1053, 1111),
    '0158r8': ('0158', 4689, 4729, 1868, 1926),
}

def grid_of(n, xa, xb, ya, yb):
    return digit_read.grid(ims[n], (xa, xb, ya, yb, 0))

refs = {k: grid_of(*v) for k, v in REF.items()}
print('%-12s %s' % ('suspect', '  '.join('%-11s' % k for k in refs)))
for sk, sv in SUS.items():
    g = grid_of(*sv)
    scores = ['%d@%.2f' % (int(k[0]), digit_read.corr(g, rg))
              for k, rg in refs.items()]
    print('%-12s %s' % (sk, '  '.join('%-11s' % s for s in scores)))
