# -*- coding: utf-8 -*-
"""OCR the flagged numeric/name cells from tight ink-bboxes; several
configs per cell, majority reported. Doubtful cells get ASCII art."""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from num_read import RULES, SRC, OCR
from PIL import Image


def bbox(px, x0, x1, y0, y1, thr=175):
    pts = [(x, y) for x in range(x0, x1) for y in range(y0, y1)
           if px[x, y] < thr]
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), max(xs), min(ys), max(ys)


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    import num_read
    cells = num_read.CELLS
    ims = {}
    for n, num, col in cells:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bb = bbox(px, x0, x1, y0 + 2, y1 - 2)
        if not bb:
            print('%s r%d c%d EMPTY' % (n, num, col), flush=True)
            continue
        bx0, bx1, by0, by1 = bb
        c = im.crop((bx0 - 3, by0 - 3, bx1 + 4, by1 + 4))
        outs = []
        for sc in (6, 9):
            cc = c.resize((c.size[0] * sc, c.size[1] * sc), Image.LANCZOS)
            p = os.path.join(OCR, 'cell_tmp.png')
            cc.save(p)
            for lang in ('pol', 'deu'):
                for psm in (7, 8, 13):
                    try:
                        t = read(p, lang=lang, psm=psm).strip()
                        t = t.replace('\n', ' / ')
                        if t and t not in outs:
                            outs.append(t)
                    except Exception:
                        pass
        print('%s r%d c%d bbox x%d-%d y%d-%d -> %s'
              % (n, num, col, bx0, bx1, by0, by1, ' | '.join(outs[:6])),
              flush=True)


if __name__ == '__main__':
    main()
