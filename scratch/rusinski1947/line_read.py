# -*- coding: utf-8 -*-
"""Per-line blob analysis for the tall flagged cells: cluster blobs by
y-center, match each cluster against the digit library."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read
from PIL import Image

JOBS = None  # filled from the draft's junk census when run with 'auto'


def census():
    """Enumerate the draft's junk numeric cells (non-digit, non-dash)
    in cols 9/10/11 (0-based 8/9/10) per series."""
    import re
    t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', '..', 'literature', 'rusinski1947',
                          'original.md'), encoding='utf-8').read()
    marks = [m.start() for m in
             re.finditer(r'<!-- annex sheet 0(1\d\d) -->', t)]
    segs = []
    for i, s in enumerate(marks):
        e = marks[i + 1] if i + 1 < len(marks) else t.find('[p. 145]')
        segs.append((t[s:e], '015' + '' if False else None))
    # simpler: sheet-tagged segments
    out = []
    cur = None
    for ln in t.splitlines():
        m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r'\| (\d+) \| ', ln)
        if m and cur:
            cells = [c.strip(' |') for c in ln.split(' | ')]
            for k in (8, 9, 10):
                v = cells[k].replace('*', '').strip()
                if re.fullmatch(r'[\d.]+', v) or v in ('—', '-', ''):
                    continue
                out.append((cur, int(m.group(1)), k + 1))
    return out


def main():
    lib = digit_read.digit_lib()
    jobs = census() if len(sys.argv) > 1 and sys.argv[1] == 'auto' \
        else [tuple(a if i == 2 else int(a) if i else a
                    for i, a in enumerate(a.split(':')))
              for a in sys.argv[1:]]
    for n, num, col in jobs:
        if n not in digit_read._ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            digit_read._ims[n] = (im, im.load())
        im, px = digit_read._ims[n]
        rules = RULES[n]
        y0, y1 = digit_read.at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2)
        if not bl:
            print(n, 'r%d c%d EMPTY' % (num, col), flush=True)
            continue
        # cluster by y-center with gap threshold
        bl2 = sorted(bl, key=lambda b: ((b[2] + b[3]) // 2, b[0]))
        lines = []
        for b in bl2:
            yc = (b[2] + b[3]) // 2
            if lines and yc - lines[-1]['yc'] <= 30:
                lines[-1]['blobs'].append(b)
                lines[-1]['yc'] = (lines[-1]['yc'] + yc) // 2
            else:
                lines.append({'yc': yc, 'blobs': [b]})
        parts = []
        for L in lines:
            ds = []
            for b in sorted(L['blobs'], key=lambda x: x[0]):
                w, h = b[1] - b[0], b[3] - b[2]
                tag = 'DASH' if w >= 38 and h <= 20 and b[4] <= 1100 else \
                      ('tiny' if b[4] < 300 or h < 25 else None)
                if tag:
                    ds.append(tag)
                    continue
                g = digit_read.grid(px, b)
                sc = sorted(((max(digit_read.corr(g, rg)
                                  for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)
                ds.append('%s%.2f[x%d-%d y%d-%d w%d h%d]'
                          % (sc[0][1], sc[0][0], b[0], b[1], b[2], b[3],
                             w, h))
            parts.append(' | '.join(ds))
        print(n, 'r%d c%d y%d-%d n=%d' % (num, col, y0, y1, len(bl)),
              '   LINES:', ' // '.join(parts), flush=True)


if __name__ == '__main__':
    main()
