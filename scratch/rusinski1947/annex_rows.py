# -*- coding: utf-8 -*-
"""Rebuild the ANEKS I rows from the editor's separator lines
(rowlines.json, original-scan y pixels per sheet).

Each band between consecutive separators is one printed row; the band
is cropped full-width and OCR'd (3x, psm 6, pol; pol-std fallback when
the row number is not recovered). Output: annex_rows.json (the band
texts, for inspection) + annex_table.json in compose's format.

Bands too thin (<45px) are separator double-draws; empty bands are
skipped. 0081 (Tabela V) is already rebuilt by hand - not touched."""
import json, os, io, re, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TMP = os.path.join(OCR, 'row_tmp.png')

rowlines = json.load(open(os.path.join(OCR, 'rowlines.json'),
                          encoding='utf-8'))
out = {}
table = {}
for n in sorted(k for k in rowlines if k != '0081'):
    ys = sorted(rowlines[n])
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read()))
    im.load()
    W, H = im.size
    bands = []
    edges = [0] + ys + [H]
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        if b - a < 45:
            continue  # double-drawn separator
        bands.append((a, b))
    rows = []
    for (a, b) in bands:
        c = im.crop((150, a, W - 150, b))
        c = c.resize((c.size[0] * 3, c.size[1] * 3), Image.LANCZOS)
        c.save(TMP)
        try:
            t = read(TMP, lang='pol', psm=6).strip()
        except Exception:
            t = ''
        m = re.match(r'\s*[lI|]?\s*(\d{1,3})[.)]?\s', t)
        if not m:
            try:
                t2 = read(TMP, lang='pol-std', psm=6).strip()
            except Exception:
                t2 = ''
            if re.match(r'\s*[lI|]?\s*\d{1,3}[.)]?\s', t2):
                t = t2
                m = re.match(r'\s*[lI|]?\s*(\d{1,3})[.)]?\s', t)
        num = int(m.group(1)) if m else None
        rows.append({'y0': a, 'y1': b, 'text': t, 'num': num})
        print('%s band %5d-%5d num=%-4s | %s' %
              (n, a, b, num, re.sub(r'\s+', ' ', t)[:70]))
    out[n] = rows
    # table format for compose
    sheet = {}
    for r in rows:
        if r['num'] is None:
            continue
        text = re.sub(r'\s+', ' ', r['text']).strip()
        # the row's own number is the compose prefix - not part of raw
        text = re.sub(r'^[lI|]?\s*\d{1,3}[.)]?\s*', '', text).strip()
        cells = [c.strip() for c in re.split(r'\s{3,}', text) if c.strip()]
        tier = 'B' if len(cells) >= 2 else 'C'
        sheet[str(r['num'])] = {'tier': tier, 'cells': cells,
                                'raw': text, 'y': [r['y0'], r['y1']]}
    table[n] = sheet
    print('%s: %d bands, %d numbered rows' % (n, len(rows), len(sheet)))

json.dump(out, open(os.path.join(OCR, 'annex_rows.json'), 'w',
                    encoding='utf-8', newline='\n'), ensure_ascii=False)
old = json.load(open(os.path.join(OCR, 'annex_table.json'),
                     encoding='utf-8'))
print()
print('== comparison with the old table ==')
for n in sorted(table):
    on, nn = len(old[n]['rows']), len(table[n])
    od = [k for k in old[n]['rows'] if k != 'h']
    nums_old = sorted(int(k) for k in od)
    nums_new = sorted(int(k) for k in table[n])
    dup_old = len(nums_old) - len(set(nums_old))
    dup_new = len(nums_new) - len(set(nums_new))
    print('%s: rows %d -> %d | dup nums %d -> %d | range %s..%s -> %s..%s'
          % (n, on, nn, dup_old, dup_new,
             nums_old[0] if nums_old else '-', nums_old[-1] if nums_old else '-',
             nums_new[0] if nums_new else '-', nums_new[-1] if nums_new else '-'))
json.dump({'rows': table}, open(os.path.join(OCR, 'annex_table.json'), 'w',
                                encoding='utf-8', newline='\n'),
          ensure_ascii=False)
print('annex_table.json rewritten')
