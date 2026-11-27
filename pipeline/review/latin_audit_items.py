# -*- coding: utf-8 -*-
"""Blind-reader items from a led reader's findings (the Latin audit, docs/LATIN_AUDIT_PLAN.md).

    python pipeline/review/latin_audit_items.py <slug> <reader file> [<reader file> ...] [--groups N]

Each reader file is review/latin_audit/<slug>/<name>.json ({"findings": [...]}); its findings are
referred to as "<file stem>.<index>". A finding goes to the blind reader when it would change the text:
kinds misread / doubt_settled / omission / insertion / tilde, certainty sure or likely. For each, the
transcription's three words before and after the quoted place are the guides (marks of doubt stripped),
and the named band with its neighbours are the bands. The reading under question is never given.

Writes review/latin_audit/<slug>/items_b_<k>.json, grouped by page into N files (default 1), and says
which findings could not be located by their quoted words (those Claude reads itself).
The comparison afterwards: pipeline/review/latin_audit_compare.py.
"""
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    groups = 1
    if '--groups' in args:
        i = args.index('--groups')
        groups = int(args[i + 1])
        del args[i:i + 2]
    slug, files = args[0], args[1:]
    R = os.path.join(ROOT, 'review', 'latin_audit', slug)
    pages = {}
    for p in glob.glob(os.path.join(R, 'pages', '*.txt')):
        pages[os.path.basename(p)[:-4]] = re.sub(r'^\d+\t', '', io.open(p, encoding='utf-8').read(),
                                                 flags=re.M).replace('\n', ' ')
    clean = lambda w: re.sub(r'\[[^\]]*\?\]|[\[\]~¬]', '', w)
    items, miss = [], []
    for fn in files:
        stem = os.path.splitext(os.path.basename(fn))[0]
        for i, f in enumerate(json.load(io.open(os.path.join(R, os.path.basename(fn)), encoding='utf-8'))['findings']):
            if f.get('kind') not in ('misread', 'doubt_settled', 'omission', 'insertion', 'tilde'):
                continue
            if f.get('certainty') not in ('sure', 'likely'):
                continue
            ref = '%s.%d' % (stem, i)
            t = pages.get(f['page_id'], '')
            snip = re.sub(r'^\(.*?\)\s*', '', (f.get('transcribed') or '').split('...')[0].strip())
            k = t.find(snip) if snip else -1
            if k < 0:
                miss.append(ref)
                continue
            m = re.search(r'_s(\d+)', f.get('strip') or '')
            n = int(m.group(1)) if m else 4
            items.append({'ref': ref, 'page': f['page_id'],
                          'bands': ['%s_s%02d.jpg' % (f['page_id'], b) for b in (n - 1, n, n + 1) if 1 <= b <= 8],
                          'before': ' '.join(clean(w) for w in t[:k].split()[-3:]),
                          'after': ' '.join(clean(w) for w in t[k + len(snip):].split()[:3])})
    items.sort(key=lambda x: (x['page'], x['bands'][0]))
    n = len(items)
    for g in range(groups):
        part = items[g * n // groups:(g + 1) * n // groups]
        for j, x in enumerate(part, 1):
            x['item'] = j
        io.open(os.path.join(R, 'items_b_%d.json' % (g + 1)), 'w', encoding='utf-8', newline='\n').write(
            json.dumps(part, ensure_ascii=False, indent=1))
        print('items_b_%d.json: %d items, pages %s' % (g + 1, len(part), ' '.join(sorted({x['page'] for x in part}))))
    print('not located (Claude reads these):', ' '.join(miss) or 'none')


if __name__ == '__main__':
    main()
