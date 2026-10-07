# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.118: from the editor's scans and texts to the edition.

    python units/app53170koningr118/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is the register of the castle court of Konin for 1780 to 1782, the
volume after Konin Gr.117: each sitting under a line "Actum in Conin ...".
The editor photographed thirty-two openings and transcribed the entries that
concern Trąbczyn. Each entry is a document (docs/PRUSIMSKI_ERA_PLAN.md).

    doc  leaf          scan       what
    1    172v          177        note, unfinished: Zielonacki and Chełmski cite the Prusimskis and Bogdańskis (1780)
    2    266v          272        note: Zielonacki cites Prusimski to the sitting at Grab (1781)
    3    343v          349        note of Prusimski's protest against Chełmski (1781)
    4    367v          373        note: Prusimski cites the Zakrzewskis and the land court (15 October 1781)
    5    381           386        note: Chełmski cites Prusimski (30 October 1781)
    6    382v          388        note: Gałecki and Skórzewski cite Prusimski (1781)
    7    383           388        note: Chełmski cites Prusimski (1781)
    8    396, 396v     401, 402   the convent of Ląd protests against Prusimski's charge (22 November 1781)
    9    398           403        note: Zielonacki and Chełmski cite Prusimski to Grab (4 December 1781)
    10   416, 416v     421, 422   report: the convent's citation of Prusimski (January 1782)
    11   460           465        note: the decree on the Olęder settlement brought in (18 March 1782)
    12   469           474        note: Prusimski cites the Zakrzewskis (19 April 1782)
    13   475, 475v     480, 481   Gosławski protests for Prusimski against the land court's decree (1782)
    14   495v          501        report: Chełmski's citation to the sitting at Grab (1782)
    15   514v, 515     520        heading only: Chełmski against the Tribunal's decree (25 May 1782)
    16   519           524        note: Prusimski cites Chełmski to Grab (1 June 1782)
    17   523v          529        Górski, the boundary chamberlain, protests against Chełmski (June 1782)
    18   526v          532        note: an inspection brought in for Prusimski (June 1782)
    19   530, 530v     535, 536   Chełmski protests against Górski (15 June 1782)
    20   585v, 586     591        Gosławski's search for a report of citation (16 August 1782)
    21   617           625        note: Chełmski cites Prusimski and Górski (1782)
    22   622           633        note: Prusimski cites Chełmski, Orłowski and the convent (September 1782)
    23   622 to 623v   633 to 635 report: Prusimski's citation of the Zakrzewskis and other heirs (21 September 1782)
    24   626           637        note: the convent cites Prusimski (28 September 1782)
    25   671v          685        report: Prusimski's citation of Chełmski to the castle court of Kalisz (1782)
    26   673           686        report: 221 pines cut left of the new line (7 December 1782)
    27   673 to 674    686, 687   Maszewski protests for Prusimski against Chełmski (7 December 1782)
    28   674v          688        note: the boundary decree of the sitting on the ground brought in (December 1782)
    29   674v          688        note: the delivery of the settler Martin Hunt (December 1782)

The scans are photographs named by their number in a series, not by leaf.
The leaf numbers are the later ones written in the margins (the numbers at
the head of the pages are an older count, struck through); SCANS gives the
right-hand leaf of each. Page ids: leaf N recto is <N>_a2, leaf N verso is
<N+1>_a1. Twenty-seven halves carry nothing transcribed and are set apart.
The folds are courtbook.find_fold's, three of them (177, 386, 421) moved by
eye; all are first proposals for the editor.

What read_source does to the editor's file beyond cutting it:
- document 2, which is on scan 272 and not in the editor's file, is
  transcribed here from the scan (NOTE_266V): four lines in a clear hand;
- the entry under "[173]" is left out: it has a heading of its own and
  concerns a decree between Rafał Gurowski and the townsmen of Brdów, not
  Trąbczyn. The editor's English had run it on from the unfinished note on
  leaf 172 verso (docs/PRUSIMSKI_QUESTIONS.md);
- the line under "[496]" is the editor's own note ("same as 495v"), not
  text. Leaf 496 begins another entry; the citation ends on leaf 495 verso;
- the entry the editor put under "[523]" is on leaf 523 verso (scan 529,
  left), and the first note under "[622]" stands wholly on leaf 622;
- signatures are added under documents 3, 8, 13, 15, 19 and 27 (SIGN...).

The check (2026-10-07) was the light one the plan sets for the long
holdings. Read against the scans, enlarged: every heading and date line; the
one-line notes (documents 1 to 7, 9, 11, 12, 16, 18, 21, 22, 24, 28, 29) and
documents 15, 20 and 25 word for word; the first half of the convent's
protest (8), the opening and close of documents 10, 13, 17, 19 and 26, and
the signatures. ROWS has what was corrected. The long Latin of documents 13,
14, 17, 19 and 23 and the Polish of 27 were NOT read through; they stand as
the editor has them, with their marks of doubt.

The English is the editor's own. Six lines that had come into the file from
a chat window are taken out (JUNK). FIXES are the places where the English
followed a reading that was corrected; document 2 is translated here in the
editor's terms (EN_266V). In documents 8 and 13 the English page break is moved
to where the page of the text ends (carry).

