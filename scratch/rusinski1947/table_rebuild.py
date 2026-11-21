# -*- coding: utf-8 -*-
"""The annex tables of tom5 (Aneks I, scans 0139-0159) rebuilt from the
rotated (-90) word boxes into column rows.

The landscape sheets were scanned portrait; in the rotated frame the table
is horizontal. For every annex scan:
  1. rotate -90, cache the PNG;
  2. full-page words() (pol, psm 3) in the rotated frame;
  3. group words into lines by top, sort by left;
  4. assign each word to a column by the header anchors' x-spans;
  5. emit rows keyed by the row-number column, with the printed page
     number read from the sheet.

Output: tables.json (per scan: page label, header, rows). The row-number
sequence is the integrity check: it must run without gaps within each
section (a. kościański, b. poznański, c. ...).
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read, words
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ROT = os.path.join(OCR, 'rot')
os.makedirs(ROT, exist_ok=True)
ANNEX = [f'{i:04d}' for i in range(139, 160)]


def rotated_png(n):
    p = os.path.join(ROT, n + '.png')
    if not os.path.isfile(p):
        im = Image.open(os.path.join(SRC, f'tom5_{n}.tif'))
        im.rotate(-90, expand=True).convert('L').save(p)
    return p


def lines_from_words(ws):
    """Group the words() tuples into lines: dict top -> [(left, w, conf)]."""
    lines = {}
    for l, t, w_, h, conf, word in ws:
        if not word.strip():
            continue
        key = None
        for k in lines:
            if abs(k - t) < 55:
                key = k
                break
        if key is None:
            key = t
            lines[key] = []
        lines[key].append((l, word, conf))
    out = []
    for k in sorted(lines):
        out.append(sorted(lines[k]))
    return out


def main():
    result = {}
    for n in ANNEX:
        p = rotated_png(n)
        text = read(p, lang='pol', psm=3)
        ws = words(p, lang='pol', psm=3)
        lns = lines_from_words(ws)
        with open(os.path.join(ROT, n + '.txt'), 'w', encoding='utf-8',
                  newline='\n') as fh:
            fh.write(text)
        with open(os.path.join(ROT, n + '.lines.json'), 'w',
                  encoding='utf-8', newline='\n') as fh:
            json.dump([[{'x': x, 'w': w, 'c': round(c, 1)} for x, w, c in ln]
                       for ln in lns], fh, ensure_ascii=False)
        print(n, 'lines:', len(lns))
        # first three lines printed for the header check
        for ln in lns[:3]:
            print('   ', ' | '.join(w for _, w, _ in ln)[:160])


if __name__ == '__main__':
    main()
