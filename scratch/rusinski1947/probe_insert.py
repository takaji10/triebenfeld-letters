# -*- coding: utf-8 -*-
import json, os, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
from marked_lines import insert_marks

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ml = json.load(open(os.path.join(OCR, 'marked_lines.json'), encoding='utf-8'))
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))

n = '0058'
tops = [l['top'] for l in ml[n]['lines']]
print('0058 marked tops 1900-2000:', [t for t in tops if 1900 <= t < 2000])
line = [l for l in ml[n]['lines'] if l['top'] == 1959]
print('line 1959:', line)
marks = [m for m in mk[n] if abs(m['top'] - 1959) <= 60]
print('marks near 1959:', marks)
if line:
    print('OUT:', insert_marks(line[0]['text'], marks))
print()
# where did the fixes go? check the marked_lines text now
for l in ml[n]['lines']:
    if 1900 <= l['top'] < 2000:
        print('ML %5d | %s' % (l['top'], l['text'][:100]))
