# -*- coding: utf-8 -*-
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(OCR + r'\structure4.json', encoding='utf-8'))

print('== 0113 stored notes ==')
for x in s['0113']['notes']:
    print('--- note %s (top %s):' % (x['num'], x['top']))
    print(x['text'])
print()

print('== anchor structure lines ==')
s2 = json.load(open(OCR + r'\structure2.json', encoding='utf-8'))
WINS = {
    '0058': [(650, 1050), (1900, 2000), (2140, 2180), (2880, 2930),
             (3090, 3140), (3550, 3680)],
    '0083': [(640, 690), (950, 1000), (1620, 1660), (1960, 2010),
             (2150, 2190), (2260, 2300), (2900, 2950), (3220, 3260),
             (3430, 3470), (3840, 3890)],
    '0093': [(640, 700), (980, 1030), (1180, 1230), (1520, 1580),
             (2360, 2400), (2440, 2500), (3420, 3480)],
    '0101': [(760, 900), (1070, 1110), (1490, 1530), (1810, 1850),
             (1920, 1960), (2190, 2230), (2440, 2480), (2860, 2910),
             (3170, 3220)],
    '0113': [(860, 920), (1320, 1370), (1640, 1690), (2080, 2130),
             (2260, 2300), (3060, 3110)],
}
for n, wins in WINS.items():
    print('===', n)
    for a, b in wins:
        for l in s2[n]['lines']:
            if a <= l['top'] < b:
                print('  %5d | %s' % (l['top'], l['text']))
    print()
