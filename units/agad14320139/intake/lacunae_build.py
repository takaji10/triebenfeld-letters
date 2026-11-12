# -*- coding: utf-8 -*-
"""Mechanical columns of the lacuna register (docs/CONSISTORY_1882_PLAN.md, section 5).

For every "[...]" in the transcriptions: page, line, edge (left / right / mid /
whole), the line's text, and the best twin line in the other report (difflib on
the line without its marks). No proposed supply and no grade here: those are
judgements, made by reading the images (intake/lacunae.csv, columns filled by
hand). Run from the repository root:  python units/agad14320139/intake/lacunae_build.py
"""
import csv, difflib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
TR = os.path.join(os.path.dirname(HERE), 'transcriptions')
PAGES = {'0318_a': 1, '0322_a': 1, '0322_b': 2, '0345_a': 2}
MARK = re.compile(r'\[\.\.\.\]')

lines = {}
for pid in PAGES:
    with open(os.path.join(TR, pid + '.txt'), encoding='utf-8') as f:
        lines[pid] = f.read().split('\n')
    if lines[pid] and lines[pid][-1] == '':
        lines[pid].pop()

def clean(s):
    return re.sub(r'\s+', ' ', MARK.sub(' ', re.sub(r'\[\??[^\]]*\??\]|\[\?\]', ' ', s))).strip()

rows = []
n = 0
for pid, doc in PAGES.items():
    other = [p for p, d in PAGES.items() if d != doc]
    for k, text in enumerate(lines[pid], 1):
        ms = list(MARK.finditer(text))
        for j, m in enumerate(ms, 1):
            n += 1
            if text.strip() == '[...]':
                edge = 'whole'
            elif m.start() == 0:
                edge = 'left'
            elif m.end() == len(text):
                edge = 'right'
            else:
                edge = 'mid'
            best, bp = 0.0, ''
            for op in other:
                for ok, ot in enumerate(lines[op], 1):
                    r = difflib.SequenceMatcher(None, clean(text), clean(ot)).ratio()
                    if r > best:
                        best, bp = r, f'{op}:{ok}'
            rows.append({'id': f'L{n:02d}', 'doc': doc, 'page': pid, 'line': k, 'nth': j,
                         'edge': edge, 'text': text,
                         'twin': bp if best >= 0.45 else '',
                         'twin_ratio': f'{best:.2f}' if best >= 0.45 else '',
                         'twin_text': (lines[bp.split(':')[0]][int(bp.split(':')[1]) - 1]
                                       if best >= 0.45 else '')})
out = os.path.join(HERE, 'lacunae.csv')
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]) + ['supply', 'grade', 'witness', 'note'],
                       lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(len(rows), 'lacuna marks written to', out)
