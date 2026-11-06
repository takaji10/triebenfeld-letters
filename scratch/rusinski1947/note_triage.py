# -*- coding: utf-8 -*-
"""Note-noise triage: scan every footnote definition in the draft for
the catalogued strip-artifact classes."""
import re
from collections import Counter

t = open(r'literature\rusinski1947\original.md', encoding='utf-8').read()
defs = re.findall(r'\[\^(\d+-\d+)\]: (.*?)(?=\n\[\^|\n\n\[p\. |\Z)', t,
                  re.S)
print('defs:', len(defs))
hits = Counter()
examples = {}


def add(cls, lab, ctx):
    hits[cls] += 1
    examples.setdefault(cls, []).append((lab, ctx))


for lab, txt in defs:
    # 1. the l->I residue inside words (KI./OI. handled globally; the
    # 'l.' vs 'I.' inside citation strings)
    for m in re.finditer(r'(?<![A-Za-z])I(?=[a-ząćęłńóśźż])', txt):
        ctx = txt[max(0, m.start() - 25):m.end() + 25]
        add('I-inside-word', lab, ctx)
    # 2. 'CI' for 'Cl'/'Cz' family? 'Nie poł. 'Nicwiemko' class: the
    # leading N->Nic misreads
    for m in re.finditer(r'\bNic[a-ząćęłńóśźż]+', txt):
        ctx = txt[max(0, m.start() - 20):m.end() + 20]
        if not re.match(r'Nic\s*(z|za|pod|na|nad|bez|nie|co|kto|do|'
                        r'gdzie|jak|jeśli|raz|w)', m.group(0)):
            add('Nic-word', lab, ctx)
    # 3. 'OIL'/'OIl'/'OI.' variants (global pass covers OI.; this
    # catches 'OIl'/'OIL' with digit glue)
    for m in re.finditer(r'\bO[Il][\d.]', txt):
        add('OI-digit', lab, txt[max(0, m.start() - 15):m.end() + 15])
    # 4. the digit-l confusion: 'l4'/'1U'/'1Y'/'12U'/'1/' inside notes
    for m in re.finditer(r'\b\dl?\d*[UYG]\b|\b1[lUYG]\b', txt):
        add('digit-l', lab, txt[max(0, m.start() - 20):m.end() + 20])
    # 5. 'Roz.', 's.', 'fol.' glue with digits
    for m in re.finditer(r'fol\.[a-ząćęłńóśźż]', txt):
        add('fol-glue', lab, txt[max(0, m.start() - 15):m.end() + 15])
    for m in re.finditer(r'(?<=\d)0(?=[.,]\d)', txt):
        add('zero-after-digit', lab,
            txt[max(0, m.start() - 20):m.end() + 20])
for cls in hits:
    print(cls, hits[cls])
    for lab, ctx in examples[cls][:4]:
        print('    ', lab, repr(ctx[:70]))
