# -*- coding: utf-8 -*-
"""Audit: band-based blob reads of c9/c10/c11 for every row (rule
x-ranges masked out), compared with the draft values. Differences with
high-confidence reads are draft errors."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read
from PIL import Image

at = digit_read.at
OUT = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\audit.txt'
SHEETS = ['0139', '0140', '0141', '0142', '0143', '0144', '0145',
          '0146', '0147', '0148', '0149', '0150', '0151', '0152',
          '0153', '0154', '0155', '0156', '0157', '0158', '0159']


def draft_rows():
    t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', '..', 'literature', 'rusinski1947',
                          'original.md'), encoding='utf-8').read()
    cur = None
    rows = {}
    for ln in t.splitlines():
        m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r'\| (\d+) \| ', ln)
        if m and cur:
            cells = [c.strip(' |') for c in ln.split(' | ')]
            rows[(cur, int(m.group(1)))] = cells
    return rows


def main():
    draft = draft_rows()
    lib = digit_read.digit_lib()
    ims = {}
    out = []
    for n in SHEETS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        nums = sorted(int(k) for k in at[n]['rows'] if k.isdigit())
        for num in nums:
            cells = draft.get((n, num))
            if cells is None:
                continue
            y0, y1 = at[n]['rows'][str(num)]['y']
            for col in (9, 10, 11):
                x0, x1 = rules[col - 1] + 8, rules[col] - 8
                bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=25)
                parts = []
                for b in sorted(bl, key=lambda t: t[0]):
                    w, h = b[1] - b[0], b[3] - b[2]
                    cx = (b[0] + b[1]) / 2
                    # rule proximity?
                    near_rule = (abs(b[0] - rules[col - 1]) < 12 or
                                 abs(b[1] - rules[col]) < 12) and w <= 14
                    if near_rule:
                        continue
                    if w >= 38 and h <= 20 and b[4] <= 1100:
                        parts.append('-')
                        continue
                    if h < 40 and w <= 30 and b[4] < 700:
                        # clipped tops of neighbor rows sit at the crop
                        # edge; real small digits sit inside
                        edge = (b[2] - (y0 + 2) < 9) or \
                            ((y1 - 2) - b[3] < 9)
                        if edge and h < 30:
                            continue
                        g = digit_read.grid(px, b)
                        ss = sorted(((max(digit_read.corr(g, rg)
                                          for rg in gs), d)
                                     for d, gs in lib.items()),
                                    reverse=True)[:1]
                        parts.append('^%s(%.2f)' % (ss[0][1], ss[0][0]))
                        continue
                    if h > 62:
                        parts.append('|TALL%d' % h)
                        continue
                    if b[4] < 120:
                        parts.append('.')
                        continue
                    g = digit_read.grid(px, b)
                    ss = sorted(((max(digit_read.corr(g, rg)
                                      for rg in gs), d)
                                 for d, gs in lib.items()), reverse=True)[:2]
                    parts.append('%s(%.2f/%s%.2f)'
                                 % (ss[0][1], ss[0][0], ss[1][1], ss[1][0]))
                got = ' '.join(parts) if parts else 'EMPTY'
                have = cells[col - 1] if col - 1 < len(cells) else '?'
                # discrepancy flag: glyph digits only (before parenthesis),
                # raised smalls (^) treated as marks, not digits
                gd = ''
                for tok in got.split():
                    if tok in ('-', '.', 'EMPTY') or tok.startswith('|'):
                        continue
                    if tok.startswith('^'):
                        continue
                    if tok and tok[0].isdigit():
                        gd += tok[0]
                hd = re.sub(r'[^0-9]', '', have.replace('*', ''))
                flag = '  <<< DIFF' if gd and hd and \
                    gd.replace('*', '') != hd.replace('*', '') else ''
                out.append('%s r%d c%d | draft=%-12s | pix=%s%s'
                           % (n, num, col, have[:12], got, flag))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    print(len(out), 'cells ->', OUT)


if __name__ == '__main__':
    main()
