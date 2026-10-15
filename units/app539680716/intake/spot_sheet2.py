# -*- coding: utf-8 -*-
"""The second spot sheet, "The other readings in Breyer's Łazińsk notebook" (2026-10-15).

    python units/app539680716/intake/spot_sheet2.py
    python pipeline/review/queries.py --unit app539680716 --sheet readings2.csv

The editor asked to see the rest of the doubtful readings after answering
the first sheet: all 46 marks of doubt not yet put to them, and one reading
without a mark that a second look put in doubt (s47). Left
out: the four the editor kept with their doubt on the first sheet ([7.?],
[паленный?], [Jäke?], [Jaschek?]) and the editor's own new marks
(au[f/s?] and [?] in the heading of document 9, Polzfu[h?]l, [Zrost?]).
Each Cyrillic word is also given in Latin letters in the note. Made with
the machinery of spot_sheet.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spot_sheet  # noqa: E402

T2 = 'The Emilienheim liquidation table of 1868'
T4 = 'The Łazińsk liquidation table of 1868'
P4 = 'Breyer\'s pencil of 1875, after the dash: who held the holding in 1875'
T11 = 'The Orliny liquidation table'

# (key, document, page id, a piece of the line, the word as it stands, options, note)
ROWS = [
    ('s01', 2, '5164_a1', 'Цигельсдорфъ [Мар.?]', '[Мар.?]', '[Мар.?]|Мар.|Мих.',
     T2 + ', no. 11, Ziegelsdorf (Tsigelsdorf): the forename, read Мар. (Mar.) with doubt. The sheet of 1858 has a Michał Cygielsdorf (Мих., Mikh.).'),
    ('s02', 2, '5164_a1', '[Дикгофъ?] Готл.', '[Дикгофъ?]', '[Дикгофъ?]|Дикгофъ',
     T2 + ', no. 26, Gottlieb ...: the surname, read Дикгофъ (Dikgof, Dyckhoff) with doubt. The sheet of 1858 has a Gottlieb Dykhof.'),
    ('s03', 2, '5164_a2', '[Диконфъ?] Готфр.', '[Диконфъ?]', '[Диконфъ?]|Диконфъ|Дикгофъ',
     T2 + ', no. 27, Gottfried ...: the surname, read Диконфъ (Dikonf) with doubt; it may be the same name as no. 26, Дикгофъ (Dikgof).'),
    ('s04', 3, '5165_a1', '[j. Wloch?]', '[j. Wloch?]', '[j. Wloch?]|j. Wloch',
     'Breyer\'s extracts on Emilienheim: "Eingeschrieben ... i. April 1892" (entered ... in April 1892). The words read "j. Wloch" with doubt.'),
    ('s05', 4, '5165_a2', '[Брушк.?] Клиге', '[Брушк.?]', '[Брушк.?]|Брушк.',
     T4 + ', no. 14. ' + P4 + ': "... Klige", the forename read Брушк. (Brushk.) with doubt.'),
    ('s06', 4, '5166_a1', '— [Франц.?]', '[Франц.?]', '[Франц.?]|Франц.',
     T4 + ', no. 18. ' + P4 + ': read Франц. (Franz.) with doubt.'),
    ('s07', 4, '5166_a1', '— [пол.?] 14; 10 м.', '[пол.?]', '[пол.?]|пол.',
     T4 + ', no. 20. ' + P4 + ': "... 14; 10 Morgen". The first word read пол. (pol.) with doubt.'),
    ('s08', 4, '5166_a1', 'Дан. [Кинастъ?]', '[Кинастъ?]', '[Кинастъ?]|Кинастъ',
     T4 + ', no. 22. ' + P4 + ': "Dan. ...", the surname read Кинастъ (Kinast) with doubt.'),
    ('s09', 4, '5166_a1', '— [пол.?] 18;', '[пол.?]', '[пол.?]|пол.',
     T4 + ', no. 26. ' + P4 + ': "... 18; Runga Wojc. 18". The first word read пол. (pol.) with doubt, as in no. 20.'),
    ('s10', 4, '5166_a2', 'Эд. [Бромке?]', '[Бромке?]', '[Бромке?]|Бромке',
     T4 + ', no. 36. ' + P4 + ': "Ed. ...", the surname read Бромке (Bromke) with doubt.'),
    ('s11', 4, '5166_a2', '[Цельмеръ Фр.?]', '[Цельмеръ Фр.?]', '[Цельмеръ Фр.?]|Цельмеръ Фр.',
     T4 + ', no. 37: the holder of 1868, read Цельмеръ Фр. (Tselmer Fr., Zelmer) with doubt. The holders of nos. 50, 53, 65 and 67 are Цельнеръ (Tselner).'),
    ('s12', 4, '5167_a1', '[Геп.?] Зееръ', '[Геп.?]', '[Геп.?]|Геп.',
     T4 + ', no. 48. ' + P4 + ': "Iv. Henke 29; ... Seer 13", the forename read Геп. (Gep.) with doubt.'),
    ('s13', 4, '5167_a1', 'Штаркъ [Дет.?]', '[Дет.?]', '[Дет.?]|Дет.',
     T4 + ', no. 60, Stark ...: the forename, read Дет. (Det.) with doubt.'),
    ('s14', 4, '5167_a2', 'Кар. [Пашка?]', '[Пашка?]', '[Пашка?]|Пашка',
     T4 + ', no. 69. ' + P4 + ': "Kar. ...", the surname read Пашка (Pashka) with doubt.'),
    ('s15', 4, '5167_a2', '[Обстъ?] Вильг.', '[Обстъ?]', '[Обстъ?]|Обстъ',
     T4 + ', no. 71, ... Wilh.: the surname, read Обстъ (Obst) with doubt.'),
    ('s16', 4, '5167_a2', 'Эрн. [Торно?]', '[Торно?]', '[Торно?]|Торно',
     T4 + ', no. 73. ' + P4 + ': "Ern. ...", the surname read Торно (Torno) with doubt.'),
    ('s17', 4, '5167_a2', 'Ферд. [Шменель?]', '[Шменель?]', '[Шменель?]|Шменель',
     T4 + ', no. 74. ' + P4 + ': "Ferd. ...", the surname read Шменель (Shmenel) with doubt.'),
    ('s18', 4, '5169_a1', '[Готтлибъ?] Готл.', '[Готтлибъ?]', '[Готтлибъ?]|Готтлибъ',
     T4 + ', no. 88. ' + P4 + ': "... Gottl.", the first word read Готтлибъ (Gottlib) with doubt.'),
    ('s19', 4, '5169_a1', '[Бенцлеръ?]', '[Бенцлеръ?]', '[Бенцлеръ?]|Бенцлеръ',
     T4 + ', no. 89. ' + P4 + ': read Бенцлеръ (Bentsler, Benzler) with doubt.'),
    ('s20', 5, '5170_a1', '[тлахтами?]', '[тлахтами?]', '[тлахтами?]|плахтами|тлахтами',
     'Breyer\'s copy of the Łazińsk servitudes: "to carry away what is gathered ...". The last word, how the wood is carried, read тлахтами (tlakhtami) with doubt. The original copy of 1869 (APŁ 39/98/0/-/6603, document 2) has плахтами (plakhtami, "in sheets of cloth"); choose it if Breyer\'s hand allows.'),
    ('s48', 5, '5169_a2', '[паленный?]', '[паленный?]', '[паленный?]|наличный',
     'Asked again: the same servitudes, "to graze all their ... cattle". You kept паленный (palennyi) with doubt on the first sheet; the original copy of 1869 has наличный (nalichnyi, "the cattle they have"), which Breyer was copying. Choose it if his hand allows.'),
    ('s21', 8, '5172_a1', '[Бредъ?]', '[Бредъ?]', '[Бредъ?]|Бредъ',
     'Breyer\'s notes of 1935, on Orliny: a word on its own line after "4 Morgen of waste land", read Бредъ (Bred) with doubt.'),
    ('s22', 8, '5172_a1', '[Гедпаръ?]', '[Гедпаръ?]', '[Гедпаръ?]|Гедпаръ',
     'The same page, names from a forestry plan: "Vdovii Bor, Biskupice, Podbel, Szetlew, Grzebień, ..., Kreshnia". A name read Гедпаръ (Gedpar) with doubt.'),
    ('s23', 8, '5172_a1', '1909 [?]', '[?]', '[?]',
     'The same page: "1909 ... has ... the ...". The word after 1909 is not read.'),
    ('s24', 8, '5172_a1', '[entgekoit?]', '[entgekoit?]', '[entgekoit?]',
     'The same note: "1909 ... hat das ..." (has the ...). The last word read entgekoit with doubt; it makes no sense as read.'),
    ('s25', 8, '5172_a2', '[L…?]', '[L…?]', '[L…?]',
     'Józefów: "Alte Häuser mit ... Giebel z. Strasse" (old houses with ... gable to the street). Only the first letter, L, read.'),
    ('s26', 8, '5173_a1', '[Sattlern?]', '[Sattlern?]', '[Sattlern?]|Sattlern',
     '"30 years ago the bonnets disappeared. Bonnets were made from the ...": read Sattlern (saddlers) with doubt.'),
    ('s27', 8, '5174_a1', '[Sollten?]', '[Sollten?]', '[Sollten?]',
     'Under the heading "Holędry Orliny Biskupicki": "..., stehlen einander Holz" (..., they steal wood from one another). The first word read Sollten with doubt.'),
    ('s28', 8, '5174_a1', '[Frierk?]', '[Frierk?]', '[Frierk?]|Frierk',
     '"..., ein Prediger, die Söhne stehlen" (..., a preacher, the sons steal): a name, read Frierk with doubt.'),
    ('s29', 8, '5174_a1', '[Brenda?]', '[Brenda?]', '[Brenda?]',
     '"In Białoblot ... Tropfen zu Hause getrunken" (... drops drunk at home): read Brenda with doubt; perhaps a drink.'),
    ('s30', 8, '5174_a1', '[Zogel.?]', '[Zogel.?]', '[Zogel.?]|Zogel.',
     '"Viel wilde Ehen (3-4) ... Kinder 7 uneheliche" (many wild marriages; ... children, 7 illegitimate): read Zogel. with doubt, perhaps a name.'),
    ('s31', 8, '5174_a2', '[schlagen sich?]', '[schlagen sich?]', '[schlagen sich?]|schlagen sich',
     'In the right-hand column: "Nach dem Gottesdienst ... jeden Sonntag Tanzvergnügung" (after the service ... every Sunday, dancing). Read "schlagen sich" (they fight) with doubt.'),
    ('s32', 9, '5175_a1', '[Christ.?] Kasner', '[Christ.?]', '[Christ.?]|Christ.',
     'The list of farmers of the Orlin Hauland, no. 23, 17 Morgen: "... Kasner", the forename read Christ. with doubt.'),
    ('s33', 9, '5175_a1', '24,"[Gottfr.?]', '[Gottfr.?]', '[Gottfr.?]|Gottfr.',
     'The same list, no. 24, 17 Morgen: "... ditto (Kasner)", the forename read Gottfr. with doubt.'),
    ('s34', 9, '5175_a1', '[Gottfr.?] M.', '[Gottfr.?]', '[Gottfr.?]|Gottfr.',
     'The same list, no. 25, 16 Morgen: "... M.", read Gottfr. with doubt.'),
    ('s35', 11, '5177_a1', '[Стурценгеръ?]', '[Стурценгеръ?]', '[Стурценгеръ?]|Стурценгеръ',
     T11 + ', no. 8, ... Osip.: the surname, read Стурценгеръ (Sturtsenger) with doubt.'),
    ('s36', 11, '5177_a1', '[Ланитцъ?]', '[Ланитцъ?]', '[Ланитцъ?]|Ланитцъ',
     T11 + ', no. 12, ... Ad.: the surname, read Ланитцъ (Lanitts, Lanitz) with doubt.'),
    ('s37', 11, '5177_a2', '[Гралька?]', '[Гралька?]', '[Гралька?]|Гралька',
     T11 + ', no. 16, ... Wojc., 40 Morgen: the surname, read Гралька (Gralka) with doubt.'),
    ('s38', 11, '5177_a2', '[Вангольдъ?]', '[Вангольдъ?]', '[Вангольдъ?]|Вангольдъ',
     T11 + ', no. 20, ... Gottl.: the surname, read Вангольдъ (Vangold, Wangold) with doubt.'),
    ('s39', 11, '5177_a2', '[Веречъ?]', '[Веречъ?]', '[Веречъ?]|Веречъ',
     T11 + ', no. 23, ... Mat.: the surname, read Веречъ (Verech) with doubt.'),
    ('s40', 11, '5177_a2', '[Дайгеръ?]', '[Дайгеръ?]', '[Дайгеръ?]|Дайгеръ',
     T11 + ', no. 25, ... Mar.: the surname, read Дайгеръ (Daiger) with doubt.'),
    ('s41', 11, '5178_a1', 'Янке [Ш.?]', '[Ш.?]', '[Ш.?]|Ш.',
     T11 + ', no. 31, Janke ...: the initial read Ш. (Sh.) with doubt.'),
    ('s42', 11, '5178_a1', '[Куркина?]', '[Куркина?]', '[Куркина?]|Куркина',
     T11 + ', no. 40, heirs of Jan ...: the surname read Куркина (Kurkina) with doubt. Compare no. 57.'),
    ('s43', 11, '5178_a1', '[Шпицеръ?]', '[Шпицеръ?]', '[Шпицеръ?]|Шпицеръ',
     T11 + ', no. 42, ... Dan.: the surname, read Шпицеръ (Shpitser, Spitzer) with doubt.'),
    ('s44', 11, '5178_a2', '[Шиммеръ?]', '[Шиммеръ?]', '[Шиммеръ?]|Шиммеръ',
     T11 + ', no. 52, ... Leop.: the surname, read Шиммеръ (Shimmer, Schimmer) with doubt.'),
    ('s45', 11, '5179_a1', '[Курвина?]', '[Курвина?]', '[Курвина?]|Курвина|Куркина',
     T11 + ', no. 57, heirs of ...: the surname read Курвина (Kurvina) with doubt; perhaps the same as no. 40, Куркина (Kurkina).'),
    ('s46', 13, '5179_a2', '[напоръ?]', '[напоръ?]', '[напоръ?]|напоръ',
     'Breyer\'s copy of the Orliny servitudes: "in grubbing up stumps ... may be used". The tool, read напоръ (napor) with doubt. On the picture the word seems to begin at the end of the line above ("на-") and end on this one ("поръ"); if so, say so in the note.'),
    ('s47', 8, '5172_a1', 'Вдовьiй', 'Вдовьiй', 'Вдовьiй|Вельскiй',
     'Breyer\'s notes of 1935, the forestry plan: the first name, read Вдовьiй боръ (Vdovii Bor, widow\'s wood) without doubt. On a second look it may be Вельскiй боръ (Velskii Bor), the forest named in the Orliny servitudes (document 13).'),
]
SHIFT = {'s02': 2, 's03': -1, 's08': 1, 's09': 0.7, 's13': 1.5, 's16': 1, 's17': 1, 's22': 1.3, 's23': 2.5,
         's24': 3, 's30': 1, 's32': 1, 's33': 1, 's34': 2, 's35': 3.5, 's36': 4, 's38': 1, 's39': 0.5,
         's40': 1, 's42': 1.5, 's43': 2, 's44': 1, 's45': 1.5, 's46': 0.3, 's47': 2, 's48': 2}
# s31 stands in the narrow right-hand column at the top of the page
BOX = {'s31': (0.17, 0.12)}

# Answered by the editor on 2026-10-15 and worked in (intake/readings2_answers.json
# keeps their answers); taken off the sheet, as their words have changed.
ANSWERED = {'s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12', 's13',
            's14', 's15', 's16', 's17', 's18'}

if __name__ == '__main__':
    spot_sheet.main([r for r in ROWS if r[0] not in ANSWERED], SHIFT, BOX, 'readings2.csv')
