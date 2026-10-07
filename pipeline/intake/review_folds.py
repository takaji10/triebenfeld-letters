# -*- coding: utf-8 -*-
"""
Build a page for placing fold lines by hand.

    python pipeline/intake/review_folds.py --unit oe1bu14526           # not yet split
    python pipeline/intake/review_folds.py --unit oe1bu14526 --done    # check the splits

Writes processed/_spreads_review/review.html. Open it in a browser, drag the red
line onto each fold, save the JSON it offers, then:

    python pipeline/intake/split_spreads.py --unit oe1bu14526 \
        --apply-folds processed/_spreads_review/folds.json

Default lists openings still waiting. --done lists ones already split, showing
the original with the fold that was used, so an automatic decision can be
checked and moved; folds you placed yourself are left out unless you ask for
them with --include-hand.

Only spreads whose line you actually move are written to the JSON, and moving a
fold on an already-split spread undoes and redoes that split. The page is plain
HTML opened from disk: no server, nothing uploaded.
"""
import argparse
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REVIEW_AR = 1.12
CROP_RE = re.compile(r'^(.*)_([a-h]\d?)$')


def load_json(path, default):
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    return default


def detected_folds(index_path):
    """What the detector proposed, from the review index."""
    out = {}
    if not os.path.isfile(index_path):
        return out
    for line in open(index_path, encoding='utf-8'):
        m = re.match(r'\| (\S.*?) \| \d+x\d+ \| [\d.]+ \| ([\d.]+) \| (\w+) \|', line)
        if m:
            out[m.group(1)] = (float(m.group(2)), m.group(3))
    return out


def fold_from_manifest(manifest, base, suf):
    for entries in manifest.values():
        halves = [e for e in entries
                  if e['file'] in (f'{base}_{suf}1.jpg', f'{base}_{suf}2.jpg')]
        if len(halves) == 2:
            halves.sort(key=lambda e: e['bbox_original'][0])
            x0 = halves[0]['bbox_original'][0]
            x1 = halves[1]['bbox_original'][2]
            cut = halves[0]['bbox_original'][2]
            if x1 > x0:
                return (cut - x0) / (x1 - x0)
    return None


def collect(processed, review, done, include_hand):
    from PIL import Image
    proposed = detected_folds(os.path.join(review, 'INDEX.md'))
    hand = load_json(os.path.join(review, 'hand_placed.json'), {})
    manifest = load_json(os.path.join(processed, 'manifest.json'), {})
    unsplit_dir = os.path.join(processed, '_spreads_unsplit')

    items = []
    if done:
        if not os.path.isdir(unsplit_dir):
            return items
        for fn in sorted(os.listdir(unsplit_dir)):
            if not fn.lower().endswith('.jpg'):
                continue
            if fn in hand and not include_hand:
                continue
            m = CROP_RE.match(os.path.splitext(fn)[0])
            if not m:
                continue
            with Image.open(os.path.join(unsplit_dir, fn)) as im:
                w, h = im.size
            fold = fold_from_manifest(manifest, m.group(1), m.group(2))
            det, conf = proposed.get(fn, (None, 'auto'))
            items.append({'file': fn, 'src': '../_spreads_unsplit/' + fn,
                          'w': w, 'h': h,
                          'fold': round(fold if fold is not None else det or 0.5, 4),
                          'conf': ('by hand' if fn in hand else conf),
                          'state': 'split'})
        return items

    for fn in sorted(os.listdir(processed)):
        if not fn.lower().endswith('.jpg'):
            continue
        stem = os.path.splitext(fn)[0]
        m = CROP_RE.match(stem)
        if not m or os.path.isfile(os.path.join(processed, f'{stem}1.jpg')):
            continue
        with Image.open(os.path.join(processed, fn)) as im:
            w, h = im.size
        if w / h < REVIEW_AR:
            continue
        fold, conf = proposed.get(fn, (0.5, 'none'))
        items.append({'file': fn, 'src': '../' + fn, 'w': w, 'h': h,
                      'fold': fold, 'conf': conf, 'state': 'waiting'})
    return items


# The page itself is in fold_page.py, which the court-book holdings use too
# (courtbook.fold_sheet), so that the editor has one fold page and not two.
import fold_page  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--done', action='store_true',
                    help='review spreads already split, rather than ones still waiting')
    ap.add_argument('--include-hand', action='store_true',
                    help='with --done, also list folds you placed yourself')
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    review = os.path.join(processed, '_spreads_review')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(review, exist_ok=True)

    items = collect(processed, review, a.done, a.include_hand)
    if not items:
        print(f'  {unit.slug}: nothing to show'
              + (' - no splits recorded' if a.done else ' - every opening is split'))
        return

    out = os.path.join(review, 'review.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fold_page.render(unit.slug, items, save='folds.json', key='folds:' + unit.slug))

    hand = len([x for x in items if x['conf'] == 'by hand'])
    print(f'  {len(items)} spread(s) to look at'
          + (f' ({hand} of them placed by hand)' if hand else ''))
    print(f'  wrote {out}')
    print()
    print('  Red line is where the cut will go; blue is where it is now.')
    print('  Only spreads you actually move are saved. Then run:')
    print(f'    python pipeline/intake/split_spreads.py --unit {unit.slug} \\')
    print('        --apply-folds processed/_spreads_review/folds.json')


if __name__ == '__main__':
    main()
