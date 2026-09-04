# -*- coding: utf-8 -*-
"""
Produce web-sized copies of the page scans for the site.

The originals in pages/ are ~1.08 GB, far past what GitHub Pages will host, so
the site uses downscaled copies in site/assets/scans/. The originals are never
modified and never published - they stay local as the archival master.

Width is 1100px: enough to read Kurrentschrift comfortably, and about 250 MB in
total. Re-running skips anything already made and up to date, so it is cheap to
call after adding or renaming a few images.

    python3 make_scan_derivatives.py           # make what's missing
    python3 make_scan_derivatives.py --force   # rebuild everything
    python3 make_scan_derivatives.py --prune   # also delete orphans
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, time
from PIL import Image
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'pages')
DST = os.path.join(ROOT, 'site', 'assets', 'scans')

WIDTH = 1100
QUALITY = 78

FORCE = '--force' in sys.argv
PRUNE = '--prune' in sys.argv


def main():
    os.makedirs(DST, exist_ok=True)
    srcs = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.jpg'))
    made = skipped = 0
    t0 = time.time()

    for n, f in enumerate(srcs, 1):
        sp, dp = os.path.join(SRC, f), os.path.join(DST, f)
        if not FORCE and os.path.isfile(dp) and os.path.getmtime(dp) >= os.path.getmtime(sp):
            skipped += 1
            continue
        with Image.open(sp) as im:
            # draft() lets the JPEG decoder downscale while reading - much faster
            # than decoding at full size and resizing afterwards.
            im.draft('RGB', (WIDTH * 2, WIDTH * 2))
            im = im.convert('RGB')
            im.thumbnail((WIDTH, WIDTH * 4), Image.LANCZOS)
            im.save(dp, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        made += 1
        if made % 100 == 0:
            print(f'  {n}/{len(srcs)}  ({time.time() - t0:.0f}s)')

    orphans = [f for f in os.listdir(DST)
               if f.lower().endswith('.jpg') and f not in set(srcs)]
    if orphans:
        if PRUNE:
            for f in orphans:
                os.remove(os.path.join(DST, f))
            print(f'pruned {len(orphans)} derivative(s) with no original')
        else:
            print(f'NOTE: {len(orphans)} derivative(s) have no original '
                  f'(run with --prune to remove): {orphans[:3]}')

    total = sum(os.path.getsize(os.path.join(DST, f))
                for f in os.listdir(DST) if f.lower().endswith('.jpg'))
    print(f'\nderivatives: {made} made, {skipped} already current')
    print(f'total size : {total / 1024 / 1024:.0f} MB at {WIDTH}px wide')
    print(f'took       : {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
