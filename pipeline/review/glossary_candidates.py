# -*- coding: utf-8 -*-
"""Words that may want a glossary entry, for the editor to rule on.

    python glossary_candidates.py                 # every holding
    python glossary_candidates.py --unit <slug>   # one holding: what it adds
    python glossary_candidates.py --check         # fail if a qualifying word
                                                  # in a translated holding is unruled

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
  abbrev     a short word with a full stop, or a unit after a figure (rt, gg,
             fl., Fr. d'or), recurring across documents. The termbase has no
             entries for abbreviations, so without this they were never
             offered: Fr. d'or, in 19 documents, was missed in the first batch
  latin      a Latin set phrase (de dato, in fidem, sub sigillo: a Latin
             preposition and a Latin ending) or a Latin-ending word modern
             German does not know (Actum, vigore)

A candidate already covered by reference/glossary.yml (an entry, or a ruling
under `excluded:`) is marked so; with --unit only the uncovered ones are
listed, which is the new holding's work.

--check is the gate regenerate.py runs (docs/GLOSSARY_PLAN.md, section 5). It
takes the holdings whose unit.yml status is translated or published, and fails
if any word they contain from the termbase, abbreviation or Latin probes, in
3 documents or more, is neither an entry nor ruled out. The rarity probe and
the timeline are left out of the gate: they flag spelling and events, which
want a reader, not a rule. A holding still being transcribed (draft) is not
held to it until it is translated.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import os, re, sys, csv, json, argparse, collections
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
    excluded = {' '.join(str(x.get('word', '')).lower().split()) for x in g.get('excluded') or []}
    # a ruling on an abbreviation holds with or without its full stop
    excluded |= {w.rstrip('.') for w in excluded}
    return pats, excluded


GATED = ('termbase', 'abbrev', 'latin')
GATE_DOCS = 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', default=None)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    unitlib.utf8_stdout()

    live = None
    if a.check:
        live = {u.slug for u in unitlib.load_units()
                if (u.get('status') or '') in ('translated', 'published')}
    docs = [r for r in load('corpus/letters.json')
            if (not a.unit or r['unit'] == a.unit) and (live is None or r['unit'] in live)]
    # A document wholly in Latin (the Poznań court books, 2026-10-07) is
    # translated whole: its Latin words are its language, not Latin phrases
    # set in a German or Polish sentence, and none stays in the English.
    # Left in, every common word of it (partium, quibus, Judicium)
    # qualified as a term.
    docs = [r for r in docs if (r.get('language') or '') != 'la']
    texts = {r['uid']: (r.get('text') or '').replace('ſ', 's') for r in docs}
    pats, excluded = covered()

    def is_covered(word, sample=''):
        """Answered by an entry, or ruled out. Patterns that need context (a
        title before possessionis, a preposition before Michaelis, a figure
        before rt) are tried on the sample sentence too: the word is covered if
        a match there overlaps it."""
        word = ' '.join(word.split())
        # the termbase spells some terms without umlauts (Fuerst)
        forms = {word, word.replace('ue', 'ü').replace('ae', 'ä').replace('oe', 'ö')}
        if any(f.lower() in excluded for f in forms):
            return True
        if any(p.search(f) for f in forms for p in pats):
            return True
        sample = ' '.join((sample or '').split())
        i = sample.find(word.split(': ')[-1])
        if i < 0:
            return False
        j = i + len(word.split(': ')[-1])
        return any(m.start() < j and m.end() > i for p in pats for m in p.finditer(sample))

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
            ctx = next(texts[hits[0]][max(0, m.start() - 40):m.end() + 40]
                       for m in [rx.search(texts[hits[0]])])
            rows.append({'source': 'termbase:' + section, 'term': e.get('term'),
                         'english': e.get('render') or '', 'docs': len(hits),
                         'sample': sample, 'note': e.get('gloss') or '',
                         'covered': is_covered(e.get('term') or '') or is_covered(sample, ctx)})

    # rare in modern German, frequent here
    freq = load('reference/dwds_cache.json')  # also used by the latin probe
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

    # how often a short word carries a full stop, and stands after a figure
    seen_dot, after_fig = collections.Counter(), collections.Counter()
    for t in texts.values():
        seen_dot.update(m.group(1) for m in re.finditer(r'(?<![\w.])([A-Za-zÄÖÜäöüß]{1,5})\.', t))
        after_fig.update(m.group(1) for m in re.finditer(r"\d\.?\s?([A-Za-z]{1,5})\b", t))
    # abbreviations and units. An abbreviation keeps its full stop nearly
    # every time (Ew.), where a word ends a sentence only sometimes (wird.);
    # a unit stands after a figure most times it is used (rt, gg), where a
    # word does so by chance (2 Tage). Both tests are ratios over the corpus.
    words = collections.Counter()
    for t in texts.values():
        words.update(re.findall(r"[A-Za-zÄÖÜäöüß]+", t))
    ORDINAL = {'t', 'te', 'ten', 'ter', 'tes', 'tem', 'st', 'ste', 'sten', 'ster', 'stes', 'n', 'r', 'e', 'en'}
    LATIN_PREP = r'(?:de|ad|pro|sub|ex|per|cum|sine|salvo|vigore|in)'
    LATIN_WORD = r'[a-z]+(?:um|orum|arum|ibus|ione|ionis|atis|ii|ato|ali|ali|ido|io|em)'
    GERMAN = {'dem', 'diesem', 'einem', 'seinem', 'ihrem', 'meinem', 'jedem', 'welchem', 'allem',
              'solchem', 'unserm', 'deinem', 'keinem', 'wem', 'ihm', 'sum'}
    seen = collections.defaultdict(lambda: [0, set(), ''])

    def note(key, u, t, m):
        seen[key][0] += 1; seen[key][1].add(u)
        seen[key][2] = seen[key][2] or t[max(0, m.start() - 30):m.end() + 25]

    for u, t in texts.items():
        for m in re.finditer(r'(?<![\w.])([A-Za-zÄÖÜäöüß]{1,5})\.(?=[\s,;:)])', t):
            w = m.group(1)
            if words[w] and seen_dot.get(w, 0) / words[w] >= .6:
                note(('abbrev', w + '.'), u, t, m)
        for m in re.finditer(r"\d\.?\s?((?:[A-Za-z]{1,5}\.?\s?d['’]or)|[A-Za-z]{1,5})\b", t):
            w = m.group(1)
            if w in ORDINAL:
                continue
            if "d'or" in w or "d’or" in w or (words[w] and after_fig.get(w, 0) / words[w] >= .5):
                note(('abbrev', 'after a figure: ' + w), u, t, m)
        for m in re.finditer(r'\b' + LATIN_PREP + r'\s+(' + LATIN_WORD + r')\b', t, re.I):
            if m.group(1).lower() not in GERMAN:
                note(('latin', m.group(0).lower()), u, t, m)
        for m in re.finditer(r'\b[A-Za-z]+(?:um|orum|arum|ibus|ione|ionis|atis|ii)\b', t):
            # German words ending -rum, -thum (darum, Eigenthum) are not Latin
            if (len(m.group(0)) >= 5 and m.group(0).lower() not in GERMAN
                    and not re.search(r'(?:rum|thum|tum)$', m.group(0), re.I)):
                note(('latin', m.group(0)), u, t, m)
    for (src, term), (n, where, sample) in seen.items():
        if len(where) >= 3:
            word = ' '.join(term.split(': ')[-1].split())
            term = ' '.join(term.split())
            rows.append({'source': src, 'term': term, 'english': '', 'docs': len(where),
                         'sample': sample.replace('\n', ' '), 'note': f'{n} uses',
                         'covered': is_covered(word, sample)})

    # events
    if not a.unit:
        for ev in load('site/_data/timeline.yml') or []:
            rows.append({'source': 'event', 'term': ev.get('title'), 'english': '',
                         'docs': len(ev.get('refs') or []), 'sample': str(ev.get('date')),
                         'note': (ev.get('note') or '').strip()[:200],
                         'covered': False})

    if a.check:
        unruled = [r for r in rows if not r['covered'] and r['source'].split(':')[0] in GATED
                   and r['docs'] >= GATE_DOCS]
        if not unruled:
            print(f'glossary candidates: all ruled ({len(live)} translated holdings, '
                  f'{sum(1 for r in rows if r["source"].split(":")[0] in GATED and r["docs"] >= GATE_DOCS)} '
                  f'qualifying words)')
            return
        print(f'FAIL glossary candidates: {len(unruled)} word(s) in translated holdings neither '
              f'in reference/glossary.yml nor ruled out under excluded:')
        for r in sorted(unruled, key=lambda r: -r['docs']):
            print(f"  {r['term']!r} ({r['source']}, {r['docs']} documents): {r['sample'][:70]!r}")
        print('Rule each: an entry (English and German, with check_against), or a line under '
              'excluded: with the reason. See docs/NEW_UNIT.md section 8.')
        sys.exit(1)

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
