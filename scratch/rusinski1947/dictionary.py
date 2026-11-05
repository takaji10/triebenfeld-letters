# -*- coding: utf-8 -*-
"""The contextual dictionary of tom5 (Rusinski 1947), for checking the OCR.

Built from:
  - the book's own Wykaz skrotow (scans 0010-0015, printed pp. V-X): the
    sigla and the works they name;
  - the project's glossary (reference/glossary.yml) and the established
    English/German renderings of the Olender domain;
  - the annex tables' recurring column words (added as the tables are read).

Use: a draft word that is not here, and is not ordinary Polish, is a
candidate doubtful reading. The FOLD table maps the OCR variants already
observed in the two passes to the print's form (evidence: the sweep and
the first pages read).
"""

SIGLA = {
    # A. Zrodla (the archive sigla, as the Wykaz gives them)
    'AC.': 'Acta Causarum 1739-40, Archiwum Archidiecezjalne w Poznaniu',
    'AGH': 'Akta gruntowe i hipoteczne',
    'AM': 'Akta miejskie',
    'AW': 'Akta wiejskie',
    'Dom.': 'Akta pruskie dot. domen panstwowych (sygn. Domeny)',
    'G': 'Goldbeck, Vollstandige Topographie des Konigreichs Preussen, t. 2 (1789)',
    'GE': 'Allgemeine Geographische Ephemeriden, t. 8 (Weimar 1801)',
    'Decr. Posn.': 'Ksiegi sadowe grodu poznanskiego',
    'Inser. Valc.': 'Ksiegi grodzkie waleckie (Inscriptiones Valcenses)',
    'Kat. I': 'Kataster ... Regierungs-Bezirk Bromberg, t. I',
    'Kat. II': 'Kataster ... Regierungs-Bezirk Bromberg, t. II',
    'Kl.': 'Akta klasyfikacyjne pruskie 1773-4 (WPZ. Kam. Dep. Bydgoszcz)',
    'KIl. M.': 'Akta klasyfikacyjne pruskie 1795, dobra Zakonu Kawalerow Maltanskich',
    'Kośc.': 'Akta dot. stosunkow wyznaniowych w zaborze pruskim po I rozbiorze',
    'Landr.': 'Akta bylych landratur pruskich',
    'Lustr.': 'Lustracja krolewszczyzn Prus Krolewskich 1664 (Fontes, Torun 1938)',
    'MG': 'Gilly, Special Karte von Sudpreussen 1:115200 (Berlin 1802-3)',
    'MGd': 'Mapa Prus Poludniowych 1796-1805, 1:57600 (duzy Gilly)',
    'MP': 'Mappa szczegulna Woiewodztwa Poznanskiego, Karol de Perthees 1791',
    'M. Schr.': 'Schroetter, Karte von Ost-Preussen ... 1796-1802',
    'M 182/': 'Special-Karte von dem ... Kreise, E. Peschel, Posen 1821',
    'O 83': 'Opisy parafij z lat 1783-4, t. XVIII-XXII (Biblioteka Narodowa, Krakow)',
    'OWK 89': 'Offiara na Woysko Powiatu koscianskiego 1789 (Ms. C. 17)',
    'Q': 'Quellen und Urkunden zur Geschichte des Netzekreises (Schulz, 1934)',
    'Rel. Cost.': 'Ksiegi grodzkie koscianskie (Relationes Costenses)',
    'Rel. Posn.': 'Ksiegi grodzkie poznanskie (Relationes Posnanienses)',
    'Rel. Valc.': 'Ksiegi grodzkie waleckie (Relationes Valcenses)',
    'Rel. Vsch.': 'Ksiegi grodzkie wschowskie (Relationes Vschovienses)',
    'Sf. TV.': 'Special Kreis Tableau ... Posenschen Kammer Dep. ... 1793 (AGAD SP)',
    'Szk.': 'Akta dot. szkolnictwa w zaborze pruskim po I rozbiorze',
    'T/6/9': 'Tarifa lanealis Posnaniensis ... (sygnatura do potwierdzenia)',
    'Tp. 89': 'Taryfa podatkowa (dymow) 1789 - Skarbowy wydzial AGAD',
    'Tp. 90': 'Taryfa podatkowa (dymow) 1790',
    'TV': 'Topographisches Verzeichniss ... Posener Cammer Departement 1793/4 (AGW SP)',
    'TW': 'Odpis tabel Ofiary/dymow/ludnosci Ziemi Wschowskiej 1789 (Mscr. G. 23)',
    'Verz. 1780': 'Verzeichniss samtlicher Ortschaften im Sudpreussischen Kammer-Departement Posen 1780',
    'Verz. 1845': 'Verzeichniss samtlicher Ortschaften des herzoglichen Bezirks Posen (Poznan 1845)',
    'Wol. Leg.': 'Volumina Legum',
    'VO 78': 'Visitatio generalis ... Srzemensis ... 1778 (A.V. nr 2)',
    'VO 83': 'Visitatio Generalia ... Crobensis, Smiglensis ... 1777-84 (A.V. nr 25)',
    'VO 84': 'Visitatio generalis ... Posnaniensis ... 1777-84 (A.V. nr 26)',
    'VO 87': 'Visitatio Generalis ... Zbaczynensis, Grodecensis ... 1780-87 (A.V. nr 28)',
    # B. Literatura
    'ZHGP': 'Zeitschrift der Historischen Gesellschaft fur die Provinz Posen',
    'DWZP': 'Deutsche Wissenschaftliche Zeitschrift fur Polen',
    'DWZW': 'Deutsche Wissenschaftliche Zeitschrift im Wartheland (od 1940)',
}

