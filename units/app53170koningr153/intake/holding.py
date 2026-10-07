# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.153: from the editor's scans and texts to the edition.

    python units/app53170koningr153/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

Leaves 1391 to 1404 of a book of the castle court of Konin for 1782 are two
original acts on stamped paper that were sewn into the book:

    doc  leaves               pages                    what
    1    1391 to 1402 verso,  1391_a2 to 1403_a1,      the decree of the boundary chamberlain of Gniezno, 28
         1403 verso           1404_a1                  November to 3 December 1782, with the Tribunal's decree
                                                       of 17 October 1782 copied into it; and the note of its
                                                       entry at Konin on 7 December
    2    1404                 1404_a2                  the delivery of the settler Martin Hunt, 28 November 1782

Image00003 is one page (leaf 1391 recto); the other thirteen images are
openings: Image00004 is leaves 1391v|1392, and so on to Image00016, leaves
1403v|1404. Page ids: leaf N recto is <N>_a2, leaf N verso is <N+1>_a1. Leaf
1403 recto is blank, barred with pen strokes, and is set apart. The folds
are courtbook.find_fold's; they are first proposals for the editor.

The first check (2026-10-07) was the light one the plan sets for the long
holdings. Read against the scans, enlarged, word for word: leaf 1391 from
"per decretum commissionis" on, leaves 1391 verso, 1401, 1401 verso, 1402,
1402 verso, 1403 verso and 1404; and parts of leaves 1395, 1395 verso, 1396
verso, 1397 verso, 1399 verso, 1400 and 1400 verso. ROWS has what was
corrected. The rest of the Tribunal's decree (leaves 1392 to 1399) was not
read through.

At the editor's word the whole holding was then read against the scans,
page by page (the full check, 2026-10-07): every page of leaves 1391 verso
to 1400 verso, and the top of leaf 1391. Its record is full_check.json
beside this file (courtbook.full_check): 106 more corrections (ROWS, applied
with --full after --correct), 33 more places where the English follows
(FIXES) and 12 more of the editor's notes left out because they discuss a
reading that is now corrected (DROP). The rows there are written against
the text as the light check left it; ROWS below come first.

Three words were corrected throughout, on the ground of the places where
they were looked at, and not each occurrence was seen:
- "Jur~to", which the editor wrote out as "jurisdictione" beside "geomethra"
  and "ministerialis", is "jurato": a sworn surveyor, a sworn messenger
  (seen on leaves 1391, 1391 verso, 1395, 1395 verso, 1396 verso);
- "Cond~nis" and "Cond~lis", written out as "conditionis" and
  "conditionalis", are "condescensionis" and "condescensorialis", the
  sitting on the ground (seen on leaves 1391 verso, 1395, 1395 verso, 1400
  verso; the note on leaf 1403 verso has "Condescensoriale" in full);
