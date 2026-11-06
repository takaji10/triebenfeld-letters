# -*- coding: utf-8 -*-
"""Final QA sweep of original.md."""
import re
from collections import Counter

t = open(r'literature\rusinski1947\original.md', encoding='utf-8').read()
ok = True


def check(name, cond):
    global ok
    print(('PASS' if cond else 'FAIL'), name)
    if not cond:
        ok = False


# 1. footnote pairing (the annex tables reuse one def for several
# refs by design - e.g. 0158's notes 3 and 5 each serve two rows - so
# the check is key-set equality: every label has a def and every def
# is referenced; the body's strict 1:1 counts live in verify_round*)
body = Counter(re.findall(r'\[\^(\d+-\d+)\](?!:)', t))
defs = Counter(re.findall(r'\[\^(\d+-\d+)\]:', t))
check('label keys == def keys (%d/%d keys)' % (len(body), len(defs)),
      set(body) == set(defs))

# 2. page-label sequence: front I, III, V..X; body 1..123; ANEKS II/III
# 145..156; the plates label 157
labels = re.findall(r'\[p\. ([IVX\d]+)\]', t)
expect = (['I', 'III'] + ['V', 'VI', 'VII', 'VIII', 'IX', 'X'] +
          [str(i) for i in range(1, 124)] +
          [str(i) for i in range(145, 157)] + ['157'])
check('page labels complete (%d)' % len(labels), labels == expect)

# 3. no dangling placeholders ('XXX' legitimately occurs as Roman
# numerals in citations - t. XXXVIII, s. LXXXIV)
for bad in ('next sitting', 'TODO', 'FIXME'):
    check('no %r placeholder' % bad, bad not in t)

# 4. the plates recorded
check('plates recorded', 'tom5_0172' in t and 'not transcribed' in t)

# 5. ANEKS II/III present
check('ANEKS II present', '[p. 145]' in t)
check('ANEKS III present', '[p. 151]' in t)

# 6. def blocks well-formed: every def line starts a line
bad_defs = [m.start() for m in re.finditer(r'(?<!\n)\[\^\d+-\d+\]:', t)]
check('def blocks all line-initial', not bad_defs)

# 7. the compose format is '[p. N]\n\n\n<para>' (label line, blank,
# paragraph block) - only flag a page head followed by NOTHING
dead = re.findall(r'\[p\. [^\]]+\]\n\n\n+\[p\.', t)
check('no empty pages (%d)' % len(dead), not dead)

# 8. the annex as Markdown tables: 282 data rows + the series spans
at = t[t.find('ANEKS I'):t.find('[p. 145]')]
nums = re.findall(r'^\| (\d+) \|', at, re.M)
check('annex md rows 282', len(nums) == 282)
check('annex spans a1-111 b1-156 c1-9',
      '| 111 |' in at and '| 156 |' in at and 'Trojanowskie' in at)
# the print repeats its table header on every sheet, and sheet 0159
# carries a second table (the sub-table 'Osady o charakterze
# nieokreslonym') - 22 headers total
check('table headers 22', at.count('Lp. | Nazwa osady') == 22)

# 10b. the series-c footnote block (0158's sołtys remarks) present
# below its table
check('series-c notes present', 'Sołtys za osobnym' in at
      and 'dziedziczny' in at)

# 9. the S09 [sic] markers (the book's own 1889/1890 error)
check('S09 [sic] present', '1889 [sic]' in t and '1890 [sic]' in t)
check('Tp. 72 [sic] present', 'Tp. 72 [sic; TKS. 72]' in t)

# 10. the l->I normalization (editor ruling): no KI./OI./OIL sigla left
left = re.findall(r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])(KI\.|OIL\b|OI\.)', t)
check('no KI./OI. residue (%d)' % len(left), not left)

print('---')
print('QA', 'ALL PASS' if ok else 'FAILURES PRESENT')
