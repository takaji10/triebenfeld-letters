# -*- coding: utf-8 -*-
"""The editor's corrections to document 1 of APP 53/968/0/-/669 (2026-10-14), applied once.

    python units/app539680669/intake/editor_corrections.py

A record, not to be run again (it asserts the old readings). It edits TEXT in
holding.py and ENGLISH in english.py; then holding.py --write --english
--cache and a rebuild. Page numbers are the document's (1 the cover, 2
inside the front cover, 3 = 0002_a2 ...).

The editor read the English against the scans and sent these corrections.
Years shown as "1,907" were a fault of the edition's thousands grouping,
which took only 1500-1899 for years (numerals.py, now 1500-1999); nothing in
the text was changed for them.

Page 35 (inside the back cover): the editor's own reading, with gaps, was
read again against the scan and partly completed here: "weil", "ihn" and
"herausgerettet", "i. d. Hölle", "von", and "Pfaffen" for the editor's
"Pfaffer". The last lines are a saying: when the paving in hell, made of
pastors and priests, is finished, the world will end.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))

TEXT_FIXES = [
    # p. 4
    ('Aus Smaszew Gem.', 'Aus Grodziec Gem.'),
    ('Czarnica, Grondy.', 'Ciswica, Grondy.'),
    # p. 8
    ('[?] [?] der [?]\nMielke\nin Łazinsk.', 'Westlig[?] der Schule\nMielke\nin Łazinsk.'),
    ('„[Gehege?]" [?] in [?]', '„[Gehege?]" [?] in Grądzeń'),
    # p. 9
    ('„Morast". —', '„Moraß". —'),
    # p. 13
    ('Baustellen. In Emilienheim.\n„Kafeln"', 'In Emilienheim.\nBaustellen.\n„Kafeln"'),
    # p. 14
    ('31. I. 1864 [gestor…?]', '31. I. 1864 gestor[ben]'),
    # p. 17
    ('Zelmer Ed. war 34 Jahre.', 'Zelmer Ed[uard] war 34 Jahre.'),
    # p. 19: the insertion "heiratstüchtige" is marked to stand after "Züchten"
    ('sagt man „[Züchten?]"\nin Zamęty.\nheiratstüchtige\n', 'sagt man „[Züchten?]"\nheiratstüchtige\nin Zamęty.\n'),
    # p. 22
    ('5) Gä[ehe?]blotte', '5) Oldergschie[h?]'),
    # p. 23
    ('ge[?]kt, vor 50 Jahren.', '[gefinkt?], vor 50 Jahren.'),
    # p. 27
    ('Las, Chruścik — Brücher', 'Las, Chruściki — Brücher'),
    # p. 28
    ('(als Kind immer Pastor werden. —)\nEin Sohn d. Schultz Pastor i. Deutschl.',
     'Ein Sohn d. Schultz Pastor i. Deutschl.\n(als Kind immer Pastor werden. —)'),
    # p. 30
    ('N 4 Haus 12 1/25', 'N 4 Fam[?] 12 1/25'),
    # p. 31
    ('Michalinow!', 'Michalinow'),
    ('''I Kl. 14 Mor. Bl. 9. 1/10 Sek
II " 235 " Land.
III " 25 " 5 Uhr Bl. 12
IV " 49 " Gf. 1/5
Nieużyt. 14 "
337 morg.''', '''I Kl. 14 Mor.
II " 235 "
III " 25 "
IV " 49 "
Nieużyt. 14 "
337 morg.
Bl. 9. 1/10 Sek
Land.
5 Uhr Bl. 12
Gf. 1/5'''),
    # p. 32
    ('5 [Kistler?] Bl. 18', '5 Kinder Bl. 18'),
    # p. 33
    ('3 [Mielke?] 9 Uh', '3 Birke 9 Uh'),
    # p. 35
    ('''[?]: Wasserquelle
haben d. Polen verbo¬
ten d. [Rutkowski?] [?]
[?] [?] [?]
den [Rutkowski?] nach [Wars…?]
abgeholt, die Gem. [?]
[?].
[?] das Pflaster [?] [?]
[?] Posen u. [Pfaffen?]
fertig ist, dann geht
die Welt unter.''', '''Gebet[buch?]: Wasserquelle
haben d. Pastoren verbo¬
ten d. Rutkowski [weil?]
[sein?] [?] [vorynier?]
den Rutkowski nach Warschau
abgeholt, die Gem. [ihn?]
herausgerettet.
[?] das Pflaster i. d. [Hölle?]
[von?] Pastoren u. Pfaffen
fertig ist, dann geht
die Welt unter.'''),
]

ENGLISH_FIXES = [
    ('From the Smaszew congregation', 'From the Grodziec congregation'),
    ('Czarnica, Grondy.', 'Ciswica, Grondy.'),
    ('[illegible] [illegible] of the [illegible]\nMielke\nin Łazinsk.',
     '[uncertain: Westlig] of the school\nMielke\nin Łazinsk.'),
    ('"[uncertain: Gehege]" [illegible] in [illegible]', '"[uncertain: Gehege]" [illegible] in Grądzeń'),
    ('"Morast" (bog). —', '"Moraß" (bog). —'),
    ('Baustellen (building plots). In Emilienheim.\n"Kafeln"',
     'In Emilienheim.\nBaustellen (building plots).\n"Kafeln"'),
    ('31 January 1864 [uncertain: died…]', '31 January 1864 died'),
    ('In the Pyzdry Hollands\nWrocław and Züllichau [books]',
     'In the Pyzdry Hollendry\npeople from Wrocław (Breslau) and Züllichau'),
    ('Ed. Zelmer was there 34 years.', 'Ed[uard] Zelmer was there 34 years.'),
    ('someone else passed the\nexamination for him.', 'someone else passed the\nexamination for him (Zelmer).'),
    ('they say "[uncertain: Züchten]"\nin Zamęty.\nmarriageable\nPlötzer = gallants',
     'they say "[uncertain: Züchten]",\nmarriageable,\nin Zamęty.\nPlötzer = Kavaliere (gallants, bachelors)'),
    ('5) Gä[uncertain: ehe]blotte', '5) Oldergschie[uncertain: h]'),
    ('ge[illegible]kt, 50 years ago.', '[uncertain: gefinkt], 50 years ago.'),
    ('"In the door a linen\npanel against the heat"',
     '"In der Tür eine Leinwandplatte\ngegen d. Hitze" (in the door a linen\npanel against the heat)'),
    ('"they all like poppy-seed dumplings"', '"alle essen gern Mohnklösse" (they all like poppy-seed dumplings)'),
    ('Las, Chruścik — Brücher', 'Las, Chruściki — Brücher'),
    ('"ick war do" = Brücher.\nI was there\ner hud = he had',
     '"ick war do" = Brücher.\nich war da (I was there)\ner hud = er hatte (he had)'),
    ('(as a child always [wanted to] be a pastor. —)\nA son of Schultz\'s a pastor in Germany.',
     'A son of Schultz\'s a pastor in Germany.\n(as a child always [wanted to] be a pastor. —)'),
    ('No. 4 house 12 1/25', 'No. 4 [uncertain: Fam.] 12 1/25'),
    ('Michalinow!', 'Michalinow'),
    ('''Class I 14 Morgen ap. 9. 1/10 sec.
II " 235 " land.
III " 25 " 5 o'clock ap. 12
IV " 49 " yellow filter 1/5
Waste land 14 "
337 Morgen.''', '''Class I 14 Morgen
II " 235 "
III " 25 "
IV " 49 "
Waste land 14 "
337 Morgen.
ap. 9. 1/10 sec.
land.
5 o'clock ap. 12
yellow filter 1/5'''),
    ('5 [uncertain: Kistler] ap. 18', '5 children ap. 18'),
    ('3 [uncertain: Mielke] 9 o\'clock', '3 birch 9 o\'clock'),
    ('''[illegible]: spring of water
the Poles have forbidden the [uncertain: Rutkowski] [illegible]
[illegible] [illegible] [illegible]
took [uncertain: Rutkowski] to [uncertain: Wars…]
away, the commune [illegible]
[illegible].
[illegible] the paving [illegible] [illegible]
[illegible] Poznań and [uncertain: Pfaffen]
is finished, then the world
will end.''', '''Prayer [uncertain: book]: spring of water
the pastors have forbidden
Rutkowski [uncertain: because]
[uncertain: his] [illegible] [uncertain: vorynier]
took Rutkowski away to Warsaw,
the community rescued [uncertain: him].
[illegible] the paving in [uncertain: hell]
[uncertain: of] pastors and priests
is finished, then the world
will end.'''),
]


def apply(path, fixes):
    s = io.open(path, encoding='utf-8').read()
    for a, b in fixes:
        assert s.count(a) == 1, (os.path.basename(path), a[:60])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    apply(os.path.join(HERE, 'holding.py'), TEXT_FIXES)
    apply(os.path.join(HERE, 'english.py'), ENGLISH_FIXES)
    print(len(TEXT_FIXES), 'text and', len(ENGLISH_FIXES), 'English corrections applied')
