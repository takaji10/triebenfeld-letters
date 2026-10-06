# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.115: from the editor's scans and texts to the edition.

    python units/app53170koningr115/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is a rough register of the castle court of Konin for 1768 to 1774:
short entries, many to a page, each sitting under a line "Actum in Conin ...".
The editor photographed or received sixteen openings and transcribed the
entries that concern Trąbczyn and Łukom. Each entry is a document; two notes
of one sitting on one page are one document (docs/PRUSIMSKI_ERA_PLAN.md).

    doc  leaf        scan   page      what
    1    3v          006    0004_a1   note: Chełmski's citation of Prusimski (January 1768)
    2    35v         040    0036_a1   two notes of 17 May 1768: citations to the Tribunal
    3    37          041    0037_a2   note: Prusimski's approbation for quashing (May 1768)
    4    185v        186    0186_a1   note: the delivery of Lusnia brought in (2 December 1771)
    5    186v        187    0187_a1   Chełmski presents captured arms (20 December 1771)
    6    186v        187    0187_a1   report: the embankment broken, the inn shot at (same day)
    7    226         226    0226_a2   report: the inn's windows and doors carried off (1 December 1772)
    8    241, 241v   235,   0241_a2,  report for Prusimski: trees felled (26 February 1773)
                     236    0242_a1
    9    245         245    0245_a2   Chełmski's protest (March 1773)
    10   245         245    0245_a2   report: the inn wrecked on 29 January 1773 (March 1773)

Scans 006, 040, 041, 235 and 236 are photographs named by their number in a
series; the others are the archive's, named after the leaf on the right. Leaf
numbers were read off the pages. Page ids: leaf N recto is <N>_a2, leaf N
verso is <N+1>_a1. The other half of each of the nine scans is cut and set
apart. Seven scans (185, 224, 225, 227, 228, 244, 246) carry nothing that is
transcribed and are not used; nor is the subfolder "Incorrect Pages" (the
editor, 2026-10-06). "[47v]" in the editor's file has no text under it.

What read_source does to the editor's file beyond cutting it:
- the bold round the leaf marks, the italics, and three dictionary links the
  editor put on Polish words are taken off;
- the two notes on leaf 35 verso, which the editor gave as "Videatur hoc
  loco…", are given as far as they were read on the scan (NOTES_35V); "…"
  stands, as in the editor's file, for what is not transcribed;
- Stanisław Ścibor Chełmski's signature under his protest on leaf 245 is
  added (SIGNATURE). His signature also stands twice at the foot of leaf 186
  verso, under the two entries there; it is not clear which it signs, and it
  is not transcribed.

The check (2026-10-07). Read against the scans, enlarged: all of documents
5, 6 and 9, the second half of documents 7, 8 and 10, the notes 2 and 3, and
every heading and date line. ROWS has what was corrected.

The English. The editor's file translates documents 4 to 10. The three early
notes (1 to 3) had no English; they are translated here (EARLY), in the
editor's terms. FIXES are the places where the editor's English followed a
reading that was corrected.
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr115'
REF = 'APP 53/17/0/-/Konin Gr.115'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1768-1774 (53.17.0.-.Konin Gr.115)"

# (file, x of the fold, left page, right page). First proposals; the editor's
# saved folds (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('006.jpg', 2136, '0004_a1', '0004_a2'),
    ('040.jpg', 2115, '0036_a1', '0036_a2'),
    ('041.jpg', 2133, '0037_a1', '0037_a2'),
    ('186.jpg', 2704, '0186_a1', '0186_a2'),
    ('187.jpg', 2716, '0187_a1', '0187_a2'),
    ('226.jpg', 2625, '0226_a1', '0226_a2'),
    ('235.jpg', 1963, '0241_a1', '0241_a2'),
    ('236.jpg', 1963, '0242_a1', '0242_a2'),
    ('245.jpg', 2711, '0245_a1', '0245_a2'),
]
SKIP = ('0004_a2', '0036_a2', '0037_a1', '0186_a2', '0187_a2', '0226_a1', '0241_a1', '0242_a2', '0245_a1')
LEAF = {'0004_a1': '3 verso', '0004_a2': '4 recto', '0036_a1': '35 verso', '0036_a2': '36 recto',
        '0037_a1': '36 verso', '0037_a2': '37 recto', '0186_a1': '185 verso', '0186_a2': '186 recto',
        '0187_a1': '186 verso', '0187_a2': '187 recto', '0226_a1': '225 verso', '0226_a2': '226 recto',
        '0241_a1': '240 verso', '0241_a2': '241 recto', '0242_a1': '241 verso', '0242_a2': '242 recto',
        '0245_a1': '244 verso', '0245_a2': '245 recto'}
