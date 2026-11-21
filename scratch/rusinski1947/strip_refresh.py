# -*- coding: utf-8 -*-
"""Refresh wide strips whose y0 sits BELOW the page's true note-block
start. The block start (geometric estimate): the last transition from
a body-type line (h >= 0.9 x BH) to a small-type line (h <= 0.85 x BH)
that stays small to the page bottom (allowing stray tall junk lines).
Pages whose estimate is far above the strip's y0 get the strip
re-read from max(900, est - 400).

Writes refreshed strips in place; prints the refresh list.
"""
import sys, os, json, io, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
from pipeline.ocr import read
from PIL import Image
import structure2 as S

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = S.OCR
OUT = os.path.join(OCR, 'widestrips')


def block_start(lns, BH):
    """The last body->small transition that stays small to the end."""
    cand = None
    for i, l in enumerate(lns):
        if l['h'] <= 0.88 * BH and l['h'] >= 25:
            # check the tail: of the lines after i, at most ~15% tall
            tail = [x for x in lns[i:] if x['h'] > 0.93 * BH]
            if len(tail) <= max(1, int(0.15 * (len(lns) - i))):
                cand = l['top']
    return cand


def main():
    only = sys.argv[1:] or None
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    v1 = json.load(open(os.path.join(OCR, 'structure.json'),
                        encoding='utf-8'))
    refresh = []
    for n in sorted(struct):
        if only and n not in only:
            continue
        if n < '0016' or n > '0137' or n in S.NO_NOTES:
            continue
        sp = os.path.join(OUT, n + '.json')
        if not os.path.isfile(sp):
            refresh.append((n, None, 'no strip'))
            continue
        d = json.load(open(os.path.join(OUT, n + '.json'),
                           encoding='utf-8'))
        y0 = d['y0']
        d2 = json.load(open(os.path.join(OCR, n + '.json'),
                            encoding='utf-8'))
        lns = S.lines_of(d2)
        # BH = the 90th percentile of the TOP THIRD's line heights (the
        # body occupies the page top; on note-heavy pages the upper-half
        # median IS a note line and every ratio inverts)
        top3 = lns[:max(1, len(lns) // 3)]
        hs = sorted(l['h'] for l in top3 if l['h'] >= 30)
        BH = hs[min(len(hs) - 1, int(0.9 * len(hs)))] if hs else 80
        est = block_start(lns, BH)
        if est is not None and est < y0 - 120:
            refresh.append((n, y0, est))
    print('refresh candidates:', len(refresh))
    for n, old, est in refresh:
        new_y0 = max(900, int((est if isinstance(est, int) else 2000)) - 400)
        print(n, 'y0', old, '->', new_y0)
        with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
            data = fh.read()
        im = Image.open(io.BytesIO(data)).convert('L')
        im.load()
        W, H = im.size
        c = im.crop((0, new_y0, W, H))
        c = c.resize((W * 3, (H - new_y0) * 3), Image.LANCZOS)
        tmp = os.path.join(OUT, 'tmp.png')
        c.save(tmp)
        t1 = read(tmp, lang='pol', psm=4).strip()
        t2 = read(tmp, lang='pol-std', psm=4).strip()
        with open(os.path.join(OUT, n + '.json'), 'w', encoding='utf-8',
                  newline='\n') as fh:
            json.dump({'y0': new_y0, 'pol': t1, 'std': t2}, fh,
                      ensure_ascii=False)


if __name__ == '__main__':
    main()
