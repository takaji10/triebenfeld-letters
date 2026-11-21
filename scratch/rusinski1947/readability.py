# -*- coding: utf-8 -*-
"""The readability replacements: systematic OCR misreads that are
contextually UNAMBIGUOUS, verified by the read-through (five independent
readings of the whole draft).

Whole-token matches only. Deliberately NOT here: anything with a real
alternative reading or a real-word lookalike ('lisy' could be foxes,
'wyrosiła' could be 'grew') - those are spot-sheet items.
"""

UNI = {
    # the r->n class ('n' misread as 'r'; systematic on several scans)
    'trudro': 'trudno', 'Trudro': 'Trudno',
    'możrość': 'możność', 'Możrość': 'Możność',
    'ronad': 'ponad',
    'powinrością': 'powinnością', 'mocro': 'mocno',
    'nieufrość': 'nieufność', 'Pilrość': 'Pilność',
    'skazara': 'skazana', 'skazaro': 'skazano',
    'oszdników': 'osadników', 'osądników': 'osadników',
    'osądnika': 'osadnika', 'osądniku': 'osadniku',
    'dysporowania': 'dysponowania', 'dysporowaniem': 'dysponowaniem',
    'korntyngentu': 'kontyngentu',
    'lokoware': 'lokowane',
    # single-letter garbles, certain by context
    'nieji': 'niego',
    'micszkańcy': 'mieszkańcy', 'Micszkańcy': 'Mieszkańcy',
    'rrasuwa': 'nasuwa', 'rrasuwają': 'nasuwają',
    'danira': 'danina', 'danirą': 'daniną',
    'szkolrego': 'szkolnego', 'rauczyciela': 'nauczyciela',
    'chcrakteryzuje': 'charakteryzuje',
    'rozszerzdjąca': 'rozszerzająca',
    'zagospodlarowanie': 'zagospodarowanie',
    'sprowedzali': 'sprowadzali', 'zepotrzebowania': 'zapotrzebowania',
    'domirowsło': 'dominowało', 'omawiare': 'omawiane',
    'obecrość': 'obecność', 'wszystkic': 'wszystkie',
    'Naramowskic': 'Naramowskie', 'olędrskie': 'olęderskie',
    'przypadzło': 'przypadło',
    'Polaki': 'Polacy', 'sporc': 'spośród',
    'pzńskich': 'pańskich', 'zdolrość': 'zdolność',
    'ludł.ość': 'ludność', 'ludł.ości': 'ludności',
    'chuby': 'huby', 'siebic': 'siebie',
    'molradeł': 'mokradeł', 'starowił': 'stanowił',
    'kzrczmarza': 'karczmarza', 'rdzbiorów': 'rozbiorów',
    'nezogół': 'Naogół', 'Neogół': 'Naogół',
    'chronologiczrą': 'chronologiczną',
    'wicksze': 'większe', 'klesyfikacyjne': 'klasyfikacyjne',
    'mcterialnych': 'materialnych', 'tebeli': 'tabeli',
    'spcłecznym': 'społecznym', 'przykłed': 'przykład',
    'ż:den': 'żaden', 'Holer.drów': 'Holendrów',
    'Murzyrowskie': 'Murzynowskie', 'bsada': 'osada',
    'podzwaną': 'podawaną', 'mcnonitów': 'menonitów',
    # annex II/III old-Polish garbles verified by internal repeats
    'stedmsctnego': 'siedmsetnego', 'nadare': 'nadane',
    'jwinie': 'winien', 'Dzicdzica': 'Dziedzica',
    'Kicińskicego': 'Kicińskiego', 'bkbydź': 'bydź',
    'więccy': 'więcej', 'iakiegokolwick': 'iakiegokolwiek',
    'Kotusą': 'Kotusz', 'bobrawiona': 'poprawiona',
    'żęby': 'żeby',
}

# two-token pairs (a split or doubled word)
BI = {
    ('Zdarze', 'ły'): ('Zdarzały', ''),
    ('Spotyksło', 'nie'): ('Spotykano', ''),
}


def apply(text):
    toks = text.split(' ')
    out = []
    i = 0
    while i < len(toks):
        if i + 1 < len(toks):
            c1 = toks[i].strip('.,;:!?»”"()')
            c2 = toks[i + 1].strip('.,;:!?»”"()')
            if (c1, c2) in BI:
                r1, r2 = BI[(c1, c2)]
                t1 = toks[i]
                pre = t1[:t1.find(c1)] if c1 in t1 else ''
                out.append(pre + r1 if r1 else '')
                if r2:
                    t2 = toks[i + 1]
                    post = t2[t2.find(c2) + len(c2):] if c2 in t2 else ''
                    if post:
                        out.append(r2 + post)
                i += 2
                continue
        tok = toks[i]
        core = tok.strip('.,;:!?»”"()')
        if core in UNI:
            idx = tok.find(core)
            pre = tok[:idx] if idx >= 0 else ''
            post = tok[idx + len(core):] if idx >= 0 else ''
            out.append(pre + UNI[core] + post)
        else:
            out.append(tok)
        i += 1
    return ' '.join(out)
