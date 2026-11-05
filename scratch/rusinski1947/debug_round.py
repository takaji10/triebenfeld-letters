# -*- coding: utf-8 -*-
import json, re, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
D = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
     r'\rusinski1947\literature\rusinski1947')
t = open(os.path.join(D, 'original.md'), encoding='utf-8').read()
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))


def seg(lbl):
    i = t.find('[p. %s]' % lbl)
    j = t.find('\n[p. ', i + 1)
    return t[i:j if j > 0 else len(t)]


print('== p. 49 tail / p. 50 head ==')
s49 = seg('49').rstrip()
print('49 tail: ...%s' % s49[-160:].replace('\n', ' / '))
print('50 head: %s' % seg('50')[:160].replace('\n', ' / '))
print()
print('== p. 1 tail / p. 2 head ==')
s1 = seg('1').rstrip()
print('1 tail: ...%s' % s1[-160:].replace('\n', ' / '))
print('2 head: %s' % seg('2')[:160].replace('\n', ' / '))
print()
print('== p. 109 tail / p. 110 head ==')
s109 = seg('109').rstrip()
k = s109.rfind('Potwierdza')
print('109 around Potwierdza: %s' % s109[max(0, k - 100):k + 60]
      .replace('\n', ' / '))
print('110 head: %s' % seg('110')[:160].replace('\n', ' / '))
print()
print('== eaten words ==')
for pat in ('inicjatywy', 'wdzięcznością', 'wyczerpaniu'):
    i = t.find(pat)
    print('%s: ...%s' % (pat, t[max(0, i - 60):i + 30].replace('\n', ' / ')
                         if i >= 0 else 'NOT FOUND'))
print()
print('== markers on the five pages ==')
for n in ('0016', '0019', '0047', '0058', '0083', '0093', '0101', '0113',
          '0064'):
    print(n, [(m['label'], m['top'], m['tok'], m['kind'],
               m.get('out', '')[:22]) for m in mk.get(n, [])])
print()
print('== label context checks ==')
for pat in ('60[^68-', '30[^86-', '70[^86-', 'litra[^78-', 'włóki[^98-',
            '5% sumy', 'lata[^43-', 'lat[^43-'):
    i = t.find(pat)
    print('%-14s: %s' % (pat, '...' + t[max(0, i - 60):i + 40]
                         .replace('\n', ' / ') if i >= 0 else 'NOT FOUND'))
