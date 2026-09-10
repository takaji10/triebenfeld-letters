# -*- coding: utf-8 -*-
"""
Where the translation admits doubt and the transcription does not.

    python unmarked_doubts.py --unit oe1bu14526

check_translations.py counts these per page and calls them `unmarked-in-german`:
the English carries `[uncertain: ...]`, `[illegible]` or `[text lost]` at a
point where the German has no `[?]` and no `[...]`. They are the most valuable
rows it produces, because a marker the transcription never set is corruption
nobody has flagged - the reading looked fluent enough to pass.

What that check cannot say is *where*. A row reading "0 marked / 3 marked" names
a page, and a page is twenty-odd lines of Kurrent. This resolves each marker to
the German line it stands over, so the claim can be checked against the
manuscript:

  anchored   the marker carries the German token itself - `[uncertain: Ahten]` -
             and that token is on the page. The line is exact
  landmark   the marker carries the English rendering, but a figure or a name
             that both texts share stands beside it, and that pins the line to
             within a line or two
  estimated  neither - the place is reckoned from how far through the page the
             marker falls. Treat it as a neighbourhood, not a citation

Nothing is applied. The sheet has a `decision` column and
apply_transcription_fixes.py reads the same explicit form, so a ruling here can
be written as `@<line> <token> -> <reading>`.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, difflib, argparse

import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EN_MARK = re.compile(r'\[illegible\]|\[uncertain:\s*([^\]]*)\]|\[text lost\]')
DE_MARK = re.compile(r'\[[^\]]*(?:\?|\.\.\.)[^\]]*\]')
WORD = re.compile(r'[^\W\d_]{3,}', re.UNICODE)


def anchor(payload, lines):
    """The line carrying the German token a marker names, if it is one.

    The translator writes either the German it could not settle or the English
    it settled on. Only the first can be pointed at a line, and it is worth
    telling the two apart rather than guessing at both.
    """
    toks = WORD.findall(payload or '')
    if not toks:
        return 0, ''
    best, best_score = 0, 0.0
    for i, line in enumerate(lines):
        for w in WORD.findall(line):
            for t in toks:
                s = difflib.SequenceMatcher(a=t.lower(), b=w.lower()).ratio()
                if s > best_score:
                    best, best_score = i, s
    return (best, 'exact' if best_score >= 0.99 else 'near') if best_score >= 0.82 \
        else (0, '')


def landmark(en, at, lines):
    """The German line nearest the marker, found by what both texts share.

    Reckoning a marker's place from how far through the page it falls assumes
    the English runs at the German's pace, and it does not: a line of numerals
    translates to four words and a line of chancery formula to twenty. But a
    figure of two digits or more, and a proper noun the translator was told to
    carry across unchanged, appear in both. The nearest one either side of the
    marker puts it within a line or two instead of within a page.
    """
    marks = [(m.start(), m.group(0)) for m in
             re.finditer(r'\d[\d.,/]{1,}|[A-ZÄÖÜ][^\W\d_]{3,}', en)]
    if not marks:
        return 0
    near = min(marks, key=lambda x: abs(x[0] - at))
    if abs(near[0] - at) > 400:
        return 0
    token = re.sub(r'[.,/]', '', near[1])
    for i, line in enumerate(lines):
        for w in WORD.findall(line) + re.findall(r'\d[\d.,/]*', line):
            if re.sub(r'[.,/]', '', w).lower() == token.lower():
                return i + 1        # 1-based, 0 meaning "no landmark"
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds '
                                   'more than one')
    ap.add_argument('--tag', default=None, help='read a second witness instead')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    rev = unitlib.review_dir(slug)
    src = os.path.join(ROOT, 'cache', 'translation-raw' + (f'-{a.tag}' if a.tag else ''))

    recs = unitlib.records_by_pad(ROOT)

    out, pages_seen, n_marked_de = [], 0, 0
    for fn in unitlib.scope_to_unit(sorted(os.listdir(src)), slug):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        got = json.load(io.open(os.path.join(src, fn), encoding='utf-8'))
        rec = recs.get(os.path.splitext(fn)[0])
        if rec is None or not isinstance(got.get('pages'), list):
            continue
        segs = {p.get('page'): p for p in got['pages'] if isinstance(p, dict)}
        for p in rec['pages']:
            seg = segs.get(p['page'])
            if not seg:
                continue
            en = seg.get('en') or ''
            de = p.get('diplomatic') or ''
            marks = list(EN_MARK.finditer(en))
            if not marks:
                continue
            pages_seen += 1
            if DE_MARK.search(de):
                # the transcription already admits doubt here; that is the
                # ordinary case and not what this sheet is for
                n_marked_de += 1
                continue
            lines = de.split('\n')
            for m in marks:
                payload = (m.group(1) or '').strip()
                idx, how = anchor(payload, lines)
                if not how:
                    hit = landmark(en, m.start(), lines)
                    if hit:
                        idx, how = hit - 1, 'landmark'
                    else:
                        # last resort: how far through the page the marker falls
                        idx = min(len(lines) - 1,
                                  int(len(lines) * m.start() / max(1, len(en))))
                ctx = en[max(0, m.start() - 90):m.end() + 90].replace('\n', ' ')
                out.append({
                    'decision': '',
                    'confidence': {'': 'estimated', 'landmark': 'landmark'}
                                  .get(how, 'anchored'),
                    'letter': rec['letter_id'], 'page': p['page'],
                    'page_id': p.get('page_id', ''),
                    'line': p['line_start'] + idx,
                    'marker': m.group(0),
                    'german': lines[idx].strip(),
                    'english': ctx.strip(),
                    'pad': rec['pad'],
                })

    out.sort(key=lambda d: (d['confidence'] != 'anchored',
                            int(d['letter']) if str(d['letter']).isdigit() else 0,
                            d['line']))
    dest = os.path.join(rev, 'unmarked_doubts.csv')
    cols = ['decision', 'confidence', 'letter', 'page', 'page_id', 'line',
            'marker', 'german', 'english', 'pad']
    with io.open(dest, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    kinds = Counter(d['confidence'] for d in out)
    print(f'{pages_seen} page(s) where the English marks doubt')
    print(f'  {n_marked_de} of them the German already marks - not listed')
    print(f'  {len(out)} marker(s) the German does not: '
          + ', '.join(f'{v} {k}' for k, v in kinds.most_common()))
    print(f'\nwrote {dest}')


if __name__ == '__main__':
    main()
