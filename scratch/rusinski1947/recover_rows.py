# -*- coding: utf-8 -*-
"""Targeted row recovery for the annex rows the psm 4 parse missed.

For every row number a sheet's parse lacks: the psm 3 direct TSV carries
the row numbers as separate tokens with boxes (the number column is the
table's first column in the stored orientation); the token's top gives
the row's y-band (to the next number's top), and that band is strip-read
at 3x with both models at psm 6 - the scale at which the annex strips
read cleanly (annex_v3's finding).

Output: recovery/<scan>_<num>.txt (pol pass) and .std.txt, plus a summary
line per recovered row.
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read, words
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
REC = os.path.join(OCR, 'recovery')
os.makedirs(REC, exist_ok=True)

# the gaps after the psm 4 parse (2026-11-05)
GAPS = {
    '0144': [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86],
    '0150': [59, 60, 61, 62, 63, 64, 65, 66],
    '0151': [],
    '0152': [59, 60, 61, 62, 63, 64, 65, 66],
    '0155': [119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
             130, 131, 132],
    '0159': [10, 11],
}


def anchors(n):
    """The row-number anchors from the psm 3 direct TSV: [(num, top)].
    The number column sits at x about 700-1250 in the stored orientation
    (0144's numbers at x 952-960; '99814' at 772 is the page's own
    artefact). For numbers the TSV lost or misread ('17' for 77), the
    top is interpolated between the neighbours."""
    d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
    cand = []
    for x in d['words']:
        w = x[5].strip().rstrip('.,')
        if w.isdigit() and 1 <= int(w) <= 200 and 650 <= x[0] <= 1250 \
                and x[2] < 200:
            cand.append((int(w), x[1]))
    best = {}
    for num, top in cand:
        if num not in best or top < best[num]:
            best[num] = top
    have = sorted(best.items())
    out = dict(have)
    # interpolate the missing ones between their numbered neighbours
    for i in range(len(have) - 1):
        (a, ya), (b, yb) = have[i], have[i + 1]
        if b - a > 1 and b - a <= 20:
            for num in range(a + 1, b):
                out[num] = ya + (yb - ya) * (num - a) / (b - a)
    return out


def main():
    for n, want in GAPS.items():
        if not want:
            continue
        anc = anchors(n)
        tops = {num: top for num, top in anc.items()}
        have = sorted(tops)
        im = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
        W, H = im.size
        for num in want:
            if num not in tops:
                print(n, num, 'NO ANCHOR')
                continue
            y0 = tops[num]
            nxt = [t for t in have if t > y0]
            y1 = nxt[0] - 5 if nxt else min(H, y0 + 320)
            a, b = max(0, y0 - 15), min(H, y1 + 15)
            a, b = int(a), int(b)
            c = im.crop((0, a, W, b))
            c = c.resize((W * 3, (b - a) * 3), Image.LANCZOS)
            p = os.path.join(REC, 'tmp.png')
            c.save(p)
            t1 = read(p, lang='pol', psm=6).strip()
            t2 = read(p, lang='pol-std', psm=6).strip()
            with open(os.path.join(REC, f'{n}_{num}.txt'), 'w',
                      encoding='utf-8', newline='\n') as fh:
                fh.write(t1 + '\n@@@\n' + t2)
            print(n, num, '|', t1.replace('\n', ' ')[:130])


if __name__ == '__main__':
    main()
