# -*- coding: utf-8 -*-
"""Band re-reads for the doubtful words of tom5 (Rusinski 1947).

From the per-page JSONs, group the candidate doubtful words (the two passes'
disagreements and the mid-confidence words) into lines by their boxes, crop
each line as a full-width band with vertical padding, upscale 2.5x, and
re-read it with both models at psm 7 (a single text line). The band passes
are the third and fourth witnesses; where they agree with each other and
against the page passes, their reading wins.

Landscape annex sheets (0139-0159) are cropped from the image rotated -90
degrees, in the rotated frame's coordinates: the JSON words of those pages
were read in portrait and are useless for cropping, so for them the bands
are cut from a whole-page rotated re-read instead (see table_rebuild.py).

Writes bands/<scan>_<top>.png and bands.csv (scan, top, band text of both
passes, the candidate words found on the line).
"""
import sys, os, json, csv, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
BANDS = os.path.join(OCR, 'bands')
os.makedirs(BANDS, exist_ok=True)
THRESH = 75.0
LANDSCAPE = {f'{i:04d}' for i in range(139, 160)}


def fold(w):
    return w.lower().strip('.,;:!?«»"\'()')


def candidates(page):
    """The candidate doubtful words of one page's JSON, as (conf, word)."""
    out = []
    cpol = {}
    for w in page['pol'].split():
        f = fold(w)
        if f:
            cpol[f] = cpol.get(f, 0) + 1
    cstd = {}
    for w in page['std'].split():
        f = fold(w)
        if f:
            cstd[f] = cstd.get(f, 0) + 1
    for x in page['words']:
        w = x[5].strip()
        if not w:
            continue
        f = fold(w)
        # punctuation-only tokens and ditto marks are noise in every pass;
        # drop them here (the table rebuild handles the dittos)
        if len(f) < 2 or not re.search(r'\w', f, re.UNICODE):
            continue
        conf = x[4]
        midconf = 0.0 < conf < THRESH
        disagreed = len(f) > 3 and cpol.get(f, 0) > cstd.get(f, 0)
        if midconf or disagreed:
            out.append((x[0], x[1], x[2], x[3], conf, w))
    return out


def main():
    files = sorted(f for f in os.listdir(OCR) if f.endswith('.json'))
    rows = []
    for fn in files:
        n = fn[:4]
        if n in LANDSCAPE:
            continue
        with open(os.path.join(OCR, fn), encoding='utf-8') as fh:
            page = json.load(fh)
        cands = candidates(page)
        if not cands:
            continue
        # group into lines by top
        cands.sort(key=lambda c: c[1])
        lines = []
        for c in cands:
            for ln in lines:
                if abs(ln[0] - c[1]) < 60:
                    ln[1].append(c)
                    break
            else:
                lines.append([c[1], [c]])
        im = Image.open(os.path.join(SRC, f'tom5_{n}.tif'))
        W, H = im.size
        for top, group in lines:
            bot = max(c[1] + c[3] for c in group)
            a, b = max(0, top - 25), min(H, bot + 25)
            band = im.crop((0, a, W, b))
            band = band.resize((int(W * 2.5), int((b - a) * 2.5)),
                               Image.LANCZOS).convert('L')
            p = os.path.join(BANDS, f'{n}_{a}.png')
            band.save(p)
            try:
                t1 = read(p, lang='pol', psm=7).strip()
                t2 = read(p, lang='pol-std', psm=7).strip()
            except Exception as e:
                t1 = t2 = 'ERR ' + str(e)[:60]
            rows.append([n, a, t1, t2,
                         ' '.join(c[5] for c in group)])
            print(n, a, '|', t1[:80], '||', t2[:80])
    with open(os.path.join(OCR, 'bands.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        wr = csv.writer(fh)
        wr.writerow(['scan', 'top', 'band_pol', 'band_std', 'candidates'])
        wr.writerows(rows)
    print('bands:', len(rows))


if __name__ == '__main__':
    main()
