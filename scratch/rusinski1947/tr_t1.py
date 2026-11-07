# -*- coding: utf-8 -*-
"""T1 builder: append the bibliography (B. Literatura) verbatim from
original.md to english.md (citations keep their original languages),
and check the T1 result."""
import re

SRC = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\original.md')
TGT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
       r'\rusinski1947\literature\rusinski1947\english.md')

s = open(SRC, encoding='utf-8').read()
t = open(TGT, encoding='utf-8').read()

i = s.find('B. Literatura')
j = s.find('[p. 1]')
bib = s[i:j].replace('B. Literatura\n\n', '').rstrip()
# drop the translated heading already in the target; append entries
t = t.rstrip() + '\n\n' + bib + '\n'
open(TGT, 'w', encoding='utf-8', newline='\n').write(t)
print('bibliography appended: %d chars' % len(bib))

# ---------------- the T1 check -------------------------------------------
def blocks(txt, upto):
    """page-label -> block text, up to the '[p. 1]' boundary."""
    out = {}
    cur = None
    for ln in txt[:upto].splitlines():
        m = re.match(r'^\[p\. (\w+)\]$', ln.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur:
            out[cur].append(ln)
    return {k: '\n'.join(v) for k, v in out.items()}

si = s.find('[p. 1]')
ti = t.find('[p. 1]')
sb = blocks(s, si)
tb = blocks(t, ti)

ok = True
def check(name, cond):
    global ok
    print('%s %s' % ('PASS' if cond else 'FAIL', name))
    if not cond:
        ok = False

check('label sequence', list(sb) == list(tb))
print('  source:', list(sb))
print('  target:', list(tb))

def digits(txt):
    """digit-sequence multiset after separator stripping."""
    txt = txt.replace('.', '').replace(',', '').replace('—', '-')
    return sorted(re.findall(r'\d+', txt))

for lab in sb:
    check('digits %s' % lab, digits(sb[lab]) == digits(tb.get(lab, '')))

# sigla inventory: every occurrence in source must occur in target
# (word-boundary matching; counted from [p. I] onward so the
# translator's note's example sigla do not pollute the counts)
START = t.find('[p. I]')
SIGLA = ['AC.', 'AGH', 'AM', 'AW', 'Dom.', 'Decr. Posn.', 'Inser. Valc.',
         'Kat.', 'Kl. M.', 'Kośc.', 'Landr.', 'Lustr. pruska', 'MG', 'MGd',
         'MP', 'M. Schr.', 'M 1821', 'O 83', 'OWK', 'Rel. Cost.',
         'Rel. Posn.', 'Rel. Valc.', 'Rel. Vsch.', 'St. T.', 'Szk.',
         'T 1769', 'Tb.', 'TKS.', 'Tod.', 'Tołł.', 'Tp. 75', 'Tp. 89',
         'TW', 'Verz/1800', 'Verz/1845', 'Wol. Leg.', 'VO 78']


def n_hits(sg, txt):
    return len(re.findall(r'(?<![A-Za-z])' + re.escape(sg) +
                          r'(?![A-Za-z])', txt))


for sg in SIGLA:
    n_s = n_hits(sg, s[:si][s[:si].find('[p. I]'):])
    n_t = n_hits(sg, t[:ti][START:])
    check('siglum %-14s (%d)' % (sg, n_s), n_s == n_t)

# call marks: their digit-bearing identifiers must survive
# (whitespace-tolerant: a wrap between words is legitimate)
for cm in ['XII. A. 1', 'XII. 6 I–V', 'XII. 7', 'XII. 13', 'SPZ. C. I. 14',
           'II. B.', 'III. B.', 'Ms. C. 17', 'M.S. C. 10', 'Mscr. G. 23',
           'Generalia A. VII. 12', 'Manuscr. II. 494', 'LI. 508, 113',
           'LI no. 111', '163, no. 5. A', 'A. V. no. 2', 'A. V. no. 25',
           'A. V. no. 26', 'A. V. no. 28']:
    pat = re.escape(cm).replace(r'\ ', r'\s+')
    check('call mark %s' % cm, re.search(pat, t[START:ti]))

# bibliography verbatim
bib_t = t[t.find('ZHGP —'):ti].rstrip()
check('bibliography verbatim', bib in bib_t)
check('bibliography ends with Zimmermann',
      'Zimmermann Kazimierz' in bib_t and
      'Poznań 1915' in bib_t)

print('T1 %s' % ('ALL PASS' if ok else 'FAILURES PRESENT'))
