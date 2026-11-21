# -*- coding: utf-8 -*-
"""Wave-2 audit sheet: per short page, the candidate markers the v4
detector already finds (with per-candidate semantic check against the
def list) - the working list for MANUAL entry authoring."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure4.json'),
                   encoding='utf-8'))
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))

for n in sorted(s):
    notes = s[n]['notes']
    if not notes or len(mk.get(n, [])) >= len(notes):
        continue
    ft = min(x['top'] for x in notes)
    print('=== %s  %d/%d' % (n, len(mk.get(n, [])), len(notes)))
    print('  DEFS:', ' | '.join('%d:%s' % (x['num'],
          re.sub(r'\s+', ' ', x['text'])[:38]) for x in notes))
    for m in mk.get(n, []):
        print('   got %-5s top=%5d tok=%-12r %s' %
              (m['label'], m['top'], m['tok'], m['kind']))
    print()
