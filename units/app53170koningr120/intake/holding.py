# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.120: from the editor's scans and texts to the edition.

    python units/app53170koningr120/intake/holding.py [--crop] [--sheet] [--write] [--correct] [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is the register of the castle court of Konin for 1785 and 1786.
The editor photographed two openings and transcribed two entries.

    doc  leaf         scan  page               what
    1    63           063   0063_a2            a Trąbczyn subject shows his injuries (14 March 1785)
    2    623v, 624    632   0624_a1, 0624_a2   report: Chełmski cites Prusimski to the Tribunal (late 1786)

Page ids: leaf N recto is <N>_a2, leaf N verso is <N+1>_a1. The left half of
063.jpg is set apart. The folds were set by eye; first proposals for the
editor.

Near the head of document 2 six lines are struck out (the clerk began the
text of another citation and crossed it through); they are not transcribed
(docs/EDITORIAL_RULES.md), and the editor did not transcribe them either.

The check (2026-10-07). Both entries were read whole against the scans.
ROWS has what was corrected; words the transcription had passed over near
the end of document 2 are restored. Left as the editor has them:
"Sarzyński" (the scan may have "Saryński"), "discedenti", "Trachultz",
"hippercausti", "praesente Conte Citati".
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr120'
REF = 'APP 53/17/0/-/Konin Gr.120'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1785-1786 (53.17.0.-.Konin Gr.120)"

# (file, x of the fold, left page, right page). First proposals, set by eye.
SCANS = [
    ('063.jpg', 2180, '0063_a1', '0063_a2'),
    ('632.jpg', 2145, '0624_a1', '0624_a2'),
]
SKIP = ('0063_a1',)
LEAF = {'0063_a1': '62 verso', '0063_a2': '63 recto', '0624_a1': '623 verso', '0624_a2': '624 recto'}
DOCS = [(1, ['0063_a2']), (2, ['0624_a1', '0624_a2'])]
FOLD_NOTE = 'Both scans are shown. The left half of the first is left out.'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == [('63', 3), ('623v', 3), ('624', 1)], leaves
    L = dict(leaves)
    return {(1, '0063_a2'): L['63'], (2, '0624_a1'): L['623v'], (2, '0624_a2'): L['624']}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0063_a2', 'Commonstrant Officio praesenti Concessiones Infrascripta ut pote Oculuri dextrum',
     'Commonstravit Officio praesenti Contusiones Infrascriptas ut pote Oculum dextrum',
     'the scan has "Commonstravit ... Contusiones Infrascriptas ut pote Oculum": he showed the bruises written below'),
    ('0063_a2', 'Oculum Sinostrum', 'Oculum Sinistrum', 'the scan has "Sinistrum"'),
    ('0063_a2', 'intumefactos [i?]ctos Quae', 'intumefactos Quae', 'the word after "intumefactos" is struck out'),
    ('0063_a2', 'Idem Obduciens per', 'Idem Obducens per', 'the scan has "Obducens"'),
    ('0063_a2', 'viam praecidendo Sabbatho proximo praeterito vi et violanter', 'viam praecludens Sabbatho proximo praeterito vi et violenter',
     'the scan has "praecludens", barring the way, after a struck word; and "violenter"'),
    ('0624_a1', 'de Bonis Tcies~[?] Mandamus [?]eri Judiciis', 'de Bonis Tuis Mandamus ut in Judiciis', 'the scan has "de Bonis Tuis Mandamus ut in Judiciis"'),
    ('0624_a1', 'recete in Quatuor Septimaris', 'recte in Quatuor Septimanis', 'the scan has "recte in Quatuor Septimanis"'),
    ('0624_a1', 'Causa praesens Regno Sibi Competenti', 'Causa praesens Regestro Sibi Competenti', 'the scan has "Regro" with a mark: the register the cause belongs to'),
    ('0624_a1', 'personaliter legitimes Compareas Ad Instantium', 'personaliter legitimeque Compareas Ad Instantiam', 'the scan has "legitimeque" and "Instantiam"'),
    ('0624_a1', 'Actt~, Qu[?] Te ad paratas Inscriptiones Connexas et Comportationem Citt~', 'Actt~, Qui Te ad paratas Inscriptiones Connexas et Competentes Citt~',
     'the scan has "Qui Te ... Connexas et Competentes Citt"'),
    ('0624_a1', 'Specifici Di[?]menti Scilicet Contractus Intuita Divenditionis Sylvae [?]cineae cum Spectabili Joanne Trachultz Incti et Confe[c?][?]',
     'Specifici Documenti Scilicet Contractus Intuitu Divenditionis Sylvae quercineae cum Spectabili Joanne Trachultz Initi et Confecti',
     'the scan has "Documenti", "Intuitu", "Sylvae quer|cineae" over the line end (an oak wood, as in the protest of 1778) and "Initi et Confecti"'),
    ('0624_a2', 'praei[s?]o[praeitero?] Juramento', 'praevio Juramento', 'the scan has "praevio Juramento": an oath first being taken'),
    ('0624_a2', 'ad Judicium ple[r/n?][c[u?][i?]m, quam', 'ad Judicium plenum, quam', 'the scan has "plenum"'),
    ('0624_a2', 'ad Judiciium Tribunalitium exprocuratae Remissionis Confraque', 'ad Judicium Tribunalitium exprocuratae Remissionis Contraque', 'the scan has "Judicium" and "Contraque"'),
    ('0624_a2', 'et praestandam ac Anteriores', 'et praestandam Injungi. Caetera Secundum Conclusionem ponendam ac Anteriores',
     'four words were passed over: "Injungi. Caetera Secundum Conclusionem ponendam"'),
    ('0624_a2', 'Actu expresserum', 'Actu expressorum', 'the scan has "expressorum"'),
]

