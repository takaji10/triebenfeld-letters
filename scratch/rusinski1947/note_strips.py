# -*- coding: utf-8 -*-
"""Strip re-reads of every note block, at 3x, both models.

The note blocks were never re-read at high scale (the full-line pass
stopped at v1's wrong note boundary), so their leading digits and small
type rest on the page passes alone. Every page with parsed notes gets
its note block re-read as one strip (y from the first note's top - 40
to the page bottom), psm 6, both models, 3x.

Output: notestrips/<n>.json {'y0','y1','pol','std'}; the reconciliation
against structure2's parse is note_reconcile.py.
"""
import sys, os, json
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
OUT = os.path.join(OCR, 'notestrips')
os.makedirs(OUT, exist_ok=True)


def main():
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    done = 0
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            continue
        p = os.path.join(OUT, n + '.json')
        if os.path.isfile(p):
            done += 1
            continue
        y0 = min(x['top'] for x in notes) - 40
        im = Image.open(os.path.join(SRC, f'tom5_{n}.tif')).convert('L')
        W, H = im.size
        y1 = H
        c = im.crop((0, max(0, y0), W, y1))
        c = c.resize((W * 3, (y1 - max(0, y0)) * 3), Image.LANCZOS)
        sp = os.path.join(OUT, 'tmp.png')
        c.save(sp)
        try:
            t1 = read(sp, lang='pol', psm=6).strip()
            t2 = read(sp, lang='pol-std', psm=6).strip()
        except Exception as e:
            t1 = t2 = 'ERR ' + str(e)[:80]
        with open(p, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump({'y0': int(y0), 'y1': int(y1), 'pol': t1,
                       'std': t2}, fh, ensure_ascii=False)
        done += 1
        if done % 10 == 0:
            print('done', done)
    print('note strips:', done)


if __name__ == '__main__':
    main()
