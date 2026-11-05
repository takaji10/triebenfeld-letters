# -*- coding: utf-8 -*-
"""Merge the annex-row witnesses into one reading per row.

Witnesses per annex row (scans 0139-0159):
  - the psm 4 parse (annex_rows.json, from annex_rows.py);
  - the annex_v3 strip reads (annex_strips/<n>.json) - whole rows and
    wrapped lines at 2x, psm 6;
  - the targeted recovery bands (recovery/<n>_<num>.txt) - one row per
    band at 3x, where the psm 4 parse lacks the row.

Merge rules:
  - the recovery band is the witness of record where it exists (the
    band was cut on the row's own anchors, its top/bottom at the
    neighbours' tops): it is the tightest crop;
  - else the strip text whose cells give the row's name-column words;
  - else the psm 4 row.
Every merged row records its witnesses, so the compose step can flag
single-witness rows for the editor's spot sheet.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ANNEX = [f'{i:04d}' for i in range(139, 160)]


def load_json(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def recovery_text(n, num):
    p = os.path.join(OCR, 'recovery', f'{n}_{num}.txt')
    if not os.path.isfile(p):
        return None
    t = open(p, encoding='utf-8').read()
    pol, _, std = t.partition('\n@@@\n')
    return {'pol': pol.strip(), 'std': std.strip()}


def strips(n):
    p = os.path.join(OCR, 'annex_strips', n + '.json')
    if not os.path.isfile(p):
        return []
    return load_json(p)


def strip_rows(n):
    """Rows parsed from the strip texts (leading number = new row)."""
    rows = {}
    cur = None
    for r in strips(n):
        for l in r['pol'].split('\n'):
            l = l.strip().strip('|').strip()
            if not l:
                continue
            m = re.match(r'^\|?\s*(\d{1,3})\s*[\|.,;]?\s*(.*)$', l)
            if m and 1 <= int(m.group(1)) <= 200:
                num = int(m.group(1))
                if cur is not None:
                    rows[cur['num']] = cur
                cur = {'num': num, 'lines': [m.group(2)]}
            elif cur is not None:
                cur['lines'].append(l)
    if cur is not None:
        rows[cur['num']] = cur
    for r in rows.values():
        joined = ' '.join(r['lines'])
        r['cells'] = [c.strip(' |') for c in joined.split('|') if c.strip(' |')]
        del r['lines']
    return rows


def psm4_rows(n):
    d = load_json(os.path.join(OCR, 'annex_rows.json'))
    return {r['num']: r for r in d[n]['rows'] if r['num'] is not None}


def main():
    psm4 = load_json(os.path.join(OCR, 'annex_rows.json'))
    merged = {}
    for n in ANNEX:
        p4 = psm4_rows(n)
        sr = strip_rows(n)
        # the recovery bands' own numbers: from the files on disk
        rec_nums = set()
        recdir = os.path.join(OCR, 'recovery')
        if os.path.isdir(recdir):
            for f in os.listdir(recdir):
                m = re.match(rf'^{n}_(\d+)\.txt$', f)
                if m:
                    rec_nums.add(int(m.group(1)))
        rows = {}
        nums = sorted(set(p4) | set(sr) | rec_nums)
        for num in nums:
            witnesses = {}
            if num in p4:
                witnesses['psm4'] = p4[num]
            if num in sr:
                witnesses['strip'] = sr[num]
            rec = recovery_text(n, num)
            if rec:
                witnesses['recovery'] = rec
            rows[num] = {'witnesses': witnesses}
        merged[n] = {'rows': rows}
        singles = [k for k, v in rows.items() if len(v['witnesses']) == 1]
        print(n, 'rows:', len(rows), 'single-witness:', singles)
    with open(os.path.join(OCR, 'annex_merged.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(merged, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
