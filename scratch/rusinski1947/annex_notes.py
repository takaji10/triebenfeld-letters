# -*- coding: utf-8 -*-
"""The annex tables' footnote apparatus, transcribed from the prints.

The print attaches numbered footnotes to the ANEKS I tables in two ways:
(a) superscript digits after the Nazwa cell's text, (b) - for the two
osady whose figures split between two entries (Niewiemko Nowe/Stare) -
asterisk-keyed. The note blocks print below a sheet's table; a row's ref
resolves to the nearest block below its own sheet (blocks are numbered
from 1 each). Printed-page label prefixes follow the draft convention
[^<page>-<n>].

RAZEM holds the series' totals rows (a: below 0146, b: below 0157) that
the row detection missed; the c-series totals (u0/u2) come from the
furniture layer of annex_md.json.
"""

# refs: (sheet, row) -> (note_number, printed_page_of_block, junk_chars)
# junk_chars = the OCR artifact the superscript left in the nazwa cell
REFS = {
    ('0143', 72): (1, '129', ' 1'),
    ('0145', 88): (1, '131', ' !'),
    ('0150', 52): (1, '137', '!'),
    ('0148', 23): (1, '137', ''),
    ('0152', 88): (2, '137', ' ?'),
    ('0155', 122): (1, '141', ' !'),
    ('0156', 141): (1, '141', '! i'),
    ('0156', 143): (1, '141', ' !'),
    ('0158', 1): (2, '143', '”?'),
    ('0158', 2): (3, '143', ''),
    ('0158', 3): (4, '143', ' 4'),
    ('0158', 4): (3, '143', ''),
    ('0158', 5): (5, '143', ' ?'),
    ('0158', 6): (6, '143', ''),
    ('0158', 7): (7, '143', ' ”'),
    ('0158', 8): (5, '143', ' 9'),
    ('0158', 9): (1, '143', ' ⁹'),
    ('0159', 10): (1, '144', ' !'),
    ('0159', 11): (2, '144', ' *?'),
    ('0159', 1): (3, '144', ' Ś'),
    ('0159', 2): (4, '144', ' *'),
    ('0159', 3): (5, '144', ' 5'),
    ('0159', 4): (6, '144', ' $'),
}

# asterisk-keyed note (0152 note 1): the dymy cells 10*/5* carry it
ASTERISK_NOTES = {'0152': [1]}

RAZEM = {
    '0146': {'cells': ['Razem z poprzedn.', '—', '—', '—', '—', '—',
                       '—', '—', '2.386', '92', '12.967'],
             'ref': (2, '131')},
    '0157': {'cells': ['Razem z poprzedn.', '—', '—', '—', '—', '—',
                       '—', '—', '2.071', '38', '4.484'],
             'ref': None},
}

