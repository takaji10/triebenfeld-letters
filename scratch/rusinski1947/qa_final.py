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


# 1. footnote pairing
body = Counter(re.findall(r'\[\^(\d+-\d+)\](?!:)', t))
defs = Counter(re.findall(r'\[\^(\d+-\d+)\]:', t))
check('labels == defs (%d/%d)' % (sum(body.values()), sum(defs.values())),
      sum(body.values()) == sum(defs.values()) and
      not [k for k in body if body[k] > defs.get(k, 0)] and
      not [k for k in defs if defs[k] > body.get(k, 0)])

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

# 8. the four annex furniture rows + all 282 annex rows
at = t[t.find('ANEKS I'):t.find('[p. 145]')]
nums = re.findall(r'^(\d+)\. ', at, re.M)
check('annex rows 282', len(nums) == 282)
check('annex numbering spans a1-111 b1-156 c1-9',
      '111. ' in at and '156. ' in at and 'Trojanowskic' in at)

# 9. the S09 [sic] markers (the book's own 1889/1890 error)
check('S09 [sic] present', '1889 [sic]' in t and '1890 [sic]' in t)

print('---')
print('QA', 'ALL PASS' if ok else 'FAILURES PRESENT')
