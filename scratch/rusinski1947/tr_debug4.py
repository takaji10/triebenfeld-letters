# -*- coding: utf-8 -*-
"""Context dump for the ANEKS-pages digit drops (146-156)."""
import re

BASE = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
        r'\rusinski1947\literature\rusinski1947')
S = open(BASE + r'\original.md', encoding='utf-8').read()
T = open(BASE + r'\english.md', encoding='utf-8').read()


def blocks(txt):
    out, cur = {}, None
    for ln in txt.splitlines():
        m = re.match(r'^\[p\. (\w+)\]$', ln.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur is not None:
            out[cur].append(ln)
    return {k: '\n'.join(v) for k, v in out.items()}


sb, tb = blocks(S), blocks(T)

for lab in ('146', '147', '148', '149', '153', '155', '156'):
    print('=' * 20, 'p.', lab)
    # source numeric tokens with context
    seen = []
    for m in re.finditer(r'\d+', sb[lab]):
        a = max(0, m.start() - 40)
        seen.append(sb[lab][a:m.end() + 30].replace('\n', ' | '))
    tgt = []
    for m in re.finditer(r'\d+', tb[lab]):
        a = max(0, m.start() - 40)
        tgt.append(tb[lab][a:m.end() + 30].replace('\n', ' | '))
    print('SOURCE %d tokens:' % len(seen))
    for x in seen:
        print('  S:', x)
    print('TARGET %d tokens:' % len(tgt))
    for x in tgt:
        print('  T:', x)
