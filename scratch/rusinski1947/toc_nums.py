# -*- coding: utf-8 -*-
"""Batch-read the TOC page-number column (0008/0009) and the uncertain
Wykaz sigla. Prints one line per query."""
import sys, os, io, json
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode'
                r'\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\priv2.png'
s = json.load(open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
                   r'\tom5_ocr\structure4.json', encoding='utf-8'))
ims = {}


def im(n):
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            ims[n] = Image.open(io.BytesIO(fh.read())).convert('L')
        ims[n].load()
    return ims[n]


def num(n, top):
    """The page number right of the dotted leader for the TOC line at
    top (the numbers column sits at the sheet's right edge)."""
    i = im(n).crop((3030, top - 4, 3190, top + 70))
    i = i.resize((i.size[0] * 6, i.size[1] * 6), Image.LANCZOS)
    i.save(TMP)
    outs = []
    for psm in (7, 8, 10):
        try:
            t = read(TMP, lang='pol', psm=psm).strip()
            if t and t not in outs:
                outs.append(t)
        except Exception:
            pass
    return ' / '.join(outs)


print('===== 0008 TOC numbers')
for top in (1785, 1886, 1992, 2079, 2164, 2351, 2657, 2763, 3240,
            3339, 3450, 3642, 3995, 4084, 4173, 4550, 4764, 4851,
            4938, 5026):
    line = next((l['text'] for l in s['0008']['lines']
                 if abs(l['top'] - top) <= 4), '?')
    print(top, num('0008', top), '|', line[:60])
print('===== 0009 TOC numbers')
for top in (763, 849, 936, 1046, 1132, 1740, 2177, 2270, 2374, 2743,
            2851, 2935, 3045, 3378, 3489, 3640, 3831, 3936, 4041,
            4142, 4230, 4446, 4652, 4760, 4868, 4976):
    line = next((l['text'] for l in s['0009']['lines']
                 if abs(l['top'] - top) <= 4), '?')
    print(top, num('0009', top), '|', line[:60])