The full check (2026-10-07, at the editor's word, after they had read the
record of the light one). What the light check had left was read against the
scans, enlarged, word for word: documents 13 (leaves 475, 475 verso), 14
(495 verso), 17 (523 verso), 19 (530, 530 verso) and 23 (622 to 623 verso);
the Polish of 26 and 27 (673 to 674); document 10 (416, 416 verso) and the
second page of 8 (396 verso, which agrees with the editor's text). With the
light check that is every entry of the holding. Its record is
full_check.json beside this file (courtbook.full_check): 133 corrections
(ROWS, applied with --full after --correct) and 36 places where the English
follows (FIXES, applied after the FIXES below).

What it found, beyond single words:
- Five passages where a line or part of one was passed over: three in
  document 13, one each in 10 and 17; they are restored.
- "ott~", "oto[?]" is "olim", the late (documents 14 and 23).
- In document 14 "Illustris Magnifice Prusimski" is the form of address to
  Antoni Prusimski ("you, Prusimski"); there is no "Magnifica Prusimska".
  Teresa Bogdańska is the successor of her two dead sisters.
What is still marked as doubtful was looked at and could not be read with
confidence; nothing was completed by guess. Not read again: the name before
"Szkudlarka" and "z Torami" in document 27.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

FULL = courtbook.full_check(HERE)

SLUG = 'app53170koningr118'
REF = 'APP 53/17/0/-/Konin Gr.118'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1780-1782 (53.17.0.-.Konin Gr.118)"

# (file, x of the fold, left page, right page). First proposals; the editor's
# saved folds (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('177.jpg', 1965, '0173_a1', '0173_a2'),
    ('272.jpg', 1820, '0267_a1', '0267_a2'),
    ('349.jpg', 1921, '0344_a1', '0344_a2'),
    ('373.jpg', 1951, '0368_a1', '0368_a2'),
    ('386.jpg', 1990, '0381_a1', '0381_a2'),
    ('388.jpg', 1975, '0383_a1', '0383_a2'),
    ('401.jpg', 1989, '0396_a1', '0396_a2'),
    ('402.jpg', 1990, '0397_a1', '0397_a2'),
    ('403.jpg', 1992, '0398_a1', '0398_a2'),
    ('421.jpg', 2080, '0416_a1', '0416_a2'),
    ('422.jpg', 2020, '0417_a1', '0417_a2'),
    ('465.jpg', 1952, '0460_a1', '0460_a2'),
    ('474.jpg', 1972, '0469_a1', '0469_a2'),
    ('480.jpg', 1983, '0475_a1', '0475_a2'),
    ('481.jpg', 1987, '0476_a1', '0476_a2'),
    ('501.jpg', 2030, '0496_a1', '0496_a2'),
    ('520.jpg', 2047, '0515_a1', '0515_a2'),
    ('524.jpg', 1969, '0519_a1', '0519_a2'),
    ('529.jpg', 1974, '0524_a1', '0524_a2'),
    ('532.jpg', 1982, '0527_a1', '0527_a2'),
    ('535.jpg', 1980, '0530_a1', '0530_a2'),
    ('536.jpg', 1984, '0531_a1', '0531_a2'),
    ('591.jpg', 1986, '0586_a1', '0586_a2'),
    ('625.jpg', 2100, '0617_a1', '0617_a2'),
    ('633.jpg', 2102, '0622_a1', '0622_a2'),
    ('634.jpg', 2101, '0623_a1', '0623_a2'),
    ('635.jpg', 2104, '0624_a1', '0624_a2'),
    ('637.jpg', 2107, '0626_a1', '0626_a2'),
    ('685.jpg', 2171, '0672_a1', '0672_a2'),
    ('686.jpg', 2172, '0673_a1', '0673_a2'),
    ('687.jpg', 2171, '0674_a1', '0674_a2'),
    ('688.jpg', 2175, '0675_a1', '0675_a2'),
]
SKIP = ('0173_a2', '0267_a2', '0344_a2', '0368_a2', '0381_a1', '0396_a1', '0397_a2', '0398_a1', '0416_a1', '0417_a2', '0460_a1', '0469_a1', '0475_a1', '0476_a2', '0496_a2', '0519_a1', '0524_a2', '0527_a2', '0530_a1', '0531_a2', '0617_a1', '0622_a1', '0624_a2', '0626_a1', '0672_a2', '0673_a1', '0675_a2')
LEAF = {'0173_a1': '172 verso', '0173_a2': '173 recto', '0267_a1': '266 verso', '0267_a2': '267 recto', '0344_a1': '343 verso', '0344_a2': '344 recto', '0368_a1': '367 verso', '0368_a2': '368 recto', '0381_a1': '380 verso', '0381_a2': '381 recto', '0383_a1': '382 verso', '0383_a2': '383 recto', '0396_a1': '395 verso', '0396_a2': '396 recto', '0397_a1': '396 verso', '0397_a2': '397 recto', '0398_a1': '397 verso', '0398_a2': '398 recto', '0416_a1': '415 verso', '0416_a2': '416 recto', '0417_a1': '416 verso', '0417_a2': '417 recto', '0460_a1': '459 verso', '0460_a2': '460 recto', '0469_a1': '468 verso', '0469_a2': '469 recto', '0475_a1': '474 verso', '0475_a2': '475 recto', '0476_a1': '475 verso', '0476_a2': '476 recto', '0496_a1': '495 verso', '0496_a2': '496 recto', '0515_a1': '514 verso', '0515_a2': '515 recto', '0519_a1': '518 verso', '0519_a2': '519 recto', '0524_a1': '523 verso', '0524_a2': '524 recto', '0527_a1': '526 verso', '0527_a2': '527 recto', '0530_a1': '529 verso', '0530_a2': '530 recto', '0531_a1': '530 verso', '0531_a2': '531 recto', '0586_a1': '585 verso', '0586_a2': '586 recto', '0617_a1': '616 verso', '0617_a2': '617 recto', '0622_a1': '621 verso', '0622_a2': '622 recto', '0623_a1': '622 verso', '0623_a2': '623 recto', '0624_a1': '623 verso', '0624_a2': '624 recto', '0626_a1': '625 verso', '0626_a2': '626 recto', '0672_a1': '671 verso', '0672_a2': '672 recto', '0673_a1': '672 verso', '0673_a2': '673 recto', '0674_a1': '673 verso', '0674_a2': '674 recto', '0675_a1': '674 verso', '0675_a2': '675 recto'}
DOCS = [(1, ['0173_a1']), (2, ['0267_a1']), (3, ['0344_a1']), (4, ['0368_a1']), (5, ['0381_a2']), (6, ['0383_a1']),
        (7, ['0383_a2']), (8, ['0396_a2', '0397_a1']), (9, ['0398_a2']), (10, ['0416_a2', '0417_a1']), (11, ['0460_a2']),
        (12, ['0469_a2']), (13, ['0475_a2', '0476_a1']), (14, ['0496_a1']), (15, ['0515_a1', '0515_a2']), (16, ['0519_a2']),
        (17, ['0524_a1']), (18, ['0527_a1']), (19, ['0530_a2', '0531_a1']), (20, ['0586_a1', '0586_a2']), (21, ['0617_a2']),
        (22, ['0622_a2']), (23, ['0622_a2', '0623_a1', '0623_a2', '0624_a1']), (24, ['0626_a2']), (25, ['0672_a1']),
        (26, ['0673_a2']), (27, ['0673_a2', '0674_a1', '0674_a2']), (28, ['0675_a1']), (29, ['0675_a1'])]
FOLD_NOTE = ('All thirty-two scans are shown. On five, both halves are pages of the edition; on twenty-seven, one half is a '
             'page and the other is left out.')

NOTE_266V = [
    'Ex Parte M Zielonacki Judicis Terrestris Calissiensis contra JM Prusimski Capitaneum Nieszczevicen~ Relatio',
    'Videatur hoc loco Relatio ex parte Magnifici Stephani Zielonacki Judicis Terrestris Calissien~ contra Illustrem Magnificum '
    'Antonium Prusimski Capitaneum Nieszczevicen~ pro Termino Condescensionis In Fundo Bonorum Grab agitt~ Inciden~ prout Copia '
    'in productis',
]
EN_266V = ('On behalf of the Illustrious Zielonacki, Judge of the Kalisz Land Court, against the Illustrious Prusimski, Starost '
           'of Niszczewice — a Report\n\n'
           'Let there be seen at this place a Report on behalf of the Illustrious Stefan Zielonacki, Judge of the Kalisz Land '
           'Court, against the Illustrious Magnificent Antoni Prusimski, Starost of Niszczewice — for the Term of the '
           'Condescension in the settlement of the estates of Grab, being conducted, upcoming — as the copy in the submitted '
           'documents [attests].')