- "Gerski" is Gorski (seen on leaf 1391 verso; he signs "Jacobus Pomian
  Gorski" in Konin Gr.118).
"siparitio[?]" is "sipatio", the raising of mounds.

The English is the editor's own. FIXES are the places where it followed a
reading that was corrected. Seventeen of its forty-two translator's notes
are left out (DROP): they discuss readings that are corrected here, or the
editor's own working rules. The section headings are the editor's.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr153'
REF = 'APP 53/17/0/-/Konin Gr.153'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes-oblatae [protocollon] 1782 (53.17.0.-.Konin Gr.153)"

# (file, x of the fold or None for a single page, left page, right page).
# First proposals; the editor's saved folds (folds.json beside this file) are
# used instead where they exist.
SCANS = [
    ('Image00003.jpg', None, '1391_a2', None),
    ('Image00004.jpg', 2425, '1392_a1', '1392_a2'),
    ('Image00005.jpg', 2472, '1393_a1', '1393_a2'),
    ('Image00006.jpg', 2473, '1394_a1', '1394_a2'),
    ('Image00007.jpg', 2450, '1395_a1', '1395_a2'),
    ('Image00008.jpg', 2483, '1396_a1', '1396_a2'),
    ('Image00009.jpg', 2445, '1397_a1', '1397_a2'),
    ('Image00010.jpg', 2454, '1398_a1', '1398_a2'),
    ('Image00011.jpg', 2459, '1399_a1', '1399_a2'),
    ('Image00012.jpg', 2455, '1400_a1', '1400_a2'),
    ('Image00013.jpg', 2449, '1401_a1', '1401_a2'),
    ('Image00014.jpg', 2448, '1402_a1', '1402_a2'),
    ('Image00015.jpg', 2492, '1403_a1', '1403_a2'),
    ('Image00016.jpg', 2471, '1404_a1', '1404_a2'),
]
SKIP = ('1403_a2',)
LEAF = {'1391_a2': '1391 recto', '1392_a1': '1391 verso', '1392_a2': '1392 recto', '1393_a1': '1392 verso', '1393_a2': '1393 recto', '1394_a1': '1393 verso', '1394_a2': '1394 recto', '1395_a1': '1394 verso', '1395_a2': '1395 recto', '1396_a1': '1395 verso', '1396_a2': '1396 recto', '1397_a1': '1396 verso', '1397_a2': '1397 recto', '1398_a1': '1397 verso', '1398_a2': '1398 recto', '1399_a1': '1398 verso', '1399_a2': '1399 recto', '1400_a1': '1399 verso', '1400_a2': '1400 recto', '1401_a1': '1400 verso', '1401_a2': '1401 recto', '1402_a1': '1401 verso', '1402_a2': '1402 recto', '1403_a1': '1402 verso', '1403_a2': '1403 recto', '1404_a1': '1403 verso', '1404_a2': '1404 recto'}
LEAVES = ['1391', '1391v', '1392', '1392v', '1393', '1393v', '1394', '1394v', '1395', '1395v', '1396', '1396v', '1397',
          '1397v', '1398', '1398v', '1399', '1399v', '1400', '1400v', '1401', '1401v', '1402', '1402v', '1403v', '1404']


def page_of(leaf):
    n = int(leaf.rstrip('v'))
    return '%d_a1' % (n + 1) if leaf.endswith('v') else '%d_a2' % n


DOCS = [(1, [page_of(l) for l in LEAVES[:-1]]), (2, ['1404_a2'])]
FOLD_NOTE = ('All fourteen scans are shown. The first is a single page. Of the thirteen openings, every half is a page of '
             'the edition except the blank right-hand page of the last but one.')


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [l for l, _ in leaves] == LEAVES, [l for l, _ in leaves]
    return {(2 if l == '1404' else 1, page_of(l)): p for l, p in leaves}


FULL = courtbook.full_check(HERE)

JUR = '"Jur~to" on the scan: jurato, sworn, not "jurisdictione"'
JUR2 = JUR + ' (corrected on the ground of the places looked at; this one was not)'
CON = '"Cond~nis" / "Cond~lis" on the scan: condescensio, the sitting on the ground, not "conditio"'
CON2 = CON + ' (corrected on the ground of the places looked at; this one was not)'
GOR = 'the name is Gorski: so on leaf 1391 verso, and so he signs in Konin Gr.118'

# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('1391_a2', 'tum sub alterno inferius', 'tum subalterno inferius', 'one word on the scan: a subaltern decree, specified below'),
    ('1391_a2', 'Geomethra Jurisdictione et Privilegiato', 'Geomethra Jurato et Privilegiato', JUR),
    ('1391_a2', 'Commissario Graniciali Jurisdictionis Majoris Poloniae', 'Commissario Generali Jurato Majoris Poloniae',
     'the scan has "Commissario Gnali Jurto": the sworn general commissioner, as Łukaszewicz signs on leaf 1404'),
    ('1392_a1', 'ad actum praesentibus conjugatis', 'ad actum praesentem congregatis', 'the scan has "ad Actum praesen Congregatis": gathered for the act'),
    ('1392_a1', 'authentico et jurisdictione actum praesentium acclamante', 'authentico et jurato actum praesentem acclamante', JUR),
    ('1392_a1', 'Equitem actorem, __ per Magnificum', 'Equitem actorem et c[itatum] per Magnificum',
     'the scan has "actt et C" at the edge of the page: actorem et citatum, as on leaf 1404'),
    ('1392_a1', 'citatos et actores personaliter Generosum Jacobum Gerski', 'citatum et actorem personaliter Generosum Jacobum Gorski',
     'the scan has "Citt et Actt pnltr", of Chełmski alone; and "Gorski"'),
    ('1392_a1', 'Ignatium Ijazdowski', 'Ignatium Ujazdowski', 'the scan has "Ujazdowski"'),
    ('1392_a1', 'ad objectam latere conditionem die undecima mensis 7bris anno 1780 in conditionis in fundo',
     'ad objectam latere condemnationem die undecima mensis 7bris anno 1780 in condescensionis in fundo',
     'the scan has "Condonem" with a mark, condemnationem (the same condemnation is "objecta sibi condemnatione" at the foot of the '
     'page), and "Condnis", condescensionis'),
    ('1392_a1', 'judicio praesenti ordinarium generale', 'judicium praesens ordinarium generale', 'the scan has "Judm praesens Ordinarium Gnale"'),
    ('1392_a1', 'quoniam non dicit imo', 'quoniam non [do]cet imo', 'the scan has "non" at the cut edge and "cet" on the next line: he does not show it'),
    ('1392_a2', 'conditioneque in ordine', 'condescensioneque in ordine', CON2),
    ('1392_a2', 'Jacobum Gerski', 'Jacobum Gorski', GOR),
    ('1393_a1', 'siparitionem[?]', 'sipationem', 'the word is "Sipationem" where it was looked at, on leaf 1400 verso: the raising of mounds (Polish "sypanie")'),
    ('1393_a1', 'actu officii conditionali', 'actu officii condescensoriali', CON2),
    ('1393_a1', 'per officii conditionalia', 'per officii condescensorialia', CON2),
    ('1393_a2', 'siparitione[?]', 'sipatione', 'the word is "Sipationem" where it was looked at, on leaf 1400 verso'),
    ('1393_a2', 'supra conditionalem facta', 'supra condescensorialem facta', CON2),
    ('1393_a2', 'officii conditionali campestri', 'officii condescensoriali campestri', CON2),
    ('1393_a2', 'decretis conditionalibus', 'decretis condescensorialibus', CON2),
    ('1394_a2', 'variis conditionum terminis', 'variis condescensionum terminis', CON2),
    ('1395_a1', 'conditionem judiciorum', 'condescensionem judiciorum', CON2),
    ('1395_a1', 'verò conditionis graniciali', 'verò condescensionis graniciali', CON2),
    ('1395_a2', 'geomethrae jurisdictionem à diamethro', 'geomethrae jurato à diamethro', JUR),
    ('1395_a2', 'geomethram jurisdictionem perfecisse', 'geomethram juratum perfecisse', JUR),
    ('1395_a2', 'campestria conditionalia revisam', 'campestria condescensorialia revisam', CON),
    ('1395_a2', 'officia conditionalia secum', 'officia condescensorialia secum', CON2),
    ('1396_a1', 'officium conditionali ad', 'officium condescensoriali ad', CON),
    ('1396_a1', 'geomethras jurisdictionis circa', 'geomethras juratos circa', JUR),
    ('1396_a1', 'Privilegiatum et Jurisdictionem', 'Privilegiatum et Juratum', JUR2),
    ('1396_a2', 'per geomethram jurisdictionem ad erectionem', 'per geomethram juratum ad erectionem', JUR2),
    ('1397_a1', 'necessariam esse conditionem', 'necessariam esse condescensionem', CON2),
    ('1397_a1', 'geomethra jurisdictionis, Gnesniensis', 'geomethra jurato, Gnesniensis', JUR),
    ('1397_a1', 'geomethrae jurisdictio perficere', 'geomethrae jurato perficere', JUR),
    ('1398_a1', 'proxime incidenti conditionis', 'proxime incidenti coram',
     'the scan has "Coram" and the catchword "Offo": before the office and records of the castle court of Poznań'),
    ('1398_a2', 'campestri conditionali quod', 'campestri condescensoriali quod', CON2),
    ('1399_a1', 'officia conditionalia campestria', 'officia condescensorialia campestria', CON2),
    ('1399_a1', 'Magnificus Gerski Camerarius', 'Magnificus Gorski Camerarius', GOR),
    ('1399_a1', 'eundem Magnificum Gerski', 'eundem Magnificum Gorski', GOR),
    ('1400_a1', 'notarius Terraris Palatinatus', 'notarius Terrestris Palatinatus', 'the scan has "Trris" with a mark: Terrestris, land notary'),
    ('1400_a1', 'Judicium officii decreti campestris camerarialis', 'Judicium officii campestris camerarialis', 'there is no "decreti" on the scan'),
    ('1400_a1', 'decretaque tribunalis complexas', 'decretoque tribunalis complexas', 'the scan has "Decretoque"'),
    ('1400_a1', 'veri nobilis, regni, granatialis capite libri', 'voce ministerialis, regni, generalis in capite libri',
     'the scan has "Voce Mlis, Rni, Gnalis in Capite Libri": by the voice of the court messenger named at the head of the book'),
    ('1400_a1', 'diem crastinam vidulit 29', 'diem crastinam videlicet 29', 'the scan has "vidlt" with a mark: videlicet'),
    ('1400_a2', 'Comitis Sierabowski', 'Comitis Sierakowski', 'the scan has "Sie|rakowski"; the editor\'s English has the name right'),
    ('1400_a2', 'Kęszycki Clia', 'Kęszycki Castellani', 'the scan has "Cllni" with a mark, before "Gnesn" on the next page: castellan of Gniezno'),
    ('1401_a1', '_ lineam quam rectissimam', 'lineam quam rectissimam', 'the mark is a flourish that fills the line; no word is missing'),
    ('1401_a1', 'actus conditionis ob', 'actu condescensionis ob', 'the scan has "in anteriori Actu Condnis"'),
    ('1401_a1', 'siparitionem[?]', 'sipationem', 'the scan has "ad Sipationem Seu Erectionem Scopulorum"'),
    ('1401_a1', 'diem sequentum crastinam', 'diem sequentem crastinam', 'the scan has "Sequentem"'),
    ('1401_a1', 'Sabbatho ipso facto', 'Sabbatho ipso Festo', 'the scan has "ipso Festo", with "Sancti Andreae Apostoli" on the next page: on the feast itself'),
    ('1401_a2', 'in actu specificat[ionis] linea recta formata', 'in actu specificatorum linea recte formata',
     'the scan has "Specificator" with a mark and "recte": the corner mounds specified in the act'),
    ('1402_a1', 'ubi ab advesperascentem diem actuum suum', 'ubi ob advesperascentem diem actum suum', 'the scan has "ob" and "Actum"'),
    ('1403_a1', 'in scopulos impun[ia?] consueta', 'in scopulos imponi consueta', 'the scan has "imponi": the signs customarily put into mounds'),
    ('1403_a1', 'et nomine contradicente', 'et nemine contradicente', 'the scan has "Nemine": no one contradicting, as the editor\'s English has it'),
    ('1403_a1', 'Franz-Xaverius Rawicz', 'Franciscus Xaverius Rawicz', 'the signature has "Franc" with a mark'),
    ('1404_a1', 'ad acti camae ad actis hisce', 'ad acticandum et actis hisce', 'the scan has "ad Acticandum et actis hisce": to be entered in the acts'),
    ('1404_a1', 'ac ei[j]dem insutum', 'ac iisdem insutum', 'the scan has "iisdem"'),
    ('1404_a2', 'Praesentibus Generosus Michaële', 'Praesentibus Generosis Michaële', 'the scan has "Generosis"'),
    ('1404_a2', 'actum praesentium acclamante', 'actum praesentem acclamante', 'the scan has "presentem"'),
    ('1404_a2', 'cathegoriam granicialium', 'cathegoriam granicialem', 'the scan has "Granicialem"'),
    ('1404_a2', 'Prusimski conduendo redderet', 'Prusimski conducendo redderet', 'the scan has "Conducendo"'),
    ('1404_a2', 'in actu aliam positionem praeciso', 'in actualem possessionem praeciso', 'the scan has "in actualem possessionem": into actual possession'),
    ('1404_a2', 'circa actum hinc personali praesentis', 'circa actum hunc personaliter praesentis',
     'the scan has "Circa actum hunc personaliter presentis": Prusimski was present in person'),
    ('1404_a2', 'possessione nomine impugnante', 'possessione nemine impugnante', 'the scan has "nemine": no one opposing'),
    ('1404_a2', 'obedientiae eundem reliquit pro ut relinquit actus praesentia vigore', 'obedientia eundem reliquit prout relinquit actus praesentis vigore',
     'the scan has "obedientia" and "actus presentis vigore": obedience having been enjoined on Hunt'),
    ('1404_a2', 'Generalis Commissarius Officialis', 'Generalis Commissarius mp', 'after "Commissarius" the scan has only the flourish of "manu propria"'),
]

