# -*- coding: utf-8 -*-
"""Document 2 of APP 53/968/0/-/669: Albert Breyer's notebook "V. Grodziec Juli 1936".

Added at the editor's request on 2026-10-14, from their raw photos IMG_5192
to IMG_5205 (photos.py makes the page images from them). A grey-blue exercise
book, pencil, mostly in Latin script; one page (5199_a1) and two lines of
5203_a1 in Kurrent. Despite the "Grodziec" on its cover it is about Łazińsk
and its neighbours: Włodzimierów, Emilienheim, Augustynów, Obory,
Kazimierka, Józefów, Białobłoty.

Pages. The photo number and the side: 5192_a the cover alone; 5193_a2 to
5205_a1 the written pages. The two inside covers, 5193_a1 and 5205_a2, are
blank and are not pages of the edition (the rule for openings with one blank
side). IMG_5205 is the opening of the last page and the inside back cover;
the editor asked for it turned: the camera recorded it as turned (EXIF
orientation 6), and photos.py takes the unturned preview, which is upright.

The reading (2026-10-14) was made in the session from the photos, each page
in three strips at about four times the size, under the same rules as
document 1 (holding.py). The editor's "Breyer Notes.md" in the scans folder
is a partial English rendering of this notebook; it was read after the
reading was made, and the two agree where both have a passage.
"""

FOLDS2 = {5193: 1481, 5194: 1405, 5195: 1454, 5196: 1456, 5197: 1388, 5198: 1472, 5199: 1399, 5200: 1372,
          5201: 1386, 5202: 1396, 5203: 1333, 5204: 1354, 5205: 1420}
BLANK2 = {'5193_a1', '5205_a2'}
PAGE_IDS2 = ['5192_a'] + [pid for n in sorted(FOLDS2) for pid in ('%d_a1' % n, '%d_a2' % n) if pid not in BLANK2]

