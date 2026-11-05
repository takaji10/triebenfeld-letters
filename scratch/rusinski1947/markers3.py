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

# markers recovered against the print (the per-page audit): scan ->
# [(line_top, tok, kind, out)] where 'out' is an explicit replacement
# for the token ('{label}' placeholder) when the fused token must be
# split ('608' -> '60' + marker 6); tok matches the STRUCTURE-line
# token (substring match). Every entry below was verified against the
# print (3x band reads) and the def's content.
MANUAL_ADD = {
    # p. 43: 1 ciała¹, 2 gminnego², 3 lata³, 4 lat⁴, 5 Marianowo⁵,
    # 6 rozbiorów⁶ (auto '8,' keeps), 7 Gebhardta⁷, 8 Schulza⁸, 9 1613⁹
    '0058': [
        (778, '1),', 'manual', '[^{label}]),'),
        (996, 'gminnego.', 'glued', None),
        (1959, '3,', 'manual', '[^{label}],'),
        (1959, '£.', 'manual', '[^{label}].'),
        (2176, '5.', 'manual', None),
        (3132, '7?', 'manual', '[^{label}]'),
        (3132, '8,', 'manual', '[^{label}],'),
        (3428, '1613', 'manual', '1613[^{label}],'),
    ],
    # p. 68: 1 cale¹, 2 57,6 cm², 3 ślady³ (auto), 4 hubą⁴ (auto *.),
    # 5 morgom⁵, 6 60⁶, 7 włóki⁷, 8 powienien⁸, 9 śladu⁹, 10 gospodarzy¹⁰
    '0083': [
        (682, 'cale', 'glued', None),
        (999, '?.', 'manual', 'cm[^{label}].'),
        (2174, '8.', 'manual', '[^{label}].'),
        (2278, '608', 'manual', '60[^{label}]'),
        (2919, '”.', 'manual', '[^{label}].'),
        (3239, '8,', 'manual', '[^{label}],'),
        (3454, '?.', 'manual', '[^{label}].'),
        (3865, "'0)", 'manual', '[^{label}]).'),
    ],
    # p. 78: 1 garncy¹, 2 litra², 3 sąsiednich³, 4 1773⁴ (auto £.),
    # 5 pańskiego⁵ (auto), 6 pieniężny⁶ (auto 6), 7 poczciwi⁷ (auto ?),
    # 8 domowej⁸, 9 sztrafą⁹
    '0093': [
        (702, '1.', 'manual', '[^{label}].'),
        (1004, '*.', 'manual', '[^{label}].'),
        (1329, '3,', 'manual', '[^{label}],'),
        (3473, 'poczciwi”', 'manual', '„poczciwi”[^{label}]'),
        (3685, 'domowej', 'glued', None),
        (3685, 'sztrafą', 'manual', 'sztrafą”[^{label}].'),
    ],
    # p. 86: 1 30¹, 2 70², 3 zł³, 4 XVIII⁴, 5 czasowo⁵, 6 równocześnie⁶,
    # 7 tynfa⁷, 8 ogólnego⁸, 9 leśne⁹ (auto ?.), 10 zł¹⁰ (auto zł10)
    '0101': [
        (783, '301', 'manual', '30[^{label}]'),
        (889, '70?', 'manual', '70[^{label}]'),
        (1100, '8,', 'manual', '[^{label}],'),
        (1515, '£.', 'manual', '[^{label}].'),
        (2149, '5.', 'manual', None),
        (2254, 'równocześnie$.', 'manual', 'równocześnie[^{label}],'),
        (2566, '%.', 'manual', '[^{label}].'),
        (2785, '8.', 'manual', '[^{label}].'),
    ],
    # p. 98: 1 Schmidt¹, 2 1773², 3 podatkowych³, 4 włóki⁴, 5 morgów⁵,
    # 6 g⁶
    '0113': [
        (1010, '1.', 'manual', '[^{label}].'),
        (1323, '1773', 'manual', '1773[^{label}],'),
        (1773, '%.', 'manual', '[^{label}].'),
        (2182, '$,', 'manual', '[^{label}],'),
        (2317, '5,', 'manual', '[^{label}],'),
        (3373, 'g%.', 'manual', 'g[^{label}].'),
    ],
    # p. 97: 1 ujskiego¹ (auto), 2 Brandenburger², 3 Koerth³
    '0112': [
        (1175, 'Brandenburger?', 'manual', 'Brandenburger[^{label}]'),
        (1175, '3.', 'manual', '[^{label}].'),
    ],
}
# false auto candidates to remove: scan -> [(top, tok)]
MANUAL_DROP = {    '0058': [(984, '2.'), (1947, '44'), (1947, '3.'), (1947, '60'),
             (1978, '44'), (1978, '00'), (1978, '*.'), (2163, '5,'),
             (3117, '7'), (3117, '8,')],
    '0083': [(661, '24'), (976, 'com2'), (976, 'cm2'), (976, '6'),
             (1440, '??'), (2171, '2'), (2171, '60'), (2927, '*.')],
    '0093': [(666, '8'), (1205, '1'), (2474, 'C7yNns7'), (3451, '?')],
    '0101': [(777, '50'), (879, '|'), (1093, '38'), (1511, '|'),
             (1830, '2'), (1937, '10'), (1937, '6'), (3196, '|')],
    '0113': [(1345, 'Jl57'), (2281, 'morgów*9'), (991, '1.')],
    # p. 97: '22' was the DATE ('22 maja 1782'), not a marker; the
    # '8' in the quote was the 8 of '8 Ellen'
    '0112': [(1830, '22'), (2626, '8')],
}
# whole regions where every digit is table data, not a marker:
# scan -> [(lo, hi)]
MANUAL_DROP_RANGES = {
    '0081': [(1900, 2900)],
}


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
        if re.fullmatch(r'[*?$§£?]+[.,;:»”"]?', w):
            # an isolated artifact glyph: the print's inline marker as
            # the models read it ('*', '$', '?.') - almost always the
            # marker, never prose. '|' excluded (line-art, not markers)
            out.append(('artifact', i, w, 2))
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
        # the TSV word boxes for the GEOMETRIC check: a superscript
        # marker digit is ~half the line's type height; a TEXT number
        # ('co 4 tygodnie') is full height. Without this check real
        # numbers were consumed as markers and their digits LOST from
        # the text (the readers' 'numbers dropped behind labels'
        # class), shifting every later label on the page.
        pw = json.load(open(os.path.join(OCR, n + '.json'),
                            encoding='utf-8'))['words']
        line_h = {}
        for x in pw:
            if x[5].strip():
                line_h.setdefault(round(x[1] / 45), []).append(x[3])
        line_h = {k: sorted(v)[len(v) // 2] for k, v in line_h.items()}

        def is_superscript(top, tok):
            # The print sets its footnote markers as INLINE FULL-SIZE
            # digits (measured: 'Bemberga 1.' h=57 vs line 64; the old
            # 0.62-height test killed real markers). No geometric
            # separation exists - every candidate is kept; the
            # number-context flag below marks the ambiguous placements
            # for the spot sheet instead.
            return True, 0, 0
        cands = []
        for r in recs:
            if r.get('skipped'):
                # skipped lines were high-confidence and tail-free; but
                # a marker may still ride them: BOTH the glued tails
                # and the standalone/artifact candidates of the page
                # pass's own read are the fallback
                for kind, i, w, weight in line_candidates(r['page']):
                    cands.append((kind, r['top'], w, 1, False))
                for w in r['page'].split():
                    m = TAIL.match(w)
                    if m and re.search(r'\d$', w) \
                            and len(m.group('base')) >= 2:
                        cands.append(('skipped-glued', r['top'], w, 1,
                                      False))
                continue
            for src in ('line_pol', 'line_std'):
                toks = (r.get(src) or '').split()
                for kind, i, w, weight in line_candidates(r.get(src) or ''):
                    if kind == 'standalone':
                        ok, h, lh = is_superscript(r['top'], w)
                        if not ok:
                            continue
                        # number-context flag: a standalone digit whose
                        # next token is a lowercase word is ambiguous
                        # (marker 'Hollander 2' vs number 'co 4
                        # tygodnie') - the placement keeps the digit
                        # and the spot sheet lists the case
                        nxt = toks[i + 1] if i + 1 < len(toks) else ''
                        num_ctx = bool(nxt) and nxt[:1].islower()
                    else:
                        num_ctx = False
                    cands.append((kind, r['top'], w, weight, num_ctx))
        # order by line, then position
        cands.sort(key=lambda c: (c[1], c[0] != 'glued-artifact'))
        # dedup: both OCR models produce the same candidate on a line
        # (same top, same token) - the pairs displaced REAL markers via
        # the count-trim and stacked double labels in the body
        norm = lambda tk: re.sub(r'[^\w]', '', tk, re.UNICODE).lower()
        best = {}
        for c in cands:
            k = (c[1], norm(c[2]))
            if k not in best or c[3] > best[k][3]:
                best[k] = c
        cands = sorted(best.values(),
                       key=lambda c: (c[1], c[0] != 'glued-artifact'))
        # manual audit marks: markers recovered against the print that
        # the models missed (fused digits '608' = '60' + marker 6), and
        # false auto candidates to drop ('44' read as a marker). A
        # manual add carries an 'out' replacement for the text token.
        cands = [c for c in cands
                 if not any(abs(c[1] - dt) <= 80 and norm(c[2]) == norm(dtk)
                            for (dt, dtk) in MANUAL_DROP.get(n, []))
                 and not any(lo <= c[1] < hi
                             for (lo, hi) in MANUAL_DROP_RANGES.get(n, []))]
        prot = []
        rest = []
        for c in cands:
            covered = norm(c[2]) and any(
                abs(c[1] - mtop) <= 80 and norm(c[2]) == norm(mtok)
                for (mtop, mtok, mk_, mo) in MANUAL_ADD.get(n, []))
            (prot if c[3] >= 4 or covered else rest).append(c)
        for (mtop, mtok, mkind, mout) in MANUAL_ADD.get(n, []):
            prot.append((mkind, mtop, mtok, 4, False, mout))
        # the trim only drops UNPROTECTED candidates: the audit-verified
        # markers must survive it
        room = max(0, want - len(prot))
        if len(rest) > room:
            rest = sorted(rest, key=lambda c: -c[3])[:room]
        cands = prot + rest
        cands = [(c + (None,))[:6] if len(c) == 5 else c for c in cands]
        cands.sort(key=lambda c: (c[1], c[0] != 'glued-artifact'))
        out = []
        for i, (kind, top, w, weight, num_ctx, extra) in enumerate(cands):
            e = {'label': f'{int(n) - 15}-{i + 1}', 'top': top,
                 'tok': w, 'kind': kind, 'weight': weight,
                 'num_ctx': num_ctx}
            if extra:
                e['out'] = extra
            out.append(e)
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
