# -*- coding: utf-8 -*-
"""Read-variant test for the wide strips: which scale/psm keeps the
note paragraphs separated on the problematic pages."""
import sys, os, json, io, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

n = sys.argv[1]
j = json.load(open(os.path.join(OCR, 'widestrips', n + '.json'),
                  encoding='utf-8'))
y0 = j['y0']
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    data = fh.read()
im = Image.open(io.BytesIO(data)).convert('L')
im.load()
W, H = im.size
c0 = im.crop((0, y0, W, H))
for scale in (2, 3):
    for psm in (4, 6):
        c = c0.resize((W * scale, (H - y0) * scale), Image.LANCZOS)
        sp = os.path.join(OCR, 'widestrips', 'tmp.png')
        c.save(sp)
        t = read(sp, lang='pol', psm=psm).strip()
        paras = [p for p in re.split(r'\n\s*\n', t) if p.strip()]
        print(f'scale={scale} psm={psm}: paras={len(paras)}')
        for p in paras[:6]:
            print('   |', p[:70].replace('\n', ' / '))
