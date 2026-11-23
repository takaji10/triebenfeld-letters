# -*- coding: utf-8 -*-
"""After the move and the rebuild: in every moved document the date is one
paragraph of the reading text, directly after the paragraph that ends with the
anchor; and where the English has been corrected, the English page has as many
paragraphs as the German (docs/DATE_ORDER_PLAN.md, Method 4-5).

    python pipeline/review/date_order_verify.py --unit oe1bu9454 [--english]
"""
import io
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import unitlib  # noqa: E402
import date_order as D  # noqa: E402
from date_order_english import LABELS  # noqa: E402


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    spec = D._yaml(os.path.join(unit.dir, 'intake', 'date_order.yml')).get('moves') or []
    recs = {str(r['letter_id']): r for r in
            json.load(io.open(os.path.join(ROOT, 'dataset', 'units', slug, 'letters.json'), encoding='utf-8'))}
    docs = dict(D.documents(unit))
    bad = 0
    for ent in spec:
        L = str(ent['letter'])
        rec = recs[L]
        date = [str(x) for x in ent['date']] + [str(x) for x in ent.get('join') or []]
        texts = [t for _, _, t in docs[L]]
        s = next((i for i in range(len(texts)) if texts[i:i + len(date)] == date), None)
        if s is None or texts[s - 1] != str(ent['after']):
            print('!! %s: the date does not stand directly after the anchor in corpus.txt' % L)
            bad += 1
            continue
        page_id = docs[L][s][1]
        page = next(p for p in rec['pages'] if p.get('page_id') == page_id)
        gp = [norm(p) for p in page['paragraphs']]
        want = norm(' '.join(date))
        hits = [i for i, p in enumerate(gp) if p == want]
        if len(hits) != 1:
            print('!! %s: no single German paragraph is the date "%s"' % (L, want))
            bad += 1
            continue
        i = hits[0]
        if i == 0 or not gp[i - 1].endswith(norm(str(ent['after']))):
            print('!! %s: the paragraph before the date does not end with "%s"' % (L, ent['after']))
            bad += 1
            continue
        if '--english' in sys.argv:
            tp = os.path.join(ROOT, 'site', '_data', 'translations', rec['pad'] + '.yml')
            seg = next(x for x in yaml.safe_load(io.open(tp, encoding='utf-8'))['segments']
                       if x['page'] == page['page'])
            ep = [p for p in re.split(r'\n\s*\n', seg.get('en') or '') if p.strip() and p.strip() not in LABELS]
            if len(ep) != len(gp):
                print('!! %s: German %d paragraphs, English %d' % (L, len(gp), len(ep)))
                bad += 1
    print('%s: %d moved document(s) checked, %d problem(s)' % (slug, len(spec), bad))


if __name__ == '__main__':
    main()