# Signatures, as written. "[?]" is a word not read.
SIGN3 = 'Super manifestationem Antoni Ostrorog na Kolnie Prusimski [?]'
SIGN8 = 'F Tesselinus Malechowski [?] qua Plens~ mpp'
SIGN13 = 'Petrus Gosławski qua [?]'
SIGN_CH = 'Stanisław Scibor Chełmski'
COUNTS = [('172v', 2), ('173', 1), ('343v', 2), ('367v', 3), ('381', 3), ('382v', 2), ('383', 2), ('396', 3), ('396v', 1),
          ('398', 2), ('416', 2), ('416v', 1), ('460', 3), ('469', 3), ('475', 2), ('475v', 1), ('495v', 2), ('496', 1),
          ('514v', 3), ('519', 3), ('523', 3), ('526v', 2), ('530', 3), ('530v', 3), ('585v', 2), ('586', 2), ('617', 2),
          ('622', 5), ('622v', 1), ('623', 1), ('623v', 1), ('626', 3), ('671v', 2), ('673', 5), ('673v', 1), ('674', 2),
          ('674v', 4)]


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == COUNTS, [(l, len(p)) for l, p in leaves]
    L = dict(leaves)
    assert L['173'][0].startswith('Decreti Commissorialis Inter Incolas Brdove'), L['173']
    assert L['496'][0].startswith('Tracholz/'), L['496']
    v = L['530v']
    return {
        (1, '0173_a1'): L['172v'],
        (2, '0267_a1'): NOTE_266V,
        (3, '0344_a1'): L['343v'] + [SIGN3],
        (4, '0368_a1'): L['367v'],
        (5, '0381_a2'): L['381'],
        (6, '0383_a1'): L['382v'],
        (7, '0383_a2'): L['383'],
        (8, '0396_a2'): L['396'],
        (8, '0397_a1'): L['396v'] + [SIGN8],
        (9, '0398_a2'): L['398'],
        (10, '0416_a2'): L['416'],
        (10, '0417_a1'): L['416v'],
        (11, '0460_a2'): L['460'],
        (12, '0469_a2'): L['469'],
        (13, '0475_a2'): L['475'],
        (13, '0476_a1'): L['475v'] + [SIGN13],
        (14, '0496_a1'): L['495v'],
        (15, '0515_a1'): L['514v'][:1],
        (15, '0515_a2'): L['514v'][1:] + [SIGN_CH],
        (16, '0519_a2'): L['519'],
        (17, '0524_a1'): L['523'],
        (18, '0527_a1'): L['526v'],
        (19, '0530_a2'): L['530'],
        (19, '0531_a1'): [v[0], SIGN_CH, v[1], v[2], SIGN_CH],
        (20, '0586_a1'): L['585v'],
        (20, '0586_a2'): L['586'],
        (21, '0617_a2'): L['617'],
        (22, '0622_a2'): L['622'][:2],
        (23, '0622_a2'): L['622'][2:],
        (23, '0623_a1'): L['622v'],
        (23, '0623_a2'): L['623'],
        (23, '0624_a1'): L['623v'],
        (24, '0626_a2'): L['626'],
        (25, '0672_a1'): L['671v'],
        (26, '0673_a2'): L['673'][:3],
        (27, '0673_a2'): L['673'][3:],
        (27, '0674_a1'): L['673v'],
        (27, '0674_a2'): L['674'],
        (28, '0675_a1'): L['674v'][:2],
        (29, '0675_a1'): L['674v'][2:],
    }


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0173_a1', 'Ex parte MM Zielonacki Judicium Terrestris', 'Ex parte MM Zielonacki Judicis Terrestris', 'the heading has "J T C": Judicis, the judge'),
    ('0173_a1', 'contra MM Prusimski Bogdanskie a[d?] nbl Relatio', 'contra MM Prusimskie Bogdanskie ad Tribunal Relatio',
     'the heading has "MM. Prusimskie Bogdanskie ad Tribl Rel": to the Tribunal'),
    ('0173_a1', 'Staphani Zielonacki Judicium Terrestris', 'Stephani Zielonacki Judicis Terrestris', 'the scan has "Stephani Zielonacki Judicis"'),
    ('0344_a1', 'Manifestatis Certa[m?]', 'Manifestatio Certa', 'the scan has "Manifestatio Certa", the set phrase'),
    ('0383_a1', 'B[ae?]septanei', 'Praesentanei',
     'the scan has "Praesentanei": Gałecki is the former ("anteacti") and Skórzewski the present heir of Biskupice'),
    ('0396_a2', 'Osobi[cie?]', 'Osobiscie', 'the word is plain on the scan'),
    ('0396_a2', 'niewzruszenie bięczy', 'niewzruszenie ręczy', 'the scan has "ręczy": for whose standing by it he vouches'),
    ('0396_a2', 'oczyszczaiącsy', 'oczyszczaiąc się', 'the scan has "oczyszczaiąc się"'),
    ('0397_a1', 'sprzyiancem', 'sprzyianiem', 'the scan has "sprzyianiem": favour'),
    ('0397_a1', 'przyczyn[y?]', 'przyczyn', 'the word is plain on the scan'),
    ('0397_a1', 'go[t?]owość', 'gotowość', 'the word is plain on the scan'),
    ('0397_a1', 'przyzwostych', 'przyzwoitych', 'the scan has "przyzwoitych"'),
    ('0398_a2', 'pro Termino Conditionis in Fundo Bonorum Grab [A?]agitt~', 'pro Termino Condescensionis in Fundo Bonorum Grab agitt~',
     'the scan has "p Tmo Condnis ... Grab agitt": Condescensionis, as in the heading'),
    ('0416_a2', 'seco[?] tunc', 'seu tunc', 'the scan has "seu tunc"'),
    ('0416_a2', 'Ladovie~ Benedicti', 'Ludovici Benedicti', 'the scan has "Lu|dovici" over the line end: the abbot\'s first name'),
    ('0417_a1', 'pronuntiam', 'pronuntiari', 'the scan has "pro|nuntiari"'),
    ('0417_a1', 'Ancitta Die horna Acta', 'Ancilla Die horna Actu', 'the scan has "Ancilla ... Actu Contenta": a maidservant being present'),
    ('0460_a2', 'in Hollandoris', 'in Hollandris', 'the scan has "in Hollandris"'),
    ('0476_a1', 'praemissio attestato', 'praemisso attestato', 'the scan has "praemisso attestato"'),
    ('0515_a2', 'Super requisitionem [?]uinocae Spati manupropria', 'Super requisitionem hujusce[?] Spatii manupropria',
     'read as "hujusce Spatii", this space, the words of the note on leaf 530 verso; left marked'),
    ('0527_a1', 'in Pap[?][?]ro', 'in Papyro', 'the scan has "in Papyro": on stamped paper'),
    ('0527_a1', 'Gros~ unius[?] argen~', 'Gros~ unius argen~', 'the word is plain on the scan'),
    ('0527_a1', 'Eonandem', 'Eorundem', 'the scan has "Eorundem"'),
    ('0531_a1', 'Thoma Reczkoyki[?] et Suent[o/i?] elai[?] Bogusławski nec non Providi Mathaei Matuszewski nie[x?] de Szetlewek',
     'Thoma Reczkowski et Sventoslai Bogusławski nec non Providi Mathaei Matuszkiewicz de Szetlewek',
     'the scan has "Reczkowski", "Sventoslai" and "Matuszkie|wicz" over the line end: the messenger of documents 25 and others'),
    ('0586_a2', 'vel ne [l/c?]ui Requisitioni', 'vel ne Cui Requisitioni', 'the scan has "Cui Requisitioni"'),
    ('0586_a2', 'de Inecistentia[?]', 'de Inexistentia', 'the scan has "de Inexistentia"'),
    ('0617_a2', 'Chełmski W contra', 'Chełmski T V contra', 'the heading has "T V": Thesaurarii Vschovensis'),
    ('0617_a2', 'pro Judicium ordinariis', 'pro Judiciis ordinariis', 'the scan has "pro Judiciis"'),
    ('0622_a2', 'Recognotvit se Citationes Litationes Authen~ unius ejusdem esseniae tri~nas',
     'Recognovit se Citationes Litteras Authen~ unius ejusdemque essentiae trinas', 'the scan has "Recognovit se Citationes Litteras ... ejusdemque essentiae trinas"'),
    ('0626_a2', 'Die scilicet 29 Mensis [????] Anno', 'Die scilicet 29 Mensis 7bris Anno', 'the scan has "29 Mens 7bris"'),
    ('0626_a2', 'Venerabilis Contentus Landensem', 'Venerabilis Conventus Landensem', 'the scan has "Conven"'),
    ('0672_a1', 'attentatum Violentiam', 'attentatarum Violentiarum', 'the scan has both words abbreviated in the genitive plural'),
    ('0672_a1', 'armiariolo[?]', 'armariolo', 'the scan has "armariolo": a small cupboard'),
    ('0673_a2', 'nalezącyn', 'nalezącym', 'the scan has "nalezącym"'),
    ('0673_a2', 'wisciętey[?]', 'wyciętey', 'the scan has "wyciętey": the line that was cut'),
    ('0673_a2', 'Ko[t/ł?]kami', 'Kołkami', 'the scan has "Kołkami": with stakes'),
    ('0673_a2', 'Budynkonych', 'Budynkowych', 'the scan has "Budynkowych": building timber'),
    ('0673_a2', '[N/W?]Jmc', 'WJmc', 'the scan has "WJmc"'),
    ('0674_a2', 'Leon Maszewski', 'Leon Maszewski Imieniem Pana mego', 'the signature goes on: in the name of my lord'),
    ('0675_a1', 'Protocollo Obl[ata?]', 'Prolati Oblata', 'the heading ends "Prolati Oblata"'),
    ('0675_a1', 'per M Josephus Lukaszewicz', 'per M Josephum Łukaszewicz', 'the scan has "Josephum Łukaszewicz"'),
    ('0675_a1', 'Poloniae peractis', 'Poloniae peracta', 'the scan has "peracta"'),
]

