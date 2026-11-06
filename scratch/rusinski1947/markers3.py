# -*- coding: utf-8 -*-
"""Markers v3: the line pass as the primary source.

The page-pass TSV yields only ~14% of the markers; the line pass (2.5x)
yields ~105% of them as (a) glued digit tails and (b) standalone 1-2
digit tokens after a word. v3 collects the line-pass candidates in
reading order, drops the number-context false positives (a digit whose
neighbour tokens are numeric; a 3+ digit token; a digit inside a date
span), then assigns 1..n in order against the page's note count. Where
the candidates exceed the notes, the excess (weakest-context) drop;
where they fall short, the page is flagged for the spot sheet with the
line crops.

Output: markers.json v3 + shortfall report. The label: <page>-<n>.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TAIL = re.compile(r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)[*?]*\d{1,2}[*?]?'
                  r'[.,;:»”"]?$', re.UNICODE)
DIGIT = re.compile(r'^\d{1,2}[.,]?$')

# markers recovered against the print (the per-page audit): scan ->
# [(line_top, tok, kind, out)] where 'out' is an explicit replacement
# for the token ('{label}' placeholder) when the fused token must be
# split ('608' -> '60' + marker 6); tok matches the STRUCTURE-line
# token (substring match). Every entry below was verified against the
# print (3x band reads) and the def's content.
MANUAL_ADD = {
    # p. 43: 1 ciała¹, 2 gminnego², 3 lata³, 4 lat⁴, 5 Marianowo⁵,
    # 6 rozbiorów⁶ (auto '8,' keeps), 7 Gebhardta⁷, 8 Schulza⁸, 9 1613⁹
    '0058': [
        (778, '1),', 'manual', '[^{label}]),'),
        (996, 'gminnego.', 'glued', None),
        (1959, '3,', 'manual', '[^{label}],'),
        (1959, '£.', 'manual', '[^{label}].'),
        (2176, '5.', 'manual', None),
        (3132, '7?', 'manual', '[^{label}]'),
        (3132, '8,', 'manual', '[^{label}],'),
        (3428, '1613', 'manual', '1613[^{label}],'),
    ],
    # p. 68: 1 cale¹, 2 57,6 cm², 3 ślady³ (auto), 4 hubą⁴ (auto *.),
    # 5 morgom⁵, 6 60⁶, 7 włóki⁷, 8 powienien⁸, 9 śladu⁹, 10 gospodarzy¹⁰
    '0083': [
        (682, 'cale', 'glued', None),
        (999, '?.', 'manual', 'cm[^{label}].'),
        (2174, '8.', 'manual', '[^{label}].'),
        (2278, '608', 'manual', '60[^{label}]'),
        (2919, '”.', 'manual', '[^{label}].'),
        (3239, '8,', 'manual', '[^{label}],'),
        (3454, '?.', 'manual', '[^{label}].'),
        (3865, "'0)", 'manual', '[^{label}]).'),
    ],
    # p. 78: 1 garncy¹, 2 litra², 3 sąsiednich³, 4 1773⁴ (auto £.),
    # 5 pańskiego⁵ (auto), 6 pieniężny⁶ (auto 6), 7 poczciwi⁷ (auto ?),
    # 8 domowej⁸, 9 sztrafą⁹
    '0093': [
        (702, '1.', 'manual', '[^{label}].'),
        (1004, '*.', 'manual', '[^{label}].'),
        (1329, '3,', 'manual', '[^{label}],'),
        (3473, 'poczciwi”', 'manual', '„poczciwi”[^{label}]'),
        (3685, 'domowej', 'glued', None),
        (3685, 'sztrafą', 'manual', 'sztrafą”[^{label}].'),
    ],
    # p. 86: 1 30¹, 2 70², 3 zł³, 4 XVIII⁴, 5 czasowo⁵, 6 równocześnie⁶,
    # 7 tynfa⁷, 8 ogólnego⁸, 9 leśne⁹ (auto ?.), 10 zł¹⁰ (auto zł10)
    '0101': [
        (783, '301', 'manual', '30[^{label}]'),
        (889, '70?', 'manual', '70[^{label}]'),
        (1100, '8,', 'manual', '[^{label}],'),
        (1515, '£.', 'manual', '[^{label}].'),
        (2149, '5.', 'manual', None),
        (2254, 'równocześnie$.', 'manual', 'równocześnie[^{label}],'),
        (2566, '%.', 'manual', '[^{label}].'),
        (2785, '8.', 'manual', '[^{label}].'),
    ],
    # p. 98: 1 Schmidt¹, 2 1773², 3 podatkowych³, 4 włóki⁴, 5 morgów⁵,
    # 6 g⁶
    '0113': [
        (1010, '1.', 'manual', '[^{label}].'),
        (1323, '1773', 'manual', '1773[^{label}],'),
        (1773, '%.', 'manual', '[^{label}].'),
        (2182, '$,', 'manual', '[^{label}],'),
        (2317, '5,', 'manual', '[^{label}],'),
        (3373, 'g%.', 'manual', 'g[^{label}].'),
    ],
    # p. 97: 1 ujskiego¹ (auto), 2 Brandenburger², 3 Koerth³
    '0112': [
        (1175, 'Brandenburger?', 'manual', 'Brandenburger[^{label}]'),
        (1175, '3.', 'manual', '[^{label}].'),
    ],
    # p. 6 (0021): 1 chełmińskiego¹ (auto), 2 niderlandzkich² (auto ?.),
    # 3 domniemana³ (print '3', line-pass misread '8'), 4 gminy⁴
    # (misread 'ft.'), 5 wybieralny⁵ (misread '9;'), 6 naturze⁶
    # (auto $.), 7 robocizny⁷ (misread '?,'), 8 polskich⁸ (fused/lost)
    '0021': [
        (1938, '3;', 'manual', '[^{label}];'),
        (2249, 'ft.', 'manual', '[^{label}].'),
        (2461, '9;', 'manual', '[^{label}];'),
        (3099, '?,', 'manual', '[^{label}],'),
        (3207, 'polskich;', 'manual', 'polskich[^{label}];'),
    ],
    # p. 23 (0038): 1 fused into 'Tp. 89¹,' ('891,'); 2-5 auto
    '0038': [
        (1864, '891,', 'manual', '89[^{label}],'),
    ],
    # p. 27 (0042): 1 ewangelicka¹ (dropped by the old trim),
    # 2 osady² ('?' artifact on the structure token), 3 osad³
    # ('%' artifact), 4-5 auto (Charłub⁴/Chromiec⁵), 6-7 Kiączyńskie⁶
    # Radoszkowskie⁷ (lost in the trim), 8-11 auto
    '0042': [
        (1880, '1,', 'manual', None),
        (2515, 'osady?', 'manual', 'osady[^{label}]'),
        (2626, '%.', 'artifact', '[^{label}].'),
        (3043, '6,', 'manual', None),
        (3043, '7,', 'manual', None),
    ],
    # p. 31 (0046): 1 jawiają się¹ (auto), 2 Niemcami² ('?' on 'cami?'),
    # 3 Polacy³ ('%' artifact), 4 auto
    '0046': [
        (2790, 'cami?', 'manual', 'cami[^{label}],'),
        (2899, '%.', 'artifact', '[^{label}].'),
    ],
    # p. 36 (0051): 1 auto, 2 itd.² ('?.'), 3 krajem³ ('%'), 4 auto;
    # '28' is the count 'w 28 wypadkach', '*.' at 805 is junk;
    # 5 = 'wędrówek⁵.' - the raised 5 pixel-verified at the last
    # line's end (top bar + bowl), the structure lost it entirely:
    # LINE_TEXT places the label, this entry feeds the walk its index
    '0051': [
        (2044, '?.', 'artifact', '[^{label}].'),
        (2145, '%.', 'artifact', '[^{label}].'),
        (2989, 'wędrówek.', 'manual', 'wędrówek[^{label}].'),
    ],
    # p. 45 (0060): 1 fused '1721¹,', 2 czynszowe”², 3 Schmidta³ (auto
    # '*'), 4 auto '4' (the '£' misread), 5 wyjątkami⁵ ('?,'),
    # 6 obrócić”⁶ ('8%.'), 7 dworskich⁷ ('?.')
    '0060': [
        (671, '1721,', 'manual', '1721[^{label}],'),
        (880, 'szowe”', 'manual', 'szowe”[^{label}]'),
        (1940, '?,', 'artifact', '[^{label}],'),
        (3003, '8%.', 'manual', '[^{label}].'),
        (3552, '?.', 'artifact', '[^{label}].'),
    ],
    # p. 47 (0062): 1 auto, 2 rąk² ('?;'), 3-4 auto, 5 '(r. 1785)⁵,',
    # 6 Chełmskich⁶ ('€'), 7-8 glued 'Ol.7'/'OI.8,', 9 auto '?*.',
    # 10 będzie”¹⁰ ('!*.'), 11 mielcucha¹¹ ("';");
    # the '1's are 'i' misreads, '2' is the beczek count
    # p. 48 (0063): 1 fused 'pan¹,', 2 = zoom pending (the '”.' on 789),
    # 3-5 auto, 6 pastwisko⁶ ('%.'), 7-9 auto ('*.' at 3244 duplicates
    # the '7,' - both models' read of the same marker)
    '0063': [
        (680, '1,', 'manual', '[^{label}],'),
        # the print's marker 2: a 46px glyph after 'gminy' (pixel-verified),
        # misread by both models as the closing quote
        (789, 'gminy”', 'manual', 'gminy[^{label}]'),
        (2685, '%.', 'artifact', '[^{label}].'),
    ],
    # p. 54 (0069): 1 dokumenty¹ ('L'), 2 auto, 3 gruntu³ ('%),'),
    # 4 Klugegeld⁴ ('*.'), 5 auto '*' (robocizn), 6 auto, 7 pan⁷ ('?.'),
    # 8 fused 'panu⁸;' ('panu$8;'), 9-11 auto; the hocizn6/8 gluings
    # are model-junk of the robocizn line
    '0069': [
        (779, 'L', 'manual', '[^{label}]'),
        (1198, '%),', 'manual', '[^{label}]).'),
        (1304, '*.', 'artifact', '[^{label}].'),
        (2028, '?.', 'artifact', '[^{label}].'),
        (2340, 'panu$8;', 'manual', 'panu[^{label}];'),
    ],
    # p. 74 (0089): 1 'zezwalał¹,' (glued, raised 1 pixel-verified),
    # 2 'pastuchów².' (the '%.'; def 2 Rataje pastucha quote), 3
    # 'pańskim³.' ('?.' — def 3 Sygn. J.w. = the 2nd Rataje ref), 4
    # 'opłat⁴.' (the '+.'; def 4 Stróżewskie quote), 5 'barciach⁵.'
    # (def 5 Zakrzewo), 6 'dworze⁶.' (def 6 Złotkowo), 7-9 auto
    # (Kliny curiosum, Puszczykowskie 'do dworu', Inscr. Valc.
    # nieograniczone). NOTE: norm() strips artifact glyphs to '', so a
    # MANUAL_DROP with an artifact tok kills every artifact candidate
    # within +-80px - the drops below clear the whole artifact cluster
    # ('?.'@777/'*.'@807 dual-pass pair, '£'@1215 heading junk,
    # '*.'@1248), and 2 and 4 are re-added as manual entries.
    '0089': [
        (677, 'zezwalał1,', 'manual', 'zezwalał[^{label}],'),
        (781, '%.', 'artifact', '[^{label}].'),
        (995, '?.', 'artifact', '[^{label}].'),
        (1248, '+.', 'manual', '[^{label}].'),
        (1332, 'barciach5.', 'manual', 'barciach[^{label}].'),
        (1535, 'dworze 6.', 'manual', 'dworze[^{label}].'),
    ],
    # p. 80 (0095): markers are RAISED glyphs on this plate. 1 'na
    # przekup”¹.' (the '? 1.' is one raised digit read twice), 2
    # 'kupować².' (structure lost it; band read 'wać ?.'; pixel check:
    # small raised blob + period), 3 '(browaru)³.' (raised '3' after
    # the paren, shape-matched to note-3's '3'), 4 '„kawał roli”⁴.'
    # (reads '€'/'4'), 5 'rzadko⁵,' (pixel-verified raised '5'), 6
    # 'bezpłatnie⁶;' (bowl glyph, $/€ misreads), 7 'zakazane⁷,'
    # (pixel-verified '7'); note 7 (AW. Borkowskie) was merged into
    # note 6 by the strip - split in spot_fixes. Auto '1'@1731 (the
    # '€.' misread), '$;'@3568 and '*'@4266 (notes-region '+') are
    # spurious - left to the count-trim.
    '0095': [
        # the '? 1.' is one raised digit read twice; the LINE_TEXT
        # rewrite in spot_fixes places 80-1 (this entry only feeds the
        # walk its correct index)
        (919, '1.', 'standalone', None),
        (1219, 'wać.', 'manual', 'wać[^{label}].'),
        (1430, '?.', 'artifact', None),
        (1747, '€.', 'manual', '[^{label}].'),
        (3470, 'rzadko5,', 'manual', 'rzadko[^{label}],'),
        (3600, '$;', 'manual', '[^{label}];'),
        (3692, '7”,', 'manual', '[^{label}],'),
    ],
    # p. 81 (0096): 1 'owiec¹.' (auto missed it), 2 'owiec)²,' (the
    # '*?' fused; '4,'@1193 and '25'@1296 are the DATA digits 'od
    # każdych 4 / 25 owiec' - dropped), 3-5 auto (wszystkie owce³,
    # świadczenia⁴, pastwiska⁵), 6 'panem⁶.' (the '*.'), 7 'zapas⁷,'
    # (the '”' = raised 7), 8 'huby⁸.' (auto missed it), 9
    # 'rogaciznę⁹.' (the '?.'), 10 AUTO '19.'@2687 = the print's
    # '10.' ('0' misread '9'; closed-oval shape matches the note
    # block's '10'), 11 'kultury¹¹.' (the twin '1' autos read the two
    # digits separately - dropped, '11.' re-added), 12 'lasu¹².' (the
    # '*.', the record's '12.'@2999 confirms); the raised ticks after
    # 'wypasać' (2476 end) and 'trzody' (2588) are blemishes, not
    # markers - the 1-12 sequence completes without them
    '0096': [
        (1089, '1.', 'standalone', None),
        (1296, 'owiec)*?,', 'manual', 'owiec)[^{label}],'),
        (1942, 'panem*.', 'manual', 'panem[^{label}].'),
        (2152, 'zapas”,', 'manual', 'zapas[^{label}],'),
        (2269, '8.', 'standalone', None),
        (2476, 'rogaciznę?.', 'manual', 'rogaciznę[^{label}].'),
        (2903, '11.', 'standalone', None),
        (3015, '*.', 'artifact', None),
    ],
    # p. 83 (0098): 1 auto (rzadkości¹), 2 'odstąpić².' (the '”' =
    # raised 2; def 2 AW. B. 110), 3 auto ('%.' on ekwiwalentu — def 3
    # Krystynka), 4 'owsie)⁴.' (the '*.'), 5 'gruntach⁵,' (auto read
    # it num_ctx — dropped, re-added plain; def 5 Cisiogórskie), 6
    # 'pańskich⁶.' (the '8' misread; def 6 Kawczyn), 7 auto ('%.' on
    # cegielni — def 7 Zamorze), 8 'piwa⁸.' (the record read '9.';
    # def 8 Stróżewskie beczka piwa); '1'@2822 = the word 'i' in
    # 'rozwój i dochodowość'
    '0098': [
        (981, 'odstąpić”.', 'manual', 'odstąpić[^{label}].'),
        (1300, '*.', 'artifact', None),
        (2071, '5,', 'standalone', None),
        (2071, '8.', 'standalone', None),
        (3445, '8.', 'standalone', None),
    ],
    # p. 84 (0099): 1 'dworu¹.' (the '!' glued; def 1 wyżywienie
    # sources), 2 'sąsiednich².' (the structure lost the raised 2; the
    # band read '?. ' - placed via LINE_TEXT, this entry feeds the
    # walk its index), 3 'itd.) ³.' (the '3.'), 4 'gospodarcze⁴.'
    # (the '£'), 5 'lat⁵,' (glued 'lat5,'; def 5 = the wolnizny
    # statistics, confirming the body's '6—7 lat'), 6 'siedzib⁶.'
    # (the '$'); '4.'@2792 was the record's read of the '£' (dropped),
    # '1'@3116 = the data digit of 'od 1—3 lat'
    '0099': [
        (676, 'dworu!.', 'manual', 'dworu[^{label}].'),
        (892, 'sąsiednich.', 'manual', 'sąsiednich[^{label}].'),
        (1218, '3.', 'standalone', None),
        (2798, '£.', 'artifact', None),
        (2907, 'lat5,', 'manual', 'lat[^{label}],'),
        (3874, '$.', 'artifact', None),
    ],
    # p. 88 (0103): the okupne chronology - every note is a place+date
    # matching a body item. 1 'zł)¹' (the '!' after '== 120 zł' =
    # Stare Dłuskie 40 talarów), 2 'zł)².' (the ')?.' = Meryń Stary
    # 100 talarów), 3-6 '(r. 1701)³ (r. 1707)⁴ (r. 1709)⁵ (r. 1712)⁶'
    # (all in the structure text, autos missed them), 7 'zł⁷,' (the
    # '”' on 600 zł — def 7 Krystynka/Huta), 8 AUTO '8,'@2466 (6 zł —
    # def 8 Chełmskie), 9 'huby⁹.' (the '?.', def 9 Złotkowo),
    # 10-11 '©,' and '4,' on the r. 1771/1773 line (def 10 Zamorze,
    # def 11 Lubaskie), 12-13 '2,' and '13,' (def 12 Rudka, def 13
    # Chmielinka), 14 "'4," (def 14 Włościejewskie), 15-17 '5,' '16,'
    # '"r.' (the raised '17' pixel-verified as two top-aligned glyphs;
    # def 15 Boruja r. 1785, def 16 Strychowskie, def 17 Charłub
    # r. 1787). Dropped data-digit autos: '2' (2 grupy), '?'@1717
    # (no glyph on the line - gaps pixel-checked empty), '2' (2
    # osadach), '40'/'15'/'5' (talarów/kurs amounts), '1'@3126 (the
    # 14's first digit). Sliver lines 1963/2699/2931/3036/3143 held
    # the words the structure lost ('po', 'za', three dashes) -
    # restored via LINE_TEXT and the slivers dropped.
    '0103': [
        (1941, 'zł)!', 'manual', 'zł)[^{label}]'),
        (2047, 'zł)?.', 'manual', 'zł)[^{label}].'),
        (2047, '3,', 'standalone', None),
        (2155, '4,', 'standalone', None),
        (2155, '5,', 'standalone', None),
        (2155, '6.', 'standalone', None),
        (2364, 'zł”,', 'manual', 'zł[^{label}],'),
        (2597, '?.', 'artifact', None),
        (2893, '©,', 'manual', '[^{label}],'),
        (2893, '4,', 'standalone', None),
        (3004, '2,', 'standalone', None),
        (3004, '13,', 'standalone', None),
        (3108, "'4,", 'manual', '[^{label}],'),
        (3236, '5,', 'standalone', None),
        (3236, '16,', 'standalone', None),
        (3236, '"r.', 'manual', '[^{label}].'),
    ],
    # p. 90 (0105): 1 'zupełnie¹,' (auto read it num_ctx - dropped,
    # re-added plain), 2 'huby².' (the glued '*?.'; def 2 Tuchorskie
    # AGH), 3 'jutrzyny³.' (the '%.'; def 3 Rutkowski), 4 'zagonów”⁴,'
    # (the '*,'; def 4 Kiełczynek), 5 'roli⁵.' (glued 'roli5.'; def 5
    # Stare Łoskońskie), 6-7 '(30⁶ do 60⁷ zagonów)' (the '€' and the
    # '60?' glue; band OCR read the two raised glyphs differently, so
    # 6-before-7 stands), 8 'koszenie⁸,' (auto num_ctx - dropped,
    # re-added), 9 'koszenie⁹,' (the '%,'), 10 'siewu¹⁰.' (the '0.'),
    # 11 'łąki¹¹.' (the '1.'), 12 'zarastały”¹².' (the '1%.');
    # dropped data autos: '50' (50 dni), '3'/'12' (3 dni po 12
    # zagonów), '1'@2711 (junk). Note 6 carries note 7's '7"?' (strip
    # merge) and note 7 a '? ' prefix - fixed in spot_fixes
    '0105': [
        (1113, '1,', 'standalone', None),
        (1221, 'huby*?.', 'manual', 'huby[^{label}].'),
        (1879, '%.', 'artifact', None),
        (2393, '*.', 'artifact', None),
        (2501, 'roli5.', 'manual', 'roli[^{label}].'),
        (2622, '€', 'manual', '[^{label}]'),
        (2622, '60?', 'manual', '60[^{label}]'),
        (2715, '8.', 'standalone', None),
        (2715, '%.', 'artifact', None),
        (2843, '0.', 'standalone', None),
        (2933, '1.', 'standalone', None),
        (3178, '1%.', 'manual', '[^{label}].'),
    ],
    # p. 96 (0111): 1 'Holsche¹.' (the structure's 'l.' after 'sche' =
    # a pixel-verified raised 1 + period; def 1 Geographie u.
    # Statistik), 2 auto ('?.' on 'zmniejszała się ciągle' — def 2
    # Netzdistrikt), 3 auto ('9.' = the raised 3 on 'liczne procesy'),
    # 4 auto ('£.' on 'Schmitt *.'), 5 'panowaniem⁵.' (glued; def 5 =
    # the Brzekiniec petition quote); '1'@2039 = junk near '(r. 1849)'
    '0111': [
        (1628, 'l.', 'standalone', None),
        (3552, 'panowaniem5.', 'manual', 'panowaniem[^{label}].'),
    ],
    # p. 92 (0107): 1 'sformułowany¹,' (the '!' after 'mułowany'; def 1
    # = the Suchylas 'Iłuki... bez wymówienia' quote), 2 '"nie
    # powinien"²,' (the '2,' in the structure text; def 2 AW. B. 296),
    # 3 'szarwarkowymi)³,' (the '%,'; def 3 Charłub), 4
    # 'sprzężajne⁴.' (the '£.'; def 4 Kl. XII Króteckie/Rożnowskie/
    # Rudka/Zamorze), 5 'pracy⁵,' (the '$5' double-misread of the
    # raised 5; def 5 Milczewskich/Snowidowic), 6 AUTO '$,'@3733 on
    # 'budynków dworskich⁶.' (def 6 = the long Blinek... list).
    # Dropped: '4'@2862 (the £. misread), 'pracyvy*5,'@2991 (the
    # record's duplicate read), '1'@3733 (the 'i' of 'młynów i').
    # NOTE SPLIT: the print has SIX notes - the strip merged note 4
    # (Kl. XII...Zamorze, its '4' misread as ''') into note 3; fixed
    # in spot_fixes
    '0107': [
        (2149, 'mułowany!,', 'manual', 'mułowany[^{label}],'),
        (2461, '2,', 'standalone', None),
        (2890, '%,', 'artifact', None),
        (2890, '£.', 'artifact', None),
        (2998, 'pracy$5,', 'manual', 'pracy[^{label}],'),
    ],
    # p. 103 (0118): 1 'mienia¹.' (the '1.'; def 1 Zimmermann,
    # Fryderyk Wielki), 2 'stanu².' (the '??.' glued to 'stanu' —
    # def 2 'Por. s. 84, przyp. 258'), 3 'polskich³.' (the '%.'; def 3
    # = the Trzydomy petition's German quote)
    '0118': [
        (770, '1.', 'standalone', None),
        (1824, 'stanu”??.', 'manual', 'stanu[^{label}].'),
        (3728, '%.', 'artifact', None),
    ],
    # p. 104 (0119): 1 auto ('1,' on procesy¹ — def 1 Dom. P. 0755),
    # 2 'robocizny².' (the structure lost the 2; def 2 Dom. P. 5209,
    # the Chorzępowa robocizny), 3 'procesy³.' (the structure's '9.' =
    # the raised 3; def 3 Meryń), 4 auto ('*' on 'po największej
    # części' — def 4 the kościol zwolnienie remark), 5 auto ('5.' on
    # proboszczów — def 5 Zakrzewo kompozyty quote), 6 auto ('6.' on
    # meszne — def 6 Wyszyński), 7 'równocześnie⁷.' (the '?.', def 7
    # Kuślińskie quote), 8 '(ziarnie)⁸,' (glued; def 8
    # Włościejewskie/Książ), 9 'pieniądzach⁹.' (the '%.'; the record's
    # '9'@2935 duplicate dropped; def 9 Huta/Tuchorskie)
    '0119': [
        (1018, 'robocizny.', 'manual', 'robocizny[^{label}].'),
        (1231, '9.', 'standalone', None),
        (2846, '?.', 'artifact', None),
        (2975, '(ziarnie)8,', 'manual', '(ziarnie)[^{label}],'),
        (2975, '%.', 'artifact', None),
    ],
    # p. 108 (0123): 1 'znosić"¹.' (the '1.'; def 1 Góździn), 2
    # 'szkatuły².' (the '?..' — one dot is the period; def 2
    # Nieszawskie), 3 'uchwalone"³,' (the '3,'; def 3 Rel. Posn. 140),
    # 4 'podymnym⁴.' (the '*.'; the auto '4.'@1636 misplaces - dropped;
    # def 4 Pecna), 5 'hybernę⁵.' (the band's '85' double-read of the
    # raised 5; def 5 Brzekiniec/Słonawskie), 6 'kasy⁶,' (the '%.'; the
    # num_ctx auto '6'@2269 dropped; def 6 Podgradowice/Kotusz), 7
    # '100 zł⁷,' (the '?'; def 7 Sieraków amounts), 8 '1775⁸' (glued;
    # def 8 Rybarski). '50'@3012 = the data 'około 50 zł'
    '0123': [
        (688, '1.', 'standalone', None),
        (902, '?..', 'manual', '[^{label}].'),
        (1434, '3,', 'standalone', None),
        (1641, '*.', 'artifact', None),
        (1746, '5.', 'standalone', None),
        (2279, '%,', 'artifact', None),
        (3132, 'zł?,', 'manual', 'zł[^{label}],'),
        (3243, '17758', 'manual', '1775[^{label}]'),
    ],
    # p. 109 (0124): 1 'podymnym¹.' (glued '!.'; def 1
    # Rożnowskie/Skrzydlewo), 2 '1789²' (the '?' glue; def 2 Rybarski),
    # 3 'rzezi³,' (the '%,'; def 3 AW. Wilcz), 4-5 auto (duchownych⁴,
    # ekwipunkiem⁵), 6 'biedny"⁶.' (the '8.'; def 6 Von den
    # Haulindern), 7 'dobrze"⁷.' (the '?.'; def 7 Netzdistrikt);
    # dropped junk autos at 756/885 (the record's reads of the same
    # markers)
    '0124': [
        (786, 'podymnym!.', 'manual', 'podymnym[^{label}].'),
        (863, '1789?', 'manual', '1789[^{label}]'),
        (863, '%,', 'artifact', None),
        (2870, '8.', 'standalone', None),
        (2960, '?.', 'artifact', None),
    ],
    # p. 114 (0129): 1 'gospodarzy¹.' (the structure lost the raised 1 -
    # LINE_TEXT places it; def 1 = the nauczyciel income list), 2
    # 'mniej².' (the '?.'), 3 auto ('3.' on budynków), 4 '1793⁴' (the
    # '+' = the raised 4 before 'składały się'), 5 'rzemieślnika⁵' (the
    # structure misread the raised 5 as '8'; top set to 2950 so it
    # sorts before the 6), 6 auto ('6.' on gospodarza — the same
    # glyph's better record-read), 7 'tkacz⁷,' (the '%,'), 8
    # 'karczmarz⁸,' (the '%,'), 9 'krawcom⁹.' (the '?*.'). Dropped:
    # data digits '6'/'3' (6 zł/3 zł od dzieci), '7'×2 (junk), '8'@2956
    # (the other pass's read of the 5), '8,'@3175 (the record's read of
    # the 8)
    '0129': [
        (696, 'gospodarzy.', 'manual', 'gospodarzy[^{label}].'),
        (1019, '?.', 'artifact', None),
        (1997, '+', 'manual', '[^{label}]'),
        (2950, '8', 'standalone', None),
        (3063, '%,', 'artifact', None),
        (3192, '%,', 'artifact', None),
        (3300, '?*.', 'artifact', None),
    ],
    # p. 119 (0134): 1 'wyjątki¹.' (the '!.' = raised 1 + period; def 1
    # Rel. Cost. 217 Rostarzewscy), 2 'Miłkowskie OI.².' (the '?.';
    # def 2 Komisja pruska pastor Piotrowa quote), 3 'ironią³.' - the
    # raised 3 pixel-verified after 'ironią' (two-bowl glyph,
    # top-aligned); the structure lost it: LINE_TEXT places the label,
    # this entry feeds the walk its index; def 3 Von den Haulindern
    # s. 254. The print's note block has THREE notes - the strip split
    # note 2's German quote into a phantom note 3 (fixed in
    # spot_fixes); '*.'@1306 = junk
    '0134': [
        (1500, 'wyjątki!.', 'manual', 'wyjątki[^{label}].'),
        (1930, 'OI.?.', 'manual', 'OI.[^{label}].'),
        (2885, 'ironią.', 'standalone', None),
    ],
    # p. 120 (0135): 1 'okolicy¹.' - the raised 1 pixel-verified
    # between 'okolicy' and the period (flag + base serif); the
    # structure lost it: LINE_TEXT places the label, this entry feeds
    # the walk its index; def 1 Schmitt Geschichte s. 401, 2
    # 'ogrodzić².' (the '%.'; def 2 AW. Góździn kierchow quote)
    '0135': [
        (677, 'okolicy.', 'standalone', None),
        (1313, '%.', 'artifact', '[^{label}].'),
    ],
    # p. 117 (0132): 1 'wyznania¹' (the '!' glued at line end; def 1
    # AW. Wielkokrobielewskie), 2 'religijnych².' (the '%.'; def 2
    # Kuślińskie), 3 auto ('3,' on 'członków'); '*'@1940 = the other
    # pass's duplicate of the '%.' (dropped - norm('') coverage check
    # can't see artifact duplicates)
    '0132': [
        (1841, 'wyznania!', 'manual', 'wyznania[^{label}]'),
        (1957, 'religijnych %.', 'manual', 'religijnych[^{label}].'),
    ],
    # p. 26 (0041): the coefficient paragraph. 1 '93.569¹.' (the
    # structure's glued '93.5691.' - the raised 1 pixel-verified after
    # '93.569'; the auto '1'@2043 placed after 'pozostanie' is a
    # spurious data digit - dropped), 2 'zmian²;' (the '”' = the
    # raised 2, pixel-verified; def 2 = the Tp. 72/89/90 comparison),
    # 3 = the inline full-size '3' of '6.05 3,' (separate word box;
    # def 3 'Współczynnik ten...' = the 6.05 coefficient). The print's
    # note block has THREE notes - the strip merged note 3
    # ('Współczynnik ten...') into note 2 after 'KI. i G.' (fixed in
    # spot_fixes)
    '0041': [
        (2360, '93.5691.', 'manual', '93.569[^{label}].'),
        (3078, 'zmian”;', 'manual', 'zmian[^{label}];'),
        (3504, '3,', 'standalone', None),
    ],
    # p. 29 (0044): THREE notes (the strip's 'note 1' = 'Wszystkie
    # wspomniane osady...' is actually LIST ITEM 1 of the 'danych
    # zrodlowych' enumeration - body lines 3457/3553/3668; removed and
    # the notes renumbered in spot_fixes). 1 'Polak¹.' - the raised 1
    # pixel-verified between 'Polak' and the period (flag+stem+base
    # serif; the structure's 'Polaki' read the marker as 'i'; def 1
    # 'Natomiast miało miejsce przenikanie...' contrasts the claim), 2
    # 'zupełnie².' (the structure's 'zupełnie*?.' - three independent
    # OCR reads saw the raised 2; def 2 'Zupełnie wyjątkowo znalazła
    # się taka notatka źródłowa' = the Brodnica names note, echoing
    # 'brak prawie zupełnie'), 3 'Holendrzy³.' (the '%.'; def 3
    # Gebhardt's contrary position on the first settlers). '40%,'
    # = the %'s own circles misread (BODY_FIXES); the small mark after
    # 'równouprawnienia,' (y2146) is an apostrophe-class blemish
    '0044': [
        (893, 'Polaki.', 'manual', 'Polak[^{label}].'),
        (2046, 'zupełnie*?.', 'manual', 'zupełnie[^{label}].'),
        (2796, '%.', 'artifact', '[^{label}].'),
    ],
    # p. 4 (0019): 1 'czasów¹.' (the '!.' = raised 1; def 1
    # Beheim-Schwarzbach Meklemburgia tradition), 2 'współwyznawców².'
    # (the '”' = raised 2; def 2 Schmidt s. 315), 3 = the '3,' after
    # '(Preussisch Holland)' (def 3 Schumacher), 4 'Ferbera⁴' (glued;
    # def 4 Ludkiewicz), 5 'Holendrów⁵.' (the '$.'; def 5 Schmidt s.
    # 316 + Baranowski), 6 'Gdańsk⁶,' (the structure lost the raised 6;
    # def 6 Ludkiewicz s. 31 on the Gdańsk route). Dropped false
    # candidates: '1'@1199 and 'Dodieqłvcl1'@2033 (the words 'i'), and
    # the note-block number glyphs '*'@4585/'*'@4690/'$'@4904
    '0019': [
        (1306, '!.', 'manual', '[^{label}].'),
        (2666, 'współwyznawców”.', 'manual', 'współwyznawców[^{label}].'),
        (3095, '3,', 'standalone', None),
        (3723, 'Ferbera4', 'manual', 'Ferbera[^{label}]'),
        (3723, 'Holendrów$.', 'manual', 'Holendrów[^{label}].'),
        (4064, 'Gdańsk,', 'manual', 'Gdańsk[^{label}],'),
    ],
    # p. 7 (0022): 1 'kilkudziesięciu¹.' (the '!.' = raised 1; def 1
    # Ludkiewicz + Lustracja 30/50 lat), 2 'wieczystą².' (the '?.' auto
    # already correct), 3 'wolni³.' (the '3,' auto), 4 = the '£.' on the
    # '...i Książęcych' line (raised 4; def 4 'Zob. dalej, s. 12') -
    # placed by LINE_TEXT (the auto landed after 'osz-'), 5
    # 'odrębne⁵,' (raised 5 lost by the structure; def 5 Guradze), 6
    # 'równoważne⁶.' (def 6 'Zob. dalej, s. 55'), 7 = the '8.' after
    # 'zalesionych' (pixel-verified 8-shaped glyph - the print's 7th
    # marker; def 7 Stenger's Hauland definition). Dropped: the '1'
    # num_ctx doubles at 877/909 and the note-block '?'@4585
    '0022': [
        (788, '!.', 'manual', '[^{label}].'),
        (1199, '3,', 'standalone', None),
        (2883, 'odrębne,', 'manual', 'odrębne[^{label}],'),
        (2967, 'równoważne.', 'manual', 'równoważne[^{label}].'),
        (3178, '8.', 'standalone', None),
        (2344, 'Książęcych', 'manual', 'Książęcych'),
    ],
    # p. 8 (0023): 1 auto (rozbiór¹), 2 = the '?' at the 'słowa
    # Holländer' line end (def 2 Beheim-Schwarzbach/Schmidt/Maas), 3 =
    # 'leśnych³.' - the sliver's '8' = the raised 3 (LINE_TEXT restores
    # the words the slivers hold; def 3 Kremmer/Schütze), 4 = the '4'
    # after 'Hładyłowicz' (def 4 Zmiany krajobrazu s. 86). Dropped: the
    # note-block '*'@4457/'*'@4562 (note 2's number glyph read twice)
    '0023': [
        (883, '1.', 'standalone', None),
        (1728, '?', 'artifact', '[^{label}]'),
        (2276, '4', 'standalone', None),
        (2041, 'leśnych', 'manual', 'leśnych'),
    ],
    # p. 56 (0071): 1 województwa¹ (full-size digit, TSV w=45), 2
    # rozrzuconej² ('?.'); the line-pass '1' at 2023 is the word 'i'
    # ('ulicówka i typ' - no page-pass digit box exists there)
    '0071': [
        (882, '1.', 'manual', '[^{label}].'),
        (2129, '?.', 'artifact', '[^{label}].'),
    ],
    # p. 57 (0072): 1 sztuczny¹ ('1,'), 2 chrustu² ('?.'), 3
    # szkudłami³ ('*'); the '1' at 896 is 'i' ('wąwałku i to')
    '0072': [
        (2491, '1,', 'manual', '[^{label}],'),
        (3411, '?.', 'artifact', '[^{label}].'),
        (3722, '*.', 'artifact', '[^{label}].'),
    ],
    # p. 58 (0073): 1 auto, 2 wystawiony”² ('%.'), 3 dyspozycją”³
    # ('%.'), 4 stawiali”⁴ ('4,'), 5-6 auto; '*?,' at 1204 is the
    # line-pass read of the same '%' - dropped
    '0073': [
        (1221, '%.', 'artifact', '[^{label}].'),
        (1421, '%.', 'artifact', '[^{label}].'),
        (1537, '4,', 'manual', '[^{label}],'),
    ],
    # p. 47 (0062): 1 auto, 2 rąk² ('?;'), 3-4 auto, 5 '(r. 1785)⁵,',
    # 6 Chełmskich⁶ ('€'), 7-8 glued 'Ol.7'/'OI.8,', 9 auto '?*.',
    # 10 będzie”¹⁰ ('!*.'), 11 mielcucha¹¹ ("';");
    # the '1's are 'i' misreads, '2' is the beczek count
    '0062': [
        (1412, '?;', 'artifact', '[^{label}];'),
        (1938, '5,', 'manual', '[^{label}],'),
        (1938, '€', 'artifact', '[^{label}]'),
        (2041, 'Ol.7', 'glued', None),
        (2041, 'OI.8,', 'glued', None),
        (2682, '!*.', 'manual', '[^{label}].'),
        (2892, "';", 'manual', '[^{label}];'),
    ],
}
# false auto candidates to remove: scan -> [(top, tok)]
MANUAL_DROP = {    '0058': [(984, '2.'), (1947, '44'), (1947, '3.'), (1947, '60'),
             (1978, '44'), (1978, '00'), (1978, '*.'), (2163, '5,'),
             (3117, '7'), (3117, '8,')],
    '0083': [(661, '24'), (976, 'com2'), (976, 'cm2'), (976, '6'),
             (1440, '??'), (2171, '2'), (2171, '60'), (2927, '*.')],
    '0093': [(666, '8'), (1205, '1'), (2474, 'C7yNns7'), (3451, '?')],
    '0101': [(777, '50'), (879, '|'), (1093, '38'), (1511, '|'),
             (1830, '2'), (1937, '10'), (1937, '6'), (3196, '|')],
    '0113': [(1345, 'Jl57'), (2281, 'morgów*9'), (991, '1.')],
    # p. 97: '22' was the DATE ('22 maja 1782'), not a marker; the
    # '8' in the quote was the 8 of '8 Ellen'
    '0112': [(1830, '22'), (2626, '8')],
    '0021': [(1915, '8.'), (3693, '18')],
    '0042': [(2489, '3'), (2489, '7'), (2489, '*'), (2609, '17')],
    '0019': [(1199, '1'), (2033, 'Dodieqłvcl1'), (4585, '*'),
             (4690, '*'), (4904, '$')],
    '0022': [(776, '1,'), (877, '1'), (909, '1'), (4585, '?')],
    '0023': [(2280, '*'), (4457, '*'), (4562, '*'), (2250, '4')],
    '0051': [(977, '28'), (805, '*.')],
    '0060': [(1934, 'wyjlątkam1*,'), (2991, '$.')],
    '0062': [(2140, '1'), (2238, '1'), (2778, '2')],
    '0063': [(3244, '*.')],
    '0069': [(1593, 'hocizn6'), (1593, 'hocizn8')],
    '0089': [(807, '*.'), (1215, '£')],
    '0096': [(1193, '4,'), (1296, '25'), (2789, '1'), (2892, '1'),
             (2892, 'Z20216N12'), (2999, '12.')],
    '0098': [(2060, '5,'), (2822, '1'), (3445, '9.')],
    '0099': [(2792, '4.'), (3116, '1'), (3874, '6.')],
    '0103': [(1304, '2'), (1717, '?'), (1752, '2'), (1832, '40'),
             (1942, '15'), (1942, '5'), (3126, '1')],
    '0105': [(1099, '50'), (1129, '1,'), (1211, 'hubv?2.'), (1855, '3.'),
             (2285, '3'), (2285, '12'), (2711, '8.'), (2711, '1')],
    '0111': [(2039, '1')],
    '0107': [(2862, '4'), (2991, 'pracyvy*5,'), (3733, '1')],
    '0118': [(1812, '?,')],
    '0119': [(989, '2.'), (1205, '?.'), (2935, '9')],
    '0123': [(1636, '4.'), (2269, '6'), (3012, '50')],
    '0124': [(756, '1'), (885, '1'), (885, '$,'), (885, 'rzez1')],
    '0129': [(2075, '7'), (2297, '7'), (2513, '6'), (2620, '3'),
             (2956, '8'), (3175, '8,')],
    '0134': [(1306, '*.')],
    '0132': [(1940, '*')],
    '0041': [(2043, '1')],
    '0071': [(2023, '1')],
    '0072': [(908, '1')],
    '0073': [(1204, '*?,')],
}
# whole regions where every digit is table data, not a marker:
# scan -> [(lo, hi)]
MANUAL_DROP_RANGES = {
    '0081': [(1900, 2900)],
}


def line_candidates(text):
    """Candidates in one line's tokens: [(kind, tok_index, tok, weight)]."""
    toks = text.split()
    out = []
    for i, w in enumerate(toks):
        prev = toks[i - 1] if i else ''
        nxt = toks[i + 1] if i + 1 < len(toks) else ''
        m = TAIL.match(w)
        if m and '*' in w or (m and '?' in w):
            out.append(('glued-artifact', i, w, 3))
            continue
        if m and re.search(r'\d$', w) and len(m.group('base')) >= 2 \
                and not re.fullmatch(r'\d+', w):
            out.append(('glued', i, w, 2))
            continue
        if re.fullmatch(r'[*?$§£?]+[.,;:»”"]?', w):
            # an isolated artifact glyph: the print's inline marker as
            # the models read it ('*', '$', '?.') - almost always the
            # marker, never prose. '|' excluded (line-art, not markers)
            out.append(('artifact', i, w, 2))
            continue
        if DIGIT.match(w) and i > 0:
            prev_ok = re.search(r'[^\W\d_]$', prev, re.UNICODE)
            nxt_num = re.fullmatch(r'[\d.,%/]+', nxt) if nxt else False
            prev_num = re.fullmatch(r'[\d.,%/]+', prev) if prev else False
            if prev_ok and not nxt_num and not prev_num:
                out.append(('standalone', i, w, 1))
    return out


