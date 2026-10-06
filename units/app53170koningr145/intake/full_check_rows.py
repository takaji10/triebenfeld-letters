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
    dict(page='0660_a1', kind='misread', weight='formula',
         old='komisja a statibus ani wypadła', new='komisja a statibus Regni wypadła', scan='Kommissya a Statibus Rni wypadła',
         en_old='', en_new='', note='"Rni" is Regni: issued by the Estates of the Kingdom'),
    dict(page='0660_a1', kind='dropped', weight='formula',
         old='ażeby urodzony Prusimski konstytucji wypadłej też przypozwy',
         new='ażeby urodzony Prusimski zadość czyniąc tak prawu koronnemu jako też konstytucji wypadłej też przypozwy',
         scan='ażeby Uro: Prusimski zadosyć czyniąc tak Prawu Koronnemu jako też Konstytucyi wypadłey też Przypozwy',
         en_old='', en_new='', note='seven words: the court orders Prusimski to file his summonses "satisfying both the law of the Crown and the constitution"'),
    dict(page='0661_a1', kind='misread', weight='fact',
         old='Osin, Łazów, Szetlewka dziedzic dukt swój', new='Osin, Łazów, Szetlewa dziedzic dukt swój', scan='Osin, Łazow Szetlewa Dziedzic Dukt swoy',
         en_old='', en_new='', note='Szetlew, as in the list of his estates on the page before, not Szetlewek'),
    dict(page='0661_a2', kind='misread', weight='formula',
         old='dziewięćdziesiątego drugiego ze znanej od drogi', new='dziewięćdziesiątego drugiego zeznanej od drogi', scan='Drugiego zeznaney od Drogi',
         en_old='', en_new='', note='"zeznanej", recorded; the same slip as on leaf 673'),
    dict(page='0661_a2', kind='misread', weight='fact',
         old='teraz do Pyzdr naukom bieżąca', new='teraz do Pyzdr na Łukom bieżąca', scan='teraz do Pyzdr na Łukom bieżąca',
         en_old='', en_new='', note='the road from Osiny "now running to Pyzdry by way of Łukom"'),
    dict(page='0662_a1', kind='misread', weight='formula',
         old='jeszcze pokłada manifest i wzywa o podobnyż postępek', new='jeszcze pokłada manifest i wizją o podobnyż postępek',
         scan='ieszcze pokłada manifest y wizyą o podobnyż postępek',
         en_old='', en_new='', note='he lays before the court a protest and an inspection ("wizją"), not "and calls"'),
    dict(page='0662_a2', kind='misread', weight='formula',
         old='bez wielkiej dyskwizycji będących', new='bez wszelkiej dyskwizycji będących', scan='bez wszelkiey dyskwizycyi będących',
         en_old='', en_new='', note='"beyond all question", not "without great question"'),
    dict(page='0662_a2', kind='dropped', weight='fact',
         old='i jakoby od tegoż narożnika przez Konwent jednostajnie zawsze',
         new='i jakoby od tegoż narożnika przez urodzonego Prusimskiego przedtem i teraz formowanego a przez Konwent jednostajnie zawsze',
         scan='y iakoby od tegoż narożnika przez Uro Prusimskiego przedtym y teraz formowanego a przez Konwent iednostaynie zawsze',
         en_old='', en_new='', note='eight words skipped between two "przez": the corner point is the one "formed by the Honourable Prusimski before and now, and acknowledged by the Convent" at all three earlier sittings'),
    dict(page='0664_a1', kind='misread', weight='formula',
         old='oblatowany twierdzące podług tego Kompromisu lub inszego jakowego, aktu którego nie można ob revolutionem temporum z na lesć kopce',
         new='oblatowany twierdząc że podług tego Kompromisu lub inszego jakowego, aktu którego nie można ob revolutionem temporum znaleźć kopce',
         scan='Oblatowany twierdząc że podług tego Kompromissu lub inszego iakowego, Aktu, ktorego nie można ob revolutionem temporum znaleść kopce',
         en_old='', en_new='', note='"asserting that ... which act cannot be found by reason of the passage of time"'),
    dict(page='0664_a1', kind='misread', weight='formula',
         old='Łomowa jednym gruncie jako to jest per directum wtej kontumacji wyrażono będących z Trąbczynem i innymi wsiami pryncypał nie pozwanych',
         new='Łomowa w jednym gruncie jako to jest per directum w tej kontumacji wyrażono będących z Trąbczynem i innymi wsiami pryncypalnie pozwanych',
         scan='Łomowa w iednym gruncie iako to iest per directum w tey kontumacyi wyrażono będących z Trąbczynem y innemi wsiami pryncypalnie pozwanych',
         en_old='', en_new='', note='"summoned as principals"; the words "dziedzicach o rozgraniczenie tychże dziedzin Łukomia Imielna i Łomowa" are a clerk\'s insertion from the foot of the page, and the transcription has them in the right place'),
    dict(page='0664_a1', kind='misread', weight='formula',
         old='ani Bukowe ab illo od Łukomia', new='ani Bukowe ab aevo od Łukomia', scan='ani Bukowe ab ævo od Łukomia',
         en_old='', en_new='', note='"from of old"; the ligature æ was read as "ill". Fairly sure, not certain'),
    dict(page='0664_a2', kind='misread', weight='formula',
         old='od narogu zagórowskiego, o nez między', new='od narogu zagórowskiego, oneż między', scan='od narogu zagorowskiego, oneż między',
         en_old='', en_new='', note='"oneż", the same (boundary)'),
    dict(page='0665_a1', kind='misread', weight='fact',
         old='w głowie lasu Ostrowie zaraz', new='w głowie lasu Ostrowce zaraz', scan='w Głowie lasu Ostrowce zaraz',
         en_old='', en_new='', note='the wood is Ostrowce, as everywhere else'),
    dict(page='0665_a1', kind='misread', weight='formula',
         old='zeznanej za sądzą jako też', new='zeznanej zasadza jako też', scan='zeznaney zasadza iako też',
         en_old='', en_new='', note='"zasadza", sets up (his corner point), not "judges"'),
    dict(page='0665_a1', kind='misread', weight='formula',
         old='urodzonego Starosty osądzając Bukowe', new='urodzonego Starosty osadzając Bukowe', scan='Uo Starosty osadzaiąc Bukowe',
         en_old='', en_new='', note='"osadzając", putting Bukowe in the place of Trąbczyn, not "judging"'),
    dict(page='0665_a2', kind='misread', weight='fact',
         old='czerniakowic Tomasz i Fabian', new='Czerniakowie Tomasz i Fabian', scan='Czerniakowie Tomasz y Fabian',
         en_old='', en_new='', note='a surname in the plural: the Czerniaks, Tomasz and Fabian'),
    dict(page='0665_a2', kind='misread', weight='fact',
         old='borowy Piotr, Szyman, narożnik, Wojciech Zelak', new='borowy Piotr Szyman, Nadolnik, Wojciech Zelak', scan='Borowy Piotr Szyman, Nadolnik, Woyciech Zelak',
         en_old='Piotr, Szyman, [uncertain: narożnik], Wojciech Zelak', en_new='Piotr Szyman, Nadolnik, Wojciech Zelak',
         note='a name in the list of Trąbczyn witnesses; the editor had marked "narożnik" as doubtful in the English. The scan has Nadolnik'),
    dict(page='0665_a2', kind='misread', weight='formula',
         old='dawno i teraz wyzwany a zaś', new='dawno i teraz używany a zaś', scan='dawno y teraz używany a zaś',
         en_old='', en_new='', note='"used", not "challenged": the Łukom forest "of old and now used" by Łukomia'),
    # --- add above ---
]
