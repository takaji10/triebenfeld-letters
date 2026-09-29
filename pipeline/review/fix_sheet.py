# -*- coding: utf-8 -*-
"""Turn hand rulings into the sheet apply_transcription_fixes.py reads.

    python pipeline/review/fix_sheet.py --unit oe1bu9454 rulings.tsv
    python pipeline/review/apply_transcription_fixes.py --unit oe1bu9454 --apply

rulings.tsv has one ruling per line, tab-separated:

    <corpus line>  <old token>  <new token>  <reason>

(# starts a comment.) Every row becomes an explicit @line ruling, so a fix
changes exactly the token named on exactly the line named. The corpus line is
the line number in units/<slug>/corpus.txt, as show_letter.py prints it in its
first column, not the letter line the site shows.

A row is flagged when `old` does not occur exactly once on its line (the apply
step would refuse it) or when old and new are far apart (similarity < 0.6).
That second flag is a prompt to re-read the row, not a refusal: Erer -> Ewr and
um -> und are right and still dissimilar.

Writes review/<slug>/transcription_fixes.csv, replacing what was there.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, csv, hashlib, difflib, argparse
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', required=True)
    ap.add_argument('rulings')
    a = ap.parse_args()
    u = unitlib.one_unit(a.unit)
    L = open(os.path.join(u.dir, 'corpus.txt'), encoding='utf-8').read().split('\n')
    doc = [None] * (len(L) + 1); pid = [None] * (len(L) + 1); pno = [0] * (len(L) + 1)
    cur = p = None; n = 0
    for i, l in enumerate(L, 1):
        m = re.match(r'\[DOC (\S+)\]', l)
        if m:
            cur = m.group(1); n = 0
        m = re.match(r'\[PAGE (\S+)\]', l)
        if m:
            p = m.group(1); n += 1
        doc[i], pid[i], pno[i] = cur, p, n
    rows, bad = [], 0
    for raw in open(a.rulings, encoding='utf-8'):
        if not raw.strip() or raw.startswith('#'):
            continue
        ln, old, new, why = raw.rstrip('\n').split('\t')
        ln = int(ln); line = L[ln - 1]
        c = len(re.findall(r'(?<![^\W\d_])' + re.escape(old) + r'(?![^\W\d_])', line))
        sim = difflib.SequenceMatcher(None, old.lower(), new.lower()).ratio()
        flag = '' if c == 1 and sim >= 0.6 else f'  <-- count={c} sim={sim:.2f}'
        bad += bool(flag)
        print(f'{ln} [{doc[ln]}] {old} -> {new}{flag}')
        lid = doc[ln]
        rows.append(dict(key=hashlib.md5(f'{lid}|{ln}|{old}|{new}'.encode()).hexdigest()[:8],
                         pad=u.pad(lid), letter=lid, page=pno[ln], page_id=pid[ln], line=ln,
                         confidence='line', needs='', transcribed=old, proposed=new,
                         decision=f'@{ln} {old} -> {new}', why=why))
    if not rows:
        sys.exit('no rulings')
    out = os.path.join(unitlib.review_dir(u.slug), 'transcription_fixes.csv')
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), 'rows,', bad, 'flagged ->', out)


if __name__ == '__main__':
    main()
