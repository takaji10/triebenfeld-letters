# -*- coding: utf-8 -*-
"""The English of APŁ 39/98/0/-/6603, written in session (2026-10-15).

Tables: the English table has the same rows and the same figures as the
original (publish_translations.english_table checks it); only the name
column and the words of the headings and text rows are translated. Names
are transliterated letter by letter from the Russian, as in 53/968/0/-/716
(the old letters ѣ, і, ъ included; the hard sign is left out), so "Мерцъ
Карлъ" is "Merts Karl"; the German form behind a name is not guessed. A
line of text in a table document is translated line by line, so a word
broken at the end of a line in the Russian is completed on that line.

Terms: моргъ Morgen, прентъ rod (the Polish pręt), десятина desiatina,
сажень sazhen (square), Присутствіе board, Учредительный Комитетъ the
Constituent Committee, Непремѣнный Членъ permanent member, плахта
sheet-load (the cloth in which wood was carried), фура cart.

Text documents: TEXT_EN, page by page. A doubtful word is
"[uncertain: ...]", a word not read "[illegible]".
"""
import re

TRANS = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'і': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'iu', 'я': 'ia', 'ѣ': 'e', 'ѳ': 'f', 'ѵ': 'i',
}

WORDS = [
    (r'\bНаслѣд\.', 'heirs of'), (r'\bНасл\.', 'heirs of'), (r'\bНас\.', 'heirs of'), (r'\bН-ки\b', 'heirs of'),
]

_LAND = 'Amount of land in each farmstead holding, in Morgen and rods.'
_DUES = 'Amount of the dues to be compensated by the Government under articles 14 to 26 of the Ukase on the Liquidation Commission.'
_FARMS = 'Farmsteads that passed into the full ownership of the peasants under the Imperial Ukases of 19 February (2 March) 1864.'
_SERV = 'Kinds and extent of the servitudes the peasants enjoy. Remarks.'

