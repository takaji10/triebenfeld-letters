# -*- coding: utf-8 -*-
"""Crops for the six degraded-line zones (S23): 1-2 lost body lines
each, sentences break; the scan gives the text up at every setting."""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OUT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\spot_crops')

ZONES = [
    ('S23a_0064_testamenty.png', '0064', 2240, 2430),
    ('S23b_0114_do200.png',      '0114', 3560, 3780),
    ('S23c_0116_podwyz.png',     '0116', 4060, 4280),
    ('S23d_0123_przywileje.png', '0123', 3260, 3470),
    ('S23e_0124_row.png',        '0124', 4160, 4400),
    ('S23f_0132_wzglednie.png',  '0132', 2600, 2860),
]
for name, n, a, b in ZONES:
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read()))
    im.load()
    W, H = im.size
    b = min(H, b)
    c = im.crop((0, a, W, b))
    c = c.resize((int(W * 0.8), int((b - a) * 0.8)), Image.LANCZOS)
    c.save(os.path.join(OUT, name))
    print(name, c.size)
