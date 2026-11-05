# -*- coding: utf-8 -*-
"""The full-line re-read of tom5's body text: every body line of every
page cropped from the scan, upscaled 2.5x, and read with both models at
psm 7.

Purpose (2026-11-05):
  1. a line-level third and fourth witness for the whole book (the page
     passes were read at the scan's own resolution; the lines re-read
     larger resolve the doubtful spots);
  2. the superscript footnote markers, which the page passes lose almost
     entirely: in the line crop they read, and the diff against the
     page-pass line isolates them (extra tokens that are digits or the
     known artifact forms).

Body lines come from structure.json (the TSV-box lines minus the foot-note
block). Landscape annex sheets are excluded (table_rebuild.py handles
them). Output: lines/<scan>.json with one record per line:
  {top, page_text, line_pol, line_std, markers: [tokens]}
where markers = the extra tokens of the line passes against the page pass.
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
LINES = os.path.join(OCR, 'lines')
os.makedirs(LINES, exist_ok=True)
LANDSCAPE = {f'{i:04d}' for i in range(139, 160)}
SCALE = 2.5
PAD = 20


def main():
    struct = json.load(open(os.path.join(OCR, 'structure.json'),
                            encoding='utf-8'))
    for n in sorted(struct):
        if n in LANDSCAPE:
            continue
        outp = os.path.join(LINES, n + '.json')
        if os.path.isfile(outp):
            continue
        page = struct[n]
        # the note block's first top, to bound the body
        note_top = min((x['top'] for x in page['notes']), default=None)
        im = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
        W, H = im.size
        recs = []
        # confidence per word, mapped to lines by top
        d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
        wconf = [(x[1], x[4]) for x in d['words'] if x[5].strip()]
        for ln in page['lines']:
            if note_top is not None and ln['top'] >= note_top:
                continue
            # skip the re-read where every word of the line read at high
            # confidence (or the conf-0 quirk) and no marker candidate
            # (a glued digit run) rides in it: the line passes' unique
            # yield there would be nil
            confs = [c for (t, c) in wconf if abs(t - ln['top']) < 30]
            safe = (confs and all(c == 0.0 or c >= 80.0 for c in confs)
                    and not re.search(r'[a-ząćęłńóśźż]{2,}\d{1,2}\b',
                                      ln['text']))
            if safe:
                recs.append({'top': ln['top'], 'page': ln['text'],
                             'line_pol': None, 'line_std': None,
                             'skipped': True})
                continue
            a = max(0, ln['top'] - PAD)
            b = min(H, ln['top'] + 75)
            band = im.crop((0, a, W, b))
            band = band.resize((int(W * SCALE), int((b - a) * SCALE)),
                               Image.LANCZOS)
            p = os.path.join(LINES, 'tmp.png')
            band.save(p)
            try:
                t1 = read(p, lang='pol', psm=7).strip()
                t2 = read(p, lang='pol-std', psm=7).strip()
            except Exception as e:
                t1 = t2 = 'ERR ' + str(e)[:60]
            recs.append({'top': ln['top'], 'page': ln['text'],
                         'line_pol': t1, 'line_std': t2})
            print(n, ln['top'], '|', t1[:70])
        with open(outp, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(recs, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