DOCS = [(1, ['0004_a1']), (2, ['0036_a1']), (3, ['0037_a2']), (4, ['0186_a1']), (5, ['0187_a1']), (6, ['0187_a1']),
        (7, ['0226_a2']), (8, ['0241_a2', '0242_a1']), (9, ['0245_a2']), (10, ['0245_a2'])]
FOLD_NOTE = ('Nine of the sixteen scans are shown: the ones with a transcribed entry. On each, one half is a page of the '
             'edition and the other is left out.')

NOTES_35V = [
    'Videatur hoc Loco Citationis ex Parte Magnifici Antonii de Kolno Prusimski Capitanei Nieszczeviensis In et Contra '
    'Magnificos Chełmski Successores Żychlinianos Ignatium Gałecki Capitaneum Bydgostiensem … Abbatem et Venerabilem '
    'Conventum Landensem pro Judiciis Tribunalis Regni Bidg~ ad Granitian~ editt~ Relatio In Productis.',
    'Videatur hoc Loco Citationis ex Parte Magnifici Stanislai Chełmski In et Contra Illustrem Reverendissimum Słowiecki '
    'Abbatem et Conventum Landensem Magnificos Prusimski Gałecki …',
]
SIGNATURE = 'Stanisław Scibor Chełmski mp'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    s = io.open(f[0], encoding='utf-8-sig').read().replace('\r\n', '\n').replace('**', '')
    s, n = re.subn(r'(?<!\\)\[([^\]\\]+)\]\(https?://[^)]+\)', r'\1', s)       # the editor's dictionary links
    assert n == 3, n
    parts = re.split(r'(?m)^\\\[(\d+v?)\\\]\s*$', s)
    assert not parts[0].strip()
    leaves = [(leaf, [re.sub(r'\s+', ' ', courtbook.plain(l)).strip() for l in t.split('\n') if l.strip()])
              for leaf, t in zip(parts[1::2], parts[2::2])]
    assert [l for l, _ in leaves] == ['3v', '35v', '37', '47v', '185v', '186v', '226', '241', '241v', '245'], [l for l, _ in leaves]
    L = dict(leaves)
    assert L['47v'] == [] and [len(L[k]) for k in ('3v', '35v', '37', '185v', '186v', '226', '241', '241v', '245')] == \
        [2, 5, 2, 3, 5, 3, 3, 1, 4], [len(v) for v in L.values()]
    n35 = list(L['35v'])
    assert n35[2] == n35[4] == 'Videatur hoc loco…', n35
    n35[2], n35[4] = NOTES_35V
    return {
        (1, '0004_a1'): L['3v'],
        (2, '0036_a1'): n35,
        (3, '0037_a2'): L['37'],
        (4, '0186_a1'): L['185v'],
        (5, '0187_a1'): L['186v'][:3],
        (6, '0187_a1'): L['186v'][3:],
        (7, '0226_a2'): L['226'],
        (8, '0241_a2'): L['241'],
        (8, '0242_a1'): L['241v'],
        (9, '0245_a2'): L['245'][:2] + [SIGNATURE],
        (10, '0245_a2'): L['245'][2:],
    }


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0004_a1', 'Stanislai Chełmski In[?] Contra Magnificos', 'Stanislai Chełmski In et Contra Magnificos',
     'the scan has "In" at the end of one line and "et Contra" at the head of the next'),
    ('0037_a2', 'Pro Parte M Prusimski Approbatus ad Cassan~ factae Oblata', 'Pro Parte M Prusimski Approbationis ad Cassan~ factae Oblata',
     'the scan has "Approbatis" with a mark of abbreviation: Approbationis, as "Approbationem" in the note itself'),
    ('0037_a2', 'Deprompti et probationem Termini ad Cassanam Condemnationem', 'Deprompti et Approbationem Termini ad Cassandam Condemnationem',
     'the scan has "et Ap|probationem" over the line end, and "Cassandam"'),
    ('0187_a1', 'Ministerialis Regni Generalis existens Commissione Magnifici', 'Ministerialis Regni Generalis Speciali Commissione Magnifici',
     'the scan has "Speciali Commissione", after a word struck out: by special commission'),
    ('0187_a1', 'Hollandis Superind[i?]ficata ad Bona', 'Hollandis Superin[ae]dificata ad Bona',
     'the scan has "Superindificata" with a blot on the middle: superinaedificata, built upon by the settlers'),
    ('0187_a1', 'Quae sic praesentata rustus adse recepit', 'Quae sic praesentata rursus ad se recepit', 'the scan has "rursus ad se"'),
    ('0187_a1', 'Feria Secunda Immediate praeterita[?] Fundum', 'Feria Secunda Immediate praeterita Fundum',
     'the word is plain on the scan; a word after it is struck out'),
    ('0187_a1', 'Zniesione i Wodą z ryby wypuszczoną', 'Zniesione i Wodę z rybą wypuszczoną', 'the scan has "Wodę z rybą": the water let out with the fish'),
    ('0187_a1', 'wyciętych Dziur Osn w blochach', 'wyciętych Dziur Osm w blochach', 'the scan has "Osm", eight'),
    ('0187_a1', 'per Subditos Trąmpczyną plus quam Triginta Congregatos de nomine ex post Specificato',
     'per Subditos Trąmpczynenses plus quam Triginta Congregatos de nomine ex post Specificandos',
     'the scan has "Trąmpczynen" and "Specifican" with marks of abbreviation: the subjects of Trąbczyn, to be named afterwards'),
    ('0226_a2', 'Lusnensem possedit ac Officiose Condescenderat', 'Lusnensem personaliter ac Officiose Condescenderat',
     'the scan has "pslr" with a mark: personaliter, the set phrase (as in the report on leaf 241 verso)'),
    ('0226_a2', 'Fenestras Treis Januas', 'Fenestras Tres Januas', 'the scan has "Tres"'),
    ('0226_a2', 'per Nobili Lipinski Economum Trąmpczyniensem Radzewski Notatorem Proventualis Vladarium',
     'per Nobilem Lipinski Economum Trąmpczyniensem Radzewski Notatorem Proventualem Vladarium',
     'the scan has "Nobilem" and "Proventualem"'),
    ('0226_a2', 'ad Attentandos Tumultus Instrumentorum evicta esse', 'ad Attentandos Tumultus Instructorum evecta esse',
     'the scan has "Instructorum evecta": carried off with a band of subjects fitted out to make a tumult'),
    ('0242_a1', 'et Prata[?] ad Bona', 'et Prata ad Bona', 'the word is plain on the scan'),
    ('0242_a1', 'Kąty voci[t?]atis', 'Kąty vocitatis', 'the word is plain on the scan'),
    ('0242_a1', 'tum Hominis de Bonis Podbiele', 'tum Homines de Bonis Podbiele', 'the scan has "Homines": men, not one man'),
    ('0245_a2', 'Magnifici Chełmski contra Magnifici Prusimski Manifestatur', 'Magnifici Chełmski contra Magnificum Prusimski Manifestatio',
     'the heading has "M. Chełmski con. M. Prusimski Mnfstio" with a mark of abbreviation: Manifestatio, a protest'),
    ('0245_a2', 'Cum Attinentiis Haereditatis Hollandorum Lusnie', 'Cum Attinentiis Haeres Hollandorum Lusnie',
     'the scan has "Haeres": heir of Łukom, possessor of the settlers of Lusnia'),
    ('0245_a2', 'Jure Sibi Manifesti agnitam esse', 'Jure Sibi Manifestanti agnitam esse',
     'the scan has "Mnfsti" with a mark: Manifestanti, to him, the one protesting'),
    ('0245_a2', 'ex Speciali re[?] Mandato', 'ex Speciali ne Mandato', 'the scan has "ne": whether by special order or by connivance'),
    ('0245_a2', 'Conniventia Nobili[s?] Lipinski Economum Marzęcki Aulicum Cubicularem Suu[m]',
     'Conniventia Nobiles Lipinski Economum Marzęcki Aulicum Cubicularem Suum', 'the scan has "Nobiles" and "Suum"'),
    ('0245_a2', 'Violentias exegui Perpetrareque', 'Violentias exequi Perpetrareque', 'the scan has "exequi"'),
    ('0245_a2', 'fecit Eoque Omnia Se debite', 'fecit Eaque Omnia Se debite', 'the scan has "Eaque"'),
]

