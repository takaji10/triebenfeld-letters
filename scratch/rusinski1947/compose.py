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
    # unstack the triple miswire
    ('w zdewaluowanych[^85-6][^85-7][^85-8] złotówkach',
     'w zdewaluowanych złotówkach'),
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
    ('pojawiały[^48-9] się rzadko', 'pojawiały się rzadko'),
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
    for a, b in zip(order, order[1:]):
        pa, pb = page_paras[a], page_paras[b]
        while pa and not pa[-1].strip():
            pa.pop()
        while pb and not pb[0].strip():
            pb.pop(0)
        if not pa or not pb:
            continue
        tail = pa[-1].rstrip()
        tail_txt = LABEL_RE.sub(' ', tail).rstrip()
        head = pb[0].lstrip()
        joined = None
        if tail_txt.endswith('-'):
            toks = tail.split()
            # the fragment = the last token that is not a parked label;
            # labels parked after it belong to the joined word
            fi = len(toks) - 1
            parked = []
            while fi >= 0 and LABEL_RE.fullmatch(toks[fi]):
                parked.insert(0, toks[fi])
                fi -= 1
            frag_w = toks[fi] if fi >= 0 else ''
            base = LABEL_RE.sub('', frag_w).rstrip('-')
            m = LABEL_RE.search(frag_w)
            lab = m.group(0) if m else ''
            # the fragment must be a plausible word-half (lowercase
            # letters): rejects sliver junk ('Ooz————') and digits
            if base and re.fullmatch(r'[a-ząćęłńóśźż]+', base) \
                    and len(base) >= 2 and head[:1].islower():
                bw = head.split(' ', 1)
                first = base + bw[0]
                rest = bw[1] if len(bw) > 1 else ''
                joined = first + lab
                if parked:
                    joined += ' ' + ' '.join(parked)
                if rest:
                    joined += ' ' + rest
                page_paras[a] = pa[:-1] + \
                    ([' '.join(toks[:fi])] if fi > 0 else [])
                page_paras[b] = [joined] + pb[1:]
                continue
        elif not tail_txt.endswith(TERM) and head[:1].islower() \
                and not head.startswith('„') and not head.startswith('«'):
            # plain mid-sentence page break: the print's paragraph
            # simply continues over the leaf - the whole paragraph
            # moves to page B (intact, labels included)
            page_paras[a] = pa[:-1]
            page_paras[b] = [tail + ' ' + head] + pb[1:]
            continue
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
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('written', os.path.abspath(OUT), len(text), 'chars')


if __name__ == '__main__':
    main()
