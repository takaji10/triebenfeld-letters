# -*- coding: utf-8 -*-
"""Orientation probe for the five misoriented annex sheets of tom5.

The strip reads showed 0144, 0150, 0152, 0154, 0158 reading as gibberish
in the orientation table_rebuild.py cached (the even sheets' rotate(-90)
PNG). Each is probed in all four orientations: a middle band of the page
is read at 2x with psm 6 in each, and the pass whose output carries the
most Polish words (the frequency heuristic: tokens with Polish diacritics
or >= 6 letters) is the sheet's true orientation.
"""
import sys, os, json
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
TMP = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
PROBE = os.path.join(TMP, 'tom5_ocr', 'probe')
os.makedirs(PROBE, exist_ok=True)
SHEETS = ['0144', '0150', '0152', '0154', '0158']
ORIENTS = [('d0', 0), ('r90', 90), ('r180', 180), ('r270', 270)]


def score(text):
    toks = [t.strip('.,;:!?|«»"\'()[]') for t in text.split()]
    good = [t for t in toks
            if len(t) >= 5 and (re.search(r'[ąćęłńóśźż]', t, re.I)
                                or t.isalpha() and t.islower())]
    return len(good)


def main():
    for n in SHEETS:
        im0 = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
        W, H = im0.size
        best = None
        for tag, rot in ORIENTS:
            im = im0.rotate(rot, expand=True) if rot else im0
            w, h = im.size
            band = im.crop((0, int(h*0.35), w, int(h*0.65)))
            band = band.resize((int(w*1.5), int((int(h*0.65)-int(h*0.35))*1.5)),
                               Image.LANCZOS)
            p = os.path.join(PROBE, f'{n}_{tag}.png')
            band.save(p)
            t = read(p, lang='pol', psm=6)
            s = score(t)
            print(n, tag, 'score:', s, '::', t.strip().replace('\n', ' ')[:110])
            if best is None or s > best[1]:
                best = (tag, s)
        print(n, 'BEST:', best[0], best[1])


import re
if __name__ == '__main__':
    main()
