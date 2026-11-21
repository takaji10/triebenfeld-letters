# -*- coding: utf-8 -*-
"""Enumerate suspect text cells (ci 4 rok, 5 char, 6 zrodlo) in the
b/c-series annex tables. GOOD = regex vocab + print-verified phrase set."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
BC = ('0147', '0148', '0149', '0150', '0151', '0152', '0153', '0154',
      '0155', '0156', '0157', '0158', '0159')
GOOD = re.compile(
    r'^(—||)$'
    r'|^[\dIVX()/ .?]+$'                      # rok: year-like
    r'|^ok\. \d+$|^przed r\. \d+$|^między r\. \d+ a \d+$'
    r'|^(wieś|las|folwark|owczarnia|obora|zarośla|nieużytki'
    r'|mokradła \(\?\)|zarośla, łąki|zarośla, mokradła|zarośla, las'
    r'|folw\. częścią zarosły|rola częścią zarosła'
    r'|ta sama wieś i mieszkańcy|wieś z budynkami|gotowa rola'
    r'|grunty opustoszałe|grunty zarosłe|wieś, częśc\.|wieś 1 folw\.'
    r'|„grunt zarosłami zarosły”|wieś z bud)[^|]*$'
    r'|^(Rel\. Posn\.|Rel\. Cost\.|AW\.|AGH\.|AG\.|KI\. XII|Kl\. XII'
    r'|AM\.|Landr\.|Dom\.P\.|Dom\. P\.|AW\. dep\.|Arch\. P\.|Repertorium'
    r'|DWZP\.|GC\.|Kl\. M\.|Kal\.|Kat\.|Schulz W\.|Werner, Steffani'
    r'|Bór\.|dto|AW\. Chodzież)[^|]*$')
rows = []
cur = None
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur in BC:
        c = [x.strip() for x in ln.split('|')][1:-1]
        if len(c) >= 11:
            rows.append((cur, c[0], c[4], c[5], c[6]))
bad = []
for sh, num, rok, char, zr in rows:
    for ci, v, tag in ((4, rok, 'rok'), (5, char, 'char'), (6, zr, 'zr')):
        if GOOD.match(v):
            continue
        bad.append('%s r%s c%d %s=%r' % (sh, num, ci, tag, v))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\textbad.txt',
     'w', encoding='utf-8').write('\n'.join(bad))
print(len(bad), 'suspect text cells')
for b in bad:
    print(' ', b)
