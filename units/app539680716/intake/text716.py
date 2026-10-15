# -*- coding: utf-8 -*-
"""The reading of APP 53/968/0/-/716, made in session from the editor's photos (2026-10-14).

FRONT: the pages before the first document (the archive's title page, the
notebook's cover). DOCS: {document number: [(page id, lines)]}; a page that
carries the end of one document and the start of the next stands under both.
TABLES: the documents given as tables; their lines are rows, cells separated
by "|" here and written out as CSV by holding.py.

Conventions (EDITORIAL_RULES, and the notebooks of 53/968/0/-/669):
- "[?]" a word not read, "[word?]" a word read with doubt, "[Ab…?]" where
  only some letters are read; "¬" ends a word broken at the end of a line;
  Breyer's dividers between notes ("—o—") are kept.
- Struck-out words are left out; words written above the line are put where
  they belong; sketches are not transcribed.
- In the tables the entry's number stands first and the name second, as in
  every table of the edition, although on the loose sheet of 1858 the name
  comes first. Where the copyist wrote only the last figure of a number
  ("1", "2" for 21, 22) the number is given in full. The copyist's dash
  after a name ("Шульцъ Крист. —") is left out. A heading repeated at the
  head of a page is given once.
- In the Łazińsk table Breyer wrote in pencil, between the lines, who held
  each holding in 1875 ("Bleistift Jahr 1875" at the head): his pencil
  stands in the name cell after " — ". The figures he added in pencil stand
  there too.
"""

FRONT = [
    ('5159_a', [
        'Spuścizna Alberta Breyera',
        'Łazińsk [pow. słupecki, woj. poznańskie',
        '- notatki, statystyka]',
        '1937.',
        'Spuśc. A. Breyera',
        '716',
    ]),
    ('5162_a', [
        'Łazińsk',
        'Emilienheim',
        'Ликвидац. табель',
    ]),
]

TABLES = {1, 2, 4, 7, 9, 11}

