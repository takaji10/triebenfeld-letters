# -*- coding: utf-8 -*-
"""Parse the ANEKS I rows into their print columns (annex_cells.json).

The print's table (series a, b and c share the layout) has 11 content
columns behind 12 vertical rules:
  1 L.p. | 2 Nazwa osady w okresie rozbiorów | 3 Ówczesna parafia |
  4 Nazwa dzisiejsza | 5 Rok założ. osady | 6 Charakter terenu przed
  założ. osady | 7 Przywilej lub wzmianka - sygn. źródła |
  8 data | 9 L. dymów wg Tp. 89 lub 90 | 10 dymów oblicz./szacunkowo |
  11 Ludn. osad wg Tołł.

Per sheet the rules are detected (near-vertical continuous ink), then
ALWAYS passed through a template fit: every (first, last) pair of
detections is hypothesized to be the template's outer frame, the
interior detections are matched monotonically to the template ladder,
and the least-squares residual ranks the hypotheses. A perfect
detection reproduces itself exactly (residual ~0); sheets with faint,
missing or spurious rules get the missing positions interpolated and
the junk dropped. Each row x column cell is then OCR'd and lightly
cleaned; the tier-C raw row text stays as the cross-check."""
import sys, json, os, io, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode'
                r'\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TMP = os.path.join(OCR, 'cell_tmp.png')
NCOL = 11

# the template rule positions (0139's clean detection; the sheets share
# the print layout at slightly different offsets/scales)
TPL = [795, 992, 1866, 2361, 2916, 3202, 3694, 4190, 4528, 4794,
       5024, 5256]


def detect(n, y_lo, y_hi):
    fn = os.path.join(SRC, 'tom5_%s.tif' % n)
    with open(fn, 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    W, H = im.size
    ys = list(range(y_lo, y_hi, 3))
    n_y = len(ys)
    cols = []
    for x in range(200, W - 10, 2):
        dark = sum(1 for y in ys if px[x, y] < 160)
        if dark > 60 and dark / n_y > 0.25:
            cols.append(x)
    runs = []
    for x in cols:
        if runs and x - runs[-1] <= 20:
            runs[-1] = (runs[-1] + x) // 2
        else:
            runs.append(x)
    return im, runs


def fit(runs):
    """Fit the template ladder to the sheet's detected rules. Returns
    (residual, ladder in pixels) or None if no hypothesis is sane."""
    tn = [(x - TPL[0]) / (TPL[-1] - TPL[0]) for x in TPL]
    best = None
    for i0 in range(len(runs)):
        for i1 in range(i0 + 1, len(runs)):
            span = runs[i1] - runs[i0]
            if span < 3800:
                continue  # cannot be the outer frame at any sane scale
            rn = [(x - runs[i0]) / span for x in runs]
            pairs = []
            j = 0
            for rv in rn:
                while j + 1 < len(tn) and abs(tn[j + 1] - rv) \
                        < abs(tn[j] - rv):
                    j += 1
                if pairs and j <= pairs[-1][0]:
                    if abs(tn[j] - rv) > 0.04:
                        j += 1
                        if j >= len(tn) or abs(tn[j] - rv) > 0.04:
                            continue  # spurious run - skip it
                    else:
                        continue
                pairs.append((tn[j], rv))
            if len(pairs) < 7:
                continue
            n_ = len(pairs)
            st = sum(t for t, _ in pairs)
            sr = sum(r for _, r in pairs)
            stt = sum(t * t for t, _ in pairs)
            str_ = sum(t * r for t, r in pairs)
            den = n_ * stt - st * st
            if abs(den) < 1e-9:
                continue
            scale = (n_ * str_ - st * sr) / den
            off = (sr - scale * st) / n_
            resid = sum(abs(scale * t + off - r)
                        for t, r in pairs) / n_
            cand = (resid, i0, i1, scale, off, len(pairs))
            if best is None or cand[0] < best[0]:
                best = cand
    if best is None or best[0] > 0.02:
        return None
    _, i0, i1, scale, off, npair = best
    span = runs[i1] - runs[i0]
    return best[0], [runs[i0] + (t * scale + off) * span for t in tn]


def ocr_cell(im, x0, x1, y0, y1):
    if x1 - x0 < 12 or y1 - y0 < 14:
        return ''
    c = im.crop((x0, max(0, y0), min(im.size[0], x1),
                 min(im.size[1], y1)))
    c = c.resize((int(c.size[0] * 2), int(c.size[1] * 2)), Image.LANCZOS)
    c.save(TMP)
    try:
        return read(TMP, lang='pol', psm=6).strip()
    except Exception:
        return ''


def clean(txt):
    txt = re.sub(r'[|¦]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt).strip(' .,;:-_=+*')
    return txt


def main():
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    out = {}
    residuals = []
    for n in sorted(at):
        rows = at[n]['rows']
        nums = sorted(int(k) for k in rows if k.isdigit())
        if not nums:
            continue
        y_lo = min(rows[str(k)]['y'][0] for k in nums)
        y_hi = max(rows[str(k)]['y'][1] for k in nums)
        im, runs = detect(n, y_lo, y_hi)
        got = fit(runs)
        if got is None:
            residuals.append((n, 'no sane template fit; %d runs %s'
                              % (len(runs), runs)))
            continue
        resid, rules = got
        if resid > 0.008:
            residuals.append((n, 'resid %.4f runs %s' % (resid, runs)))
        bounds = [rules[0] - 60] + rules + [rules[-1] + 120]
        sheet = {}
        for num in nums:
            y0, y1 = rows[str(num)]['y']
            cells = []
            for i in range(NCOL):
                x0, x1 = bounds[i] + 8, bounds[i + 1] - 8
                raw = ocr_cell(im, x0, x1, y0 + 2, y1 - 2)
                cells.append(clean(raw))
            sheet[str(num)] = {'y': [y0, y1], 'cells': cells,
                               'resid': round(resid, 4)}
        out[n] = sheet
        print(n, 'resid %.4f rules' % resid,
              [int(r) for r in rules], 'rows', len(nums), flush=True)
    with open(os.path.join(OCR, 'annex_cells.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    if residuals:
        print('== residuals ==')
        for r in residuals:
            print(' ', r)


if __name__ == '__main__':
    main()
