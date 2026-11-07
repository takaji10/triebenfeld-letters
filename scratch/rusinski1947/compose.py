# -*- coding: utf-8 -*-
"""Compose original.md for Rusinski 1947 - the working draft.

Structure:
  - front matter (title page, imprint, contents, Wykaz skrotow) from
    front_matter.md (composed separately; included as a literal here);
  - the body pages [p. 1]..[p. 122] from the marked paragraphs;
  - the footnote definitions after each page's body, page-prefixed;
  - ANEKS I as HTML tables from annex_table.json (tier A/B rows parsed
    into the nine columns; tier C rows kept as raw cell text pending the
    spot sheet);
  - ANEKS II (pp. 145-150) and III (pp. 151-156) as prose;
  - the four plates recorded.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'literature', 'rusinski1947',
                   'original.md')

BODY = [f'{i:04d}' for i in range(16, 138)]
ANEX2 = [f'{i:04d}' for i in range(160, 166)]
ANEX3 = [f'{i:04d}' for i in range(166, 172)]


def label(n):
    return str(int(n) - 15)


# ---- SPOT ANSWERS round 2: the footnote-marker audit ---------------------
# sup_scan (letter+digit), fused_scan ('. N Capital' inside defs) and
# the dup-tail scan located the print's true superscript positions:
# miswired refs moved, fused note-splits + renumberings applied here.
# Keyed by scan number (label + 15).
BODY_FIXES = {
    '0016': [   # p. 1: markers 1-6 at their visible digits
        ('a więc[^1-1]', 'a więc'),
        ('Wschowską.[^1-2]', 'Wschowską.'),
        ('dotyczącym[^1-3]', 'dotyczącym'),
        ('Prace[^1-4][^1-5] tę', 'Prace tę'),
        ('Baranowskiego 1 wydana', 'Baranowskiego[^1-1] wydana'),
        ('Inglota? daje', 'Inglota[^1-2] daje'),
        ('Schmidta * wymienić', 'Schmidta[^1-3] wymienić'),
        ('Maasa4 i', 'Maasa[^1-4] i'),
        ('Schulza 5. Prace', 'Schulza[^1-5]. Prace'),
        ('Atlasu Historycznego Polski 6,',
         'Atlasu Historycznego Polski[^1-6],'),
    ],
    '0017': [   # p. 2: i->1 garbles; markers 2/3 at their sentences
        ('akta gruntowe 1[^2-2] hipoteczne 1,',
         'akta gruntowe i hipoteczne,'),
        ('ziemi wschowskiej z r. 1789. Ze zbiorów',
         'ziemi wschowskiej z r. 1789[^2-2]. Ze zbiorów'),
        ('spisu ludności %. Niestety', 'spisu ludności[^2-3]. Niestety'),
    ],
    '0045': [   # p. 30: markers 1-5 all at visible digits
        ('otrzymują[^30-1] grunty', 'otrzymują grunty'),
        ('brzmienie flamandzko-holenderskie[^30-2],',
         'brzmienie flamandzko-holenderskie,'),
        ('dla Ol. Ujskich1 1 Ol. Nowe Dwory ?,',
         'dla Ol. Ujskich[^30-1] i Ol. Nowe Dwory[^30-2],'),
        ('nazwiska osadników. Większość',
         'nazwiska osadników[^30-3]. Większość'),
        ('inwentarze majętności wieleńskiej4, '
         'przeciwstawiając ich[^30-3] osadnikom Niemcom 5.',
         'inwentarze majętności wieleńskiej[^30-4], '
         'przeciwstawiając ich osadnikom Niemcom[^30-5].'),
    ],
    '0081': [   # p. 66: split note 1 (Maas/Hładyłowicz), renumber 2-4
        ('nowożytną!, a uzasadniają krytyczne stanowisko '
         'Hładyłowicza ?.[^66-1]',
         'nowożytną[^66-1], a uzasadniają krytyczne stanowisko '
         'Hładyłowicza[^66-2].'),
        ('gruntów[^66-2]. Wyjątkowo', 'gruntów[^66-3]. Wyjątkowo'),
        ('grunt cudzy[^66-3]. Karczowanie', 'grunt cudzy[^66-4]. Karczowanie'),
    ],
    '0085': [   # p. 70: markers 8/9 at their '$'/'?' remnants
        ('w rozmiar gruntów$, tak samo', 'w rozmiar gruntów[^70-8], tak samo'),
        ('granice i miedze?. Niekiedy', 'granice i miedze[^70-9]. Niekiedy'),
        ('dodawał kawałek[^70-9] pan', 'dodawał kawałek pan'),
    ],
    '0104': [   # p. 89: markers 2/3/4/5 at their remnants; note 3+4 merged
        ('pan pobierał[^89-1] tynfów', 'pan pobierał tynfów'),
        ('od uiszczania opłat targowych w miastach',
         'od uiszczania opłat targowych[^89-1] w miastach'),
        ('od każdego aktu *%.', 'od każdego aktu[^89-2].'),
        ('opłatę for-[^89-2] malnie', 'opłatę formalnie'),
        ('Uiszczali ją olędrzy co[^89-3] lat w wysokości[^89-4] zł z huby',
         'uiszczali ją olędrzy co lat w wysokości zł z huby'),
        ('na posiedanym gruncie %.', 'na posiedanym gruncie[^89-3].'),
        ('przy wydawa-[^89-5] niu córek', 'przy wydawaniu córek'),
        ('polega na nieporozumieniu f.[^89-6]',
         'polega na nieporozumieniu[^89-4]'),
        ('przez rzekę Wertę5,', 'przez rzekę Wartę[^89-5],'),
    ],
    '0122': [   # p. 107: markers 1/3/4/5 at their digits/remnants
        ('Skorzystali z niego olędrzy1, Według obliczeń[^107-1] '
         'Kniata[^107-2]',
         'Skorzystali z niego olędrzy[^107-1]. Według obliczeń '
         'Kniata[^107-2]'),
        ('w dobrach państwowych[^107-3] gr', 'w dobrach państwowych gr'),
        ('w dobrach duchownych 7[^107-4] talarów 42[^107-5] gr',
         'w dobrach duchownych 7 talarów 42 gr'),
        ('kościoła parafialnego katolickiego *. Zdarzało',
         'kościoła parafialnego katolickiego[^107-3]. Zdarzało'),
        ('obu kościołów równocześnie 4, Świadczenia',
         'obu kościołów równocześnie[^107-4]. Świadczenia'),
        ('do znacznej wysokości 5,', 'do znacznej wysokości[^107-5].'),
    ],
}
# NOTE_FIXES: full ordered rebuild of a page's note list (num, text);
# the fused-note splits renumber the defs to the print's numbering.
NOTE_REBUILD = {
    # ---- SPOT round 5: the pp. 24-25 totals-notes in the print's
    # line-by-line layout (each figure + its text on its own line;
    # the arithmetic closes: 16.303-17=16.286, +92+15=16.393,
    # -2.478=13.915 / 14.489-16-84=14.389)
    '0039': [
        (1, 'Do tej cyfry dochodzimy drogą następujących obliczeń: '
            'Tp. 89 wykazuje dla powiatu kościańskiego\n'
            '    13.737 dymów szlacheckich\n'
            '    2.227 dymów duchownych\n'
            '    339 dymów królewskich\n'
            '    16.303 dymy\n'
            '    mniej 17 dymów wsi Orchowo, leżącej w pow. '
            'pyzdrskim,\n'
            '    16.286 dymów.\n'
            '    Dochodzą 92 dymy olęderskie, nie podane w Tp. 89,\n'
            '    oraz 15 dymów wsi Sowinice,\n'
            '    razem 16.393 dymy\n'
            '    mniej 2.478 dymów olęderskich.\n'
            '    Otrzymujemy w rezultacie 13.915 dymów.'),
    ],
    '0040': [
        (1, 'Tj. podane w Tp. 89\n'
            '    10.703 dymy szlacheckie\n'
            '    2.834 dymy duchowne\n'
            '    952 dymy królewskie\n'
            '    14.489 dymów\n'
            '    mniej 16 dymów liczonych w Tp. 89 podwójnie (Ol. '
            'Psarskie),\n'
            '    mniej 84 dymy należącej do Kościana majętn. '
            'Sowinice,\n'
            '    razem 14.389 dymów.\n'
            '    Dochodzą 42 dymy opuszczonej w Tp. 89 par. Iwno,\n'
            '    razem 14.431 dymów. Jak widzimy z zamieszczonej w '
            'aneksie I rubryki dymów nie uwzględnionych w Tp. 89, to '
            'ostatnie źródło dla powiatu poznańskiego jest '
            'niezupełne. Przypuszczać należy, że opuszczenia w Tp. '
            '89, na które natknęliśmy się przy obliczaniu dymów '
            'olęderskich, miały miejsce również w odniesieniu do '
            'pozostałych dymów wiejskich. Ponieważ jednak w ramach '
            'niniejszej pracy nie jest rzeczą możliwą sprawdzać '
            'dymy każdej z osobna miejscowości powiatu, '
            'poprzestać trzeba na powiększeniu dymów wiejskich '
            'nieolęderskich w tej samej proporcji, jak przy '
            'olędrach, tj. w proporcji 38 : 2216. Do poprzednio '
            'podanej cyfry 14431 dymów dojdzie w ten sposób jeszcze '
            '247 dymów, co uczyni razem 14678 dymów. Po odliczeniu '
            '2216 dymów przypadających na osady olęderskie, '
            'otrzymamy ostatecznie 12.462 dymy.'),
    ],
    '0016': [
        (1, 'Wsie holenderskie.'),
        (2, 'Problem kolonizacji flamandzko-holenderskiej.'),
        (3, 'Geschichte des Deutschtums im Lande Posen.'),
        (4, 'Patrz wykaz skrótów.'),
        (5, 'Tamże.'),
        (6, 'Por. Wojciechowska M., Sprawozdanie z prac nad mapą woj. '
            'poznańskiego w dobie Sejmu czteroletniego. Poznań 1934. '
            'Odbitka ze Sprawozdań Poznańskiego Tow. Przyjaciół Nauk '
            'nr 3 za r. 1933. Tamże scharakteryzowane zostały bliżej '
            'niektóre zużytkowane tutaj materiały źródłowe.'),
    ],
    '0017': [
        (1, 'Cytowanie tych akt nasuwa pewne trudności. Zostały one '
            'przekazane przez poszcze- gólne sądy do depozytu '
            'archiwalnego tylko częściowo, stąd nie mogła być narazie '
            'przepro- wadzona numeracja poszczególnych tomów. Cytowane '
            'więc są według numeracji sądowej, a w razie szeregu tych '
            'samych sygli lub w ogóle braku Jakichkolwiek, dla '
            'odróżnienia podana jest przy każdym tomie ilość stron '
            'wzgl. kart.'),
        (2, 'Tabela sporządzona niezależnie od tabeli z tego samego '
            'roku, wymienionej poprzednio.'),
        (3, 'Korzon T., Wewnętrzne dzieje Polski, t. I, s. 68.'),
    ],
    '0045': [
        (1, 'Z 16 IV 1597 (Inscr. Valc. nr 85, r. 1663—4, fol. 402).'),
        (2, 'Z 21 II 1601 (Rel. Posn. nr 140, r. 1601—2, fol. 659).'),
        (3, 'Ujskie Ol.: Jan Borth, Marcin Schueneke, Michał Boleman, '
            'Krystian Paul, Joachim Bartz, Joachim Schmiket, Jan '
            'Werner, Andrzej Dumken, Jan Elwig. Nowe Dwory Ol.: '
            'Barthlomicy Unswaldt, Hanus Renik, Andreas Brozy, Krystow '
            'Olemborg, Peter Barkaw, Peter Wanczlaw, Henrik Carstan, '
            'Jakub Hanik, Michael Hoffman, Philyp Bem (wzgl. Bein). '
            'Transkrypcja polska.'),
        (4, 'Inwentarz z r. 1630 (Rel. Posn. nr 157, r. 1632, fol. '
            '169—178) oraz z r. 1653 (Rel. Posn. nr 179, r. 1654, fol. '
            '718—779).'),
        (5, 'Inwentarz z r. 1653 odróżnia wsie polskie, niemieckie '
            '(wzgl. mieszane), oraz „olęderskie”.'),
    ],
    '0081': [
        (1, 'Maas, Entwaldung, s. 23—5.'),
        (2, 'Zmiany krajobrazu, s. 19—20.'),
        (3, 'Np. w przywileju dla Milczewskich Ol. (AW. A. 1).'),
        (4, 'Takie postanowienie spotykamy w przywilejach z r. 1677 '
            'dla olędrów majętności wieleńskiej.'),
    ],
    '0104': [
        (1, 'Zwolnieni od ceł byli olędrzy majętn. wieleńskiej. Por. '
            'przywileje z r. 1677.'),
        (2, 'AW. Milczewskie Ol., A. 1 i Kl. XII 6 V, fol. 116, '
            'Lubaskie Ol.'),
        (3, 'zur Anerkennung des Ober Eigenthums jedes mal nach '
            'Verlauf von finfzig Jahren, zwei Dukaten zu achtzehn '
            'polskie Gulden” (AGH sąd Wolsztyn, majętn. Obra, vol. '
            'IV, fol. 1137, reces z r. 1843).'),
        (4, 'Entstehung, s. 84. Autor tłumacząc tekst pracy Stan. '
            'Kutrzeby, Historia ustroju Polski w zarysie, gdzie w t.I, '
            'nas. 236 (wydanie z r. 1931) znajduje się zwrot dotyczący '
            'olędrów, nie spostrzegł, że dalsze rozważania Kutrzeby '
            'dotyczą już ogółu ludności włościańskiej. Wypadło stąd, '
            'że olędrzy nie tylko uiszczają wspomnianą wyżej opłatę, '
            'ale nadto na żądanie pańskie muszą stawać do służby we '
            'dworze.'),
        (5, 'Rel. Posn. nr 038, r. 1791, fol. 602.'),
    ],
}
# NOTE_FIXES: text overrides without renumbering (the dup-tail trims:
# the OCR duplicated the next note's text into this def's tail)
NOTE_FIXES = {
    '0085': {
        7: 'Według przywileju dla Ol. Żamorze główna droga wiejska '
           'winna mieć 2 pręty, a drogi boczne 1 pręt szerokości. '
           'Sołtys winien dbać o to, aby nikt dróg nie podorywał '
           '(Rel. Posn. nr 641, r. 1792, fol. 164).',
        9: 'Góździn, AW. A. 1: „Pozwala im się też... miedze wolne '
           'przy każdej hubie całej potrzebne”. Karpicko, AW. A. 1: '
           '„Miedze, drogi, wygoniska nie wchodzą w rozmierzenie '
           'hubów”.',
    },
    '0101': {
        8: 'Rel. Cost. nr 164, r. 1729, Podgradowice: „corocznie '
           'powinni dawać do dworu od każdej huby po 60 tynfów, '
           'rachując i od owiec”. Item Rel. Cost. nr 190, r. 1755, '
           'fol. 33, Krzemieniewo.',
        9: 'AW. Zielonka, A. 1 (r. 1704). Opłata wynosiła 2 talary.',
    },
    '0107': {
        3: 'Rel. Cost. nr 220, r. 1787, fol. 182, Charłub Ol.',
        4: 'Z. huby płacono: w Ostrowie i Borgowie (r. 1785) — '
           '126 zł, w Skrzydlewie (r. 1785) — 16',
    },
    '0066': {
        6: 'W Ol. Charłub, Komorowskich, Włościejewskich '
           '(sygn. w aneksie I).',
    },
}

# p. 85 (= scan 0100) / p. 86 (= scan 0101) body fixes: the whole
# marker map was decodable (the czynsz paragraph spans the leaf break)
BODY_FIXES['0100'] = [
    # marker 1 at its visible digit ('polskie1.'); note 1 = the
    # numismatics literature (Gumowski/Rutkowski) - the conversion basis
    ('złote polskie1. Często', 'złote polskie[^85-1]. Często'),
    ('alternatywnie[^85-1] w dwóch', 'alternatywnie w dwóch'),
]
BODY_FIXES['0101'] = [
    # marker 2 = the '?' remnant after '30-morgowej' (note 2 = the
    # Ujskie privilege source)
    ('wyrosił[^85-2] zł z huby 30-morgowej ?,',
     'wyrosił zł z huby 30-morgowej[^85-2],'),
    # marker 3 = the '%' remnant after '60-morgowej' (note 3 = the
    # Nowe Dwory + Róża/pomiar sources)
    ('jak[^85-3] wynika z późniejszych pomiarów, 60-morgowej %.',
     'jak wynika z późniejszych pomiarów, 60-morgowej[^85-3].'),
    # Róża's czynsz = 36 (forced by note 4's '36-zlotowy czynsz mamy
    # w...' phrasing); marker 4 = the '5' digit after 'w. XVII'
    # (small-type 4-as-5 tie)
    ('był nieco wyższyi wynosił[^85-4] zł z huby[^85-5],',
     'był nieco wyższy i wynosił 36 zł z huby,'),
    ('przez cały w. XVII 5.', 'przez cały w. XVII[^85-4].'),
    # marker 5 = note 5 (the Dłuskie source + Schmidt's misreading)
    ('w Dłuskich Starych Ol. (r. 1688) czynsz',
     'w Dłuskich Starych Ol. (r. 1688)[^85-5] czynsz'),
    # marker 6 = '$' after 'obniżką czynszu' (note 6 = Jasionowe/
    # Glinki 1701 - the first tynf-era settlements)
    ('obniżką czynszu $. W pierwszej', 'obniżką czynszu[^85-6]. W pierwszej'),
    # marker 7 = '?' after 'dobrej monecie' (note 7 = J.w. + 1709/1713)
    ('„dobrej monecie” ?, tzn.', '„dobrej monecie”[^85-7], tzn.'),
    # marker 8 = '*' after '8—12 talarów' (note 8 = the talar-list)
    ('względnie 8—12 talarów *—', 'względnie 8—12 talarów[^85-8]—'),
    # the stróżowe garble (the '*' sat inside 'każdej')
    ('od każ. * dej huby płacono I zł[^86-10]',
     'od każdej huby płacono 1 zł[^86-10]'),
    # p. 30: the old miswire inside the Folsztyn quote
    ('wier gegeben[^30-4] Rechstaler', 'wier gegeben Rechstaler'),
    # p. 70: the old miswire on the drogi sentence
    ('biegnących[^70-6] przez grunty osady[^70-8].',
     'biegnących[^70-6] przez grunty osady.'),
    # remnants sitting directly at their wired refs: the glyph was the
    # superscript the ref now represents
    ('zagrabieniem pola *.[^82-5]', 'zagrabieniem pola[^82-5].'),
    ('przeciętnej *.[^100-5]', 'przeciętnej[^100-5].'),
    ('charakteru $.[^112-4]', 'charakteru[^112-4].'),
    # ---- SPOT round 5: the no-move re-slotting re-exposed these
    # old-miswire copies at their new leaf positions
    ('w zdewaluowanych[^85-6][^85-7][^85-8', 'w zdewaluowanych'),
    ('ciężary poja-[^48-9]', 'ciężary poja-'),
    # ---- SPOT ANSWERS round 2 (S36): the marker numbers, editor-read ----
    ('Zajączkowo Wielkie i Małe *, dalej',
     'Zajączkowo Wielkie i Małe[^5-4], dalej'),
    ('Szóstaki par. Sieraków %;', 'Szóstaki par. Sieraków[^18-3];'),
    ('czyńskie %, Ol. Włościejewskie', 'czyńskie, Ol. Włościejewskie'),
    ('była protestancka *.', 'była protestancka[^36-4].'),
    ('np. tymczasowa umowa wstępna *,',
     'np. tymczasowa umowa wstępna[^40-3],'),
    ('32 w języku niemieckim %, a', '32 w języku niemieckim[^40-6], a'),
    ('przez grunt olęderski *.', 'przez grunt olęderski[^48-9].'),
    ('wybierana była dożywotnio %,', 'wybierana była dożywotnio,'),
    ('nazwiska wszystkich osadników $.',
     'nazwiska wszystkich osadników[^51-6].'),
    ('olędrom Starego i Nowego Ujścia %.',
     'olędrom Starego i Nowego Ujścia[^51-3].'),
    ('od której klucz mieli ławnicy $,',
     'od której klucz mieli ławnicy[^54-6],'),
    ('pan zastrzegał sobie tylko część dochodów *,',
     'pan zastrzegał sobie tylko część dochodów[^54-9],'),
    ('prawo łowiectwa było nieograniczone *.',
     'prawo łowiectwa było nieograniczone[^74-9].'),
    ('uciążliwym obowiązkiem *.', 'uciążliwym obowiązkiem.'),
    ('wyjaśnił już kilka lat przed tym %.',
     'wyjaśnił już kilka lat przed tym[^99-3].'),
    ('chociaż bywało: i odwrotnie %.', 'chociaż bywało: i odwrotnie[^100-6].'),
    ('aż wszystko zostanie sprzątnięte %.',
     'aż wszystko zostanie sprzątnięte[^101-2].'),
    ('zdarzały się rzadko %.', 'zdarzały się rzadko[^102-3].'),
    ('omówiona została już poprzednio *.',
     'omówiona została już poprzednio[^112-2].'),
    ('się z jednej osady do innej *.',
     'się z jednej osady do innej[^112-4].'),
    ('bezpłatnie jeden z budynków %.',
     'bezpłatnie jeden z budynków[^114-3].'),
    ('swobodę wyznania[^117-1] i praktyk religijnych %.',
     'swobodę wyznania[^117-1] i praktyk religijnych.'),
    # ---- the old compositor miswires of the same markers (the editor
    # ruled the true positions above; these copies must go) ----
    ('procesem ciągłego[^100-6] zwiększania',
     'procesem ciągłego zwiększania'),
    ('jakkol-[^101-2] wiek', 'jakkolwiek'),
    ('„Die Wirthe,[^102-3][^102-4]', '„Die Wirthe,[^102-4]'),
    ('wśród olędrów nałogowo[^112-2].', 'wśród olędrów nałogowo.'),
    ('i charakteru[^112-4].', 'i charakteru.'),
    ('Poza[^114-3] dochodami', 'Poza dochodami'),
    ('w par. Brody[^18-3];', 'w par. Brody;'),
    ('czy do[^36-4] opuszczenia', 'czy do opuszczenia'),
    (' przywilej innej gminy[^40-3].', ' przywilej innej gminy.'),
    ('a 2[^40-6] w języku', 'a 2 w języku'),
    ('wyrasta[^5-4] też cały', 'wyrasta też cały'),
    ('powinności dworskie[^51-3].', 'powinności dworskie.'),
    ('Przed[^54-6] upływem', 'Przed upływem'),
    ('lub też[^54-9] przeznaczał', 'lub też przeznaczał'),
    ('Dochód[^74-9] olędrów', 'Dochód olędrów'),
    ('wyników[^99-3] pracy Fr. Guradze', 'wyników pracy Fr. Guradze'),
]

# BODY_FIXES2: amount restorations that depend on the wirings above
# having run first (the search strings exist only after them)
BODY_FIXES2 = [
    ('pan pobierał tynfów (14 zł)', 'pan pobierał 11 tynfów (14 zł)'),
    ('uiszczali ją olędrzy co lat w wysokości zł z huby',
     'uiszczali ją olędrzy co 50 lat w wysokości 36 zł z huby'),
    ('w dobrach państwowych gr,', 'w dobrach państwowych 19 gr,'),
    ('wier gegeben Rechstaler', 'wier gegeben 18 Rechstaler'),
    ('wyrosił zł z huby 30-morgowej', 'wyrosił 20 zł z huby 30-morgowej'),
    ('immuhnitetam1', 'immunitetami'),
]

# ---- SPOT round 5b: the single-letter debris merges (see the applied
# block in main() for the per-stray pixel evidence)
STRAY_FIXES = [
    # p. 38: 'z' opens the print line 'z calkowitego majatku swego...'
    ('Gdy tedy żalący się\ncałkowitego majątku swego ogołoconym został, '
     'nadto i wielc przykrości doznawał, przeto\nz\ndo Xiąg',
     'Gdy tedy żalący się\nz całkowitego majątku swego ogołoconym został, '
     'nadto i wielc przykrości doznawał, przeto\ndo Xiąg'),
    # p. 49: 'w' begins the print line 'w traktuje te sprawe...'
    ("Nieco inaczej '\nw\ntrąktuje tę sprawę",
     "Nieco inaczej '\nw trąktuje tę sprawę"),
    # p. 49: 'z' = 'kto z nich'
    ('gdyby zaś kto nich miał umrzeć.\nz\nbezpotomnie',
     'gdyby zaś kto z nich miał umrzeć.\nbezpotomnie'),
    # p. 49: 'z' = 'ktorykolwiek z naszych Holendrow'
    ('którykolwiek naszych Holendrów\nz\nczapurskich',
     'którykolwiek z naszych Holendrów\nczapurskich'),
    # p. 49: 'w' = 'ze w osadach wczesniej-'
    ('że osądach wcześniej-\nw\nszych po bezpotomnej',
     'że w osądach wcześniej-\nszych po bezpotomnej'),
    # p. 99: 'r.' = 'krotko przed r. 1800'
    ('krótko przed 1800 (AM. Wieleń, G. 250 fol. 20) powinności olędrów '
     'składają się tylko\nr.\nz czynszów',
     'krótko przed r. 1800 (AM. Wieleń, G. 250 fol. 20) powinności olędrów '
     'składają się tylko\nz czynszów'),
    # p. 99: 'gr w' = the missing 'gr w' after the first fraction
    # (print: 3030 zl 20 1/2 gr w Nowych Dworach i 2349 zl 28 1/2 gr
    # w Folsztynie)
    ("3030 zł 20'/, Nowych Dworach i 2349 zł 28'/, gr w Folsztynie) "
     'i z robocizn,\ngr w\nktóre odprawiali',
     "3030 zł 20'/, gr w Nowych Dworach i 2349 zł 28'/, gr w Folsztynie) "
     'i z robocizn,\nktóre odprawiali'),
    # p. 103: 'uns' begins the print line 'uns auf Erbpacht uberlassen'
    ('erhalten kónnen, Wiesen\nuns\nauf Erbpacht iiberlassen',
     'erhalten kónnen, Wiesen\nuns auf Erbpacht iiberlassen'),
    # p. 116: 'w' begins the print line 'w aktach regulacyjnych...'
    ('Metryki 441 C). Nawet\naktach regulacyjnych',
     'Metryki 441 C). Nawet\nw aktach regulacyjnych'),
    # p. 116: 'z' = 'czesc z nich'
    ('osadnicy, mimo że\nw\nczęść nich korzystała z nauki szkolnej już za '
     'czasów pruskich, w większości wypadków nie\nz\numieli się podpisać.',
     'osadnicy, mimo że\nczęść z nich korzystała z nauki szkolnej już za '
     'czasów pruskich, w większości wypadków nie\numieli się podpisać.'),
    # ---- p. 25: the phantom markers were the print's INLINE table
    # number 'Tp. 90' (raw h63 = body height, vs a true superscript's
    # h30); the only real marker is the raised '1' after '12.462'
    # (bbox h38, top-aligned) -> and the note block is ONE note: the
    # totals list plus its prose continuation (no '2' number glyph at
    # the continuation's line start - ink-checked x540-960)
    ('względnie[^25-1] (oznaczone gwiazdką)',
     'względnie 90 (oznaczone gwiazdką)'),
    ('względne[^25-2] brak', 'względne 90 brak'),
    ('wynosi tutaj 12.462 1. Przy', 'wynosi tutaj 12.462[^25-1]. Przy'),
    # the tiny two-mark glyph after '93.518 osob.' - not an 'm' word
    # (ink = two sparse marks w9/w16, no letter body); debris
    ('uczyni 93.518 osób. m W ziemi', 'uczyni 93.518 osób. W ziemi'),
    # ---- p. 23: 'i' misOCR'd as '1' (raw token 'i'@x1690; the body's
    # parallel list reads 'Jaromierskich Nowych i Starych Ol.'), and
    # the note-4 total: both OCR passes + the glyph render give
    # '24.667' (the '6' = wide-top-curl + closed bowl, not a '0');
    # 24.667 - 8.520 - 225 - 82 = 15.840 vs the body's 15.831 (print-
    # internal Delta 9, flagged in the SPOT sheet)
    ('Jaromierskich Nowych 1 Starych', 'Jaromierskich Nowych i Starych'),
    ('summa summarum 24.067 dymów', 'summa summarum 24.667 dymów'),
    ('poznański, gdzic była', 'poznański, gdzie była'),
    # ---- S53 verification find: the note 38-3 narrative's line order
    # was scrambled ('patrywana' stranded after 'twier-'); the raw
    # x-order reconstructs: 'gdzie byla roz- / patrywana w trzech
    # terminach (...) Pozwani twier- / dzili, ze cala kwote ...'
    ('gdzie była roz-\nw trzech terminach (Decr. Posn. nr 137, fol. 303, '
     '485 i 597—600). Pozwani twier-\npatrywana\ndzili',
     'gdzie była roz-\npatrywana w trzech terminach (Decr. Posn. nr 137, '
     'fol. 303, 485 i 597—600). Pozwani twier-\ndzili'),
]

# ---- the body tables rebuilt from the editor's corrected grids
# (tabele_body.xlsx, SPOT round 4): span replacements on the final
# line list - lines from the start-anchor through the end-anchor are
# replaced by the rebuilt table + note defs. Table-note refs wired
# per the editor's print copy.
TABLE_SPANS = [
    ('TABELA I', 'pz', [
        'TABELA I',
        '',
        'Ludność wiejska; w tym ludność olęderska:',
        '',
        '| Powiat | Ludność wiejska ogółem | '
        'w tym ludność olęderska, w cyfrach absolutn. | procentowo |',
        '| --- | --- | --- | --- |',
        '| kościański | 105.000 | 14.987 | 14,3 |',
        '| poznański | 93.500 | 13.637 | 14,6 |',
        '| z wschowski | 10.900 | — | — |',
        '| **Województwo poznańskie** (w granicach po I rozbiorze) '
        '| **209.400** | **28.624** | **13,7** |',
        '',
    ]),
    ('TABELA II', '4 Nauczycieli wiejskich,', [
        'TABELA II',
        '',
        'Skład zawodowy ludności 94 osad pow. kościańskiego wg Tol.',
        '',
        '| Zawody | osoby trudniące się podanym zawodem, jako zaw. '
        'głównym | ubocznie | % zatrudnionych (jako zaw. głównym) | '
        '% w obrębie grupy |',
        '| --- | --- | --- | --- | --- |',
        '| I. Rolnictwo | 12.643 | 162 | 97,5 | 100,0 |',
        '| a. gospodarze ol. | 8.805 | — | | 69,6 |',
        '| b. komornicy | 1.542 | 122 | | 12,2 |',
        '| c. czeladź | 1.513 | — | | 12,0 |',
        '| d. luźni za robotą | 491 | — | | 3,9 |',
        '| e. żebracy | 292 | — | | 2,3 |',
        '| 2. Karczmarze[^61-1] | 155 | 156 (?) | 1,2 | |',
        '| 3. Młynarze[^61-2] | 14 | 42 | 0,1 | |',
        '| 4. Rzemiosło | 142 | — | 1,1 | |',
        '| 5. Hutnictwo[^61-3] | 7 | — | 0,1 | |',
        '| 6. Szkolni[^61-4] | 6 | 140 (?) | 0,0 | |',
        '| **Razem** | **12.967** | **500** | **100,0** | |',
        '',
        'łecznym decydował przede wszystkim stopień gospodarczej '
        'samodzielności danej jednostki. Z tego punktu widzenia '
        'możemy w obrębie każdego stanu przeprowadzić przekrój '
        'społeczny w ten sposób, że do war—',
        '',
        '[^61-1]: Że karczmarzy było więcej, niż wykazuje ich Tol., '
        'można wywnioskować z ilości dymów podanych dla karczem w '
        'Tol. 89. Nie ulega wątpliwości, że dla wszystkich '
        'karczmarzy podstawą utrzymania były gospodarstwa rolne '
        '(częstokroć zwolnione od czynszów). Część karczmarzy w '
        'Tol. podana została zapewne w rubryce „gospodarze”. '
        'Oszacowaliśmy ich, mnożąc nadwyżkę dymów karczmarskich w '
        'Tol. 89 przez współczynnik 5, wyrażający liczbę osób '
        'przypadających na rodzinę karczmarską według tab. III.',
        '[^61-2]: Ogółem w osadach znajdował się 1 młyn wodny i 8 '
        'wietrznych (wiatraków). Młyn wodny znajdujący się w '
        'Sroczewskich Ol. istniał już przed lokacją olędrów. W Tol. '
        'podane są tylko rodziny 2 młynarzy. Rodziny pozostałych '
        'właścicieli młynów w liczbie 7, podanych w Tol. 89, '
        'oszacowaliśmy licząc 6 osób na dym młynarski na 42 osoby. '
        'Niewątpliwie ich głównym zawodem było rolnictwo.',
        '[^61-3]: Osoby zaliczone do tej grupy stanowią obsługę '
        'hamru znajdującego się w Ol. Borujskich. Hamer ten istniał '
        'już przed lokacją olędrów; nie był on objęty przywilejem '
        'lokacyjnym. Przypuszczać jednak można, że jego pracownicy '
        'składali się z mieszkańców osady. Źródłowych wiadomości '
        'tutaj brak.',
        '[^61-4]: Nauczycieli wiejskich, jak można wnioskować z '
        'różnych przygodnych wzmianek, musiało być więcej niż 1 '
        'rodzina wykazana w Tol. Mieszczą się oni zapewne w '
        'rubrykach: „gospodarze”, „komornicy”, i „rzemieślnicy”. '
        'Podana w przedziałce „zajęci ubocznie w danym zawodzie” '
        'cyfra osób należących do rodzin nauczycieli obliczona '
        'została szacunkowo na podstawie wyników tabeli III. Na 94 '
        'osady powiatu kościańskiego wypadło proporcjonalnie 36 '
        'nauczycieli (łącznie z lektorami — por. tab. III), z czego '
        '1 został już uwzględniony, reszta zaś, licząc 4 osoby na '
        'nauczyciela wzgl. lektora z rodziną, uczyniła w sumie 140 '
        'dusz.',
    ]),
    ('TABELA III', '3 ] nauczyciel,', [
        'TABELA III',
        '',
        'Skład zawodowy ludności 36 osad olęderskich powiatu '
        'poznańskiego (zawodowo czynni i bierni)',
        '',
        '| Kategorie zawodów | 28 wsi klasyfikowanych w r. 1773: '
        'rodzin | osób (zawód główny) | osób (zawód uboczny) | '
        '8 wsi maj. sierakowskiej: rodzin | osób (zawód główny) | '
        'osób (zawód uboczny) | Razem: rodzin | osób (zawód główny) '
        '| osób (zawód uboczny) |',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- | '
        '--- |',
        '| I. Rolnictwo | 653 | 3262 | 60[^62-2] | 100 | 601 | '
        '13[^62-2] | 753 | 3863 | 73 |',
        '| a. gospodarze ol. | 418 | 2434 | — | 85 | 454 | — | 503 '
        '| 2888 | — |',
        '| b. chałupnicy[^62-1] | 37 | 125 | — | — | — | — | 37 | '
        '125 | — |',
        '| c. komornicy | 198 | 429 | — | 15 | 40 | — | 213 | 469 '
        '| — |',
        '| d. czeladź | — | 274 | — | — | 107 | — | — | 381 | — |',
        '| 2. Hodowla (pasterze) | 31 | 92 | — | 11 | 39 | — | 32 '
        '| 131 | — |',
        '| 3. Karczmarze | 10 | 54 | — | 4 | 13 | — | 14 | 67 | '
        '— |',
        '| 4. Młynarze | 1 | 6 | — | — | — | — | 1 | 6 | — |',
        '| 5. Rzemiosło | 23 | 86 | — | 2 | 9 | — | 25 | 95 | — |',
        '| a. kowale | 15 | 52 | — | — | — | — | 15 | 52 | — |',
        '| b. kołodzieje | 1 | 5 | — | — | — | — | 1 | 5 | — |',
        '| c. sukiennicy | 1 | 6 | — | — | — | — | 1 | 6 | — |',
        '| d. półciennicy | 1 | 1 | — | — | — | — | 1 | 1 | — |',
        '| e. krawcy | 4 | 19 | — | 1 | 4 | — | 5 | 23 | — |',
        '| f. szewcy | 1 | 3 | — | 1 | 5 | — | 2 | 8 | — |',
        '| 6. Przem. leśny (smolarze) | 1 | 4 | — | — | — | — | 1 '
        '| 4 | — |',
        '| 7. Ośw. i kult. rel. (nauczyciele, lektorzy) | 8 | 28 | '
        '1 | 5[^62-3] | 10 | — | 13 | 38 | 1 |',
        '| **Razem** | **717** | **3532** | **61** | **122** | '
        '**672** | **13** | **839** | **4204** | **74** |',
        '',
        'stwy przodującej zaliczymy Jednostki gospodarczo '
        'samodzielne, niższą społecznie kategorię będą tworzyły te '
        'jednostki, które mając niedosta-',
        '',
        '[^62-1]: Źródło miesza chałupników z komornikami. Ściśle '
        'warstw tych rozgraniczyć na podstawie danych akt '
        'klasyfikacyjnych nie można; w tabeli za podstawę '
        'rozgraniczenia przyjęto terminologię źródłową.',
        '[^62-2]: Karczmarze i młynarze.',
        '[^62-3]: 1 nauczyciel, 4 lektorów (Vorleser).',
    ]),
    ('TABELA IV', 'l Por. Rusiński', [
        'TABELA IV',
        '',
        'Społeczne uwarstwienie ludności osad olęderskich',
        '',
        '| Kompleksy terytorialne | Liczba osad | gospod. samodz. '
        '(osób) | pośrednich (osób) | niesamodz. (osób) | razem |',
        '| --- | --- | --- | --- | --- | --- |',
        '| **Cyfry absolutne** | | | | | |',
        '| Pow. kościański | 94 | 8.974 | 149 | 3.844 | 12.967 |',
        '| z powiatu poznańskiego: | | | | | |',
        '| a. osady klasyfikowane w r. 1773 | 28 | 2.494 | 90 | 948 '
        '| 3.532 |',
        '| b. maj. sierakowska (r. 1759) | 8 | 467 | 9 | 196 | 672 '
        '|',
        '| **Ogółem** | **130** | **11.935** | **248** | **4.988** '
        '| **17.171** |',
        '| **Cyfry procentowe** | | | | | |',
        '| Pow. kościański | — | 69,2 | 1,1 | 29,7 | 100,00 |',
        '| a. osady klasyfikowane w r. 1773 | — | 70,7 | 2,5 | 26,8 '
        '| 100,00 |',
        '| b. maj. sierakowska (r. 1759) | — | 69,5 | 1,3 | 29,2 | '
        '100,00 |',
        '| **Ogółem** | — | **69,5** | **1,4** | **29,1** | '
        '**100,00** |',
        '',
        'Z. braku cyfr porównawczych dla innych osad Wielkopolski '
        'ograniczymy się do zestawienia otrzymanych tutaj wyników z '
        'cyframi dotyczącymi uwarstwienia społecznego ludności '
        'królewszczyzn pruskich[^64-1]. Struktura społeczno-zawodowa '
        'tej ludności była pod wieloma względami analogiczna do '
        'struktury ludności olęderskich osad powiatu kościańskiego '
        'i poznańskiego.',
        '',
        '[^64-1]: Por. Rusiński Władysław, Uwarstwienie ludności '
        'wiejskiej w królewszczyznach Prus Królewskich w drugiej '
        'połowie XVII w. Roczniki dziejów społecznych i '
        'gospodarczych, t. VI, r. 1937, s. 111.',
    ]),
    ('TABELA V', '|', [
        'TABELA V',
        '',
        'Charakter gruntów, na których powstały osady olęderskie',
        '',
        '| Powiaty | Ogólna liczba osad zapisanych w źródłach | '
        'osad powstałych na rolach gotowych (uprawnych) | osad '
        'powstałych na rolach częścią zarosłych | osad powstałych '
        'na rolach zarosłych (wytrzebionych przez olędrów) |',
        '| --- | --- | --- | --- | --- |',
        '| **w cyfrach absolutnych** | | | | |',
        '| kościański | 44 | 20 | 3 | 21 |',
        '| poznański | 78 | 17 | 3 | 58 |',
        '| **Razem** | **122** | **37** | **6** | **79** |',
        '| **procentowo** | | | | |',
        '| kościański | — | 45,5 | 6,8 | 47,7 |',
        '| poznański | — | 21,8 | 3,8 | 74,4 |',
        '| **Razem** | — | **30,3** | **4,9** | **64,8** |',
        '',
    ]),
]


def main():
    spath = os.path.join(OCR, 'structure4.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure2.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure.json')
    struct = json.load(open(spath, encoding='utf-8'))
    sys.path.insert(0, HERE)
    from paragraphs2 import assemble_marked
    import readability
    # the pct/fraction token map (pct_frac.py's 5x-verified decisions):
    # applied to body AND note texts (the earlier fix pass reached only
    # the body lines; the note layer carried the same artifacts)
    tokmap = {}
    pf = os.path.join(OCR, 'pct_frac.json')
    if os.path.isfile(pf):
        for k, v in json.load(open(pf, encoding='utf-8')).items():
            if v.get('resolved') and v.get('print') not in (None, 'MARKER') \
                    and v['print'] != v['tok']:
                key = v['tok'].strip('.,;:!?»”"()')
                tokmap[key] = v['print']
    # MANUAL supplement: percent tokens the queue missed or misclassed,
    # each verified by the read-through's cross-references (p. 13's 75%
    # confirmed by p. 31's "do 25%", p. 14's one-third confirmed by the
    # 832/550 arithmetic, the p. 34 range by the chapter's subject)
    tokmap.update({
        '5%/': '5%', '10%/': '10%', '36%/': '36%', '20%/': '20%',
        '13.6%%': '13.6%', '750/y': '75%', '!/': '⅓',
        '35—38?/': '35—38%',
    })

    def fix_toks(text):
        out = []
        for tok in text.split(' '):
            core = tok.strip('.,;:!?»”"()')
            if core in tokmap:
                out.append(tok.replace(core, tokmap[core]))
            else:
                out.append(tok)
        return ' '.join(out)
    parts = []

    # ---- front matter -------------------------------------------------
    fm = os.path.join(HERE, 'front_matter.md')
    if os.path.isfile(fm):
        parts.append(open(fm, encoding='utf-8').read().strip())
    # ---- body ---------------------------------------------------------
    # paragraphs collected per page first: the readability pass + the
    # cross-page hyphen join (a word hyphenated over the leaf: p. 32
    # 'Element nie-' -> p. 33 'miecki...') run before assembly
    page_paras = {}
    for n in BODY + ANEX2 + ANEX3:
        page_paras[n] = [fix_toks(readability.apply(p))
                         for p in assemble_marked(n)]
        for note in struct[n]['notes']:
            note['text'] = fix_toks(readability.apply(note['text']))
        # SPOT ANSWERS round 2: the footnote-marker audit - full note
        # rebuilds (fused splits + renumberings), text overrides
        # (dup-tail trims) and body-ref rewires to the print's true
        # superscript positions
        nr = NOTE_REBUILD.get(n)
        if nr:
            struct[n]['notes'] = [{'num': k, 'text': v}
                                  for k, v in nr]
        nf = NOTE_FIXES.get(n)
        if nf:
            have = {note['num'] for note in struct[n]['notes']}
            for note in struct[n]['notes']:
                if note['num'] in nf:
                    note['text'] = nf[note['num']]
            for k, v in nf.items():          # notes the OCR dropped
                if k not in have:
                    struct[n]['notes'].append({'num': k, 'text': v})
                    struct[n]['notes'].sort(key=lambda x: x['num'])
    order = BODY + ANEX2 + ANEX3
    LABEL_RE = re.compile(r'\[\^[^\]]+\]')
    TERM = ('.', '!', '?', '…', '”', '»', ':', ';')
    # SPOT round 5 (the footnote-page pass): the cross-page joins are
    # DISABLED. The old logic moved whole paragraphs across leaves
    # (mid-sentence breaks and hyphenated words alike); in flowing
    # sections the moves CHAINED and migrated discussions pages
    # forward (print p. 27's confession text reached our p. 29 block;
    # p. 85's czynsz paragraph leaked into p. 86). Rule 1 (a page's
    # markers reference that page's notes) requires each marker to sit
    # on its true page, so the paragraphs stay where the print breaks
    # them: assemble_marked already builds each page's block from that
    # page's own lines - the per-page halves ARE the leaf-split parts,
    # faithful to the print (cf. the approved p. 85/86 split).
    for n in BODY:
        parts.append(f'[p. {label(n)}]\n')
        parts.append('\n\n'.join(page_paras[n]))
        notes = []
        for note in struct[n]['notes']:
            notes.append(f"[^{label(n)}-{note['num']}]: {note['text']}")
        if notes:
            parts.append('\n'.join(notes))
    # ---- ANEKS I tables (printed pp. 123-144) ---------------------------
    # real Markdown tables (the editor's ruling): per-column cells from
    # annex_md.json (pixel-classified dash/empty cells + cleaned OCR
    # text); furniture rows (the series-c title, the b-series totals
    # line) as plain lines outside the tables
    amd_path = os.path.join(OCR, 'annex_md.json')
    amd = json.load(open(amd_path, encoding='utf-8')) \
        if os.path.isfile(amd_path) else None
    # the series-c OCR noise cells (0158 row 9's Nazwa/Parafia are the
    # one bad multi-line cell pair) - the strip's row text is
    # print-verified for this row; substituted at compose time
    NOISE_FIX = {
        ('0158', 9): ['Trojanowskie Olędry ⁹', 'Mur. Goślina',
                      'razem z Głębockiem a na miejscu Trzcianki',
                      'las', '—', 'AW. B. 1037', '5 VIII 1788',
                      '—', '—', '—'],
    }
    if amd:
        for n in amd:
            for r in amd[n]['rows']:
                fix = NOISE_FIX.get((n, r['num']))
                if fix:
                    r['cells'] = [r['cells'][0]] + fix
    # the annex tables' footnote apparatus (annex_notes.py: the print's
    # superscript refs in the Nazwa cells and the note blocks below the
    # sheets' tables; blocks numbered from 1, a ref resolves to the
    # nearest block below its own sheet)
    import annex_notes
    import annex_fixes
    if amd:
        nf = annex_fixes.apply(amd)
        print('annex_fixes applied:', nf)
    # the c-series totals rows: real table rows in the print (the
    # values pixel-verified; the leading '4.' of the Ludn figures sits
    # tight to the column rule and was lost in the first reads)
    C_TOTALS = {
        'u0': ['Razem z poprzedn.', '—', '—', '—', '—', '—', '—', '—',
               '2.178', '38', '4.514'],
        'u2': ['Ogółem', '—', '—', '—', '—', '—', '—', '—',
               '2.216', '38', '4.514'],
    }
    parts.append('[p. 123]\n\nANEKS I\n')
    # the print's page-top furniture (the rotated top-bands): the
    # tables carry titles on their first pages; exact wording of the
    # title lines SPOT-pending (S45/S46/S47 crops). The p. 129 band
    # also carries the asterisk note (the '*' explanation for the
    # dymy column) - it prints ABOVE the table on the page.
    PRELUDES = {
        '0139': ['TABELA VI',
                 'Osady olęderskie w byłym powiecie kościańskim '
                 'w okresie rozbiorów'],
        '0144': ['* Dymy niektórych osad podane są w Tp. 89 zbiorowo '
                 'dla całej osady; wysokość ich na poszczególne '
                 'zagrody przeliczona została według Tp. 90.'],
        '0147': ['TABELA VII',
                 'Osady olęderskie w byłym powiecie poznańskim '
                 'w okresie rozbiorów'],
        '0158': ['Osady olęderskie w ziemi wschowskiej w okresie '
                 'rozbiorów'],
    }
    HEAD = ('Lp. | Nazwa osady w okresie rozbiorów | Ówczesna parafia | '
            'Nazwa dzisiejsza | Rok założ. osady | Charakter terenu '
            'przed założ. osady | Przywilej lub wzmianka — sygn. źródła | '
            'data | L. dymów wg Tp. 89 lub 90 * | dymów oblicz. '
            'szacunkowo | Ludn. osad wg Tołł.')
    SEP = ' | '.join(['---'] * 11)
    for n in [f'{i:04d}' for i in range(139, 160)]:
        parts.append(f'\n<!-- annex sheet {n} -->\n')
        if amd and n in amd:
            sh = amd[n]
            # the print's order: rows and furniture interleaved by
            # y (0159: rows 10-11, the totals line, the sub-table
            # title, then sub-rows 1-4 - two tables on one sheet)
            items = ([{'kind': 'row', 'y': r['y'][0], 'r': r}
                      for r in sh['rows']]
                     + [{'kind': 'furn', 'y': f['y'][0], 'f': f}
                        for f in sh['furniture']])
            items.sort(key=lambda x: x['y'])
            page = label(n)
            for pl in PRELUDES.get(n, []):
                parts.append(pl)
            if n in PRELUDES:
                parts.append('')
            nums = sorted(r['num'] for r in sh['rows'])
            last_num = nums[-1] if nums else None

            def flush(table):
                if table:
                    parts.append(HEAD)
                    parts.append(SEP)
                    parts.extend(table)
                    parts.append('')
                    return []
                return table

            table = []
            for it in items:
                if it['kind'] == 'furn':
                    f = it['f']
                    if f['key'] in C_TOTALS:
                        # the print's totals row belongs to the table
                        # it follows (no header of its own)
                        cells = ['**%s**' % C_TOTALS[f['key']][0]] + \
                            C_TOTALS[f['key']][1:]
                        table.append('| ' + ' | '.join(cells) + ' |')
                        continue
                    table = flush(table)
                    if f['key'] == 'u1':
                        parts.append('**%s**\n' % f['text'].strip())
                    else:
                        parts.append('*%s*\n' % f['text'].strip())
                    continue
                r = it['r']
                cells = [c if c.strip() else ' '
                         for c in r['cells'][1:]]
                ref = annex_notes.REFS.get((n, r['num']))
                if ref:
                    note_num, ref_page, junk = ref
                    naz = cells[0]
                    if junk and naz.rstrip().endswith(junk):
                        naz = naz.rstrip()[:-len(junk)].rstrip()
                    else:
                        # fall back to a targeted strip of the common
                        # artifacts the superscript left behind
                        naz = re.sub(r'\s*[!?„”"$Ś9⁹*]+$', '', naz)
                    cells[0] = naz + f'[^{ref_page}-{note_num}]'
                table.append(f"| {r['num']} | " + ' | '.join(cells)
                             + ' |')
                if n in annex_notes.RAZEM and r['num'] == last_num:
                    # the series' totals row prints after the last
                    # numbered row (0146: after r111; 0157: after r156)
                    rz = annex_notes.RAZEM[n]
                    cells = ['**%s**' % rz['cells'][0]] + rz['cells'][1:]
                    if rz.get('ref'):
                        nn_, pg_ = rz['ref']
                        cells[0] += f'[^{pg_}-{nn_}]'
                    table.append('| ' + ' | '.join(cells) + ' |')
            table = flush(table)
            # the sheet's note block (the print sets it below the
            # sheet's table)
            for num, ntext in annex_notes.NOTES.get(n, []):
                parts.append(f'[^{page}-{num}]: {ntext}')
            if annex_notes.NOTES.get(n):
                parts.append('')
        else:
            # fallback: the raw-row rendering
            rows = json.load(open(os.path.join(OCR, 'annex_table.json'),
                                  encoding='utf-8'))[n]['rows']
            for num in sorted(int(k) for k in rows if k.isdigit()):
                raw = rows[str(num)].get('raw') or ''
                parts.append(f"{num}. {raw}  ")
        parts.append('')
    # ---- ANEKS II and III (printed sources, pp. 145-150, 151-156) -------
    for group in (ANEX2, ANEX3):
        for n in group:
            parts.append(f'[p. {label(n)}]\n')
            parts.append('\n\n'.join(page_paras[n]))
            notes = []
            for note in struct[n]['notes']:
                notes.append(f"[^{label(n)}-{note['num']}]: {note['text']}")
            if notes:
                parts.append('\n'.join(notes))
    # ---- the plates -----------------------------------------------------
    parts.append("""
