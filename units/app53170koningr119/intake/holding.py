# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.119: from the editor's scans and texts to the edition.

    python units/app53170koningr119/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is the register of the castle court of Konin for 1783 and 1784, the
volume after Konin Gr.118. The editor photographed fourteen openings and
transcribed eight entries. Each entry is a document.

    doc  leaf        scan       page                what
    1    62, 62v     065, 066   0062_a2, 0063_a1    report: Chełmski cites Prusimski and Maszewski (March 1783)
    2    62v, 63     066        0063_a1, 0063_a2    report: Chełmski cites Prusimski for the inroad at Łomowo (March 1783)
    3    73          076        0073_a2             Chełmski's messenger searches for two reports (18 March 1783)
    4    73          076        0073_a2             report: Prusimski and others cite Chełmski (18 March 1783)
    5    128         131        0128_a2             report: Prusimski cites Chełmski on a penalty (22 May 1783)
    6    131         134        0131_a2             report: Chełmski cites Prusimski (May 1783)
    7    304v        310        0305_a1             Prusimski's protest (October 1783)
    8    685         679        0685_a2             Maszewski searches for a report (15 September 1784)

The scans are photographs named by their number in a series; leaf numbers
were read off the pages. Page ids: leaf N recto is <N>_a2, leaf N verso is
<N+1>_a1. The other half of each of the seven scans is set apart. The folds
are courtbook.find_fold's, two of them (065, 066) moved by eye; all are
first proposals for the editor.

Not used: seven scans with entries the editor did not transcribe (144, 320,
321, 348, 349, 680, 681); what is on them is listed in
docs/PRUSIMSKI_QUESTIONS.md. The line under "[140]" in the editor's file is
their own note on scan 144, not text.

The check (2026-10-07). Read against the scans, enlarged: every heading and
date line; documents 3, 4, 7 and 8 whole; the second half of document 1,
the body of document 2 and most of document 5. Document 6 and the first
half of document 1 were not read. ROWS has what was corrected; a phrase the
transcription had passed over in document 2 is restored.

The English is the editor's own. FIXES are the places where it followed a
reading that was corrected.

The full check (2026-10-07, at the editor's word, after they had read the
record of the first one). The two parts the first check had left were read
against the scans, enlarged, word for word: the first half of document 1
(leaf 62) and document 6 (leaf 131). Every entry of the holding is now read.
Its record is full_check.json beside this file (courtbook.full_check): 8
corrections (ROWS, applied with --full after --correct) and 4 places where
the English follows (FIXES, applied after the FIXES below). In document 6 a
line had been passed over: the citation was left "In Bonis Nowawieś
Praedioque Ibidem Sito super Scrinio hippi". The summary of document 6 says
so now (S).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

FULL = courtbook.full_check(HERE)

SLUG = 'app53170koningr119'
REF = 'APP 53/17/0/-/Konin Gr.119'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1783-1784 (53.17.0.-.Konin Gr.119)"

# (file, x of the fold, left page, right page). First proposals; the editor's
# saved folds (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('065.jpg', 1890, '0062_a1', '0062_a2'),
    ('066.jpg', 1940, '0063_a1', '0063_a2'),
    ('076.jpg', 1840, '0073_a1', '0073_a2'),
    ('131.jpg', 1968, '0128_a1', '0128_a2'),
    ('134.jpg', 1978, '0131_a1', '0131_a2'),
    ('310.jpg', 2170, '0305_a1', '0305_a2'),
    ('679.jpg', 2137, '0685_a1', '0685_a2'),
]
SKIP = ('0062_a1', '0073_a1', '0128_a1', '0131_a1', '0305_a2', '0685_a1')
LEAF = {'0062_a1': '61 verso', '0062_a2': '62 recto', '0063_a1': '62 verso', '0063_a2': '63 recto',
        '0073_a1': '72 verso', '0073_a2': '73 recto', '0128_a1': '127 verso', '0128_a2': '128 recto',
        '0131_a1': '130 verso', '0131_a2': '131 recto', '0305_a1': '304 verso', '0305_a2': '305 recto',
        '0685_a1': '684 verso', '0685_a2': '685 recto'}
