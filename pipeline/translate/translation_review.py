# -*- coding: utf-8 -*-
"""Read back translation_review.csv and act on your rulings.

    python translation_review.py --read            # summarise what is filled in
    python translation_review.py --read --apply    # act on it

The `ruling` column works exactly as it does in name_review.csv, because you
already know that convention and there is no reason to invent a second one:

    blank        not looked at yet - nothing happens
    OK           confirmed fine. Recorded in translation_rulings.json so the
                 same row is never raised at you again, however often the
                 checks are re-run.
    anything else
                 the corrected English for that page. It replaces the
                 published text for that page, and the old file is backed up
                 first.

A letter whose every raised row carries a ruling is promoted from `draft` to
`reviewed`. publish_translations.py will then refuse to overwrite it, so a
later model run cannot silently undo work you have signed off.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, csv, json, shutil, argparse
from collections import defaultdict

import yaml
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = os.path.join(ROOT, 'review', 'translation_review.csv')
RULINGS = os.path.join(ROOT, 'reference', 'translation_rulings.json')
DEST = os.path.join(ROOT, 'site', '_data', 'translations')


def key(row):
    """Stable identity of a raised row, so a cleared one stays cleared."""
    return f"{row['letter']}|{row['page']}|{row['kind']}|{row['german']}"


def load_rulings():
    if os.path.isfile(RULINGS):
        return json.load(open(RULINGS, encoding='utf-8'))
    return {'_comment': 'Rulings on translation_review.csv. check_translations.py '
                        'reads this and never raises a cleared row again. Add to it; '
                        'do not remove entries, or the same question comes back.',
            'cleared': [], 'corrected': {}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--read', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.read:
        ap.error('use --read (add --apply to act on it)')
    if not os.path.isfile(SHEET):
        sys.exit(f'no sheet at {SHEET} - run check_translations.py first')

    rows = list(csv.DictReader(open(SHEET, encoding='utf-8-sig', newline='')))
    confirmed, corrected = [], []
    per_letter_total, per_letter_ruled = defaultdict(int), defaultdict(int)
    for r in rows:
        per_letter_total[r['letter']] += 1
        v = (r.get('ruling') or '').strip()
        if not v:
            continue
        per_letter_ruled[r['letter']] += 1
        (confirmed if v.upper() == 'OK' else corrected).append((r, v))

    print(f'{len(rows)} row(s) raised across {len(per_letter_total)} letter(s)')
    print(f'{len(confirmed)} confirmed as-is, {len(corrected)} correction(s)')
    done = [l for l in per_letter_total if per_letter_ruled[l] == per_letter_total[l]]
    print(f'{len(done)} letter(s) fully ruled on'
          + (f': {", ".join("L" + x for x in sorted(done)[:12])}' if done else ''))
    for r, v in corrected[:15]:
        print(f"   L{r['letter']} p{r['page']} {r['kind']}: {v[:70]}")

    if not a.apply:
        print('\n(reporting only - add --apply to act on it)')
        return

    rulings = load_rulings()
    cleared = set(rulings.get('cleared', []))
    for r, _ in confirmed:
        cleared.add(key(r))

    # Corrections replace the English for that page in the published file.
    by_pad = defaultdict(dict)
    for r, v in corrected:
        if r['page']:
            by_pad[r['pad']][int(r['page'])] = v
            rulings.setdefault('corrected', {})[key(r)] = v

    changed = 0
    for pad, pages in by_pad.items():
        path = os.path.join(DEST, pad + '.yml')
        if not os.path.isfile(path):
            print(f'  {pad}: not published yet, correction held')
            continue
        doc = yaml.safe_load(open(path, encoding='utf-8')) or {}
        shutil.copy2(path, path + '.bak')
        for seg in doc.get('segments', []):
            if seg['page'] in pages:
                seg['en'] = pages[seg['page']]
                changed += 1
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=100)

    # Promote fully-ruled letters, and never demote.
    promoted = 0
    pad_of = {r['letter']: r['pad'] for r in rows}
    for lid in done:
        path = os.path.join(DEST, pad_of[lid] + '.yml')
        if not os.path.isfile(path):
            continue
        doc = yaml.safe_load(open(path, encoding='utf-8')) or {}
        if doc.get('status') == 'reviewed':
            continue
        doc['status'] = 'reviewed'
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=100)
        promoted += 1

    rulings['cleared'] = sorted(cleared)
    with open(RULINGS, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(rulings, f, ensure_ascii=False, indent=2)

    print(f'\n{len(cleared)} row(s) cleared for good -> {RULINGS}')
    print(f'{changed} page(s) of English replaced by your corrections')
    print(f'{promoted} letter(s) promoted to reviewed')


if __name__ == '__main__':
    main()
