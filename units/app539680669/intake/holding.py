# -*- coding: utf-8 -*-
"""APP 53/968/0/-/669: Albert Breyer's notebook of July 1936 on Łazińsk and Emilienheim.

    python units/app539680669/intake/holding.py            # check only
    ... --crop        cut the page images at the folds
    ... --sheet       the fold page for the editor
    ... --crop2       cut the page images of document 2 (photos.py first)
    ... --write       page files and corpus.txt from TEXT and TEXT2
    ... --english     write translation/doc1.yml from ENGLISH
    ... --cache       put it into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding. The steps are
those of courtbook.holding_main (pipeline/intake/courtbook.py), as in APP
53/968/0/-/783.

The unit. The archive's unit 53/968/0/-/669 of the papers of Albert Breyer
is a bundle of his field notebooks ("Grodziec [Notatki dotyczące Grodźca,
Józefowa Zamentu, Łazińska]"). The editor photographed four notebooks in
April 2023 (IMG_5181 to IMG_5210, raw files, in the unit's folder) and had
the archive's scans of one of them (Image00001 to Image00018, in the folder
"Notes on Łazińsk"). The holding is that one notebook and nothing else
(editor, 2026-10-14). The editor's file "Breyer Notes.md" in that folder is
a partial English rendering of another notebook, headed "Grodziec Juli
1936" (IMG_5192 to IMG_5205): it is not used here.

The notebook. A small school exercise book with a lilac cover, written in
pencil, mostly in Latin script; field names and a few notes in German
Kurrent. The cover has "Juli 1936", "Łazinsk", "Emilienheim" in coloured
pencil. Breyer wrote it from the front in Łazińsk and Emilienheim, two
German settlements of the gmina Trąbczyn, and used the last pages, from the
back, as a log of his photographs: one of those pages is headed "Juli
1935" and names Gostynin, Leonberg and Grabie, another district. The
inside covers are written on too, faintly.

Images. Image00001 is the front cover alone; Image00002 to Image00018 are
openings, cut at the fold. Image00002 has the inside front cover on the
left; Image00018 the inside back cover on the right. Page ids carry the
image number: 0001_a, then 0002_a1, 0002_a2 to 0018_a1, 0018_a2. The folds
are first proposals from courtbook.find_fold, checked against the gutter.

The reading (2026-10-14). There was no transcription. Every page was read
from the archive's scans in the session: each opening cut at the fold, in
four strips at about twice the size, the faint inside covers in the red
channel. TEXT is the reading, line by line as on the page.
- Doubt: "[?]" for a word not read, "[word?]" for one read with doubt, and
  "[Sm…?]" where only some letters are read (EDITORIAL_RULES). There are
  many on the two inside covers, which are barely legible.
- A word broken at the end of a line ends in "¬", as in the other German
  holdings.
- Breyer's dividers between notes, a short line with a small circle, are
  given as "—o—".
- Struck-out words are left out; words he wrote above the line are put
  where his mark sends them. Where a note stands at the side of the page it
  is given after the line it stands beside.
- Not transcribed: his sketches (the fronts of houses and barns, 0003_a2;
  the corner bracing of a barn, 0005_a2; the shapes of grave boards in
  Łazińsk and Emilienheim, 0016_a1); the boxes and braces round notes.
- A word broken across two lines is given whole on the second line
  ("Strażniki", 0016_a1, where the page has "Kraż-" / "niki", first read
  "[Krainik?]"): a mark of doubt must stand on one line for the counts.
- The stamp of the village headman of the colony of Łazińsk on 0006_a1 is
  given in its own three lines, as it reads.
- The editor's answers on the spot sheet "Readings in Breyer's notebook"
  (2026-10-14, review/app539680669/readings_answers.json) are in TEXT:
  Wagelt[?] for Wagels[?]; 17. IV 1832; Halwege; Hormann[?] for
  Hossmann[?]; Neumann L. 1889 – 1849 (the editor's reading; the years run
  backwards as written); Włodzimierow for Wlodziemen[?]; Bärwinkel. Gullat[?],
  1928[?] and Wolwachówka[?] stand with their doubt.
- The editor's answers on the second spot sheet, "More readings in
  Breyer's notebook" (2026-10-14, readings2_answers.json), are in TEXT as
  the editor typed them, with the edition's marks: Mühle (not Müller);
  annähre[t/s?]den; Birk[?]la[ch?] (not Kavelung); Rotkapp; Noga (not
  Kroge: the same field name stands on 0007_a2); Kühnstubben; Lieder;
  Oborscher; Zamęty; Gä[ehe?]blotte; Griefenberge (typed "Griefenbergr.",
  taken as the evident slip for the "-berge" first read); ge[?]kt (not
  gekauft); Hausker[?] (the editor could not tell, and offered it);
  Swięcer (not Smięcer); Schabeln; Olszewo; vortüng Kr[?] (not
  vorläufig); Parkre; Strażniki (a village, not the name Krainik);
  St[?]pin (not Sm…); Paprotk[?]; Izbitz. Lodz., Kb., Gehege, grob,
  Züchten (the editor offered Züchter), Kaveln and the word before "i.
  Brasilien" stand with their doubt.
- The third sheet, "Sm or Sw in Breyer's notebook" (2026-10-14,
  readings3_answers.json): "Aus Swięcia" and "Budendorf stammt aus
  Swięcia" on 0012_a1 (first read Smięcia, without doubt), and St[y?]pin
  for the second "[Sm…?]" on 0018_a1.
- The English (ENGLISH) translates the notes and keeps the names as he
  wrote them; Trąbczyn takes the edition's spelling.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app539680669'
REF = 'APP 53/968/0/-/669'
RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Grodziec [Notatki dotyczące Grodźca, Józefowa Zamentu, Łazińska] (53.968.0.-.669)\Notes on Łazińsk (53.968.0.-.669)")

# (file, x of the fold or None for a single page, left page, right page). First proposals.
FOLDS = {2: 1264, 3: 1286, 4: 1286, 5: 1288, 6: 1290, 7: 1290, 8: 1293, 9: 1293, 10: 1302, 11: 1310,
         12: 1313, 13: 1309, 14: 1303, 15: 1292, 16: 1309, 17: 1306, 18: 1292}
SCANS = [('Image00001.jpg', None, '0001_a', None)] + [
    ('Image%05d.jpg' % n, x, '%04d_a1' % n, '%04d_a2' % n) for n, x in sorted(FOLDS.items())]
PAGE_IDS = ['0001_a'] + ['%04d_a%d' % (n, s) for n in sorted(FOLDS) for s in (1, 2)]
LEAF = {'0001_a': 'the cover', '0002_a1': 'inside the front cover', '0018_a2': 'inside the back cover'}
FOLD_NOTE = 'Both halves are pages of the edition.'

TEXT = {
 '0001_a': """Juli 1936
