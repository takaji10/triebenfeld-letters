# -*- coding: utf-8 -*-
"""
Trim the head and the tail off pages, at lines placed in the head/tail page.

    python pipeline/intake/apply_headtail.py --unit oe1bu14525 \
        --cuts processed/_headtail_review/headtail.json
    python pipeline/intake/apply_headtail.py --unit oe1bu14525 --undo

The file is {page filename: [top, bottom]} as fractions of the height, which is
what the review page saves. Everything above top and below bottom goes, in one
pass, because a short leaf shows a band at both ends and they are independent.

Originals are kept in processed/_pre_headtail/ - a folder of its own, not the
_untrimmed/ that apply_trims.py uses, so that undoing one of the two trims does
not silently undo the other.

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
MIN_PX = 2                 # a line this close to the end means no cut there


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


def apply_one(processed, kept_dir, manifest, name, top, bottom, dry_run):
    src = os.path.join(processed, name)
    if not os.path.isfile(src):
        return 'missing'
    with Image.open(src) as im:
        w, h = im.size
        y0 = int(round(top * h))
        y1 = int(round(bottom * h))
        head, tail = y0, h - y1
        if head < MIN_PX and tail < MIN_PX:
            return 'nothing'
        if y1 - y0 < h // 10:
            print(f'  {name}: lines leave only {y1 - y0}px of {h}, skipping')
            return 'refused'
        if dry_run:
            print(f'  {name}: would cut head {head}px, tail {tail}px '
                  f'({w}x{h} -> {w}x{y1 - y0})')
            return 'would'
        # keep the untrimmed original once; a second pass cuts the cut file, but
        # the original stays the one in _pre_headtail/
        os.makedirs(kept_dir, exist_ok=True)
        keep = os.path.join(kept_dir, name)
        if not os.path.isfile(keep):
            shutil.copy2(src, keep)
        out = im.convert('RGB').crop((0, y0, w, y1))
        out.save(src, quality=JPEG_QUALITY)

    e = entry_for(manifest, name)
    if e and len(e.get('bbox_original', [])) == 4:
        x0, oy0, x1, oy1 = e['bbox_original']
        scale = (oy1 - oy0) / h if h else 1
        e['bbox_original'] = [x0, round(oy0 + y0 * scale), x1, round(oy0 + y1 * scale)]
        e['size'] = [w, y1 - y0]
        e['headtail'] = [head, tail]
    print(f'  {name}: cut head {head}px, tail {tail}px -> {w}x{y1 - y0}')
    return 'done'


def run_undo(processed, kept_dir, dry_run):
    if not os.path.isdir(kept_dir):
        print('  nothing to undo')
        return
    names = sorted(f for f in os.listdir(kept_dir) if f.lower().endswith('.jpg'))
    if not names:
        print('  nothing to undo')
        return
    manifest = load_manifest(processed)
    for name in names:
        if dry_run:
            print(f'  would restore {name}')
            continue
        dst = os.path.join(processed, name)
        shutil.move(os.path.join(kept_dir, name), dst)
        e = entry_for(manifest, name)
        if e:
            e.pop('headtail', None)
            with Image.open(dst) as im:
                e['size'] = list(im.size)
        print(f'  restored {name}')
    if not dry_run:
        save_manifest(processed, manifest)
        if not os.listdir(kept_dir):
            os.rmdir(kept_dir)
    print(f'\n{"(dry run) " if dry_run else ""}restored {len(names)} page(s); '
          'their manifest boxes are stale until the next build')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--cuts', metavar='PATH', help='JSON saved by the head/tail review page')
    ap.add_argument('--undo', action='store_true', help='restore every page to full height')
    ap.add_argument('--dry-run', action='store_true', help='report only; write nothing')
    a = ap.parse_args()

    if bool(a.cuts) == bool(a.undo):
        raise SystemExit('pass either --cuts PATH or --undo')

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    kept_dir = os.path.join(processed, '_pre_headtail')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')

    if a.undo:
        run_undo(processed, kept_dir, a.dry_run)
        return

    path = a.cuts if os.path.isabs(a.cuts) else os.path.join(unit.raw_dir, a.cuts)
    with open(path, encoding='utf-8') as f:
        cuts = json.load(f)

    manifest = load_manifest(processed)
    counts = {}
    for name in sorted(cuts):
        pair = cuts[name]
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            print(f'  {name}: expected [top, bottom], got {pair!r}, skipping')
            counts['bad'] = counts.get('bad', 0) + 1
            continue
        r = apply_one(processed, kept_dir, manifest, name,
                      float(pair[0]), float(pair[1]), a.dry_run)
        counts[r] = counts.get(r, 0) + 1
    if not a.dry_run:
        save_manifest(processed, manifest)

    done = counts.get('done', 0) or counts.get('would', 0)
    print(f'\n{"(dry run) " if a.dry_run else ""}trimmed {done} page(s)'
          + (f"; {counts['nothing']} left at full height" if counts.get('nothing') else '')
          + (f"; {counts['refused']} refused as too deep" if counts.get('refused') else '')
          + (f"; {counts['missing']} not found" if counts.get('missing') else ''))
    if done and not a.dry_run:
        print(f'  originals kept in processed/_pre_headtail/ - --undo restores them')


if __name__ == '__main__':
    main()
