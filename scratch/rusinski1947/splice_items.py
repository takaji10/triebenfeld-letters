# -*- coding: utf-8 -*-
"""Splice the round-3 ITEMS into spot_html_gen.py."""
import io, os
P = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba' \
    r'\rusinski1947\scratch\rusinski1947\spot_html_gen.py'
src = open(P, encoding='utf-8').read()
first = src.find('ITEMS = [')
k = src.find('# ---------------- the tables')
assert first > 0 and k > first, (first, k)
ITEMS = '''ITEMS = [
    ('S43', 'B', 'p. 129', 'the asterisk note above the table',
     '* Dymy niekt\\u00f3rych osad podane s\\u0105 w Tp. 89 zbiorowo '
     'dla ca\\u0142ej osady; wysoko\\u015b\\u0107 ich na '
     'poszczeg\\u00f3lne zagrody przeliczona zosta\\u0142a '
     'wed\\u0142ug Tp. 90.',
     'confirm or correct the wording (the scan is marginal)',
     'the band = the print page\\'s top strip (rotated in the scan); '
     'the note sits under the column header.',
     'S43_p129_band.png'),
    ('S44', 'B', 'p. 131', 'the two notes on p. 131 - do they match '
     'the transcription?',
     'transcribed: 131-1 = "Sroczewskie Ol\\u0119dry powsta\\u0142y z '
     'dawnej wsi Sroczewa..." (long); 131-2 = "Razem z Ol. '
     'G\\u00f3ry."',
     'confirm the band\\'s two note lines are these two notes (and '
     'their order)',
     'the band shows the notes small; the transcription came from '
     'the strip OCR.',
     'S44_p131_band.png'),
    ('S45', 'B', 'p. 124', 'TABELA VI + the a-table\\'s title',
     'TABELA VI / Osady ol\\u0119derskie w by\\u0142ym powiecie '
     'ko\\u015bcia\\u0144skim w okresie rozbior\\u00f3w',
     'confirm the exact wording of the title line',
     'the band\\'s second and third lines.',
     'S45_p124_band.png'),
    ('S46', 'B', 'p. 132', 'TABELA VII + the b-table\\'s title',
     'TABELA VII / Osady ol\\u0119derskie w by\\u0142ym powiecie '
     'pozna\\u0144skim w okresie rozbior\\u00f3w',
     'confirm the exact wording (does it mention ziemia wschowska '
     'too?)',
     'the band\\'s second and third lines.',
     'S46_p132_band.png'),
    ('S47', 'B', 'p. 143', 'the c-table\\'s title',
     'Osady ol\\u0119derskie w ziemi wschowskiej w okresie '
     'rozbior\\u00f3w (no TABELA number seen)',
     'confirm the exact wording and whether a TABELA number '
     'precedes it',
     'the band\\'s second line.',
     'S47_p143_band.png'),
    ('S48', 'B', 'p. 130', 'the p. 130 band: is there a continuation '
     'marker?',
     '(nothing transcribed)',
     'does the print carry a "(ci\\u0105g dalszy)" or similar '
     'marker on p. 130 (and the other continuation pages)?',
     'the band between the running head and the column header.',
     'S48_p130_band.png'),
    ('S49', 'B', 'p. 62', 'TABELA III - the repair pass',
     'the table is garbled; the notes are unlinked',
     'your marker info is logged (b. cha\\u0142upnicy[^1]; the '
     'Rolnictwo line: 60[^2] and 13[^2]; the O\\u015bw. line: '
     '5[^3]). I will do a dedicated pixel-level repair pass of the '
     'table and then wire the four notes - no answer needed now, '
     'unless you want to prioritize it.',
     'the table spans most of p. 62.',
     None),
    ('S50', 'B', '?', 'the Ujskie czynsz amount - which print page?',
     'our p. 86 reads: "W najwcze\\u015bniejszych osadach by\\u0142 '
     'on bardzo niski: w Ujskich Ol. (r. 1597) wyrosi\\u0142 ___ '
     'z\\u0142 z huby 30-morgowej, w Ol. Nowe Dwory (r. 1601) 25 '
     'z\\u0142 z huby..."',
     'you marked this "not on page 86" - which print page holds '
     'this sentence? (our page labels may drift from the print\\'s '
     'folios in the body; the sentence\\'s true page would '
     'recalibrate them)',
     'the sentence opens the czynsz-gruntowy discussion.',
     None),
]
'''
new = src[:first] + ITEMS + src[k:]
with open(P, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(new)
print('spliced, items block', len(ITEMS), 'chars')
