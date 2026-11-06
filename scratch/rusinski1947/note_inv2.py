# -*- coding: utf-8 -*-
"""Full inventory of the annex tables' footnote apparatus:
(a) per sheet: the Nazwa column's trailing superscript marks,
(b) per sheet: note lines below the table (leading digit at x~1090-1210),
(c) the same for the notes that start mid-sheet-bottom and wrap.
Writes a report for transcription planning."""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(os.path.join(OCR, 'annex_table.json'), encoding='utf-8'))

SHEETS = ['0139', '0140', '0141', '0142', '0143', '0144', '0145', '0146',
          '0147', '0148', '0149', '0150', '0151', '0152', '0153', '0154',
          '0155', '0156', '0157', '0158', '0159']

def rules_of(px, y0, y1):
    cands = []
    for x in range(700, 5400):
        dark = sum(1 for y in range(y0, y1) if px[x, y] < 170)
        if dark > (y1 - y0) * 0.8:
            cands.append(x)
    groups = []
    for x in cands:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    return [(g[0] + g[-1]) // 2 for g in groups]

out = []
for n in SHEETS:
    p = os.path.join(SRC, 'tom5_%s.tif' % n)
    with open(p, 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    rows = at[n]['rows']
    nums = sorted(int(k) for k in rows if k.isdigit())
    y_end = max(rows[str(k)]['y'][1] for k in nums)
    mid = rows[str(nums[len(nums) // 2])]['y']
    rules = rules_of(px, mid[0] + 30, mid[1] - 20)
    out.append('=== %s (table ends y%d, rules %s)' % (n, y_end, rules))
    # nazwa marks
    marks = []
    for num in nums:
        ry0, ry1 = rows[str(num)]['y']
        cols = []
        prev = False
        for x in range(rules[1] + 6, rules[2] - 6):
            dark = any(px[x, y] < 170 for y in range(ry0 + 20, ry1 - 5))
            if dark and not prev:
                a = x
            if prev and not dark:
                if x - a > 2:
                    cols.append((a, x))
            prev = dark
        if len(cols) >= 2:
            last = cols[-1]
            gap = last[0] - cols[-2][1]
            w = last[1] - last[0]
            if gap > 10 and 10 <= w <= 45:
                ys = [y for y in range(ry0, ry1) if any(
                    px[x, y] < 170 for x in range(last[0], last[1] + 1))]
                marks.append((num, last[0], last[1], min(ys), max(ys)))
    out.append('  marks: %s' % marks)
    # note lines below table: scan y_end+20 .. +700 for lines starting x1090-1220
    y = y_end + 20
    y_stop = min(y + 750, im.size[1] - 5)
    note_lines = []
    prev = False
    for yy in range(y, y_stop):
        n_ink = sum(1 for x in range(830, 5260, 2) if px[x, yy] < 190)
        cur = n_ink > 6
        if cur and not prev:
            a = yy
        if prev and not cur:
            if yy - a > 12:
                # find the line's first ink x
                fx = None
                for x in range(900, 1400):
                    if any(px[x, yy2] < 190 for yy2 in range(a, yy)
                           for yy2 in [yy2]):
                        pass
                note_lines.append((a, yy))
        prev = cur
    out.append('  text bands below table: %s' % note_lines)

with open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\ninv2.txt', 'w',
          encoding='utf-8') as fh:
    fh.write('\n'.join(out) + '\n')
print('written ninv2.txt')
