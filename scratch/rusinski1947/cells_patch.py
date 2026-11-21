# -*- coding: utf-8 -*-
"""Re-OCR one sheet's rows within (new) row bands and merge into
annex_cells.json. Used after annex_rows2.py changes a sheet's row
bounds (0159's sub-table override)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annex_cells import detect, fit, ocr_cell, clean, NCOL
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def main():
    n = sys.argv[1]
    nums = [int(a) for a in sys.argv[2:]] or None
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    ac = json.load(open(os.path.join(OCR, 'annex_cells.json'),
                        encoding='utf-8'))
    rows = at[n]['rows']
    all_nums = sorted(int(k) for k in rows if k.isdigit())
    y_lo = min(rows[str(k)]['y'][0] for k in all_nums)
    y_hi = max(rows[str(k)]['y'][1] for k in all_nums)
    im, runs = detect(n, y_lo, y_hi)
    got = fit(runs)
    resid, rules = got
    print(n, 'resid %.4f' % resid, [int(r) for r in rules])
    bounds = rules + [rules[-1] + 120]
    targets = nums if nums else all_nums
    for num in targets:
        y0, y1 = rows[str(num)]['y']
        cells = []
        for i in range(NCOL):
            x0, x1 = bounds[i] + 8, bounds[i + 1] - 8
            raw = ocr_cell(im, x0, x1, y0 + 2, y1 - 2)
            cells.append(clean(raw))
        ac[n][str(num)] = {'y': [y0, y1], 'cells': cells,
                           'resid': round(resid, 4)}
        print(' r%d' % num, cells)
    with open(os.path.join(OCR, 'annex_cells.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(ac, fh, ensure_ascii=False)
    print('merged into annex_cells.json')


if __name__ == '__main__':
    main()
