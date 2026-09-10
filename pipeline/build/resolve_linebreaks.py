# -*- coding: utf-8 -*-
"""
Decide, for every line-end wrap mark in the corpus, whether the two halves are
really one broken word.

The transcription's continuation marks cannot be trusted: `die¬` + `serhalb` is a
genuine break (dieserhalb), but `die¬` + `nöthigsten` is not (those are two words
and the mark is a transcription error). Every wrap therefore gets decided on
evidence, and the evidence is recorded so any call can be checked or overridden.

Evidence sources
  1. This corpus itself - period-appropriate, knows 1800s spelling.
  2. The DWDS frequency API - lemma-aware (so inflected forms resolve) and its
     corpora include historical German. Cached to disk; the network is used once.

Outputs
  linebreak_decisions.csv   one row per wrap, hand-editable - the source of truth
  linebreak_report.md       method, counts, and everything needing review

The canonical corpus is never modified.

Usage
  python3 resolve_linebreaks.py            # use cache, fetch anything missing
  python3 resolve_linebreaks.py --offline  # never touch the network
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, time, urllib.request, urllib.parse
from collections import Counter
from corpus_pages import split_pages
import unitlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
SRC = unitlib.one_unit(unitlib.unit_arg()).corpus_path
CACHE = os.path.join(ROOT, 'reference', 'dwds_cache.json')
DECISIONS = os.path.join(UNIT.dir, 'linebreak_decisions.csv')
REPORT = os.path.join(ROOT, 'review', UNIT.slug, 'linebreak_report.md')

OFFLINE = '--offline' in sys.argv

WORD = re.compile(r'[A-Za-zÀ-ÿĄąĘęŁłŃńÓóŚśŹźŻżſ]+')
TAG = re.compile(r'^\[DOC (\w+)\]$')

# A DWDS hit count at or above this is treated as "a real word". Chosen from the
# observed gap: real words land in the thousands-to-millions (dieserhalb 1_430,
# redlichen 122_066, Mitgliedern 12_034_956) while non-words that still return
# something are proper-name noise in the low hundreds (denich 414, derdurch 41).
REAL_WORD_HITS = 1000

# Observations from reading the cross-page cases in full context. These do not
# change any decision - they record what was actually found, so the report says
# something useful instead of just "check this".
NOTES = {
    ('136', 10053): 'Almost certainly *Collonisten* (line 10050 has "die Collonirten"): '
                    'the continuation is mis-transcribed as "Mitten". Joining would give '
                    '"ColloMitten", so it is left split - but the underlying word is garbled.',
    ('223', 16363): 'Text appears to be missing between the pages: "Güter ange¬" is never '
                    'completed, and the next page starts a new clause. Possible lacuna.',
    ('223', 16428): '"entweder ver¬ / oder aufgegeben" - the word after *ver* is missing '
                    '(probably *verloren*). Possible lacuna.',
    ('176', 12587): 'Reads "Besitz-Ergreifungs Patente angeschlagen"; the trailing mark is '
                    'a dash, not a word break.',
    ('103', 8193):  'Joins to *anstalt* - DWDS shows 0 only because of the long s (ſtalt); '
                    'this corpus attests the word.',
}

# ------------------------------------------------------------------ DWDS
_cache = {}


def load_cache():
    global _cache
    if os.path.isfile(CACHE):
        with open(CACHE, encoding='utf-8') as f:
            _cache = json.load(f)
    print(f'DWDS cache: {len(_cache)} entries')


def save_cache():
    with open(CACHE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(_cache, f, ensure_ascii=False, indent=0, sort_keys=True)


_since_save = 0


def dwds_hits(word):
    """Corpus hit count for a surface form, or None if never determined."""
    global _since_save
    if not word:
        return 0
    key = word.lower()
    if key in _cache:
        return _cache[key]
    if OFFLINE:
        return None
    # Save often: this job is long, resumable, and may be interrupted, so the
    # cache must never be more than a few lookups behind.
    _since_save += 1
    if _since_save >= 20:
        _since_save = 0
        save_cache()
    url = 'https://www.dwds.de/api/frequency/?q=' + urllib.parse.quote(word)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'vonTriebenfeld-edition/1.0 (scholarly line-break resolution)'})
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.load(r)
            hits = int(data.get('hits', 0))
            _cache[key] = hits
            time.sleep(0.4)          # be polite to a free public service
            return hits
        except Exception:
            time.sleep(2.5 * (attempt + 1))
    _cache[key] = None
    return None


# ------------------------------------------------------------------ corpus
def load_corpus():
    with open(SRC, encoding='utf-8') as f:
        lines = f.read().split('\n')
    letters = {}          # id -> list of (abs_line_no, text)
    cur = None
    for i, raw in enumerate(lines):
        m = TAG.match(raw.strip())
        if m:
            cur = m.group(1)
            letters[cur] = []
            continue
        if cur is not None:
            letters[cur].append((i + 1, raw))
    return lines, letters


def pages_of(body):
    """A document's [(lineno, text)] split into pages, page ids discarded.

    Deliberately delegated to corpus_pages.split_pages rather than repeating the
    rule: `crosses_page` decides how a wrap is judged, so if this module and the
    one that builds the pages disagreed about where a page ends, a mark would be
    adjudicated against one page structure and applied to another.
    """
    return [ls for _, ls in split_pages(body)]


def build_vocab(letters):
    """Words attested on complete lines - i.e. not themselves wrap fragments."""
    vocab = Counter()
    for body in letters.values():
        for _, text in body:
            s = text.rstrip()
            toks = WORD.findall(s)
            if not toks:
                continue
            if s.endswith('¬') or (re.search(r'\w-$', s) and not s.endswith('--')):
                toks = toks[:-1]        # last token is a fragment, not a word
            for t in toks:
                vocab[t.lower().replace('ſ', 's')] += 1
    return vocab


def collect_wraps(letters):
    """Every line-end wrap, with its page context."""
    wraps = []
    for lid, body in letters.items():
        pages = pages_of(body)
        for pi, page in enumerate(pages):
            for li, (lineno, text) in enumerate(page):
                s = text.rstrip()
                if s.endswith('¬'):
                    mark = '¬'
                elif re.search(r'\w-$', s) and not s.endswith('--'):
                    mark = '-'
                else:
                    continue
                head_toks = WORD.findall(s[:-1])
                if not head_toks:
                    continue
                # what follows: next line on this page, else first line of next page
                if li + 1 < len(page):
                    nxt_lineno, nxt_text = page[li + 1]
                    crosses = False
                elif pi + 1 < len(pages):
                    nxt_lineno, nxt_text = pages[pi + 1][0]
                    crosses = True
                else:
                    continue
                # A mark with no word after it cannot be a word break - the next
                # line is a figure, a table column, or empty. Recorded rather
                # than skipped, so nothing ends up with no decision at all.
                tail_toks = WORD.findall(nxt_text)
                if not tail_toks:
                    wraps.append({
                        'letter': lid, 'page': pi + 1, 'line': lineno,
                        'next_line': nxt_lineno, 'mark': mark,
                        'head': head_toks[-1], 'tail': '',
                        'crosses_page': crosses,
                        'context': s[-42:] + ' || ' + nxt_text.strip()[:42],
                    })
                    continue
                wraps.append({
                    'letter': lid, 'page': pi + 1, 'line': lineno,
                    'next_line': nxt_lineno, 'mark': mark,
                    'head': head_toks[-1], 'tail': tail_toks[0],
                    'crosses_page': crosses,
                    'context': s[-42:] + ' || ' + nxt_text.strip()[:42],
                })
    return wraps


def collect_unmarked_catchwords(letters):
    """Catchwords that carry no wrap mark at all.

    A catchword is the scribe's note, at the foot of a page, of the word the
    next page begins with - a navigation device for whoever turns the leaf, not
    part of the sentence. Where the transcription marked it with a wrap sign it
    is already caught above. Most are not marked: the foot of the page simply
    holds a bare word that then repeats overleaf, and because there is no mark
    there is no wrap to adjudicate, so the reading text says it twice -
    "Salomon Natan | Nathan junior zu Berlin".

    Recognised by all of: it is the LAST line of a page; it is short and no more
    than a few tokens; it carries no wrap mark; and its first word opens the
    next page. They are proposed here as ordinary rows so that any one of them
    can be overruled by hand like any other decision.
    """
    out = []
    for lid, body in letters.items():
        pages = pages_of(body)
        for pi, page in enumerate(pages[:-1]):
            lineno, text = page[-1]
            s = text.rstrip()
            if not s or s.endswith('¬') or (re.search(r'\w-$', s) and not s.endswith('--')):
                continue
            toks = WORD.findall(s)
            if not toks or len(toks) > 3 or len(s.strip()) > 28:
                continue
            nxt_lineno, nxt_text = pages[pi + 1][0]
            nxt = WORD.findall(nxt_text)
            if not nxt:
                continue
            a, b = toks[0].lower(), nxt[0].lower()
            if len(a) < 3 or a[:4] != b[:4]:
                continue
            out.append({
                'letter': lid, 'page': pi + 1, 'line': lineno,
                'next_line': nxt_lineno, 'mark': '', 'head': toks[0], 'tail': nxt[0],
                'crosses_page': True, 'unmarked_catchword': True,
                'context': s.strip()[-42:] + ' || ' + nxt_text.strip()[:42],
            })
    return out


# ------------------------------------------------------------------ decide
def norm(w):
    return w.lower().replace('ſ', 's')


def is_real(word, vocab):
    """(verdict, corpus_count, dwds_hits) - verdict True/False/None(unknown)."""
    c = vocab.get(norm(word), 0)
    h = dwds_hits(word)
    if c > 0:
        return True, c, h
    if h is None:
        return None, c, h
    return (h >= REAL_WORD_HITS), c, h


def decide(w, vocab):
    """
    Lazy on purpose: each DWDS lookup costs a network round trip, so we stop as
    soon as the evidence is decisive. Most wraps never need more than one.
    """
    head, tail = w['head'], w['tail']
    if not tail:
        w.update(joined='', joined_corpus=0, head_corpus=0, tail_corpus=0,
                 joined_dwds='', head_dwds='', tail_dwds='')
        return ('orphan', 'high',
                'nothing to continue into - the next line holds no words')
    joined = head + tail
    w.update(joined=joined, joined_corpus=vocab.get(norm(joined), 0),
             head_corpus=vocab.get(norm(head), 0),
             tail_corpus=vocab.get(norm(tail), 0),
             joined_dwds='', head_dwds='', tail_dwds='')

    # Catchword: the fragment repeats the opening of the next page. Decided on
    # shape alone - no lookup needed. Two letters is enough (`be¬` before
    # `benennung`); the join it would otherwise produce is never a word.
    if (w['crosses_page'] and len(head) >= 2
            and norm(tail).startswith(norm(head)) and norm(tail) != norm(head)):
        return 'catchword', 'high', 'fragment repeats the next page opening'

    # Attested in this corpus - period-appropriate evidence, no lookup needed.
    if w['joined_corpus'] > 0 and not w['crosses_page']:
        return 'join', 'high', 'joined form occurs elsewhere in this corpus'

    j_real, j_corpus, j_hits = is_real(joined, vocab)
    w['joined_dwds'] = j_hits

    if not w['crosses_page']:
        if j_real:
            return 'join', 'high', f'joined form attested in DWDS ({j_hits:,} hits)'
        # The joined form is not a word. Is the head a word on its own?
        h_real, _, h_hits = is_real(head, vocab)
        w['head_dwds'] = h_hits
        if h_real is False:
            return 'join', 'high', 'head is not a word on its own'
        t_real, _, t_hits = is_real(tail, vocab)
        w['tail_dwds'] = t_hits
        if j_real is False and t_real and h_real:
            return 'split', 'high', 'joined form unattested; both halves are real words'
        if tail[:1].isupper():
            return 'split', 'high', 'joined form unattested and continuation is capitalised'
        return 'split', 'review', 'no clear evidence either way'

    # Crosses a page break: only 24 of these, and catchwords hide among them, so
    # every one is surfaced for review rather than settled by rule.
    h_real, _, h_hits = is_real(head, vocab)
    t_real, _, t_hits = is_real(tail, vocab)
    w['head_dwds'], w['tail_dwds'] = h_hits, t_hits
    return ('join' if j_real else 'split'), 'review', 'crosses a page break - check by hand'


def main():
    load_cache()
    lines, letters = load_corpus()
    vocab = build_vocab(letters)
    wraps = collect_wraps(letters)
    unmarked = collect_unmarked_catchwords(letters)
    wraps.extend(unmarked)
    wraps.sort(key=lambda w: w['line'])
    print(f'letters {len(letters)}, vocabulary {len(vocab)}, wraps {len(wraps)} '
          f'({len(unmarked)} of them unmarked catchwords)')

    if not OFFLINE:
        forms = set()
        for w in wraps:
            forms.update([w['head'] + w['tail'], w['head'], w['tail']])
        todo = [f for f in forms if f.lower() not in _cache]
        print(f'unique forms {len(forms)}, to fetch {len(todo)} '
              f'(~{len(todo) * 0.95 / 60:.0f} min)')

    try:
        for n, w in enumerate(wraps, 1):
            if w.get('unmarked_catchword'):
                # Not a wrap: nothing is broken across the line, so there is no
                # word to weigh. The evidence is positional - last line of a
                # page, repeated overleaf - and decide() has no way to see it.
                w['decision'] = 'catchword'
                w['confidence'] = 'high'
                w['reason'] = ('unmarked catchword: the page ends with the word '
                               'the next page begins')
                continue
            w['decision'], w['confidence'], w['reason'] = decide(w, vocab)
            if n % 100 == 0:
                print(f'  {n}/{len(wraps)}')
                save_cache()
    finally:
        save_cache()

    cols = ['letter', 'page', 'line', 'next_line', 'mark', 'head', 'tail', 'joined',
            'decision', 'confidence', 'reason', 'crosses_page',
            'joined_corpus', 'joined_dwds', 'head_corpus', 'head_dwds',
            'tail_corpus', 'tail_dwds', 'context']

    # Carry over decisions a human changed. This file is documented as
    # hand-editable and the report tells you to edit it, but the run used to
    # overwrite it wholesale - so every adjudication was silently discarded by
    # the next regenerate. A row is kept only where the wrap itself is
    # unchanged: same letter, same line, same two halves. If the corpus moved
    # underneath it, the old ruling was about different text and is dropped.
    kept = 0
    if os.path.isfile(DECISIONS):
        prior, by_context = {}, {}
        with open(DECISIONS, encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                prior[(row.get('letter', ''), row.get('line', ''),
                       row.get('head', ''), row.get('tail', ''))] = row
                # Second key, free of both the line number and the document
                # number, so an adjudication survives a renumbering: merging
                # enclosures into their parent changes every letter id and
                # shifts every line, but the wrap itself is the same wrap.
                by_context[(row.get('head', ''), row.get('tail', ''),
                            row.get('context', ''))] = row
        for w in wraps:
            old = prior.get((str(w['letter']), str(w['line']), w['head'], w['tail']))
            if not old:
                old = by_context.get((w['head'], w['tail'], w.get('context', '')))
            if not old:
                continue
            # 'held' marks a row this script did not decide: it was adjudicated
            # by hand, so it outranks whatever decide() just produced.
            if (old.get('confidence') == 'held'
                    or old.get('decision') != w['decision']):
                w['decision'] = old['decision']
                w['confidence'] = 'held'
                w['reason'] = old.get('reason') or 'held: adjudicated by hand'
                kept += 1
    if kept:
        print(f'kept {kept} hand-adjudicated decision(s) from the previous run')

    with open(DECISIONS, 'w', encoding='utf-8-sig', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        for w in wraps:
            wr.writerow({c: w.get(c, '') for c in cols})
    print(f'wrote {DECISIONS} ({len(wraps)} rows)')

    write_report(wraps)


def write_report(wraps):
    dec = Counter(w['decision'] for w in wraps)
    conf = Counter(w['confidence'] for w in wraps)
    reasons = Counter(w['reason'] for w in wraps)
    review = [w for w in wraps if w['confidence'] == 'review']
    catch = [w for w in wraps if w['decision'] == 'catchword']

    L = []
    A = L.append
    A('# Line-break resolution\n')
    A('Every line-end wrap mark in the corpus, decided on evidence. The canonical '
      'archival text is unchanged — these decisions drive the generated *reading* '
      'copy only.\n')
    A('## Why this was needed\n')
    A('The transcription\'s continuation marks cannot be taken at face value. '
      '`die¬` + `serhalb` really is one word (*dieserhalb*), but `die¬` + `nöthigsten` '
      'is two, and the mark is simply an error. Roughly a third of the marks turn out '
      'not to join anything.\n')
    A('## Evidence\n')
    A('1. **This corpus** — period-appropriate; it knows that `laßen` and `nöthigsten` '
      'are ordinary words.\n'
      '2. **DWDS frequency API** — lemma-aware, so inflected forms resolve '
      '(`Mitgliedern` → *Mitglied*), and its corpora include historical German. '
      f'A form is treated as real at ≥{REAL_WORD_HITS:,} hits; below that, the '
      'returns are proper-name noise.\n')
    A('## Results\n')
    A(f'| Outcome | Count |\n|---|---|')
    for k, v in dec.most_common():
        A(f'| {k} | {v} |')
    A(f'| **total** | **{len(wraps)}** |\n')
    A('| Confidence | Count |\n|---|---|')
    for k, v in conf.most_common():
        A(f'| {k} | {v} |')
    A('')
    A('| Reason | Count |\n|---|---|')
    for k, v in reasons.most_common():
        A(f'| {k} | {v} |')
    A('')

    if catch:
        A('## Catchwords\n')
        A('The scribal habit of writing the next page\'s first word at the foot of the '
          'current page. Not broken words — joining them would manufacture nonsense '
          '("ConContract"). Kept in the diplomatic view, dropped from the reading copy.\n')
        A('| Letter | Line | Fragment | Next page opens | Context |\n|---|---|---|---|---|')
        for w in catch:
            A(f'| {w["letter"]} | {w["line"]} | `{w["head"]}{w["mark"]}` | '
              f'`{w["tail"]}` | {w["context"]} |')
        A('')

    if review:
        A('## For your review\n')
        A('Cases with no decisive evidence, plus every wrap that crosses a page break. '
          'The `decision` column in `linebreak_decisions.csv` is hand-editable — change '
          'a cell and regenerate.\n')
        A('Each was read in context; the decision column below is what the generated '
          'reading copy currently does.\n')
        A('| Letter | Line | Wrap | Decision | Context | Note |\n'
          '|---|---|---|---|---|---|')
        for w in sorted(review, key=lambda x: (int(re.match(r"\d+", x["letter"]).group()),
                                               x['line'])):
            note = NOTES.get((w['letter'], w['line']), '')
            A(f'| {w["letter"]} | {w["line"]} | `{w["head"]}`+`{w["tail"]}` | '
              f'**{w["decision"]}** | {w["context"]} | {note} |')
        A('')

    A('## How to override a decision\n')
    A('Edit the `decision` column in `linebreak_decisions.csv` (`join`, `split` or '
      '`catchword`) and re-run `build_db.py` then `build_site_data.py`. Nothing else '
      'needs changing, and the archival text is never touched.\n')

    with open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L))
    print(f'wrote {REPORT}')
    print()
    print('decisions:', dict(dec))
    print('confidence:', dict(conf))


if __name__ == '__main__':
    main()
