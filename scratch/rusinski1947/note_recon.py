# -*- coding: utf-8 -*-
"""Column-aware reconstruction of the table-note blocks on scans 0076
(TABELA II notes 1-4) and 0077 (TABELA III notes 1-3)."""
import json, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def dump(n, y0, y1):
    d = json.load(open(os.path.join(OCR, '%s.json' % n), encoding='utf-8'))
    ws = d['words']
    # column split: find the x-gap
    xs = sorted(w[0] for w in ws if y0 <= w[1] <= y1)
    # histogram of x to find the gutter
    import collections
    h = collections.Counter(x // 50 * 50 for x in xs)
    cols = sorted(k for k, v in h.items() if v > 3)
    print('=== scan %s zone y%d-%d: x-range %d-%d' % (n, y0, y1, xs[0], xs[-1]))
    print('x histogram buckets:', [c for k, c in sorted(h.items())])
    # lines with x
    lines = {}
    for w in ws:
        if y0 <= w[1] <= y1:
            lines.setdefault(round(w[1] / 26), []).append(w)
    for k in sorted(lines):
        ws2 = sorted(lines[k], key=lambda x: x[0])
        left = ' '.join(w[5] for w in ws2 if w[0] < 1900)
        right = ' '.join(w[5] for w in ws2 if w[0] >= 1900)
        print('%5d | L: %-58s | R: %s' % (k * 26, left[:58], right[:70]))


dump('0076', 3040, 5120)
print()
dump('0077', 4300, 5936)
