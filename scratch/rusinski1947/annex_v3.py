# -*- coding: utf-8 -*-
"""Annex-table extraction for Aneks I of tom5, v3: ruling-line strips.

Lessons of v1/v2 (2026-11-05):
  - no annex sheet's full-page psm 3 read is trustworthy for row order
    (Tesseract blocks the table by its columns or mangles the grid);
  - plain above-threshold projection banding merges everything on the
    ruled sheets (the horizontal ruling lines keep the projection above
    any text-level threshold).

v3: in each sheet's true orientation (orient.json, from the four-way
probe), the row projection's PEAKS are the ruling lines; rows are the
intervals between consecutive rulings; every interval is strip-read at 2x
with psm 6 (both models). A leading integer starts a row; non-integer
lines wrap into it; '|' cell marks split the cells.

Output: annex_rows.json (per scan: orient, rows with num/cells/raw),
annex_strips/<n>.json (the strip reads kept for the record).
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image
import numpy as np

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ROT = os.path.join(OCR, 'rot')
STrips = os.path.join(OCR, 'annex_strips')
os.makedirs(STrips, exist_ok=True)
ANNEX = [f'{i:04d}' for i in range(139, 160)]
ORIENTS = {'d0': 0, 'r90': 90, 'r180': 180, 'r270': 270}


def image_for(n, orient):
    rot = ORIENTS[orient]
    if rot == -90:
        p = os.path.join(ROT, n + '.png')
        if not os.path.isfile(p):
            im = Image.open(os.path.join(SRC, f'tom5_{n}.tif'))
            im.rotate(-90, expand=True).convert('L').save(p)
        return Image.open(p)
    im = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
    if rot:
        im = im.rotate(rot, expand=True)
    return im


def rulings(im):
    """The horizontal ruling lines as y positions: peaks of the row
    projection above a high threshold, merged."""
    a = np.asarray(im)
    dark = (a < 128)
    rp = dark.sum(axis=1).astype(float)
    W = a.shape[1]
    # a ruling crosses most of the width
    thr = W * 0.45
    peaks = [y for y in range(len(rp)) if rp[y] > thr]
    merged = []
    for y in peaks:
        if merged and y - merged[-1][-1] <= 8:
            merged[-1].append(y)
        else:
            merged.append([y])
    return [int(np.mean(g)) for g in merged]


def strip(im, y0, y1, scale=2):
    W, H = im.size
    a, b = max(0, y0 - 10), min(H, y1 + 10)
    c = im.crop((0, a, W, b))
    c = c.resize((W * scale, (b - a) * scale), Image.LANCZOS)
    p = os.path.join(STrips, 'tmp.png')
    c.save(p)
    t1 = read(p, lang='pol', psm=6).strip()
    t2 = read(p, lang='pol-std', psm=6).strip()
    return t1, t2


def parse_rows(strip_recs):
    """Rows from the strip texts: leading integer = new row."""
    rows = []
    cur = None
    for r in strip_recs:
        for raw in (r['pol'], r['std']):
            pass
        text = r['pol']
        for l in text.split('\n'):
            l = l.strip().strip('|').strip()
            if not l:
                continue
            m = re.match(r'^(\d{1,3})\s*[\|;:,]?\s*(.*)$', l)
            if m and (cur is None or int(m.group(1)) == cur['num'] + 1
                      or (cur is not None and int(m.group(1)) == cur['num']
                          and not cur['cells'])):
                if cur is not None:
                    rows.append(cur)
                cur = {'num': int(m.group(1)), 'lines': [m.group(2)]}
            elif cur is not None:
                cur['lines'].append(l)
            else:
                rows.append({'num': None, 'lines': [l]})
    if cur is not None:
        rows.append(cur)
    for r in rows:
        joined = ' '.join(r['lines'])
        cells = [c.strip(' |') for c in joined.split('|')]
        r['cells'] = [c for c in cells if c]
        r['raw'] = joined
        del r['lines']
    return rows


def main():
    orient = json.load(open(os.path.join(OCR, 'orient.json'),
                            encoding='utf-8'))
    out = {}
    for n in ANNEX:
        o = orient[n]['orient']
        im = image_for(n, o)
        W, H = im.size
        ys = rulings(im)
        # intervals: above the first ruling (head), between rulings, below
        cuts = [0] + ys + [H]
        recs = []
        for i in range(len(cuts) - 1):
            y0, y1 = cuts[i], cuts[i + 1]
            if y1 - y0 < 40:
                continue
            if y1 - y0 > 2200:
                # an unruled stretch (head or foot): read it whole
                pass
            t1, t2 = strip(im, y0, y1)
            recs.append({'y0': int(y0), 'y1': int(y1), 'pol': t1,
                         'std': t2})
            print(n, o, y0, '|', t1.replace('\n', ' ')[:95])
        rows = parse_rows(recs)
        nums = [r['num'] for r in rows if r['num'] is not None]
        out[n] = {'orient': o, 'rows': rows, 'strips': len(recs)}
        print(n, 'rows:', len([r for r in rows if r['num'] is not None]),
              'nums:', nums[:6], '...', nums[-3:])
        with open(os.path.join(STrips, n + '.json'), 'w', encoding='utf-8',
                  newline='\n') as fh:
            json.dump(recs, fh, ensure_ascii=False)
    with open(os.path.join(OCR, 'annex_rows.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
