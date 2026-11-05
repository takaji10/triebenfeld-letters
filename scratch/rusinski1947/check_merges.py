# -*- coding: utf-8 -*-
import re
"""Check the readers' specific merge examples against the current draft."""
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
cases = [
    ('p8',  'Por. daty przypisu'),
    ('p14', 'Podaną cyfrę trudno skontrolować'),
    ('p18', 'Źródła: MP — Holendry Nadziejewskie'),
    ('p28', 'Przywilej lokacyjny dla Ostrówka'),
    ('p32', 'Niemcy katolicy mieszkali we wsiach duchownych'),
    ('p39', 'Wenn man im 16 und 17'),
    ('p50', 'iako do macierzystey substancyi'),
    ('p76', 'KI. XII 6 I, fol. 62'),
    ('p108', 'Metryki 441 C'),
    ('p110', 'Skorzystali z nieji'),
]
for tag, needle in cases:
    i = t.find(needle)
    if i < 0:
        print(tag, needle[:38], '-> NOT FOUND (gone/never)')
        continue
    # is it inside a definition? definitions may wrap; look back for
    # the '[^p-k]:' marker within 400 chars with no [p. N] between
    back = t[max(0, i - 400):i]
    is_def = re.search(r'\[\^[\w.-]+\]:[^[]*$', back) is not None
    print(tag, needle[:38], '-> DEF-OK' if is_def else 'IN-BODY!',
          repr(t[max(0, i - 60):i + 50].replace('\n', ' / ')))
