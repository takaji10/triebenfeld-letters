# -*- coding: utf-8 -*-
"""Strip-band reads of the weak annex sheets of tom5.

The weak sheets (their full-page reads come out block-ordered or tilted:
0144, 0147, 0150, 0152, 0154, 0158, 0159, plus 0139's first row) are read
as horizontal strips: the correct-orientation image (direct TIFF for the
odd scans, the rotate(-90) PNG for the even ones) is cut into row bands
found by the dark-pixel row projection, and every band is read with both
models at psm 6 (a uniform block), 2x upscaled.

Output: strips/<n>.json: [{'y0', 'y1', 'pol', 'std'}]. The row parser of
annex_rows.py then works from these texts for the weak sheets.
"""
import sys, os, json
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image
import numpy as np

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
STrips = os.path.join(OCR, 'strips')
os.makedirs(STrips, exist_ok=True)
EVEN = {f'{i:04d}' for i in range(140, 160, 2)}
WEAK = ['0139', '0144', '0147', '0150', '0152', '0154', '0158', '0159']


def image_for(n):
    if n in EVEN:
        p = os.path.join(OCR, 'rot', n + '.png')
        if not os.path.isfile(p):
            im = Image.open(os.path.join(SRC, f'tom5_{n}.tif'))
            im.rotate(-90, expand=True).convert('L').save(p)
        return Image.open(p)
    return Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')


def row_bands(im):
    a = np.asarray(im)
    dark = a < 128
    rp = dark.sum(axis=1)
    thr = max(20, int(rp.mean() * 0.25))
    on = rp > thr
    bands = []
    y0 = None
    for y, v in enumerate(on):
        if v and y0 is None:
            y0 = y
        elif not v and y0 is not None:
            bands.append((y0, y))
            y0 = None
    if y0 is not None:
        bands.append((y0, len(on)))
    # merge bands separated by less than 25 px
    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] < 25:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b))
    # drop slivers
    return [b for b in merged if b[1] - b[0] > 30]


def main():
    for n in WEAK:
        im = image_for(n)
        bands = row_bands(im)
        W, H = im.size
        recs = []
        for (y0, y1) in bands:
            a, b = max(0, y0 - 12), min(H, y1 + 12)
            c = im.crop((0, a, W, b))
            c = c.resize((W * 2, (b - a) * 2), Image.LANCZOS)
            p = os.path.join(STrips, 'tmp.png')
            c.save(p)
            try:
                t1 = read(p, lang='pol', psm=6).strip()
                t2 = read(p, lang='pol-std', psm=6).strip()
            except Exception as e:
                t1 = t2 = 'ERR ' + str(e)[:60]
            recs.append({'y0': a, 'y1': b, 'pol': t1, 'std': t2})
            print(n, a, '|', t1.replace('\n', ' ')[:100])
        with open(os.path.join(STrips, n + '.json'), 'w', encoding='utf-8',
                  newline='\n') as fh:
            json.dump(recs, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
