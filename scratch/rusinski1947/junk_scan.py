# -*- coding: utf-8 -*-
"""Enumerate junk numeric cells (dymy/obl/ludn) with strip raws."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
at = json.load(open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
                    r'\tom5_ocr\annex_table.json', encoding='utf-8'))
out = []
cur = None
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur:
        c = [x.strip() for x in ln.split('|')][1:-1]
        if len(c) < 11:
            continue
        for ci, tag in ((8, 'dymy'), (9, 'obl'), (10, 'ludn')):
            v = c[ci]
            if v in ('—', '') or re.fullmatch(r'\d+(?: \*)?', v):
                continue
            if re.fullmatch(r'\d+ \d', v):      # raised small mark (SPOT)
                continue
            if re.fullmatch(r'\d+\[\^\d+-\d+\]', v):   # footnote ref (ruled)
                continue
            raw = (at.get(cur, {}).get('rows', {})
                   .get(m.group(1), {}) or {}).get('raw') or ''
            out.append('%s r%s c%d %s=%r RAW %s'
                       % (cur, m.group(1), ci, tag, v, raw[:110]))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\junklist.txt',
     'w', encoding='utf-8').write('\n'.join(out))
print(len(out), 'junk cells')
from collections import Counter
print(Counter(l[:4] for l in out))
