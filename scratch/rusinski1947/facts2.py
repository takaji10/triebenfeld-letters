# -*- coding: utf-8 -*-
import json, re, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
D = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
     r'\rusinski1947\literature\rusinski1947')
t = open(os.path.join(D, 'original.md'), encoding='utf-8').read()


def body_seg(label):
    i = t.find('[p. %s]' % label)
    j = t.find('\n[^', i)
    return t[i:j if j > 0 else i + 2500]


print('== body tails/heads ==')
for lbl in (49, 99, 109, 116, 117):
    b = body_seg(str(lbl)).rstrip()
    print('p.%s body tail: ...%s' % (lbl, b[-130:].replace('\n', ' / ')))
print()
print('p.110 body head:', body_seg('110')[:200].replace('\n', ' / '))
print()
print('"również fakt" in p.110?', 'również fakt' in body_seg('110'))
print('"nież fakt" anywhere?', t.count('nież fakt'))
print()
print('== Tabela V row ==')
i = t.find('45,5')
print(t[i - 700:i + 300].replace('\n', ' / ')[:900])
print()
print('== p. 97 German ==')
b97 = body_seg('97')
i = b97.find('Aller')
if i < 0:
    i = b97.find('gna')
print('p.97 body len:', len(b97))
print(b97[:400].replace('\n', ' / '))
print('...')
k = b97.find('Wśród')
print(b97[k:k + 600].replace('\n', ' / ') if k >= 0 else '(no Wśród)')