def main():
    spath = os.path.join(OCR, 'structure4.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure2.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure.json')
    struct = json.load(open(spath, encoding='utf-8'))
    markers = {}
    shorts = []
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            continue
        want = len(notes)
        lp_path = os.path.join(OCR, 'lines', n + '.json')
        if not os.path.isfile(lp_path):
            shorts.append((n, want, 0, 'no line pass'))
            continue
        recs = json.load(open(lp_path, encoding='utf-8'))
        # the TSV word boxes for the GEOMETRIC check: a superscript
        # marker digit is ~half the line's type height; a TEXT number
        # ('co 4 tygodnie') is full height. Without this check real
        # numbers were consumed as markers and their digits LOST from
        # the text (the readers' 'numbers dropped behind labels'
        # class), shifting every later label on the page.
        pw = json.load(open(os.path.join(OCR, n + '.json'),
                            encoding='utf-8'))['words']
        line_h = {}
        for x in pw:
            if x[5].strip():
                line_h.setdefault(round(x[1] / 45), []).append(x[3])
        line_h = {k: sorted(v)[len(v) // 2] for k, v in line_h.items()}

        def is_superscript(top, tok):
            # The print sets its footnote markers as INLINE FULL-SIZE
            # digits (measured: 'Bemberga 1.' h=57 vs line 64; the old
            # 0.62-height test killed real markers). No geometric
            # separation exists - every candidate is kept; the
            # number-context flag below marks the ambiguous placements
            # for the spot sheet instead.
            return True, 0, 0
        cands = []
        for r in recs:
            if r.get('skipped'):
                # skipped lines were high-confidence and tail-free; but
                # a marker may still ride them: BOTH the glued tails
                # and the standalone/artifact candidates of the page
                # pass's own read are the fallback
                for kind, i, w, weight in line_candidates(r['page']):
                    cands.append((kind, r['top'], w, 1, False))
                for w in r['page'].split():
                    m = TAIL.match(w)
                    if m and re.search(r'\d$', w) \
                            and len(m.group('base')) >= 2:
                        cands.append(('skipped-glued', r['top'], w, 1,
                                      False))
                continue
            for src in ('line_pol', 'line_std'):
                toks = (r.get(src) or '').split()
                for kind, i, w, weight in line_candidates(r.get(src) or ''):
                    if kind == 'standalone':
                        ok, h, lh = is_superscript(r['top'], w)
                        if not ok:
                            continue
                        # number-context flag: a standalone digit whose
                        # next token is a lowercase word is ambiguous
                        # (marker 'Hollander 2' vs number 'co 4
                        # tygodnie') - the placement keeps the digit
                        # and the spot sheet lists the case
                        nxt = toks[i + 1] if i + 1 < len(toks) else ''
                        num_ctx = bool(nxt) and nxt[:1].islower()
                    else:
                        num_ctx = False
                    cands.append((kind, r['top'], w, weight, num_ctx))
        # order by line, then position
        cands.sort(key=lambda c: (c[1], c[0] != 'glued-artifact'))
        # dedup: both OCR models produce the same candidate on a line
        # (same top, same token) - the pairs displaced REAL markers via
        # the count-trim and stacked double labels in the body
        norm = lambda tk: re.sub(r'[^\w]', '', tk, re.UNICODE).lower()
        best = {}
        for c in cands:
            k = (c[1], norm(c[2]))
            if k not in best or c[3] > best[k][3]:
                best[k] = c
        cands = sorted(best.values(),
                       key=lambda c: (c[1], c[0] != 'glued-artifact'))
        # manual audit marks: markers recovered against the print that
        # the models missed (fused digits '608' = '60' + marker 6), and
        # false auto candidates to drop ('44' read as a marker). A
        # manual add carries an 'out' replacement for the text token.
        cands = [c for c in cands
                 if not any(abs(c[1] - dt) <= 80 and norm(c[2]) == norm(dtk)
                            for (dt, dtk) in MANUAL_DROP.get(n, []))
                 and not any(lo <= c[1] < hi
                             for (lo, hi) in MANUAL_DROP_RANGES.get(n, []))]
        prot = []
        rest = []
        for c in cands:
            covered = norm(c[2]) and any(
                abs(c[1] - mtop) <= 80 and norm(c[2]) == norm(mtok)
                for (mtop, mtok, mk_, mo) in MANUAL_ADD.get(n, []))
            (prot if c[3] >= 4 or covered else rest).append(c)
        for (mtop, mtok, mkind, mout) in MANUAL_ADD.get(n, []):
            prot.append((mkind, mtop, mtok, 4, False, mout))
        # re-dedup within prot: a manual entry duplicating an already
        # covered auto candidate must not stack two labels (norm()''
        # artifact toks fall back to the raw token so two DIFFERENT
        # artifact glyphs on one line never merge)
        best2 = {}
        for c in prot:
            k = (c[1], norm(c[2]) or c[2])
            if k not in best2 or c[3] > best2[k][3]:
                best2[k] = c
        prot = list(best2.values())
        # the trim only drops UNPROTECTED candidates: the audit-verified
        # markers must survive it
        room = max(0, want - len(prot))
        if len(rest) > room:
            rest = sorted(rest, key=lambda c: -c[3])[:room]
        cands = prot + rest
        cands = [(c + (None,))[:6] if len(c) == 5 else c for c in cands]
        cands.sort(key=lambda c: (c[1], c[0] != 'glued-artifact'))
        out = []
        for i, (kind, top, w, weight, num_ctx, extra) in enumerate(cands):
            e = {'label': f'{int(n) - 15}-{i + 1}', 'top': top,
                 'tok': w, 'kind': kind, 'weight': weight,
                 'num_ctx': num_ctx}
            if extra:
                e['out'] = extra
            out.append(e)
        markers[n] = out
        if len(out) < want:
            shorts.append((n, want, len(out), ''))
            print(n, f'SHORT {len(out)}/{want}')
    with open(os.path.join(OCR, 'markers.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(markers, fh, ensure_ascii=False)
    print('pages:', len(markers), 'short:', len(shorts))


if __name__ == '__main__':
    main()