# The domain vocabulary the book uses (Polish forms with the German terms
# it glosses); each entry: the print's form(s), what it means, the OCR
# variants already seen. The English renderings follow the project's
# glossary where it has the term.
TERMS = {
    'olęder': 'a settler under Dutch (Olęder/Hauländer) law; pl. olędrzy, '
              'coll. olędrstwo; the book also writes Ol. for the plural '
              'in compound settlement names (Ol. Ujskie, Ol. Róża)',
    'Holendrzy': 'the same settlers, named for their origin; the book uses '
                 'Holendrzy and olędrzy near-interchangeably',
    'Hauländer': 'the German form of the same word, in German titles',
    'dym': 'hearth (fiscal unit); pl. dymy; the counts the annex tables give',
    'włóka': 'the Polish long acre (about 16.8-19.5 ha by locality); the '
             'settlement land unit, włók as fraction (1/2, 1/4 wł.)',
    'łan': 'the Magdeburg/Silesian hide, the other land unit (łan chełmiński '
           'defined p. 68 at 24 cali = 59.55 cm łokieć)',
    'morga': 'the smaller land measure (Morgen)',
    'okupne': 'the entry fine of an Olęder lease (Gloger: okup); also okup',
    'sołtys': 'the village headman the Olęder commune elects (glossary: schulze)',
    'ławnik': 'the commune juror/alderman (Schöffe)',
    'wilkierz': 'the commune bye-law (the book spells Wilkierz; Aneks III is one)',
    'przywilej': 'the foundation charter (locational privilege)',
    'lokacja': 'the founding of a settlement (lokalizacja in modern Polish)',
    'karczunek': 'the clearing of forest for the settlement',
    'serwitut': 'the use-right on the lord\'s land (pastwiskowe, leśne, rybne)',
    'robocizna': 'labour dues (Robocizny, pl.)',
    'propinacja': 'the lord\'s drink monopoly (przymus propinacyjny)',
    'czynsz': 'rent, pieniężny/w naturze',
    'folwark': 'the manor farm (Vorwerk)',
    'kmieć': 'full peasant farmer; półkmieć half; zagrodnik cottager; '
             'chałupnik hut-dweller; komornik lodger',
    'Tabela': 'the in-text statistical tables (TABELA I-III)',
    'Aneks': 'the annexes: I the settlement tables, II the Kicin privilege, '
             'III the Kotusz wilkierz',
    'Sejm czteroletni': 'the Four Years Sejm (1788-92), the book\'s census era',
    'rozbior': 'partition; pierwszym rozbiorze 1772, po rozbiorach',
}

# OCR variants observed in the two passes, mapped to the print's form.
# Added as the passes expose them; each line is evidence-backed.
#
# UNVERIFIED ENTRIES, to settle on the band re-reads (do not trust until
# ruled): SIGLA 'T/6/9' (sweep truncation, scan 0011); SIGLA 'Verz. 1780'
# (the passes read "18820", the year guessed); 'O 83' (read "O 83" but the
# Opisy parafij are 1783-4, the siglum may be OP 83); 'VO 78/83/84/87'
# (the years read off the visitations' titles, not the siglum itself).
FOLD = {
    'poangeliscken': 'poznańskich',      # 0015: Werner title, p. X
    'ldndliche': 'ländliche',            # 0015: Stein title
    'PIidagogische': 'Pädagogische',     # 0015: Schwochow title
    'Beriicksichtigung': 'Berücksichtigung',  # 0015
    'Filehner': 'Filehner',              # 0013: as printed? (check band)
    'Schónlanke': 'Schönlanke',          # 0013
    'Kónigsberg': 'Königsberg',          # 0013: Holsche
    'Konigsberg': 'Königsberg',          # 0013
    'Sud-': 'Süd-',                      # throughout the German titles
    'Sudpreussischen': 'Südpreussischen',
    'fir': 'für',                        # 0014
    'Rudolf,': 'Rudolf',                 # 0013/0014: stray comma at line ends
}

if __name__ == '__main__':
    print('sigla:', len(SIGLA), 'terms:', len(TERMS), 'folds:', len(FOLD))
