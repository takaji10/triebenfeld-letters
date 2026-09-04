# -*- coding: utf-8 -*-
"""
Keep the descriptive part of each scan filename in step with the mapping.

Filenames look like:

    Oe_1_Bu_9454_0343_a1-L179a_04.jpg
    <---- archival identity ---->|<- derived label ->

The left half (signature, capture, crop) is stable and identifies the physical
image. The label after the hyphen is a convenience, derived from
page_scan_map.csv - so it goes stale the moment the mapping changes. This script
recomputes it, which makes the label safe to rely on rather than a snapshot of
whatever the mapping happened to be when the files were last renamed.

It renames the originals in pages/, updates scan_decisions.json and
scan_rename_map.json to match, and prunes derivatives whose names have changed.

    python3 relabel_scans.py            # report only
    python3 relabel_scans.py --apply    # actually rename
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json
from collections import Counter
import unitlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
PAGES = os.path.join(ROOT, 'pages')
DERIV = os.path.join(ROOT, 'site', 'assets', 'scans')
MAP = os.path.join(UNIT.dir, 'page_scan_map.csv')
DECISIONS = os.path.join(UNIT.dir, 'scan_decisions.json')
RENAME_MAP = os.path.join(UNIT.dir, 'scan_rename_map.json')

STEM = re.compile(r'^(Oe_1_Bu_9454_\d{4}_[a-h]\d?)(?:-[^.]*)?\.jpg$')
SUFFIX = {'front_matter': 'front', 'dropped': 'notapage',
          'image_no_text': 'notext', 'beyond_last_page': 'unplaced'}

APPLY = '--apply' in sys.argv


def main():
    rows = list(csv.DictReader(open(MAP, encoding='utf-8-sig')))
    want = {}
    for r in rows:
        img = r['image']
        if not img:
            continue
        m = STEM.match(img)
        if not m:
            print(f'  cannot parse: {img}')
            continue
        if r['letter'] and r['page']:
            label = f"L{r['letter']}_{int(r['page']):02d}"
        else:
            label = SUFFIX.get(r['status'], 'unplaced')
        want[img] = f'{m.group(1)}-{label}.jpg'

    on_disk = {f for f in os.listdir(PAGES) if f.lower().endswith('.jpg')}
    missing = on_disk - set(want)
    if missing:
        print(f'  {len(missing)} file(s) in pages/ are absent from the mapping: '
              f'{sorted(missing)[:3]}')

    changes = {a: b for a, b in want.items() if a != b and a in on_disk}
    clash = [k for k, v in Counter(want.values()).items() if v > 1]

    print(f'images in mapping : {len(want)}')
    print(f'labels to update  : {len(changes)}')
    print(f'name collisions   : {len(clash)} {clash[:3]}')
    if not changes:
        print('\nnothing to do - every label already matches the mapping.')
        return
    if clash:
        print('\nrefusing to rename while names would collide.')
        sys.exit(1)
    for a, b in list(changes.items())[:5]:
        print(f'   {a}\n     -> {b}')
    if not APPLY:
        print(f'\n(report only - re-run with --apply to rename {len(changes)} files)')
        return

    # Two-phase, so a new name can never overwrite a file still to be renamed.
    tmp = {}
    for i, a in enumerate(changes):
        t = f'__rl_{i:04d}.jpg'
        os.rename(os.path.join(PAGES, a), os.path.join(PAGES, t))
        tmp[t] = changes[a]
    for t, b in tmp.items():
        os.rename(os.path.join(PAGES, t), os.path.join(PAGES, b))
    print(f'\nrenamed {len(changes)} file(s)')

    # Carry the decisions and the original-name record across.
    if os.path.isfile(DECISIONS):
        d = json.load(open(DECISIONS, encoding='utf-8'))
        conv = lambda x: changes.get(x, x)
        for k in ('front_matter', 'dropped', 'image_no_text', 'image_order'):
            d[k] = [conv(f) for f in d.get(k, [])]
        d['notes'] = {conv(k): v for k, v in d.get('notes', {}).items()}
        json.dump(d, open(DECISIONS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('updated scan_decisions.json')

    if os.path.isfile(RENAME_MAP):
        m = json.load(open(RENAME_MAP, encoding='utf-8'))
        json.dump({orig: changes.get(cur, cur) for orig, cur in m.items()},
                  open(RENAME_MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('updated scan_rename_map.json (originals -> current names)')

    if os.path.isdir(DERIV):
        gone = [f for f in os.listdir(DERIV)
                if f.lower().endswith('.jpg') and f not in set(want.values())]
        for f in gone:
            os.remove(os.path.join(DERIV, f))
        print(f'pruned {len(gone)} stale derivative(s) - '
              f'run make_scan_derivatives.py to rebuild them')


if __name__ == '__main__':
    main()
