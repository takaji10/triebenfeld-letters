# -*- coding: utf-8 -*-
"""Read the note-number column (left margin of the note block) at 6x,
psm 6 - the digits sequence decides the note count."""
import sys, os, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\col_tmp.png'

n = sys.argv[1]
x0, x1 = int(sys.argv[2]), int(sys.argv[3])
a, b = int(sys.argv[4]), int(sys.argv[5])
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    data = fh.read()
im = Image.open(io.BytesIO(data)).convert('L')
im.load()
c = im.crop((x0, a, x1, b))
c = c.resize((c.size[0] * 6, c.size[1] * 6), Image.LANCZOS)
c.save(TMP)
for psm in (6, 4):
    t = read(TMP, lang='pol', psm=psm).strip()
    print(f'--- psm {psm}:')
    print(t)
