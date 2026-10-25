# -*- coding: utf-8 -*-
"""Add the Themen-block ruling to docs/CHANGELOG.md. Run once."""
import io

p = 'docs/CHANGELOG.md'
s = io.open(p, encoding='utf-8').read()
i = s.index('## 2026-10-25 - Published')
entry = ('## 2026-10-25 - The word of the Themen block ruled\n\n'
         '- The editor ruled the doubtful word of 0030\'s Themen block '
         '"polnische"\n'
         '  ("Verschlungen hat ihr der polnische Mund"). The transcription, '
         'the\n'
         '  English and the holding\'s pages corrected; the check clean; '
         'rebuilt.\n\n')
s = s[:i] + entry + s[i:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('changelog ok')
