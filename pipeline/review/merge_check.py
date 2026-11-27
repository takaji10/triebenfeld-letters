# -*- coding: utf-8 -*-
"""Before and after a merge (docs/DOCUMENT_MERGE_PLAN.md): every document's state
recorded under its number, then compared through the holding's merge map.

    python pipeline/review/merge_check.py --unit <slug> --before   # record (before the merge)
    python pipeline/review/merge_check.py --unit <slug> --after    # compare (after the rebuild)

A renumbered document must be what it was in every field. A merged document
must hold exactly the lines and the words (text and English) of its parts,
keep its main part's date, place, sender, recipient and type, and have each
page once.
"""
import collections
import io
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
import unitlib  # noqa: E402

FIELDS = ('date_iso', 'date_precision', 'place', 'sender', 'recipient', 'doc_type', 'language', 'estates')
LABELS = {'[Written by the receiving office:]', '[Written in the margin:]', '[Written in another hand:]',
          '[The document continues:]'}


def state(slug):
    recs = json.load(io.open(os.path.join(ROOT, 'dataset', 'units', slug, 'letters.json'), encoding='utf-8'))
    en_sum = yaml.safe_load(io.open(os.path.join(ROOT, 'site', '_data', 'summaries.yml'), encoding='utf-8')) or {}
    de_sum = yaml.safe_load(io.open(os.path.join(ROOT, 'site', '_data', 'summaries_de.yml'), encoding='utf-8')) or {}
    out = {}
    for r in recs:
        d = {k: r.get(k) for k in FIELDS}
        d['lines'] = sorted(l for p in r['pages'] for l in p['diplomatic'].split('\n') if l.strip())
        d['reading_words'] = sorted(w for p in r['pages'] for w in p.get('reading', '').split())
        d['page_ids'] = [p.get('page_id') for p in r['pages']]
        tp = os.path.join(ROOT, 'site', '_data', 'translations', r['pad'] + '.yml')
        en = ''
        if os.path.isfile(tp):
            t = yaml.safe_load(io.open(tp, encoding='utf-8')) or {}
            en = '\n\n'.join(s.get('en') or '' for s in t.get('segments') or [])
        d['english_words'] = sorted(w for w in en.split() if w not in ('[Written', 'in', 'another', 'hand:]')
                                    or True)
        d['english_words'] = sorted(w for para in re.split(r'\n\s*\n', en) if para.strip() not in LABELS
                                    for w in para.split())
        d['summary_en'] = en_sum.get(r['pad'])
        d['summary_de'] = de_sum.get(r['pad'])
        out[str(r['letter_id'])] = d
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    p = os.path.join(ROOT, 'review', 'merge_state_%s.json' % slug)
    if '--before' in sys.argv:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(state(slug), io.open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False)
        print('recorded', p)
        return
    was = json.load(io.open(p, encoding='utf-8'))
    now = state(slug)
    mp = json.load(io.open(os.path.join(unit.dir, 'intake', 'merge_map.json'), encoding='utf-8'))
    idmap = mp['idmap']
    groups = collections.defaultdict(list)
    for old, new in idmap.items():
        groups[new].append(old)
    bad = 0
    for new, olds in sorted(groups.items(), key=lambda kv: int(kv[0])):
        n = now.get(new)
        if n is None:
            print('!! new document %s is missing' % new)
            bad += 1
            continue
        if len(olds) == 1 and olds[0] not in was:
            # a document put in before the run (Konin Gr.118's "17a", 2026-11-28): nothing to compare
            print('   %s (was %s): added, no earlier state' % (new, olds[0]))
            continue
        if len(olds) == 1:
            o = was[olds[0]]
            diffs = [k for k in o if o[k] != n.get(k)]
            if diffs:
                print('!! %s (was %s): differs in %s' % (new, olds[0], diffs))
                bad += 1
            continue
        main = next(x for x in olds if was[x]['page_ids'] and was[x]['page_ids'][0] == n['page_ids'][0])
        exp_lines = sorted(l for x in olds for l in was[x]['lines'])
        exp_words = sorted(w for x in olds for w in was[x]['reading_words'])
        exp_en = sorted(w for x in olds for w in was[x]['english_words'])
        msgs = []
        if exp_lines != n['lines']:
            msgs.append('lines')
        if exp_words != n['reading_words']:
            msgs.append('reading words')
        if exp_en != n['english_words']:
            c1, c2 = collections.Counter(exp_en), collections.Counter(n['english_words'])
            msgs.append('english words (missing %s, extra %s)' % (list((c1 - c2).items())[:5],
                                                                 list((c2 - c1).items())[:5]))
        for k in ('date_iso', 'place', 'sender', 'recipient', 'doc_type'):
            if was[main][k] != n[k]:
                msgs.append('%s %r -> %r' % (k, was[main][k], n[k]))
        if len(set(n['page_ids'])) != len(n['page_ids']):
            msgs.append('a page twice')
        print('%s %s (merged from %s): %s' % ('!!' if msgs else 'ok', new, '+'.join(olds),
                                            '; '.join(msgs) if msgs else 'every line and word, main metadata kept'))
        bad += bool(msgs)
    seen = collections.Counter(pid for d in now.values() for pid in d['page_ids'] if pid)
    before = collections.Counter(pid for d in was.values() for pid in d['page_ids'] if pid)
    # pages that already held two entries before the run are not a problem (Konin Gr.118, 2026-11-28)
    twice = [k for k, c in seen.items() if c > 1 and before[k] < c]
    print('pages under two documents: %s' % (twice or 'none'))
    print('%s: %d problem(s)' % (slug, bad + bool(twice)))


if __name__ == '__main__':
    main()
