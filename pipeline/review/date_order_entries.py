# -*- coding: utf-8 -*-
"""Write the settled moves into units/<slug>/intake/date_order.yml
(docs/DATE_ORDER_PLAN.md, Method 2), the date and anchor lines copied from
corpus.txt by their line numbers.

    python pipeline/review/date_order_entries.py --unit oe1bu9454 --settled review/date_order/settled_oe1bu9454.json

The settled file: [{"letter", "date_lines": [n...], "after_line": n, "join": [n...], "note"}].
An entry for a letter already in the file is not written again.
"""
import io
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import unitlib  # noqa: E402
import date_order as D  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    settled = json.load(io.open(sys.argv[sys.argv.index('--settled') + 1], encoding='utf-8'))
    path = os.path.join(unit.dir, 'intake', 'date_order.yml')
    raw = io.open(path, encoding='utf-8').read() if os.path.isfile(path) else (
        '# The date moved after the signature (docs/DATE_ORDER_PLAN.md; the editor,\n'
        '# 2026-11-23). Carried out by pipeline/review/date_order.py --move --write;\n'
        '# an entry already carried out is skipped. Lines exactly as in corpus.txt.\n')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    spec = yaml.safe_load(raw) or {}
    entries = spec.get('moves') or []
    have = {str(e['letter']) for e in entries}
    docs = dict(D.documents(unit))
    added = 0
    for s in settled:
        L = str(s['letter'])
        if L in have:
            continue
        text = {n: t for n, _, t in docs[L]}
        ent = {'letter': L, 'date': [text[n] for n in s['date_lines']], 'after': text[s['after_line']]}
        if s.get('join'):
            ent['join'] = [text[n] for n in s['join']]
        if s.get('ps_lines'):
            ent['ps'] = [text[n] for n in s['ps_lines']]
        ent['note'] = s.get('note', '')
        entries.append(ent)
        added += 1
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(head + yaml.safe_dump({'moves': entries}, allow_unicode=True, sort_keys=False, width=1000))
    print('%s: %d entries added, %d in all' % (slug, added, len(entries)))


if __name__ == '__main__':
    main()