CELL = {
    # the heading of the printed form
    'Количество земли въ каждомъ усадебномъ участкѣ, въ моргахъ и прентахъ.': _LAND,
    'Размѣръ повинности, подлежащій вознагражденію отъ Правительства по статьямъ 14—26 Указа о Ликвидаціонной Коммиссіи.': _DUES,
    'По проекту ликвидаціонной табели.': 'In the draft liquidation table.',
    'Подъ жилымъ строеніемъ съ огородомъ или безъ огорода.': 'Under the dwelling, with or without a garden.',
    'Подъ пахатными полями.': 'Under arable fields.', 'Подъ лугами.': 'Under meadows.', 'Подъ выгономъ.': 'Under pasture.',
    'Неудобной.': 'Unusable.', 'Всей вообще.': 'In all.',
    '№№ усадьбъ. По порядку.': 'No. of the farmstead, in order.',
    'Усадьбы, поступившія въ полную собственность крестьянъ на основаніи Высочайшихъ Указовъ 19 Февраля (2 Марта) 1864 года.': _FARMS,
    'М.': 'M.', 'П.': 'R.', 'Рубли.': 'Roubles.', 'Коп.': 'Kop.',
    # the title pages
    'ЛИКВИДАЦІОННАЯ ТАБЕЛЬ': 'LIQUIDATION TABLE',
    'селенія Колоніи Лазинской': 'of the village of the Łazińsk Colony',
    'состоящаго Калишской губерніи, Слупецкаго уѣзда,': 'in the Kalisz governorate, Słupca district,',
    'состоящаго въ Калишской губерніи, Слупецкаго уѣзда,': 'in the Kalisz governorate, Słupca district,',
    'Пыздрскаго округа въ гминѣ Тромбчинъ.': 'Pyzdry circuit, in the commune of Trąbczyn.',
    'округа въ гминѣ Тромбчинъ.': 'circuit, in the commune of Trąbczyn.',
    'Селеніе находится въ первомъ изъ отдѣловъ, установленныхъ статьею 21-ю Указа 19 Февраля (2 Марта) 1864 года о Ликвидаціонной Коммиссіи.':
        'The village is in the first of the classes set by article 21 of the Ukase of 19 February (2 March) 1864 on the Liquidation Commission.',
    'Вѣдомства Калишской Коммиссіи по крестьянскимъ дѣламъ.': 'Under the Kalisz Commission for Peasant Affairs.',
    # rows of text in the tables
    'I. Усадьбы подходящія подъ дѣйствіе Указовъ 26 Мая (7 Іюня) 1846 и 19 Февраля (2 Марта) 1864.':
        'I. Farmsteads coming under the Ukases of 26 May (7 June) 1846 and 19 February (2 March) 1864.',
    'I. Усадьбы подходящія подъ дѣйствіе Указовъ 26 Мая (7 Іюня) 1846 г. и 19 Февраля (2 Марта) 1864 года.':
        'I. Farmsteads coming under the Ukases of 26 May (7 June) 1846 and 19 February (2 March) 1864.',
    'II. Усадьбы подходящія подъ дѣйствіе Указовъ 19 Февраля (2 Марта) 1864 г. Усадьбы и земли общественныя.':
        'II. Farmsteads coming under the Ukases of 19 February (2 March) 1864. Common farmsteads and land.',
    'II. Отдѣлъ': 'Part II', 'транспортъ': 'carried forward',
    'Усадьба сельской школы': 'Farmstead of the village school', 'Общественное кладбище': 'Common cemetery',
    'Участокъ общественной земли': 'Plot of common land', 'Уч. общественной земли': 'Plot of common land',
    'Солтыскій участокъ': "The village headman's plot", 'Участокъ Солтыскаго': "The village headman's plot",
    'Участокъ солтыса': "The village headman's plot", 'Подъ дорогами': 'Under roads',
    'Итого': 'Total', 'Итого по I и II Отдѣламъ': 'Total of parts I and II',
    'Сельская школа': 'Village school', 'Неудобной земли': 'Unusable land', 'Всего': 'In all',
    'Виды и размѣры сервитутовъ, состоящихъ въ пользованіи крестьянъ. Примѣчанія.': _SERV,
    # copy A, the approval of 1868
    '1868 года 8 Февраля состоящая при Учредительномъ Комитетѣ Центральная по крестьянскимъ дѣламъ Коммиссія постановила:':
        'On 8 February 1868 the Central Commission for Peasant Affairs attached to the Constituent Committee resolved:',
    'сію разсмотрѣнную и исправленную ликвидаціонную табель, по которой въ собственность крестьянъ Селенія Лазинской':
        'this liquidation table, examined and corrected, under which there pass into the ownership of the peasants of the village of the Łazińsk',
    'Колоніи поступаетъ земли удобной одна тысяча шестьсотъ восемьдесятъ одинъ моргъ двѣсти девяносто пять прентовъ (1681 мор.':
        'Colony one thousand six hundred and eighty-one Morgen two hundred and ninety-five rods of usable land (1681 Morgen',
    '295 пр.) неудобной девять морговъ двѣсти двадцать четыре прента (9 мор. 224 пр.) а всего одна тысяча шестьсотъ девяносто одинъ':
        '295 rods), nine Morgen two hundred and twenty-four rods of unusable (9 Morgen 224 rods), and in all one thousand six hundred and ninety-one',
    'моргъ двѣсти девятнадцать прентовъ (1691 мор. 219 прен.) утвердить, опредѣливъ въ пользу бывшаго владѣльца селенія ликвида-':
        'Morgen two hundred and nineteen rods (1691 Morgen 219 rods), to be confirmed, fixing for the former owner of the village a liquida-',
    'ціонный капиталъ въ десять тысячъ пятьдесятъ пять руб. семьдесятъ коп. (10055 руб. 70 коп.)':
        'tion capital of ten thousand and fifty-five roubles seventy kopecks (10055 roubles 70 kopecks).',
    'Подлинную подписали Предсѣдательствующій и Члены Центральной Коммиссіи.—':
        'The original was signed by the presiding member and the members of the Central Commission.',
    '603 34 20/6': '603 34 20/6', '10055 70': '10055 70',
    # copy B
    'Сервитуты.': 'Servitudes.',
    'Всѣ крестьяне сел. Лазинскіе Голендры имѣютъ право:': 'All the peasants of the village of the Łazińsk Hollanders have the right:',
    '1) Пасти весь свой наличный скотъ въ лѣсу „Студзіанка"': '1) to graze all the cattle they have in the forest "Studzianka";',
    '2) Собирать въ томъ же лѣсу два раза въ недѣлю сбиранину состоящую изъ лежанины и сухихъ вѣтвей.':
        '2) to gather in the same forest twice a week fallen wood consisting of lying wood and dry branches.',
    'Собранное уносить плахтами. Болѣе никакихъ правъ на сервитуты крестьяне не имѣютъ.':
        'What is gathered they carry away in sheet-loads. The peasants have no other rights to servitudes whatever.',
    '1868 года 8 Февраля состоящая при Учредительномъ Комитетѣ Центральная по крестьян-':
        'On 8 February 1868 the Central Commission for Peasant',
    'скимъ дѣламъ Коммиссія постановила: сію разсмотрѣнную и исправленную ликвидаціонную':
        'Affairs attached to the Constituent Committee resolved: this liquidation table, examined and corrected,',
    'табель, по которой въ собственность крестьянъ Колоніи Лазинской поступаетъ земли удоб-':
        'under which there pass into the ownership of the peasants of the Łazińsk Colony, of usa-',
    'ной одна тысяча шестьсотъ восемьдесятъ одинъ моргъ двѣсти девяносто пять прен-':
        'ble land, one thousand six hundred and eighty-one Morgen two hundred and ninety-five rods',
    '(1681 мор. 295 пр.) неудобной девять морговъ двѣсти двадцать четыре пр. (9 мор. 224 пр.)':
        '(1681 Morgen 295 rods), of unusable nine Morgen two hundred and twenty-four rods (9 Morgen 224 rods),',
    'а всего одна тысяча шестьсотъ девяносто одинъ моргъ двѣсти девятнадцать':
        'and in all one thousand six hundred and ninety-one Morgen two hundred and nineteen',
    'пр. (1691 мор. 219 пр.) утвердить, опредѣливъ въ пользу бывшаго владѣльца селенія ликви-':
        'rods (1691 Morgen 219 rods), to be confirmed, fixing for the former owner of the village a liqui-',
    'даціонный капиталъ въ десять тысячъ пятьдесятъ пять руб. семьдесятъ коп. (10,055 руб. 70 к.':
        'dation capital of ten thousand and fifty-five roubles seventy kopecks (10,055 roubles 70 kopecks).',
    'Подлинное за надлежащимъ подписомъ.—': 'The original bears the proper signature.',
    'На основаніи 56 ст. Указа 19 Февраля (2 Марта) 1864 года, о порядкѣ введенія':
        'On the basis of article 56 of the Ukase of 19 February (2 March) 1864 on the manner of bringing',
    'въ дѣйствіе новыхъ о крестьянахъ постановленій, сія Копія съ окончательно':
        'into force the new regulations on the peasants, this copy of the finally',
    'утвержденной ликвидаціонной табели на Кол. Лозинскую списана въ Ка-':
        'confirmed liquidation table for the Łozińsk Colony was copied at the Ka-',
    'лишской Коммиссіи по крестьянскимъ дѣламъ для храненія въ Губернскомъ':
        'lisz Commission for Peasant Affairs, to be kept at the Governorate',
    'Правленіи. Г. Калишъ 10 Сентября 1869 г.': 'Government. Kalisz, 10 September 1869.',
    '[Предсѣдатель?]: [?]': '[uncertain: Chairman]: [illegible]',
    'Секретарь: [Бергъ?]': 'Secretary: [uncertain: Berg]',
    # the statement
    'Вѣдомость': 'Statement',
    'о количествѣ крестьянскаго надѣла, записаннаго въ ликвидаціонной табели на селеніе „Колонія Лазинскіе Голендры", Слупецкаго уѣзда.—':
        'of the amount of the peasant allotment entered in the liquidation table for the village "Łazińsk Colony, the Łazińsk Hollanders", Słupca district.',
    'Количество надѣла [оказавшагося?] по сему измѣренію.— Десятины и сажени.': 'Amount of the allotment [uncertain: found] by this survey. Desiatins and sazhens.',
    'Подъ строеніями и огородами.': 'Under buildings and gardens.', 'Пахатной.': 'Arable.', 'Луговъ.': 'Meadow.',
    'Подъ выгономъ.': 'Under pasture.', 'Неудобной.—': 'Unusable.', 'Всего вообще.': 'In all.',
    '№ по табели.': 'No. in the table.', 'Усадьбы, поступившія въ собственность крестьянъ.—': 'Farmsteads that passed into the ownership of the peasants.',
    'Съ подлиннымъ вѣрно:': 'True to the original:',
    'Непремѣнный Членъ Присутствія, Н. [?]': 'Permanent member of the Board, N. [illegible]',
    'Секретарь А. [?]': 'Secretary A. [illegible]',
}


