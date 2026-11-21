# -*- coding: utf-8 -*-
"""Tight ink-bbox crops of the flagged cells, 6 per image at high zoom
for reliable visual transcription."""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
from PIL import Image, ImageDraw


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    import num_read
    cells = num_read.CELLS
    ims = {}
    panels = []
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
        pts = [(x, y) for x in range(x0, x1) for y in range(y0 + 2, y1 - 2)
               if px[x, y] < 175]
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        c = im.crop((bx0 - 5, by0 - 5, bx1 + 6, by1 + 6))
        sc = min(9, 1350 / c.size[0], 1900 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d c%d' % (n, num, col), c))
    per = 6
    for si in range(0, len(panels), per):
        chunk = panels[si:si + per]
        W = max(p.size[0] for _, p in chunk) + 180
        H = sum(p.size[1] + 12 for _, p in chunk) + 10
        out = Image.new('L', (W, H), 255)
        d = ImageDraw.Draw(out)
        yy = 5
        for tag, p in chunk:
            out.paste(p, (170, yy))
            d.text((5, yy + p.size[1] // 2), tag, fill=0)
            yy += p.size[1] + 12
        out.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tb_%02d.png'
                 % (si // per))
        print('tb_%02d.png' % (si // per), out.size,
              [t for t, _ in chunk])


if __name__ == '__main__':
    main()
