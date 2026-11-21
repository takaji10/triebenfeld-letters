# -*- coding: utf-8 -*-
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
D = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
     r'\rusinski1947\literature\rusinski1947')
t = open(os.path.join(D, 'original.md'), encoding='utf-8').read()
ml = json.load(open(os.path.join(OCR, 'marked_lines.json'), encoding='utf-8'))
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))

for n, lo, hi, tag in (('0116', 3950, 4130, 'podwyż tail'),
                       ('0113', 2100, 2260, 'włóki $'),
                       ('0093', 950, 1060, 'litra'),
                       ('0058', 1900, 2010, 'lata/lat')):
    print('===', n, tag)
    for l in ml[n]['lines']:
        if lo <= l['top'] < hi:
            print('  %5d | %s' % (l['top'], l['text'][:110]))
    print('  markers:', [(m['label'], m['top'], m['tok'], m['kind'],
                          m.get('out')) for m in mk[n]
                         if lo - 60 <= m['top'] < hi + 60])
    print()

def seg(lbl):
    i = t.find('[p. %s]' % lbl)
    j = t.find('\n[p. ', i + 1)
    return t[i:j if j > 0 else len(t)]

print('p.101 tail:', seg('101').rstrip()[-140:].replace('\n', ' / '))
print('p.102 head:', seg('102')[:130].replace('\n', ' / '))
print('p.109 tail:', seg('109').rstrip()[-140:].replace('\n', ' / '))
print('p.110 head:', seg('110')[:130].replace('\n', ' / '))
print('p.1 tail:', seg('1').rstrip()[-140:].replace('\n', ' / '))
print('p.2 head:', seg('2')[:130].replace('\n', ' / '))