JUNK = re.compile(r'^(\d{1,2}:\d\d [ap]\.m\.|Please fix the most recent one\.|Show more|\[Claude responded.*)$')
FIXES = [
    ('Report to the Noble [Court]', 'Report to the Tribunal', '"ad Tribunal Relatio"'),
    ('certain[T.N.] in its substance', 'certain in its substance', 'a stray note mark'),
    ('Gałecki, former Starost of Bydgoszcz, and', 'Gałecki, Starost of Bydgoszcz, and', '"anteacti" goes with "Haeredum", not with the starosty'),
    ('Ignacy Gałecki, formerly Starost of Bydgoszcz, and the Illustrious Magnificent Michał Drogosław Skorzewski, Sub-chamberlain '
     'of Poznań, [B[uncertain: ae]septanei], Heirs of the estate of Biskupice',
     'Ignacy Gałecki, Starost of Bydgoszcz, the former heir, and the Illustrious Magnificent Michał Drogosław Skorzewski, '
     'Sub-chamberlain of Poznań, the present heir of the estate of Biskupice',
     '"anteacti et ... Praesentanei Bonorum Biskupice Haeredum"'),
    (', [uncertain: A] being conducted', ', being conducted', '"agitt~" is plain'),
    ('[Ancitta] present', 'a maidservant present', '"praesente Ancilla"'),
    ('upon the requisition of the [?uinocae Spati] — by his own hand.', 'upon the requisition of [uncertain: this] space — by his own hand.',
     '"hujusce[?] Spatii"'),
    ('Tomasz Reczko[uncertain: y]ki and Svętosław Bogusławski, and also the Honest Mateusz Matuszewski [nie[uncertain: x] of Szetlewek',
     'Tomasz Reczkowski and Świętosław Bogusławski, and also the Honest Mateusz Matuszkiewicz of Szetlewek', 'the names as read'),
    ('Chełmski [[uncertain: pr]p T R P]', 'Chełmski [for the Crown Tribunal at Piotrków]', 'the abbreviation written out'),
    ('Chełmski [W] against', 'Chełmski, Treasurer of Wschowa, against', '"T V"'),
    ('upon the [uncertain: armiariolo] in the heated room', 'upon the small cupboard in the heated room', '"super armariolo"'),
    ('on the left side of the [uncertain: cleared] line', 'on the left side of the cut line', '"wyciętey Linij"'),
    ('between the estates of Trąbczyn and Łukom — enrolled in the Protocol', 'issued between the estates of Trąbczyn and Łukom',
     '"Prolati Oblata", not "Protocollo"'),
]
SIGN_CH_EN = 'Stanisław Ścibor Chełmski'
COUNTS_EN = [('172v', 2), ('173', 1), ('343v', 2), ('367v', 3), ('381', 3), ('382v', 2), ('383', 2), ('396', 3), ('396v', 1),
             ('398', 2), ('416', 3), ('416v', 1), ('460', 3), ('469', 3), ('475', 2), ('475v', 2), ('495v', 3), ('514v', 3),
             ('519', 3), ('523', 6), ('526v', 2), ('530', 3), ('530v', 2), ('530v', 2), ('585v', 2), ('586', 2), ('617', 2),
             ('622', 2), ('622', 3), ('622v', 3), ('623', 3), ('623v', 2), ('626', 3), ('671v', 2), ('673', 7), ('673v', 1),
             ('674', 2), ('674v', 2), ('674v', 2)]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    n = sum(1 for _, p in leaves for x in p if JUNK.match(x))
    assert n == 6, n
    leaves = [(l, [x for x in p if not JUNK.match(x)]) for l, p in leaves]
    assert [(l, len(p)) for l, p in leaves] == COUNTS_EN, [(l, len(p)) for l, p in leaves]
    E = courtbook.fix_english({i: p for i, (_, p) in enumerate(leaves)}, FIXES + FULL['FIXES'])

    def carry(i, k, mark):
        """The editor's page break stands later in the English than in the text: move it to `mark`."""
        head, tail = E[i][k].split(mark)
        E[i][k] = head + mark
        E[i + 1][0] = tail.strip() + ' ' + E[i + 1][0]
    carry(7, 2, 'during the last commission with no')      # leaf 396 ends "zadną"
    carry(14, 1, 'paying no attention whatsoever')          # leaf 475 ends "minime attent[i?]"
    j = '\n\n'.join
    return {
        1: [j(E[0])],
        2: [EN_266V],
        3: [j(E[2] + ['Upon the manifest: Antoni Ostroróg of Kolno Prusimski [illegible]'])],
        4: [j(E[3])], 5: [j(E[4])], 6: [j(E[5])], 7: [j(E[6])],
        8: [j(E[7]), j(E[8] + ['Fr. Tesselinus Malechowski [illegible], as plenipotentiary, by his own hand'])],
        9: [j(E[9])],
        10: [j(E[10]), j(E[11])],
        11: [j(E[12])], 12: [j(E[13])],
        13: [j(E[14]), j(E[15] + ['Petrus Gosławski, as [illegible]'])],
        14: [j(E[16])],
        15: [j(E[17][:1]), j(E[17][1:] + [SIGN_CH_EN])],
        16: [j(E[18])], 17: [j(E[19])], 18: [j(E[20])],
        19: [j(E[21]), j(E[22] + [SIGN_CH_EN] + E[23] + [SIGN_CH_EN])],
        20: [j(E[24]), j(E[25])],
        21: [j(E[26])], 22: [j(E[27])],
        23: [j(E[28]), j(E[29]), j(E[30]), j(E[31])],
        24: [j(E[32])], 25: [j(E[33])],
        26: [j(E[34][:5])],
        27: [j(E[34][5:]), j(E[35]), j(E[36][:1] + ['Leon Maszewski, in the name of my lord'])],
        28: [j(E[37])], 29: [j(E[38])],
    }


