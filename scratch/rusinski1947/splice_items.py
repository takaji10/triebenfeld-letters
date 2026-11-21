# -*- coding: utf-8 -*-
"""Replace the ITEMS block: round 4 fully answered - no open items;
the sheet stays as the review harness for future rounds."""
P = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba' \
    r'\rusinski1947\scratch\rusinski1947\spot_html_gen.py'
src = open(P, encoding='utf-8').read()
first = src.find('ITEMS = [')
k = src.find('# ---------------- the tables')
assert first > 0 and k > first, (first, k)
ITEMS = '''ITEMS = [
]
'''
new = src[:first] + ITEMS + src[k:]
with open(P, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(new)
print('spliced: ITEMS emptied')
