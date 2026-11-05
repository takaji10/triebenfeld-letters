# -*- coding: utf-8 -*-
"""The word settlement, v2: real position-level alignment.

For each candidate word (doubtful.csv, body pages):
  1. its line in the page pass is found by the box's top;
  2. the page-std pass, the 2.5x line passes (both models) and the 2x
     band passes are ALIGNED against the page-pol line with difflib
     (token level, autojunk off); the witness's reading at the
     candidate's token position is read out of the alignment's opcodes
     (equal -> agrees; replace/substitute -> the aligned token(s));
  3. each distinct reading is scored: witness weights (page pol is the
     reference, not scored), page_std 2, line_pol 3, line_std 2,
     band_pol 2, band_std 2; lexicon membership adds min(3, 1+log10
     count) - the empirical dictionary of words both page passes emit
     somewhere in the book;
  4. the highest score wins; ties and readings outside the lexicon go
     to the spot list with the crop box.

Evidence rule (from the sampled disagreements: a band can be wrong where
the page pass and lexicon agree - 'malący' vs 'mający'): no witness is
sovereign; the lexicon is the sense check.
"""
import sys, os, json, csv, re, math, difflib
from collections import defaultdict

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
BODY = {f'{i:04d}' for i in range(16, 138)} | \
       {f'{i:04d}' for i in range(160, 172)}


def fold(w):
    return re.sub(r'^\W+|\W+$', '', w).lower()


def page_lines(n, src):
    """[(top, [tokens])] of one page pass, from the TSV boxes."""
    d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
    ws = [(x[1], x[0], x[5].strip()) for x in d['words'] if x[5].strip()]
    ws.sort()
    lines = []
    for top, left, word in ws:
        if lines and abs(lines[-1][0] - top) < 30:
            lines[-1][2].append((left, word))
        else:
            lines.append([top, left, [(left, word)]])
    out = []
    for top, left, parts in lines:
        parts.sort()
        out.append((top, [w for _, w in parts]))
    return out


def aligned_reading(ref_toks, wit_toks, idx, window=8):
    """The witness's reading at ref_toks[idx], difflib-aligned over a
    LOCAL window (whole-line alignment drifts on OCR-noisy lines and
    maps the reading to a wrong token). Returns None (agree), a string,
    or '' (the witness lacks the token)."""
    lo = max(0, idx - window)
    hi = min(len(ref_toks), idx + window)
    ref_w = ref_toks[lo:hi]
    rel = idx - lo
    # the witness window: align to the same slice by proportion is
    # unreliable; instead align the full strings but only trust the
    # opcode that covers rel, and only when the opcode's span is small
    # (a local edit), which the window makes likely
    sm = difflib.SequenceMatcher(None, ref_w, wit_toks, autojunk=False)
    for tag, a1, a2, b1, b2 in sm.get_opcodes():
        if a1 <= rel < a2:
            if tag == 'equal':
                return None
            if tag == 'replace':
                wits = wit_toks[b1:b2]
                r = rel - a1
                if r < len(wits):
                    return wits[r]
                return wits[-1] if wits else ''
            if tag == 'delete':
                return ''
            return None
    return None


