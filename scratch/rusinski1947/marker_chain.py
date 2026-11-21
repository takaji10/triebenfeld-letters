# -*- coding: utf-8 -*-
"""The marker chain: an inventory arbiter independent of the foot.

Each printed note has a superscript marker in the body; the print
numbers them 1..k per page. The 2.5x line pass reads the markers as
glued digit tails ('Ujskich1') or standalone digits. Collecting the
candidates in READING ORDER and taking the longest 1,2,3,...k
subsequence yields k - the expected note count - without touching the
foot geometry at all. (A missed marker mid-chain breaks the chain, so
a clean run 1..k is strong evidence; a missed LAST marker can
undercount by one - flagged, not silently resolved.)

Output: marker_chain.json {page: {k, cands, chain_tops}} and a
comparison against structure2 (v4) and structure4 (the verified
inventory).
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TAIL = re.compile(r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)[*?]*\d{1,2}[*?]?'
                  r'[.,;:»”"]?$', re.UNICODE)
DIGIT = re.compile(r'^\d{1,2}[.,]?$')


def candidates(recs, body_top):
    """[(top, order, value, weight)] - marker-number candidates in the
    body region, reading order."""
    out = []
    for r in recs:
        if r.get('skipped'):
            continue
        if body_top and r['top'] >= body_top:
            continue
        for src in ('line_pol', 'line_std'):
            toks = (r.get(src) or '').split()
            for i, w in enumerate(toks):
                prev = toks[i - 1] if i else ''
                nxt = toks[i + 1] if i + 1 < len(toks) else ''
                val = None
                wgt = 0
                m = TAIL.match(w)
                if m and re.search(r'\d$', w) and len(m.group('base')) >= 2 \
                        and not re.fullmatch(r'\d+', w):
                    val = int(re.search(r'(\d+)$', w).group(1))
                    wgt = 2
                elif DIGIT.match(w) and i > 0:
                    prev_ok = re.search(r'[^\W\d_]$', prev, re.UNICODE)
                    nxt_num = re.fullmatch(r'[\d.,%/]+', nxt) if nxt else False
                    prev_num = re.fullmatch(r'[\d.,%/]+', prev) if prev \
                        else False
                    if prev_ok and not nxt_num and not prev_num:
                        val = int(re.sub(r'\D', '', w))
                        wgt = 1
                if val is not None and 1 <= val <= 40:
                    out.append((r['top'], src, val, wgt, w))
    return out


def longest_chain(cands):
    """The longest 1..k subsequence in reading order (first occurrence
    greedy from each start; candidates are few)."""
    best = []
    for start in range(len(cands)):
        if cands[start][2] != 1:
            continue
        chain = [cands[start]]
        want = 2
        for c in cands[start + 1:]:
            if c[2] == want:
                chain.append(c)
                want += 1
        if len(chain) > len(best):
            best = chain
    return best


def main():
    struct4 = json.load(open(os.path.join(OCR, 'structure4.json'),
                             encoding='utf-8'))
    struct2 = json.load(open(os.path.join(OCR, 'structure2.json'),
                             encoding='utf-8'))
    out = {}
    rows = []
    for n in sorted(struct4):
        notes4 = struct4[n]['notes']
        notes2 = struct2[n]['notes']
        if not notes4 and not notes2:
            continue
        lp = os.path.join(OCR, 'lines', n + '.json')
        if not os.path.isfile(lp):
            continue
        recs = json.load(open(lp, encoding='utf-8'))
        # body region: above the FIRST note top of either inventory
        tops = [x['top'] for x in notes4 + notes2 if x.get('top')]
        body_top = min(tops) if tops else None
        cands = candidates(recs, body_top)
        chain = longest_chain(cands)
        k = chain[-1][2] if chain else 0
        out[n] = {'k': k, 'cands': len(cands),
                  'chain_tops': [c[0] for c in chain],
                  'n4': len(notes4), 'n2': len(notes2)}
        if k and (k != len(notes4) or k != len(notes2)):
            rows.append((n, k, len(notes4), len(notes2)))
    with open(os.path.join(OCR, 'marker_chain.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('pages with notes:', len(out))
    print('marker-chain disagrees with an inventory:', len(rows))
    for r in rows:
        print(r)


if __name__ == '__main__':
    main()