FIXES = [
    ('showing to the present office the following submissions below, namely', 'showed to the present office the bruises written below, namely',
     '"Commonstravit ... Contusiones Infrascriptas"'),
    ('likewise the right shoulders swollen and struck.', 'likewise the right shoulders swollen.', 'the word after "intumefactos" is struck out'),
    ('of the goods of Trąmpczyn — We command your appearance at our Ordinary General Sessions', 'regarding your goods We command that at our Ordinary General Sessions',
     '"de Bonis Tuis Mandamus ut in Judiciis"'),
    ('when the present cause, competent to the Kingdom for judgment, being called and proclaimed, shall fall due; that you appear personally and legitimately.',
     'when the present cause, called and proclaimed for judgment from the register competent to it, shall fall due, you appear personally and lawfully,',
     '"Regestro Sibi Competenti"; one sentence'),
    ('At the instance of Right Honourable', 'at the instance of Right Honourable', 'the sentence runs on'),
    ('who [cites] you to prepared connected registrations and to the presentation of citations, and to see and hear you to the presentation of '
     'the specific settlement, namely the contract for the sale of pine woodland, entered into and concluded with the Honourable Joannes '
     'Trachultz, defendant,',
     'who cites you to the prepared, connected and competent inscriptions, to see and hear yourself — to the production of a specific document, '
     'namely the contract for the sale of oak woodland, entered into and concluded with the Honourable Joannes Trachultz,',
     '"Connexas et Competentes"; "Specifici Documenti"; "Sylvae quercineae", oak; no "defendant" in the text'),
    ('and to be rendered; and the earlier terms', 'and ordered to be rendered; the rest according to the conclusion to be put; and the earlier terms',
     'the words restored: "Injungi. Caetera Secundum Conclusionem ponendam"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [(l, len(p)) for l, p in leaves] == [('63', 3), ('623v', 3), ('624', 3)], leaves
    E = courtbook.fix_english(dict(leaves), FIXES)
    j = '\n\n'.join
    return {1: [j(E['63'])], 2: [j(E['623v']), j(E['624'])]}

S = {
 1: ('Eintrag vom 14. März 1785 im Buch des Burggerichts Konin. Andrzej Kinos, ein Untertan aus dem Dorf Trąbczyn, zeigt dem Amt seine Verletzungen: das rechte Auge ringsum blutunterlaufen, darunter geschwollen und blau, das linke Auge blutunterlaufen und blau, das ganze Gesicht geschwollen, die rechte Schulter geschwollen. Er gibt an, Marcin Sarzyński habe sie ihm am vergangenen Samstag mit Fäusten und einem Stock zugefügt, als er ihm im Dorf Obory auf öffentlicher Straße den Weg zur Stadt Pleszew versperrte.',
     'An entry of 14 March 1785 in the book of the castle court at Konin. Andrzej Kinos, a subject from the village of Trąbczyn, shows the office his injuries: the right eye suffused with blood all round and swollen and livid beneath, the left eye suffused with blood and livid, the whole face swollen, the right shoulder swollen. He states that Marcin Sarzyński inflicted them on him with fists and a stick on the Saturday before, barring his way on the public road in the village of Obory as he was going to the town of Pleszew.'),
 2: ('Bericht des Gerichtsboten Sebastian Biegański von Sławsk, eingetragen in Konin Ende 1786. Er hat Antoni Prusimski von Kolno, Starost von Niszczewice, eine königliche Ladung vor das Krontribunal in Petrikau zugestellt, ausgestellt in Petrikau am 2. Oktober 1786, auf Betreiben von Stanisław Chełmski, Schatzmeister von Wschowa. Prusimski soll unter Eid angehalten werden, eine bestimmte Urkunde vorzulegen, die bei ihm verblieben sei: den mit dem Kaufmann Jan Tracholz geschlossenen Vertrag über den Verkauf eines Eichenwaldes. Er soll ferner dafür bestraft werden, dass er die Sache vom Gericht des Ortstermins an das volle Landgericht und von dort an das Tribunal hat verweisen lassen; die Dekrete des Kalischer Landgerichts in Konin, die den Ortstermin ansetzen, sollen vollzogen werden. Der Bote hat die Ladung im Gutshof von Trąbczyn hinterlegt.',
     'A report of the court messenger Sebastian Biegański of Sławsk, entered at Konin at the end of 1786. He has served on Antoni Prusimski of Kolno, Starost of Niszczewice, a royal citation before the Crown Tribunal at Piotrków, dated at Piotrków on 2 October 1786, at the instance of Stanisław Chełmski, Treasurer of Wschowa. Prusimski is to be bound under oath to produce a particular document said to have stayed with him: the contract made with the merchant Jan Tracholz for the sale of an oak wood. He is also to be punished for having had the cause sent from the court of the sitting on the ground to the full land court and from there to the Tribunal; the decrees of the Kalisz land court at Konin that fix the sitting on the ground are to be carried out. The messenger left the citation at the manor of Trąbczyn.'),}

HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
