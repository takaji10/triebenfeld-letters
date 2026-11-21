# -*- coding: utf-8 -*-
"""Zoom read: one band at 6x, psm 6 and 7, to resolve tiny type."""
import sys, os, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\zoom_tmp.png'
n = sys.argv[1]
a, b = int(sys.argv[2]), int(sys.argv[3])
scale = int(sys.argv[4]) if len(sys.argv) > 4 else 6
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    data = fh.read()
im = Image.open(io.BytesIO(data)).convert('L')
im.load()
W, H = im.size
c = im.crop((0, a, W, min(H, b)))
c = c.resize((W * scale, (min(H, b) - a) * scale), Image.LANCZOS)
c.save(TMP)
for psm in (6, 4):
    t = read(TMP, lang='pol', psm=psm).strip()
    print(f'--- {n} {a}-{b} @{scale}x psm {psm}:')
    print(t[:600])