Łazinsk
Emilienheim""",
 '0002_a1': """An [?] [?] [?] [?]
In Orlin: [?]
Bahnhof
Töpferecke:
bei Białobłoty
Weißer Berg
Schwarze [Damm?]
[Li…?] Straße
nach [?]
Neu-[Schl…?]
[?] [?]
[Wal…?], [?]
d. Wald
auf d. [?]""",
 '0002_a2': """In Obory Lehrer Kampel.
[Lodz.?] Sem.
ist seit 5 Jahren.
In Józefow ein Mathys
Kantor.
(die Akten bei ihm)
[Kb.?]-Bücher ab 1907
P. Gross
Konin u. Słupca
mit Zagórow
wenig verschwägert —
häufig dafür: Nowo-
u. Alt Łazinsk u.
Józefow; seltener i. Zagórow
mehr nach Lissa-Peisern
heiraten auch aus dem""",
 '0003_a1': """Posenschen.
Aus Smaszew Gem.
heiraten aus Orlin
u. Białobłoty, Obory
auch Borowiec in die
Zagórower Gem.
seltener: Wojciechowo,
Czarnica, Grondy.
—o—
Wrąbczynek. Kolonia
mit Polen stark durch¬
mischt, sprechen mit
Vorliebe polnisch.""",
 '0003_a2': """singen gut, sehr viele
musik. Familien.
Intelligenter als Grodziec (i. Gem. Zagórow)
Verkehr mit Posenschen
—o—
Michalinow
Pommersche Scheunen in
u. bei Emilienheim.
Häuser aus Lehm mit
Holzbindung
Lehm
die pommersche Scheune
jedoch nicht rein ausge¬
prägt""",
 '0004_a1': """Michalinow.
