# -*- coding: utf-8 -*-
"""Rule-enhanced zone renders for the junk pass: Lp column + chosen
figure columns, horizontal rules darkened, so each figure group can be
assigned to its print row by eye.

usage: python junk_eyes.py <sheet> <y0> <y1> <tag> [coli,colhi]
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
from PIL import Image

n = sys.argv[1]
ya, yb = int(sys.argv[2]), int(sys.argv[3])
tag = sys.argv[4]
coli = int(sys.argv[5]) if len(sys.argv) > 5 else 0
chi = int(sys.argv[6]) if len(sys.argv) > 6 else 11

with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
rules = RULES[n]
x0, x1 = rules[coli] + 2, rules[chi] - 2
c = im.crop((x0, ya, x1, yb))
sc = min(1420.0 / c.size[0], 1350.0 / c.size[1], 3.2)
c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
c = c.convert('L')
# darken: stretch contrast so rules and ink pop
lo, hi = c.getextrema()
if hi > lo:
    c = c.point(lambda v: 0 if v < lo + (hi - lo) * 0.45 else 255)
c.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\junk_%s.png' % tag)
print('saved junk_%s.png' % tag, c.size, 'x%d-%d y%d-%d sc%.2f'
      % (x0, x1, ya, yb, sc))
