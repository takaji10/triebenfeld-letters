# -*- coding: utf-8 -*-
"""Re-crops for S04/S07/S09/S14: tight, 2x-zoomed, numbers legible."""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OUT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\spot_crops')

CROPS = [
    # p. 26: '514 dymów' line + the '6,05 ... 3.122' line
    ('S04_p26_514_dymow.png', '0041', 600, 3400, 3560, 2.0),
    # p. 43 note 5: 'W r. 1643 olędrom Marianowa przedłużono dzierżawę'
    ('S07_p43fn_r1643.png', '0058', 600, 4380, 4540, 2.0),
    # p. 16 note 1: the 'Tp. 89, 90 — Wymysłowo, 1889/1890' sigla lines
    ('S09_p16_wysylowo.png', '0031', 600, 3420, 3700, 2.0),
    # p. 68: the inline table (pręt length -> włóka area)
    ('S14_p68_wloka_table.png', '0083', 500, 1100, 1500, 2.0),
]
for name, n, x0, y0, y1, sc in CROPS:
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read()))
    im.load()
    c = im.crop((x0, y0, im.size[0] - x0, y1))
    c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
    c.save(os.path.join(OUT, name))
    print(name, c.size)