DOCS = [(1, ['0062_a2', '0063_a1']), (2, ['0063_a1', '0063_a2']), (3, ['0073_a2']), (4, ['0073_a2']), (5, ['0128_a2']),
        (6, ['0131_a2']), (7, ['0305_a1']), (8, ['0685_a2'])]
FOLD_NOTE = ('Seven of the fourteen scans are shown: the ones with a transcribed entry. On one, both halves are pages of '
             'the edition; on six, one half is a page and the other is left out.')


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == [('62', 2), ('62v', 3), ('63', 1), ('73', 6), ('128', 3), ('131', 2), ('140', 1),
                                               ('304v', 3), ('685', 4)], [(l, len(p)) for l, p in leaves]
    L = dict(leaves)
    assert L['140'][0].startswith('[Relatio between Bronikowski'), L['140']
    return {
        (1, '0062_a2'): L['62'],
        (1, '0063_a1'): L['62v'][:1],
        (2, '0063_a1'): L['62v'][1:],
        (2, '0063_a2'): L['63'],
        (3, '0073_a2'): L['73'][:4],
        (4, '0073_a2'): L['73'][4:],
        (5, '0128_a2'): L['128'],
        (6, '0131_a2'): L['131'],
        (7, '0305_a1'): L['304v'],
        (8, '0685_a2'): L['685'],
    }


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0062_a2', 'ac per[e/a?][n/m?] plt~ Compareatis', 'ac peremptorie Compareatis', 'the scan has "perempt~" with a mark: the set phrase'),
    ('0062_a2', 'ad viden~ et Authen~ Vos', 'ad viden~ et Audien~ Vos', 'the scan has "Audien": to see and hear'),
    ('0062_a2', 'Inva[s?]orem Bo[u?][m?] Currus et Securum hominibus', 'Invasorem Boum Currus et Securium hominibus',
     'the scan has "Invasorem Boum Currus et Securium": oxen, carts and axes'),
    ('0062_a2', 'Causa E[o?]ehendarum non ni[s?]i pro', 'Causa Evehendarum non nisi pro', 'the scan has "Evehendarum non nisi"'),
    ('0062_a2', 'cum Pab~sis Thoma', 'cum Laboriosis Thoma', 'the scan has "Labsis" with a mark: Laboriosis, the working men'),
    ('0062_a2', 'Joanni Mathiae Ministerialis qui', 'Joanni Mathiae Ministerialibus qui', 'the scan has "Ministe|rialibus" over the line end'),
    ('0062_a2', 'mulctandem[?] Censori', 'mulctan~ Censeri', 'the scan has "mulctan" with a mark and "Censeri"'),
    ('0063_a1', 'de mandato Sui executae', 'de mandato Tui executae', 'the scan has "Tui": at your order'),
    ('0063_a1', 'Vestri Manifestatione[?] ac Visione', 'Vestri Manifestatione ac Visione', 'the word is plain on the scan'),
    ('0063_a1', 'Statutionem hominum demandeoque[?] Simiti[?]nium educendum', 'Statuitionem hominum demandari Scrutinium educendum',
     'the scan has "Statuitionem hominum demandari Scrutinium educendum": the production of the men to be ordered, an inquiry held'),
    ('0063_a1', '[B/P?]aedioque', 'Praedioque', 'the scan has "Praedioque": at the farm'),
    ('0063_a1', 'super Sell[e/a?] hippi praesen~ Siriba proventuali, Dae[?]orna~ Actu', 'super Sella hippi praesen~ Scriba proventuali, Die horna Actu',
     'the scan has "Sella", "Scriba" and "Die horna"'),
    ('0063_a2', 'Qui Se Inhaerendo Manifestantibus[?] factus sive faciendis Citant, Idque adviden~ et Audien~ Se paenis Respectu Bonorum Łomowo cum querra',
     'Qui Te Inhaerendo Manifestationibus factis sive faciendis Citant, Idque adviden~ et Audien~ Te paenis Respectu Bonorum Łomowo ad '
     'Principaliora Bona Łukom Sui Actt~ haereditt~ spectan~ cum querra',
     'the scan has "Te" twice and "Manifestationibus factis"; and after "Łomowo" a phrase that was passed over: "ad Principaliora Bona Łukom '
     'Sui Actt haereditt spectan"'),
    ('0063_a2', 'Mul[i?]tan[dem?] Censeri damna Compensanda injuri[g?][i?] pro quo Citt~ sis panitt~ et Judicialiter responsarum',
     'Mulctan~ Censeri damna Compensanda injungi pro quo Citt~ sis paritt~ et Judicialiter responsurus',
     'the scan has "Mulctan", "injungi", "paritt" and "responsurus"'),
    ('0063_a2', 'Die hodierna Acta Contenta', 'Die horna Actu Contenta', 'the scan has "Die horna Actu Contenta"'),
    ('0073_a2', 'praesenti, citrum[?] Relationes Citatiorum binarum', 'praesenti, utrum Relationes Citationum binarum', 'the scan has "utrum Relationes Citationum"'),
    ('0073_a2', 'per Ministerialis Recognovit et Termini ad Eacdem porrecti', 'per Ministeriales Recognitae et Termini ad Easdem porrecti',
     'the scan has "per Ministeriales Recognitae ... ad Easdem"'),
    ('0073_a2', 'Anni Immediate prot[a?]ti[?] Millesimi', 'Anni Immediate praeteriti Millesimi', 'the scan has "pteriti" with a mark: praeteriti'),
    ('0073_a2', 'Feriae Sextae[?] post', 'Feriae Sextae post', 'the word is plain on the scan'),
    ('0073_a2', 'Mathieum Mataszkiewicz de Villa Podbiele Ministerialem Regni Generalem Recognovit, ad',
     'Mathieum Matuszkiewicz de Villa Podbiele Ministerialem Regni Generalem Recognitam, ad',
     'the messenger is Matuszkiewicz (Konin Gr.117 and Gr.118); the report was "Recognitam", declared'),
    ('0073_a2', 'non provenit, Idea de inexistentia Eorundem publicam facit fiden~', 'non provenit, Ideo de inexistentia Earundem publicam facit fidem',
     'the scan has "Ideo de inexistentia Earundem publicam facit fidem"'),
    ('0073_a2', 'Pana Imienien', 'Pana Imieniem', 'the signature ends "Imieniem"'),
    ('0073_a2', 'Callisien~ pro re in Castro Calissien~ Celabrand~ Quia ex Parte', 'Callisien~ proxime in Castro Calissien~ Celebrand~ Qua ex Parte',
     'the scan has "proxime in Castro Calis Celebran Qua ex Parte"'),
    ('0073_a2', 'tum Generosum Leonis', 'tum Generosorum Leonis', 'the scan has "Gnorum": of the noble Leon Maszewski and Franciszek Liberacki'),
    ('0073_a2', 'Copiae et essentiate futuro', 'Copiae et essentiae futuro', 'the scan has "essentiae"'),
    ('0073_a2', 'Actum hornum praesedente', 'Actum hornum praecedente', 'the scan has "praecedente": the day before'),
    ('0128_a2', 'editi teneris sequentis', 'editt~ tenoris sequentis', 'the scan has "editt tenoris sequentis"'),
    ('0128_a2', 'Rarzyński', 'Raczyński', 'the scan has "Raczynski"'),
    ('0128_a2', 'de Bonis Tusi[?] ac', 'de Bonis Tuis ac', 'the scan has "Tuis"'),
    ('0128_a2', 'In Judiciis Stris~ Castren~', 'In Judiciis Nris~ Castren~', 'the scan has "Nris" with a mark: Nostris'),
    ('0128_a2', 'praempto Comparas Ad', 'perempto~ Compareas Ad', 'the scan has "pempto" with a mark and "Compareas"'),
    ('0128_a2', 'Qui Se Citt~ Idque pro Eo: Quatenus [T/S?]a Penam', 'Qui Te Citt~ Idque pro Eo: Quatenus Tu Penam', 'the scan has "Qui Te Citt" and "Tu"'),
    ('0128_a2', 'per Se Citt~ pro se Actt~ ad Erranium[?] Instigatorii', 'per Te Citt~ pro se Actt~ ad Aerarium Instigatorii', 'the scan has "per Te Citt" and "Aerarium"'),
    ('0128_a2', 'Leves procescumque[?] [?]e[i?]per se Actt~', 'Leves processumque super se Actt~', 'the scan has "Leves processumque super se Actt"'),
    ('0128_a2', 'sis parituru[?] est Judicialiter responsurus[?]', 'sis pariturus et Judicialiter responsurus', 'the scan has "pariturus et ... responsurus"'),
    ('0128_a2', 'Actum hornam praesedente', 'Actum hornum praecedente', 'the scan has "Actum hornum praecedente"'),
    ('0305_a1', 'Equeo succirrendo', 'Eques succurrendo', 'the scan has "Eques succurrendo"'),
    ('0305_a1', '[D/X?]enim', 'Etenim', 'the scan has "Etenim"'),
    ('0305_a1', 'extiten~ illico', 'extiterit illico', 'the scan has "extiterit"'),
    ('0305_a1', 'explicando [quod/quam?] haec', 'explicando quod haec', 'the scan has "qd" with a mark: quod'),
    ('0305_a1', 'per acta deducetur', 'peracta deducetur', 'one word: if it is shown to have been done by those men'),
    ('0305_a1', 'arestum non provenit ne igit~ aliquod ex inde pati vidiatur Damnum offer~ praesen~',
     'arestum non praevenit ne igit~ aliquod ex inde pati videatur Damnum offert praesen~',
     'the scan has "non praevenit" (the p with the mark for prae), "videatur" and "offert"'),
    ('0305_a1', 'Homines non prevenit Emandaturum', 'Homines non praevenit Emundaturum', 'the scan has "Emundaturum": that he will clear himself'),
    ('0685_a2', 'speciali Commissario Illustris', 'speciali Commisso Illustris', 'the scan has "Commisso": by special commission'),
    ('0685_a2', 'extradique Petit[tione?] Relationem ed itaque Citationis', 'extradique Petiit Relationem edittae Citationis',
     'the scan has "Petiit Relationem" with "edittae" written above the line'),
    ('0685_a2', 'Tribunalis Petricovien~', 'Tribunalis Regni Petricovien~', 'the scan has "Triblis Rni Petricovien"'),
    ('0685_a2', 'exportat[e?] ut[n/r?][o/u?]r[?] in Actis', 'exportatae utrum in Actis', 'the scan has "exportatae utrum"'),
    ('0685_a2', 'Reviso Protocollo pro factae Relationis publicam facis~ fide[m/n?]',
     'Reviso Protocollo Relationum a Feria Quinta proxime praeterita. De inexistentia praefatae Relationis, publicam facit fidem',
     'a line was passed over: the scan has "Reviso Protocollo Relaonum a Fra Quinta pxe pterita. De inexistentia pfatae Relaonis, publicam '
     'facit fidem". The office certifies that the report does NOT exist'),
]