# The editor's notes that discuss a reading corrected here (3, 5, 7, 8, 15, 30 to 35, 38, 39, 41, 42), the name of the
# monk Tesselin, who is known from Konin Gr.118 (28), and a working rule of the editor's (40).
DROP = ('3', '5', '7', '8', '15', '28', '30', '31', '32', '33', '34', '35', '38', '39', '40', '41', '42')
FIXES = [
    ('another road running from Zagórowo and Drzewce', 'another road running from Zagórów and Drzewce',
     'the form of the name used in the edition; the Latin has "de Zagurowo"'),
    ('licensed and privileged geometer', 'sworn and privileged geometer', '"Geomethra Jurato et Privilegiato"'),
    ('Józef Łukaszewicz, Boundary Commissioner of Greater Poland', 'Józef Łukaszewicz, sworn General Commissioner of Greater Poland',
     '"Commissario Generali Jurato Majoris Poloniae"'),
    ('authenticated and jurisdictional, proclaiming', 'authentic and sworn, proclaiming', '"authentico et jurato"'),
    ('plaintiff, [unclear] through the Right Honourable Maciej Rudnicki', 'plaintiff and cited, through the Right Honourable Maciej Rudnicki',
     '"actorem et c[itatum]"'),
    ('Ignacy Ijazdowski', 'Ignacy Ujazdowski', '"Ujazdowski"'),
    ('concerning the field inspection alleged on that side, conducted on 11 September 1780 at the estate of Grab pursuant to the Tribunal decree,',
     'concerning the condemnation objected from that side, obtained on 11 September 1780 at the field inspection held at the estate of Grab '
     'pursuant to the Tribunal decree,', '"ad objectam latere condemnationem ... obtentam": what is objected is the condemnation'),
    ('Starost of Niszczewice, a condemnation having been obtained to his advantage for the contravention',
     'Starost of Niszczewice, to his advantage, for the contravention', 'the same'),
    ('since he does not contest this but rather', 'since he does not demonstrate it but rather', '"quoniam non [do]cet"'),
    ("had ordered the geometer's jurisdiction to complete the straight line", 'had ordered the sworn geometer to complete the straight line', '"geomethrae jurato"'),
    ("had been completed by the geometer's jurisdiction in accordance", 'had been completed by the sworn geometer in accordance', '"geomethram juratum"'),
    ('licensed geometers are obliged', 'sworn geometers are obliged', '"geomethras juratos"'),
    ('Licensed and Jurisdictional Geometer', 'Privileged and Sworn Geometer', '"Geomethram Privilegiatum et Juratum"'),
    ("as accurately as possible by the geometer's jurisdiction, for", 'as accurately as possible by the sworn geometer, for', '"per geomethram juratum"'),
    ('a licensed geometer also having first been engaged', 'a sworn geometer also having first been engaged', '"geomethra jurato"'),
    ("he shall order, the geometer's jurisdiction to complete the straightest", 'he shall order, the sworn geometer to complete the straightest',
     '"geomethrae jurato"'),
    ('The court of the boundary decree field office of the Gniezno Voivodeship, by virtue',
     "The court of the Boundary Surveyor's field office of the Gniezno Voivodeship, by virtue", '"Judicium officii campestris camerarialis"'),
    ('guarded by the [Court Summoner], true noble of the realm, boundary [official], expressed by name at the head of the book',
     'guarded by the voice of the general Court Summoner of the realm, expressed by name at the head of the book',
     '"voce ministerialis, regni, generalis in capite libri de nomine expressi"'),
    ('Kęszycki, [Clia]', 'Kęszycki, Castellan', '"Castellani"'),
    ('[gap] to form the straightest', 'to form the straightest', 'no word is missing'),
    ('Franz Ksawery Rawicz Jasiński', 'Franciszek Ksawery Rawicz Jasiński', '"Franciscus Xaverius"'),
    ("for the act of the [boundary surveyor's] court, to be left in the original in these records",
     'to be entered in the acts and left in the original in these records', '"ad acticandum et actis hisce in originali relinquendum"'),
    ('at a calculated reckoning, in a separately described act — the same decree', 'at a calculated reckoning — the same decree',
     '"in actualem possessionem", which the English already had; "in actu aliam positionem" was a misreading of the same words'),
    ('Prusimski, from this act, by personal presence;', 'Prusimski, who was present in person at this act;', '"circa actum hunc personaliter praesentis"'),
    ('and left the said Freeborn Martin Hunt in peaceful possession, no one challenging, under no process having been declared, on behalf of the '
     'Most Honourable Prusimski, Starost of Niszczewice, in obedience to him —',
     'and left him in peaceful possession, no one challenging, obedience to the Most Honourable Prusimski, Starost of Niszczewice, having been '
     'enjoined on the said Freeborn Martin Hunt —', '"nemine impugnante indicta suprascripto Ingenuo Martino Hunt ... obedientia"'),
    ('General Commissioner Official of the Greater Poland Voivodeship.', 'General Commissioner of the Greater Poland Voivodeship, by his own hand.',
     '"Generalis Commissarius mp"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*English*.md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0], drop_notes=tuple(DROP) + tuple(FULL['DROP']))
    assert [l for l, _ in leaves] == LEAVES[:24] + ['1403v', '1403v', '1404'], [l for l, _ in leaves]
    n = sum(x.count('Gerski') for _, p in leaves for x in p)
    m = sum(x.count('[uncertain: demarcation]') for _, p in leaves for x in p)
    assert (n, m) == (4, 3), (n, m)
    leaves = [(l, [x.replace('Gerski', 'Gorski').replace('[uncertain: demarcation]', 'raising') for x in p]) for l, p in leaves]
    E = courtbook.fix_english({i: p for i, (_, p) in enumerate(leaves)}, FIXES + FULL['FIXES'])
    assert E[25][-1].startswith('[Section 6'), E[25][-1]
    j = '\n\n'.join
    return {1: [j(E[i]) for i in range(24)] + [j(E[24] + E[25][:-1])], 2: [j(E[25][-1:] + E[26])]}


S = {
 1: ('Dekret des Feldgerichts von Franciszek Ksawery Jasiński, Grenzkämmerer der Woiwodschaft Gnesen, begonnen am 28. November 1782 auf dem Grund von Trąbczyn bei den drei Eckhügeln von Trąbczyn Minus oder Nowa Wieś, Łukom und Drzewce. Es rückt das Dekret des Krontribunals in Petrikau vom 17. Oktober 1782 zwischen Antoni Prusimski, Starost von Niszczewice, und Stanisław Chełmski, Schatzmeister von Wschowa, im Wortlaut ein; geladen waren auch die Grenzkämmerer Jakub Górski von Inowrocław und Alojzy Orłowski vom Land Dobrzyń sowie Abt Lubstowski und der Konvent von Ląd. Das Tribunal hält fest: Die von den Ständen eingesetzte Kommission hatte den Grenzstreit durch zwei einander widersprechende, in Abwesenheit ergangene Dekrete entschieden; nach dem Gesetz von 1776 kamen beide Parteien vor das Tribunal, das am 23. Januar 1782 endgültig entschied. Jenes Dekret bestimmte den Eckpunkt von Trąbczyn und Łukom mit Drzewce und den Endpunkt mit Biskupice so, wie die Karte sie zeigt, und bestätigte darin das Dekret der von Prusimski beigezogenen Kommissare; dazwischen zog es auf der Karte eine gerade Linie, vom Präsidenten und vom Marschall unterschrieben. Die Olęder, die Chełmski in Besitz genommen hatte, waren Prusimski zurückzugeben, bis auf einen, Martin Hunt, der Chełmski belassen wurde; das geschah am 6. März und wurde am 18. März in Konin eingetragen. Beim Ortstermin am 27. Mai zog der vereidigte Geometer die Linie; Hunt lag aber nicht auf der Chełmski zugesprochenen rechten Seite, und die beiden Feldämter gingen auseinander: Das von Dobrzyń verwies die Sache an das Tribunal zurück, das von Inowrocław wollte die Linie so verbessern, dass die Stelle einer vor vier Jahren abgebrannten Olęder-Stelle rechts bliebe, was Chełmski ablehnte. Das Tribunal entscheidet: Ein vereidigter Geometer hat nur Grenzzüge und Grenzzeichen zu vermessen, Häuser trägt er bloß der Lage nach ein; das Dekret vom 23. Januar ist unabänderlich und zu erfüllen, die Akten beider Feldämter werden aufgehoben. Binnen sechs Wochen soll ein Unterkämmerer oder Kämmerer mit einem vereidigten Geometer auf dem Grund erscheinen, die Linie von den drei Eckhügeln bis zum Endpunkt mit Biskupice ziehen lassen und nur Wandhügel errichten; was rechts der Linie liegt, gehört zu Łukom, was links liegt, zu Trąbczyn oder Nowa Wieś; die 1775 von Chełmskis Kommissaren errichteten Hügel sind alle, die von Prusimskis Kommissaren errichteten Wandhügel ebenfalls zu schleifen. Weil Martin Hunt nicht rechts der Linie sitzt, hat Chełmski ihn binnen sechs Wochen vor dem Kommissar der großpolnischen Woiwodschaft in Prusimskis Besitz zu übergeben, bei Strafe der Verbannung. Chełmski soll Prusimski die schon zuerkannte Summe für die von den Olędern bezogenen Einkünfte samt Strafgeldern am 20. Januar 1783 in Posen zahlen. Górski, den Prusimski beigezogen hatte, wird wegen der eigenmächtigen Verbesserung der Linie zu einer Woche Turmhaft in der Burg Radziejów und zu einer Geldbuße an Chełmski verurteilt; Orłowski, den Chełmski beigezogen hatte, wegen der unbegründeten Rückverweisung zu einer Geldbuße an Prusimski. Der Konvent von Ląd wird von der geforderten Strafe freigesprochen: Sein Protest in Posen vom 26. Juni war nur vorsorglich und ist am 16. Oktober zurückgenommen worden. Der Vollzug: Am 29. November erschien Prusimski, Chełmski blieb aus; Prusimski legte die Karte mit der vom Präsidenten Sebastian Sierakowski und vom Marschall Ksawery Kęszycki unterschriebenen Linie vor, und der vereidigte Geometer Benedykt Woronowski, Kanoniker von Łęczyca, stellte die Linie mit Stangen her. Am 30. November, am 2. und am 3. Dezember ließ das Gericht entlang der Linie einundvierzig Wandhügel aufwerfen und im Sumpf namens Stawisko einunddreißig Pfähle aus Erle und Eiche einschlagen; am 2. Dezember erschien Chełmski persönlich. Der letzte Hügel steht zwölfeinhalb Ruten vor den Endhügeln von Trąbczyn, Łukom und Biskupice, die unberührt blieben; jeder Hügel misst sechs Ellen im Geviert und enthält als Zeichen fünf Steine in Kreuzform, Ziegelstücke, Glasscherben und Kohle. Danach ließ das Gericht die älteren Hügel schleifen und für nichtig erklären; Jasiński hat unterschrieben. Ein Vermerk hält fest, dass Leon Maszewski das Dekret am 7. Dezember 1782 dem Burgamt Konin vorgelegt hat und das Original in die Akten eingeheftet wurde.',
     "The decree of the field court of Franciszek Ksawery Jasiński, boundary chamberlain of the palatinate of Gniezno, begun on 28 November 1782 on the ground of Trąbczyn at the three corner mounds of Trąbczyn Minus or Nowa Wieś, Łukom and Drzewce. It copies in full the decree of the Crown Tribunal at Piotrków of 17 October 1782 between Antoni Prusimski, Starost of Niszczewice, and Stanisław Chełmski, Treasurer of Wschowa; the boundary chamberlains Jakub Górski of Inowrocław and Alojzy Orłowski of the land of Dobrzyń, and Abbot Lubstowski and the convent of Ląd, were cited too. The Tribunal records: the commission appointed by the Estates had decided the boundary cause by two decrees that contradicted each other and were given in default; under the law of 1776 both parties came before the Tribunal, which gave its final decree on 23 January 1782. That decree fixed the corner of Trąbczyn and Łukom with Drzewce and the end point with Biskupice as the map shows them, confirming on that point the decree of the commissioners engaged by Prusimski; between the two it drew a straight line on the map, signed by the President and the Marshal. The Olęder settlers whom Chełmski had taken into possession were to be given back to Prusimski, all but one, Martin Hunt, who was left to Chełmski; this was done on 6 March and entered at Konin on 18 March. At the sitting on the ground on 27 May the sworn surveyor drew the line; but Hunt did not lie on the right-hand side adjudged to Chełmski, and the two field offices disagreed: that of Dobrzyń sent the cause back to the Tribunal, that of Inowrocław meant to correct the line so that the site of an Olęder holding burnt down four years before should stay on the right, which Chełmski refused. The Tribunal decides: a sworn surveyor has to measure only boundary lines and boundary signs, and marks houses merely by their position; the decree of 23 January cannot be changed and is to be carried out, and the acts of both field offices are quashed. Within six weeks a sub-chamberlain or chamberlain is to come to the ground with a sworn surveyor, have the line drawn from the three corner mounds to the end point with Biskupice, and raise wall mounds only; what lies to the right of the line belongs to Łukom, what lies to the left to Trąbczyn or Nowa Wieś; the mounds raised in 1775 by Chełmski's commissioners are all to be levelled, and the wall mounds raised by Prusimski's commissioners as well. Because Martin Hunt does not sit to the right of the line, Chełmski is to hand him over into Prusimski's possession within six weeks before the commissioner of the palatinate of Greater Poland, on pain of banishment. Chełmski is to pay Prusimski the sum already adjudged for the revenue drawn from the Olęder settlers, with penalties, on 20 January 1783 at Poznań. Górski, whom Prusimski had engaged, is sentenced for correcting the line on his own authority to a week in the tower of Radziejów castle and a money penalty to Chełmski; Orłowski, whom Chełmski had engaged, for sending the cause back without ground, to a money penalty to Prusimski. The convent of Ląd is freed from the penalty claimed: its protest at Poznań of 26 June was only a precaution and was withdrawn on 16 October. The execution: on 29 November Prusimski appeared and Chełmski stayed away; Prusimski produced the map with the line signed by the President, Sebastian Sierakowski, and the Marshal, Ksawery Kęszycki, and the sworn surveyor Benedykt Woronowski, canon of Łęczyca, set out the line with poles. On 30 November and on 2 and 3 December the court had forty-one wall mounds thrown up along the line and thirty-one stakes of alder and oak driven into the marsh called Stawisko; on 2 December Chełmski appeared in person. The last mound stands twelve and a half perches short of the end mounds of Trąbczyn, Łukom and Biskupice, which were left untouched; each mound measures six cubits square and holds as signs five stones in the form of a cross, pieces of brick, broken glass and charcoal. The court then had the older mounds levelled and declared void; Jasiński signed. A note records that Leon Maszewski brought the decree to the castle office at Konin on 7 December 1782 and that the original was sewn into the records."),
 2: ('Urkunde vom 28. November 1782, aufgenommen in der Trąbczyner Olęder-Siedlung im Haus von Martin Hunt, in Gegenwart von Michał Brzeżański, Leon Maszewski und anderen; der Gerichtsbote Bartłomiej Szepczyński von Trąbczyn rief die Handlung aus. Das Kommissariatsamt der großpolnischen Woiwodschaft handelt nach dem Dekret des Krontribunals in Petrikau vom 17. Oktober desselben Jahres zwischen Antoni Prusimski, Starost von Niszczewice, und Stanisław Chełmski, Schatzmeister von Wschowa. Danach sitzt der Olęder Martin Hunt nicht rechts der vom Tribunal bestimmten Linie und kann nicht Chełmski gehören, der ihn bis dahin besaß; Chełmski sollte ihn binnen sechs Wochen vor dem Kommissar an Prusimski herausgeben. Auf Verlangen Prusimskis, der persönlich anwesend ist, übergibt der Kommissar Martin Hunt in dessen tatsächlichen Besitz und verpflichtet Hunt zum Gehorsam gegenüber Prusimski; niemand widerspricht. Józef Łukaszewicz, Generalkommissar der großpolnischen Woiwodschaft, hat unterschrieben.',
     "An act of 28 November 1782, done in the Olęder settlement of Trąbczyn at the house of Martin Hunt, in the presence of Michał Brzeżański, Leon Maszewski and others; the court messenger Bartłomiej Szepczyński of Trąbczyn proclaimed the act. The commissioner's office of the palatinate of Greater Poland acts under the decree of the Crown Tribunal at Piotrków of 17 October of the same year between Antoni Prusimski, Starost of Niszczewice, and Stanisław Chełmski, Treasurer of Wschowa. By that decree the Olęder settler Martin Hunt does not sit to the right of the line the Tribunal fixed and cannot belong to Chełmski, who had held him until then; Chełmski was to give him up to Prusimski within six weeks before the commissioner. At the request of Prusimski, who is present in person, the commissioner delivers Martin Hunt into his actual possession and binds Hunt to obedience to Prusimski; no one objects. Józef Łukaszewicz, general commissioner of the palatinate of Greater Poland, signed."),
}
HOW = ('written in the working session from the Latin as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
