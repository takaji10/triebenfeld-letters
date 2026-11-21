# -*- coding: utf-8 -*-
"""Full sweep: for every annex row, line-crop c8(rok)/c9/c10/c11 and
report blobs, classifying small raised marks (star vs digit) and tall
strokes. Output: compact per-row report."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read, json
from PIL import Image

at = digit_read.at
OUT = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\sweep.txt'

SHEETS = {'0139': 31, '0140': 29, '0141': 35, '0142': 61, '0143': 73,
          '0144': 80, '0145': 111, '0146': 112, '0147': 12, '0148': 34,
          '0149': 48, '0150': 66, '0151': 79, '0152': 92, '0153': 103,
          '0154': 118, '0155': 128, '0156': 137, '0157': 156,
          '0158': 8, '0159': 11}


def main():
    # star templates
    star_grids = []
    STARS = [('0139', 9), ('0140', 21), ('0140', 26), ('0141', 36),
             ('0142', 48), ('0142', 54), ('0144', 77), ('0144', 78),
             ('0147', 1), ('0147', 12), ('0148', 15), ('0148', 17),
             ('0148', 22), ('0148', 24), ('0149', 44), ('0149', 48),
             ('0150', 62), ('0151', 74), ('0151', 75), ('0151', 77),
             ('0151', 79), ('0152', 82), ('0152', 83), ('0152', 84),
             ('0152', 85), ('0152', 87), ('0152', 91), ('0153', 103),
             ('0155', 119), ('0155', 123), ('0155', 127), ('0158', 1),
             ('0159', 1), ('0159', 3), ('0154', 107)]
    import line_crop
    ims = {}
    lib = digit_read.digit_lib()
    out = []
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
            try:
                ly0, ly1 = line_crop.true_lines(n, num, im, px)
            except Exception:
                out.append('%s r%d LINE-FAIL' % (n, num))
                continue
            cells = []
            for col in (9, 10, 11):
                x0, x1 = rules[col - 1] + 6, rules[col] - 6
                bl = digit_read.blobs(px, x0, x1, ly0, ly1, minpx=25)
                parts = []
                for b in sorted(bl, key=lambda t: t[0]):
                    w, h = b[1] - b[0], b[3] - b[2]
                    if w >= 38 and h <= 20 and b[4] <= 1100:
                        parts.append('-')
                        continue
                    if h < 42 and w <= 30 and b[4] < 700:
                        g = digit_read.grid(px, b)
                        ss = sorted(((max(digit_read.corr(g, rg)
                                          for rg in gs), d)
                                     for d, gs in lib.items()),
                                    reverse=True)[:1]
                        st = max(digit_read.corr(g, sg)
                                 for sg, _ in star_grids) \
                            if star_grids else 0
                        parts.append('^%s(%.2f/s%.2f)'
                                     % (ss[0][1], ss[0][0], st))
                        continue
                    if h > 62:
                        parts.append('|TALL')
                        continue
                    if b[4] < 120:
                        parts.append('.')
                        continue
                    g = digit_read.grid(px, b)
                    ss = sorted(((max(digit_read.corr(g, rg)
                                      for rg in gs), d)
                                 for d, gs in lib.items()), reverse=True)[:2]
                    parts.append('%s(%.2f/%s%.2f)'
                                 % (ss[0][1], ss[0][0],
                                    ss[1][1], ss[1][0]))
                cells.append('c%d[%s]' % (col, ' '.join(parts)
                                          if parts else 'EMPTY'))
            out.append('%s r%d y%d-%d %s' % (n, num, ly0, ly1,
                                             ' '.join(cells)))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    print(len(out), 'rows ->', OUT)


if __name__ == '__main__':
    main()
