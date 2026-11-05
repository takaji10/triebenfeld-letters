# -*- coding: utf-8 -*-
"""Orientation map for every annex sheet of tom5.

The five-sheets probe (2026-11-05) showed the sheets' orientations vary
individually, not by scan parity. Every sheet is probed in four
orientations (direct, +90, 180, -90): a middle band read at 1.5x, psm 6,
scored by the count of plausible Polish words. The winner is recorded in
orient.json, the input of the row rebuild.
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
PROBE = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr\probe'
os.makedirs(PROBE, exist_ok=True)
ANNEX = [f'{i:04d}' for i in range(139, 160)]
ORIENTS = [('d0', 0), ('r90', 90), ('r180', 180), ('r270', 270)]
CACHED = os.path.join(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr',
                      'rot')


def score(text):
    toks = [t.strip('.,;:!?|«»"\'()[]') for t in text.split()]
    return len([t for t in toks if len(t) >= 5 and t.isalpha()
                and (re.search(r'[ąćęłńóśźż]', t, re.I) or t.islower())])


def main():
    out = {}
    for n in ANNEX:
        im0 = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
        W, H = im0.size
        results = []
        for tag, rot in ORIENTS:
            if rot == -90 and os.path.isfile(os.path.join(CACHED, n + '.png')):
                im = Image.open(os.path.join(CACHED, n + '.png'))
            elif rot:
                im = im0.rotate(rot, expand=True)
            else:
                im = im0
            w, h = im.size
            band = im.crop((0, int(h * 0.35), w, int(h * 0.65)))
            band = band.resize((int(w * 1.5),
                                int((int(h * 0.65) - int(h * 0.35)) * 1.5)),
                               Image.LANCZOS)
            p = os.path.join(PROBE, f'{n}_{tag}.png')
            band.save(p)
            t = read(p, lang='pol', psm=6)
            s = score(t)
            results.append((tag, s))
            print(n, tag, s, '::', t.strip().replace('\n', ' ')[:90])
        best = max(results, key=lambda z: z[1])
        out[n] = {'orient': best[0], 'scores': dict(results)}
        print(n, 'BEST:', best[0], best[1])
    with open(os.path.join(PROBE, '..', 'orient.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
