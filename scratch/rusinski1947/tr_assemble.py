# -*- coding: utf-8 -*-
"""Assemble english.md: front matter + T2..T5 + the ANEKS-I note + T6."""
import os

BASE = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
        r'\rusinski1947')
TR = os.path.join(BASE, 'scratch', 'rusinski1947', 'tr')
ENG = os.path.join(BASE, 'literature', 'rusinski1947', 'english.md')

order = ['t2_a.md', 't2_b.md', 't2_c.md',
         't3_a.md', 't3_b.md', 't3_c.md',
         't4_a.md', 't4_b.md', 't4_c.md',
         't5_a.md', 't5_b.md', 't5_c.md']

head = open(ENG, encoding='utf-8').read()
# idempotent: T1 (front matter) = everything before the first [p. 1]
cut = head.find('[p. 1]')
if cut > 0:
    head = head[:cut]
head = head.rstrip() + '\n'

parts = [head]
for f in order:
    p = os.path.join(TR, f)
    txt = open(p, encoding='utf-8').read().strip()
    parts.append(txt + '\n')

# the ANEKS-I note (decision D6: the annex tables are not translated)
parts.append("""[p. 123]

**ANEKS I** — [The settlement tables of this annex (printed pp.
123–144) are not translated in this edition; the Polish tables,
reconciled against the page images, are in `original.md`, pp. 123–144.]
""")

parts.append(open(os.path.join(TR, 't6_a.md'),
                  encoding='utf-8').read().strip() + '\n')

out = '\n'.join(parts)
# normalize: no triple blank lines
while '\n\n\n' in out:
    out = out.replace('\n\n\n', '\n\n')
open(ENG, 'w', encoding='utf-8', newline='\n').write(out)
print('english.md assembled: %d chars' % len(out))