def sim(a, b):
    """difflib ratio on the raw tokens (case-sensitive; OCR errors are
    character-level)."""
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def main():
    lex = json.load(open(os.path.join(OCR, 'lexicon.json'),
                         encoding='utf-8'))['words']
    cands = [r for r in csv.DictReader(
        open(os.path.join(OCR, 'doubtful.csv'), encoding='utf-8'))
        if r['scan'] in BODY]
    by_scan = defaultdict(list)
    for r in cands:
        by_scan[r['scan']].append(r)
    spot = []
    out = {}
    resolved = 0
    for n in sorted(by_scan):
        pol_lines = dict()
        for top, toks in page_lines(n, 'pol'):
            pol_lines[top] = toks
        std_lines = dict()
        for top, toks in page_lines(n, 'std'):
            std_lines[top] = toks
        lines_pass = []
        lp = os.path.join(OCR, 'lines', n + '.json')
        if os.path.isfile(lp):
            for r in json.load(open(lp, encoding='utf-8')):
                if not r.get('skipped'):
                    lines_pass.append((r['top'],
                                       (r.get('line_pol') or '').split(),
                                       (r.get('line_std') or '').split()))
        band_pass = []
        bp = os.path.join(OCR, 'bands.csv')
        if os.path.isfile(bp):
            for r in csv.DictReader(open(bp, encoding='utf-8')):
                if r['scan'] == n:
                    band_pass.append((int(r['top']),
                                      r['band_pol'].split(),
                                      r['band_std'].split()))
        for r in by_scan[n]:
            top = int(r['top'])
            word = r['word']
            wf = fold(word)
            if not wf:
                continue
            # the candidate's own line: the page-pass line with the
            # closest top that contains a fold-match
            best_line = None
            best_dist = 10 ** 9
            for lt, toks in pol_lines.items():
                if any(fold(t) == wf for t in toks):
                    d = abs(lt - top)
                    if d < best_dist:
                        best_dist = d
                        best_line = (lt, toks)
            if best_line is None or best_dist > 60:
                continue
            lt, ptoks = best_line
            idx = next(i for i, t in enumerate(ptoks) if fold(t) == wf)
            scores = defaultdict(float)
            readings = {wf}
            # page std, aligned at the same line top
            if lt in std_lines:
                wit = aligned_reading(ptoks, std_lines[lt], idx)
                if wit is not None:
                    for w in ([wit] if isinstance(wit, str) else wit):
                        f = fold(w)
                        if f:
                            scores[f] += 2
                            readings.add(f)
            # the 2.5x line passes: align the page line against each
            for (ltop, lp1, lp2) in lines_pass:
                if abs(ltop - lt) > 90:
                    continue
                for src, wtoks, weight in (('line_pol', lp1, 3),
                                           ('line_std', lp2, 2)):
                    if not wtoks:
                        continue
                    wit = aligned_reading(ptoks, wtoks, idx)
                    if wit is not None:
                        for w in ([wit] if isinstance(wit, str) else wit):
                            f = fold(w)
                            if f:
                                scores[f] += weight
                                readings.add(f)
            # the 2x band passes
            for (btop, bp1, bp2) in band_pass:
                if abs(btop - lt) > 110:
                    continue
                for src, wtoks, weight in (('band_pol', bp1, 2),
                                           ('band_std', bp2, 2)):
                    if not wtoks:
                        continue
                    wit = aligned_reading(ptoks, wtoks, idx)
                    if wit is not None:
                        for w in ([wit] if isinstance(wit, str) else wit):
                            f = fold(w)
                            if f:
                                scores[f] += weight
                                readings.add(f)
            # the lexicon
            for f in list(readings):
                c = lex.get(f, 0)
                if c:
                    scores[f] += min(3.0, 1.0 + math.log10(c))
            if not scores:
                continue
            best = max(scores.items(), key=lambda z: (z[1], z[0] == wf))
            # 'best' prefers wf on exact ties
            if best[0] == wf:
                resolved += 1
                choice = word
            else:
                # THE GUARD: a replacement must be a near-spelling of the
                # original (OCR errors are character-level). A far
                # reading means the alignment drifted onto another word,
                # not that the print says something else: keep the
                # original, and let the spot sheet carry the case if the
                # scores favour the far reading strongly.
                ordered = sorted(scores.items(), key=lambda z: -z[1])
                margin = ordered[0][1] - (ordered[1][1] if len(ordered) > 1
                                          else 0.0)
                if sim(word.rstrip('.,;:!?»”" '), best[0]) < 0.62:
                    if margin >= 2.0:
                        spot.append([n, r['left'], r['top'], r['width'],
                                     r['height'], word, best[0]])
                    resolved += 1
                    choice = word
                elif margin < 0.5:
                    choice = None
                    spot.append([n, r['left'], r['top'], r['width'],
                                 r['height'], word, best[0]])
                else:
                    resolved += 1
                    choice = best[0]
            out[f'{n}_{r["left"]}_{r["top"]}'] = {
                'word': word, 'top_line': lt, 'idx': idx,
                'choice': choice, 'scores': dict(scores)}
    with open(os.path.join(OCR, 'settle.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    with open(os.path.join(OCR, 'spot_words.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        w = csv.writer(fh)
        w.writerow(['scan', 'left', 'top', 'width', 'height', 'word',
                    'alt'])
        w.writerows(spot)
    print('candidates settled:', len(out), 'resolved:', resolved,
          'spot:', len(spot))


if __name__ == '__main__':
    main()
