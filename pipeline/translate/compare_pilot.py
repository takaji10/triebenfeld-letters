# -*- coding: utf-8 -*-
"""Score the pilot: which model reads this hand better, Opus 5 or Sonnet 5.

Agreement with the existing corpus is NOT the score. The corpus is the thing
under suspicion -- a model that agrees with it perfectly has told us nothing.
What counts is whether a model recovers readings we independently know to be
right, and whether it corrupts readings we know are already right.

Three measures, in order of weight:

  RECOVERED  passages where the corpus is known to be wrong and we know the
             true reading. A model that finds these is genuinely reading ink.
  KEPT       passages where the corpus is known to be right. A model that
             breaks these is inventing, and that is worse than missing one.
  AGREEMENT  raw token overlap with the corpus. Context only: too high means
             it may be echoing the obvious, too low means noise.

Then the head-to-head: where both models independently depart from the corpus
in the SAME direction, that is the strongest signal available without going to
the manuscript, and it is what the full run would be mining.

    python compare_pilot.py
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, json, unicodedata
from difflib import SequenceMatcher
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRICES = {'claude-opus-5': (5, 25), 'claude-sonnet-5': (2, 10),
          'claude-fable-5-1': (10, 50), 'claude-haiku-4-5': (1, 5)}
FULL_CORPUS_PAGES = 869

# (letter, page, what the corpus reads, the true reading, where truth comes from)
RECOVER = [
    ('1', '1', 'Vnß land', 'Rußland',
     'read off the scan this session -- Österreich, Rußland und Preußen'),
    ('1', '1', 'Begrif', 'Congreß', 'read off the scan this session'),
    ('1', '1', 'schreib', 'schleunig', 'read off the scan this session'),
    ('48', '1', 'Traperiner', 'Trąbcz',
     'confirmed real place, Phase 2; letter 302 reads it correctly'),
    ('48', '1', 'Rechnung', 'Verrechnung',
     'confirmed correct reading, collation 48/302 item 15'),
    ('302', '1', 'Habik', 'Hawich',
     'confirmed correct reading, collation 48/302 items 7 and 30'),
]

# (letter, page, reading the corpus already has right) -- breaking one is a fault
KEEP = [
    ('302', '1', 'Trąbcz'), ('302', '1', 'exmittirt'), ('302', '1', 'Hawich'),
    ('48', '1', 'Hawich'),
]

TOKEN = re.compile(r'\[[^\]]*\]|[^\W\d_]+|\d+[\d.,/]*|[^\s\w]', re.UNICODE)
LANG_LINE = re.compile(r'^\s*\[lang:\s*([a-z]{2})\s*\]\s*$', re.I)


def fold(s):
    s = s.lower().replace('ſ', 's').replace('ß', 'ss')
    s = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in s if not unicodedata.combining(c))


def has(text, probe):
    return fold(probe) in fold(text)


def load_a():
    recs = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8'))
    return {(str(r['letter_id']), str(p['page'])): p['diplomatic']
            for r in recs for p in r['pages']}


def load_witness(d):
    out = {}
    if not os.path.isdir(d):
        return out
    for fn in os.listdir(d):
        if not re.match(r'L(.+)_p(.+)\.json$', fn):
            continue
        rec = json.load(open(os.path.join(d, fn), encoding='utf-8'))
        if not rec.get('text'):
            continue
        lines = rec['text'].split('\n')
        lang = None
        if lines and LANG_LINE.match(lines[0]):
            lang = LANG_LINE.match(lines[0]).group(1).lower()
            lines = lines[1:]
        rec['body'] = '\n'.join(lines).strip()
        rec['lang'] = lang
        out[(str(rec['letter']), str(rec['page']))] = rec
    return out


def agreement(a, b):
    at = [fold(t) for t in TOKEN.findall(a)]
    bt = [fold(t) for t in TOKEN.findall(b)]
    if not at:
        return 0.0
    sm = SequenceMatcher(None, at, bt, autojunk=False)
    return sum(n for _, _, n in sm.get_matching_blocks()) / len(at) * 100


def departures(a, b):
    """Tokens where B departs from A -- as (a_side, b_side) pairs."""
    at, bt = TOKEN.findall(a), TOKEN.findall(b)
    sm = SequenceMatcher(None, [fold(t) for t in at], [fold(t) for t in bt],
                         autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            out.append((' '.join(at[i1:i2]), ' '.join(bt[j1:j2])))
    return out


def main():
    wa = load_a()
    dirs = [(d, os.path.join(ROOT, d)) for d in sorted(os.listdir(ROOT))
            if d.startswith('retranscription')
            and os.path.isdir(os.path.join(ROOT, d))]
    wits = {d: load_witness(p) for d, p in dirs}
    wits = {d: w for d, w in wits.items() if w}
    if not wits:
        print('No pilot output yet. Run:  python retranscribe.py --pilot --sweep')
        return

    print('=' * 74)
    print('PILOT SCORECARD')
    print('=' * 74)

    summary = {}
    for d, w in wits.items():
        models = {r.get('model', '?') for r in w.values()}
        model = models.pop() if len(models) == 1 else '/'.join(sorted(models))
        tin = sum(r['usage']['input'] + r['usage'].get('cache_read', 0)
                  + r['usage'].get('cache_write', 0) for r in w.values())
        tout = sum(r['usage']['output'] for r in w.values())
        pi, po = PRICES.get(model, (5, 25))
        cost = tin / 1e6 * pi + tout / 1e6 * po
        pages = len(w)

        rec_hits, rec_miss = [], []
        for lt, pg, corpus_reads, truth, why in RECOVER:
            r = w.get((lt, pg))
            if r is None:
                continue
            (rec_hits if has(r['body'], truth) else rec_miss).append(
                (f'L{lt} p{pg}', corpus_reads, truth))
        keep_ok, keep_broke = [], []
        for lt, pg, probe in KEEP:
            r = w.get((lt, pg))
            if r is None:
                continue
            (keep_ok if has(r['body'], probe) else keep_broke).append(
                (f'L{lt} p{pg}', probe))
        agr = [agreement(wa[k], r['body']) for k, r in w.items() if k in wa]

        summary[d] = dict(model=model, pages=pages, cost=cost, tin=tin, tout=tout,
                          rec_hits=rec_hits, rec_miss=rec_miss,
                          keep_ok=keep_ok, keep_broke=keep_broke,
                          agr=sum(agr) / len(agr) if agr else 0, w=w)

        n_rec = len(rec_hits) + len(rec_miss)
        n_keep = len(keep_ok) + len(keep_broke)
        print(f'\n### {model}   ({d}/)')
        print(f'  pages          {pages}')
        print(f'  RECOVERED      {len(rec_hits)}/{n_rec} known corpus errors')
        for tag, was, now in rec_hits:
            print(f'                   OK   {tag}  {was!r} -> {now!r}')
        for tag, was, now in rec_miss:
            print(f'                   miss {tag}  {was!r} -> {now!r}')
        print(f'  KEPT           {len(keep_ok)}/{n_keep} readings already correct')
        for tag, probe in keep_broke:
            print(f'                   BROKE {tag}  lost {probe!r}')
        print(f'  agreement w/A  {summary[d]["agr"]:.1f}%  (context, not a score)')
        print(f'  cost           ${cost:.3f} for {pages} pages '
              f'= ${cost/pages:.4f}/page')
        print(f'  extrapolated   ${cost/pages*FULL_CORPUS_PAGES:.0f} live / '
              f'${cost/pages*FULL_CORPUS_PAGES/2:.0f} batched, all '
              f'{FULL_CORPUS_PAGES} pages')
        langs = {k: r['lang'] for k, r in w.items() if r['lang'] not in (None, 'de')}
        if langs:
            print(f'  non-German     {langs}')

    if len(summary) >= 2:
        print('\n' + '=' * 74)
        print('HEAD TO HEAD - where both models leave the corpus the same way')
        print('=' * 74)
        print('These are the strongest candidates a full run would surface: two')
        print('independent readers departing from the corpus in the same direction.\n')
        names = list(summary)
        a_, b_ = summary[names[0]], summary[names[1]]
        shared = sorted(set(a_['w']) & set(b_['w']),
                        key=lambda k: (len(k[0]), k[0], k[1]))
        agreed = 0
        for k in shared:
            if k not in wa:
                continue
            da = {(x, y) for x, y in departures(wa[k], a_['w'][k]['body']) if x.strip()}
            db = {(x, y) for x, y in departures(wa[k], b_['w'][k]['body']) if x.strip()}
            both = sorted(da & db)
            if not both:
                continue
            print(f'  L{k[0]} p{k[1]}  ({len(both)} agreed departures)')
            for x, y in both[:8]:
                print(f'      corpus {x[:34]!r:<38} both models {y[:34]!r}')
            if len(both) > 8:
                print(f'      ... and {len(both)-8} more')
            agreed += len(both)
            print()
        print(f'  total: {agreed} places where {a_["model"]} and {b_["model"]}')
        print(f'  independently disagree with the corpus in the same way.')

    print('\n' + '=' * 74)
    print('HOW TO READ THIS')
    print('=' * 74)
    print('RECOVERED is the measure that matters. A model that recovers the known')
    print('errors is reading the manuscript; one that misses them is guessing from')
    print('context. KEPT is the safety check - breaking a correct reading is worse')
    print('than missing a wrong one, because it manufactures work.')
    print('If Sonnet matches Opus on RECOVERED and KEPT, take Sonnet: same result,')
    print('roughly 40% of the cost. If it trails, the gap is what the extra buys.')


if __name__ == '__main__':
    main()
