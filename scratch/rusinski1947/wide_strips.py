# -*- coding: utf-8 -*-
"""Wide note strips: the WHOLE foot region at 3x, both models.

The earlier notestrips were cropped from v2's first-note top - they
could never witness the boundary itself (0075's swallowed heading was
inside v2's block, so its strip 'confirmed' it; notes ABOVE a too-low
block start were invisible). The wide strips crop from safely above
any plausible note start (min known note top - 300px, capped at 0.5H)
to the page bottom. The note paragraphs parsed from THESE strips are
matched back to page lines to anchor the boundary - the strip is then
an independent witness of both the inventory and the boundary.

Output: widestrips/<n>.json {'y0','pol','std'}.
"""
import sys, os, json, io
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
OUT = os.path.join(OCR, 'widestrips')
os.makedirs(OUT, exist_ok=True)


def main():
    known = {}
    for name in ('structure.json', 'structure2.json', 'structure4.json'):
        p = os.path.join(OCR, name)
        if os.path.isfile(p):
            s = json.load(open(p, encoding='utf-8'))
            for n, page in s.items():
                for x in page['notes']:
                    known.setdefault(n, []).append(x['top'])
    done = 0
    for n in sorted(known):
        p = os.path.join(OUT, n + '.json')
        if os.path.isfile(p):
            done += 1
            continue
        y0 = int(min(0.55 * 5936, min(known[n]) - 300))
        try:
            with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
                data = fh.read()
            im = Image.open(io.BytesIO(data)).convert('L')
            im.load()
        except Exception as e:
            print('SKIP', n, type(e).__name__)
            continue
        W, H = im.size
        c = im.crop((0, y0, W, H))
        c = c.resize((W * 3, (H - y0) * 3), Image.LANCZOS)
        sp = os.path.join(OUT, 'tmp.png')
        c.save(sp)
        try:
            t1 = read(sp, lang='pol', psm=4).strip()
            t2 = read(sp, lang='pol-std', psm=4).strip()
        except Exception as e:
            t1 = t2 = 'ERR ' + str(e)[:80]
        with open(p, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump({'y0': y0, 'pol': t1, 'std': t2}, fh,
                      ensure_ascii=False)
        done += 1
        if done % 20 == 0:
            print('done', done)
    print('wide strips:', done)


if __name__ == '__main__':
    main()
