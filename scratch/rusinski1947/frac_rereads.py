# -*- coding: utf-8 -*-
"""Targeted re-reads of the fraction artifacts, at 5x.

The print sets vulgar fractions (1/2, 1/4, 3/4 with a horizontal bar)
which the page passes split ('81/,', '271/4', '3/g'). Every body token
matching the split shapes is cropped with its two neighbours at 5x and
re-read with both models (psm 7). The readings land in
fractions/<scan>_<left>_<top>.txt (both passes, '@@@'-separated); the
settlement step applies them where they agree.
"""
import sys, os, json, re, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
OUT = os.path.join(OCR, 'fractions')
os.makedirs(OUT, exist_ok=True)
BODY = {f'{i:04d}' for i in range(16, 138)} | \
       {f'{i:04d}' for i in range(160, 172)}

# the split shapes: digits glued to a slash-plus-fragment
SPLIT = re.compile(
    r'^(?P<pre>\d{1,3})(?P<num>\d{1,2})?[/\u2019\u2018\u0027]'
    r'(?P<den>[,.gso0Oo Il1ly].{0,2})?[.,;:]?$')


def is_frac(tok):
    if not SPLIT.match(tok):
        return False
    # exclude plain decimals like 16,80 (a comma between digits, no
    # slash) and dates; require a slash or apostrophe
    return '/' in tok or '\u2019' in tok or "'" in tok


def main():
    import PIL
    print('PIL from:', PIL.__file__, '| Image from:', Image.__file__)
    # self-test: the exact open the loop performs
    with open(os.path.join(SRC, 'tom5_0028.tif'), 'rb') as fh:
        sd = fh.read()
    try:
        si = Image.open(io.BytesIO(sd))
        si.load()
        print('SELF-TEST OK', si.size)
    except Exception as e:
        print('SELF-TEST FAIL', type(e).__name__, e)
    count = 0
    for fn in sorted(os.listdir(OCR)):
        if not (fn.endswith('.json') and len(fn) == 9):
            continue
        n = fn[:4]
        if n not in BODY:
            continue
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        hits = [x for x in d['words'] if is_frac(x[5].strip())
                and x[4] != 0.0]
        for x in hits:
            l, t, w_, h = x[0], x[1], x[2], x[3]
            outp = os.path.join(OUT, f'{n}_{l}_{t}.txt')
            if os.path.isfile(outp):
                continue
            im = None
            err = ''
            for attempt in range(3):
                try:
                    with open(os.path.join(SRC, f'tom5_{n}.tif'),
                              'rb') as fh:
                        data = fh.read()
                    im = Image.open(io.BytesIO(data))
                    im.load()
                    break
                except Exception as e:
                    im = None
                    head = data[:12].hex() if data else '-'
                    err = (f'{type(e).__name__}: {e} '
                           f'len={len(data) if data else -1} head={head}')
            if im is None:
                print('SKIP (unreadable)', n, x[5], err)
                continue
            W, H = im.size
            a, b = max(0, t - 12), min(H, t + h + 12)
            lo = max(0, l - 500)
            hi = min(W, l + w_ + 500)
            c = im.crop((lo, a, hi, b))
            c = c.resize((c.size[0] * 5, c.size[1] * 5), Image.LANCZOS)
            sp = os.path.join(OUT, 'tmp.png')
            c.save(sp)
            try:
                t1 = read(sp, lang='pol', psm=7).strip()
                t2 = read(sp, lang='pol-std', psm=7).strip()
            except Exception as e:
                t1 = t2 = 'ERR ' + str(e)[:60]
            with open(outp, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(x[5].strip() + '\n---\n' + t1 + '\n@@@\n' + t2)
            count += 1
    print('fraction re-reads:', count)


if __name__ == '__main__':
    main()