[p. 157]

Plany osad (the settlement plans, eight plates) and the Mapa: image
plates, not transcribed (the editor's ruling). Scans tom5_0172-tom5_0175;
tom5_0174's caption reads "3. Nowe al. Wielkokrobielewskie Olędry.
Przykład osady rozrzuconej. Fotografia mapy nr 113 z r. 1830."
""")
    text = '\n\n'.join(parts) + '\n'
    # the print sets its markers tight to the word ('lata³,'): remove
    # the space the token replacement leaves before a label
    text = re.sub(r' +(\[\^)', r'\1', text)
    # the strip's systemic lowercase-l -> capital-I artifact (editor
    # ruling): 'Kl.' (Klassifikationsanschlaege) read as 'KI.', 'Ol.'
    # (Olendry) as 'OI.'/'OIL' - restore the print's sigla everywhere
    # (word-boundary guarded; single-letter Roman numerals untouched)
    for pat, rep in ((r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])KI\.', 'Kl.'),
                     (r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])OIL\b', 'Ol.'),
                     (r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])OI\.', 'Ol.'),
                     # note-layer l->I residue
                     (r'\bNickiedy\b', 'Niekiedy'),
                     (r'Ilolendry', 'Holendry')):
        n = len(re.findall(pat, text))
        text = re.sub(pat, rep, text)
        print('normalize %s -> %s: %d' % (pat, rep, n))
    # SPOT ANSWERS round 2: the footnote-marker audit's ref rewires -
    # applied here on the final text, AFTER the OI./KI. normalizers
    # (several search strings contain 'Ol.')
    nfix = 0
    for n in sorted(BODY_FIXES):
        for old, new in BODY_FIXES[n]:
            if old in text:
                text = text.replace(old, new)
                nfix += 1
            else:
                print('WARN body fix miss %s: %r' % (n, old[:60]))
    print('body marker fixes applied:', nfix)
    nfix2 = 0
    for old, new in BODY_FIXES2:
        if old in text:
            text = text.replace(old, new)
            nfix2 += 1
        else:
            print('WARN body fix2 miss: %r' % old[:60])
    print('body amount fixes applied:', nfix2)
    # ---- SPOT round 5b: the single-letter debris from the two-column
    # OCR scatter. Each stray's true slot was determined from the raw
    # word x/y geometry (x-order inside the print line):
    #  p. 38  'z'  -> line start 'z calkowitego majatku...' (scan 0053,
    #                x377 before calkowitego@440; 'Gdy tedy zalacy sie
    #                z calkowitego majatku swego ogoloconym zostal')
    #  p. 49  'w'  -> line start 'w traktuje te sprawe' (0064 x369,
    #                print line begins at the note margin)
    #  p. 49  'z'  -> 'kto z nich' (0064 x2556 between kto@2436 and
    #                nich@2616)
    #  p. 49  'z'  -> 'ktorykolwiek z naszych Holendrow' (0064 x2508
    #                between ktorykolwiek@2110 and naszych@2560)
    #  p. 49  'w'  -> 'ze w osadach wczesniej-' (0064 x2505 between
    #                ze@2416 and osadach@2580)
    #  p. 99  'r.' -> 'krotko przed r. 1800' (0114 x905 between
    #                przed@709-869 and 1800@987)
    #  p. 99  'gr w' -> '3030 zl 20 1/2 gr w Nowych Dworach' (0114:
    #                the blob after '20' decomposes into small-1/slash/
    #                small-2 = the fraction 1/2, then 'gr'@1254 'w'@1365)
    #  p. 103 'uns' -> line start of the 'auf Erbpacht' line (0118
    #                x366 = note margin; 'Wiesen uns auf Erbpacht
    #                uberlassen')
    #  p. 116 'w'  -> 'Nawet w aktach regulacyjnych' (0132 x387 line
    #                start of the 'aktach' line)
    #  p. 116 'z'  -> 'czesc z nich' (0132 x570 between czesc@386 and
    #                nich@634)
    nfix3 = 0
    for old, new in STRAY_FIXES:
        if old in text:
            text = text.replace(old, new)
            nfix3 += 1
        else:
            print('WARN stray fix miss: %r' % old[:60])
    print('stray fixes applied:', nfix3)
    # ---- the p. 85 leaf repair (SPOT S50's deeper finding): the
    # czynsz paragraph physically begins on print p. 85 (scan 0100,
    # verified y1617-3210 + the printed folio on 0101 = 86) and the
    # print breaks it mid-word after 'w zdewaluowanych'; our assembly
    # leaked the whole paragraph into the p. 86 block. Also: the
    # print's p. 85 note block has NINE notes - the OCR fused notes
    # 3+4 and mis-numbered 5-8; the defs are re-split/renumbered and
    # the refs re-wired to the print's numbers (marker 5 visible at
    # 'w. XVII' in the scan).
    tl = text.split('\n')
    pi = next((i for i, ln in enumerate(tl)
               if ln.startswith('Wśród czynszów pieniężnych')), None)
    di = next((i for i, ln in enumerate(tl)
               if ln.startswith('[^85-1]:')), None)
    if pi is None or di is None:
        print('WARN p85 repair anchors missing', pi, di)
    else:
        par = tl[pi]
        k = par.find('złotówkach tynfowych;')
        part1, part2 = par[:k].rstrip(), par[k:]
        tl[pi] = part2                      # p. 86 keeps the tail
        tl[di:di] = [part1, '']             # p. 85 gains the head
        print('p85 leaf split applied (parts %d/%d chars)'
              % (len(part1), len(part2)))
    text = '\n'.join(tl)
    nfix3 = 0
    for old, new in (
        # def splits/renumbers to the print's 9-note numbering
        ('[^85-3]: Rel. Posn. nr 140, r. 1602, fol. 659 i Kl. XII 7. '
         't Rel. Posn. nr 638, r. 1791, fol. 597.',
         '[^85-3]: Rel. Posn. nr 140, r. 1602, fol. 659 i Kl. XII 7.\n'
         '[^85-4]: Rel. Posn. nr 638, r. 1791, fol. 597.'),
        ('[^85-4]: 36-zlotowy czynsz mamy',
         '[^85-5]: 36-złotowy czynsz mamy'),
        ('[^85-5]: AW. Dłuskic Stare Ol., A. 1.',
         '[^85-8]: AW. Dłuskic Stare Ol., A. 1.'),
        ('[^85-8]: AW. Tuchorskie Stare Ol., dep. A. 1 (r. 1703)',
         '[^85-9]: AW. Tuchorskie Stare Ol., dep. A. 1 (r. 1703)'),
        # ref re-wiring to the print's numbers
        ('przez cały w. XVII[^85-4].', 'przez cały w. XVII[^85-5].'),
        ('wynosił 36 zł z huby,', 'wynosił 36 zł z huby[^85-4],'),
        ('(r. 1688)[^85-5] czynsz', '(r. 1688)[^85-8] czynsz'),
        ('względnie 8—12 talarów[^85-8]—', 'względnie 8—12 talarów[^85-9]—'),
        # the two-column word-order repair (raw y3000-3240)
        ('a nawet 8 zł talar i wtedy wartość wyrosiła jak poprzednio '
         '30—36. za — czynszu zł (srebrnych) 8, względnie 8—12 '
         'talarów',
         'a nawet 8 zł za talar, i wtedy wartość czynszu wyrosiła '
         'jak poprzednio 30—36 zł (srebrnych), względnie 8—12 '
         'talarów'),
    ):
        if old in text:
            text = text.replace(old, new)
            nfix3 += 1
        else:
            print('WARN p85 fix miss: %r' % old[:60])
    print('p85 repair fixes applied:', nfix3)
    # the corrected body tables (SPOT round 4): span replacements
    tl = text.split('\n')
    for start_a, end_a, repl in TABLE_SPANS:
        si = next((i for i, ln in enumerate(tl)
                   if ln.startswith(start_a)), None)
        if si is None:
            print('WARN table span start miss:', start_a)
            continue
        ei = next((i for i in range(si, len(tl))
                   if tl[i].startswith(end_a)), None)
        if ei is None:
            print('WARN table span end miss:', end_a)
            continue
        tl[si:ei + 1] = repl
        print('table span %s: lines %d-%d -> %d' % (start_a, si, ei,
                                                    len(repl)))
    text = '\n'.join(tl)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('written', os.path.abspath(OUT), len(text), 'chars')


if __name__ == '__main__':
    main()
