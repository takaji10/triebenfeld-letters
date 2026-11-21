# -*- coding: utf-8 -*-
import sys, os, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\priv_tmp.png'
n, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sc = int(sys.argv[4]) if len(sys.argv) > 4 else 6
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
c = im.crop((300, a, 3900, b))
c = c.resize((c.size[0] * sc, c.size[1] * sc), Image.LANCZOS)
c.save(TMP)
for psm in (6, 4):
    try:
        print('psm%d: %s' % (psm, read(TMP, lang='pol', psm=psm)
                             .strip()[:200].replace('\n', ' / ')))
    except Exception as e:
        print('psm%d ERR %s' % (psm, str(e)[:60]))
