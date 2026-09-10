# -*- coding: utf-8 -*-
"""
Bring a unit's cropped pages into pages/ under the project's naming rules.

    python pipeline/intake/stage_pages.py --unit oe1bu14526
    python pipeline/intake/stage_pages.py --unit oe1bu14526 --dry-run
    python pipeline/intake/stage_pages.py --unit oe1bu14526 --prune

The intake scripts leave their output in <raw_dir>/processed/, named the way the
archive named the scans: spaces, umlauts and all. Everything downstream reads
pages/ instead and parses the filename, so the name has to be ASCII and has to
start with the unit's ascii_prefix:

    Oe 1_Bü 14526_0011_a1.jpg   ->   pages/Oe_1_Bu_14526_0011_a1.jpg

That prefix is what scopes a build to its own images - pages/ is one flat folder
shared by every holding - so it is taken from unit.yml and never guessed.

The capture and crop (0011_a1) are the page's archival identity and are carried
through untouched. relabel_scans.py may later append a -L<doc>_<page> label; a
page already staged is recognised by its identity, label or no label, so this is
safe to re-run and will not undo a relabelling.

units/<slug>/scan_rename_map.json records original name -> staged name, so the
move is always reversible and a page can be traced back to the file the archive
sent. It is also what makes a re-run safe: once a unit has been staged, a source
image that the map does not mention was left out on purpose - a blank leaf, or a
page dropped during review - and is reported rather than quietly restored.
Staging one of those anyway needs --force.
"""
import argparse
import io
import json
import os
import shutil
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')


def raw_stem(unit):
    """The literal part of raw_glob before the wildcard: 'Oe 1_Bü 14526_'."""
    glob = unit.raw_glob
    if '*' not in glob:
        raise SystemExit(f'{unit.slug}: scans.raw_glob has no wildcard: {glob!r}')
    return glob.split('*', 1)[0]


def ascii_fold(s):
    """'Bü' -> 'Bu'. Anything else outside ASCII becomes an underscore."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return ''.join(c if (c.isalnum() or c in '._-') else '_' for c in s)


def staged_name(unit, source_name, stem):
    """Source basename -> the name it takes in pages/, or None if off-pattern."""
    if not source_name.startswith(stem):
        return None
    rest = ascii_fold(source_name[len(stem):])
    return f'{unit.ascii_prefix}_{rest}' if rest else None


def identity_of(unit, staged):
    """'Oe_1_Bu_14526_0011_a1-L7_03.jpg' -> '0011_a1'. The part that never moves."""
    head = unit.ascii_prefix + '_'
    if not staged.startswith(head) or not staged.lower().endswith('.jpg'):
        return None
    body = staged[len(head):-4]
    return body.split('-', 1)[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--dry-run', action='store_true', help='report only; write nothing')
    ap.add_argument('--force', action='store_true', help='re-copy pages already staged')
    ap.add_argument('--prune', action='store_true',
                    help='also delete staged pages whose source is gone')
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(PAGES, exist_ok=True)

    stem = raw_stem(unit)
    sources = sorted(f for f in os.listdir(processed)
                     if f.lower().endswith('.jpg')
                     and os.path.isfile(os.path.join(processed, f)))
    if not sources:
        raise SystemExit(f'{unit.slug}: no page images in {processed}')

    # What this unit already has in pages/, by archival identity, so a page that
    # has since been relabelled is still recognised as the same page.
    existing = {}
    for f in os.listdir(PAGES):
        if f.lower().endswith('.jpg'):
            ident = identity_of(unit, f)
            if ident:
                existing[ident] = f

    # The provenance record doubles as the list of pages this unit has decided
    # to carry. Its absence means the unit has never been staged.
    map_path = os.path.join(unit.dir, 'scan_rename_map.json')
    rename = {}
    if os.path.isfile(map_path):
        with open(map_path, encoding='utf-8') as f:
            rename = json.load(f)
    first_pass = not rename

    plan, skipped, offpattern, excluded = [], [], [], []
    for src in sources:
        want = staged_name(unit, src, stem)
        if not want:
            offpattern.append(src)
            continue
        ident = identity_of(unit, want)
        have = existing.get(ident)
        if have and not a.force:
            skipped.append((src, have))
            continue
        if not have and not first_pass and src not in rename and not a.force:
            # Staged before, and this page was not taken. That is a decision -
            # blank leaves are removed before the mapping is built - so restoring
            # it here would silently add a page the mapping does not expect.
            excluded.append(src)
            continue
        plan.append((src, have or want, ident))

    if excluded:
        print(f'  {len(excluded)} source image(s) were left out when this unit was '
              f'staged and are not being restored: {excluded[:3]}')
        print('    (pass --force if they really should be staged now)')
    if offpattern:
        print(f'  WARNING: {len(offpattern)} file(s) do not start with '
              f'{stem!r} and were left alone: {offpattern[:3]}')

    for src, dst, _ in plan:
        print(f'  {src}  ->  {dst}')
        if not a.dry_run:
            shutil.copy2(os.path.join(processed, src), os.path.join(PAGES, dst))

    # Merged, never replaced: a unit staged in two passes must not lose the
    # first pass's provenance.
    for src, dst, _ in plan:
        rename[src] = dst
    for src, have in skipped:
        rename.setdefault(src, have)
    if not a.dry_run:
        with open(map_path, 'w', encoding='utf-8') as f:
            json.dump(dict(sorted(rename.items())), f, ensure_ascii=False, indent=1)

    pruned = []
    if a.prune:
        wanted = {identity_of(unit, staged_name(unit, s, stem) or '')
                  for s in sources if staged_name(unit, s, stem)}
        for ident, f in sorted(existing.items()):
            if ident not in wanted:
                pruned.append(f)
                if not a.dry_run:
                    os.remove(os.path.join(PAGES, f))

    print(f'\n{unit.slug}: {len(sources)} page image(s) in processed/')
    print(f'  staged        : {len(plan)}')
    print(f'  already there : {len(skipped)}')
    if excluded:
        print(f'  left out      : {len(excluded)} excluded when first staged')
    if pruned:
        print(f'  pruned        : {len(pruned)} with no source left')
    elif not a.prune:
        orphans = len(existing) - len(skipped) - sum(1 for _, d, _ in plan if d in existing.values())
        if orphans > 0:
            print(f'  NOTE: {orphans} staged page(s) have no source in processed/ '
                  f'(run with --prune to remove)')
    print(f'  rename map    : {len(rename)} entries in units/{unit.slug}/scan_rename_map.json')
    if a.dry_run:
        print('\ndry run - nothing was written')
    else:
        print('\nnext: python pipeline/build/make_scan_derivatives.py')


if __name__ == '__main__':
    main()
