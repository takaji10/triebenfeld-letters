# -*- coding: utf-8 -*-
"""Words that may want a glossary entry, for the editor to rule on.

    python glossary_candidates.py                 # every holding
    python glossary_candidates.py --unit <slug>   # one holding: what it adds

Writes review/glossary_candidates.csv (review/<slug>/ with --unit). A word
qualifies when a reader who is interested but not an expert would stop at it
and not know what it means (docs/GLOSSARY_PLAN.md). This finds candidates; it
does not decide. Four sources:

  termbase   reference/translation_glossary.yml: every term the translator is
             told how to render, counted by the documents its pattern hits
  rare       a word frequent in the letters but rare in modern German
             (reference/dwds_cache.json). This flags period spelling as readily
             as real obscurity, so every row wants judgement
  event      site/_data/timeline.yml
  office     the roles in reference/people.yml

A candidate already covered by reference/glossary.yml (an entry, or a ruling
under `excluded:`) is marked so; with --unit only the uncovered ones are
listed, which is the new holding's work.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import os, re, csv, json, argparse, collections
import yaml
import unitlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return yaml.safe_load(f) if path.endswith('.yml') else json.load(f)


def covered():
    """Lowercased words the glossary already answers for: entries' headwords
    and match surfaces, and the words ruled out."""
    p = os.path.join(ROOT, 'reference', 'glossary.yml')
    if not os.path.exists(p):
        return [], set()
    g = load('reference/glossary.yml') or {}
    pats = []
    for e in g.get('entries') or []:
        for k in ('match_de', 'match_en'):
            v = e.get(k)
            for x in ([v] if isinstance(v, str) else v or []):
                pats.append(re.compile(x, re.I))
        for k in ('head_de', 'head_en', 'orig'):
            if e.get(k):
                pats.append(re.compile(r'\b' + re.escape(str(e[k]).split(',')[0].strip()) + r'\b', re.I))
    excluded = {str(x.get('word', '')).lower() for x in g.get('excluded') or []}
    return pats, excluded


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', default=None)
    a = ap.parse_args()
    unitlib.utf8_stdout()

    docs = [r for r in load('corpus/letters.json')
            if not a.unit or r['unit'] == a.unit]
    texts = {r['uid']: (r.get('text') or '').replace('ſ', 's') for r in docs}
    pats, excluded = covered()

    def is_covered(word):
        # the termbase spells some terms without umlauts (Fuerst)
        forms = {word, word.replace('ue', 'ü').replace('ae', 'ä').replace('oe', 'ö')}
        return any(f.lower() in excluded or any(p.search(f) for p in pats) for f in forms)

    rows = []

    # termbase
    tb = load('reference/translation_glossary.yml')
    for section in ('currency', 'honorifics', 'formulas', 'terms', 'latin_terms'):
        for e in tb.get(section) or []:
            if not isinstance(e, dict) or not e.get('pattern'):
                continue
            rx = re.compile(e['pattern'])
            hits = [u for u, t in texts.items() if rx.search(t)]
            if not hits:
                continue
            sample = next(m.group(0) for m in [rx.search(texts[hits[0]])])
            rows.append({'source': 'termbase:' + section, 'term': e.get('term'),
                         'english': e.get('render') or '', 'docs': len(hits),
                         'sample': sample, 'note': e.get('gloss') or '',
                         'covered': is_covered(e.get('term') or '')})

    # rare in modern German, frequent here
    freq = load('reference/dwds_cache.json')
    tok, where = collections.Counter(), collections.defaultdict(set)
    for u, t in texts.items():
        for w in re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", t):
            k = w.lower(); tok[k] += 1; where[k].add(u)
    for w, n in tok.items():
        f = freq.get(w)
        if isinstance(f, int) and 1 <= f <= 3000 and len(where[w]) >= 3:
            rows.append({'source': 'rare', 'term': w, 'english': '',
                         'docs': len(where[w]), 'sample': w,
                         'note': f'{n} uses; modern frequency {f}',
                         'covered': is_covered(w)})

    # events
    if not a.unit:
        for ev in load('site/_data/timeline.yml') or []:
            rows.append({'source': 'event', 'term': ev.get('title'), 'english': '',
                         'docs': len(ev.get('refs') or []), 'sample': str(ev.get('date')),
                         'note': (ev.get('note') or '').strip()[:200],
                         'covered': False})

    rows.sort(key=lambda r: (r['covered'], -r['docs']))
    if a.unit:
        rows = [r for r in rows if not r['covered']]
    out_dir = os.path.join(ROOT, 'review', a.unit) if a.unit else os.path.join(ROOT, 'review')
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, 'glossary_candidates.csv')
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['source', 'term', 'english', 'docs', 'sample',
                                          'note', 'covered', 'ruling'])
        w.writeheader()
        for r in rows:
            w.writerow(dict(r, ruling=''))
    left = sum(1 for r in rows if not r['covered'])
    print(f'{len(rows)} candidates, {left} not yet covered by reference/glossary.yml -> {out}')


if __name__ == '__main__':
    main()