TEXT2 = {
 '5192_a': """V. Grodziec
Juli 1936""",
 '5193_a2': """Łazinsk
Vor 65 Jahren
im März, sehr viele
nach Russland.
Ein Monat gewandert,
wenn es gut war.
(Maas, Merk, Munker
Lieske,
vor 46 Jahre ein
Lieske weggezogen,
hat hier Geld.
Kurz vor d. Kriege sind
auch Wolhyn. zurückgek.""",
 '5194_a1': """haben den Wald dort
ausgerodet, die [?]
haben dann [?]
[?], sind zurück¬
gekommen (Hom, Liske)
Łazinsker Lehm¬
kaite[r/n?], alle nehmen
Lehm.
—o—
Augustenhoff
Augustynow u. Emilien¬
heim zusammengegründet,
gehen d. Kinder zur Schule
nach Emilienheim""",
 '5194_a2': """Nach Włodzimierow.
Włodzimierow parzeliert
fast alles Deutsche.
Parzeliert Włodzimierow
vor 25 Jahre vom Gute Tramb¬
czyn, Besitzer hiess: Graf
Miączyński.
Gleich ausgezahlt.
Restgut hatte an 60 Morgen.
Jesse kam aus Białobłoty.
Die anderen aus dieser Gegend.
—o—
In Łazinsk ist Schwind¬
sucht verbreitet. Doktor Brede
in Zagórów wundert sich da¬
rüber; er meint, in dieser Gegend""",
 '5195_a1': """[Tür?]ver¬
zierung
—o—
Haus
Emilienheim
dürfte doch keine Schwind¬
sucht herrschen.""",
 '5195_a2': """In Łazinsk
mächtige parabolische
Dünen
Die erste bei Emilienheim
" zweite bei Łazinsk.
Wiesen
u. Wasserlöcher
[Grenzwald?]
Schule
bei""",
 '5196_a1': """Gottesdienst i. Łazinsk.
Eigentümlichkeiten:
Bei dem allgemeinen Gebet
kniet die Gemeinde.
Beim letzten Vers des letzten
Liedes stehen alle auf.
—o—
Bei 40 Jahre als Wło¬
dzimierzow entstand
von Trąbczyn aus
—o—
Wo die Kanzlei steht
u. der Pole Ankowiak
(5 Morg) gehörten
zu Grabina""",
 '5196_a2': """Neu angesiedelt auf
Waldland rechts der
Strasse die Deutschen
Bochenski 20 M., Kinast, Winterfeld, Neihe[?]
Retzläff, ein Pole, Schwarz
Lipelt, Schmechel.
Das Land war Wald, der
gehörte zum Gute Trombczyn
Den Wald u. a. der Boden
kaufte ein Jude; 5–6 Jahre
vor dem Kriege an Deutsche
abverkauft. Die Neusiedl.
heisst Trompczyn D.""",
 '5197_a1': """Obory
Kazimierka
Józefów
„Oberscher"
„Kirschhacker"
hie = hier
do = dort
Sünde
„Ich will Häfer keipen,
Kavaliere = Prietzer
Kuchen zum Fleisch
Mit d. Vieh u. den Hunden
zur Hochzeit getanzt.""",
 '5197_a2': """Herzfeld b. Berlin
Robert Nintz[?],
[?]
hat dort geheir.
Merk, Bruders
4 Kinder [Kin…?]
Herzfeld
auch Arbeiter.
Merk
Gustav Stark
Ziegelstreicher
Herzfelde.
Der Bruder
G. Merk hat
hier 10 Morgen
verkauft
hat gekauft i. Brudzewo
bei Strzałkowo; jetzt i. Pommer¬
ellen 48 Morg. gutes Land
Bukowiec bei Jabłonowo
Kr. Brodnica
Um 1830 kamen auch noch
einzelne nach Łazinsk.
Merk hat 53 Jahre, ge¬
denkt die russ. Auswand.
nicht. Des Vaters Bruder Daniel
kam vor d. Kriege zu Besuch
nach Łazinsk""",
 '5198_a1': """Ein Janke war 30 Jahre i.
Wolhynien ist doch zurück
gekommen, hier gestorben.
Arm hingezogen, arm zurück
gekommen.
Amerikaner: Ed. Buch 4 M.
Weber, Kr. Bauch 10 M.
Kolonisationskommission
Sind viele weggezogen,
Bauch aus Obory,
Merk —
Deckert,
Haben gutes, drainiertes
Land bekommen.
In Ostfelde Wrześ. die Deutschen
aus Łazinsk von d. Polen
runtergejagt, paar Groschen
bezahlt.""",
 '5198_a2': """Wurmbusch Mainitz
Kr. Wreschen Kr. Wreschen
—o—
Koppen — Garbenhaufen
In Łazinsk stellenweise
schöner Weizen
—o—
Es gibt auf [Rhein…?]
im Dorfe?
Ein altes Paar liegt im Winter
„mich angegrölt" — angeschrien. unbeweglich
Es wurden Kartoffeln gestoh¬
len, aus Gutmütigkeit. —
—o—
Geschlechtliche Krankheiten
nicht vorhanden.""",
 '5199_a1': """Uneheliche Kinder
viel.
Fru[c?]ksucht auf [Wanderschaft?],
[stärker?] Sommerarbeit
auf früheren [Gottmanns?]¬
[?], jetzt [verkauft?]
nicht
Die nach ins[?] Posen[schen?] gehen
die Mädchen bringen
sehr oft Kinder mit.
Nach Danzig gegangen
an 20 Mann, mehr
Mädchen.
Aus [?] 50 Personen.""",
 '5199_a2': """Wege gehen durch die
Höfe.
—o—
Mursch, schwarze Erde
vermischt mit Sand, gibt
erträglichen Boden.
Sonst geht sogar die
[Sprachweizen?] zugrunde.
—o—
Im [Sü…?] haben die
Łazinsker v. Tromp¬
czyn C, Wald angekauft
„Swirkhaber\"""",
 '5200_a1': """Vor 10 Jahren bekamen die Białoblot
u. Orlin Servitut zu
4 Morgen auch grossen
Wald, hauen ihn aus.
Vom Gute Biała
für Hütung u. Holzrecht
u. Streu.
—o—
Ständerhäuser
niedrige Schorn¬
steine.""",
 '5200_a2': """Lehmgebäude
„ins Holland" rein
sagte d. Frau.
1 dt. Lehr. u. 1 poln.
Lehrer.
Pommersche Scheunen
i. Obor.
Viel Elsen.
Torf gegraben.
Backöfen draussen""",
 '5201_a1': """In Łazinsk drinnen
d. Backöfen
Kleine Wirtschaft.
In Obory viel schlech¬
ter Wald für Servi¬
tut. Bekommen
vor d. Kriege.
Servitut vom Gute
Niniew.
—o—
In Kazimierka""",
 '5201_a2': """wenig Wiesen. An¬
deres Landsch.-Bild
Viel Häuser mit
Dachziegeln gedeckt.
Offene Landschaft
Querlin — Restgut
d. Pydde
Ziegelei""",
 '5202_a1': """Ständerscheune.
Mit Karren Ge¬
treide eingefahren.
Dicht neben d. Stän¬
derscheune eine
pommersche.
Keine Wanderdüne
[sehe ich?] die zweite.
pomm. Scheune
Tür
Backöfen draussen""",
 '5202_a2': """Kazmierka
Kirchhof dicht
a. d. Kirche.
Grabbretter wie
in Łazinsk
Zementdenkmäler
wie Łazinsk,
gleicher Schmuck
Zur Kirche hat [Pydde?]
Ziegeln geschenkt.
—o—
Bei Józefów eine Neue
Welt, ein Dorf,
nach [Ko…?]-Chocz.""",
 '5203_a1': """Na olędrach
" barwy
Józefów
Firstgugge[?]
Dachgugge
Józefów: guter Boden
Viel Weizen""",
 '5203_a2': """Erlenreihen
Gute Wirtschaftsgebäude
Ständerhaus
i. Józefów
Spitzer Giebel
Torfwiesen
Eigener Wald.
Józefów: Grabbretter auf
d. Friedhof wie Łazinsk.
Haus Schmiedemeyer. —
Ständerhaus
mit d. Giebel zur Strasse.
Pom. Häuser — mit Breitseite""",
 '5204_a1': """40 dt. Wirte i. Józefów. Land
i. einem Stück, Wald 2 Morgen
besonders.
5½ Morg. Land.
Kein deutscher Unterricht
an 60 deut. Kinder.
Ein poln.-evang. Lehrer, der
nichts Deutsch versteht, gibt
Relig.-Unt. Vor 2 Jahren
wollte er poln. Religionsunt.
einführen, die Kinder wollten
nicht, so musste er deutsch
machen: es ist aber ein Ge¬
lächter, übt m. 2 d. [Hochz?],
dann war er ganz weg.
—o—
Vom Gute Chocz. Gleich am
Land liegt d. [Gemeinde?] Wald.""",
 '5204_a2': """Laut Inventar bekamen Servitut
vor 45 Jahren.
Vater d. Janke sprach kaschub.
sind alle ausgestorben.
Wegert = platt.
Vor d. Krieg — Küster bis
v. 1907.
1907 die Schule gebaut
1907 – 1928 Fr. Lehmann.
vor Kuske Thiem
1895 – 1898, dann Hebzer.
Rottke war lange Jahre
in Watzke.
Die meisten sprachen plattdeutsch
Nach Russland: ein Onkel Zimmer
Kochanek, vor 46 Jahr. Hat es
in Wolh. schlecht gehabt. Wollte""",
 '5205_a1': """den Vater hineinführen, es ging
ihm schlecht.
In Kazim. Neu- u. Alt weniger
Plattdeutsch gesprochen.
In Obory 15 Mor. Schulland
„war im Druck" in Angst.
Züllichau
Gesangb. 1744.
Alt-Kazimierka 1782
Józefów 9 Nov. 1790.
vom Gute Chocz, Besit. Lipski
er hiess Josef = Józefów
Kazimierz = Kazimierka
Nowo-Lipsk = Lipski
12 dekt.
gehören zum Kantorat
Józefów""",
}