S = {
 1: ('Unvollendeter Registervermerk im Buch des Burggerichts Konin, 1780: Bericht über eine Ladung vor das Tribunal, erwirkt von Stefan Zielonacki, Richter des Kalischer Landgerichts, und Stanisław Chełmski, Schatzmeister von Wschowa, gegen die Prusimski und die Bogdański. Der Vermerk bricht nach den Namen der Kläger ab.',
     "An unfinished register note in the book of the castle court at Konin, 1780: the report of a citation before the Tribunal obtained by Stefan Zielonacki, judge of the Kalisz land court, and Stanisław Chełmski, Treasurer of Wschowa, against the Prusimskis and the Bogdańskis. The note breaks off after the plaintiffs' names."),
 2: ('Registervermerk von 1781: Bericht über die Ladung, die Stefan Zielonacki, Richter des Kalischer Landgerichts, gegen Antoni Prusimski, Starost von Niszczewice, zum Ortstermin auf dem Grund des Gutes Grab erwirkt hat; eine Abschrift liegt bei den vorgelegten Schriftstücken.',
     'A register note of 1781: the report of the citation that Stefan Zielonacki, judge of the Kalisz land court, obtained against Antoni Prusimski, Starost of Niszczewice, for the sitting on the ground of the estate of Grab; a copy is among the documents produced.'),
 3: ('Registervermerk über einen Protest, 1781: Antoni Ostroróg Prusimski, Starost von Niszczewice, Ritter des St.-Stanislaus-Ordens, Erbherr von Trąbczyn, Trąbczynek und Nowa Wieś, ist persönlich erschienen und protestiert vorsorglich gegen Stanisław Chełmski, Schatzmeister von Wschowa, Erbherr von Łukomia und Łomów; eine Abschrift liegt bei den vorgelegten Schriftstücken. Prusimski hat unterschrieben.',
     'A register note of a protest, 1781: Antoni Ostroróg Prusimski, Starost of Niszczewice, knight of the Order of St Stanislaus, heir of Trąbczyn, Trąbczynek and Nowa Wieś, appeared in person and protests, as a precaution, against Stanisław Chełmski, Treasurer of Wschowa, heir of Łukomia and Łomów; a copy is among the documents produced. Prusimski signed.'),
 4: ('Registervermerk vom 15. Oktober 1781: Bericht über die Ladung, die Antoni Prusimski, Starost von Niszczewice, gegen Kazimierz Zakrzewski und dessen Söhne Nepomucen, Ignacy und Ludwik sowie gegen das Kalischer Landgericht vor das Krontribunal in Petrikau erwirkt hat.',
     'A register note of 15 October 1781: the report of the citation that Antoni Prusimski, Starost of Niszczewice, obtained against Kazimierz Zakrzewski and his sons Nepomucen, Ignacy and Ludwik, and against the Kalisz land court, before the Crown Tribunal at Piotrków.'),
 5: ('Registervermerk vom 30. Oktober 1781: Bericht über die Zustellung der Ladung, die Stanisław Chełmski, Schatzmeister von Wschowa, gegen Antoni Prusimski, Starost von Niszczewice, vor das Krontribunal in Petrikau erwirkt hat.',
     'A register note of 30 October 1781: the report that the citation was served which Stanisław Chełmski, Treasurer of Wschowa, obtained against Antoni Prusimski, Starost of Niszczewice, before the Crown Tribunal at Piotrków.'),
 6: ('Registervermerk von 1781: Bericht über die Ladung, die Ignacy Gałecki, Starost von Bromberg, und Michał Drogosław Skórzewski, Unterkämmerer von Posen, der frühere und der jetzige Erbherr von Biskupice, gegen Antoni Prusimski, Starost von Niszczewice, vor das Krontribunal in Petrikau erwirkt haben.',
     'A register note of 1781: the report of the citation that Ignacy Gałecki, Starost of Bydgoszcz, and Michał Drogosław Skórzewski, sub-chamberlain of Poznań, the former and the present heir of Biskupice, obtained against Antoni Prusimski, Starost of Niszczewice, before the Crown Tribunal at Piotrków.'),
 7: ('Registervermerk von 1781: Bericht über die Ladung, die Stanisław Ścibor Chełmski, Schatzmeister von Wschowa, gegen Antoni Prusimski, Starost von Niszczewice, vor das Krontribunal in Petrikau erwirkt hat.',
     'A register note of 1781: the report of the citation that Stanisław Ścibor Chełmski, Treasurer of Wschowa, obtained against Antoni Prusimski, Starost of Niszczewice, before the Crown Tribunal at Piotrków.'),
 8: ('Protest vom 22. November 1781, auf Polnisch. Pater Tesselin Malechowski, Verwalter des Konvents von Ląd, erklärt im eigenen Namen und im Namen des ganzen Konvents gegen einen Vorwurf von Antoni Prusimski, Starost von Niszczewice: Im Grenzstreit mit Łukomia und Trąbczyn, der das Konventsgut Drzewce berührt, habe sich der Konvent bei der letzten Kommission von keiner Absprache und Begünstigung leiten lassen. Er habe den Punkt, an dem die drei Gemarkungen Łukomia, Trąbczyn und Drzewce zusammenstoßen, so anerkannt, wie Chełmski ihn zeigte, aus den im Kommissionsdekret genannten Gründen, und bleibe dabei. Der Konvent sei bereit, das zu beschwören, und werde wegen des Vorwurfs Strafen betreiben. Malechowski hat unterschrieben.',
     "A protest of 22 November 1781, in Polish. Father Tesselin Malechowski, administrator of the convent of Ląd, declares in his own name and in that of the whole convent, against a charge made by Antoni Prusimski, Starost of Niszczewice: in the boundary disputes with Łukomia and Trąbczyn, which touch the convent's estate of Drzewce, the convent was led by no collusion or favour at the last commission. It acknowledged the point where the three grounds of Łukomia, Trąbczyn and Drzewce meet as Chełmski showed it, for the reasons given in the commission's decree, and stands by that. The convent is ready to swear to it and will seek penalties for the charge. Malechowski signed."),
 9: ('Registervermerk vom 4. Dezember 1781: Bericht über die Ladung, die Stefan Zielonacki, Richter des Kalischer Landgerichts, und Stanisław Chełmski, Schatzmeister von Wschowa, gegen Antoni Prusimski, Starost von Niszczewice, zum Ortstermin auf dem Grund des Gutes Grab erwirkt haben.',
     'A register note of 4 December 1781: the report of the citation that Stefan Zielonacki, judge of the Kalisz land court, and Stanisław Chełmski, Treasurer of Wschowa, obtained against Antoni Prusimski, Starost of Niszczewice, for the sitting on the ground of the estate of Grab.'),
 10: ('Bericht des Gerichtsboten Simon Głabik von Drzewce, eingetragen in Konin im Januar 1782. Er hat Antoni Prusimski, Starost von Niszczewice und Erbherr von Trąbczyn, eine königliche Ladung vor das Krontribunal in Petrikau zugestellt, ausgestellt in Petrikau am 4. Januar 1782, auf Betreiben von Abt Benedykt Lubstowski und dem Konvent von Ląd, Erbherren von Drzewce. Der Konvent will von dem Vorwurf der Absprache mit dem Erbherrn von Łukomia freigesprochen werden und beruft sich auf Tribunalsdekrete und die Besichtigung von 1592. Der Bote hat die Ladung im Gutshof von Trąbczyn hinterlegt.',
     'A report of the court messenger Simon Głabik of Drzewce, entered at Konin in January 1782. He has served on Antoni Prusimski, Starost of Niszczewice and heir of Trąbczyn, a royal citation before the Crown Tribunal at Piotrków, dated at Piotrków on 4 January 1782, at the instance of Abbot Benedykt Lubstowski and the convent of Ląd, heirs of Drzewce. The convent asks to be cleared of the charge of collusion with the heir of Łukomia and relies on Tribunal decrees and the inspection of 1592. The messenger left the citation at the manor of Trąbczyn.'),
 11: ('Registervermerk vom 18. März 1782: Das Dekret des Ortstermins über die zu Trąbczyn gehörende Olęder-Siedlung, ergangen zwischen Antoni Prusimski, Starost von Niszczewice, und Stanisław Chełmski, Schatzmeister von Wschowa, wird zur Eintragung vorgelegt; das Original ist bei den vorgelegten Schriftstücken eingeheftet.',
     'A register note of 18 March 1782: the decree of the sitting on the ground concerning the Olęder settlement that belongs to Trąbczyn, given between Antoni Prusimski, Starost of Niszczewice, and Stanisław Chełmski, Treasurer of Wschowa, is brought in for entry; the original is sewn in among the documents produced.'),
 12: ('Registervermerk vom 19. April 1782: Bericht über die Ladung, die Antoni Prusimski, Starost von Niszczewice, Ritter des St.-Stanislaus-Ordens, gegen Vater und Söhne Zakrzewski sowie gegen das Kalischer Landgericht vor das Krontribunal in Petrikau erwirkt hat.',
     'A register note of 19 April 1782: the report of the citation that Antoni Prusimski, Starost of Niszczewice, knight of the Order of St Stanislaus, obtained against the Zakrzewskis, father and sons, and against the Kalisz land court, before the Crown Tribunal at Piotrków.'),
 13: ('Protest von Piotr Gosławski als Bevollmächtigtem von Antoni Prusimski, Starost von Niszczewice, gegen ein Dekret des Kalischer Landgerichts, eingetragen in Konin 1782 und von ihm unterschrieben. Vor dem Landgericht in Konin habe sein Auftraggeber am 15. Oktober des Vorjahres ein Zeugnis von Franciszek Ksawery Kęszycki, Marschall des Krontribunals, vom 13. Oktober vorgelegt und um Aufschub gebeten. Das Landgericht habe das Zeugnis nicht beachtet und Aufschub und Antrag nicht zugelassen; der Vertreter habe sich, ohne Urkunden, zurückziehen müssen. Gosławski protestiert gegen das Landgericht und die Gegenpartei und kündigt an, die Aufhebung des Dekrets und der erwirkten Verurteilung zu betreiben.',
     'A protest of Piotr Gosławski, as plenipotentiary of Antoni Prusimski, Starost of Niszczewice, against a decree of the Kalisz land court, entered at Konin in 1782 and signed by him. Before the land court at Konin on 15 October of the year before, his principal laid down a certificate of Franciszek Ksawery Kęszycki, Marshal of the Crown Tribunal, of 13 October, and asked for a delay. The land court disregarded the certificate and admitted neither the delay nor the motion; the representative, without the papers, had to withdraw. Gosławski protests against the land court and the other party and announces that he will seek to have the decree and the condemnation obtained under it quashed.'),
 14: ('Bericht des Gerichtsboten Bartłomiej Wrzask von Sławsk, eingetragen in Konin 1782, für Stanisław Ścibor Chełmski, Schatzmeister von Wschowa. Er hat eine königliche Ladung zum Ortstermin auf dem Grund des Gutes Grab zugestellt, ausgestellt in Petrikau am 26. November 1781. Geladen sind Antoni Prusimski, Starost von Niszczewice, sowie die Eheleute Bogdański: Ludwik, Landkämmerer von Kalisz, und Teresa, geborene Rozdrażewska, Erbin der Katarzyna Prusimska, geborene Rozdrażewska, Erbfrau von Grab. Sie sollen am 3. Juni 1782 vor dem Gericht des Ortstermins erscheinen, das ein Dekret des Krontribunals angeordnet hat. Chełmski verlangt die Zahlung der Summe, die der Kaufmann Tracholz ihm abgetreten hat, samt Zinsen; vier Untertanen aus Nowa Wieś sollen als Zeugen gestellt werden. Der Bote hat die Ladung am Freitag, dem Vorabend von Mariä Empfängnis 1781, in Trąbczyn hinterlegt.',
     'A report of the court messenger Bartłomiej Wrzask of Sławsk, entered at Konin in 1782, for Stanisław Ścibor Chełmski, Treasurer of Wschowa. He has served a royal citation to the sitting on the ground of the estate of Grab, dated at Piotrków on 26 November 1781. Cited are Antoni Prusimski, Starost of Niszczewice, and the Bogdańskis, husband and wife: Ludwik, land chamberlain of Kalisz, and Teresa, born Rozdrażewska, heiress of Katarzyna Prusimska, born Rozdrażewska, the heiress of Grab. They are to appear on 3 June 1782 before the court of the sitting on the ground, which a decree of the Crown Tribunal ordered. Chełmski claims payment of the sum that the merchant Tracholz made over to him, with interest; four subjects from Nowa Wieś are to be produced as witnesses. The messenger left the citation at Trąbczyn on the Friday on the eve of the Immaculate Conception 1781.'),
 15: ('Überschrift eines Eintrags vom 25. Mai 1782: Chełmski, Schatzmeister von Wschowa, protestiert gegen ein Dekret des Krontribunals. Der Text wurde nicht geschrieben. Darunter haben Piotr Gosławski als Bevollmächtigter, auf seine Nachfrage wegen des Platzes, und Stanisław Ścibor Chełmski unterschrieben.',
     'The heading of an entry of 25 May 1782: Chełmski, Treasurer of Wschowa, protests against a decree of the Crown Tribunal. The text was not written. Under it Piotr Gosławski, as plenipotentiary, on his inquiry about the space, and Stanisław Ścibor Chełmski signed.'),
 16: ('Registervermerk vom 1. Juni 1782: Bericht über die Ladung, die Antoni Prusimski von Kolno, Starost von Niszczewice, gegen Stanisław Chełmski, Schatzmeister von Wschowa, zum Ortstermin auf dem Gut Grab erwirkt hat; eine Abschrift liegt bei den vorgelegten Schriftstücken.',
     'A register note of 1 June 1782: the report of the citation that Antoni Prusimski of Kolno, Starost of Niszczewice, obtained against Stanisław Chełmski, Treasurer of Wschowa, for the sitting on the ground at the estate of Grab; a copy is among the documents produced.'),
 17: ('Protest von Jakub Pomian Górski, Grenzkämmerer der Woiwodschaft Inowrocław, gegen Stanisław Ścibor Chełmski, Schatzmeister von Wschowa und Erbherr von Łukom, eingetragen in Konin im Juni 1782 und von ihm unterschrieben. Górski war, von Prusimski beigezogen, zum Ortstermin zwischen Trąbczyn Minus oder Nowa Wieś und Łukom erschienen, den das Krontribunal in Petrikau mit seinem Dekret vom 23. Januar des laufenden Jahres angesetzt hatte, um Grenzhügel zu errichten; das Tribunal hatte den Grenzstreit nach der Karte entschieden und über zwei einander widersprechende Kommissionsdekrete befunden. Als er das Dekret nach der vom Tribunal in die Karte eingetragenen Linie vollziehen wollte, widersetzte sich Chełmski persönlich mit seinem Gefolge, stieß den Mann fort, der die Messkette zog, trat die Kette von der Linie, drohte und erklärte, er lasse eine weitere Berichtigung der Linie nicht zu. Górski brach die Amtshandlung ab, um beim Kriegsdepartement militärische Hilfe zu erwirken.',
     "A protest of Jakub Pomian Górski, boundary chamberlain of the palatinate of Inowrocław, against Stanisław Ścibor Chełmski, Treasurer of Wschowa and heir of Łukom, entered at Konin in June 1782 and signed by him. Górski, engaged by Prusimski, had come to the sitting on the ground between Trąbczyn Minus or Nowa Wieś and Łukom that the Crown Tribunal at Piotrków fixed by its decree of 23 January of the current year for the raising of boundary mounds; the Tribunal had decided the boundary cause from the map and ruled on two commission decrees that contradicted each other. When he set about carrying out the decree along the line the Tribunal had drawn on the map, Chełmski in person, with his followers, resisted, pushed away the man who was drawing the surveyor's chain, kicked the chain off the line, made threats, and declared that he would allow no further correction of the line. Górski broke off his proceedings in order to obtain military help from the War Department."),
 18: ('Registervermerk vom Juni 1782: Für Antoni Prusimski, Starost von Niszczewice, wird die Besichtigung eines Ortes auf Trąbczyner Erbgrund zur Eintragung vorgelegt, von zwei Adligen und einem Gerichtsboten auf Stempelpapier zu einem Silbergroschen aufgesetzt und von den Adligen eigenhändig unterschrieben; das Original liegt bei den vorgelegten Schriftstücken.',
     'A register note of June 1782: for Antoni Prusimski, Starost of Niszczewice, the inspection of a place on the hereditary ground of Trąbczyn is brought in for entry, drawn up by two noblemen and a court messenger on paper stamped at one silver grosz and signed by the noblemen in their own hands; the original is among the documents produced.'),
 19: ('Protest von Stanisław Ścibor Chełmski, Erbherr von Łukomia und Myszakowo, gegen Jakub Górski, Grenzkämmerer von Inowrocław, vom 15. Juni 1782, von Chełmski unterschrieben. Vollziehende Ämter hätten Dekrete des Krontribunals zu vollziehen, nicht auszulegen. Górski habe beim Ortstermin auf dem Grund von Trąbczyn die Regel des Tribunalsdekrets überschritten, sei vom Feldamt des Landes Dobrzyń abgewichen und habe sich in die Auslegung des Dekrets eingelassen. Er habe Chełmski beschrieben, als hätte dieser sich widersetzt, seine Amtshandlung ohne Zustimmung der Parteien auf unbestimmte Zeit vertagt und seine Akten wegen militärischer Hilfe an das Kriegsdepartement des Immerwährenden Rates geschickt, statt die Sache an das Tribunal zu verweisen. Chełmski erklärt Górskis Handlung für nichtig. Darunter ein Vermerk vom 16. August: Piotr Gosławski, Bevollmächtigter Prusimskis, hat vor Zeugen wegen des Platzes nachgefragt, für den keine Angaben und keine Abschrift geliefert worden waren.',
     "A protest of Stanisław Ścibor Chełmski, heir of Łukomia and Myszakowo, against Jakub Górski, boundary chamberlain of Inowrocław, of 15 June 1782, signed by Chełmski. Executive offices, he says, are to carry out the decrees of the Crown Tribunal, not to interpret them. At the sitting on the ground of Trąbczyn Górski went beyond the rule of the Tribunal's decree, departed from the field office of the land of Dobrzyń, and took upon himself to interpret the decree. He described Chełmski as though he had resisted, put off his proceedings without the parties' consent to an unnamed time, and sent his acts to the War Department of the Permanent Council for military help, instead of remitting the cause to the Tribunal. Chełmski declares Górski's act null. Under it is a note of 16 August: Piotr Gosławski, Prusimski's plenipotentiary, inquired before witnesses about the space, for which no information and no copy had been supplied."),
 20: ('Eintrag vom 16. August 1782. Piotr Gosławski, Bevollmächtigter von Antoni Prusimski, Starost von Niszczewice, fragt mit zwei Adligen in der Kanzlei, ob der Bericht über die Zustellung einer Ladung in Trąbczyn, die Stanisław Chełmski gegen Prusimski vor das Krontribunal in Petrikau erwirkt haben soll, vor dem Amt erklärt worden ist. Das Amt bescheinigt, dass ein solcher Bericht nicht vorliegt und nicht herausgegeben werden kann. Gosławski hat unterschrieben.',
     'An entry of 16 August 1782. Piotr Gosławski, plenipotentiary of Antoni Prusimski, Starost of Niszczewice, asks in the chancery, with two noblemen, whether the report of a citation served at Trąbczyn, which Stanisław Chełmski is said to have obtained against Prusimski before the Crown Tribunal at Piotrków, has been declared before the office. The office certifies that there is no such report and that none can be given out. Gosławski signed.'),
 21: ('Registervermerk von 1782: Bericht über die Ladung, die Stanisław Chełmski, Schatzmeister von Wschowa, gegen Antoni Prusimski, Starost von Niszczewice, und Jakub Górski, Grenzkämmerer von Inowrocław, vor das Krontribunal in Petrikau erwirkt hat.',
     'A register note of 1782: the report of the citation that Stanisław Chełmski, Treasurer of Wschowa, obtained against Antoni Prusimski, Starost of Niszczewice, and Jakub Górski, boundary chamberlain of Inowrocław, before the Crown Tribunal at Piotrków.'),
 22: ('Registervermerk vom September 1782: Bericht über die Zustellung der Ladung, die Antoni Prusimski von Kolno, Starost von Niszczewice, gegen Stanisław Chełmski, Schatzmeister von Wschowa, gegen Jan Alojzy Orłowski, Kämmerer des Landes Dobrzyń, und gegen Abt Benedykt Lubstowski und den ganzen Konvent von Ląd vor das Krontribunal in Petrikau erwirkt hat.',
     'A register note of September 1782: the report that the citation was served which Antoni Prusimski of Kolno, Starost of Niszczewice, obtained against Stanisław Chełmski, Treasurer of Wschowa, against Jan Alojzy Orłowski, chamberlain of the land of Dobrzyń, and against Abbot Benedykt Lubstowski and the whole convent of Ląd, before the Crown Tribunal at Piotrków.'),
 23: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 21. September 1782. Er hat drei Ausfertigungen einer königlichen Ladung vor das Krontribunal in Petrikau zugestellt, ausgestellt in Petrikau am Montag nach St. Bartholomäus 1782. Geladen sind Kazimierz Zakrzewski, Landrichter von Brześć Kujawski, und seine Söhne Nepomucen, Ignacy und Ludwik aus der Ehe mit der verstorbenen Marianna Prusimska; deren Söhne erster Ehe Paweł und Józef Tomicki; Franciszek Tworowicz und Elżbieta, Frau von Jakub Taczanowski, Kinder der verstorbenen Wiktoria Prusimska; und Kunegunda Kołaczkowska, Tochter der verstorbenen Konstancja Prusimska und des Jan Kowalski. Geladen sind ferner die Amtsträger des Kalischer Landgerichts: der Richter Stefan Leszczyc Zielonacki, der Unterrichter Andrzej Bogdański, der Notar Xawery Mikorski und der Kämmerer Ignacy Rapacki. Kläger ist Antoni Prusimski von Kolno, Starost von Niszczewice: Sohn des verstorbenen Stefan Prusimski und der Wiktoria Malczewska, Enkel von Krzysztof Prusimski und Teresa Golińska, Neffe von deren Söhnen Jan, Bogumił, Antoni und Paweł Prusimski und nach dem kinderlosen Tod von Antoni und Paweł deren einziger Rechtsnachfolger. Er beruft sich auf ein Tribunalsdekret von 1738, das den Eheleuten Kowalski die Erbfolge nach Jan und Bogumił Prusimski absprach, und auf dessen Bestätigung durch ein Dekret von 1760. Er verlangt, die Dekrete des Landgerichts aufzuheben, ihn von dem Anspruch auf die Erbfolge nach Antoni und Paweł Prusimski freizusprechen und den Geladenen ewiges Schweigen aufzuerlegen: Töchter, die der Vater ausgestattet hat, könnten von den Brüdern nichts fordern. Die Ausfertigungen wurden in den Gutshöfen von Zieleniec und Mostki und in Konin im Haus der Bürgerin Wiśniewska hinterlegt, wo die Kanzlei des Landgerichts ist.',
     'A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 21 September 1782. He has served three copies of a royal citation before the Crown Tribunal at Piotrków, dated at Piotrków on the Monday after St Bartholomew 1782. Cited are Kazimierz Zakrzewski, land judge of Brześć Kujawski, and his sons Nepomucen, Ignacy and Ludwik by his marriage with the late Marianna Prusimska; her sons of her first marriage, Paweł and Józef Tomicki; Franciszek Tworowicz and Elżbieta, wife of Jakub Taczanowski, children of the late Wiktoria Prusimska; and Kunegunda Kołaczkowska, daughter of the late Konstancja Prusimska and Jan Kowalski. Cited too are the officers of the Kalisz land court: the judge Stefan Leszczyc Zielonacki, the sub-judge Andrzej Bogdański, the notary Xawery Mikorski and the chamberlain Ignacy Rapacki. The plaintiff is Antoni Prusimski of Kolno, Starost of Niszczewice: son of the late Stefan Prusimski and Wiktoria Malczewska, grandson of Krzysztof Prusimski and Teresa Golińska, nephew of their sons Jan, Bogumił, Antoni and Paweł Prusimski and, after Antoni and Paweł died childless, their sole successor. He relies on a Tribunal decree of 1738, which denied the Kowalskis the succession to Jan and Bogumił Prusimski, and on its confirmation by a decree of 1760. He asks that the decrees of the land court be quashed, that he be freed from the claim to the succession of Antoni and Paweł Prusimski, and that perpetual silence be laid on those cited: daughters whom their father has dowered can claim nothing from their brothers. The copies were left at the manors of Zieleniec and Mostki and at Konin in the house of the townswoman Wiśniewska, where the chancery of the land court is.'),
 24: ('Registervermerk vom September 1782: Bericht über die Ladung, die der Konvent von Ląd gegen Antoni Prusimski, Starost von Niszczewice, vor das Krontribunal in Petrikau erwirkt hat; eine Abschrift liegt bei den vorgelegten Schriftstücken.',
     'A register note of September 1782: the report of the citation that the convent of Ląd obtained against Antoni Prusimski, Starost of Niszczewice, before the Crown Tribunal at Piotrków; a copy is among the documents produced.'),
 25: ('Bericht des Gerichtsboten Mateusz Matuszkiewicz von Szetlewek, eingetragen in Konin 1782. Er hat Stanisław Chełmski, Schatzmeister von Wschowa und Erbherr von Łukom, und anderen eine Ladung vor das Burggericht Kalisz zugestellt, auf Betreiben von Antoni Prusimski von Kolno, Starost von Niszczewice: wegen der Strafen für verübte Gewalttaten samt der Festnahme von Leuten. Er hat sie im Gutshof von Łukom in Gegenwart des Geladenen hinterlegt.',
     'A report of the court messenger Mateusz Matuszkiewicz of Szetlewek, entered at Konin in 1782. He has served on Stanisław Chełmski, Treasurer of Wschowa and heir of Łukom, and on others a citation before the castle court of Kalisz, at the instance of Antoni Prusimski of Kolno, Starost of Niszczewice: for the penalties for acts of violence committed, with the seizing of people. He left it at the manor of Łukom in the presence of the man cited.'),
 26: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 7. Dezember 1782, für Antoni Prusimski von Kolno, Starost von Niszczewice. Mit zwei Adligen, Adam Milewski und Jan Wilgiewicz, war er am 4. des laufenden Monats im Trąbczyner Kiefernwald. Links der Linie, die nach dem Dekret des Tribunals und des Ortstermins ausgehauen und mit Pflöcken bezeichnet ist, zählte er 221 gefällte Baukiefern, nach seiner Angabe am 28. November des laufenden Jahres von Leuten aus Łukomia, Łomów und anderen Gütern Chełmskis geschlagen und auf dessen Güter fortgeschafft, bis auf sieben Klötze. Nach seiner Angabe geschah es auf Befehl Chełmskis.',
     "A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 7 December 1782, for Antoni Prusimski of Kolno, Starost of Niszczewice. With two noblemen, Adam Milewski and Jan Wilgiewicz, he was in the pine wood of Trąbczyn on the 4th of the current month. On the left of the line that was cut and staked under the decree of the Tribunal and of the sitting on the ground he counted 221 felled building pines, cut by his account on 28 November of the current year by people from Łukomia, Łomów and other estates of Chełmski's and carried off to those estates, all but seven logs. He states that it was done at Chełmski's order."),
 27: ('Protest vom 7. Dezember 1782, auf Polnisch, von Leon Maszewski, Verwalter von Trąbczyn, auf Befehl seines Herrn Antoni Prusimski von Kolno, Starost von Niszczewice, der selbst nicht vor den Büchern erscheinen konnte, gegen Stanisław Chełmski, Schatzmeister von Wschowa, dessen Diener Jaroszewski und andere; Maszewski hat im Namen seines Herrn unterschrieben. Chełmski wisse aus den Dekreten des Tribunals und des Ortstermins dieses Jahres, dass die Linie von der Ecke von Trąbczyn, Łukom und Drzewce bis zur Ecke mit Biskupice, vom Tribunal in die Karte gezogen und vom Geometer in Chełmskis Gegenwart im Gelände ausgehauen und abgepflockt, Trąbczyn von Łukomia scheidet. Dennoch habe er seine Leute aus Łomów und Łukom, die der Protest mit Namen nennt, mit Schlitten, Pferden, Ochsen und Äxten in den Kiefernwald links der Linie geschickt, der zu Trąbczyn gehört; sie hätten eine große Zahl Kiefern gefällt und nach Łukomia gebracht. Chełmskis Leute seien außerdem in Trąbczyn eingefallen, hätten Leute aus Trąbczyn auf der Straße angegriffen und andere Gewalttaten verübt.',
     "A protest of 7 December 1782, in Polish, by Leon Maszewski, steward of Trąbczyn, at the order of his lord Antoni Prusimski of Kolno, Starost of Niszczewice, who could not come before the books himself, against Stanisław Chełmski, Treasurer of Wschowa, his servant Jaroszewski and others; Maszewski signed in his lord's name. Chełmski knows from the decrees of the Tribunal and of this year's sitting on the ground that the line from the corner of Trąbczyn, Łukom and Drzewce to the corner with Biskupice, drawn on the map by the Tribunal and cut and staked on the ground by the surveyor in Chełmski's own presence, divides Trąbczyn from Łukomia. Yet he sent his people from Łomów and Łukom, whom the protest names, with sledges, horses, oxen and axes into the pine wood on the left of the line, which belongs to Trąbczyn; they felled a great number of pines and took them to Łukomia. Chełmski's people also rode into Trąbczyn, attacked people of Trąbczyn on the road and committed other acts of violence."),
 28: ('Registervermerk vom Dezember 1782: Das Grenzdekret des Ortstermins zwischen den Gütern Trąbczyn und Łukom, ergangen zwischen Antoni Prusimski, Starost von Niszczewice, Stanisław Chełmski, Schatzmeister von Wschowa, und anderen, mit der Beschreibung der Grenzhügel, wird zur Eintragung vorgelegt und liegt bei den vorgelegten Schriftstücken.',
     'A register note of December 1782: the boundary decree of the sitting on the ground between the estates of Trąbczyn and Łukom, given between Antoni Prusimski, Starost of Niszczewice, Stanisław Chełmski, Treasurer of Wschowa, and others, with the description of the boundary mounds, is brought in for entry and is among the documents produced.'),
 29: ('Registervermerk vom Dezember 1782: Für Antoni Prusimski, Starost von Niszczewice, liegt die Übergabe des Trąbczyner Olęders Martin Hunt bei den vorgelegten Schriftstücken, vorgenommen von Józef Łukaszewicz, Kommissar der großpolnischen Woiwodschaften.',
     'A register note of December 1782: for Antoni Prusimski, Starost of Niszczewice, the delivery of Martin Hunt, an Olęder settler of Trąbczyn, carried out by Józef Łukaszewicz, commissioner of the palatinates of Greater Poland, is among the documents produced.'),
}
HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
