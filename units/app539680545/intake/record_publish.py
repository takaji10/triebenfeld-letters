# -*- coding: utf-8 -*-
"""Record the publication of APP 53/968/0/-/545 (2026-10-25). Run once."""
import io

# TODO section 35: publish ticked
p = 'docs/TODO.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace(
    '## 35. APP 53/968/0/-/545: Breyer\'s sheets on the Polonised names (added and\n    translated 2026-10-25, on the branch app539680545; not published)',
    '## 35. APP 53/968/0/-/545: Breyer\'s sheets on the Polonised names (added,\n    translated and published 2026-10-25)')
s = s.replace('- [ ] Publish at your word.',
              '- [x] Published at your word (2026-10-25): the branch merged to main and\n      pushed; the "Build and deploy" run succeeded.')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# CLAUDE.md: not published -> published
p = 'CLAUDE.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace('2026-10-25 on the branch `app539680545`, **not published**):',
              '2026-10-25, **published 2026-10-25**):')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# changelog
p = 'docs/CHANGELOG.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace('## 2026-10-25 - APP 53/968/0/-/545 added and translated (branch app539680545; not published)',
              '## 2026-10-25 - Published\n\n- The editor said "Publish". Main was pushed after a local build and\n  verify passed; the "Build and deploy" run succeeded. APP 53/968/0/-/545\n  went live with it.\n\n## 2026-10-25 - APP 53/968/0/-/545 added and translated (branch app539680545)')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# NEEDS_CONFIRMATION: drop "not published"
p = 'docs/NEEDS_CONFIRMATION.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace('(Breyer\'s sheets on the Polonised names, added and\n  translated 2026-10-25, on the branch app539680545; not published;',
              '(Breyer\'s sheets on the Polonised names, added, translated and\n  published 2026-10-25;')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('bookkeeping updated')
