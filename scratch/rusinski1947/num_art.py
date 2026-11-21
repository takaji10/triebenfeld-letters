# -*- coding: utf-8 -*-
"""ASCII art of the flagged cells' ink bboxes (1:1 pixels, threshold
tiers) for visual transcription. Output -> $env:TEMP\\opencode\\numart.txt"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
from PIL import Image


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    import num_read
    cells = num_read.CELLS
    ims = {}
    out = []
    for n, num, col in cells:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = im.load()
        px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        pts = [(x, y) for x in range(x0, x1) for y in range(y0 + 2, y1 - 2)
               if px[x, y] < 175]
        if not pts:
            out.append('=== %s r%d c%d EMPTY' % (n, num, col))
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        out.append('=== %s r%d c%d x%d-%d y%d-%d n=%d'
                   % (n, num, col, bx0, bx1, by0, by1, len(pts)))
        step = 2 if (by1 - by0) > 70 else 1
        for y in range(by0 - 1, by1 + 2, step):
            row = ''
            for x in range(bx0 - 1, bx1 + 2):
                v = min(px[x, y], px[x, y + 1])
                row += '#' if v < 160 else ('+' if v < 200
                                            else ('-' if v < 230 else '.'))
            out.append('%4d %s' % (y, row))
    with open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\numart.txt',
              'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out) + '\n')
    print('written', len(out), 'lines')


if __name__ == '__main__':
    main()
