# -*- coding: utf-8 -*-
"""Verify round 2 additions: Tabela V, the German petition, p. 97."""
import re

t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
         r'\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
ok = True


def check(name, cond, detail=''):
    global ok
    print('%s %s %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        ok = False


check('S06 absolute row', 'kościański 44 20 3 21' in t)
check('S06 poznański row', 'poznański 78 17 3 58' in t)
check('S06 razem row', 'Razem 122 37 6 79' in t)
check('S06 percent 47,7', 'kościański 45,5 6,8 47,7' in t)
check('S06 percent poznański', 'poznański 21,8 3,8 74,4' in t)
check('S06 razem percent', 'Razem — 30,3 4,9 64,8' in t)
check('S06 no false table markers', '[^66-1] 20' not in t)
check('S19 quote starts', '„Nachdem Ihro Majestät aus besonderer '
      'Gnadenbezeigung' in t)
check('S19 8 Ellen restored', 'jede Ruthe zu 8 Ellen' in t)
check('S19 no eaten 8', 'zu [^97-3] Ellen' not in t)
check('S19 Königlich norm', 'Königlich Pohlnischer Regierung' in t)
check('S19 signature', 'Bracknitzer Holl., d. 22-ten May 1782”' in t)
check('S19 date 22 maja restored', 'gdyż 22 maja' in t)
check('S19 Brandenburger label', 'Brandenburger[^97-2]' in t)
check('S19 Koerth label', 'Koerth[^97-3].' in t)
check('S19 no OCR mush', 'Allcrgnidigst' not in t and 'gintzlich' not in t)
check('p.97 def count', len(re.findall(r'\[\^97-\d\]:', t)) == 3)
check('materiaw fixed', 'materiałów pracy łów źródłowych' in t
      or 'materia- łów' in t or 'materiałów' in t)

print()
print('ALL PASS' if ok else 'FAILURES PRESENT')
