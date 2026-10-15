# -*- coding: utf-8 -*-
"""The English of APP 53/968/0/-/716, written in session (2026-10-14).

Tables: the English table has the same rows and the same figures as the
original (publish_translations.english_table checks it); only the name
column and the words of the heading are translated. Names written in
Cyrillic in the Russian liquidation tables are transliterated letter by
letter (TRANS: the old letters ѣ, і, ъ included; the hard sign is left out),
so "Шенвальдъ Кр." is "Shenvald Kr."; the German form behind a name is not
guessed. Words in a name cell are translated (WORDS). The other cells that
hold words are translated by CELL, which must cover every one of them.

Text: TEXT_EN, page by page. A doubtful word is "[uncertain: ...]", a word
not read "[illegible]", as in the other holdings.
"""
import re

TRANS = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'і': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'iu', 'я': 'ia', 'ѣ': 'e', 'ѳ': 'f', 'ѵ': 'i', 'ѡ': 'o', 'ѫ': 'u',
}

# whole words in a name cell, before transliteration
WORDS = [
    (r'\bНасл(?:ѣд)?\.', 'heirs of'), (r'\bНас\.', 'heirs of'), (r'\bВдова\b', 'widow'), (r'\bвдова\b', 'widow'),
    (r'(\w+)\[\?\]', r'[uncertain: \1]'),   # a word read with doubt in the editor's form, "nur[?]"
    (r'\bсынъ\b', 'son'), (r'\bм\.$', 'Morgen'), (r'(?<=\d) м\.', ' Morgen'), (r'\bWdowa\b', 'Widow'),
]

