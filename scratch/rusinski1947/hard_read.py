# -*- coding: utf-8 -*-
"""Hard-case read: crop, autocontrast + threshold, big scale, several
psm modes - for warp-damaged lines."""
import sys, os, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image, ImageOps, ImageFilter

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\hard_tmp.png'
n, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
scale = int(sys.argv[4]) if len(sys.argv) > 4 else 8
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    data = fh.read()
im = Image.open(io.BytesIO(data)).convert('L')
im.load()
c = im.crop((0, a, im.size[0], min(im.size[1], b)))
c = c.resize((c.size[0] * scale, c.size[1] * scale), Image.LANCZOS)
c = ImageOps.autocontrast(c)
# sharpen + binarize at a few thresholds
for thr in (120, 150, 180):
    bw = c.point(lambda v, t=thr: 255 if v > t else 0)
    bw = bw.filter(ImageFilter.MedianFilter(3))
    bw.save(TMP)
    for psm in (6, 4):
        try:
            t = read(TMP, lang='pol', psm=psm).strip()
        except Exception as e:
            t = 'ERR ' + str(e)[:50]
        print('--- thr=%d psm=%d: %s' % (thr, psm, t[:200].replace('\n', ' / ')))
