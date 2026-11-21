# -*- coding: utf-8 -*-
"""Superscript-remnant scan: letter immediately followed by a digit
outside refs/tables - the print's footnote markers glued to the word
by OCR ('polskie1.'). Excludes years, vol./Tp./fol. citations, table
rows, footnote-def lines."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
lines = t.splitlines()
hits = []
for idx, ln in enumerate(lines):
    if ln.startswith('|') or re.match(r'\[\^\d+-\d+\]:', ln):
        continue
    # mask legit digit contexts: [^..] refs, fol., vol., r., s., Tp.,
    # w., numbers with separators
    m_ln = re.sub(r'\[\^\d+-\d+\]', '@REF@', ln)
    for m in re.finditer(
            r'(?<![0-9IVXivx.\-])[a-ząćęłńóśźż](\d)(?![0-9.\-])', m_ln):
        i = m.start()
        ctx = m_ln[max(0, i - 45):i + 25].replace('\t', ' ')
        hits.append((idx + 1, m.group(1), ctx))
print(len(hits), 'letter+digit hits in prose')
for idx, dg, ctx in hits:
    print('L%-5d %s  %r' % (idx, dg, ctx))
