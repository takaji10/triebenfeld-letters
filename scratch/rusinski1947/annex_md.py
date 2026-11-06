# -*- coding: utf-8 -*-
"""Build annex_md.json: the ANEKS I rows as cleaned per-column cells
ready for Markdown table rendering.

Each cell is classified against the print's pixels first: EMPTY (no
ink), DASH (only dash-stroke ink: a long thin horizontal run), or TEXT
(else - keep the OCR text, cleaned). This kills the junk the OCR
produces on the dim dash cells ('Sz=—=—'). Text cleanup: rule-pipe
artifacts removed, hyphen-wrapped words joined, punctuation-run tokens
dropped, whitespace collapsed."""
import sys, json, os, io, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annex_cells import detect, fit
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def classify(px, x0, x1, y0, y1):
    w, h = x1 - x0, y1 - y0
    if w < 10 or h < 10:
        return 'empty', 0
    ink = [(x, y) for y in range(y0, y1) for x in range(x0, x1, 1)
           if px[x, y] < 160]
    n = len(ink)
    if n < 15:
        return 'empty', n
    xs = sorted(set(x for x, _ in ink))
    xext = xs[-1] - xs[0] + 1
    ys = sorted(set(y for _, y in ink))
    yext = ys[-1] - ys[0] + 1
    # the print's dash: ~70px wide, ~8px tall (measured on 0139's
    # dash cells); two dashes side by side stay within the envelope
    if xext >= 38 and yext <= 20 and n <= 1100:
        return 'dash', n
    return 'text', n


def clean(txt):
    if not txt:
        return ''
    t = txt.replace('|', ' ').replace('¦', ' ')
    t = t.replace('\n', ' ')
    # hyphen-wrapped words
    t = re.sub(r'([a-ząćęłńóśźż])- ([a-ząćęłńóśźż])', r'\1\2', t)
    toks = []
    for tok in t.split(' '):
        core = tok.strip(' .,;:!?()[]')
        if core and re.fullmatch(r'[=_\-—~·.]+', core):
            continue  # a dash/punct run the pixel pass will decide on
        toks.append(tok)
    t = ' '.join(toks)
    t = re.sub(r'\s+', ' ', t).strip(' .,;:-_=+*')
    return t


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    ac = json.load(open(os.path.join(OCR, 'annex_cells.json'),
                        encoding='utf-8'))
    out = {}
    stats = {'empty': 0, 'dash': 0, 'text': 0}
    for n in sorted(ac):
        rows = at[n]['rows']
        nums = sorted(int(k) for k in rows if k.isdigit())
        y_lo = min(rows[str(k)]['y'][0] for k in nums)
        y_hi = max(rows[str(k)]['y'][1] for k in nums)
        im, runs = detect(n, y_lo, y_hi)
        got = fit(runs)
        rules = got[1] if got else runs
        px = im.load()
        bounds = rules + [rules[-1] + 120]
        sheet = {'rows': [], 'furniture': []}
        for num in nums:
            y0, y1 = rows[str(num)]['y']
            cells = []
            for i in range(11):
                x0, x1 = int(bounds[i]) + 8, int(bounds[i + 1]) - 8
                kind, nink = classify(px, x0 + 4, x1 - 4, y0 + 4, y1 - 4)
                stats[kind] += 1
                if kind == 'empty':
                    cells.append('')
                elif kind == 'dash':
                    cells.append('—')
                else:
                    ocr = ac[n][str(num)]['cells'][i]
                    cells.append(clean(ocr))
            sheet['rows'].append({'num': num, 'y': [y0, y1],
                                  'cells': cells})
        for k in sorted(rows):
            if not k.isdigit():
                raw = rows[k].get('raw') or ''
                raw = re.sub(r'\s*\|\s*', ' ', raw).strip(' |')
                fy = rows[k].get('y') or [10 ** 9, 10 ** 9]
                sheet['furniture'].append({'key': k, 'y': fy,
                                           'text': raw})
        out[n] = sheet
        print(n, 'rows', len(nums), flush=True)
    with open(os.path.join(OCR, 'annex_md.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('cell classes:', stats)


if __name__ == '__main__':
    main()
