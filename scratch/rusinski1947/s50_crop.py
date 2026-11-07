# -*- coding: utf-8 -*-
"""S50 crop: print pp. 85 + 86 side by side (full pages), plus zoomed
strips of p. 85's bottom and p. 86's top (the leaf junction)."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC
from PIL import Image, ImageOps

OUT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\spot_crops')
ims = {}
for n in ('0100', '0101'):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    ims[n] = im

# full pages side by side
sc = 1350.0 / 3999
fulls = [ims[n].resize((1350, int(5936 * sc)), Image.LANCZOS)
         for n in ('0100', '0101')]
W = 1350 * 2 + 30
H = fulls[0].size[1] + 40
top = Image.new('L', (W, H), 255)
top.paste(fulls[0], (0, 40))
top.paste(fulls[1], (1380, 40))

# zoomed strips: p. 85 bottom quarter, p. 86 top quarter
strips = []
for n, ya, yb in (('0100', 4450, 5936), ('0101', 0, 1500)):
    c = ims[n].crop((250, ya, 3999 - 250, yb))
    s = 2300.0 / c.size[0]
    c = c.resize((2300, int(c.size[1] * s)), Image.LANCZOS)
    strips.append(c)
W2 = 2300
H2 = sum(s.size[1] + 20 for s in strips) + 10
bot = Image.new('L', (W2, H2), 255)
yy = 0
for s in strips:
    bot.paste(s, (0, yy))
    yy += s.size[1] + 20

# stack: full pages first, then the strips
FH = top.size[1] + bot.size[1] + 20
panel = Image.new('L', (max(W, W2), FH), 255)
panel.paste(top, (0, 0))
panel.paste(bot, (0, top.size[1] + 20))
panel.save(os.path.join(OUT, 'S50_p85_p86.png'))
print('saved', panel.size)
