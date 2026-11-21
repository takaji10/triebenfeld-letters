# -*- coding: utf-8 -*-
import json, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
D = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
     r'\rusinski1947\literature\rusinski1947')
t = open(os.path.join(D, 'original.md'), encoding='utf-8').read()
ml = json.load(open(os.path.join(OCR, 'marked_lines.json'), encoding='utf-8'))
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))

print('Dzięki cennej in draft:', t.count('Dzięki cennej'))
i = t.find('Dzięki cennej')
if i >= 0:
    print('  ...%s' % t[max(0, i - 120):i + 80].replace('\n', ' / '))
print()
for n, pat in (('0016', 'Dzięki'), ('0017', 'Dzięki'), ('0017', 'interesują'),
               ('0018', 'wdzięcznością'), ('0019', 'wyczerpaniu'),
               ('0019', 'iniciatywy'), ('0019', 'Ferbera'),
               ('0065', 'dzone'), ('0065', 'dzane')):
    hits = [(l['top'], l['text']) for l in ml.get(n, {}).get('lines', [])
            if pat in l['text']]
    print(n, pat, '->', hits[:3])
print()
print('0018 markers:', mk.get('0018'))
print('0019 markers:', mk.get('0019'))
print()
i = t.find('[^4-1]')
print('around [^4-1]:', t[max(0, i - 80):i + 60].replace('\n', ' / '))
i = t.find('[^3-1]')
print('around [^3-1]:', t[max(0, i - 80):i + 60].replace('\n', ' / '))
i = t.find('[^4-3]')
print('around [^4-3]:', t[max(0, i - 80):i + 60].replace('\n', ' / '))
