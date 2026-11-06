# -*- coding: utf-8 -*-
"""Per-row high-zoom renders of the figure columns (c8..c11) for
verification: one strip per row, stacked 5 per page, Lp anchor marked.

usage: python row_zoom.py <sheet> <row,row,...> [yext]
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
n = sys.argv[1]
rows = [int(x) for x in sys.argv[2].split(',')]
yext = int(sys.argv[3]) if len(sys.argv) > 3 else 26

with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
rules = RULES[n]
panels = []
for num in rows:
    y0, y1 = at[n]['rows'][str(num)]['y']
    # Lp anchor for a guide line
    bl = digit_read.blobs(px, rules[0] + 4, rules[1] - 4,
                          y0 - 20, y1 + yext + 20, minpx=150)
    anch = [(b[2] + b[3]) // 2 for b in bl if 25 <= b[3] - b[2] <= 75]
    c = im.crop((rules[8] + 2, y0 - 16, rules[11] - 2, y1 + yext))
    sc = min(1420.0 / c.size[0], 620.0 / c.size[1], 5.5)
    c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    for a in anch:
        yy = int((a - (y0 - 16)) * sc)
        d.line([(0, yy), (c.size[0], yy)], fill=140, width=2)
    panels.append(('r%d' % num, c))
per = 5
for si in range(0, len(panels), per):
    chunk = panels[si:si + per]
    W = max(p.size[0] for _, p in chunk) + 150
    H = sum(p.size[1] + 12 for _, p in chunk) + 10
    out = Image.new('L', (W, H), 255)
    d = ImageDraw.Draw(out)
    yy = 5
    for tag, p in chunk:
        out.paste(p, (145, yy))
        d.text((5, yy + p.size[1] // 2), tag, fill=0)
        yy += p.size[1] + 12
    fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\rz_%s_%d.png' \
        % (n, si // per)
    out.save(fn)
    print(fn, out.size, [t for t, _ in chunk])
