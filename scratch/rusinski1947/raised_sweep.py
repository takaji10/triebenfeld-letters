# -*- coding: utf-8 -*-
"""Find ALL raised small blobs in dymy (c9) cells; classify star vs
digit; tabulate digit values to test the mill-count hypothesis
(body: 1 water mill + 8 windmills = 9 mills total)."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read, line_crop
from PIL import Image

at = digit_read.at
SHEETS = {'0139': 13, '0140': 29, '0141': 44, '0142': 61, '0143': 73,
          '0144': 86, '0145': 111, '0146': 112, '0147': 12, '0148': 34,
          '0149': 48, '0150': 66, '0151': 79, '0152': 92, '0153': 103,
          '0154': 118, '0155': 132, '0156': 145, '0157': 156,
          '0158': 8, '0159': 11}


def main():
    lib = digit_read.digit_lib()
    ims = {}
    total = 0
    for n in sorted(SHEETS):
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        for num in range(1, SHEETS[n] + 1):
            key = str(num)
            if key not in at[n]['rows']:
                continue
            y0, y1 = at[n]['rows'][str(num)]['y']
            # extended window to catch raised marks
            x0, x1 = rules[8] + 8, rules[9] - 8
            bl = digit_read.blobs(px, x0, x1, y0 - 6, y1 + 6, minpx=60)
            for b in bl:
                w, h = b[1] - b[0], b[3] - b[2]
                if h > 44 or w > 34:
                    continue   # full digits / dashes
                if h < 12:
                    continue
                # raised = blob top is well above the band's digit baseline?
                # just report all small blobs
                g = digit_read.grid(px, b)
                ss = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)[:2]
                print('%s r%d small x%d-%d y%d-%d w%d h%d n%d -> %s'
                      % (n, num, b[0], b[1], b[2], b[3], w, h, b[4],
                         ' '.join('%s:%.2f' % (d, s) for s, d in ss)),
                      flush=True)
                try:
                    total += int(ss[0][1])
                except Exception:
                    pass
    print('SUM of small-blob top digits:', total)


if __name__ == '__main__':
    main()
