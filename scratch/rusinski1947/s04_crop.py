# -*- coding: utf-8 -*-
"""S04's crop done so it cannot fail: the three relevant lines cropped
tight, zoomed 3x, stacked vertically with white gaps - every number
huge and impossible to miss."""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image, ImageDraw

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OUT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\spot_crops')

with open(os.path.join(SRC, 'tom5_0041.tif'), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read()))
im.load()
W, H = im.size
frags = []
for y0, y1 in ((3270, 3340), (3380, 3450), (3480, 3550)):
    c = im.crop((900, y0, 3200, y1))
    c = c.resize((int(c.size[0] * 3), int(c.size[1] * 3)), Image.LANCZOS)
    frags.append(c)
    print('frag', y0, y1, c.size)
w = max(f.size[0] for f in frags)
gap = 60
h = sum(f.size[1] for f in frags) + gap * (len(frags) + 1)
canvas = Image.new('RGB', (w, h), 'white')
d = ImageDraw.Draw(canvas)
y = gap
for f in frags:
    canvas.paste(f, (0, y))
    d.line([(0, y - gap // 2), (w, y - gap // 2)], fill=(200, 60, 60), width=4)
    y += f.size[1] + gap
canvas.save(os.path.join(OUT, 'S04_p26_514_dymow.png'))
print('S04 crop:', canvas.size)
