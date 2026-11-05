# -*- coding: utf-8 -*-
import json, re, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
D = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
     r'\rusinski1947\literature\rusinski1947')
t = open(os.path.join(D, 'original.md'), encoding='utf-8').read()

print('== line-pass records for the manual-mark anchors ==')
for n, pat in (('0083', '608'), ('0101', '301'), ('0101', '70'),
               ('0093', '4:58'), ('0058', 'lata'), ('0113', '52/5'),
               ('0113', 'włóki'), ('0064', 'sporzą'), ('0114', '200'),
               ('0116', 'podwyż'), ('0124', 'rów'), ('0131', 'rzeczy')):
    lp = os.path.join(OCR, 'lines', n + '.json')
    recs = json.load(open(lp, encoding='utf-8'))
    for r in recs:
        txt = (r.get('line_pol') or '') + ' | ' + (r.get('line_std') or '')
        if pat in txt:
            print('%s top=%5d sk=%s | %s' % (n, r['top'], r.get('skipped'),
                                             (r.get('line_pol') or '')[:90]))
print()

print('== p. 110 around "również fakt" ==')
i = t.find('[p. 110]')
j = t.find('\n[p. ', i + 1)
seg = t[i:j]
k = seg.find('również fakt')
print(seg[max(0, k - 260):k + 160].replace('\n', ' / '))
print()

print('== tabela search "41,7" ==')
for m in re.finditer(r'.{140}41,7.{60}', t):
    print(m.group(0).replace('\n', ' / '))
    print('---')
print()

print('== draft p. 86 (0101) and p. 78 (0093) states ==')
for lbl in (86, 78, 43, 98):
    i = t.find('[p. %s]' % lbl)
    j = t.find('\n[^', i)
    seg = t[i:j]
    for pat in ('301', '70', '4:58', '4,58', 'lata 3', '52/5', '8814',
                '21 razy', '608'):
        k = seg.find(pat)
        if k >= 0:
            print('p.%s %s: ...%s...' % (lbl, pat,
                                         seg[max(0, k - 70):k + 70]
                                         .replace('\n', ' / ')))
print()

print('== p. 97 German block (full body) ==')
i = t.find('[p. 97]')
j = t.find('\n[^', i)
print(t[i:j].replace('\n', ' / '))
