# -*- coding: utf-8 -*-
"""Count standalone candidates rejected by the superscript check,
sample the rejects."""
import json, os, re, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import markers3 as M

OCR = M.OCR
struct = json.load(open(os.path.join(OCR, 'structure4.json'),
                        encoding='utf-8'))
n = sys.argv[1] if len(sys.argv) > 1 else '0027'
notes = struct[n]['notes']
want = len(notes)
recs = json.load(open(os.path.join(OCR, 'lines', n + '.json'),
                      encoding='utf-8'))
pw = json.load(open(os.path.join(OCR, n + '.json'),
                    encoding='utf-8'))['words']
line_h = {}
for x in pw:
    if x[5].strip():
        line_h.setdefault(round(x[1] / 45), []).append(x[3])
line_h = {k: sorted(v)[len(v) // 2] for k, v in line_h.items()}

kept = rejected = 0
for r in recs:
    if r.get('skipped'):
        continue
    for src in ('line_pol', 'line_std'):
        for kind, i, w, weight in M.line_candidates(r.get(src) or ''):
            if kind != 'standalone':
                kept += 1
                continue
            core = re.sub(r'[.,;:]', '', w)
            hit = None
            for x in pw:
                if x[5].strip() and abs(x[1] - r['top']) <= 40 \
                        and x[5].strip().rstrip('.,;:') == core:
                    hit = x
                    break
            if hit is None:
                kept += 1
                continue
            lh = line_h.get(round(hit[1] / 45), 60)
            if hit[3] <= 0.62 * lh:
                kept += 1
                print('KEEP  top=%d tok=%r h=%d lh=%d' % (
                    r['top'], w, hit[3], lh))
            else:
                rejected += 1
                print('REJ   top=%d tok=%r h=%d lh=%d | %s' % (
                    r['top'], w, hit[3], lh,
                    r.get('line_pol', '')[:60]))
print('want notes:', want, '| kept:', kept, 'rejected:', rejected)
