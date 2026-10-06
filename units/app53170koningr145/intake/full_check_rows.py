# -*- coding: utf-8 -*-
"""What the full check of APP 53/17/0/-/Konin Gr.145 against the scans found.

The editor asked (2026-10-06) for every page to be read for dropped phrases,
and for each to be listed with a word on whether it matters to the meaning.
One entry per finding, in page order:

    page    the page id (leaf N recto is <N>_a2, leaf N verso is <N+1>_a1)
    kind    'dropped'  words on the scan that the transcription lacks
            'misread'  a reading that changes the sense (small slips of spelling are not collected)
    old     the transcription as it stood; must stand exactly once on the page
    new     the same with the scan's words put in, in the modern spelling of the rest
    scan    the words as the scan has them
    en_old, en_new   the English before and after, where it has to follow ('' where it need not)
    weight  'court'    changes what the court found or ordered
            'fact'     adds or changes a place, person, measure, date or party
            'formula'  wording only
    note    anything else

Which pages have been read is in full_check_pages.txt (full_check_note.py).
The rows are applied by corrections_full.py when the check is finished.
"""

ROWS = [
    dict(page='0655_a2', kind='misread', weight='formula',
         old='obtulit officium prosequenti ad actandum et in acta prosequenti ingrossandum porrexit Decretum Commissoriale graniciale imprimis Haereditates eodem decreto specificatas pro illustris magnificos commissarios prolaturus sigillisque Gentilicis communitum sanum salvum ex illesum',
         new='obtulit officio praesenti ad acticandum et in acta praesentia ingrossandum porrexit Decretum Commissoriale graniciale inter Haereditates eodem decreto specificatas per illustres magnificos commissarios prolatum sigillisque Gentilitiis communitum sanum salvum et illesum',
         scan='obtulit Offo pnti ad acticand et in Acta pntia ingrossand porrexit Decrum Comissoriale graniciale inr Hareditates Eod Decro specificatas p Illres Mgcos Commissarios prolatum sigillisq Gentilicus communitum sanum salvum et illesum',
         en_old="presented to the office for prosecution, and submitted for enrollment in the present records, a Commissorial Boundary Decree, setting forth in the first instance the estates specified in the said decree, to be laid before the illustrious Right Honourable commissioners, sealed with family seals",
         en_new="presented to the present office for entry, and submitted for enrollment in the present records, a Commissorial Boundary Decree between the estates specified in the said decree, pronounced by the illustrious Right Honourable commissioners, sealed with family seals",
         note='the abbreviations of the Latin formula were filled out wrongly: "pnti" is praesenti, "inr" inter, "p" per, "prolatum" agrees with Decretum'),
    dict(page='0655_a2', kind='dropped', weight='fact',
         old='oraz dla Drzewiec konwentskich zaś Drzewice i Trąbczyna dla dóbr swoich',
         new='oraz dla Drzewiec konwentskich z odpychaniem tylko z tąd dziedziny Trąbczyna, dziedzicy zaś Drzewiec i Trąbczyna dla dóbr swoich',
         scan='oraz dla Drzewiec Konwentskich z odpychaniem tylko z tąd Dziedziny Trąbczyna, Dziedzicy zaś Drzewiec y Trąbczyna dla Dobr swoich',
         en_old="and for the convent's Drzewce — and for Drzewce and Trąbczyn Mały, for their own estates and for Łukomia with rejection, and also Bukowe",
         en_new="and for the convent's Drzewce, with rejection only of the estate of Trąbczyn from here; while the heirs of Drzewce and Trąbczyn, for their own estates and for Łukomia with rejection, and also Bukowe",
         note='eight words skipped between two mentions of Drzewce and Trąbczyn. They say which neighbour each side acknowledged the three corner mounds for: the Chełmski brothers for Łukomia, Bukowe and Drzewce but not for Trąbczyn; the heirs of Drzewce and Trąbczyn for their own estates and Łukomia'),
    dict(page='0657_a1', kind='misread', weight='formula',
         old='w tę rotę ja wyżej przysięgam', new='w tę rotę: Ja N. przysięgam', scan='w tę Rotę. Ja N. Przysięgam',
         en_old='', en_new='', note='"N." for the name of the man swearing; check the English'),
    dict(page='0657_a2', kind='misread', weight='formula',
         old='zeznam świadectw sądzie będę', new='zeznań świadectw sądził będę', scan='zeznań świadectw sądził będę',
         en_old='', en_new='', note='check the English'),
    dict(page='0657_a2', kind='misread', weight='formula',
         old='kary na Ziemi o gwałtowności poczynione będzie należeć ściągną, nad grodę szkody przez wiolencych,',
         new='kary na kiem o gwałtowności poczynione będzie należeć ściągną, nadgrodę szkody przez wiolencje,',
         scan='kary na kiem o gwałtowności poczynione będzie należeć ściągną, nadgrodę szkody przez wiolencye,',
         en_old='', en_new='', note='"on whom it shall fall", not "on the land"; "compensation for damage", one word; check the English'),
    dict(page='0657_a2', kind='misread', weight='formula',
         old='wyznaczeni przez nas wyżej wyrażonej i urodzeni komisarze', new='wyznaczeni przez nas wielmożni i urodzeni komisarze',
         scan='wyznaczeni przez nas WW. y Uro: Kommisarze',
         en_old='', en_new='', note='"WW." is Wielmożni, the style of the commissioners; check the English'),
    # --- add above ---
]
