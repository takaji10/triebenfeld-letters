# -*- coding: utf-8 -*-
"""ASCII art of every junk numeric cell (cols 9-11), line-clustered,
with the OCR raw for cross-checking."""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC, OCR
import digit_read, line_read
from PIL import Image

OUT = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\artcells.txt'


def main():
    at = digit_read.at
    jobs = line_read.census()
    byrow = {}
    for n, num, col in jobs:
        byrow.setdefault((n, num), []).append(col)
    ims = {}
    lines = []
    for (n, num), cols in sorted(byrow.items()):
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        raw = (at[n]['rows'][str(num)].get('raw') or '').replace('\n', ' ')
        lines.append('=== %s r%d c%s' % (n, num, ','.join(map(str, cols))))
        lines.append('  RAW: ' + repr(raw[:210]))
        rules = digit_read.RULES[n] if hasattr(digit_read, 'RULES') \
            else None
        import num_read
        rules = num_read.RULES[n]
        for col in cols:
            x0, x1 = rules[col - 1] + 6, rules[col] - 6
            y0, y1 = at[n]['rows'][str(num)]['y']
            bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=25)
            if not bl:
                lines.append('  c%d: EMPTY' % col)
                continue
            bl2 = sorted(bl, key=lambda b: ((b[2] + b[3]) // 2, b[0]))
            clusters = []
            for b in bl2:
                yc = (b[2] + b[3]) // 2
                if clusters and yc - clusters[-1][0] <= 30:
                    clusters[-1][1].append(b)
                    clusters[-1][0] = (clusters[-1][0] + yc) // 2
                else:
                    clusters.append([yc, [b]])
            for ci, (_, grp) in enumerate(clusters):
                xs = [v for b in grp for v in (b[0], b[1])]
                ys = [v for b in grp for v in (b[2], b[3])]
                bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
                lines.append('  c%d L%d x%d-%d y%d-%d:'
                             % (col, ci, bx0, bx1, by0, by1))
                head = ''.join(str((x // 10) % 10)
                               for x in range(bx0 - 2, bx1 + 3))
                lines.append('     ' + head)
                for y in range(by0 - 2, by1 + 3, 2):
                    row = ''
                    for x in range(bx0 - 2, bx1 + 3):
                        v = min(px[x, y], px[x, y + 1])
                        row += '#' if v < 160 else \
                            ('+' if v < 200 else ('-' if v < 235 else '.'))
                    if row.strip('.'):
                        lines.append('%5d %s' % (y, row))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
    print(len(lines), 'lines ->', OUT)


if __name__ == '__main__':
    main()