Land: 1) Baustücke
2 Morgen
2) Kaveln 4 Morgen
3) 4 Morgenstücke magdeb.
4) Wiesen b. Oleśnica
1, 2, 3 Morgen
4a) Wiesen b. Olchowo
1, 2, 3 Morg.
Schulzenland sind 2 M. L.
1 M. W.
1 Morg. Wiese für Mühle""",
 '0004_a2': """Schule 7 Morgen.
—o—
Meist Breslauer Gesang¬
bücher. —
Nach Wolhynien
sind viele ausgewand.
nach Nowograd-Wolyn.
—o—
Wohnhäuser in annähre[t/s?]den Fachwerk
Restgut Trąbczyn.
Jesse gekauft, wann?
Wie ist das Land klassiert? i. Mich.""",
 '0005_a1': """[?] [?] der [?]
Mielke
in Łazinsk.
„Die Büschen" Flurnamen
Wirtschaften: „[Gehege?]"
—o—
„Die Birk[?]la[ch?]"
„Rotkapp"
„Die Noga"
([?] Fuß)
„Trieb" [?] „[Gehege?]" [?] in [?]""",
 '0005_a2': """„Bärwinkel"
„Morast". —
—o—
Alter Krüger (86 J.)
Sohn d. Krüg. im Posenschen Schmied.
sein Lehrer Neumann
Kosiniery im Dorf keinen
Schaden gemacht
Krüger hat d. Tochter auch 4 Morgen Land
verschrieben an [Wagelt?].
An den Ecken d. Scheunen
gestützt mit schmalen
Querbalken
In Emilienheim sprechen nicht
so [grob?] wie Łazinsk.""",
 '0006_a1': """Kolonja Łazińsk.
GROMADA ŁAZIŃSKA KOLONJA
SOŁTYS
GMINA Trąbczyn
2040 Morgen.
Wirte 250 Wirte.
Nur eine Kategorie III.
auch Huta Trąbczyńska
ein Restgut aufgeteilt
II. Kategorie
Trombczyn Neuland.
4 Morgen für 1 gezahlt.""",
 '0006_a2': """Klatt hat d. Gesangbuch
mitgenommen.
z. B. bei Schröter Ludwig
war d. Name Pydde Michel.
niemand gedenkt,
wann dieser gelebt hat.
—o—
Servitut bekommen vom
Gute Trombczyn um 1880?
Grünwald um 1904
Die Servitute wurden zum
alten Land beim Rejenten
zugeschrieben, müssen auch
davon hohe Steuern zahlen.
—o—
Die 60 Wirte sind i. d. Zeit
zugekommen.""",
 '0007_a1': """Sind i. d. Wald gekommen:
haben an d. Hütung gebaut,
für den Hofreite.
In Emilienheim heisst
es Baustelle.
Jeder hat um Hause seine Hütung,
auch wenn er zwei Morgen Land
nur besitzt.
Der grösste bis zum kleinsten
hat sein Stückchen Wiese.
—o—
Torf auf d. Wiesen d. Lehrers
u. d. Schulzen, sonst wenig
Torf. 10–15 haben für eigenen
Bedarf.
Die Birkenrinde findet""",
 '0007_a2': """man noch, Torfschicht
