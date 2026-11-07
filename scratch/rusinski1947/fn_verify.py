# -*- coding: utf-8 -*-
"""Verify the footnote-marker audit's wirings + count remnants."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
from collections import Counter
b = Counter(re.findall(r'\[\^(\d+-\d+)\](?!:)', t))
d = Counter(re.findall(r'\[\^(\d+-\d+)\]:', t))
print('refs:', sum(b.values()), 'defs:', sum(d.values()))
print('defs w/o refs:', sorted(set(d) - set(b)))
print('refs w/o defs:', sorted(set(b) - set(d)))
print('count mismatches:',
      {k: (b[k], d[k]) for k in set(b) & set(d) if b[k] != d[k]})
CHECKS = [
    'Baranowskiego[^1-1]', 'Inglota[^1-2]', 'Schmidta[^1-3]',
    'Maasa[^1-4]', 'Schulza[^1-5]', 'Polski[^1-6]',
    'Ujskich[^30-1] i Ol. Nowe Dwory[^30-2]', 'osadników[^30-3]',
    'wieleńskiej[^30-4]', 'Niemcom[^30-5]',
    'polskie[^85-1]', '30-morgowej[^85-2]', '60-morgowej[^85-3]',
    'huby[^85-4],', 'w. XVII[^85-5]', '(r. 1688)[^85-8]',
    'obniżką czynszu[^85-6]', 'talarów[^85-9]—',
    '20 zł z huby 30-morgowej',
    '[^85-4]: Rel. Posn. nr 638, r. 1791, fol. 597.',
    '[^85-9]: AW. Tuchorskie Stare Ol., dep. A. 1 (r. 1703)',
    'targowych[^89-1]', 'aktu[^89-2]', 'gruncie[^89-3]',
    'nieporozumieniu[^89-4]', 'Wartę[^89-5]',
    'olędrzy[^107-1]', 'katolickiego[^107-3]',
    'równocześnie[^107-4]', 'wysokości[^107-5]',
    'gruntów[^70-8]', 'miedze[^70-9]', 'płacono 1 zł[^86-10]',
    'Hładyłowicza[^66-2]', 'gruntów[^66-3]', 'cudzy[^66-4]',
    'Karczmarze[^61-1]', 'Młynarze[^61-2]', 'Hutnictwo[^61-3]',
    'Szkolni[^61-4]', 'chałupnicy[^62-1]', '60[^62-2]', '13[^62-2]',
    '5[^62-3]', 'królewszczyzn pruskich[^64-1]',
]
bad = 0
for pat in CHECKS:
    n = len(re.findall(re.escape(pat), t))
    if n != 1:
        print('CHECK %s -> %d' % (pat, n))
        bad += 1
print('spot-checks: %d/%d ok' % (len(CHECKS) - bad, len(CHECKS)))
