# -*- coding: utf-8 -*-
"""Targeted band reads for layout adjudication: read y-band(s) of one
scan at 3x psm 4 and print, so the print's own structure decides."""
import sys, os, json, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\band_tmp.png'

n = sys.argv[1]
bands = [(int(a), int(b)) for a, b in
         (x.split(':') for x in sys.argv[2].split(','))]
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    data = fh.read()
im = Image.open(io.BytesIO(data)).convert('L')
im.load()
W, H = im.size
for (a, b) in bands:
    c = im.crop((0, a, W, min(H, b)))
    c = c.resize((W * 3, (min(H, b) - a) * 3), Image.LANCZOS)
    c.save(TMP)
    t = read(TMP, lang='pol', psm=4).strip()
    print(f'===== {n} band {a}-{b} =====')
    print(t)
    print()
