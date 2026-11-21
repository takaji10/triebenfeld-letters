# -*- coding: utf-8 -*-
"""Compare the 2.5x line pass against strip candidate lines for the
fragment-vs-real question."""
import json, os, re, sys, difflib
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())

n = sys.argv[1]
needles = sys.argv[2:]
lp = json.load(open(os.path.join(OCR, 'lines', n + '.json'),
                   encoding='utf-8'))
lps = [(r['top'], r.get('line_pol') or '') for r in lp
       if not r.get('skipped')]
for needle in needles:
    nf = fold(needle)[:24]
    print('=== needle:', needle)
    for top, txt in lps:
        t = fold(txt)[:24]
        if t and difflib.SequenceMatcher(None, t, nf).ratio() >= 0.55:
            print('   %d | %s' % (top, txt[:80]))
