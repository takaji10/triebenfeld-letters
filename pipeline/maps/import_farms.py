# -*- coding: utf-8 -*-
"""Merge the working page's farm labels and red-number corrections into the
map's data files.

    python pipeline/maps/import_farms.py [files...] [--map <key>]

Three kinds of file, all written by scratch/map4456/farm_labels.html:

- the Export JSON button's file - the whole working state in one:
  {"farms": [{n, x, y}, ...], "reds": [{n, x, y}, ...]}. Both halves are
  imported, farms into farms.yml and reds into reds.yml.
- farm_labels_latest.json - every farm label, existing and new, in the
  mosaic's pixels: [{n, x, y}]. The settlers stay as they are; the marks
  list is replaced wholesale (the working page holds the whole set), sorted
  by farm number.
- red_labels_latest.json - the red numbers' readings: [{n, x, y}] where n
  is the reading as written (a bracketed [?] doubt stays). Matched to the
  marks of reds.yml by position - the positions are the marks' identity -
  and only the changed ones are written; the unsure flag follows the
  reading's brackets.

With no file named, the working files under scratch/map4456/ are taken
where they exist.
"""
import io
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRATCH = os.path.join(ROOT, 'scratch', 'map4456')
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'maps'))
from common import die  # noqa: E402

MAPS_DIR = os.path.join(ROOT, 'maps')


def import_farms(labels, d, src):
    if not isinstance(labels, list) or not labels:
        die(f'{src}: expected a non-empty list of labels')
    seen = set()
    marks = []
    for lb in labels:
        n = lb.get('n')
        if not isinstance(n, int):
            die(f'{src}: a label without an integer n: {lb!r}')
        # a farm number may repeat: a farmer can hold several farmsteads
        # within his plot, each with its own label; only the same number at
        # the same position twice is a mistake
        trip = (n, int(lb['x']), int(lb['y']))
        if trip in seen:
            die(f'{src}: farm {n} twice at {lb["x"]},{lb["y"]}')
        seen.add(trip)
        marks.append({'n': n, 'x': int(lb['x']), 'y': int(lb['y']),
                      'note': lb.get('note') or None})
    marks.sort(key=lambda m: (m['n'], m['x'], m['y']))
    before = len(d.get('marks') or [])
    d['marks'] = marks
    print(f'  farms: marks {before} -> {len(marks)} '
          f'(+{len(marks) - before})')


def import_reds(readings, d, src):
    # the working state arrives either as a bare list (the old format) or
    # as {marks, deleted} - the deletions are the baked positions of the
    # marks the editor removed
    dels = []
    if isinstance(readings, dict):
        dels = readings.get('deleted') or []
        readings = readings.get('marks') or []
    if not isinstance(readings, list) or not readings:
        die(f'{src}: expected a non-empty list of red readings')
    marks = d.get('marks') or []
    # the deletions first: the marks baked at those positions are gone -
    # the editor read a smudge as a number, or the number is not there
    dropped = 0
    if dels:
        dset = {f'{int(x["x"])},{int(x["y"])}' for x in dels}
        kept = []
        for m in marks:
            if f'{m["x"]},{m["y"]}' in dset:
                dropped += 1
                print(f'    red {m["x"]},{m["y"]}: {m["n"]} deleted')
            else:
                kept.append(m)
        marks = kept
    # the saved entry's identity is the position its mark had when it was
    # written: a moved red carries that baked position in ox,oy beside its
    # new place in x,y (older files have only x,y and never moved)
    by_pos = {}
    for x in readings:
        kx = x['ox'] if x.get('ox') is not None else x['x']
        ky = x['oy'] if x.get('oy') is not None else x['y']
        by_pos[f'{kx},{ky}'] = x
    fixed = 0
    for m in marks:
        v = by_pos.get(f'{m["x"]},{m["y"]}')
        if v is None:
            continue
        old = m['n']
        moved = (int(v['x']) != m['x'] or int(v['y']) != m['y'])
        if v['n'] == m['n'] and not moved:
            continue
        m['n'] = v['n']
        # the doubt follows the reading: a bracketed reading is unsure,
        # a firm one is not - a correction can clear a doubt as well as
        # set one
        m['unsure'] = '[' in str(m['n'])
        if moved:
            m['x'] = int(v['x'])
            m['y'] = int(v['y'])
        fixed += 1
        print(f'    red {m["x"]},{m["y"]}: {old} -> {m["n"]}'
              + (' (moved)' if moved else '')
              + (' (unsure)' if m['unsure'] else ''))
    # the hand-added marks: negative ids in the working state become real
    # marks appended to the yml
    added = 0
    for x in readings:
        if not isinstance(x.get('id'), int) or x['id'] >= 0:
            continue
        marks.append({'n': str(x['n']), 'x': int(x['x']), 'y': int(x['y']),
                      'unsure': '[' in str(x['n'])})
        added += 1
        print(f'    red {x["x"]},{x["y"]}: {x["n"]} added')
    d['marks'] = marks
    print(f'  reds: {fixed} correction(s)/move(s), {dropped} deleted, '
          f'{added} added -> reds.yml ({len(marks)} marks)')