def translit(s):
    out = []
    for ch in s:
        low = ch.lower()
        if low in TRANS:
            t = TRANS[low]
            out.append(t[:1].upper() + t[1:] if ch != low and t else t)
        else:
            out.append(ch)
    return ''.join(out)


def doubt(s):
    s = re.sub(r'\[\?\]', '[illegible]', s)
    return re.sub(r'\[([^\[\]]+?)\?\]', r'[uncertain: \1]', s)


def name_en(s):
    if s in CELL:
        return CELL[s]
    for pat, new in WORDS:
        s = re.sub(pat, new, s)
    return doubt(translit(s))


def cell_en(s, k):
    """Cell k of a row: the name column (1) is translated or transliterated, a heading word by CELL, figures kept."""
    if not s.strip():
        return s
    if k == 1:
        return name_en(s)
    if re.search(r'[А-Яа-яѣіъ]', s):
        assert s in CELL, s
    return CELL.get(s, s)


TEXT_EN = {
 (3, '0028_a'): '''"On the basis of articles 1302 and 2800 of the Resolution of the Constituent Commi-
ttee, and by the resolution of the Kalisz Governorate Board for Peasant Affairs
of 25 February 1882, it has been determined that this inscription''',
 (3, '0030_a'): '''be entered in this table in certifi-
cation that the peasants of the vil-
lage of the Łazińsk Colony, who have
the right to the servitude of fuel in
the form set by the table,
are entitled to receive from the manor
forest "Studzianka" 104 sheet-
loads, equal to 10½ ordi-
nary two-horse peas-
ant carts, a year for
each farmstead, and that the same
farmsteads are entitled to graze in the same
tract four hundred and eight head
of horned cattle."
Town of Kalisz, March 1884.
Vice-Governor [illegible]
Councillor [illegible]
for the Senior Clerk [illegible]''',
 (4, '0031_a'): '''Copy of the inscription to be entered in
the liquidation table for the village of the colony
Łazińsk, commune of Trąbczyn, Słupca
district.
"On the basis of articles 1302 and 2800 of the resolutions of the Constituent
Committee, and by the resolution of the Kal-
isz Governorate Board for Peasant Affairs
of 12 October 1894, this in-
scription has been entered in certification that,
by a voluntary transaction of 14 June
1892, made under a resolution
of the village assembly of 14 June 1892, no. 4, and
confirmed by the Governorate Board
on 29 April 1894, the peasants of the vil-
lage of the Łazińsk colony gave up once
and for all, in favour of the owner of the estate
of Trąbczyn, Countess Maria Wielo-
polska, the rights granted by this ta-
ble to the farmsteads entered in it under
nos. 1 to 91 inclusive and under no. 96
to the servitude of pasture in
the forest called "Studzianka" and to the gath-
ering in the same forest of lying wood and
dry branches; in return for which
the farmstead holders received into full
ownership the following amount
of usable manor land: nos. 1 to 7, 9 to 13,
15 to 46, 48 to 58, 60, 62, 64, 65, 67 to 74 and 76 to 91 in-
clusive and no. 96, 4 Morgen each, which for
84 farmsteads makes 336 Morgen; nos. 8,
14, 59, 61, 63, 66 and 75, 6 Morgen each, in
all 42 Morgen, and no. 47, 5 Morgen; in all 383 Morgen,
and besides, of unusable land under roads
and boundaries, 10 Morgen 154 rods. In all,
by the transaction, there passed into the ownership
of the peasants 393 Morgen 154 rods, within the boundaries''',
 (4, '0032_a'): '''described in detail in the record of the Com-
missioner of the Słupca district of 27 and 28
June 1893, pointed out to the persons who made
the transaction, known to them and
fixed by temporary boundary
marks."
Kalisz, 10 June 1900.
The original record with the proper
signatures.
True to the original:
Permanent member
of the Board, N. [illegible]
Secretary, A. [illegible]''',
 (5, '0033_a'): '''Copy of the inscription entered in the liquidation table
for the village of the Łazińsk Colony, commune of Trąb-
czyn, Słupca district.
"On the basis of articles 1302 and 2800 of the resolutions
of the Constituent Committee, and by the resolution of the Kal-
isz Governorate Board for Peasant Affairs
of 29 November 1897, in conse-
quence of the survey made in 1896
by the surveyor [uncertain: Pelzutski], the exact extent of the whole
peasant allotment of this village, together with
the land that passed to the peasants for the forest
and pasture servitudes under the volun-
tary transaction made on 14 June 1892, the terms
of which were entered in this table by the resolu-
tion of the Governorate Board of 12 October
1894, has been determined at 1068 desiatins 1272 sazhens, of
which 1034 desiatins 2102 sazhens usable and 33 desiatins
1570 sazhens unusable; the amount of each kind of land and of the
whole land in each separate farmstead is
shown in the proper columns of the table, after the remo-
val of the former figures, which proved to be wrong."
Town of Kalisz, 14 July 1901.
The original record with the proper signatures.
True to the original:
Permanent member
of the Board, N. [illegible]
Secretary A. [illegible]''',
}
