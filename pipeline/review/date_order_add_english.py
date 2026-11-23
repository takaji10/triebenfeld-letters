# -*- coding: utf-8 -*-
"""Append checked English drafts to reference/english_corrections.yml
(docs/DATE_ORDER_PLAN.md, Method 5).

    python pipeline/review/date_order_add_english.py <drafts.yml> [--skip 151,...] [--key drafts]

Each draft: pad, page, find, replace, why. Refused (and reported) unless
`find` occurs once on the published page and its words equal those of
`replace` (commas aside). A pad/page already corrected for the date is skipped.
Written one entry per line, strings in JSON form (valid YAML).
"""
import collections
import io
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def words(s):
    # --loose: also full stops at word ends and a lone dash, where a mark that
    # only separated the moved date from the closing goes with it (2026-11-23:
    # "Highness's. Berlin", "Highness's — Berlin"); listed in the report
    if '--loose' in sys.argv:
        return collections.Counter(w.strip(',.') for w in s.split() if w.strip(',.') and w != '—')
    return collections.Counter(w.strip(',') for w in s.split() if w.strip(','))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    skip = set(sys.argv[sys.argv.index('--skip') + 1].split(',')) if '--skip' in sys.argv else set()
    key = sys.argv[sys.argv.index('--key') + 1] if '--key' in sys.argv else 'drafts'
    drafts = yaml.safe_load(io.open(args[0], encoding='utf-8'))[key]
    cp = os.path.join(ROOT, 'reference', 'english_corrections.yml')
    have = {(c['pad'], c['page']) for c in yaml.safe_load(io.open(cp, encoding='utf-8'))['corrections']
            if 'the date after the signature' in str(c.get('why', ''))}
    lines, n = [], 0
    for d in drafts:
        letter = d['pad'].rsplit('-', 1)[1].lstrip('0') or '0'
        if letter in skip or (d['pad'], d['page']) in have:
            continue
        tp = os.path.join(ROOT, 'site', '_data', 'translations', d['pad'] + '.yml')
        seg = next(x for x in yaml.safe_load(io.open(tp, encoding='utf-8'))['segments'] if x['page'] == d['page'])
        en = seg.get('en') or ''
        if en.count(d['find']) != 1:
            print('!! %s p%s: find occurs %d times' % (d['pad'], d['page'], en.count(d['find'])))
            continue
        if words(d['find']) != words(d['replace']):
            print('!! %s p%s: the words differ' % (d['pad'], d['page']))
            continue
        lines.append('- {pad: %s, page: %s, find: %s, replace: %s, why: %s}' % (
            d['pad'], d['page'], json.dumps(d['find'], ensure_ascii=False),
            json.dumps(d['replace'], ensure_ascii=False), json.dumps(d['why'], ensure_ascii=False)))
        n += 1
    if lines:
        raw = io.open(cp, encoding='utf-8').read().rstrip('\n') + '\n'
        with io.open(cp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(raw + '\n'.join(lines) + '\n')
        yaml.safe_load(io.open(cp, encoding='utf-8'))  # still valid
    print('%d correction(s) added' % n)


if __name__ == '__main__':
    main()
