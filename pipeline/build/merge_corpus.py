# -*- coding: utf-8 -*-
"""
Merge every unit's build into one corpus.

build_db.py runs per unit and writes corpus/units/<slug>/. This combines those
into the files the website and the review tools read:

    corpus/letters.json      every document, chronological then by unit
    corpus/letters.csv
    corpus/pages.csv
    corpus/reading.txt
    corpus/chronological.txt

Units whose corpus.txt is still empty are skipped and reported, so a unit can
be scaffolded long before it is transcribed without breaking a build.
"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(ROOT, 'corpus')
UNITS_OUT = os.path.join(CORPUS, 'units')


def sort_key(r):
    """Dated documents in date order, undated last, ties broken by unit then
    archival position, so the order is stable across rebuilds."""
    return (not r['date_iso'], r['date_iso'] or '', r['unit'], r['seq_archival'])


def main():
    units = unitlib.load_units()
    records, skipped = [], []

    for u in units:
        path = os.path.join(UNITS_OUT, u.slug, 'letters.json')
        if not os.path.isfile(path):
            skipped.append((u.slug, 'not built yet'))
            continue
        with open(path, encoding='utf-8') as f:
            recs = json.load(f)
        if not recs:
            skipped.append((u.slug, 'no documents'))
            continue
        records.extend(recs)
        print(f'  {u.slug:14s} {len(recs):4d} documents')

    if not records:
        raise SystemExit('nothing to merge: no unit has been built')

    records.sort(key=sort_key)

    # uid must be unique, or two units are claiming the same document
    seen = {}
    for r in records:
        if r['uid'] in seen:
            raise SystemExit(f'duplicate uid {r["uid"]!r} in {r["unit"]} and {seen[r["uid"]]}')
        seen[r['uid']] = r['unit']

    os.makedirs(CORPUS, exist_ok=True)
    with open(os.path.join(CORPUS, 'letters.json'), 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=1)

    # CSV and pages.csv are concatenations of the per-unit files, header once
    for name in ('letters.csv', 'pages.csv'):
        rows, header = [], None
        for u in units:
            path = os.path.join(UNITS_OUT, u.slug, name)
            if not os.path.isfile(path):
                continue
            with open(path, encoding='utf-8-sig', newline='') as f:
                rd = csv.reader(f)
                h = next(rd, None)
                if h is None:
                    continue
                header = header or h
                rows.extend(rd)
        if header:
            with open(os.path.join(CORPUS, name), 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.writer(f)
                w.writerow(header)
                w.writerows(rows)

    # the reading and chronological texts, unit by unit with a heading
    for name in ('reading.txt', 'chronological.txt'):
        parts = []
        for u in units:
            path = os.path.join(UNITS_OUT, u.slug, name)
            if not os.path.isfile(path):
                continue
            with open(path, encoding='utf-8') as f:
                parts.append(f'=== {u["ref"]} ({u.slug}) ===\n\n' + f.read())
        if parts:
            with open(os.path.join(CORPUS, name), 'w', encoding='utf-8', newline='\n') as f:
                f.write('\n\n'.join(parts))

    print(f'  merged: {len(records)} documents from {len(units) - len(skipped)} unit(s)')
    print(f'          {sum(len(r["pages"]) for r in records)} manuscript pages')
    for slug, why in skipped:
        print(f'  skipped {slug}: {why}')


if __name__ == '__main__':
    main()