mannshoch.
—o—
Der Graben geht bis Peisern
über Bukow, Łukom.
„Noga" „Maras"
Bei d. Schule „Altes Holland"
„Bärwinkel"
„Neues Holland"
„Neu-Warschau"
Der Kanal heisst „Graben"
Baustellen. In Emilienheim.
„Kafeln" „Viermorgen\"""",
 '0008_a1': """Man findet noch alte
Kühnstubben. (gräbt ihn
aus)
1929 Lieder.
im Bresl. Buch.
Friedhof: Józefow
Agnes Schütz, geb. Neumann
In Neustädtl in Schlesien,
geb. 17. IV 1832
31. I. 1864 [gestor…?]""",
 '0008_a2': """Peltzer (vom Kulturbund)
zwei Mal im
Seminar aufgenommen.
Bei Berendt: Dienstmädchen.
Ist spurlos verschwunden.
—o—
10 Jahre hindurch 170 Schüler
bei einem Lehrer.
Seit 2 Jahren eine Hilfs¬
kraft, da ein neues Schul¬
gebäude gebaut wurde.
Militärbehörden beklagten
sich im Unter.-Min., dass
die Rekruten d. Gem. Trąb¬
czyn nicht polnisch können.""",
 '0009_a1': """In Peisern Holl.
Breslauer u. Züllichauer
Aus Łazinsk sind
nach Russland gegangen
kamen auch zurück.
—o—
Neu Holland hinter
d. Hütte.
—o—
Die Schwiegermutter des
Kranich gedenkt, dass
das Vorwerk Huta""",
 '0009_a2': """aufgeteilt wurde.
—o—
Mielke
Der alte Ludw. Klingbeil,
ging nach Amerika, wurde
dort „Pastor", Vervielfältigen
konnte er, teilen nicht.
Nur Religion unterrichtet.
Im ersten Unterrichtstag
waren i. d. Schule 186 Kinder.
Lehrer i. Łazinsk:
Mielke seit 1925.
Klingbeil war 9 Jahre.
Zelmer Ed. war 34 Jahre.
aus Łazinsk
Radke 10 Jahre
Rasch 50 Jahre
ein anderer hat für ihn die
Prüfung bestanden.""",
 '0010_a1': """Rasch war noch mit
80 Jahren Lehrer, hier
in Łazinsk gestorben.
—o—
Mutter schwer krank. Es
wird d. Pastor geholt,
unterwegs fragt er den
Sohn: Wie geht es der
Mutter? Sehr schlecht
hoffentlich ist sie schon
tod, ehe wir hinkommen.
Pastor wendet ein: Viel¬
leicht. —
Die Oborer: Hockerling.""",
 '0010_a2': """Oborscher Kirschknacker
—o—
Auf d. Mädchen
sagt man „[Züchten?]"
in Zamęty.
heiratstüchtige
Plötzer = Kavaliere
Wenn sie grob sprechen:
Hockerlinge.
In Orlin u. Białoblot:
Kaschuben""",
 '0011_a1': """Michalinow Olesn.
Kühe ziehen Erntewagen
Zäune angekalkt. —
Vor zwei Jahren Schule ver¬
grössert, bezäunt, Gmina
dazu gegeben 300 zł. —
Emilienheim angeschlossen
an Drzewce, weil 11 Person
fehlten zur Zahl 200. Jetzt
daraus grosse Schwierig¬
keiten. Der Schulze i. Drzewce
kennt d. dt. Leute nicht
Unterschulze ist noch Krüger,
muss helfen""",
 '0011_a2': """Nach Russland
Budendorfs
ist des Vaters Schwester
gezogen (die Frau Budendorf)
auch noch 2 aus Michalinow
Schwiegervater bekam zwei
Morgen sandiges Land, hat
sich aufgebaut. —
Was Halwege war, ging
nach Deutschland. Budendorf
haben sich nur auf diese Art
die Wirtschaft auszahlen können.
Breslauer Bücher in Emilien¬
heim.
2 St. Religion i. d. Woche""",
 '0012_a1': """Aus Swięcia
Budendorf stammt aus Swięcia
Flurnamen
1) Bronikel
2) Steinbruch
3) Grüne [Kaveln?]
4) Gänseblotte
5) Gä[ehe?]blotte
6) Griefenberge.
7) Grosse Blotte
8) Baustellen.""",
 '0012_a2': """Ein [Gullat?], [Hormann?]
nach Russland. Budendorf
ge[?]kt, vor 50 Jahren.
—o—
Bruch ist hinter Oleśnica
Tarszewo, Olchowo, Mały
Las, Dombrowitz — alles
vor d. Warthe —; die
Menschen werden „Die
Brücher" genannt.
—o—
Myśliborer Holl., Węglewer
[Hausker?] Holl. Kein
Bruch.""",
 '0013_a1': """Die Leute im Bruch sprechen
nach d. Swięcer Sprache, alles
kurz.
„In der Tür eine Leinwand¬
platte gegen d. Hitze"
—o—
Die Häuser Ständer mit
Lehm ausgefüllt, im Win¬
ter kalt.
—o—
Schabeln geraten nicht, schlechtes
Land.
„alle essen gern Mohnklösse"
—o—
Bei Schultz i. d. Küche sauber.
—o—
Deutsche Dienstboten bei Schultz.
In Węgl. Holländer — polnische.""",
 '0013_a2': """Bei Schulz Ständerscheune.
Auch treten in Emilienheim
bereits Pappeln auf, sie wachsen
aber nicht kerzengerade, verzwei¬
gen sich mehr.
—o—
Auf d. Friedhof i. Emilienheim
ähnliche hölzerne Grabbretter
wie in Łazinsk
auch die neuen Zement¬
kreuze sind den Łazinsker
gleich. —o—
„Kopitzen": Garbenhaufen
sagen i. Emilienheim.""",
 '0014_a1': """Neues Holl. i. Łazinsk?
Wie sprechen i. Emilienheim?
Wie in Tarszewo, Olszewo
Wann parzelliert Restgut
Trąbczyn? Jesse gekauft,
wann? Heisst heute Włodzi¬
mierow. Noch lange vor dem
Kriege. —
Eine Tante d. Krügers vor mehr 40 Jahren
nach Brasilien mit ihrem Manne.
[?] i. Brasilien. Früher war
die Epistel drin, konnte man
zusammen mit Kantor lesen.""",
 '0014_a2': """Tarszewo, Olchowo, Mały
Las, Chruścik — Brücher
„sprechen langsam gedehnt
„j" anstatt g
„jejen" „jejangen"
—o—
„ick war do" = Brücher.
ich war da
er hud = er hatte
—o—
alte Schultz
In jedem Holland ein ande¬
res Buch, darum gleiche
Bücher eingeführt
Privileg für Züllichau 1786.""",
 '0015_a1': """Der Vater d. alten Schultz kam
aus Tomice
1889 — [1928?]
immer 80–90 auch 100 Kind.
Kantor bis 1934.
Neumann L. 1889 – 1849
Pflegel. 1849. —
Schulchronik geschrieben
v. Schultz.
In Emilienheim Land und
nieużytek
(Matura gemacht das schwerste i. Leben)
Früher Breslauer Gesang¬
bücher.
(als Kind immer Pastor werden. —)
Ein Sohn d. Schultz Pastor i. Deutschl.
Postbeamte, Missionar, Indien, Eng¬
land, Krieg, Dänemark, Rostock.""",
 '0015_a2': """Zur Schulgem. gehören:
Augustynow, Włodzimierow
Michalinow, auch Drzewce.
[vortüng Kr?] um 1876
Nach Wolhynien sind aus¬
gewandert 4 Brüder d. Schulz,
in d. Gegend v. [Wolwachówka?],
Kr. Żytomierz. Die meisten
dort hingezogen.
Nach Amerika viel ge¬
zogen, kam zurück, kaufte
sich Land oder zahlte
das angekaufte aus. Ein
Sohn d. Schultz i. Parkre, ist
Farmer.
Das Gut Drzewce parzelliert
haben auch einige Deutsche
genommen, noch vor jap. Kriege
um 1900""",
 '0016_a1': """Łazinsk
Emilienheim
Łazinsk
Sonne
N 4 Haus 12 1/25
Ohne 6,3
1 Uhr 8 Mann 1/25 B. 6
7. Haus 1/10 Bl. 9
3 Uhr N 9. Schultz 1/50 Bl. 9
Emilienheimer
zahlen gut Abga¬
ben sagte d. Steuerinspek.
nicht zusammen¬
schliessen; dann aber doch.
Strażniki: im Dorfe, der einzige
Pole, Ladenbesitzer, zahlt kein Steuern""",
 '0016_a2': """N 6, 10 Uhr Sonne Bl. 18, 1/10
7 " " B. 25 1/10 Mädch.
Janina Bednarek
Michalinow!
—o—
Haus 11 Uhr,
Kind 25 Bl. 1/10
Fam.
[Film?] ohne
Morg.
Emilienheim N 1, Bethaus
7. 1933 12 Uhr, Gf
I Kl. 14 Mor. Bl. 9. 1/10 Sek
II " 235 " Land.
III " 25 " 5 Uhr Bl. 12
IV " 49 " Gf. 1/5
Nieużyt. 14 "
337 morg.""",
 '0017_a1': """N 4 Haus B. 12, Gf. 1/5 Sek 4 Uhr
N 6 Krüger Bl. 9. Gf 1/5 " 4 Uhr
Sonne
N 8 Schule Lehr. Bl. 12. Gf. 1/5 " 12½ Uhr
Sonn
5 [Kistler?] Bl. 18 Ohne 1/15 "
3 " Bl. 12 " 1/25 "
Sonne
N 1 Neue [W…?]. Bl. 12 Ohne 1/10 5!
2. [?] Bl. Ohne 1/5 5
3 Lands. Bl. 4,5 " 1/25 5
4 Mühle " 4,5 " 1/10 5½
N 1 Haus Bl. 9, Ohne 1/10 6 Uhr
Mann Bl. 6,3 " 1/10 6 Uhr
8. [Kazm.?] 11 Uhr. Gf B. 9. 1/5""",
 '0017_a2': """Juli 1935.
9 Uhr Haus Radatz i. Schatten
mit 7 Gänsen
Bl. 9. Ohne 1/25 Sek.
9½ Uhr. Penno. Im Stalle
Bl. 12. Ohne 1/10 Sek.
Haus Radatz, 4 Uhr nachm.
Bl. 12. Selbf. 1/10 Sek.
g. d. Sonne.
12 Uhr mittags, Sonne, Weichsell.
Bl. 9. Gf. 1/25 Sek.
Sonne
Gostynin, Kirche, 11 Uhr. Gf. Bl. 6 1/5
viel Vordergr.
Leonberg, Schule, 10 Uhr, Ohne Bl. 25 1/10
" Friedhof, 10 " Gf. Bl. [4,5?], 1/10
Grabie, Landwirt. 5½ " Ohne Bl. 9. 1/10
Frau Vogel, 3 Uhr, Gf. Bl. 4,5 1/25
Montag
N 9 Wirtsch. 7 Uhr Bl. 9 1/2 Sek Oh.
3 [Mielke?] 9 Uh Bl. [?] 1/10 Sek O.
6 Obory 10 " Bl. 9 1/10 Gf""",
 '0018_a1': """Landgüte:
Białobł.
Leit = Leine
übergreigeln = überfahren
Müller
Vor 54 Jahren aus St[?]pin
nach Deutschl. zur Arbeit.
kamen aus Emilienheim mit
einem Mädchen zusammen
und heirateten. —
Neu Czarkow, Briesen, Paprotk[?]
auch Brücher
Psary verkopp. im J. 1868
In St[y?]pin bei 6 Stücke: um 1868
[Bloh.?]: hinterm Kanal.
Trockene, Neuland, hinterm
Kirchhof; Vermessen: Dornstein
nach Izbitz „[?]" im Gute
„Grochowisko".""",
 '0018_a2': """[?]: Wasserquelle
haben d. Polen verbo¬
ten d. [Rutkowski?] [?]
[?] [?] [?]
den [Rutkowski?] nach [Wars…?]
abgeholt, die Gem. [?]
[?].
[?] das Pflaster [?] [?]
[?] Posen u. [Pfaffen?]
fertig ist, dann geht
die Welt unter.""",
}

