# -*- coding: utf-8 -*-
"""Batch print reads (sequential - shared tmp PNG) for the repair
adjudications: 0064 body/note-1 seam, 0031 sigla block, 0114 note 1,
0113 bottom (join witness), the lost-line gaps on 0116/0123/0124."""
import sys, os, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\batch_tmp.png'

JOBS = [
    ('0064', 1900, 2500, 3),
    ('0031', 2600, 3950, 3),
    ('0114', 3350, 4250, 3),
    ('0113', 4800, 5936, 3),
    ('0116', 3900, 4400, 4),
    ('0123', 3050, 3550, 4),
    ('0124', 4000, 4500, 4),
]
for n, a, b, sc in JOBS:
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read()))
    im.load()
    W, H = im.size
    b = min(H, b)
    c = im.crop((0, a, W, b))
    c = c.resize((W * sc, (b - a) * sc), Image.LANCZOS)
    c.save(TMP)
    t = read(TMP, lang='pol', psm=4).strip()
    print('===== %s  %d-%d  @%dx =====' % (n, a, b, sc))
    print(t)
    print()
