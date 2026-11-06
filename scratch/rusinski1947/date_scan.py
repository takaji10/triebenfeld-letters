# -*- coding: utf-8 -*-
"""List annex data-cell (col 8, 0-based 7) values that are not clean
dates, with the strip raw for decoding."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
at = json.load(open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
                    r'\tom5_ocr\annex_table.json', encoding='utf-8'))
cur = None
bad = []
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur:
        cells = [c.strip(' |') for c in ln.split(' | ')]
        v = cells[7] if len(cells) > 7 else ''
        ED = r'(?:\d{1,2} )?[IVX]{1,4} \d{4}'   # day-optional month+year
        D2 = r'\d{1,2} [IVX]{1,4}'              # day+month, no year
        D4 = r'\d{4}'                           # bare year (print repeats it)
        D5 = r'\d{1,2} \d{1,2} \d{4}'           # numeric month style (r76)
        pat = ('^(' + ED + '(?:(?:; ?| i | )' + ED + ')*(?: i ' + D4 + ')?'
               '|' + D2 + '(?: i ' + D4 + ')?'
               '|' + D4 + '|' + D5 + ')$')
        ok = (v == '—' or re.fullmatch(pat, v.strip()) or v == '')
        if not ok:
            raw = (at.get(cur, {}).get('rows', {}).get(m.group(1), {})
                   .get('raw') or '')
            bad.append('%s r%d | %r | RAW %r' % (cur, int(m.group(1)),
                                                 v[:40], raw[:170]))
print(len(bad), 'bad data cells')
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\datebad.txt',
     'w', encoding='utf-8').write('\n'.join(bad))