from english import ENGLISH  # noqa: E402  (the English, page by page: intake/english.py)
# Document 2, the notebook "V. Grodziec Juli 1936" (the editor's photos; notebook2.py, photos.py).
from notebook2 import BLANK2, ENGLISH2, FOLDS2, PAGE_IDS2, TEXT2  # noqa: E402
from photos import PHOTOS  # noqa: E402

SCANS2 = [(PHOTOS + '/IMG_5192.jpg', None, '5192_a', None)] + [
    (PHOTOS + '/IMG_%d.jpg' % n, x, '%d_a1' % n, '%d_a2' % n) for n, x in sorted(FOLDS2.items())]
DOCS = [(1, PAGE_IDS), (2, PAGE_IDS2)]

S = {
 1: ('Notizbuch Albert Breyers, mit Bleistift geschrieben, auf dem Umschlag „Juli 1936“, „Łazinsk“ und „Emilienheim“: Notizen nach den Angaben der Bewohner der deutschen Siedlungen der Gemeinde Trąbczyn. Die Kolonie Łazińsk, bei der der Stempel ihres Schulzen im Heft steht, hat 2040 Morgen und 250 Wirte; vom Gut Trąbczyn erhielt sie um 1880, mit Fragezeichen, Servitute, die beim Notar dem alten Land zugeschrieben wurden und hoch besteuert sind. Breyer fragt, wann das Restgut Trąbczyn parzelliert wurde, das Jesse kaufte und das heute Włodzimierow heißt. Er notiert die Lehrer in Łazińsk: Mielke seit 1925, Klingbeil 9 Jahre, Ed. Zelmer 34 Jahre, Radke 10 Jahre, Rasch 50 Jahre, der noch mit 80 Jahren unterrichtete; am ersten Unterrichtstag waren 186 Kinder in der Schule, und zehn Jahre lang hatte ein Lehrer 170 Schüler. Die Militärbehörden klagten beim Unterrichtsministerium, die Rekruten der Gemeinde Trąbczyn könnten nicht Polnisch. Viele sind nach Wolhynien ausgewandert, aus Łazinsk auch nach Russland und zurück, andere nach Amerika und Brasilien. Emilienheim wurde an Drzewce angeschlossen, weil 11 Personen zur Zahl 200 fehlten. Weiter: Heiratskreise, Gesangbücher aus Breslau und Züllichau, Flurnamen, Redensarten der „Brücher“ („ick war do“), Häuser, Scheunen und hölzerne Grabbretter. Die letzten Seiten sind ein Verzeichnis seiner Aufnahmen; eine davon trägt die Überschrift „Juli 1935“ und nennt Gostynin, Leonberg und Grabie.',
     'Albert Breyer\'s notebook, written in pencil, with "Juli 1936", "Łazinsk" and "Emilienheim" on the cover: notes from what the people of the German settlements of the commune of Trąbczyn told him. The colony of Łazińsk, beside which the stamp of its village mayor stands in the notebook, has 2,040 Morgen and 250 farmers; about 1880, with a question mark, it received servitudes from the Trąbczyn estate, which were added to the old land at the notary\'s and are heavily taxed. Breyer asks when the remaining manor land of Trąbczyn was parcelled out, which Jesse bought and which is now called Włodzimierow. He lists the teachers of Łazińsk: Mielke since 1925, Klingbeil 9 years, Ed. Zelmer 34 years, Radke 10 years, Rasch 50 years, who still taught at 80; on the first day of lessons there were 186 children in the school, and for ten years one teacher had 170 pupils. The military authorities complained to the Ministry of Education that the recruits of the commune of Trąbczyn could not speak Polish. Many emigrated to Volhynia, people from Łazinsk also to Russia and back, others to America and Brazil. Emilienheim was joined to Drzewce because 11 persons were lacking to make 200. Further notes cover marriage circles, hymn books from Wrocław and Züllichau, field names, the speech of the "Brücher" ("ick war do"), houses, barns and wooden grave boards. The last pages are a log of his photographs; one of them is headed "Juli 1935" and names Gostynin, Leonberg and Grabie.'),
 2: ('Zweites Notizbuch Albert Breyers vom Juli 1936, mit Bleistift geschrieben, auf dem Umschlag „V. Grodziec Juli 1936“; es handelt jedoch von Łazińsk und den Nachbarorten. Vor 65 Jahren seien im März sehr viele aus Łazińsk nach Russland gegangen, einen Monat zu Fuß; kurz vor dem Krieg seien auch Leute aus Wolhynien zurückgekehrt. Włodzimierów sei vor 25 Jahren vom Gut Trąbczyn parzelliert worden, dessen Besitzer Graf Miączyński hieß, fast alles an Deutsche; das Restgut hatte etwa 60 Morgen, Jesse kam aus Białobłoty. Auf Waldland des Gutes Trąbczyn, das ein Jude gekauft und 5–6 Jahre vor dem Krieg an Deutsche weiterverkauft hatte, liegt die Neusiedlung „Trompczyn D.“ mit Bochenski, Kinast, Retzlaff, Schwarz, Lipelt, Schmechel und einem Polen. In Łazińsk ist nach dem Arzt Brede in Zagórów die Schwindsucht verbreitet; beim Gebet kniet die Gemeinde. Deutsche aus Łazińsk erhielten durch die Kolonisationskommission drainiertes Land und wurden in Ostfelde bei Września von den Polen vertrieben. Weiter: Lehrer und Küster von 1895 bis 1928, Plattdeutsch und Kaschubisch, Servitute von den Gütern Biała, Niniew und Chocz, Ständer- und pommersche Scheunen, Grabbretter in Kazimierka und Józefów und uneheliche Kinder. Die letzte Seite nennt Jahreszahlen: ein Züllichauer Gesangbuch von 1744, Alt-Kazimierka 1782, Józefów 9. November 1790, „vom Gute Chocz“, dessen Besitzer Lipski hieß.',
     'Albert Breyer\'s second notebook of July 1936, written in pencil, with "V. Grodziec Juli 1936" on the cover; it is, however, about Łazińsk and the places around it. 65 years earlier, in March, very many people from Łazińsk had gone to Russia, a month on foot; shortly before the war people from Volhynia had come back as well. Włodzimierów had been parcelled out 25 years earlier from the Trąbczyn estate, whose owner was called Count Miączyński, almost all of it to Germans; the remaining manor had some 60 Morgen, and Jesse came from Białobłoty. On forest land of the Trąbczyn estate, which a Jew had bought and sold on to Germans 5–6 years before the war, lies the new settlement "Trompczyn D." with Bochenski, Kinast, Retzlaff, Schwarz, Lipelt, Schmechel and a Pole. In Łazińsk, according to the doctor Brede in Zagórów, consumption is widespread; during prayers the congregation kneels. Germans from Łazińsk received drained land through the Colonisation Commission and were driven out by the Poles at Ostfelde near Września. Further notes cover teachers and sextons from 1895 to 1928, Low German and Kashubian, servitudes from the estates of Biała, Niniew and Chocz, post-built and Pomeranian barns, grave boards at Kazimierka and Józefów, and illegitimate children. The last page gives dates: a Züllichau hymn book of 1744, Old Kazimierka 1782, Józefów 9 November 1790, "from the Chocz estate", whose owner was called Lipski.'),
}
HOW = 'written in the working session from the German as read (intake/holding.py, 2026-10-14).'


