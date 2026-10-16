# -*- coding: utf-8 -*-
"""The editor's answers on the spot sheet "Doubtful readings in the visitation of Trąbczyn" (2026-10-16).

    python units/adwl85/intake/spot_answers.py      # once; then holding.py --write --english --cache

Their answers are intake/readings_answers.json (copied from review/adwl85/).
Each answer is applied to the Polish (text85.py), the English (english85.py),
the catchword entry that quotes the next line (catchwords.yml) and the claim
check where it quotes the word. How each was taken:

- s01 Kozierok[?]: no button, the note "Kozierog[?]": their reading, kept with its doubt.
- s02 Uta[?]: no button, the note "Maybe Ułazwany, if that's a word?". In this hand ł is
  a t with a bar (Kościoła looks like "Kościota"), so their letters are "Uła" and the
  word after it is "zwany", called: "Folwark Uła[?] zwany". Kept with doubt, as they
  were unsure.
- s03 obok; s04 trumną; s05 Bogusławskiego; s06 Golinską; s07 Dręzgi; s08 Illust:;
  s11 58: read without doubt.
- s09 Gralewska: their reading, without doubt.
- s10 "podciorze", noted "Unsure": their reading, kept with doubt. Not understood; the
  English keeps the word.
- s12 "rozrządzonę": their reading, without doubt. Old Polish "rozrządzić" is to settle
  children with their portions; the English says "settled".
Marks of doubt in the holding: 12 before, 3 after.

Applied once, 2026-10-16 (the Polish in a first run; the English, catchwords.yml and
the claim check after one pattern was put right). Do not run it again.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(HERE)

PL = [
    ('Kozierok[?]', 'Kozierog[?]'),
    ('Uta[?]', 'Uła[?]'),
    ('oboki[?]', 'obok'),
    ('trumną[?]', 'trumną'),
    ('Bagusławskiego[?]', 'Bogusławskiego'),
    ('Golinską[?]', 'Golinską'),
    ('Drezgi[?]', 'Dręzgi'),
    ('Illust:[?]', 'Illust:'),
    ('Jalewska[?]', 'Gralewska'),
    ('sadowne[?]', 'podciorze[?]'),
    ('58[?]', '58'),
    ('rozrządzone[?]', 'rozrządzonę'),
]
EN = [
    ('Sariusz [uncertain: Kozierok] Kozierowski', 'Sariusz [uncertain: Kozierog] Kozierowski'),
    ('the farm called [uncertain: Uta]', 'the farm called [uncertain: Uła]'),
    ('[uncertain: Beside it], on the south side', 'Beside it, on the south side'),
    ('catafalque with a [uncertain: coffin],', 'catafalque with a coffin,'),
    ('placed by the noble Mr [uncertain: Bagusławski]', 'placed by the noble Mr Bogusławski'),
    ('by the noble Lady [uncertain: Golinska] on the estate', 'by the noble Lady Golinska on the estate'),
    ('from the farm of [uncertain: Drezgi]', 'from the farm of Dręzgi'),
    ('a decree of the [uncertain: Most Illustrious] Official', 'a decree of the Most Illustrious Official'),
    ('a meadow called [uncertain: Jalewska]', 'a meadow called Gralewska'),
    ('on which are [uncertain: orchards] and the parish buildings', 'on which are gardens [uncertain: podciorze] and the parish buildings'),
    ('| 275 | 298 | [uncertain: 58] | 48', '| 275 | 298 | 58 | 48'),
    ('whose great-grandchildren are [uncertain: rozrządzone].', 'whose great-grandchildren are settled.'),
]
CW = [('Łąka nazwana Jalewska[?] z dawna', 'Łąka nazwana Gralewska z dawna')]
CC = [
    ('Folwark Uta[?] zwany', 'Folwark Uła[?] zwany'),
    ('dziesięcina z Folwarku Drezgi[?] toz', 'dziesięcina z Folwarku Dręzgi toz'),
    ('Karczma Dekretem Illust:[?] Offła', 'Karczma Dekretem Illust: Offła'),
    ('the boys\' column, with 58[?] for the town, gives', 'the boys\' column, with 58 for the town, gives'),
]


def rep(name, pairs):
    p = os.path.join(UNIT, name)
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a)
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


if __name__ == '__main__':
    rep('intake/text85.py', PL)
    rep('intake/english85.py', EN)
    rep('catchwords.yml', CW)
    rep('intake/claim_check.yml', CC)
    print('applied')
