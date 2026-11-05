# -*- coding: utf-8 -*-
"""Targeted re-reads for the weak annex sheets: upscale 2x, psm 4.

The psm 4 full-page read left gaps on 0144 (rows 74-77 partial), 0152
(rows 59-66), 0155 (rows 119-132), 0159 (rows 10-11 and the closing
lines). At 2x the small type resolves and the row numbers read.
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OUT = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
SHEETS = ['0144', '0150', '0151', '0152', '0155', '0159']


def main():
    for n in SHEETS:
        im = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
        W, H = im.size
        c = im.resize((W * 2, H * 2), Image.LANCZOS)
        p = os.path.join(OUT, 'big_' + n + '.png')
        c.save(p)
        t = read(p, lang='pol', psm=4)
        with open(os.path.join(OUT, 'big_' + n + '.txt'), 'w',
                  encoding='utf-8', newline='\n') as fh:
            fh.write(t)
        nums = [int(m.group(1)) for m in
                re.finditer(r'^\s*\|?\s*(\d{1,3})\s*\|', t, re.M)
                if 1 <= int(m.group(1)) <= 200]
        print(n, 'rows:', len(nums), nums[:8], '...', nums[-3:])


if __name__ == '__main__':
    main()
