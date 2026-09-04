# -*- coding: utf-8 -*-
"""Collate the corpus transcription (witness A) against the independent
re-reading in `retranscription/` (witness B), and report where they disagree.

Neither witness is authoritative. The 48/302 twin showed each is right about as
often as the other, so a disagreement is a place to LOOK, not a verdict. This
script only ranks the looking.

Every disagreement is classified, because the classes need different treatment:

  numeral      every figure, always, whatever the two witnesses say. An
               order-of-magnitude error (25000/250000) is invisible otherwise.
  name         capitalised and not ordinary German. Names are the least
               reliable category in this hand and the hardest to spot by eye,
               because a wrong name still looks like a name.
  word/nonword one reading is a word the corpus or DWDS knows and the other is
               not. The known word usually wins - six for six in the twin.
  both-words   both readings are real. Only context decides; these are for you.
  A-only       witness B saw nothing there.
  B-only       witness B saw text the corpus has not got - usually marginalia,
               which the original pass dropped wholesale.

Convention-only differences (long s, wrap marks, [?] placement) are counted and
then set aside; they are not readings.

    python collate_witnesses.py                  # report on whatever exists
    python collate_witnesses.py --letters 1,48
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, json, csv, argparse, unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WB = os.path.join(ROOT, 'retranscription')
REPORT = os.path.join(ROOT, 'review', 'collation_report.md')
QUEUE = os.path.join(ROOT, 'review', 'collation_queue.csv')

TOKEN = re.compile(r'\[[^\]]*\]|[^\W\d_]+|\d+[\d.,/]*|[^\s\w]', re.UNICODE)


def norm(t):
    """Fold away what is convention rather than reading."""
    s = t.lower().replace('ſ', 's').replace('ß', 'ss')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s


def is_word_token(t):
    return bool(re.match(r'^[^\W\d_]+$', t, re.UNICODE))


def load_witness_a():
    recs = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8'))
    out = {}
    for r in recs:
        for p in r['pages']:
            out[(str(r['letter_id']), str(p['page']))] = p['diplomatic']
    return out


LANG_LINE = re.compile(r'^\s*\[lang:\s*([a-z]{2})\s*\]\s*$', re.I)

# Pages we already believe are not German. Witness B declares what it sees, so
# any page whose declaration falls outside this set is a finding in itself.
EXPECTED_NON_DE = {('283', '1'): 'fr', ('283', '2'): 'fr', ('72e', '1'): 'pl'}


def load_witness_b():
    """Returns {(letter, page): (text, declared_lang)} with the header stripped."""
    out = {}
    if not os.path.isdir(WB):
        return out
    for fn in os.listdir(WB):
        if not re.match(r'L(.+)_p(.+)\.json$', fn):
            continue
        rec = json.load(open(os.path.join(WB, fn), encoding='utf-8'))
        text = rec.get('text')
        if not text:
            continue
        lang = None
        lines = text.split('\n')
        if lines and LANG_LINE.match(lines[0]):
            lang = LANG_LINE.match(lines[0]).group(1).lower()
            text = '\n'.join(lines[1:]).lstrip('\n')
        out[(str(rec['letter']), str(rec['page']))] = (text, lang)
    return out


def language_check(wb):
    """Where witness B's declared language contradicts what we expected."""
    surprises = []
    for k, (_, lang) in sorted(wb.items()):
        if lang is None:
            continue
        expected = EXPECTED_NON_DE.get(k, 'de')
        if lang != expected:
            surprises.append((k, expected, lang))
    return surprises


def corpus_lexicon(wa):
    c = Counter()
    for txt in wa.values():
        for t in TOKEN.findall(txt):
            if is_word_token(t):
                c[norm(t)] += 1
    return c


def load_dwds():
    p = os.path.join(ROOT, 'reference', 'dwds_cache.json')
    if os.path.isfile(p):
        return {norm(k): v for k, v in json.load(open(p, encoding='utf-8')).items()}
    return {}


def known(tok, lex, dwds, min_corpus=3):
    n = norm(tok)
    if lex.get(n, 0) >= min_corpus:
        return True
    h = dwds.get(n)
    return bool(h and h > 0)


def classify(a_toks, b_toks, lex, dwds):
    a_s, b_s = ' '.join(a_toks), ' '.join(b_toks)
    if not a_toks:
        return 'B-only'
    if not b_toks:
        return 'A-only'
    if any(re.search(r'\d', t) for t in a_toks + b_toks):
        return 'numeral'
    aw = [t for t in a_toks if is_word_token(t)]
    bw = [t for t in b_toks if is_word_token(t)]
    if aw and bw:
        ka = all(known(t, lex, dwds) for t in aw)
        kb = all(known(t, lex, dwds) for t in bw)
        if ka != kb:
            capped = (aw[0][:1].isupper() or bw[0][:1].isupper())
            return 'name' if capped and not (ka and kb) and _namey(aw, bw, lex) else 'word/nonword'
        if ka and kb:
            if (aw[0][:1].isupper() and bw[0][:1].isupper()) and _namey(aw, bw, lex):
                return 'name'
            return 'both-words'
    if (aw and aw[0][:1].isupper()) or (bw and bw[0][:1].isupper()):
        return 'name'
    return 'both-words'


COMMON_CAP = None


def _namey(aw, bw, lex):
    """Capitalised and not merely a capitalised ordinary noun."""
    global COMMON_CAP
    if COMMON_CAP is None:
        COMMON_CAP = set()
    for t in aw + bw:
        n = norm(t)
        # a form that also occurs lowercased in the corpus is an ordinary noun
        if lex.get(n, 0) >= 3 and t[:1].isupper():
            continue
        return True
    return False


