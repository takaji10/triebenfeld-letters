# -*- coding: utf-8 -*-
"""Per-note 3x re-reads: every note cropped to its own geometry
(structure2's verified tops: this note's top to the next note's top)
and read at 3x with both models.

The page strips' paragraph segmentation proved unreliable for wholesale
adoption (psm 6 merges/splits paragraphs at odds with the print's note
boundaries); the per-note crop needs no segmentation at all - the
boundaries come from the verified inventory, the text from the higher
resolution. The leading number token is dropped from the reading (the
structure supplies the number); artifact-glyph leading tokens ('!',
'%', '*') are dropped the same way.

Output: notetexts/<n>_<k>.json {'pol','std'}; structure4.json applies
them where both models agree (or one agrees with the page text).
"""
import sys, os, json, re, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
OUT = os.path.join(OCR, 'notetexts')
os.makedirs(OUT, exist_ok=True)

LEAD = re.compile(r'^[\d!%*+$§£|.,)»\-—–\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])')


def open_tif(n):
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        data = fh.read()
    im = Image.open(io.BytesIO(data))
    im.load()
    return im


def main():
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    done = 0
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            continue
        im = None
        for n_ in notes:
            outp = os.path.join(OUT, f'{n}_{n_["num"]}.json')
            if os.path.isfile(outp):
                continue
            if im is None:
                try:
                    im = open_tif(n)
                except Exception as e:
                    print('SKIP page', n, type(e).__name__, str(e)[:60])
                    break
            W, H = im.size
            y0 = max(0, n_['top'] - 8)
            nxt = [x['top'] for x in notes if x['top'] > n_['top']]
            y1 = (nxt[0] - 4) if nxt else H
            c = im.crop((0, y0, W, min(H, y1)))
            c = c.resize((W * 3, (min(H, y1) - y0) * 3), Image.LANCZOS)
            sp = os.path.join(OUT, 'tmp.png')
            c.save(sp)
            try:
                t1 = read(sp, lang='pol', psm=6).strip()
                t2 = read(sp, lang='pol-std', psm=6).strip()
            except Exception as e:
                t1 = t2 = 'ERR ' + str(e)[:60]
            with open(outp, 'w', encoding='utf-8', newline='\n') as fh:
                json.dump({'pol': t1, 'std': t2}, fh, ensure_ascii=False)
            done += 1
        if done and done % 50 == 0:
            print('done', done)
    print('note re-reads:', done)


if __name__ == '__main__':
    main()