def read_source():
    out = {(1, pid): TEXT[pid].split('\n') for pid in PAGE_IDS}
    out.update({(2, pid): TEXT2[pid].split('\n') for pid in PAGE_IDS2})
    return out


def english():
    return {1: [ENGLISH[pid] for pid in PAGE_IDS], 2: [ENGLISH2[pid] for pid in PAGE_IDS2]}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    assert sorted(TEXT) == sorted(PAGE_IDS), set(TEXT) ^ set(PAGE_IDS)
    assert sorted(TEXT2) == sorted(PAGE_IDS2) == sorted(ENGLISH2), set(TEXT2) ^ set(PAGE_IDS2)
    for n, t in ((1, TEXT), (2, TEXT2)):
        print('document %d:' % n, len(t), 'pages,', sum(len(x.split('\n')) for x in t.values()), 'lines,',
              sum(x.count('?]') for x in t.values()), 'marks of doubt')
    if '--crop' in arg:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS))
    if '--crop2' in arg:
        # the photos stand in PHOTOS under RAW, so the pages go to the same processed/ as the scans;
        # the blank inside covers go to processed/_not_staged/
        courtbook.cut(RAW, SCANS2, skip=BLANK2)
    if '--sheet' in arg:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS), (), LEAF, note=FOLD_NOTE)
    if '--write' in arg:
        courtbook.write_pages(UNIT_DIR, DOCS, read_source())
    if '--english' in arg:
        tdir = os.path.join(HERE, 'translation')
        os.makedirs(tdir, exist_ok=True)
        for n, pages in english().items():
            courtbook.write_doc_yml(os.path.join(tdir, 'doc%d.yml' % n), pages)
    if '--cache' in arg:
        courtbook.save_cache(ROOT, SLUG, os.path.join(HERE, 'translation'))
    if '--summaries' in arg:
        courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S, HOW)


if __name__ == '__main__':
    main()
