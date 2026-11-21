# -*- coding: utf-8 -*-
"""Per-cell reading pass for one sheet: for every row/cell, classify ink
into EMPTY / DASH / blobs (n, widths, heights) and OCR the text columns
at high zoom. Output: a report file for manual encoding of fixes."""
import sys, os, json, io, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode'
                   r'\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(os.path.join(OCR, 'annex_table.json'), encoding='utf-8'))

RULES = {  # per-sheet vertical rule x positions (from band scans)
}

def get_rules(n):
    """Detect the sheet's vertical rules from a clean mid-table band."""
    if n in RULES:
        return RULES[n]
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    rows = at[n]['rows']
    nums = sorted(int(k) for k in rows if k.isdigit())
    y0 = rows[str(nums[len(nums)//2])]['y'][0] + 8
    y1 = rows[str(nums[len(nums)//2])]['y'][1] - 8
    cands = []
    for x in range(700, 5400):
        dark = sum(1 for y in range(y0, y1) if px[x, y] < 170)
        if dark > (y1 - y0) * 0.75:
            cands.append(x)
    groups = []
    for x in cands:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    r = [(g[0] + g[-1]) // 2 for g in groups]
    RULES[n] = r
    return r

def blobs(px, x0, x1, y0, y1, minpx=25):
    seen = set()
    out = []
    for x in range(x0, x1):
        for y in range(y0, y1):
            if px[x, y] < 170 and (x, y) not in seen:
                stack = [(x, y)]
                comp = []
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    comp.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if x0 <= nx < x1 and y0 <= ny < y1 \
                                    and (nx, ny) not in seen \
                                    and px[nx, ny] < 170:
                                seen.add((nx, ny))
                                stack.append((nx, ny))
                if len(comp) > minpx:
                    xs = [p[0] for p in comp]
                    ys = [p[1] for p in comp]
                    out.append((min(xs), max(xs), min(ys), max(ys),
                                len(comp)))
    return sorted(out)

def ocr_cell(im, x0, x1, y0, y1, psm_list=(7, 6)):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.size[0] * 6, c.size[1] * 6), Image.LANCZOS)
    p = os.path.join(OCR, 'cell_tmp.png')
    c.save(p)
    outs = []
    for psm in psm_list:
        try:
            t = read(p, lang='pol', psm=psm).strip()
            t = t.replace('\n', ' / ')
            if t and t not in outs:
                outs.append(t)
        except Exception:
            pass
    return ' || '.join(outs)

def main():
    n = sys.argv[1]
    r_lo = int(sys.argv[2])
    r_hi = int(sys.argv[3])
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    rules = get_rules(n)
    bounds = rules + [rules[-1] + 120]
    md = json.load(open(os.path.join(OCR, 'annex_md.json'),
                        encoding='utf-8'))
    out = []
    for num in range(r_lo, r_hi + 1):
        row = [r for r in md[n]['rows'] if r['num'] == num]
        cur = row[0]['cells'] if row else None
        y0, y1 = at[n]['rows'][str(num)]['y']
        out.append('=== r%d y=%s' % (num, (y0, y1)))
        for ci in range(1, 11):
            x0, x1 = bounds[ci] + 5, bounds[ci + 1] - 5
            bl = blobs(px, x0, x1, y0 + 4, y1 - 4)
            if not bl:
                kind = 'EMPTY'
            elif len(bl) == 1 and (bl[0][1] - bl[0][0]) >= 38 \
                    and (bl[0][3] - bl[0][2]) <= 20 and bl[0][4] <= 1100:
                kind = 'DASH'
            else:
                kind = ' '.join('%dx%d' % (b[1] - b[0] + 1,
                                           b[3] - b[2] + 1) for b in bl)
            txt = ''
            if kind not in ('EMPTY', 'DASH') and ci <= 7:
                txt = ocr_cell(im, x0, y0 + 4 and x0, x1, y1 - 4) \
                    if False else ocr_cell(im, x0, x1, y0 + 4, y1 - 4)
            out.append('  c%d [%s] cur=%r%s' % (
                ci, kind, cur[ci] if cur else None,
                (' ocr=%r' % txt) if txt else ''))
    with open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
              r'\cells_%s_%d_%d.txt' % (n, r_lo, r_hi), 'w',
              encoding='utf-8') as fh:
        fh.write('\n'.join(out) + '\n')
    print('done', n, r_lo, r_hi)

if __name__ == '__main__':
    main()
