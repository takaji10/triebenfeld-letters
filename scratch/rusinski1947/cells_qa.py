# -*- coding: utf-8 -*-
"""Cell-QA: flag suspicious cell contents across annex_cells.json."""
import json, re

ac = json.load(open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
                    r'\tom5_ocr\annex_cells.json', encoding='utf-8'))
COLS = ['Lp', 'Nazwa', 'Parafia', 'Dzisiejsza', 'Rok', 'Charakter',
        'Zrodlo', 'Data', 'DymyTp', 'DymyObl', 'Ludn']

stats = {'total': 0, 'empty': 0, 'nonword': 0, 'digit_in_name': 0}
ex = {'nonword': [], 'digit_in_name': [], 'empty_name': []}
for n in sorted(ac):
    for k, r in ac[n].items():
        cells = r['cells']
        stats['total'] += 1
        name = cells[1]
        if not name:
            stats['empty'] += 1
            ex['empty_name'].append((n, k))
            continue
        if re.search(r'[^A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9\s.,;:()\-—„”»«%*/\''
                     r'"?!*+]', name):
            stats['nonword'] += 1
            ex['nonword'].append((n, k, name[:60]))
        if re.search(r'\d', name):
            stats['digit_in_name'] += 1
            ex['digit_in_name'].append((n, k, name[:50]))
print(stats)
for key in ex:
    print('--', key)
    for e in ex[key][:15]:
        print('   ', e)
