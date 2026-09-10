# -*- coding: utf-8 -*-
"""
One sheet for every transcription fix the translator proposed, anchored to the
manuscript.

Translating a document is the most thorough reading it ever gets, and the
translator reports what it could not make sense of. Those reports land in three
places and in three shapes:

    review/<slug>/transcription_candidates.csv   the corrupt token never reached
                                                 the English - the translation is
                                                 sound, the transcription is not
    review/<slug>/translation_review.csv         emendation-degrades: the corrupt
                                                 token rode into the English
                                                 emendation-uncertain: hedged

What none of them carry is where to look. A row saying `verbühren` should read
`verliehen` on page 2 of document 2 is a claim about a manuscript page, and
checking it means finding that word in corpus.txt first. This resolves each
proposal to its page id, its absolute corpus line, and the line as transcribed,
and sorts them so the ones that can be settled quickly come first.

    python transcription_fixes.py --unit oe1bu14526

Nothing is applied. The sheet has an empty `decision` column, exactly like
uncertainty_review.csv: fill it in, and apply_transcription_fixes.py acts on it.

CONFIDENCE is about how easy the row is to check, never about whether the
proposal is right:

    line        the German is on one corpus line, and only there in the document
    lines       it spans a line break - the transcription is what to look at
    repeated    it occurs more than once in the document; every hit is listed
    hedged      the proposal itself is uncertain ('X or Y', 'X [?]')
    unlocated   not found in the document at all - usually because the model
                quoted the reading text, which resolves abbreviations
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, difflib, argparse
from collections import defaultdict, Counter

import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SOURCES = [('transcription_candidates.csv', ('transcription-note',)),
           ('translation_review.csv', ('emendation-degrades',
                                       'emendation-uncertain'))]

# how quickly a row can be checked, best first
ORDER = {'line': 0, 'lines': 1, 'repeated': 2, 'hedged': 3, 'unlocated': 4}
WORD = re.compile(r'[^\W\d_]+', re.UNICODE)
STRIP = """.,;:()[]"'¬"""


def hedged(proposed):
    return ('?' in proposed or '/' in proposed or '[' in proposed
            or ' or ' in proposed.lower())


def word_pairs(before, after):
    """The individual word substitutions a proposal amounts to, or None."""
    a, b = before.split(), after.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if tag == 'equal':
            continue
        if tag != 'replace' or (i2 - i1) != (j2 - j1):
            return None
        out.extend(zip(a[i1:i2], b[j1:j2]))
    return out


def why_open(r, freq, names):
    """Why this row still needs a person, in the words of the thing it needs.

    Everything a rule can settle has been settled; what is left is the part
    that turns on judgement, and the reader of the sheet should be told which
    kind of judgement each row is asking for rather than made to work it out.
    """
    if r['confidence'] == 'unlocated':
        return 'not located - the model quoted the reading text, not the page'
    if r['confidence'] == 'hedged':
        return 'the proposal is itself uncertain'
    if r['confidence'] == 'repeated':
        return 'occurs more than once on the page'
    pairs = word_pairs(r['transcribed'], r['proposed'])
    if not pairs:
        return 'rewrites the passage rather than a word'
    for old, new in pairs:
        o, n = old.strip(STRIP), new.strip(STRIP)
        if any(c.isdigit() for c in o + n):
            return 'changes a figure - never re-derived, only read'
        near = near_name(o, names) or near_name(n, names)
        if near:
            return f'a name ({near}) - the spelling is an editorial decision'
        if freq.get(o, 0) > 2:
            return (f'{o} occurs {freq.get(o)}x here - the claim is that this '
                    f'reading is wrong, not that the word is')
        if difflib.SequenceMatcher(a=o.lower(), b=n.lower()).ratio() < 0.62:
            return f'{o} -> {n} is a reading of a corrupt word, not a slip'
    return ''


def near_name(w, names):
    """Is this word a spelling of somebody or somewhere the edition knows?

    Exact membership is not enough: these proposals are about variant spellings
    precisely, so `Wittowes` never matches `Witow` outright.
    """
    lw = w.lower()
    if len(lw) < 5:
        return ''
    for nm in names:
        if lw == nm or lw.startswith(nm) or nm.startswith(lw):
            return nm
        if difflib.SequenceMatcher(a=lw, b=nm).ratio() >= 0.7:
            return nm
    return ''


def corpus_frequency(slug):
    freq = Counter()
    for u in unitlib.load_units():
        p = os.path.join(u.dir, u.get('corpus') or 'corpus.txt')
        if os.path.isfile(p):
            freq += Counter(WORD.findall(io.open(p, encoding='utf-8').read()))
    return freq


def authority_names():
    sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))
    from entities import load_people, load_places
    out = set()
    for _, display, _ in load_people():
        out.update(w.lower() for w in WORD.findall(display))
    for variant, canon in load_places().items():
        out.update(w.lower() for w in WORD.findall(variant))
        out.update(w.lower() for w in WORD.findall(canon))
    return {w for w in out if len(w) >= 5}


