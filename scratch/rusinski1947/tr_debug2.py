# -*- coding: utf-8 -*-
"""Per-page context dumps for the tr_full diffs needing adjudication:
sigla-count drifts, the zł/gr diffs, and specific digit diffs."""
import re
from collections import Counter

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

print('=== sigla per-page diffs')
for sg in ('AW.', 'AM.', 'Rel. Posn.', 'Kl. XII', 'Kl. M.', 'Tod. 89'):
    diffs = []
    for lab in sorted(sb, key=lambda x: int(x) if x.isdigit() else 999):
        if not lab.isdigit() or not (1 <= int(lab) <= 122
                                     or 145 <= int(lab) <= 157):
            continue
        ns = len(re.findall(r'(?<![A-Za-z])' + re.escape(sg), sb[lab]))
        nt = len(re.findall(r'(?<![A-Za-z])' + re.escape(sg), tb.get(lab, '')))
        if ns != nt:
            diffs.append((lab, ns, nt))
    print(sg, diffs)

print()
print('=== Tod. 89 / Tol. occurrences in SOURCE (per page)')
for lab in sorted(sb, key=lambda x: int(x) if x.isdigit() else 999):
    if not lab.isdigit() or not (1 <= int(lab) <= 122):
        continue
    ns = len(re.findall(r'(?<![A-Za-z])Tod\. 89', sb[lab]))
    nt = len(re.findall(r'(?<![A-Za-z])Tol\.', sb[lab]))
    if ns or nt:
        print('p.%s Tod.89=%d Tol.=%d' % (lab, ns, nt))

print()
print('=== target AW. contexts beyond the source count (sample pages)')
for lab in sorted(tb, key=lambda x: int(x) if x.isdigit() else 999):
    if not lab.isdigit() or not (1 <= int(lab) <= 122):
        continue
    ns = len(re.findall(r'(?<![A-Za-z])AW\.', sb[lab]))
    nt = len(re.findall(r'(?<![A-Za-z])AW\.', tb.get(lab, '')))
    if nt > ns:
        print('--- p.%s src %d tgt %d' % (lab, ns, nt))
        for m in re.finditer(r'(?<![A-Za-z])AW\.', tb[lab]):
            a = max(0, m.start() - 70)
            print('   T:', tb[lab][a:m.end() + 50].replace('\n', ' | '))
        for m in list(re.finditer(r'(?<![A-Za-z])AW\.', sb[lab]))[:ns]:
            a = max(0, m.start() - 70)
            print('   S:', sb[lab][a:m.end() + 50].replace('\n', ' | '))

print()
print('=== zł/gr diffs context')
for lab, sg in (('79', 'zł'), ('86', 'gr'), ('88', 'zł')):
    print('--- p.%s %s' % (lab, sg))
    for tag, bl in (('S', sb[lab]), ('T', tb[lab])):
        for m in re.finditer(r'(?<![A-Za-z])' + re.escape(sg) +
                             r'(?![A-Za-z])', bl):
            a = max(0, m.start() - 60)
            print('   %s: %s' % (tag, bl[a:m.end() + 40].replace('\n', ' | ')))

print()
print('=== p.145 1781, p.152 clause digits context')
for lab, pat in (('145', r'1781'), ('152', r'\b[2-9]\.')):
    print('--- p.%s /%s/' % (lab, pat))
    for tag, bl in (('S', sb[lab]), ('T', tb[lab])):
        for m in re.finditer(pat, bl):
            a = max(0, m.start() - 60)
            print('   %s: %s' % (tag, bl[a:m.end() + 40].replace('\n', ' | ')))