CELL = {
    # doc 1
    '[7.?] 1858': '[uncertain: 7.] 1858',
    'Wykaz opłacać się mających podatków podymnych łącznie z kaszarkowym Kol. Emilienheim w dwuch równych Ratach w mies. Marcu i Wrześniu':
        'List of the hearth taxes to be paid, together with the barracks money, by the colony of Emilienheim in two equal instalments in the months of March and September',
    'Razem': 'Total',
    'Kopojno d. 3/15 Grudnia 1858 r.': 'Kopojno, 3/15 December 1858',
    'Woyt Gminy Kopojna': 'Wójt of the commune of Kopojno',
    # doc 2
    'Ликвидацiонная табель селенiя Эмилейнхаймъ (нынѣ Михаленовъ) состоящ. Калишск. губ., Слупецк. уѣз., Пыздрск. округа и гмины':
        'Liquidation table of the village of Emilienheim (now Mikhalenov), in the Kalisz governorate, Słupca district, Pyzdry circuit and commune',
    'Эмилейнхаймъ': 'Emilienheim', 'Неудобн.': 'Unusable', 'Вообще': 'In all', 'мор.': 'Morgen', 'мор. прут.': 'Morgen, rods',
    'Участокъ солтыса': "The village headman's plot", 'Школьн. усадьба': 'School farmstead', 'Кладбище': 'Cemetery',
    'Дороги': 'Roads', 'Всего 319 мор. 250 пр.': 'In all 319 Morgen 250 rods',
    'Помѣщ. 4420 р. 53 коп.': 'To the landowner 4420 roubles 53 kopecks', '28 марта 1868 г.': '28 March 1868',
    # doc 4
    'Łazińsk': 'Łazińsk',
    'Ликвидац. табель селенiя Колонiи Лазинской Кал. губ., Слупецк. уѣз. Пыздр. окр. гмин. Тромбчинъ':
        'Liquidation table of the village of the Łazińsk Colony, Kalisz governorate, Słupca district, Pyzdry circuit, commune of Trąbczyn',
    'Bleistift Jahr 1875': 'In pencil: the year 1875', 'Мор.': 'Morgen', 'пр.': 'rods',
    'Усадьба сельск. шк.': 'Farmstead of the village school', 'Кладб.': 'Cemetery',
    '— Готфр. Хауптъ 8-179': '— Gotfr. Khaupt 8-179',
    'Общественн. земля': 'Common land', 'Солтысъ': 'Village headman', 'Рейхъ Крист.': 'Reikh Krist.',
    'Подъ дорогами': 'Under roads', 'Неудоб. 9-224': 'Unusable 9-224', 'Вообще 1691 мор. 219 пр.': 'In all 1691 Morgen 219 rods',
    'Ликвид. сумма для бывшаго владѣльца 10055 р. 70 к.': 'Liquidation sum for the former owner 10055 roubles 70 kopecks',
    'Слупца 29 iюня 1868 г.': 'Słupca, 29 June 1868',
    # doc 6
    'Jahr': 'Year', 'Wirte:': 'Farmers:', 'Morgen': 'Morgen', '91 Wirte.': '91 farmers.',
    # doc 8
    '[?] von dem Orliner Hauland zu Biskupice gehörig, sämtlich au[f/s?] das [?]':
        '[illegible] belonging to the Orlin Hauland at Biskupice, all [uncertain: on/from] the [illegible]',
    'Morg.': 'Morgen', 'Zur Schule gehörig': 'Belonging to the school', 'Gemeinschaftl. Land': 'Common land',
    '27 Huf. 28 M.': '27 Hufen 28 Morgen',
    # doc 10
    'Ликвидац. табель селенiя Орлины помѣщика гр. Альбер. Тачановскаго':
        'Liquidation table of the village of Orliny, of the landowner Count Albert Taczanowski',
    'Усадьба солт.': "The village headman's farmstead", 'Вообще 850 мор. 272 пр.': 'In all 850 Morgen 272 rods',
    'Уплатить 6049 р. 89 к.': 'To be paid 6049 roubles 89 kopecks',
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
    s = re.sub(r'\[([^\[\]]+?)\?\]', r'[uncertain: \1]', s)
    return re.sub(r'(\S+?)\[\?\]', r'[uncertain: \1]', s)


def name_en(s):
    if s in CELL:
        return CELL[s]
    for pat, new in WORDS:
        s = re.sub(pat, new, s)
    return doubt(translit(s))


def cell_en(s, k):
    """Cell k of a row: the name column (1) is translated, a heading or a closing word by CELL, figures kept."""
    if not s.strip():
        return s
    if k == 1:
        return name_en(s)
    return CELL.get(s, s)


TEXT_EN = {
 (3, '5165_a1'): '''Already 26 Nov. 1870, after measurement
by the Kalisz surveyor: usable 331 Morgen 179 rods,
unusable 5 " 179 "
—o—
Kalisz governorate board renamed,
29 Sept. 1892
Emilienheim to the local
name Mikhalinova.
Entered, however, in April 1892''',
 (5, '5169_a2'): '''All the peasants of the village of the Łazińsk
Hollanders have the right:
1) to graze all their [uncertain: paleny] cattle
in the forest "Studzianki";
2) to gather in the same forest
twice a week fallen wood''',
 (5, '5170_a1'): '''consisting of lying wood
and dry branches; to carry
what is gathered away [uncertain: by tlakhty].
The peasants have no other
rights to servitudes
whatever.
—o—''',
 (6, '5170_a1'): '''Russian entry after 1875:
Morgen 1655, rods 63
farmers 94
—o—
Year from 1901: 1660 Morgen 271 rods,
91 farmers.
Year 1906: 2044 Morgen 181 rods,
91 old farmers - 21 new farmers
with 112 Morgen.''',
 (6, '5170_a2'): '''Year 1907: 91 old farmers
and 21 new farmers
Year 1914: 137 farmers,
with 2037 Morgen.''',
 (8, '5171_a1'): '''Huta Trąbczyńska
1935 - 18 farmers, 217 Morgen.''',
 (8, '5171_a2'): '''In Orlin, July 1935
85 farmers.''',
 (8, '5172_a1'): '''Livestock of Orliny. ××
152 cows
343 sheep
furshtiki 330.
1879 fuel
for the whole village 52 cartloads
1880 - 300 Morgen 97 rods
4 Morgen of waste land.
[uncertain: Bred]
forestry plan:
"Vdovii Bor, Biskupice,
Podbel, Szetlew, Grzebień,
[uncertain: Gedpar], Kreshnia."
1909 [illegible]
has [uncertain: entgekoit] that''',
 (8, '5172_a2'): '''In Józefów
[uncertain: Jäke], Becker, Wegert, Jesswein
the first farmers.
Old houses with [uncertain: L…]
gable to the street
1056 hymns
1017 hymns in the Züllichau
hymn book
—o—
Clay for Łazińsk
from Querlin
—o—
Women wear aprons
right round the body''',
 (8, '5173_a1'): '''30 years ago the
bonnets disappeared.
Bonnets were made from the
[uncertain: saddlers].
Czarny Bród,
Little Orlin, Great Orlin
Maradza,
Bystrzyca: 1 Protestant family
160 families.''',
 (8, '5173_a2'): '''In Little Orlin
1 Hufe each for 40 farmers
The old people spoke
Low German, a little
The people of Orlin abuse those of Biało¬
błoty: the stupid Kashubians
In Wielki Bór a Protestant estate
owner, Riedel. Gave Mr
Schmidt a hymn book
In Orlin post-built houses (Bloch)
—o—
Holędry Orliny Biskupicki''',
 (8, '5174_a1'): '''[uncertain: Sollten], they steal wood from one another, steal pota¬
toes, dream of stealing hens
The German fellow countrymen robbed the teacher
on [uncertain: Zrost]. In Grodziec poor,
Łazińsk not such great thieving
The more converted, the more perverted.
[uncertain: Frierk], a preacher, the sons steal.
Protestant communists, believe in nothing.
Poverty does it mostly.
They get on well with the Poles. In Białobłoty
[uncertain: Brenda] drops drunk at home.
Immorality among married men not
widespread. Many wild marriages (3-4)
[uncertain: Zogel.] children, 7 illegitimate,
otherwise also 2-3
They marry mostly to Białobłoty. Many girls
do not marry. The Poles all speak good German
No tendencies to assimilation! Political
activity not much, but they do not pay their
membership dues. The Volksverband has more influence
through the "Volksfreund" and the calendar.
Volksverband: farmers - J.D.P. - youth''',
 (8, '5174_a2'): '''Near Grodziec "Ukerlinge", "in Obory cheeky, vulgar.
After the service [uncertain: they fight] every Sunday, dance amusement
In Orlin: the praying brethren, in the village two preachers,
for 2 years Pentecostalists and Baptists.
On Saturday no carting of dung. - Camomile
flowers only on St John's night.
When a cow calves, nothing is lent, but things are borrowed.
The young, mostly girls, to the Poznań region. 50%
with big bellies. Everything goes to the pastor; lawsuits
there are some too, but they are the exception. Theft very wide¬
spread. Many who pray, but bad with it. Bad thie-''',
 (10, '5176_a1'): '''Orlin Hauland, 1 Oct. 1806
In Orlin Kashubian was spoken.
(Weber, " Bloch's father also
from Czarny Bród, spoke Kashubian
come from Orlin)
Because of the wet years in Orlin
went bankrupt.
"Kjaufft" word.''',
 (10, '5176_a2'): '''July 1936
Class I 17
II " 370
III " —
IV " 464.69
waste land 300 =
1157.69 Morgen
village of Orlino.''',
 (12, '5179_a1'): '''Great Orlin and Czarny Bród 60 years ago.
Separation.
by the number, then by
Morgen. —
Białobłoty and Little Orlin
2 years ago
by the number.''',
 (12, '5179_a2'): '''Servitude in Orlin 300 Morgen''',
 (13, '5179_a2'): '''All the farmsteads of the village of Orliny
have the right to forest and pasture
servitudes in one half of
the forest called "Velskii
Bor", adjoining the village,
namely: a) to enter the forest
every week on Saturdays to
gather fallen wood, break off
dry branches and grub up stumps.
Branches may be broken off
the trees with a [tree] hook, and in
grubbing up stumps a
[uncertain: lever] may be used. The fuel so gathered
the farmstead holders
carry away by carts, reckoning
no more than one cart to a farmstead''',
 (13, '5180_a'): '''a week; b) to receive every year
for each farmstead 1 tree for
the repair and mending of buildings.
The tree must measure, at a height
of 2 ells from the stump, 8 inches in dia¬
meter, and is given to the peasants
with its top and branches. c)
To graze their cattle, and to rake
in the months of April, May, Sep¬
tember, October and November litter
for the cattle. The number of carts
of litter and of head of cattle each
farmstead may put out to pas¬
ture is laid down by the following
list: ××''',
}
