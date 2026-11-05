# -*- coding: utf-8 -*-
"""Verify the editor-answer round: joins, marker placements, fixes."""
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


# --- joins (no duplication, sentences continuous) ---
check('sporządzane joined', 'sporządzane w określonej formie' in t)
check('no sporząz', 'sporząz' not in t)
check('do 200 talarów', 'do 200 talarów w r. 1773' in t)
check('podwyższył joined', bool(re.search(r'podwyższył\[\^101-7\] w r\. 1793', t))
      or bool(re.search(r'podwyższył \[\^101-7\] w r\. 1793', t))
      or 'podwyższył w r. 1793' in t)
check('przywileje wystawione', 'przywileje wystawione po tychże latach'
      in t)
check('również fakt (page-break split)',
      'Potwierdza to' in t and 'również fakt, że osady wcześniej' in t)
check('rzeczy przyczynił', 'stanu rzeczy przyczynił się' in t)
check('względnie lektora', 'nauczyciela względnie lektora' in t)
check('materiał do projektowanej',
      'uzyskać materiał do projektowanej mapy' in t)
check('badanie z | interesującego (page-break split)',
      bool(re.search(r'badanie z\n', t))
      and bool(re.search(r'\ninteresującego nas tutaj', t)))
check('bądź nad brzegami', 'bądź nad brzegami wód' in t)
check('no dup: o zadawalające', t.count('o zadawalające') == 1)
check('no dup: Jak się rzecz', t.count('Jak się rzecz') == 1)
# 'Potwierdza to' legitimately appears more than once in the book
check('no dup: Potwierdza to', t.count('Potwierdza to') <= 2)
check('no dup: Początki kolonizacji', t.count('Początki kolonizacji') == 1)

# --- the editor's number rulings ---
check('S03 13.915 [sic]', '13.915 [sic]' in t)
check('S05 60[^68-6] morgów', bool(re.search(r'60\[\^68-6\]\s*\n?\s*morgów', t))
      or '60[^68-6]' in t)
check('S08 r. 1653', 'Inwentarz z r. 1653' in t)
check('S10a 2½ razy', '2½ razy większa' in t)
check('S10b 88½ zł', '88½ zł' in t)
check('S11 od 30[^86-1] do 70[^86-2]',
      'od 30[^86-1] do 70[^86-2]' in t)
check('S12 121½ garnca', '121½ garnca wódki' in t)
check('S13 4,58 litra[^78-2]', '4,58 litra[^78-2]' in t)
check('S15 5 2/5', '5 2/5' in t and '4 3/5' in t)
check('S15 włóki[^98-4]', 'włóki[^98-4]' in t)
check('S16 5% sumy', '5% sumy' in t)
check('S17 10% kwoty', '10% kwoty' in t)
check('S18 44 lata[^43-3]', '44 lata[^43-3]' in t)
check('S18 60 lat[^43-4]', '60 lat[^43-4]' in t)
check('S14 table rebuilt', '7½-łokciowym wyniesie 16,80 ha' in t)
check('S07 r. 1643 (applied)', 'W r. 1643 olędrom Marianowa' in t)
check('0058 60 lat note', 'na 60 lat' in t)
check('0113 six defs', len(re.findall(r'\[\^98-\d\]:', t)) == 6)
check('0113 note 6 Gumowski', bool(re.search(r'\[\^98-6\]: Gumowski', t)))

# --- the five marker pages: no stacked duplicate labels ---
for lbl in ('43', '68', '78', '86', '98'):
    stacked = re.findall(r'\[\^%s-\d+\] \[\^%s-\d+\]' % (lbl, lbl), t)
    check('p. %s no stacked labels' % lbl, not stacked, str(stacked[:2]))

# --- no eaten words ---
check('iniciatywy intact', 'z inicjatywy burmistrza' in t)
check('Stwierdzam intact', 'Stwierdzam z wdzięcznością' in t)
check('Po wyczerpaniu intact', 'Po wyczerpaniu się pierwszej fali' in t)

print()
print('ALL PASS' if ok else 'FAILURES PRESENT')
