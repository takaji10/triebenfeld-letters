# -*- coding: utf-8 -*-
"""
Trim the edge off pages, at lines placed in the trim review page.

    python pipeline/intake/apply_trims.py --unit oe1bu14526 \
        --trims processed/_trim_review/trims.json
    python pipeline/intake/apply_trims.py --unit oe1bu14526 --undo

The file is {page filename: fraction of width}. Whichever side of that line is
smaller is removed, which is what the review page shades. The untrimmed image
is kept in processed/_untrimmed/, so --undo puts everything back and a trim can
always be redone from the original rather than from an already-trimmed file.

The manifest is updated so each page still records where it sits in its scan.
"""
import argparse
import io
import json
import os
import shutil
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

JPEG_QUALITY = 97
MIN_PX = 2                 # a line this close to the edge means no trim


def load_manifest(processed):
    p = os.path.join(processed, 'manifest.json')
    if os.path.isfile(p):
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_manifest(processed, manifest):
    with open(os.path.join(processed, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


def entry_for(manifest, name):
    for entries in manifest.values():
        for e in entries:
            if e.get('file') == name:
                return e
    return None


def apply_one(processed, untrimmed, manifest, name, frac, dry_run):
    src = os.path.join(processed, name)
    if not os.path.isfile(src):
        return 'missing'
    with Image.open(src) as im:
        w, h = im.size
        left = frac < 0.5
        x = int(round(frac * w))
        cut_px = x if left else w - x
        if cut_px < MIN_PX:
            return 'nothing'
        if left:
            box = (x, 0, w, h)
        else:
            box = (0, 0, x, h)
        if dry_run:
            print(f'  {name}: would cut {"left" if left else "right"} {cut_px}px '
                  f'({w}x{h} -> {box[2]-box[0]}x{h})')
            return 'would'
        # keep the untrimmed original once; a second pass trims the trimmed file
        # but the original stays the one in _untrimmed/
        os.makedirs(untrimmed, exist_ok=True)
        keep = os.path.join(untrimmed, name)
        if not os.path.isfile(keep):
            shutil.copy2(src, keep)
        out = im.convert('RGB').crop(box)
        out.save(src, quality=JPEG_QUALITY)

    e = entry_for(manifest, name)
    if e and len(e.get('bbox_original', [])) == 4:
        x0, y0, x1, y1 = e['bbox_original']
        scale = (x1 - x0) / w if w else 1
        if left:
            e['bbox_original'] = [round(x0 + x * scale), y0, x1, y1]
        else:
            e['bbox_original'] = [x0, y0, round(x0 + x * scale), y1]
        e['size'] = [box[2] - box[0], h]
        e['trimmed'] = ('left' if left else 'right')
    print(f'  {name}: cut {"left" if left else "right"} {cut_px}px '
          f'-> {box[2]-box[0]}x{h}')
    return 'done'


def run_undo(processed, untrimmed, dry_run):
    if not os.path.isdir(untrimmed):
        print('  nothing to undo')
        return
    names = sorted(f for f in os.listdir(untrimmed) if f.lower().endswith('.jpg'))
    if not names:
        print('  nothing to undo')
        return
    manifest = load_manifest(processed)
    for name in names:
        if dry_run:
            print(f'  would restore {name}')
            continue
        shutil.move(os.path.join(untrimmed, name), os.path.join(processed, name))
        e = entry_for(manifest, name)
        if e:
            e.pop('trimmed', None)
        print(f'  restored {name}')
    if not dry_run:
        save_manifest(processed, manifest)
        if not os.listdir(untrimmed):
            os.rmdir(untrimmed)
    print(f'\n{"(dry run) " if dry_run else ""}restored {len(names)} page(s); '
          'their manifest boxes are stale until the next build')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--trims', metavar='PATH', help='JSON saved by the trim review page')
    ap.add_argument('--undo', action='store_true', help='restore every untrimmed page')
    ap.add_argument('--dry-run', action='store_true', help='report only; write nothing')
    a = ap.parse_args()

    if bool(a.trims) == bool(a.undo):
        raise SystemExit('pass either --trims PATH or --undo')

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    untrimmed = os.path.join(processed, '_untrimmed')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')

    if a.undo:
        run_undo(processed, untrimmed, a.dry_run)
        return

    path = a.trims if os.path.isabs(a.trims) else os.path.join(unit.raw_dir, a.trims)
    with open(path, encoding='utf-8') as f:
        trims = {k: float(v) for k, v in json.load(f).items()}

    manifest = load_manifest(processed)
    counts = {}
    for name in sorted(trims):
        r = apply_one(processed, untrimmed, manifest, name, trims[name], a.dry_run)
        counts[r] = counts.get(r, 0) + 1
    if not a.dry_run:
        save_manifest(processed, manifest)

    done = counts.get('done', 0) or counts.get('would', 0)
    print(f'\n{"(dry run) " if a.dry_run else ""}trimmed {done} page(s)'
          + (f"; {counts['missing']} not found" if counts.get('missing') else '')
          + (f"; {counts['nothing']} had nothing to cut" if counts.get('nothing') else ''))
    if not a.dry_run and done:
        print('  originals kept in processed/_untrimmed/ - apply_trims.py --undo restores them')


if __name__ == '__main__':
    main()
