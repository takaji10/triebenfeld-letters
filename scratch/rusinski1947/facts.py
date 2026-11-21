# -*- coding: utf-8 -*-
"""Facts needed for the editor-answer fixes:
1. the draft's page-tail/page-head states for the joins (S23)
2. note 14-1's current extent (S02)
3. where the fix-target tokens live (lines + page/scan + top)
4. the Tabela V kościanski row context (S06)
"""
import json, re, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
D = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
     r'\rusinski1947\literature\rusinski1947')
t = open(os.path.join(D, 'original.md'), encoding='utf-8').read()


def page_seg(label):
    i = t.find('[p. %s]' % label)
    j = t.find('\n[p. ', i + 1)
    return t[i:j if j > 0 else len(t)]


print('== 1. join states ==')
for a, b in ((49, 50), (99, 100), (101, 102), (108, 109), (109, 110),
             (116, 117), (117, 118), (2, 3)):
    ta = page_seg(str(a)).rstrip()
    tb = page_seg(str(b))
    print('p.%s tail: ...%s' % (a, ta[-90:].replace('\n', ' / ')))
    print('p.%s head: %s...' % (b, tb[:110].replace('\n', ' / ')))
    print()

print('== 2. note 14-1 ==')
m = re.search(r'\[\^14-1\]: (.*?)(?=\n\[\^|\n\n\[p\. |\Z)', t, re.S)
d = m.group(1)
print('len:', len(d))
print('tail: ...%s' % d[-260:].replace('\n', ' / '))
print()

print('== 3. fix-target lines (marked_lines) ==')
ml = json.load(open(os.path.join(OCR, 'marked_lines.json'),
                    encoding='utf-8'))
targets = {
    '0039': ['13.915'],
    '0083': ['608'],
    '0092': ['12121'],
    '0093': ['4:58'],
    '0101': ['301'],
    '0062': ['59/'],
    '0115': ['109'],
    '0113': ['52/5', '8814', '21 razy', 'razy'],
    '0058': ['lata'],
}
for n, pats in sorted(targets.items()):
    for l in ml.get(n, {}).get('lines', []):
        for p in pats:
            if p in l['text']:
                print('%s top=%5d | %s' % (n, l['top'], l['text'][:95]))
                break
print()

print('== 4. Tabela V row in draft ==')
i = t.find('kościański')
print(t[i - 500:i + 200].replace('\n', ' / '))