FIXES = [
    ('are found to have been carried out on his orders', 'are found to have been carried out on your orders', '"de mandato Tui"'),
    ('the stationing of men and the leading out of [Simitinium] to be sentenced', 'the production of the men to be ordered and an inquiry to be conducted',
     '"Statuitionem hominum demandari Scrutinium educendum Sententiari"'),
    ('in the presence of a revenue scribe, [?], the contents', 'in the presence of the revenue scribe, on this present day, the contents', '"Die horna"'),
    ('in respect of the invasion of the estates of Łomowo with a hunting party',
     "in respect of the invasion of the estate of Łomowo, which belongs to the plaintiff's hereditary principal estate of Łukom, with a hunting party",
     'the phrase restored: "ad Principaliora Bona Łukom Sui Actoris haereditaria spectantium"'),
    ('damages to be compensated; injuries [to be redressed]; for which', 'and to be ordered to make good the damages; for which', '"damna Compensanda injungi"'),
    ('by the Honest Mathaeus Mataszkiewicz', 'by the Honest Mateusz Matuszkiewicz', 'the name as in Konin Gr.117 and Gr.118'),
    ('insofar as that penalty of fourteen Polish marks, paid by the cited party upon the plaintiff to the exchequer of the Instigator of the Court '
     'of the Crown Tribunal of Piotrków, and the minor processes against the plaintiff on that account, obtained from the Register of Penalties, '
     'be quashed, and the plaintiff declared free',
     'that you lift from the plaintiff the penalty of fourteen Polish marks, paid for the plaintiff to the exchequer of the Instigator of the '
     'Court of the Crown Tribunal of Piotrków, and that the process obtained against the plaintiff on that account from the Register of '
     'Penalties be quashed, and the plaintiff declared free',
     '"Quatenus Tu Penam ... a se Actore Leves processumque super se Actore ... Cassari": "Leves" is the verb, that you lift'),
    ('while as for the others, the arrest did not proceed', 'while the others the arrest did not reach', '"Alios vero arestum non praevenit"'),
    ('and that he will make amends for the arrest of the aforementioned men not having proceeded',
     'and to clear himself that the arrest did not reach the aforementioned men', '"quod Arestum praemissos Homines non praevenit Emundaturum"'),
    ('To which requisition the present office, granting it and reviewing the Protocol, makes public certification of the made relatio.',
     'To which requisition the present office, granting it and having reviewed the Protocol of Relationes from the Thursday last past, makes '
     'public certification of the non-existence of the aforesaid relatio.', 'the line restored: "De inexistentia praefatae Relationis"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [(l, len(p)) for l, p in leaves] == [('62', 3), ('62v', 3), ('62v', 3), ('63', 3), ('73', 5), ('73', 2), ('128', 6),
                                               ('131', 2), ('304v', 4), ('685', 5)], [(l, len(p)) for l, p in leaves]
    E = courtbook.fix_english({i: p for i, (_, p) in enumerate(leaves)}, FIXES + FULL['FIXES'])
    # "Capitaneus" is "Starost", as in the editor's other translations (the editor, spot sheet of 2026-10-07)
    E = {i: [x.replace('Captain-General of Greater Poland', 'Starost General of Greater Poland')
              .replace('Captain of Niszczewice', 'Starost of Niszczewice') for x in p] for i, p in E.items()}
    assert not any('Captain' in x for p in E.values() for x in p)
    j = '\n\n'.join
    return {1: [j(E[0]), j(E[1])], 2: [j(E[2]), j(E[3])], 3: [j(E[4])], 4: [j(E[5])], 5: [j(E[6])], 6: [j(E[7])],
            7: [j(E[8])], 8: [j(E[9])]}


S = {
 1: ('Bericht des Gerichtsboten Stanisław Stachowski von Łukomia, eingetragen in Konin im März 1783. Er hat eine Ladung des großpolnischen Generalstarosten Kazimierz Raczyński vom 10. März 1783 vor das Burggericht Kalisz zugestellt: an Antoni Prusimski, Starost von Niszczewice und Erbherrn von Trąbczyn, und an dessen Verwalter Leon Maszewski, auf Betreiben von Stanisław Chełmski, Schatzmeister von Wschowa und Erbherr von Łukom, und dessen Verwalter Ignacy Jaroszewski. Maszewski sei in den Kiefernwald eingefallen, den die Linie des nachkommissarischen Dekrets auf der Karte samt einem Olęder dem Gut Łukom belassen habe, und habe Chełmskis Leuten, die dort nur das nötige Holz holten, Ochsen, Wagen und Äxte abgenommen. Genannte Leute aus Trąbczyn und Nowa Wieś werden mit der Ladung unter Arrest gestellt; auch Prusimski soll bestraft werden, falls die Gewalttaten auf seinen Befehl geschahen. Der Bote hat die Ladung im Vorwerk von Nowa Wieś hinterlegt.',
     "A report of the court messenger Stanisław Stachowski of Łukomia, entered at Konin in March 1783. He has served a citation of the Starost General of Greater Poland, Kazimierz Raczyński, of 10 March 1783, before the castle court of Kalisz: on Antoni Prusimski, Starost of Niszczewice and heir of Trąbczyn, and on his steward Leon Maszewski, at the instance of Stanisław Chełmski, Treasurer of Wschowa and heir of Łukom, and of his steward Ignacy Jaroszewski. Maszewski is charged with breaking into the pine wood that the line of the post-commission decree on the map left, with one Olęder settler, to the estate of Łukom, and with taking oxen, carts and axes from Chełmski's people, who were fetching only the wood they needed. Named men of Trąbczyn and Nowa Wieś are put under arrest by the citation; Prusimski too is to be punished if the acts of violence were done at his order. The messenger left the citation at the farm at Nowa Wieś."),
 2: ('Bericht des Gerichtsboten Jan Bekierski von Węgierce, eingetragen in Konin im März 1783. Er hat Antoni Prusimski, Starost von Niszczewice, eine Ladung des Generalstarosten vom 10. März 1783 vor das Burggericht Kalisz zugestellt, auf Betreiben von Stanisław Chełmski und dessen Verwalter Ignacy Jaroszewski. Prusimski soll bestraft werden wegen eines Einfalls mit Leuten und Hunden in das Gut Łomowo, das zu Chełmskis Hauptgut Łukom gehört, und wegen dort verübter Gewalttaten, und den Schaden ersetzen. Der Bote hat die Ladung bei den Olędern von Trąbczyn im Haus eines Mathias hinterlegt, in Gegenwart von dessen Frau.',
     "A report of the court messenger Jan Bekierski of Węgierce, entered at Konin in March 1783. He has served on Antoni Prusimski, Starost of Niszczewice, a citation of the Starost General of 10 March 1783 before the castle court of Kalisz, at the instance of Stanisław Chełmski and of his steward Ignacy Jaroszewski. Prusimski is to be punished for an inroad with men and dogs into the estate of Łomowo, which belongs to Chełmski's principal estate of Łukom, and for acts of violence done there, and is to make good the damage. The messenger left the citation among the Olęder settlers of Trąbczyn, at the house of one Mathias, in the presence of his wife."),
 3: ('Eintrag vom 18. März 1783. Der Gerichtsbote Stanisław Stachowski von Łukomia fragt im Namen von Stanisław Chełmski, Schatzmeister von Wschowa, ob die Berichte über zwei Ladungen, die Antoni Prusimski, Starost von Niszczewice, gegen Chełmski vor das Burggericht Kalisz erwirkt und nach Łukomia hat bringen lassen, vor dem Amt erklärt worden sind. Das Amt hat das Register vom 26. November 1782 bis zu diesem Tag durchgesehen und nur einen Bericht vom 29. November gefunden, erklärt vom Gerichtsboten Matuszkiewicz von Podbiele; es bescheinigt, dass weitere nicht vorliegen. Stachowski hat für sich und seinen Herrn unterschrieben.',
     'An entry of 18 March 1783. The court messenger Stanisław Stachowski of Łukomia asks, in the name of Stanisław Chełmski, Treasurer of Wschowa, whether the reports of two citations that Antoni Prusimski, Starost of Niszczewice, obtained against Chełmski before the castle court of Kalisz and had taken to Łukomia have been declared before the office. The office has looked through its register from 26 November 1782 to that day and found only one report, of 29 November, declared by the court messenger Matuszkiewicz of Podbiele; it certifies that there are no others. Stachowski signed for himself and his master.'),
 4: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 18. März 1783. Er hat eine Ladung vor das Burggericht Kalisz zugestellt, die Antoni Prusimski von Kolno, Starost von Niszczewice, mit Leon Maszewski, Franciszek Liberacki und anderen gegen Stanisław Chełmski, Schatzmeister von Wschowa, und andere erwirkt hat. Er hat sie am Vortag im Gutshof von Łukom in Gegenwart des Geladenen hinterlegt.',
     'A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 18 March 1783. He has served a citation before the castle court of Kalisz that Antoni Prusimski of Kolno, Starost of Niszczewice, with Leon Maszewski, Franciszek Liberacki and others, obtained against Stanisław Chełmski, Treasurer of Wschowa, and others. He left it the day before at the manor of Łukom in the presence of the man cited.'),
 5: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 22. Mai 1783. Er hat Stanisław Chełmski, Schatzmeister von Wschowa, eine Ladung des Generalstarosten Kazimierz Raczyński vom 15. Mai 1783 vor das Burggericht Kalisz zugestellt, auf Betreiben von Antoni Prusimski von Kolno, Starost von Niszczewice. Es geht um eine Strafe von vierzehn polnischen Mark, die an die Kasse des Instigators des Krontribunals in Petrikau gezahlt wurde; das deswegen aus dem Strafregister gegen Prusimski erwirkte Verfahren soll aufgehoben und Prusimski freigesprochen werden. Der Bote hat die Ladung im Gutshof von Łukom hinterlegt.',
     'A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 22 May 1783. He has served on Stanisław Chełmski, Treasurer of Wschowa, a citation of the Starost General Kazimierz Raczyński of 15 May 1783 before the castle court of Kalisz, at the instance of Antoni Prusimski of Kolno, Starost of Niszczewice. It concerns a penalty of fourteen Polish marks paid into the chest of the Instigator of the Crown Tribunal at Piotrków; the process obtained against Prusimski on that account from the register of penalties is to be quashed and Prusimski declared free. The messenger left the citation at the manor of Łukom.'),
 6: ('Bericht des Gerichtsboten Stanisław Stachowski von Łukomia, eingetragen in Konin im Mai 1783. Er hat eine Ladung vor das Burggericht Kalisz zugestellt, die Stanisław Chełmski, Schatzmeister von Wschowa, und andere gegen Antoni Prusimski von Kolno, Starost von Niszczewice, und andere erwirkt haben. Er hat sie im Vorwerk von Nowa Wieś hinterlegt.',
     'A report of the court messenger Stanisław Stachowski of Łukomia, entered at Konin in May 1783. He has served a citation before the castle court of Kalisz that Stanisław Chełmski, Treasurer of Wschowa, and others obtained against Antoni Prusimski of Kolno, Starost of Niszczewice, and others. He left it at the farm at Nowa Wieś.'),
 7: ('Protest von Antoni Prusimski von Kolno, Starost von Niszczewice, gegen Stanisław Chełmski, Schatzmeister von Wschowa, eingetragen in Konin im Oktober 1783 und von ihm unterschrieben. Chełmski habe ihn vor das Landgericht in Konin geladen, damit er Leute stelle, von denen einige in seinem Dienst stehen und andere bei ihm nicht zu finden sind, und damit er wegen einer angeblich verübten Gewalttat bestraft werde. Prusimski erklärt: Sollte die Gewalttat von diesen Leuten begangen worden sein, so geschah sie ohne sein Wissen und ohne seinen Befehl; stellen könne er nur zwei der in der Ladung Genannten, Gregor und Thomas; die anderen habe der Arrest nicht erreicht. Er bietet an, sich auch durch Zeugenverhöre zu reinigen, und will wegen der unbegründeten Belästigung Strafen fordern.',
     'A protest of Antoni Prusimski of Kolno, Starost of Niszczewice, against Stanisław Chełmski, Treasurer of Wschowa, entered at Konin in October 1783 and signed by him. Chełmski has cited him before the land court at Konin to produce men, some of them in his service and others not to be found with him, and to be punished for an act of violence said to have been done. Prusimski declares: if the act was done by those men, it was done without his knowledge and without his order; he can produce only two of those named in the citation, Gregory and Thomas; the arrest did not reach the others. He offers to clear himself by an examination of witnesses as well, and means to claim penalties for the groundless vexation.'),
 8: ('Eintrag vom 15. September 1784. Leon Maszewski, Kommissar der Trąbczyner Güter, fragt im Namen von Antoni Prusimski von Kolno, Starost von Niszczewice, ob der Bericht über eine Ladung vor das Krontribunal in Petrikau, die Stanisław Ścibor Chełmski, Schatzmeister von Wschowa, erwirkt hat und die am Donnerstag nach Mariä Geburt des laufenden Jahres nach Trąbczyn gebracht wurde, vor dem Amt erklärt worden ist. Das Amt hat sein Register durchgesehen und bescheinigt, dass ein solcher Bericht nicht vorliegt. Maszewski hat im Namen Prusimskis unterschrieben.',
     "An entry of 15 September 1784. Leon Maszewski, commissioner of the Trąbczyn estates, asks in the name of Antoni Prusimski of Kolno, Starost of Niszczewice, whether the report of a citation before the Crown Tribunal at Piotrków, obtained by Stanisław Ścibor Chełmski, Treasurer of Wschowa, and taken to Trąbczyn on the Thursday after the Nativity of the Virgin of the current year, has been declared before the office. The office has looked through its register and certifies that there is no such report. Maszewski signed in Prusimski's name."),
}
HOW = ('written in the working session from the Latin as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
