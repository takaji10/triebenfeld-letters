# -*- coding: utf-8 -*-
"""APP 53/15/0/-/Kalisz Gr.414: from the editor's scans and texts to the edition.

    python units/app53150kaliszgr414/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                      [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The images. Two openings of a book of the castle court of Kalisz for 1771,
each named after the leaf on its right:

    402.jpg   leaf 401 verso | leaf 402 recto
    403.jpg   leaf 402 verso | leaf 403 recto

Leaf 402 is the original of the delivery of possession, a smaller sheet sewn
into the book ("in Protocollon Insutum est"); leaf 403 has the court's record
of its being brought in. Three pages are pages of the edition: 0402_a2,
0403_a1, 0403_a2 (leaf N recto is <N>_a2, leaf N verso is <N+1>_a1). Leaf
401 verso belongs to another document and is set apart.

One document: the delivery of possession of 4 November 1771 with the record
of its entry at Kalisz on 9 November.

The check (2026-10-07). The hand is clear and the editor's text close. Read
against the scans: the opening and the recital as far as the first decree
(leaf 402, about a third), the whole delivery in Polish with the settlers'
names and the closing (leaf 402 verso, lower two thirds), and the record on
leaf 403. Not compared: the middle of the recital of the Tribunal's decrees
(the foot of leaf 402 and the head of leaf 402 verso, about 200 words).
ROWS has what was corrected. "[I2867]" after one settler's name was the
editor's own reference number and is taken out.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53150kaliszgr414'
REF = 'APP 53/15/0/-/Kalisz Gr.414'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1771 (53.15.0.-.Kalisz Gr.414)"

# (file, x of the fold, left page, right page). First proposals; the editor's
# saved folds (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('402.jpg', 2520, '0402_a1', '0402_a2'),
    ('403.jpg', 2423, '0403_a1', '0403_a2'),
]
SKIP = ('0402_a1',)
LEAF = {'0402_a1': '401 verso', '0402_a2': '402 recto', '0403_a1': '402 verso', '0403_a2': '403 recto'}
PAGE_OF = {'402': '0402_a2', '402v': '0403_a1', '403': '0403_a2'}
DOCS = [(1, ['0402_a2', '0403_a1', '0403_a2'])]
FOLD_NOTE = 'Leaf 402 is a smaller sheet sewn into the book, so the fold of the first scan lies left of the middle.'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*Latin & Polish.md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert len(head) == 3 and head[0].startswith('# Relationes'), head        # the file's own heading: not text
    assert [l for l, _ in leaves] == ['402', '402v', '403'], [l for l, _ in leaves]
    return {(1, PAGE_OF[leaf]): paras for leaf, paras in leaves}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0402_a2', 'Haeredis et jurevicentis exhibitionemque', 'Haeredis et jurevincentis exhibitionemque',
     'the scan has "jurevincentis": the one who has won at law'),
    ('0403_a1', 'Bogusław Celmer [I2867], Samól', 'Bogusław Celmer, Samól',
     '"[I2867]" is not on the page: it is the editor\'s own reference number for the man'),
    ('0403_a1', 'Qua itaque per acta nomine impugnante traditione', 'Qua itaque peracta nemine impugnante traditione',
     'the scan has "peracta nemine impugnante": the delivery was completed and no one contested it'),
    ('0403_a1', 'praestandam indixit inpensitque Traditionis', 'praestandam indixit injunxitque Traditionis',
     'the scan has "injunxitque": and enjoined it'),
    ('0403_a2', 'obtulit officium praesentia ad acticandum', 'obtulit officio praesenti ad acticandum',
     'the scan has "offo pnti" with marks of abbreviation: presented to the present office'),
    ('0403_a2', 'Traditionem in supra seu Borra Lusnie', 'Traditionem in sylva seu Borra Lusnie',
     'the scan has "in sylva seu Borra", the words the delivery itself opens with'),
]

DROP_NOTES = {
    '5': 'on "jurevicentis"; the scan has "jurevincentis"',
    '19': 'on "per acta nomine impugnante" as a formal challenge; the scan has "peracta nemine impugnante", no one contesting',
    '21': 'on "inpensitque" as an unusual form; the scan has "injunxitque"',
    '22': 'on "in supra seu Borra" as a correction by the clerk; the scan has "in sylva seu Borra"',
}
FIXES = [
    ('Which delivery of possession, therefore — the delivery having been formally challenged by name through the records, '
     'and with the inventory having been drawn up — left the same Right Honourable Chełmski',
     'Which delivery of possession having thus been completed, no one contesting it, and the inventory having been drawn '
     'up, [the office] left the same Right Honourable Chełmski',
     '"Qua itaque peracta nemine impugnante traditione": the opposite of a challenge'),
    ('and declared and imposed upon the above-named olędry, as [those] possessing the lands of the Łukom estates, that '
     'obedience was to be rendered to the Right Honourable Chełmski — and imposed [this] by virtue of the present delivery '
     'of possession.',
     'and declared to the above-named olędry, as [those] possessing the lands of the Łukom estates, that obedience was to '
     'be rendered to the Right Honourable Chełmski, and enjoined it by virtue of the present delivery of possession.',
     '"indixit injunxitque"'),
    ('Krystyan Tulka, Bogusław Celmer, Samuel Frinderberg', 'Krystyan Tulka, Bogusław Zelmer, Samuel Frinderberg',
     'the edition gives this family as Zelmer in the English (the editor, 2026-09-11); the page has "Celmer"'),
    ('the Delivery of Possession conducted in the aforesaid pine forest, or rather in the Lusnia pine forest, pertaining',
     'the Delivery of Possession conducted in the woodland, or rather the pine forest, Lusnia, pertaining',
     '"in sylva seu Borra Lusnie"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*English Translation.md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0], DROP_NOTES)
    assert [l for l, _ in leaves] == ['402', '402v', '403'], [l for l, _ in leaves]
    order = [PAGE_OF[l] for l, _ in leaves]
    pages = {PAGE_OF[l]: p for l, p in leaves}
    for a, b in zip(order, order[1:]):                 # the editor's section heading belongs to the page it heads
        if pages[a] and pages[a][-1].startswith('[Section'):
            pages[b].insert(0, pages[a].pop())
    pages = courtbook.fix_english(pages, FIXES)
    return {1: ['\n\n'.join(pages[p]) for p in order]}


S = {
 1: ('Protokoll einer Besitzeinweisung, vorgenommen am 4. November 1771 im Wald Lusnia und am 9. November in die Akten des Burggerichts Kalisz eingetragen; das Original ist in das Buch eingenäht. Der vereidigte Kommissar der Woiwodschaften Posen und Kalisz, Wawrzyniec Wstowski, handelt auf Verlangen von Stanisław Ścibor Chełmski, Erbherrn von Łukomia, der vor Gericht obsiegt hat. Er führt die Urteile an, auf die sich die Einweisung stützt: eine Verurteilung von 1761, Dekrete des Krontribunals von 1766, 1767 und 1768, nach denen die Güter Łukom und Trąbczyn abzugrenzen waren, und eine dritte Verurteilung von 1770 gegen Antoni Prusimski, Starost von Niszczewice, wegen Zuwiderhandlung. Im Beisein dreier Adliger, des Trąbczyner Verwalters Józef Jaroszewski und eines Gerichtsboten übergibt er Chełmski den Kiefern- und Laubwald Lusnia als von alters zu Łukomia gehörig, samt der vor nicht langer Zeit darin gegründeten Olęder-Siedlung: ein Schankhaus mit neuem Stall, ohne Wirt, und zwölf mit Namen genannte Olęder. Niemand widerspricht; ein Inventar wird aufgenommen, Chełmski wird im ruhigen Besitz belassen, und den Olędern wird auferlegt, ihm Gehorsam zu leisten.',
     'The record of a delivery of possession, carried out on 4 November 1771 in the Lusnia wood and entered in the records of the castle court at Kalisz on 9 November; the original is sewn into the book. The sworn commissioner of the provinces of Poznań and Kalisz, Wawrzyniec Wstowski, acts at the request of Stanisław Ścibor Chełmski, heir of Łukomia, who has won at law. He recites the judgments on which the delivery rests: a condemnation of 1761, decrees of the Crown Tribunal of 1766, 1767 and 1768 under which the estates of Łukom and Trąbczyn were to be divided by a boundary, and a third condemnation of 1770 against Antoni Prusimski, Starost of Niszczewice, for contravention. In the presence of three noblemen, of the Trąbczyn steward Józef Jaroszewski and of a court messenger he hands over to Chełmski the pine forest and wood called Lusnia as belonging to Łukomia from of old, with the Olęder settlement founded in it not long before: a tavern house with a new stable, without a keeper, and twelve Olęder settlers, who are named. No one objects; an inventory is drawn up, Chełmski is left in peaceful possession, and the settlers are ordered to obey him.'),
}
HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
