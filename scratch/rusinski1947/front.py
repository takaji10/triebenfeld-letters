# -*- coding: utf-8 -*-
"""Front matter of tom5 composed from the page passes and the strips.

The contents pages (0008-0009) read poorly at page level (the leader dots
and the two-column-number rows confuse psm 3); they get their own strip
reads. The title page (0006), the printer's imprint (0007) and the Wykaz
skrótów (0010-0015) read well at page level.
"""
import sys, os, json
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OUT = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TMP = OUT


def strip(im, y0, y1, scale=2):
    W, H = im.size
    a, b = max(0, y0), min(H, y1)
    c = im.crop((0, a, W, b))
    c = c.resize((W * scale, (b - a) * scale), Image.LANCZOS)
    p = os.path.join(TMP, 'front_tmp.png')
    c.save(p)
    t1 = read(p, lang='pol', psm=6).strip()
    t2 = read(p, lang='pol-std', psm=6).strip()
    return t1, t2


def contents():
    im = Image.open(os.path.join(SRC, 'tom5_0008.tif')).convert('L')
    W, H = im.size
    bands = [(0, 0.18), (0.17, 0.40), (0.38, 0.62), (0.60, 0.82), (0.80, 1.0)]
    for (a, b) in bands:
        t1, t2 = strip(im, int(H * a), int(H * b))
        print('--- pol ---')
        print(t1[:600])
        print('--- std ---')
        print(t2[:300])
        print()


if __name__ == '__main__':
    contents()
