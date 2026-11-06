# -*- coding: utf-8 -*-
"""Locate the print's '*' marker (small ~8x8px blob) in the starred
rows' cells: scan c4, c8, c9, c10 for a small blob next to the digit.
Report -> console; the fixes then add ' *' to the right cell."""
import sys, os, json, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annex_cells import detect, fit
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

ROWS = [
    ('0139', 9), ('0140', 21), ('0140', 26), ('0141', 36),
    ('0142', 48), ('0142', 54), ('0144', 77), ('0144', 78),
    ('0146', 102), ('0147', 1), ('0147', 12),
    ('0148', 15), ('0148', 17), ('0148', 22), ('0148', 24),
    ('0149', 44), ('0149', 47), ('0149', 48),
    ('0150', 62),
    ('0151', 74), ('0151', 75), ('0151', 77), ('0151', 78),
    ('0151', 79),
    ('0152', 82), ('0152', 83), ('0152', 84), ('0152', 85),
    ('0152', 87), ('0152', 91),
    ('0153', 103),
    ('0154', 106), ('0154', 107), ('0154', 110), ('0154', 111),
    ('0154', 113),
    ('0155', 119), ('0155', 123), ('0155', 127),
    ('0158', 1),
    ('0159', 1), ('0159', 3),
]


def blobs(px, x0, x1, y0, y1, minpx=12):
    seen = set()
    out = []
    for x in range(x0, x1):
        for y in range(y0, y1):
            if px[x, y] < 175 and (x, y) not in seen:
                stack = [(x, y)]
                comp = []
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    comp.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if x0 <= nx < x1 and y0 <= ny < y1 \
                                    and (nx, ny) not in seen \
                                    and px[nx, ny] < 175:
                                seen.add((nx, ny))
                                stack.append((nx, ny))
                if len(comp) > minpx:
                    xs = [p[0] for p in comp]
                    ys = [p[1] for p in comp]
                    out.append((min(xs), max(xs), min(ys), max(ys),
                                len(comp)))
    return sorted(out)


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    cache = {}
    for n, num in ROWS:
        if n not in cache:
            rows = at[n]['rows']
            all_nums = sorted(int(k) for k in rows if k.isdigit())
            y_lo = min(rows[str(k)]['y'][0] for k in all_nums)
            y_hi = max(rows[str(k)]['y'][1] for k in all_nums)
            im, runs = detect(n, y_lo, y_hi)
            got = fit(runs)
            resid, rules = got
            bounds = rules + [rules[-1] + 120]
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            cache[n] = (im.load(), bounds)
        px, bounds = cache[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        hits = []
        for ci in (4, 8, 9, 10):
            x0, x1 = int(bounds[ci]) + 6, int(bounds[ci + 1]) - 6
            bl = blobs(px, x0, x1, y0 + 2, y1 - 2)
            small = [b for b in bl
                     if (b[1] - b[0]) <= 16 and (b[3] - b[2]) <= 16]
            if small:
                hits.append((ci, [(b[0], b[1], b[2], b[3]) for b in small]))
        print(n, 'r%d' % num, 'star-blobs:', hits if hits else 'NONE',
              flush=True)


if __name__ == '__main__':
    main()