# The three early notes had no English in the editor's files.
EARLY = {
    1: ['On the part of the Right Honourable Chełmski against the Right Honourable Prusimski — Report of a Citation\n\n'
        'Let there be seen here, among the produced documents, the report of the citation issued on the part of the Right '
        'Honourable Stanisław Chełmski against the Right Honourables Antoni Prusimski and the successors of the late Right '
        'Honourable Prusimska, born Rozdrażewska, for the Kalisz land courts to be held here.'],
    2: ['Done in Konin on the Tuesday next after the Sunday Exaudi in the year of the Lord 1768.\n\n'
        'On the part of the Right Honourable Prusimski against the heirs and possessors of Łukom, Drzewce, Biskupice, '
        'Tomice — Report of a Citation\n\n'
        'Let there be seen here, among the produced documents, the report of the citation issued on the part of the Right '
        'Honourable Antoni Prusimski of Kolno, Starost of Niszczewice, against the Right Honourables Chełmski, the '
        'Żychliński successors, Ignacy Gałecki, Starost of Bydgoszcz, … the Abbot and the venerable Convent of Ląd, for the '
        'courts of the Crown Tribunal at Bydgoszcz, for the fixing of the boundary.\n\n'
        'On the part of the Right Honourable Chełmski against the heirs and possessors of Tomice, Drzewce, Trąbczyn, Nowa '
        'Wieś — Report of a Citation\n\n'
        'Let there be seen here the report of the citation on the part of the Right Honourable Stanisław Chełmski against '
        'the Most Reverend Słowiecki, Abbot, and the Convent of Ląd, the Right Honourables Prusimski, Gałecki …'],
    3: ['On behalf of the Right Honourable Prusimski — Oblata of the Approbation made for the Quashing\n\n'
        'Let there be seen here the Oblata, submitted among the produced documents, of an authentic extract drawn from the '
        'records of the municipal court of Bydgoszcz, containing the approbation of the term for quashing the condemnation, '
        'acknowledged by the Right Honourable Antoni Prusimski of Kolno, Starost of Niszczewice, before the municipal court '
        'records of Bydgoszcz.'],
}