NOTES = {
    '0144': [
        (1, 'Nie jest rzeczą całkiem pewną, czy osada Pożegowskie Ol. '
            'należała do osad typu olęderskiego. Wiadomości źródłowe '
            'przedstawiają się tu następująco: MP: Hol. Pożegowskie. — '
            'MG i MGd: Pożegowo (wieś). — Tp. 75: Olędry Pożegowskie, '
            'd. 18. — O 83, XVIII: Holędry Pożegowskie. — VO 84 '
            '(16—19. II 1783): „wieś z folwarkiem, 4 inquilini... agros '
            'colentes”. — Toł., Tp. 89 i OWK 89: brak. — Rel. Cost. '
            'nr 222, r. 1789, fol. 258, osada wsi: Walenty komornik, '
            'komornica Magdalena, Sebestyan chałupnik, Jan owczarz, '
            'Łukasz chałupnik, Maciejowa komornica, Antoni sołtys '
            'chałupnik, Jan komornik, Mikołaj gościnny, komornica '
            'Naganianka, Stanisław rybak, Sobestyan komornik. — TV: '
            'Pożegowe, wieś, folw., owczarnia, karczma, d. 9. Ciągłe '
            'zmniejszanie się dymów wskazywałyby na to, że być może, '
            'uczyniono tutaj próbę skolonizowania wsi na prawie '
            'olęderskim, jednak z niewiadomych przyczyn wieś powoli '
            'pustoszała, aż około r. 1793 (TV) znowu część ról '
            'wiejskich obrócono na folwark.'),
    ],
    '0146': [
        (1, 'Sroczewskie Olędry powstały z dawnej wsi Sroczewa '
            'i osadzonej na części jej gruntów kolonii olęderskiej. '
            'Były więc z początku osadą mieszaną. Przed r. 1789 starzy '
            'mieszkańcy zostali prawdopodobnie przeniesieni na prawo '
            'olęderskie i przyłączeni do gminy olędrów. Wynika to '
            'z wzmianek źródłowych: VO 78 — „Nova Colonia Sroczewskie '
            'Holędry i Sroczewo cum colonistis et cum molendino '
            'aquatico”; O 83 XX — „Sroczewo wioska z Olędrami”; Tp. 89 '
            '— Sroczewo Olędry d. 22; Tp. 89 i 90 — Hol. Sroczewo '
            'd. 22; OWK 89 — „Sroczewo wieś czyli Olędry dziedziczne”; '
            'MP — Holendry Sroczewskie; MG i MGd. — Sroczewo Holl. '
            'W chwili regulacji (AGH sąd Śrem, majętn. Książ, vol. I, '
            'fol. XVI i nast.) wszyscy mieszkańcy są oczynszowani '
            'i siedzą na równych prawach.'),
        (2, 'Razem z Ol. Góry.'),
    ],
    '0152': [
        (1, 'Jest rzeczą wątpliwą, czy były to dwie odrębne osady.'),
        (2, 'Osada wyrosła z dwóch odrębnych osiedli: 1. Olędrów '
            'Krobielewskich powstałych na miejscu dawnego Krobielewa. '
            'Pierwszy przywilej datuje się z r. 1661 — przywilej '
            'z r. 1672 jest przywilejem późniejszym dla tej samej '
            'osady. A.O. Nath, Die Gründung der Gemeinde Grosskrebbel. '
            'Grenzmärkische Heimatblätter, roczn. 14, s. 115, '
            'niesłusznie łączy z nim powstanie olędrów. Zaznaczyć '
            'należy, że autor ten, publikując przywilej w j. '
            'niemieckim, przemilczał, że oryginał wystawiony został '
            'w j. polskim; 2. Olędrów założonych na miejscu dawnej '
            'wsi Baba i tak też nazwanych przez założyciela. Ta '
            'ostatnia nazwa nie utrzymała się, a osady zlały się '
            'w jedną, przyjmując wspólną nazwę Nowe al. '
            'Wielkokrobielewskie Olędry.'),
    ],
    '0156': [
        (1, 'Osada powstała przez odłączenie się od Budziszewskich '
            'Olędrów.'),
    ],
    '0158': [
        (1, 'Razem z olędrem zamieszkałym za wsią na miejscu Trzy '
            'Góry.'),
        (2, 'Osadnicy mają własny samorząd z wybieralnym sołtysem, '
            'jednak równorzędność i solidarność w stosunku do pana '
            'nie jest całkowicie zachowana wskutek tego, że '
            'powinności dworskie wymierzone są od poszczególnych '
            'gospodarstw, a nie od jednostki gruntu.'),
        (3, 'Sołtys z nominacji pańskiej, ale kompetencje ma takie '
            'same, jak w innych wsiach olęderskich.'),
        (4, 'Nie wiadomo, czy osadnicy mieli własne sądownictwo. '
            '(W przywileju znajduje się tylko postanowienie, że '
            'gdyby się powaśnili, winny podpadać karze).'),
        (5, 'Sołtys za osobnym przywilejem. Ustanawia go dwór. '
            'Kompetencje jednak ma zwyczajne, powinnościami '
            'dworskimi niczym nie różni się od reszty mieszkańców.'),
        (6, 'Sołtys stały, wybieralni 2 ławnicy.'),
        (7, 'Osada lokowana na zasadach prawa niemieckiego (jako '
            'tzw. wieś sołtysia — sołtys otrzymał stanowisko '
            'nadrzędne w gminie). Dopiero dodatkowy przywilej z '
            'r. 1736 nazywa mieszkańców olędrami i traktuje ich '
            'równorzędnie. Sołtys prawdopodobnie pozostał nadal '
            'dziedziczny.'),
    ],
    '0159': [
        (1, 'Przywilej indywidualny dla 1 osadnika z r. 1755. Później '
            'widocznie na tych samych warunkach zostali osadzeni inni '
            'osadnicy. Według Kl. XII 6 I, fol. 118, dzierżą '
            'gospodarstwa na tych samych warunkach. Nazywani są tam '
            'olędrami.'),
        (2, 'Osadnicy mają własny samorząd z wybieralnym sołtysem, '
            'jednak równorzędność i solidarność w stosunku do pana '
            'nie jest całkowicie zachowana wskutek tego, że '
            'powinności dworskie wymierzone są od poszczególnych '
            'gospodarstw, a nie od jednostki gruntu.'),
        (3, 'Charakter osady w źródłach występuje niejasno: MP podaje: '
            '„Hollendry Janikowo”, inne źródła, jak MG, Tp. 89, 90, '
            'O 83, VO 84 (2 IV 1778) i TV określają osadę jako wieś. '
            'Przywilej generalny dla okupników klucza kicińskiego '
            '(por. aneks II, s. 121) wyliczając wszystkich okupników, '
            'Ol. Janikowo nie wymienia, natomiast w dalszej treści '
            ' przywileju mamy wzmiankę: „Janikoscy Hollendrzy”.'),
        (4, 'Wszystkie dane źródłowe ograniczają się tu do '
            'następujących wzmianek: MP — Jasien, MG — Jasienie od. '
            'Jaszin, Tp. 89, 90 — Jasion, O 83 — Jasien, wieś cała '
            'okupna, VO 84 (29 IX 1777) — „Coloni”, niegdyś '
            '10 kmieci.'),
        (5, 'Zachowały się 2 przywileje indywidualne dla 2 osadników, '
            'które z olęderskimi mało mają cech wspólnych, jednak '
            'Tp. 90 wykazuje dla tej osady 7 dymów, co dowodzi, że '
            'siedzieli tam i inni osadnicy. O ich sytuacji '
            'gospodarczo-prawnej brak jakichkolwiek danych '
            'źródłowych, natomiast w źródłach osada nazywana jest '
            'stale olędrami.'),
        (6, 'Osada stale nazywana olędrami, liczy jednak zaledwie '
            '2 dymy, a w TV jako mieszkańcy podani 1 olęder '
            'i chałupnik (Bidner). Czy w tym stanie rzeczy mogła '
            'istnieć osada olęderska, wydaje się rzeczą wątpliwą.'),
    ],
}
