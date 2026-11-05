# -*- coding: utf-8 -*-
"""Marker reconstruction for tom5, v2: positions from the TSV tails,
counts cross-checked against the line passes, numbers assigned in order.

Per page with notes (structure.json):
  1. candidates: every body token matching the tail shapes, in reading
     order, tiered - 'strong' (artifact tail *? / low confidence),
     'plain' (glued digit at high confidence; years and figures also
     match, so plain is weak evidence);
  2. the page must carry exactly len(notes) markers;
  3. assignment: strong candidates first in order, plain filling the
     gaps; if candidates exceed the notes, the excess plain ones drop
     (the last ones win when the counts force a choice: the print's
     markers cluster where the line pass saw them);
  4. shortfall: the lines where the line pass (full_lines.py) saw more
     tail tokens than the TSV did supply extra positions (the line pass
     proved it recovers markers the page pass loses); what is still
     short goes to the spot sheet with the line's crop.

Output: markers.json: per page, per marker {label, line_top, token_idx,
after (the word it rides), tier}; and shortfall report.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TAIL = re.compile(
    r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)(?P<tail>[*?]+\d{1,2}[*?]?'
    r'|\d{1,2}[*?]?)[.,;:»”"]?$', re.UNICODE)


def page_tokens(d, note_top):
    """Body tokens in reading order: [(top, idx_in_line, tok, conf)]."""
    ws = [x for x in d['words'] if x[5].strip() and x[1] < note_top - 20]
    ws.sort(key=lambda x: (x[1], x[0]))
    out = []
    line_seen = {}
    for x in ws:
        top = x[1]
        key = None
        for k in line_seen:
            if abs(k - top) < 30:
                key = k
                break
        if key is None:
            key = top
            line_seen[key] = 0
        idx = line_seen[key]
        line_seen[key] += 1
        out.append((key, idx, x[5].strip(), x[4]))
    return out


def main():
    struct = json.load(open(os.path.join(OCR, 'structure.json'),
                            encoding='utf-8'))
    markers = {}
    short_report = []
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            continue
        want = len(notes)
        d = json.load(open(os.path.join(OCR, n + '.json'),
                           encoding='utf-8'))
        note_top = min(x['top'] for x in notes)
        toks = page_tokens(d, note_top)
        cands = []
        for pos, (top, idx, tok, conf) in enumerate(toks):
            m = TAIL.match(tok)
            if not m:
                continue
            base, tail = m.group('base'), m.group('tail')
            if len(base) < 2:
                continue
            digits = re.sub(r'\D', '', tail)
            if not digits or len(digits) > 2:
                continue
            tier = 'plain'
            if '*' in tok or '?' in tok:
                tier = 'strong'
            elif conf and 0 < conf < 80:
                tier = 'strong'
            cands.append({'pos': pos, 'top': top, 'idx': idx, 'tok': tok,
                          'tier': tier})
        # cross-check against the line pass: per line, tail-token counts
        lp_path = os.path.join(OCR, 'lines', n + '.json')
        lp_counts = {}
        if os.path.isfile(lp_path):
            for r in json.load(open(lp_path, encoding='utf-8')):
                if r.get('skipped'):
                    continue
                c = 0
                for w in (r.get('line_pol') or '').split():
                    m = TAIL.match(w)
                    if m and len(m.group('base')) >= 2 \
                            and len(re.sub(r'\D', '', m.group('tail'))) <= 2:
                        c += 1
                if c:
                    lp_counts[r['top']] = max(lp_counts.get(r['top'], 0), c)
        # per-line counts from the TSV candidates
        tsv_counts = {}
        for c in cands:
            tsv_counts[c['top']] = tsv_counts.get(c['top'], 0) + 1
        # lines where the line pass saw more: candidate boosters
        boost = []
        for top, c in sorted(lp_counts.items()):
            extra = c - tsv_counts.get(top, 0)
            if extra > 0:
                boost.append((top, extra))
        strong = [c for c in cands if c['tier'] == 'strong']
        plain = [c for c in cands if c['tier'] == 'plain']
        chosen = []
        if len(cands) >= want:
            # take all strong, fill with plain from the end
            chosen = list(strong)
            for c in reversed(plain):
                if len(chosen) >= want:
                    break
                if c not in chosen:
                    chosen.append(c)
            chosen = sorted(chosen, key=lambda c: c['pos'])[:want]
        else:
            chosen = list(cands)
        chosen.sort(key=lambda c: c['pos'])
        out = []
        for i, c in enumerate(chosen):
            lab = f"{int(n) - 15}-{i + 1}"
            out.append({'label': lab, 'top': c['top'], 'idx': c['idx'],
                        'after': c['tok'], 'tier': c['tier']})
        markers[n] = out
        if len(out) < want:
            short_report.append((n, want, len(out), boost[:4]))
            print(n, f'SHORT {len(out)}/{want}', 'boost lines:', boost[:4])
    with open(os.path.join(OCR, 'markers.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(markers, fh, ensure_ascii=False)
    print('pages with notes:', len(markers),
          'complete:', len(markers) - len(short_report),
          'short:', len(short_report))


if __name__ == '__main__':
    main()
