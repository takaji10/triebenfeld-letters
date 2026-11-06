# -*- coding: utf-8 -*-
"""Dump strip raws for all text-suspect rows (text_scan output)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
at = json.load(open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
                    r'\tom5_ocr\annex_table.json', encoding='utf-8'))
BAD = open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\textbad.txt',
           encoding='utf-8').read()
rows = set()
for ln in BAD.splitlines():
    m = re.match(r'\s+(015\d) r(\d+) c\d', ln)
    if m:
        rows.add((m.group(1), m.group(2)))
out = []
for sh, num in sorted(rows):
    raw = at.get(sh, {}).get('rows', {}).get(num, {}).get('raw') or ''
    out.append('%s r%s: %s' % (sh, num, repr(raw)[:200]))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\traws.txt',
     'w', encoding='utf-8').write('\n'.join(out))
print(len(out), 'rows dumped')
