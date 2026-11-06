# -*- coding: utf-8 -*-
"""Fix annex_rows2.py: move the stray cell_cands block (currently
nested inside the sheet loop with a glued def line) to module level."""
p = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947\annex_rows2.py'
lines = open(p, encoding='utf-8').readlines()
# locate the broken def and the end of its body ('    return out')
i0 = next(i for i, l in enumerate(lines)
          if l.strip().startswith('def cell_cands'))
i1 = next(i for i, l in enumerate(lines) if l.strip() == 'return out')
body = lines[i0 + 1:i1 + 1]
del lines[i0:i1 + 1]
# dedent the body to module level and prepend a proper def
block = ['def cell_cands(n, top):\n'] + [b[4:] if b.startswith('    ')
                                         else b for b in body]
# insert after img()'s return
i2 = next(i for i, l in enumerate(lines) if l.strip() == 'return imgs[n]')
lines[i2 + 1:i2 + 1] = ['\n\n'] + block
open(p, 'w', encoding='utf-8').writelines(lines)
print('fixed; cell_cands now at module level')
