# -*- coding: utf-8 -*-
"""Render the machine's column-rule decisions over downscaled sheet
images (RULES_SHEET.html) for the editor's eyeball check. Red lines =
the rules the splitter will cut at; the sheet caption reports the
template-fit residual and any unconfirmed positions."""
import json, os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode'
                r'\worktree\14ffba\rusinski1947')
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, '..', '..', 'literature', 'rusinski1947',
                      'annex_checks')
SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TPL = [795, 992, 1866, 2361, 2916, 3202, 3694, 4190, 4528, 4794,
       5024, 5256]

SCALE = 3.2  # 5936 -> ~1855 px wide


def main():
    sys.path.insert(0, HERE)
    from annex_cells import detect, fit
    os.makedirs(OUTDIR, exist_ok=True)
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    parts = ['<!doctype html><meta charset="utf-8">',
             '<title>ANEKS I - column rules check</title>',
             '<style>body{font-family:consolas;background:#222;'
             'color:#ddd}figure{margin:8px 0}img{width:100%%;'
             'image-rendering:auto}figcaption{color:#9cf}</style>',
             '<h1>Column-rule check - flag only the wrong sheets</h1>']
    for n in sorted(at):
        rows = at[n]['rows']
        nums = sorted(int(k) for k in rows if k.isdigit())
        if not nums:
            continue
        y_lo = min(rows[str(k)]['y'][0] for k in nums)
        y_hi = max(rows[str(k)]['y'][1] for k in nums)
        im, runs = detect(n, y_lo, y_hi)
        got = fit(runs)
        if got:
            resid, rules = got
            src_txt = 'fitted (resid %.4f)' % resid
        else:
            rules = runs
            src_txt = 'RAW detection (no fit!)'
        # the drawn image: full sheet downscaled, red rules, green row
        # bounds for context
        small = im.resize((int(im.size[0] / SCALE),
                           int(im.size[1] / SCALE)), Image.LANCZOS)
        small = small.convert('RGB')
        d = ImageDraw.Draw(small)
        for r in rules:
            x = r / SCALE
            d.line([(x, 0), (x, small.size[1])], fill=(255, 60, 60),
                   width=2)
        for num in nums:
            y0, y1 = rows[str(num)]['y']
            d.line([(0, y0 / SCALE), (small.size[0], y0 / SCALE)],
                   fill=(60, 200, 60), width=1)
        jpg = os.path.join(OUTDIR, 'rules_%s.jpg' % n)
        small.convert('RGB').save(jpg, quality=72)
        parts.append(
            '<figure><figcaption>%s - %d rows, rules from %s'
            ' - unconfirmed: %s</figcaption>'
            '<img src="annex_checks/rules_%s.jpg"></figure>'
            % (n, len(nums), src_txt,
               [i for i, r in enumerate(rules)
                if not any(abs(r - d) <= 25 for d in runs)] or 'none',
               n))
    html = os.path.join(HERE, '..', '..', 'literature', 'rusinski1947',
                        'RULES_SHEET.html')
    with open(html, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(parts))
    print('written', os.path.abspath(html))


if __name__ == '__main__':
    main()
