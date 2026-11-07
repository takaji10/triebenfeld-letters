# -*- coding: utf-8 -*-
"""Replace the ITEMS block with the round-4 residue (ANEKS I out of
scope - the editor edits aneks_i.xlsx and reinserts it later)."""
P = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba' \
    r'\rusinski1947\scratch\rusinski1947\spot_html_gen.py'
src = open(P, encoding='utf-8').read()
first = src.find('ITEMS = [')
k = src.find('# ---------------- the tables')
assert first > 0 and k > first, (first, k)
ITEMS = '''ITEMS = [
    ('S50', 'B', '?', 'the Ujskie czynsz amount - which print page?',
     'our p. 86 reads: "W najwcze\\u015bniejszych osadach by\\u0142 '
     'on bardzo niski: w Ujskich Ol. (r. 1597) wyrosi\\u0142 ___ '
     'z\\u0142 z huby 30-morgowej, w Ol. Nowe Dwory (r. 1601) 25 '
     'z\\u0142 z huby..."',
     'tell me which print page holds this sentence (and the amount '
     'while you are there). The page number would recalibrate our '
     'body page labels, which may drift from the print\\'s folios.',
     'the sentence opens the czynsz-gruntowy discussion, right '
     'after the numizmatyka paragraph.',
     None),
    ('S51', 'B', 'p. 62', 'TABELA III - the repair pass (planned)',
     'the occupational table (Sk\\u0142ad zawodowy ludno\\u015bci 36 '
     'osad ol\\u0119derskich powiatu pozna\\u0144skiego) is '
     'garbled; its four table-notes are unlinked.',
     'no answer needed - I will do a dedicated pixel-level repair '
     'pass and then wire your marker info (b. cha\\u0142upnicy[^1]; '
     'the Rolnictwo line: 60[^2] and 13[^2]; the O\\u015bw. line: '
     '5[^3]). Shown here only so you know it is on the worklist; '
     'skip this item.',
     'the table spans most of p. 62.',
     None),
]
'''
new = src[:first] + ITEMS + src[k:]
with open(P, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(new)
print('spliced')
