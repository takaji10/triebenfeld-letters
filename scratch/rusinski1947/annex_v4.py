# -*- coding: utf-8 -*-
"""Annex-table extraction v4: geometric cell assignment.

The '|' text splitting proved too noisy for the nine columns. v4 works
from the geometry in the stored orientation (every sheet reads as stored;
orient.json concurs):

  - vertical ruling lines: peaks of the column projection above half the
    table's height -> the columns' x-spans;
  - row bands: the number-column tokens' tops (x about 650-1300 in the
    stored sheets, measured per sheet from the leftmost digit tokens),
    each consecutive pair bounding a row;
  - every TSV word joins the cell its (row band, column span) contains;
  - the header rows (above the first numbered row) are read as their own
    bands so the columns can be named.

Output: annex_cells.json: per scan {cols: [x-spans], rows: {num:
{cells: [text x 9], conf}} } - the number of columns comes from the
rulings; the compose step maps them to the print's nine columns.
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import words
from PIL import Image
import numpy as np

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ANNEX = [f'{i:04d}' for i in range(139, 160)]


def load_words(n):
    d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
    return [(x[0], x[1], x[2], x[3], x[4], x[5].strip())
            for x in d['words'] if x[5].strip()]


def v_rulings(n):
    im = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
    a = np.asarray(im)
    dark = (a < 128)
    cp = dark.sum(axis=0).astype(float)
    H = a.shape[0]
    thr = H * 0.35
    xs = [x for x in range(len(cp)) if cp[x] > thr]
    merged = []
    for x in xs:
        if merged and x - merged[-1][-1] <= 10:
            merged[-1].append(x)
        else:
            merged.append([x])
    return [int(np.mean(g)) for g in merged], im.size


def row_anchors(ws):
    """Number-column tokens: digits at the leftmost digit x-band."""
    digits = [(x0, y0, int(w.rstrip('.,'))) for (x0, y0, w_, h_, c, w)
              in ws if re.fullmatch(r'\d{1,3}[.,]?', w)
              and 1 <= int(w.rstrip('.,').rstrip('.,' )) <= 200]
    if not digits:
        return {}
    # the number column's x: the modal x of the smallest-x digit tokens
    xs = sorted(x0 for x0, _, _ in digits)
    xlo = xs[max(0, len(xs) // 10)]
    xhi = xlo + 700
    best = {}
    for x0, y0, v in digits:
        if xlo <= x0 <= xhi:
            if v not in best or y0 < best[v]:
                best[v] = y0
    return best


def main():
    out = {}
    for n in ANNEX:
        ws = load_words(n)
        rulings, (W, H) = v_rulings(n)
        anchors = row_anchors(ws)
        # spans between rulings; the first span starts at 0
        bounds = [0] + rulings + [W]
        spans = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)
                 if bounds[i + 1] - bounds[i] > 40]
        nums_sorted = sorted(anchors.items(), key=lambda z: z[1])
        rows = {}
        for i, (num, y0) in enumerate(nums_sorted):
            y1 = nums_sorted[i + 1][1] - 4 if i + 1 < len(nums_sorted) \
                else H
            cells = [[] for _ in spans]
            confs = []
            for (x0, y0w, w_, h_, c, word) in ws:
                if not (y0 - 4 <= y0w < y1):
                    continue
                for k, (a, b) in enumerate(spans):
                    if a <= x0 < b:
                        cells[k].append((y0w, x0, word))
                        confs.append(c)
                        break
            rows[num] = {
                'cells': [' '.join(w for _, _, w in sorted(cl))
                          for cl in cells],
                'y': y0, 'conf': round(sum(confs) / len(confs), 1)
                if confs else 0.0}
        out[n] = {'spans': spans, 'rows': rows}
        ok = sum(1 for r in rows.values()
                 if sum(1 for c in r['cells'] if c.strip()) >= 3)
        print(n, 'spans:', len(spans), 'rows:', len(rows), 'rich:', ok)
    with open(os.path.join(OCR, 'annex_cells.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