FIXES = [
    ('Royal Court Summoner, General, being present, on commission from the Right Honourable Stanisław Ścibor Chełmski',
     'Royal Court Summoner, General, by special commission of the Right Honourable Stanisław Ścibor Chełmski',
     '"Speciali Commissione"'),
    ('in the pine forest called Lusnia, among the olędry assigned to the estates of Łukom now and from antiquity',
     'in the pine forest called Lusnia, built upon by the olędry, belonging to the estates of Łukom now and from antiquity',
     '"Hollandis superinaedificata ad Bona Łukom nunc et ab antiquo spectante"'),
    ("and the besieging of the innkeeper's goods by armed and lawless men",
     "and the besieging of the innkeeper's house by armed and lawless men",
     '"gaza" is a hut or house (as in the decree of 1728), not goods'),
    ('and concerning the removal of goods, [carried out] by licentious subordinate men',
     'and concerning the shooting through of the house, [carried out] by licentious subordinate men',
     '"in Trajectione vero Gazae": the shooting through of the house, which the report has just described'),
    ('and the water with the fish let out', 'and the water let out with the fish', '"Wodę z rybą wypuszczoną"'),
    ('for the purpose of fomenting disturbances by [their] instruments', 'fitted out for attempting disturbances',
     '"ad Attentandos Tumultus Instructorum": the band of subjects was equipped for it'),
    ('carried away from the pine forest beyond Lusnia;8 and then [by] a man of the Podbiele estates of the Right Honourable '
     'Zakrzewska',
     'carried away from the pine forest beyond Lusnia; and then [by] men of the Podbiele estate of the Right Honourable '
     'Zakrzewska',
     '"Homines"; the "8" was a stray note number'),
    ('possessor by force of his rights of the estates of Łukom with their appurtenances, of the olędry called Lusnia by '
     'hereditary title, lodged',
     'heir of the estates of Łukom with their appurtenances, possessor by force of his rights of the olędry called '
     'Lusnia, lodged', '"Bonorum Łukom cum attinentiis Haeres Hollandorum Lusnie vocitatorum vi jurium suorum Possessor"'),
    ('has been acknowledged to him by right of a previously lodged manifest, nonetheless, by the special mandate or '
     'connivance of the Honourable Lipiński [his] steward, [of] Marzęcki [his] chamber attendant, together with those '
     'recruited to them — Kazimierz, farm servant of the miller of Drzęzgi, Filip Wąchnicki, and others — permitted '
     '[them] to ride upon and attack the tavern and the olędry;',
     'has been acknowledged by law to him, the protester, nonetheless — whether by his special mandate or by his '
     'connivance — permitted the Honourables Lipiński, [his] steward, and Marzęcki, his chamber attendant, together with '
     'those recruited to them — Kazimierz, farm servant of the miller of Drzęzgi, Filip Wąchnicki, and others — to ride '
     'upon and attack the tavern and the olędry;',
     '"Jure Sibi Manifestanti agnitam"; "ex Speciali ne Mandato Sive Conniventia Nobiles Lipinski ... Marzęcki ... '
     'Superinequitare permissit": it is Prusimski\'s mandate or connivance, and the two men are the ones he let ride'),
]
SIGN_EN = 'Stanisław Ścibor Chełmski, by his own hand'


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [l for l, _ in leaves] == ['185v', '186v', '186v', '226', '241', '241v', '245', '245'], [l for l, _ in leaves]
    keys = ['185v', '186v-1', '186v-2', '226', '241', '241v', '245-1', '245-2']
    pages = courtbook.fix_english({k: p for k, (_, p) in zip(keys, leaves)}, FIXES_NOW)
    j = lambda k: '\n\n'.join(pages[k])
    out = dict(EARLY)
    out.update({4: [j('185v')], 5: [j('186v-1')], 6: [j('186v-2')], 7: [j('226')], 8: [j('241'), j('241v')],
                9: [j('245-1') + '\n\n' + SIGN_EN], 10: [j('245-2')]})
    return out


