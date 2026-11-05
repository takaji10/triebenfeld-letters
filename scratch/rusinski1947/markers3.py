# -*- coding: utf-8 -*-
"""Markers v3: the line pass as the primary source.

The page-pass TSV yields only ~14% of the markers; the line pass (2.5x)
yields ~105% of them as (a) glued digit tails and (b) standalone 1-2
digit tokens after a word. v3 collects the line-pass candidates in
reading order, drops the number-context false positives (a digit whose
neighbour tokens are numeric; a 3+ digit token; a digit inside a date
span), then assigns 1..n in order against the page's note count. Where
the candidates exceed the notes, the excess (weakest-context) drop;
where they fall short, the page is flagged for the spot sheet with the
line crops.

Output: markers.json v3 + shortfall report. The label: <page>-<n>.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TAIL = re.compile(r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)[*?]*\d{1,2}[*?]?'
                  r'[.,;:»”"]?$', re.UNICODE)
DIGIT = re.compile(r'^\d{1,2}[.,]?$')


def line_candidates(text):
    """Candidates in one line's tokens: [(kind, tok_index, tok, weight)]."""
    toks = text.split()
    out = []
    for i, w in enumerate(toks):
        prev = toks[i - 1] if i else ''
        nxt = toks[i + 1] if i + 1 < len(toks) else ''
        m = TAIL.match(w)
        if m and '*' in w or (m and '?' in w):
            out.append(('glued-artifact', i, w, 3))
            continue
        if m and re.search(r'\d$', w) and len(m.group('base')) >= 2 \
                and not re.fullmatch(r'\d+', w):
            out.append(('glued', i, w, 2))
            continue
        if DIGIT.match(w) and i > 0:
            prev_ok = re.search(r'[^\W\d_]$', prev, re.UNICODE)
            nxt_num = re.fullmatch(r'[\d.,%/]+', nxt) if nxt else False
            prev_num = re.fullmatch(r'[\d.,%/]+', prev) if prev else False
            if prev_ok and not nxt_num and not prev_num:
                out.append(('standalone', i, w, 1))
    return out


def main():
    spath = os.path.join(OCR, 'structure4.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure2.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure.json')
    struct = json.load(open(spath, encoding='utf-8'))
    markers = {}
    shorts = []
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            continue
        want = len(notes)
        lp_path = os.path.join(OCR, 'lines', n + '.json')
        if not os.path.isfile(lp_path):
            shorts.append((n, want, 0, 'no line pass'))
            continue
        recs = json.load(open(lp_path, encoding='utf-8'))
        cands = []
        for r in recs:
            if r.get('skipped'):
                # skipped lines were high-confidence and tail-free; but a
                # marker may still ride them (the skip rule's residual
                # risk): the page pass's own tails are the fallback
                for w in r['page'].split():
                    m = TAIL.match(w)
                    if m and re.search(r'\d$', w) \
                            and len(m.group('base')) >= 2:
                        cands.append(('skipped-glued', r['top'], w, 1))
                continue
            for src in ('line_pol', 'line_std'):
                for kind, i, w, weight in line_candidates(r.get(src) or ''):
                    cands.append((kind, r['top'], w, weight))
        # order by line, then position
        cands.sort(key=lambda c: (c[1], c[0] != 'glued-artifact'))
        if len(cands) > want:
            # drop the weakest until the count fits
            cands = sorted(cands, key=lambda c: -c[3])[:want]
            cands = sorted(cands, key=lambda c: (c[1], c[3]))
        out = []
        for i, (kind, top, w, weight) in enumerate(cands):
            out.append({'label': f'{int(n) - 15}-{i + 1}', 'top': top,
                        'tok': w, 'kind': kind, 'weight': weight})
        markers[n] = out
        if len(out) < want:
            shorts.append((n, want, len(out), ''))
            print(n, f'SHORT {len(out)}/{want}')
    with open(os.path.join(OCR, 'markers.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(markers, fh, ensure_ascii=False)
    print('pages:', len(markers), 'short:', len(shorts))


if __name__ == '__main__':
    main()
