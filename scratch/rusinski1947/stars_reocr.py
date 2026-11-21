# -*- coding: utf-8 -*-
"""Re-OCR the rows whose cells carry the print's '*' markers (the body
p. 23-24: dymy given 'zbiorowo' in Tp. 89), so the star survives into
annex_md.json (clean() now preserves a trailing star). Idempotent for
unchanged row bands."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annex_cells import detect, fit, ocr_cell, clean, NCOL
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

ROWS = {
    '0139': [9],
    '0140': [21, 26],
    '0141': [36],
    '0142': [48, 54],
    '0144': [77, 78],
    '0146': [102],
    '0147': [1, 12],
    '0148': [15, 17, 22, 24],
    '0149': [44, 47, 48],
    '0150': [62],
    '0151': [74, 75, 77, 78, 79],
    '0152': [82, 83, 84, 85, 87, 91],
    '0153': [103],
    '0154': [106, 107, 110, 111, 113],
    '0155': [119, 123, 127],
    '0159': [1, 3],
}


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    ac = json.load(open(os.path.join(OCR, 'annex_cells.json'),
                        encoding='utf-8'))
    for n, nums in ROWS.items():
        rows = at[n]['rows']
        all_nums = sorted(int(k) for k in rows if k.isdigit())
        y_lo = min(rows[str(k)]['y'][0] for k in all_nums)
        y_hi = max(rows[str(k)]['y'][1] for k in all_nums)
        im, runs = detect(n, y_lo, y_hi)
        got = fit(runs)
        resid, rules = got
        bounds = rules + [rules[-1] + 120]
        for num in nums:
            y0, y1 = rows[str(num)]['y']
            cells = []
            for i in range(NCOL):
                x0, x1 = bounds[i] + 8, bounds[i + 1] - 8
                cells.append(clean(ocr_cell(im, x0, x1, y0 + 2, y1 - 2)))
            ac[n][str(num)] = {'y': [y0, y1], 'cells': cells,
                               'resid': round(resid, 4)}
            star_cols = [i for i, c in enumerate(cells) if '*' in c]
            print(n, 'r%d stars in cells %s' % (num, star_cols), flush=True)
    with open(os.path.join(OCR, 'annex_cells.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(ac, fh, ensure_ascii=False)
    print('done')


if __name__ == '__main__':
    main()
