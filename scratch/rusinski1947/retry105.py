# -*- coding: utf-8 -*-
"""Binarized retry of 0105's degraded last body line (~y3280-3400)."""
import sys, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0105.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
c = im.crop((300, 3255, 3660, 3400))
# binarize at several thresholds, pick by ink amount
for thr in (140, 160, 180, 200):
    bw = c.point(lambda v, t=thr: 255 if v > t else 0)
    bw = bw.resize((bw.size[0] * 3, bw.size[1] * 3), Image.LANCZOS)
    bw.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\priv2.png')
    try:
        t = read(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\priv2.png',
                 lang='pol', psm=6).strip()[:160]
    except Exception as e:
        t = 'ERR ' + str(e)[:40]
    print(thr, ':', t)