def find_in_page(needle, lines):
    """Where a proposed token sits, tolerating the line breaks around it.

    The translator quotes the reading text, in which a word broken across two
    lines is whole again. Matching that against the diplomatic lines means
    letting whitespace in the needle match a line break, and letting the
    line-end marks the transcription uses fall between the halves.
    """
    joined, offsets = [], []
    for i, line in enumerate(lines):
        offsets.append(sum(len(x) + 1 for x in joined))
        joined.append(line)
    hay = '\n'.join(joined)
    # whitespace in the needle -> any run of space, line-end mark or newline
    pat = r'[\s=\-¬/]*'.join(re.escape(w) for w in needle.split())
    hits = []
    for m in re.finditer(pat, hay):
        start = m.start()
        first = sum(1 for o in offsets if o <= start) - 1
        last = first
        while last + 1 < len(offsets) and offsets[last + 1] <= m.end() - 1:
            last += 1
        hits.append((first, last))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds '
                                   'more than one')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    rev = unitlib.review_dir(slug)

    recs = [r for r in json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'),
                                      encoding='utf-8'))
            if r['unit'] == slug]
    by_pad = {r['pad']: r for r in recs}

    rows, seen = [], set()
    for fn, kinds in SOURCES:
        p = os.path.join(rev, fn)
        if not os.path.isfile(p):
            continue
        for r in csv.DictReader(io.open(p, encoding='utf-8-sig')):
            if r.get('kind') not in kinds:
                continue
            key = (r['pad'], r['page'], r['german'], r['english'])
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)

    # Decisions already given are carried across a rebuild, keyed on what the
    # row says rather than on where it sits: the sheet is re-derived whenever
    # the corpus changes, and re-deriving it must not throw away rulings.
    dest = os.path.join(rev, 'transcription_fixes.csv')
    prior = {}
    if os.path.isfile(dest):
        for r in csv.DictReader(io.open(dest, encoding='utf-8-sig')):
            if (r.get('decision') or '').strip():
                prior[(r['pad'], r['page'], r['transcribed'], r['proposed'])] = \
                    r['decision'].strip()

    freq, names = corpus_frequency(slug), authority_names()
    out, stats = [], defaultdict(int)
    for r in rows:
        rec = by_pad.get(r['pad'])
        if rec is None:
            continue
        page = next((p for p in rec['pages'] if str(p['page']) == str(r['page'])), None)
        de, prop = r['german'].strip(), r['english'].strip()
        page_id, line_no, context = '', '', ''
        if page is not None:
            page_id = page.get('page_id', '')
            lines = page['diplomatic'].split('\n')
            hits = find_in_page(de, lines)
            if len(hits) == 1:
                first, last = hits[0]
                line_no = page['line_start'] + first
                context = ' // '.join(lines[first:last + 1])
                conf = 'line' if first == last else 'lines'
            elif len(hits) > 1:
                line_no = ' '.join(str(page['line_start'] + f) for f, _ in hits)
                context = ' // '.join(lines[f] for f, _ in hits)
                conf = 'repeated'
            else:
                conf = 'unlocated'
                context = ''
        else:
            conf = 'unlocated'
        if hedged(prop) and conf != 'unlocated':
            conf = 'hedged'
        stats[conf] += 1
        row = {
            'decision': prior.get((r['pad'], str(r['page']), de, prop), ''),
            'confidence': conf,
            'letter': r['letter'], 'page': r['page'], 'page_id': page_id,
            'line': line_no, 'transcribed': de, 'proposed': prop,
            'context': context[:200], 'why': r['note'],
            'kind': r['kind'], 'pad': r['pad'],
        }
        # A ruling already applied leaves the corpus no longer reading as the
        # row records, so the row stops locating. That is the applier's
        # receipt, not an unfinished job, and it must not come back as one.
        if row['decision'] and conf == 'unlocated':
            row['needs'] = 'applied'
        else:
            row['needs'] = why_open(row, freq, names)
        out.append(row)

    out.sort(key=lambda d: (ORDER.get(d['confidence'], 9),
                            int(d['letter']) if d['letter'].isdigit() else 0,
                            int(d['page']) if str(d['page']).isdigit() else 0))

    cols = ['decision', 'needs', 'confidence', 'letter', 'page', 'page_id',
            'line', 'transcribed', 'proposed', 'context', 'why', 'kind', 'pad']
    with io.open(dest, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    # The shorter sheet: what a rule could not settle and a ruling has not.
    open_rows = [d for d in out if not d['decision'] and d['needs']
                 and d['needs'] != 'applied']
    open_rows.sort(key=lambda d: (d['needs'].split(' ')[0], d['confidence']))
    short = os.path.join(rev, 'transcription_fixes_open.csv')
    with io.open(short, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(open_rows)

    print(f'{len(out)} proposed fix(es) from {len(rows)} row(s)')
    for k in sorted(stats, key=lambda k: ORDER.get(k, 9)):
        print(f'  {k:10s} {stats[k]:4d}')
    print(f'\n{sum(1 for d in out if d["decision"])} already ruled on, '
          f'{len(open_rows)} still open')
    print(f'wrote {dest}')
    print(f'wrote {short}  (the open ones only)')
    print('fill in `decision`: y to apply, n to reject, or write the reading you '
          'want in its place')


if __name__ == '__main__':
    main()
