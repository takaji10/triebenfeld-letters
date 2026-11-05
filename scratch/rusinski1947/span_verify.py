# -*- coding: utf-8 -*-
"""Verify spanning-note joins: read the PREV page's bottom band at 3x
(psm 4) - the last note's true ending shows there."""
import sys, os, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\band_tmp.png'

PAGES = sys.argv[1:] or ['0016', '0034', '0047', '0048', '0053', '0080',
                         '0098', '0112', '0118', '0131']
cache = {}
for n in PAGES:
    if n not in cache:
        with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
            cache[n] = Image.open(io.BytesIO(fh.read()))
        cache[n].load()
    im = cache[n]
    W, H = im.size
    c = im.crop((0, H - 950, W, H))
    c = c.resize((W * 3, 950 * 3), Image.LANCZOS)
    c.save(TMP)
    t = read(TMP, lang='pol', psm=4).strip()
    print('===== %s bottom (last 950px) =====' % n)
    print(t[-800:])
    print()