DOCS = {
 # ---------------------------------------------------------------- 1: the loose sheet of 1858, a table
 1: [
  ('5160_a', '''|[7.?] 1858|||
|Emilienheim|||
1|Krystyan Szejnwald||1.|1-50
2|Frydrych Hintz||1.|1-50
3|Gottlieb Kunke||1.|1-50
4|Gottfried Kiwer||1.|1-50
5|Krysztof Rainisz||1.|1-50
6|Wdowa Kiepcke||1.|1-50
7|Gottlieb Szeller||1.|1-50
8|Jan Berger||1.|1-50
9|Gottfried Lieske||1.|1-50
10|Gottlieb Szeinfisz||1.|1-50
11|Gottlieb Liepelt|1-3||
12|Frydrych Fink||1.|1-50
13|Krystyan Szule||1.|1-50
14|Piotr Drezer||1.|1-50
15|Frydrych Lehmann||1.|1-50
16|Karol Reszke||1.|1-50
17|Jan Henke||1.|1-50
18|Ludwik Berger||1.|1-50
19|Krystyan Liepelt||1.|1-50
20|Michał Cygielsdorf||1.|1-50
21|Gottlieb Berger||1.|1-50
22|Daniel Krueger||1.|1-50
23|Wdowa Szurak|1-3||
||2-6.|21.|31-50
|Wykaz opłacać się mających podatków podymnych łącznie z kaszarkowym Kol. Emilienheim w dwuch równych Ratach w mies. Marcu i Wrześniu|||'''),
  ('5161_a', '''|Emilienheim|2-6|21|31-50
24|Frydrych Kincel||1.|1-50
25|Andrzey Pahl||1.|1-50
26|Frydrych Dykhof||1.|1-50
27|Krystyan Sztelier||1.|1-50
28|Krystyan Szulc||1.|1-50
|Razem|2-6|26|39-
29|Gottlieb Dykhof||1.|1-50
||2-6|27|40-50
|Kopojno d. 3/15 Grudnia 1858 r.|||
|Woyt Gminy Kopojna|||'''),
 ],
 # ---------------------------------------------------------------- 2: Emilienheim, the liquidation table of 1868, a table
 2: [
  ('5163_a2', '''|Ликвидацiонная табель селенiя Эмилейнхаймъ (нынѣ Михаленовъ) состоящ. Калишск. губ., Слупецк. уѣз., Пыздрск. округа и гмины||
|Эмилейнхаймъ|Неудобн.|Вообще
||мор.|мор. прут.
1|Шенвальдъ Кр.|6|17-71
2|Гинцъ Фрид.||6-177
3|Кунке Готл.|6|6-66
4|Бергеръ Фр.|12|11-120
5|Reinisch Krist.|5|9-174
6|Schultz Krist.|6|5-114
7|Schmidt Dan.|–|4-19
8|Berger Joh.|–|9-97
9|Liske Gottfr.|11|15-93
10|Schönfisch Gottl.|5|12-247'''),
  ('5164_a1', '''11|Цигельсдорфъ [Мар.?]|24|22-187
12|Финкъ Фр.|31|12-113
13|Бочинскій Вильг.||4-44
14|Шульцъ Готфр.|41|30-182
15|Дрешеръ Петръ|5|8-174
16|Лемманъ Фр.|37|20-37
17|Цигельсдорфъ Вильг.|18|4-173
18|Генке Янъ|7|13-53
20|Насл. Бергера Люд.|23|13-96
21|Липельдъ Крист.|7|11-207
22|Бергеръ Готл.|5|10-217
23|Кригеръ Даніилъ|11|10-94
24|Шурекъ Авг.|–|16-79
25|Кинцель Фр.|–|6-40
26|Дикгофъ Готл.|33|4-283'''),
  ('5164_a2', '''27|Диконфъ Готфр.||3-74
28|Штейнбартъ Мих.||5-90
29|Штильцеръ Крис.||3-120
30|Леманъ Фр.||3-150
31|Цильке Мих.||3-150
32|Шмидтъ Готфр.||2-
33|Эссе Мих.||3-150
34|Штрезе Янъ||3-
35|Шейнфишъ Авг.||2-138
36|Нейманъ Людв.||4-205
|Участокъ солтыса||2-257
|Школьн. усадьба||7-116
|Кладбище||–198
|Дороги||3-288
|Всего 319 мор. 250 пр.||
|Помѣщ. 4420 р. 53 коп.||
|28 марта 1868 г.||'''),
 ],
 # ---------------------------------------------------------------- 3: notes on Emilienheim, 1870 and 1892
 3: [
  ('5165_a1', '''Bereits 26 Nov. 1870 nach Messung
d. Geom. Kal. удобной 331 мор. 179 пр.
неудобной 5 " 179 "
—o—
Калишск. губ. присутствiе переименов.
29 сент. 1892
Эмилейнхаймъ на мѣстное
назв. Михалинова.
Eingeschrieben jedoch i. April 1892'''),
 ],
 # ---------------------------------------------------------------- 4: Łazińsk, the liquidation table of 1868, a table
 4: [
  ('5165_a1', '''|Łazińsk||
|Ликвидац. табель селенiя Колонiи Лазинской Кал. губ., Слупецк. уѣз. Пыздр. окр. гмин. Тромбчинъ||'''),
  ('5165_a2', '''|Bleistift Jahr 1875|Мор.|пр.
1|Кончинскій Яковъ|17|84
2|Гебель Март. — Войц. Рунга|29|262
3|Мерцъ Карлъ — Авг.|48|56
4|Холмъ Дан. — Эрнстъ 26-161; Авг. Холмъ 14|40|161
5|Мерцъ Готл.|7|289
6|Гиршъ Крист. — Вильг. Холмъ|17|233
7|Кинастъ Вил.|15|112
8|Стржижиковскій Фр.|11|148
9|Саниковскій Марцинъ — Іосифъ Вавржинякъ|19|22
10|Марекъ Вильг. — Мерцъ|32|179
11|Грунвальдъ Крист.|22|273
12|Сливинскій Готл. — Готл. Кинастъ|14|122
13|Штейнбордъ Юл.|17|75
14|Холмъ Вильг. — [Брушк.?] Клиге|13|280
15|Фалькъ Авг.|5|15'''),
  ('5166_a1', '''16|Мерцъ Крист. — Кар. 16-125|23|125
17|Мерцъ Марцинъ — Крист.|8|293
18|Саниковскій Осипъ — [Франц.?]|27|244
19|Стирценбехеръ Крис.|15|24
20|Саниковскій Иванъ — nur[?] 14; 10 м.|24|187
21|Насл. Госке Карла|25|129
22|Блудзинскій Ив. — Дан. Кинастъ|9|294
23|Шмигельскій Вильг. — 31-70; 18 Карлъ Морицъ|49|70
24|Насл. Рогацкаго Петра — Пав. 15; Вдова Рогацк. 15|30|235
25|Промистъ Щепанъ|13|87
26|Рунга Войцѣхъ — nur[?] 18; Рунга Войц. 18|36|222
27|Насл. Рунга Готфр.|18|65
28|Фалькенбергъ Марцинъ|41|94
29|Госка Осипъ — + 3 м.|15|188
30|Шульцъ Крист.|7|196'''),
  ('5166_a2', '''31|Кнафкусъ Вильг. — Готл.|1|196
32|Насл. Рунге Войц. — Готл.|5|135
33|" Рунге Готфр. — Крист. Шейнфишъ|26|45
34|Рунге Март.|2|115
35|Китке Кристіянъ — Адлеръ Вильг.|6|46
36|Фриденбергъ Кристофъ — Эд. [Бромке?]|19|220
37|Цельмеръ Готф. — Шульцъ Фрид.|26|14
38|Малиновскій Петръ — + 7|5|277
39|Хауптъ Францъ — Крист. сынъ; + 2 м.|13|174
40|Швебсъ Кар. — Сам. Штильцеръ|4|168
41|Штирценбехеръ Кар.|8|45
42|Насл. Бетке Кристіян.|8|192
43|Кинастъ Матеушъ — Готфр.|3|248
44|Рашъ Фрид. Иванъ|53|196
45|Бандзертъ Эман.|4|48'''),
  ('5167_a1', '''46|Кунъ Готфр.|38|66
47|Зееръ Крист. — Ив. Генке 29; [Геп.?] Зееръ 13|42|99
48|Бандзертъ Морицъ — Дан. Зееръ|36|135
49|Мерцъ Авг.|33|93
50|Цельмеръ Генр.|35|42
51|Гебель Карл. — Кр. Гиршъ|14|105
52|Шмигельскій Сам. — Кар. Холмъ|14|13
53|Нас. Цельмера Дан. — Авг. Шмигель|12|60
54|Битнеръ Андр. — Вил. Ковальски|30|115
55|Рытамеръ Антон. — Готфр.|13|142
56|Пржистанскій Ант.|5|59
57|Бартель Карл. Людв. — Вильг.|6|68
58|Госке Войцѣхъ|16|147
59|Гинцъ Людв. — 39-245|16|287
60|Штаркъ Даніилъ|8|157'''),
  ('5167_a2', '''61|Кинастъ Войц. — Вдова|52|94
62|Кусманъ Готл.|2|66
63|Нас. Кинаста Войц. — Готф.|15|192
64|Герке Готфр.|5|277
65|Цельмеръ Мих. — Готф.|36|254
66|Штаркъ Авг. — Вдова|18|241
67|Цельмеръ Авг.|22|227
68|Липельтъ Марцинъ — Генр. Рунга|14|121
69|Готтеръ Авг. — Кар. [Пашка?]|19|64
70|Морицъ Готфр. — Вдова|54|292
71|Обстъ Вильг. — 2 ×|5|272
72|Рейхъ Кристіянъ|28|297
73|Швебсъ Иванъ — Эрн. [Торно?]|12|221
74|Хауптъ Готл. — Ферд. Шмехель|8|124
75|Хауптъ Готфр.|31|98'''),
  ('5169_a1', '''76|Хауптъ Кристьянъ Кристьяновъ|13|33
77|Хауптъ Готфридовъ Кристіянъ|12|48
78|Зельчакъ Фома — Вдова|6|104
79|Щепинскій Петръ|5|255
80|Фогель Вильг. — ?|2|214
81|Шейнфишъ Вильг.|54|218
82|Рогацкій Станисл.|16|269
83|Феттеръ Ив. — Готл. Рыбицкій|2|206
84|Штирценбехеръ Ив.|5|30
85|Кинастъ Кристіянъ — Кристь. Шейнфишъ|2|12
86|Хауптъ Готфр. — Фр. Гиршъ|4|37
86|Хауптъ Вильг. — 2|14|179
87|Германъ Войцѣхъ — 2|1|288
88|Нас. Тарновскаго Мих. — Готтлибъ Готл.|2|30
89|Роговичъ Марцинъ — [Бонцлеръ?]|–|193
90|Марыльскій Ив.|5|98
|Усадьба сельск. шк.|20|218
|Кладб.|2|282
|— Готфр. Хауптъ 8-179||'''),
  ('5169_a2', '''|Общественн. земля|1|89
|Солтысъ|2|263
|Рейхъ Крист.|1|–
|Подъ дорогами|6|242
|Неудоб. 9-224||
|Вообще 1691 мор. 219 пр.||
|Ликвид. сумма для бывшаго владѣльца 10055 р. 70 к.||
|Слупца 29 iюня 1868 г.||'''),
 ],
 # ---------------------------------------------------------------- 5: Łazińsk, the servitudes (Breyer's copy)
 5: [
  ('5169_a2', '''Всѣ крестьяне селенiя Лазинскiй
Голендры имѣютъ право:
1) пасти весь свой наличный скотъ
въ лѣсу „Студзiанки"
2) собирать въ томъ же лѣсу
два раза въ недѣлю сбиранину'''),
  ('5170_a1', '''состоящую изъ лежанины
и сухихъ вѣтвей; собранное
уносить тлахтами.
Болѣе никакихъ правъ на
сервитуты крестьяне не
имѣютъ.
—o—'''),
 ],
 # ---------------------------------------------------------------- 6: Łazińsk, Breyer's counts of farmers and land, 1875 to 1914
 6: [
  ('5170_a1', '''Rus. Eintragung nach 1875
Morgen 1655 Rut. 63
Wirte 94
—o—
Jahr v. 1901 1660 M. 271 Rut.
91 Wirte.
Jahr 1906 2044 Mor. 181 Rut.
91 alte Wirte - 21 neue Wirte
mit 112 Mor.'''),
  ('5170_a2', '''Jahr 1907 91 alte Wirte
und 21 neue Wirte
Jahr 1914. 137 Wirte,
bei 2037 Morg.'''),
 ],
 # ---------------------------------------------------------------- 7: Łazińsk, farmers and Morgen 1840 to 1935, a table
 7: [
  ('5170_a2', '''Jahr|Wirte:|Morgen
1840|87|1368
1868|91 Wirte.|1691
1875|93|1691
1890|94|1655
1895|96|1657
1901|97|1660
1906|112|2044
1914|137|2037
1935|146|1996'''),
 ],
 # ---------------------------------------------------------------- 8: notes of 1935: Huta, Orlin, Józefów, Obory
 8: [
  ('5171_a1', '''Huta Trąbczyńska
1935 - 18 Wirte 217 Morg.'''),
  ('5171_a2', '''In Orlin i. 7. 1935
85 Wirte.'''),
  ('5172_a1', '''Скотъ Орлины. ××
152 коровъ
343 овецъ
фурштики 330.
1879 Brennmaterial
für ganze Dorf 52 Fuhr
1880 - 300 мор. 97 пр.
4 морги неужит.
[Гредъ?]
лѣсохозяйств. планъ:
„Велькiй боръ, Бискупице,
Подбель, Шетлевъ, Гржебень,
[Гедпаръ?], Крешня."
1909 9 Nov.
hat das aufgehört'''),
  ('5172_a2', '''In Józefów
[Jäke?], Becker, Wegert, Jesswein
die ersten Wirte.
Alte Häuser mit d.
Giebel z. Strasse
1056 Liede
1017 Lieder i. Züllichauer
Gesang
—o—
Lehm nach Łazińsk
aus Querlin
—o—
Frauen trage Schürzen
rund um den Körper'''),
  ('5173_a1', '''Vor 30 Jahren die
Hauben verschwunden.
Von den […etli…?] machten
man Hauben.
Czarny Bród,
Kl. Orlin, Gr. Orlin
Maradza,
Bystrzyca 1 ev. Fam
160 Fam.'''),
  ('5173_a2', '''In Klein - Orlin
je 1 Hufe an 40 Wirte
Die Alten sprachen
plattdeutsch, etwas
Die Orliner schimpfen die Biało¬
bloter: die dummen Kaschuben
In Wielki Bór ein evang. Guts¬
besitzer Riedel. Schenkte d. Herrn
Schmidt ein Gesangbuch
In Orlin Ständerhäuse (Bloch)
—o—
Holędry Orliny Biskupicki'''),
  ('5174_a1', '''[Solten?], stehlen einander Holz, stehlen Kar¬
toffeln, träumen Hühnerstehlen
Den Lehrer haben d. dt. Volksgenossen
auf [Zrost?], bestohlen. In Grodziec arm
Łazińsk nicht so grosse Dieberei
Je bekehrter, desto verkehrter.
[Frierk?], ein Prediger, die Söhne stehlen.
Evang. Kommunisten, glauben an nichts.
Die Armut macht es meist.
Mit Polen kommen gut aus. In Białoblot
Brenda Tropfen zu Hause getrunken.
Die Unmoral bei verheirateten Männer nicht
verbreitet. Viel wilde Ehen (3-4)
[Zoget.?] Kinder 7 uneheliche
sonst auch 2-3
Heiraten meisten nach Białobłoty. Viele Mädel
heiraten nicht. Die Polen sprechen alle gut deutsch
Keine Assimilationstendenzen! Politische Tätig¬
keit nicht besonders, aber Mitgliedsbeiträge zah¬
len sie nicht. Volksverband hat mehr Einfluss
durch d. „Volksfreund" u. d. Kalender.
Volksverband: Wirte - J.D.P. - Jugend'''),
  ('5174_a2', '''Bei Grodziec „Ukerlinge" „in Obory frech, gemein.
Nach dem Gottesdienst schlagen sich jeden Sonntag Tanzvergnügung
In Orlin: die Betbrüder, im Dorfe zwei Prediger,
seit 2 Jahren Pfingstler u. Baptisten.
Am Sonnabend kein Dung fahren. - Kamillen¬
blüten nur in d. Johannisnacht.
Wenn eine Kuh kalbt, wird nicht verborgt, aber geborgt.
Jugend meist Mädchen ins Posenschen. 50%
mit dicken Bäuchen. Alles geht zum Pastor, Prozesse
sind auch etliche, aber Ausnahme. Diebstahl sehr verbrei¬
tet. Viel Beter, aber schlecht dabei. Schlechte Diebs-'''),
 ],
 # ---------------------------------------------------------------- 9: Orlin, the farmers and their Morgen, a table
 9: [
  ('5174_a2', '''|[?] von dem Orliner Hauland zu Biskupice gehörig, sämtlich au[f/s?] das [?]|
||Morg.
1|Bloch|18
2|Schmidt P.|15
3|Kuske|28
4|Büch|22
5|Ullrich|29
6|Kasner Mar.|14
7|" Joh|22
8|Ludewig|14
9|Hermann|17
10|Bischof|9'''),
  ('5175_a1', '''11|Frank|17
12|Stefan|18
13|Kolański|43
14|Skrzydlewski Fr.|28
15|Zur Schule gehörig|15
16|Zobel|33
17|Baumann|15
18|Borowski|22
19|Ratsch|7
20|Kientopf|28
21|Schiller|34
22|Gemeinschaftl. Land|34
23|[Crist.?] Kasner|17
24|Gottfr. "|17
25|Gottfr. M.|16'''),
  ('5175_a2', '''26|Kaźmierczak|12
28|Gallas|15
29|Kientopf|32
30|Wieczorek|11
31|Tilson|7
32|Gierke|9
33|Chmielowski|4
34|Silberman|23
35|Krisiak|22
36|Miszkiewicz|7
37|Hoffmann|14
|Ziebart|7
|Zielke|4
|Pelz|15
|Lehman|7'''),
  ('5176_a1', '''|Neumann|10
|Galant|16
|Seling|7
|Polzfu[h?]l|18
|[Jaschek?]|15
|Kress|36
|27 Huf. 28 M.|'''),
 ],
 # ---------------------------------------------------------------- 10: notes on Orlin, 1936
 10: [
  ('5176_a1', '''Orlin Hauland 1 Okt. 1806
In Orlin wurde Kaschubisch gesprochen.
(Weber, „ Der Vater d. Bloch hat auch
aus Czarny Bród, Kasub. gesprochen
stammen aus Orlin)
Der nassen Jahre wegen i. Orlin
Bankrott geworden.
„Kjaufft"-Wort.'''),
  ('5176_a2', '''7. 1936
I. Kl. 17
II. " 370
III. " —
IV. " 464,69
nieużytki 300 =
1157,69 morgen
wieś Orlino.'''),
 ],
 # ---------------------------------------------------------------- 11: Orlin, the liquidation table, a table
 11: [
  ('5177_a1', '''|Ликвидац. табель селенiя Орлины помѣщика гр. Альбер. Тачановскаго|
1|Цессъ Фома|10-245
2|Куске Людов.|37-201
3|Вольтеръ Богумилъ|15-
4|Фицнеръ Иванъ|22
5|Колодзинскій Лавр.|31
6|Рецлавъ Богусл.|15
7|Вишневскій Осипъ|22
8|Студзенка Осип.|
9|Педа Богумилъ|15
10|Юркевичъ Авг.|15
11|Юрихъ Густ.|
12|[Ланитцъ?] Ад.|'''),
  ('5177_a2', '''||2 49.
13|Цебель Андр.|11
14|" Мих.|25
15|Берка Готл.|25
16|[Гралька?] Войц.|40
17|Гаде Андр.|22
18|Хухъ Ант.|30
19|" Ив.|48
20|Вангольдъ Готл.|15
21|Тухолька Андр.|14
22|Шиллеръ Люд.|15
23|[Веречъ?] Мат.|20
24|Рейманъ М.|17
25|[Дайгеръ?] Мар.|12
26|Гессе Готл.|17
27|" вдова|12'''),
  ('5178_a1', '''28|Гессе Андр.|25
29|Шилькe Андр. Дан.|18
30|Зандекъ Ив.|15
31|Янке [Ш.?]|7
32|Мартинъ Ив.|16
33|Кроль Дан.|7
34|Шмидтъ Готл.|7
35|Вартке Крис.|11
36|Арендтъ Готл.|16
37|Мартинъ Ив.|16
38|Оттъ Ив.|16
39|Гауптеръ Крист.|4
40|Нас. Яна [Куркина?]|4
41|Шмидтке Фрид.|16
42|[Шпицеръ?] Дан.|18
43|Бернгард. Мих.|='''),
  ('5178_a2', '''44|Грегеръ Готл.|4
45|Rosentreter Фрид.|8
46|Дрешеръ Фр.|7
47|Бетке Мих.|22
48|Грегеръ Войц.|11
49|Розентретеръ|15
50|Гезе Ив.|—
51|Шульцъ Авг.|7
52|[Шиммеръ?] Леоп.|12
53|Грегеръ Авг.|15'''),
  ('5179_a1', '''54|Бергольдъ Готл.|15
55|Кассе Ив.|9
56|Берминскій Войц.|3
57|Наслѣд. [Курвина?]|3
|Усадьба солт.|4
|Вообще 850 мор. 272 пр.|
|Уплатить 6049 р. 89 к.|'''),
 ],
 # ---------------------------------------------------------------- 12: Orlin: Breyer's notes on the separation
 12: [
  ('5179_a1', '''Gross-Orlin u. Czarny Bród vor 60 Jahr.
Separat.
nach d. Nummer, dann nach
Morgen. —
Białoblot i Kl. Orlin
vor 2 Jahren
nach der Nummer.'''),
  ('5179_a2', '''Servitut i. Orlin 300 Mor'''),
 ],
 # ---------------------------------------------------------------- 13: Orliny, the servitudes (Breyer's copy)
 13: [
  ('5179_a2', '''Всѣ усадьбы селенiя Орлины
имѣютъ право на лѣсныя и пастбищ¬
ныя сервитуты въ половинѣ
лѣса называемаго „Вельскій
Боръ" прилегающаго къ селенiю
а именно: а) Входить въ лѣсъ
еженедѣльно по субботамъ для
собиранiя лежанины, ломанiя
сухихъ вѣтвей и корчеванiя пней.
Вѣтви дозволяется ломать съ
деревъ съ дерев. крюкомъ а при
корчеванiи пней употреблять
[топоръ?]. Собранный такимъ образомъ
матерiялъ для топлива усадеб¬
ники увозятъ фурами, считая
на усадьбу не болѣе одной фуры'''),
  ('5180_a', '''въ недѣлю б) получать ежегодно
на каждую усадьбу по 1 дереву на
поправку и починку строенiй.
Дерево должно имѣть по высотѣ
2 локтей отъ пня 8 цолей въ дiа¬
метрѣ и выдается крестьянамъ
съ вершиной и вѣтвями. в)
Пасти свой скотъ и сгребать
въ мѣсяцахъ: апрѣлѣ, маѣ, Сен¬
тябрѣ, октябрѣ и ноябрѣ стилку
для скота. Количество фуръ
стилки и головъ скота дозволяется
каждой усадьбѣ выпускать на паст¬
бище, опредѣляется по нижеслѣдующей
вѣдомости: ××'''),
 ],
}
