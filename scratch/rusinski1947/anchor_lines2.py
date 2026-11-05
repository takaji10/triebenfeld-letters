# -*- coding: utf-8 -*-
import json, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(OCR + r'\structure2.json', encoding='utf-8'))
WINS = {
    '0092': [(3280, 3360)],
    '0093': [(600, 1050), (1150, 1260), (1900, 2000), (2050, 2120),
             (2180, 2260), (2400, 2450), (2700, 2760), (3050, 3120)],
    '0101': [(1830, 1900), (2020, 2080), (2180, 2260), (2400, 2470),
             (2650, 2720)],
    '0058': [(3380, 3480), (3090, 3150)],
    '0113': [(760, 840), (1870, 1920), (2130, 2190), (2250, 2320),
             (3040, 3120)],
}
for n, wins in WINS.items():
    print('===', n)
    for a, b in wins:
        for l in s[n]['lines']:
            if a <= l['top'] < b:
                print('  %5d | %s' % (l['top'], l['text']))
    print()
print('== defs 0058, 0083, 0093, 0101 ==')
s4 = json.load(open(OCR + r'\structure4.json', encoding='utf-8'))
for n in ('0058', '0083', '0093', '0101'):
    print('---', n)
    for x in s4[n]['notes']:
        print('  %s: %s' % (x['num'], re.sub(r'\s+', ' ', x['text'])[:70]))
