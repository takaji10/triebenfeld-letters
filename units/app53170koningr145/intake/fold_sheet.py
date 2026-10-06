# -*- coding: utf-8 -*-
"""A sheet for the editor to approve the folds of APP 53/17/0/-/Konin Gr.145.

    python units/app53170koningr145/intake/fold_sheet.py

Writes review/app53170koningr145/folds/index.html and one picture per scan:
the whole opening with the fold drawn in red, the strip each page keeps beyond
it shaded, and each half marked as a page of the edition or as left out. The
editor looks for a red line that crosses writing, and for a half that is
marked wrongly, and says which scans to move. The folds are in build_pages.py.

The editor's rule (2026-10-06): pages are whole pages cut at the fold, and the
editor approves the folds before a holding is published. The same sheet is to
be made for every court book that is cut.
"""
import html
import io
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_pages as B  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(ROOT, 'review', 'app53170koningr145', 'folds')
WIDTH = 1500


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for n in range(B.FIRST, B.LAST + 1):
        im = Image.open(os.path.join(B.RAW, '%d.jpg' % n)).convert('RGB')
        x = B.FOLDS[n]
        d = ImageDraw.Draw(im, 'RGBA')
        d.rectangle([x - B.OVERLAP, 0, x + B.OVERLAP, im.height], fill=(255, 0, 0, 40))
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0, 255), width=5)
        k = WIDTH / im.width
        im = im.resize((WIDTH, int(im.height * k)), Image.LANCZOS)
        name = '%d.jpg' % n
        im.save(os.path.join(OUT, name), quality=80)
        left, right = '%04d_a1' % n, '%04d_a2' % n
        say = lambda pid: 'left out' if pid in B.SKIP else 'page of the edition'
        rows.append('<section><h2>Scan %d</h2><p>Left half (leaf %d verso): <b>%s</b>. Right half (leaf %d recto): <b>%s</b>. '
                    'Fold at %d of %d pixels.</p><img src="%s" alt="scan %d" loading="lazy"></section>'
                    % (n, n - 1, say(left), n, say(right), x, int(WIDTH / k), html.escape(name), n))
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Folds: APP 53/17/0/-/Konin Gr.145</title>'
            '<style>body{font:16px/1.5 Georgia,serif;max-width:1540px;margin:2em auto;padding:0 16px;background:#fbfaf7;color:#222}'
            'img{width:100%%;border:1px solid #ccc}section{margin:2.5em 0}h2{margin:0 0 .2em}</style>'
            '<h1>Folds: APP 53/17/0/-/Konin Gr.145</h1>'
            '<p>%d scans, each cut at the red line into two pages. Each page also keeps the shaded strip beyond the line, '
            'so a line of writing that runs into the fold stays whole. Please look for a red line that crosses writing, '
            'and for a half marked wrongly as a page or as left out, and tell me the scan numbers.</p>%s</html>'
            % (len(rows), '\n'.join(rows)))
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.join(OUT, 'index.html'), 'with', len(rows), 'scans')


if __name__ == '__main__':
    main()
