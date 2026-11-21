# -*- coding: utf-8 -*-
"""Second adjudication round: p.58, p.88 target, p.145 1781, p.148/152/154,
and the garbled sigla pages (43, 45, 69, 72) + p.61 Tol./Tod. mapping."""
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


def ctx(txt, pat, tag, width=70):
    for m in re.finditer(pat, txt):
        a = max(0, m.start() - width)
        print('   %s: %s' % (tag, txt[a:m.end() + width].replace('\n', ' | ')))


print('=== p.58 digits 15 vs 5,7')
ctx(sb['58'], r'\b5\b|57|15|5 OO', 'S')
print('--- T:')
ctx(tb['58'], r'\b15\b|5 OO', 'T')

print()
print('=== p.88 target around 1800/1500')
ctx(tb['88'], r'1,800|1,500', 'T')

print()
print('=== p.145 1781 both texts')
ctx(sb['145'], r'178\d|Aprilis|kwietnia|lutego', 'S')
print('--- T:')
ctx(tb['145'], r'178\d|April', 'T')

print()
print('=== p.148 missing 20')
ctx(sb['148'], r'\b20\b', 'S')
print('--- T:')
ctx(tb['148'], r'\b20\b', 'T')

print()
print('=== garbled sigla source contexts')
for lab, pat in (('43', r'Rel\.? ?Posn'), ('45', r'Kl\.? ?M'),
                 ('69', r'AM\.|\.M |M\. Sier'), ('72', r'Kl\.? ?XII')):
    print('--- p.%s S:' % lab)
    ctx(sb[lab], pat, 'S', 50)
    print('    T:')
    ctx(tb[lab], pat, 'T', 50)

print()
print('=== p.61 Tol. (S) vs Tol./Tod. (T)')
ctx(sb['61'], r'Tol\.', 'S', 55)
print('--- T Tol.:')
ctx(tb['61'], r'Tol\.', 'T', 55)
print('--- T Tod. 89:')
ctx(tb['61'], r'Tod\. 89', 'T', 55)
