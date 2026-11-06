# -*- coding: utf-8 -*-
"""For each bad data cell: blob x-geometry of the data cell
(day digits | month glyphs | year digits). Widths decide the month."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
bad = [l for l in open(
    r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\datebad.txt',
    encoding='utf-8').read().splitlines() if l[:4].isdigit()]


def main():
    ims = {}
    out = []
    for line in bad:
        m = re.match(r'(0\d\d\d) r(\d+) \| (.*?) \| RAW', line)
        if not m:
            continue
        n, num, cur = m.group(1), int(m.group(2)), m.group(3)
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        key = str(num)
        if key not in at.get(n, {}).get('rows', {}):
            continue
        y0, y1 = at[n]['rows'][key]['y']
        x0, x1 = rules[7] + 6, rules[8] - 6
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=20)
        seq = []
        for b in sorted(bl, key=lambda t: t[0]):
            w, h = b[1] - b[0], b[3] - b[2]
            seq.append('%d@w%dh%d' % (b[0], w, h))
        out.append('%s r%d cur=%r | %s' % (n, num, cur[:24],
                                           ' '.join(seq)))
    open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\dategeo.txt',
         'w', encoding='utf-8').write('\n'.join(out))
    print(len(out), 'cells')


if __name__ == '__main__':
    main()