ENGLISH2 = {
 '5192_a': """V. Grodziec
July 1936""",
 '5193_a2': """Łazinsk
65 years ago,
in March, very many
to Russia.
Walked for a month,
if it went well.
(Maas, Merk, Munker,
Lieske,
46 years ago a
Lieske moved away,
has money here.
Shortly before the war people from
Volhynia also came back.""",
 '5194_a1': """cleared the forest
there, the [illegible]
then [illegible]
[illegible], came back
(Hom, Liske)
Łazinsk clay
kaite[uncertain: r/n], everyone takes
clay.
—o—
Augustenhoff
Augustynow and Emilienheim
were founded together;
the children go to school
in Emilienheim""",
 '5194_a2': """Then Włodzimierow.
Włodzimierow parcelled out
almost everything to Germans.
Włodzimierow was parcelled
25 years ago from the Trąbczyn
estate; the owner was called Count
Miączyński.
Paid out at once.
The remaining manor had some 60 Morgen.
Jesse came from Białobłoty.
The others from this area.
—o—
In Łazinsk consumption
is widespread. Doctor Brede
in Zagórów is surprised at it;
he thinks that in this area""",
 '5195_a1': """[uncertain: Door] orna¬
ment
—o—
House
Emilienheim
there ought to be no consumption.""",
 '5195_a2': """In Łazinsk
mighty parabolic
dunes
The first near Emilienheim,
the second near Łazinsk.
Meadows
and waterholes
[uncertain: boundary forest]
School
near""",
 '5196_a1': """Church service in Łazinsk.
Peculiarities:
During the general prayer
the congregation kneels.
During the last verse of the last
hymn everyone stands up.
—o—
About 40 years ago, when Wło¬
dzimierzow came into being
out of Trąbczyn
—o—
Where the chancellery stands,
and the Pole Ankowiak
(5 Morgen), belonged
to Grabina""",
 '5196_a2': """Newly settled on
forest land to the right of the
road: the Germans
Bochenski (20 Morgen), Kinast, Winterfeld, [uncertain: Neihe]
Retzläff, a Pole, Schwarz,
Lipelt, Schmechel.
The land was forest; it
belonged to the Trąbczyn estate.
The forest, and the land among other things,
a Jew bought; 5–6 years
before the war he sold it on
to Germans. The new settlement
is called Trąbczyn D.""",
 '5197_a1': """Obory
Kazimierka
Józefów
"Oberscher"
"Kirschhacker"
hie = here
do = there
Sin
"I want to buy oats",
gallants = Prietzer
Cake with the meat
At the wedding danced with
the cattle and the dogs.""",
 '5197_a2': """Herzfeld near Berlin
Robert [uncertain: Nintz],
[illegible]
married there.
Merk, his brother's
4 children [uncertain: Kin…]
Herzfeld,
also labourers.
Merk
Gustav Stark,
brickmaker,
Herzfelde.
The brother
G. Merk sold
10 Morgen here,
bought in Brudzewo
near Strzałkowo; now in Pomerelia
48 Morgen of good land,
Bukowiec near Jabłonowo,
district of Brodnica.
About 1830 a few more
came to Łazinsk.
Merk is 53 years old and does not
remember the Russian emigration.
His father's brother Daniel
came to Łazinsk on a visit
before the war""",
 '5198_a1': """A Janke was 30 years in
Volhynia, but came back
and died here.
Went there poor, came back
poor.
Americans: Ed. Buch 4 Morgen,
Weber, district Bauch 10 Morgen.
Colonisation Commission:
many moved away,
Bauch from Obory,
Merk —
Deckert,
got good, drained
land.
In Ostfelde, district of Września, the Germans
from Łazinsk were chased off by the Poles,
paid a few groszy.""",
 '5198_a2': """Wurmbusch, Mainitz,
district of Września, district of Września
—o—
Koppen — sheaf stacks
In Łazinsk here and there
fine wheat
—o—
Is there on a [uncertain: Rhein…]
in the village?
An old couple lies in winter, motionless.
"bawled at me" — shouted at me.
Potatoes were stolen,
out of good nature. —
—o—
Venereal diseases
not present.""",
 '5199_a1': """Illegitimate children,
many.
Fru[uncertain: c]ksucht [uncertain: on the road],
[uncertain: more] summer work
on former [uncertain: Gottmann's]
[illegible], now [uncertain: sold]
not
Those who go [uncertain: into] the Poznań [uncertain: province],
the girls very often
bring children back.
Went to Danzig,
some 20 men, more
girls.
From [illegible] 50 persons.""",
 '5199_a2': """Roads run through the
farmyards.
—o—
Mursch, black earth
mixed with sand, gives
tolerable soil.
Otherwise even the
[uncertain: Sprachweizen] perishes.
—o—
In [uncertain: Sü…] the people of
Łazinsk bought forest from
Trąbczyn C,
"Swirkhaber\"""",
 '5200_a1': """10 years ago Białobłoty
and Orlin got a servitude of
4 Morgen, and a large
forest too; they are cutting it down.
From the Biała estate,
for pasture and the right to wood
and litter.
—o—
Post-built houses,
low chimneys.""",
 '5200_a2': """Clay buildings
"into Holland",
said the woman.
1 German teacher and 1 Polish
teacher.
Pomeranian barns
in Obory.
Many alders.
Peat dug.
Bread ovens outside""",
 '5201_a1': """In Łazinsk the bread
ovens are inside.
Small farm.
In Obory much poor
forest for the servi¬
tude. Got it
before the war.
Servitude from the
Niniew estate.
—o—
In Kazimierka""",
 '5201_a2': """few meadows. A
different landscape.
Many houses
roofed with tiles.
Open landscape
Querlin — remaining manor
of Pydde
Brickworks""",
 '5202_a1': """Post-built barn.
Grain brought in
with carts.
Close beside the post-built
barn a Pomeranian
one.
No wandering dune;
[uncertain: I see] the second.
Pomeranian barn
Door
Bread ovens outside""",
 '5202_a2': """Kazmierka
Churchyard close
to the church.
Grave boards as
in Łazinsk;
cement monuments
as in Łazinsk,
the same ornament
[uncertain: Pydde] gave tiles
to the church.
—o—
Near Józefów a New
World, a village,
towards [uncertain: Ko…]-Chocz.""",
 '5203_a1': """Na olędrach
" barwy
Józefów
[uncertain: Firstgugge] (a ridge ornament)
Dachgugge (a roof ornament)
Józefów: good soil
Much wheat""",
 '5203_a2': """Rows of alders
Good farm buildings
Post-built house
in Józefów
Pointed gable
Peat meadows
Own forest.
Józefów: grave boards in
the cemetery as in Łazinsk.
Schmiedemeyer's house. —
Post-built house
with the gable to the road.
Pomeranian houses — with the long side""",
 '5204_a1': """40 German farmers in Józefów. Land
in one piece, 2 Morgen of forest
separately.
5½ Morgen of land.
No German teaching
for some 60 German children.
A Polish Protestant teacher who
understands no German gives
religious instruction. 2 years ago
he wanted to bring in religious
instruction in Polish; the children would
not have it, so he had to do it
in German: but it is a laughing¬
stock; practises with 2 [uncertain: weddings],
then he was quite gone.
—o—
From the Chocz estate. Right by
the land lies the [uncertain: commune] forest.""",
 '5204_a2': """By the inventory they received
a servitude 45 years ago.
Janke's father spoke Kashubian;
they have all died out.
Wegert = Low German.
Before the war — sexton until
1907.
1907 the school built.
1907 – 1928 Fr. Lehmann.
Before Kuske, Thiem
1895 – 1898, then Hebzer.
Rottke was many years
in Watzke.
Most spoke Low German.
To Russia: an uncle Zimmer
Kochanek, 46 years ago. Had a bad
time in Volhynia. Wanted""",
 '5205_a1': """to take the father in; it went
badly for him.
In New and Old Kazimierka less
Low German spoken.
In Obory 15 Morgen of school land;
"was in a squeeze", in fear.
Züllichau
hymn book 1744.
Old Kazimierka 1782
Józefów 9 November 1790,
from the Chocz estate, owner Lipski;
he was called Józef = Józefów,
Kazimierz = Kazimierka,
Nowo-Lipsk = Lipski
12 dekt.
belong to the cantorate of
Józefów""",
}
