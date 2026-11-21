# -*- coding: utf-8 -*-
"""Body-swallow audit: the body's last line before the note block must
end a sentence; otherwise the boundary may have eaten body text."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))
sus = []
for n in sorted(s):
    notes = s[n]['notes']
    if not notes:
        continue
    first_top = min(x['top'] for x in notes)
    body = [l for l in s[n]['lines'] if l['top'] < first_top]
    if body:
        last = body[-1]['text'].strip()
        if last and not re.search(r'[.!?»:;]”?\s*$', last) \
                and len(last.split()) > 3:
            sus.append((n, last[-70:]))
print('body-swallow suspects:', len(sus))
for x in sus:
    print(x)