def collate_page(a_text, b_text, lex, dwds):
    a_raw = TOKEN.findall(a_text)
    b_raw = TOKEN.findall(b_text)
    a_n = [norm(t) for t in a_raw]
    b_n = [norm(t) for t in b_raw]
    sm = SequenceMatcher(None, a_n, b_n, autojunk=False)
    diffs = []
    same = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            same += i2 - i1
            continue
        at, bt = a_raw[i1:i2], b_raw[j1:j2]
        # context from witness A for the eye
        lo, hi = max(0, i1 - 6), min(len(a_raw), i2 + 6)
        ctx = ' '.join(a_raw[lo:hi])
        diffs.append({'a': ' '.join(at), 'b': ' '.join(bt),
                      'kind': classify(at, bt, lex, dwds), 'ctx': ctx})
    return diffs, same, len(a_raw), len(b_raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--letters')
    a = ap.parse_args()

    wa, wb = load_witness_a(), load_witness_b()
    if not wb:
        print(f'No second witness yet. Run retranscribe.py first '
              f'(expected files in {WB}/).')
        return
    keys = sorted(wb.keys() & wa.keys(),
                  key=lambda k: (len(k[0]), k[0], len(k[1]), k[1]))
    if a.letters:
        want = {s.strip() for s in a.letters.split(',')}
        keys = [k for k in keys if k[0] in want]
    if not keys:
        print('no pages in common'); return

    lex, dwds = corpus_lexicon(wa), load_dwds()
    surprises = language_check(wb)
    L, rows = [], []
    kinds = Counter()
    tot_same = tot_a = 0
    A = L.append
    A('# Collation report\n')
    A('Witness **A** is the corpus transcription; witness **B** is an '
      'independent re-reading of the same scan, made without sight of A. '
      'Neither is authoritative - a disagreement marks a place to check the '
      'manuscript, not a correction to apply.\n')
    body = []
    for k in keys:
        diffs, same, na, nb = collate_page(wa[k], wb[k][0], lex, dwds)
        tot_same += same; tot_a += na
        real = [d for d in diffs if d['kind'] != 'convention']
        for d in real:
            kinds[d['kind']] += 1
            rows.append({'letter': k[0], 'page': k[1], 'kind': d['kind'],
                         'witness_a': d['a'], 'witness_b': d['b'],
                         'context_a': d['ctx']})
        agree = same / na * 100 if na else 0
        body.append(f'\n## Letter {k[0]}, page {k[1]}\n')
        body.append(f'A: {na} tokens · B: {nb} tokens · '
                    f'**{agree:.0f}% agreement** · {len(real)} disagreements\n')
        if real:
            body.append('| Kind | Witness A | Witness B | Context (A) |')
            body.append('|---|---|---|---|')
            order = {'numeral': 0, 'name': 1, 'word/nonword': 2,
                     'B-only': 3, 'A-only': 4, 'both-words': 5}
            for d in sorted(real, key=lambda x: order.get(x['kind'], 9)):
                f = lambda s: (s or '—').replace('|', '/')[:70]
                body.append(f"| {d['kind']} | `{f(d['a'])}` | `{f(d['b'])}` | "
                            f"{f(d['ctx'])} |")
        body.append('')

    A(f'**{len(keys)} page(s) collated** · overall token agreement '
      f'**{tot_same/tot_a*100:.1f}%** · {sum(kinds.values())} disagreements\n')
    if surprises:
        A('\n### Language declarations that differ from expectation\n')
        A('Witness B declares the language it reads on each page, judged from the '
          'page alone. These came back other than expected — settle them before '
          'reading anything into their disagreement counts, since a page collated '
          'across two languages will show near-total disagreement for a trivial '
          'reason.\n')
        A('| Page | Expected | B declared |')
        A('|---|---|---|')
        for (lt, pg), exp, got in surprises:
            A(f'| L{lt} p{pg} | {exp} | **{got}** |')
        A('')
    A('| Kind | Count | What to do |')
    A('|---|---|---|')
    todo = {'numeral': 'check every one against the manuscript - figures are the '
                       'one class with no internal safety net',
            'name': 'check against the manuscript and the name canon',
            'word/nonword': 'the known word usually wins; verify then apply',
            'B-only': 'usually marginalia the corpus dropped - decide whether to add',
            'A-only': 'B saw nothing; often a genuine A reading, sometimes a drop',
            'both-words': 'only context decides - read the passage'}
    for kind, n in sorted(kinds.items(), key=lambda x: -x[1]):
        A(f'| {kind} | {n} | {todo.get(kind, "")} |')
    L.extend(body)

    with open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    with open(QUEUE, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, ['letter', 'page', 'kind', 'witness_a',
                               'witness_b', 'context_a'])
        w.writeheader(); w.writerows(rows)
    print(f'{len(keys)} page(s) · {tot_same/tot_a*100:.1f}% token agreement · '
          f'{sum(kinds.values())} disagreements')
    for kind, n in sorted(kinds.items(), key=lambda x: -x[1]):
        print(f'   {kind:<14} {n}')
    if surprises:
        print('\n   language surprises:')
        for (lt, pg), exp, got in surprises:
            print(f'     L{lt} p{pg}: expected {exp}, B declared {got}')
    print(f'\nwrote {REPORT}\nwrote {QUEUE}')


if __name__ == '__main__':
    main()
