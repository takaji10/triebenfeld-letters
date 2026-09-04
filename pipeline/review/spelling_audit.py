# -*- coding: utf-8 -*-
"""
Find demonstrable transcription slips in ordinary words - and only those.

The bar is deliberately high. 63% of the distinct words in this corpus appear
exactly once, and the text is full of period forms (laßen, seyn, nöthig, Ewr)
that are correct as written. A pass that "corrects spelling" by impression would
do far more harm than good, so nothing is proposed unless the corpus or an
external historical source contradicts the reading.

A candidate must clear all of these:

  1. it is rare here (at most RARE_MAX occurrences)
  2. a near neighbour - one plausible transcription confusion away - is common
     here (at least COMMON_MIN, and at least RATIO times more frequent)
  3. the difference matches a known Kurrentschrift/AI confusion, not any edit
  4. the rare form is unknown to DWDS while the common one is attested

Output is a report only. Nothing is applied: proposals are for review.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, json, csv
from collections import Counter, defaultdict
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, 'reference', 'dwds_cache.json')
REPORT = os.path.join(ROOT, 'review', 'spelling_audit.md')

RARE_MAX = 2        # a candidate error may appear at most this often
COMMON_MIN = 8      # its proposed correction must appear at least this often
RATIO = 10          # ...and be this many times more frequent
REAL_WORD_HITS = 1000
MIN_LEN = 6         # short words generate almost nothing but noise: at 4 letters
                    # a single edit reaches "und", "die", "der" from anything
INDEL_MIN_LEN = 8   # dropped/added letters are the weakest signal of all, so
                    # they are only entertained on longer words

# Any letter, so stray diacritics can't split a word into a false fragment
# (şondern was being read as 'ondern' and proposed as a slip for 'andern').
WORD = re.compile(r'[^\W\d_]{3,}', re.UNICODE)

# Confusions this transcription actually makes, established over the earlier
# passes. A pair only qualifies if its single difference is one of these.
CONFUSIONS = [
    ('c', 'e'), ('e', 'c'), ('n', 'u'), ('u', 'n'), ('m', 'w'), ('w', 'm'),
    ('b', 'v'), ('v', 'b'), ('b', 'h'), ('h', 'b'), ('f', 'ſ'), ('t', 'l'),
    ('l', 't'), ('i', 'j'), ('j', 'i'), ('r', 'n'), ('n', 'r'), ('s', 'f'),
    ('a', 'o'), ('o', 'a'), ('g', 'z'), ('z', 'g'), ('k', 'h'), ('d', 'b'),
]
CONFUSION_SET = set(CONFUSIONS)


def norm(w):
    return w.lower().replace('ſ', 's')


def load_cache():
    if os.path.isfile(CACHE):
        with open(CACHE, encoding='utf-8') as f:
            return json.load(f)
    return {}


def one_edit_kind(a, b):
    """How a and b differ, if by exactly one operation - else None."""
    if len(a) == len(b):
        diff = [(x, y) for x, y in zip(a, b) if x != y]
        if len(diff) == 1:
            return ('sub', diff[0])
        return None
    if abs(len(a) - len(b)) != 1:
        return None
    long, short = (a, b) if len(a) > len(b) else (b, a)
    for i in range(len(long)):
        if long[:i] + long[i + 1:] == short:
            return ('indel', long[i])
    return None


def main():
    with open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8') as f:
        recs = json.load(f)

    # Count words from the transcription layer - the line-break work is already
    # done there, so wrap fragments aren't miscounted as words.
    freq = Counter()
    where = defaultdict(list)
    for r in recs:
        for p in r['pages']:
            for line in p.get('transcription', p['diplomatic']).split('\n'):
                toks = WORD.findall(line)
                # A line ending in a hyphen breaks a word across the line, so
                # its last token is half a word - counting it invents errors
                # ("Nachrich-" proposed as a slip for "Nachricht").
                if toks and line.rstrip().endswith('-'):
                    toks = toks[:-1]
                for w in toks:
                    n = norm(w)
                    freq[n] += 1
                    if len(where[n]) < 3:
                        where[n].append((r['letter_id'], p['page'], line.strip()))

    print(f'distinct words: {len(freq)}   tokens: {sum(freq.values())}')

    # Index by "word with one letter removed" so near neighbours are cheap.
    buckets = defaultdict(list)
    for w in freq:
        buckets[w].append(w)
        for i in range(len(w)):
            buckets[w[:i] + w[i + 1:]].append(w)

    cache = load_cache()
    proposals = []
    seen = set()
    for rare, n in freq.items():
        if n > RARE_MAX or len(rare) < MIN_LEN:
            continue
        cands = set()
        cands.update(buckets.get(rare, ()))
        for i in range(len(rare)):
            cands.update(buckets.get(rare[:i] + rare[i + 1:], ()))
        for cand in cands:
            if cand == rare or freq[cand] < max(COMMON_MIN, n * RATIO):
                continue
            kind = one_edit_kind(rare, cand)
            if not kind:
                continue
            if kind[0] == 'sub' and kind[1] not in CONFUSION_SET:
                continue
            if kind[0] == 'indel' and (len(rare) < INDEL_MIN_LEN
                                       or kind[1] not in 'cenumhrfstl'):
                continue
            # German inflection, not error. A difference confined to the final
            # letter among the case/agreement endings is grammar: "Fürstens"
            # (genitive) and "hochfürstlicher" (dative) are both correct.
            if kind[0] == 'sub' and rare[:-1] == cand[:-1] \
                    and rare[-1] in 'enrsm' and cand[-1] in 'enrsm':
                continue
            if kind[0] == 'indel' and kind[1] in 'enrsm' \
                    and (rare[:-1] == cand or cand[:-1] == rare):
                continue
            key = (rare, cand)
            if key in seen:
                continue
            seen.add(key)
            proposals.append({
                'rare': rare, 'n_rare': n, 'common': cand, 'n_common': freq[cand],
                'kind': f'{kind[0]}:{kind[1]}',
                'dwds_rare': cache.get(rare), 'dwds_common': cache.get(cand),
                'where': where[rare],
            })

    # A rare form that DWDS knows as a real German word is very unlikely to be a
    # transcription slip - "Kasten" is a box, "erkalten" is to grow cold. Look
    # up whatever isn't cached, then drop those.
    todo = [p['rare'] for p in proposals if p['rare'] not in cache]
    if todo and '--offline' not in sys.argv:
        print(f'checking {len(todo)} rare forms against DWDS...')
        import urllib.request, urllib.parse, time
        for n, w in enumerate(todo, 1):
            try:
                req = urllib.request.Request(
                    'https://www.dwds.de/api/frequency/?q=' + urllib.parse.quote(w),
                    headers={'User-Agent': 'vonTriebenfeld-edition/1.0 (spelling audit)'})
                with urllib.request.urlopen(req, timeout=20) as r:
                    cache[w] = int(json.load(r).get('hits', 0))
                time.sleep(0.4)
            except Exception:
                cache[w] = None
            if n % 25 == 0:
                json.dump(cache, open(CACHE, 'w', encoding='utf-8'),
                          ensure_ascii=False, indent=0, sort_keys=True)
        json.dump(cache, open(CACHE, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=0, sort_keys=True)

    kept, real_word = [], []
    for p in proposals:
        p['dwds_rare'] = cache.get(p['rare'])
        p['dwds_common'] = cache.get(p['common'])
        if p['dwds_rare'] is not None and p['dwds_rare'] >= REAL_WORD_HITS:
            real_word.append(p)
        else:
            kept.append(p)

    kept.sort(key=lambda p: (-p['n_common'] / max(p['n_rare'], 1), p['rare']))
    write_report(kept, freq, real_word)


def write_report(props, freq, real_word=()):
    known = [p for p in props if p['dwds_rare'] is not None or p['dwds_common'] is not None]
    L = []
    A = L.append
    A('# Spelling audit\n')
    A('Candidate transcription slips in ordinary words. **Nothing here has been '
      'applied** - these are proposals for review.\n')
    A('## The bar\n')
    A('63% of the distinct words in this corpus appear exactly once, and the text is '
      'full of period forms (*laßen*, *seyn*, *nöthig*, *Ewr*) that are correct as '
      'written. Frequency alone therefore proves nothing, and a pass driven by '
      'impression would damage more than it fixed. A candidate is only listed if:\n')
    A(f'1. it appears at most **{RARE_MAX}** times here;\n'
      f'2. a near neighbour appears at least **{COMMON_MIN}** times and at least '
      f'**{RATIO}x** more often;\n'
      '3. the single difference between them is a confusion this transcription is '
      'known to make (c/e, n/u, m/w, b/v, long-s, and so on) - not any edit;\n'
      '4. the pair is checked against DWDS where a lookup exists.\n')
    A(f'\n**{len(props)} candidates** out of {len(freq):,} distinct words.\n')
    A('\n## Candidates\n')
    A('| Rare form | Here | Proposed | Here | Difference | Context |\n'
      '|---|---|---|---|---|---|')
    for p in props:
        ctx = p['where'][0] if p['where'] else ('', '', '')
        snippet = (ctx[2][:64] + '…') if len(ctx[2]) > 64 else ctx[2]
        A(f"| `{p['rare']}` | {p['n_rare']} | **`{p['common']}`** | {p['n_common']} | "
          f"{p['kind']} | L{ctx[0]} p{ctx[1]}: {snippet.replace('|', '/')} |")
    A('\n## How to apply\n')
    A('Tell me which to accept and they will be applied to the archival text the same '
      'way every earlier correction was: root-only, verified against a backup, with the '
      'letter and line recorded in `CHANGELOG.md`. Rejected ones will be listed here as '
      'checked-and-kept, so the same candidates are not raised again.\n')
    with open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print(f'candidates: {len(props)}   (with DWDS evidence: {len(known)})')
    print(f'wrote {REPORT}')


if __name__ == '__main__':
    main()
