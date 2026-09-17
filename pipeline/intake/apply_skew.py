# -*- coding: utf-8 -*-
"""
Straighten pages, at angles placed in the skew review page.

    python pipeline/intake/apply_skew.py --unit oe1bu14525 \
        --angles processed/_skew_review/skew.json
    python pipeline/intake/apply_skew.py --unit oe1bu14525 --undo

The file is {page filename: degrees counter-clockwise}, which is what the review
page saves and what PIL's rotate() takes, so the number is applied as it stands.

The canvas is grown to hold the turned page rather than cropped to the old
rectangle: nothing is lost here, and the wedges this leaves in the corners are
what the trim pass takes off next. They are filled with the page's own border
colour, not white, so the trim edge stays readable.

The unrotated image is kept in processed/_unrotated/, so --undo puts everything
back and a page can always be straightened again from the original rather than
from an already-turned file - turning twice softens the writing for nothing.

The manifest records the angle and the new size. bbox_original still says where
the page sat in its scan, which rotation does not change.
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
MIN_DEG = 0.05             # below this the rotation is not worth the resampling


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


def border_colour(im):
    """The median colour of a strip around the edge - the paper, or the cloth
    the leaf was laid on. Filling the corners with it keeps the new wedges from
    reading as page, which is what a white fill does."""
    w, h = im.size
    band = max(1, min(w, h) // 60)
    px = im.load()
    step = max(1, w // 120)
    sample = []
    for x in range(0, w, step):
        for y in (band, h - band - 1):
            sample.append(px[x, y])
    for y in range(0, h, max(1, h // 120)):
        for x in (band, w - band - 1):
            sample.append(px[x, y])
    if not sample:
        return (255, 255, 255)
    return tuple(sorted(c[i] for c in sample)[len(sample) // 2] for i in range(3))


def apply_one(processed, unrotated, manifest, name, deg, dry_run):
    src = os.path.join(processed, name)
    if not os.path.isfile(src):
        return 'missing'
    if abs(deg) < MIN_DEG:
        return 'nothing'
    if dry_run:
        with Image.open(src) as im:
            print(f'  {name}: would turn {deg:+.2f} deg ({im.width}x{im.height})')
        return 'would'

    # keep the unrotated original once; re-running turns that original again,
    # never the already-turned file
    os.makedirs(unrotated, exist_ok=True)
    keep = os.path.join(unrotated, name)
    if not os.path.isfile(keep):
        shutil.copy2(src, keep)

    with Image.open(keep) as im:
        base = im.convert('RGB')
    w, h = base.size
    out = base.rotate(deg, resample=Image.BICUBIC, expand=True,
                      fillcolor=border_colour(base))
    out.save(src, quality=JPEG_QUALITY)
    nw, nh = out.size

    e = entry_for(manifest, name)
    if e:
        e['rotated'] = round(deg, 2)
        e['size'] = [nw, nh]
    print(f'  {name}: turned {deg:+.2f} deg  {w}x{h} -> {nw}x{nh}')
    return 'done'


def run_undo(processed, unrotated, dry_run):
    if not os.path.isdir(unrotated):
        print('  nothing to undo')
        return
    names = sorted(f for f in os.listdir(unrotated) if f.lower().endswith('.jpg'))
    if not names:
        print('  nothing to undo')
        return
    manifest = load_manifest(processed)
    for name in names:
        if dry_run:
            print(f'  would restore {name}')
            continue
        dst = os.path.join(processed, name)
        shutil.move(os.path.join(unrotated, name), dst)
        e = entry_for(manifest, name)
        if e:
            e.pop('rotated', None)
            with Image.open(dst) as im:
                e['size'] = list(im.size)
        print(f'  restored {name}')
    if not dry_run:
        save_manifest(processed, manifest)
        if not os.listdir(unrotated):
            os.rmdir(unrotated)
    print(f'\n{"(dry run) " if dry_run else ""}restored {len(names)} page(s)')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--angles', metavar='PATH', help='JSON saved by the skew review page')
    ap.add_argument('--undo', action='store_true', help='restore every unrotated page')
    ap.add_argument('--dry-run', action='store_true', help='report only; write nothing')
    a = ap.parse_args()

    if bool(a.angles) == bool(a.undo):
        raise SystemExit('pass either --angles PATH or --undo')

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    unrotated = os.path.join(processed, '_unrotated')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')

    if a.undo:
        run_undo(processed, unrotated, a.dry_run)
        return

    path = a.angles if os.path.isabs(a.angles) else os.path.join(unit.raw_dir, a.angles)
    with open(path, encoding='utf-8') as f:
        angles = {k: float(v) for k, v in json.load(f).items()}

    if os.path.isdir(os.path.join(processed, '_untrimmed')):
        print('  NOTE: pages here have already been trimmed. Straightening after a')
        print('  trim leaves wedges inside the edge you just cut, so the trim has to')
        print('  be done again afterwards.')
        print()

    manifest = load_manifest(processed)
    counts = {}
    for name in sorted(angles):
        r = apply_one(processed, unrotated, manifest, name, angles[name], a.dry_run)
        counts[r] = counts.get(r, 0) + 1
    if not a.dry_run:
        save_manifest(processed, manifest)

    done = counts.get('done', 0) or counts.get('would', 0)
    print(f'\n{"(dry run) " if a.dry_run else ""}straightened {done} page(s)'
          + (f"; {counts['nothing']} already square" if counts.get('nothing') else '')
          + (f"; {counts['missing']} not found" if counts.get('missing') else ''))
    if done and not a.dry_run:
        print('  originals in _unrotated/; --undo restores them')
        print('  run review_trim.py next: the corners now carry wedges to take off')


if __name__ == '__main__':
    main()