def write_yml(key, target, d, text):
    yml = os.path.join(MAPS_DIR, key, target)
    if not os.path.isfile(yml):
        die(f'no data file at {yml}')
    if target == 'farms.yml':
        header = text.split('\nsettlers:', 1)[0]
        payload = {'settlers': d['settlers'], 'marks': d['marks']}
    else:
        header = text.split('\nmarks:', 1)[0]
        payload = {'marks': d['marks']}
    if not header.endswith('\n'):
        header += '\n'
    with open(yml, 'w', encoding='utf-8', newline='\n') as f:
        f.write(header)
        yaml.safe_dump(payload, f, allow_unicode=True,
                       default_flow_style=False, sort_keys=False,
                       width=100)
    print(f'  -> {yml}')


def load_yml(key, target):
    yml = os.path.join(MAPS_DIR, key, target)
    if not os.path.isfile(yml):
        die(f'no data file at {yml}')
    with open(yml, encoding='utf-8') as f:
        text = f.read()
    return text, yaml.safe_load(text)


def main():
    args = sys.argv[1:]
    key = 'pelzucki1896'
    if '--map' in args:
        i = args.index('--map')
        key = args[i + 1]
        args = args[:i] + args[i + 2:]
    paths = args
    if not paths:
        paths = [os.path.join(SCRATCH, n)
                 for n in ('farm_labels_latest.json', 'red_labels_latest.json')
                 if os.path.isfile(os.path.join(SCRATCH, n))]
    if not paths:
        die('usage: import_farms.py <labels.json> [...] [--map <key>]\n'
            '  or run with no file and the working files '
            'under scratch/map4456/ are taken')
    for path in paths:
        with open(path, encoding='utf-8') as f:
            payload = json.load(f)
        if isinstance(payload, dict) and ('farms' in payload
                                          or 'reds' in payload):
            # the Export JSON button's combined file: both halves
            if payload.get('farms'):
                text, d = load_yml(key, 'farms.yml')
                import_farms(payload['farms'], d, path)
                write_yml(key, 'farms.yml', d, text)
            if payload.get('reds'):
                text, d = load_yml(key, 'reds.yml')
                import_reds(payload['reds'], d, path)
                write_yml(key, 'reds.yml', d, text)
        else:
            target = 'reds.yml' \
                if 'red_labels' in os.path.basename(path) else 'farms.yml'
            text, d = load_yml(key, target)
            if target == 'farms.yml':
                import_farms(payload, d, path)
            else:
                import_reds(payload, d, path)
            write_yml(key, target, d, text)


if __name__ == '__main__':
    main()