FIXES_NOW = [x for x in FIXES if x[0] != x[1]]

S = {
 1: ('Registervermerk im Buch des Burggerichts Konin, Januar 1768: Der Bericht über die Ladung, die Stanisław Chełmski gegen Antoni Prusimski und die Rechtsnachfolger der verstorbenen Prusimska, geborene Rozdrażewska, vor das Kalischer Landgericht erwirkt hat, liegt bei den vorgelegten Schriftstücken.',
     'A register note in the book of the castle court at Konin, January 1768: the report of the citation that Stanisław Chełmski obtained against Antoni Prusimski and the successors of the late Prusimska, born Rozdrażewska, before the Kalisz land court is among the documents produced.'),
 2: ('Zwei Registervermerke vom 17. Mai 1768 über Ladungen vor das Krontribunal in Bromberg. Antoni Prusimski von Kolno, Starost von Niszczewice, hat die Chełmski, die Żychliński-Erben, Ignacy Gałecki, Starost von Bromberg, sowie Abt und Konvent von Ląd laden lassen, zur Festlegung der Grenze; Stanisław Chełmski seinerseits den Abt Słowiecki und den Konvent von Ląd, Prusimski und Gałecki. Beide Vermerke sind nur teilweise transkribiert.',
     'Two register notes of 17 May 1768 on citations before the Crown Tribunal at Bydgoszcz. Antoni Prusimski of Kolno, Starost of Niszczewice, has had the Chełmskis, the Żychliński heirs, Ignacy Gałecki, Starost of Bydgoszcz, and the abbot and convent of Ląd cited, for the fixing of the boundary; Stanisław Chełmski for his part the abbot Słowiecki and the convent of Ląd, Prusimski and Gałecki. Both notes are transcribed only in part.'),
 3: ('Registervermerk vom Mai 1768: Für Antoni Prusimski von Kolno, Starost von Niszczewice, wird ein beglaubigter Auszug aus den Akten des Burggerichts Bromberg vorgelegt; er enthält die von ihm dort erklärte Anerkennung des Termins zur Aufhebung der Verurteilung.',
     'A register note of May 1768: for Antoni Prusimski of Kolno, Starost of Niszczewice, an authentic extract from the records of the castle court at Bydgoszcz is brought in; it contains the approbation, declared by him there, of the term for quashing the condemnation.'),
 4: ('Registervermerk vom 2. Dezember 1771: Für Stanisław Ścibor Chełmski, Erbherrn von Łukomia, wird die Besitzeinweisung in den Wald Lusnia mit den Olędern vorgelegt; sie liegt bei den vorgelegten Schriftstücken.',
     'A register note of 2 December 1771: for Stanisław Ścibor Chełmski, heir of Łukomia, the delivery of possession of the Lusnia wood with the Olęder settlers is brought in; it is among the documents produced.'),
 5: ('Eintrag vom 20. Dezember 1771. Der Gerichtsbote Nicolaus Krzepczyński von Myszaków legt im besonderen Auftrag von Stanisław Ścibor Chełmski dem Burgamt Konin Waffen vor: vier Säbel in Scheiden mit Riemen und einen blanken, vier Spieße mit eisernen Spitzen, drei lange Büchsen und eine mit Messing beschlagene Flinte, mit Blei und feinem Pulver geladen. Nach seiner Angabe hat Chełmski sie am vergangenen Montag im Wald Lusnia erbeutet, als Antoni Prusimski von Kolno, Starost von Niszczewice, dort gewaltsam einfiel und Bewaffnete das Haus des Schankwirts belagerten. Der Bote nimmt die Waffen wieder an sich.',
     'An entry of 20 December 1771. The court messenger Nicolaus Krzepczyński of Myszaków, by special commission of Stanisław Ścibor Chełmski, lays weapons before the castle office at Konin: four sabres in sheaths with belts and one unsheathed, four spears with iron points, three long guns and one gun mounted with brass, loaded with lead and fine powder. He states that Chełmski took them on the Monday before in the Lusnia wood, when Antoni Prusimski of Kolno, Starost of Niszczewice, broke in there by force and armed men besieged the innkeeper\'s house. The messenger takes the weapons back.'),
 6: ('Bericht des Gerichtsboten Nicolaus Krzepczyński vom 20. Dezember 1771, für Stanisław Ścibor Chełmski. Mit zwei Adligen, Antoni Wolski und Konstanty Folwarski, hat er am vergangenen Montag den Grund von Łukomia und den Wald Lusnia besichtigt. Am Teichgrund im Łukomer Wald sahen sie den Damm aufgegraben, das Wehr mit Pfosten, Schützen und Rinnen mit Äxten zerhauen und völlig beseitigt, das Wasser mit den Fischen abgelassen; dort lagen zwanzig frisch geschnittene dicke Knüppel. Im Schankhaus bei den Olędern im Wald Lusnia waren ringsum acht Schießlöcher in die Wände gehauen und drei Fenster zerschossen. Nach seiner Angabe geschah der Dammbruch durch mehr als dreißig Untertanen von Trąbczyn in Gegenwart Prusimskis, das Durchschießen des Hauses durch seine Leute auf seinen Befehl, am selben Tag.',
     'A report of the court messenger Nicolaus Krzepczyński of 20 December 1771, for Stanisław Ścibor Chełmski. With two noblemen, Antoni Wolski and Konstanty Folwarski, he inspected the ground of Łukomia and the Lusnia wood on the Monday before. At the pond-ground in the Łukom wood they saw the embankment dug through, the weir with its posts, sluices and channels hacked with axes and wholly removed, and the water let out with the fish; twenty thick clubs, freshly cut, lay there. In the tavern house among the Olęder settlers in the Lusnia wood eight loopholes had been cut in the walls all round and three windows shot out. He states that the breaking of the embankment was done by more than thirty subjects of Trąbczyn in Prusimski\'s presence, and the shooting through of the house by his men at his order, on the same day.'),
 7: ('Bericht des Gerichtsboten Joannes Bikierski von Węgierce vom 1. Dezember 1772, für Stanisław Ścibor Chełmski, Erbherrn von Łukom, Łomowo und Myszakowo und Besitzer der Olęder im Wald Lusnia. Mit zwei Adligen hat er am vergangenen Samstag das Schankhaus in Lusnia besichtigt: Drei Fenster und vier Türen mit eisernen Angeln waren aus dem Haus herausgenommen. Nach seiner Angabe haben das in derselben Nacht der Trąbczyner Verwalter Lipiński, der Schreiber Radzewski, der Vogt und Waldhüter und der Hofdiener Wąchnicki auf Befehl von Antoni Prusimski getan und die Stücke samt einem Tisch und einem Fass Bier mit einer Schar Trąbczyner Untertanen nach Trąbczyn fortgeschafft.',
     'A report of the court messenger Joannes Bikierski of Węgierce of 1 December 1772, for Stanisław Ścibor Chełmski, heir of Łukom, Łomowo and Myszakowo and possessor of the Olęder settlers in the Lusnia wood. With two noblemen he inspected the tavern in Lusnia on the Saturday before: three windows and four doors with iron hinges had been taken out of the house. He states that this was done that night by the Trąbczyn steward Lipiński, the clerk Radzewski, the bailiff and forest keeper and the manor servant Wąchnicki, at the order of Antoni Prusimski, and that the pieces were carried off to Trąbczyn, with a table and a barrel of beer, by a band of Trąbczyn subjects.'),
 8: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 26. Februar 1773, für Antoni Prusimski von Kolno, Starost von Niszczewice. Mit zwei Adligen hat er am Vortag die Trąbczyner Wälder und Wiesen besichtigt und gezählt: im Wald hinter dem Gehölz Lusnia einundfünfzig Stümpfe gefällter, zum Bauen tauglicher Kiefern, auf den Wiesen namens Kąty zweiunddreißig Erlenstümpfe. Nach seiner Angabe haben die Untertanen Chełmskis das Holz aus dem Wald abgefahren und Leute vom Gut Podbiele der Frau Zakrzewska die Erlen auf den Wiesen geschlagen.',
     'A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 26 February 1773, for Antoni Prusimski of Kolno, Starost of Niszczewice. With two noblemen he inspected and counted, the day before, in the woods and meadows of Trąbczyn: in the wood beyond the Lusnia grove fifty-one stumps of felled pines fit for building, and on the meadows called Kąty thirty-two alder stumps. He states that Chełmski\'s subjects carted the timber out of the wood, and that men of the Podbiele estate of the lady Zakrzewska cut the alders on the meadows.'),
 9: ('Protest von Stanisław Ścibor Chełmski, Erbherrn von Łukom und Besitzer der Olęder von Lusnia, gegen Antoni Prusimski von Kolno, Starost von Niszczewice, dessen Hofleute und Untertanen, eingetragen in Konin im März 1773 und von Chełmski unterschrieben. Prusimski habe, obwohl er wisse, dass der Besitz der Olęder von Lusnia Chełmski rechtlich zuerkannt sei, seinen Verwalter Lipiński und seinen Kammerdiener Marzęcki mit anderen das Schankhaus und die Olęder überfallen lassen; sie hätten dort Gewalttaten verübt.',
     'A protest of Stanisław Ścibor Chełmski, heir of Łukom and possessor of the Olęder settlers of Lusnia, against Antoni Prusimski of Kolno, Starost of Niszczewice, his household and his subjects, entered at Konin in March 1773 and signed by Chełmski. Prusimski, although he knows that possession of the Lusnia settlers has been adjudged to Chełmski at law, let his steward Lipiński and his chamber servant Marzęcki, with others, ride upon the tavern and the settlers; they committed acts of violence there.'),
 10: ('Bericht des Gerichtsboten Joannes Bikierski von Węgierki, eingetragen in Konin im März 1773, für Stanisław Chełmski. Mit zwei Adligen hat er am vergangenen Mittwoch die Olęder-Siedlung Lusnia besichtigt: Im Schankhaus waren der Ofen, drei Fenster und vier Türen, die Chełmski neu hatte herrichten lassen, zerhauen und herausgeschlagen, der Schornstein zerstört, das Bier- und Branntweingeschirr zerschlagen. Nach seiner Angabe haben das die Adligen Lipiński, Marzęcki und andere in der Nacht des 29. Januar des laufenden Jahres getan.',
      'A report of the court messenger Joannes Bikierski of Węgierki, entered at Konin in March 1773, for Stanisław Chełmski. With two noblemen he inspected the Olęder settlement of Lusnia on the Wednesday before: in the tavern the stove, three windows and four doors, which Chełmski had newly had put in order, were hacked and cut out, the chimney was ruined, and the vessels for beer and spirits were smashed. He states that this was done by the noblemen Lipiński, Marzęcki and others in the night of 29 January of the current year.'),
}
HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
