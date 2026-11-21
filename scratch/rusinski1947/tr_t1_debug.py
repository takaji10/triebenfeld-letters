# -*- coding: utf-8 -*-
"""Detail the T1 check failures: digit diffs per block + missing sigla."""
import re
from collections import Counter

SRC = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\original.md')
TGT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\english.md')

s = open(SRC, encoding='utf-8').read()
t = open(TGT, encoding='utf-8').read()
si, ti = s.find('[p. 1]'), t.find('[p. 1]')


def blocks(txt, upto):
    out, cur = {}, None
    for ln in txt[:upto].splitlines():
        m = re.match(r'^\[p\. (\w+)\]$', ln.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur:
            out[cur].append(ln)
    return {k: '\n'.join(v) for k, v in out.items()}


sb, tb = blocks(s, si), blocks(t, ti)


def digits(txt):
    txt = txt.replace('.', '').replace(',', '').replace('—', '-')
    return Counter(re.findall(r'\d+', txt))


for lab in ('V', 'VI', 'VII'):
    ds, dt = digits(sb[lab]), digits(tb[lab])
    print('=== block', lab)
    print('  source-only:', dict(ds - dt))
    print('  target-only:', dict(dt - ds))

for sg in ('Rel. Posn.', 'Tp. 89', 'TW', 'Generalia A. VII. 12'):
    print('===', sg)
    for name, txt, upto in (('SRC', s, si), ('TGT', t, ti)):
        for m in re.finditer(re.escape(sg), txt[:upto]):
            a = max(0, m.start() - 60)
            print('  %s: ...%s...' % (name,
                                      txt[a:m.end() + 40].replace('\n', ' | ')))
