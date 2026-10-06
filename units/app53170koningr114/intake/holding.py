# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.114: from the editor's scans and texts to the edition.

    python units/app53170koningr114/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The images. Fourteen from the archive: 297.jpg and 297v.jpg, single pages
(leaf 297 recto and verso), and 334.jpg to 345.jpg, twelve openings of the
same book, each named after the leaf on its right (334.jpg is leaf 333 verso
and leaf 334 recto).

Two entries are transcribed, both reports of the court messenger Bartłomiej
Szepczyński for Antoni Prusimski in 1767, and each is a document ("Gr. 114 as
two entries of the one volume": the editor, 2026-10-06):

  1  the foot of leaf 297 and the top of leaf 297 verso: the embankment at
     the end of the pond-ground (22 April 1767)
  2  the foot of leaf 334 and the top of leaf 334 verso: the same embankment
     again (6 August 1767)

So four pages are pages of the edition: 0297_a2, 0298_a1, 0334_a2 and
0335_a1 (leaf N recto is <N>_a2, leaf N verso is <N+1>_a1). The other halves
of scans 334 and 335 are cut and set apart. Scans 336 to 345 carry none of
the transcribed text and are not used; whether anything on them is wanted is
a question held for the editor. Every page has many other short entries,
which are not transcribed; the pages are kept whole.

The texts. The editor's "(Original).md" has both entries. A second pair of
files, "... 334-334v ...", has the second entry again with a longer English
and notes: a duplicate, not used. The English is taken from "(English).md",
which has both.

The check (2026-10-07): both entries read whole against the scans. The
editor's text is close; three readings corrected (ROWS).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr114'
REF = 'APP 53/17/0/-/Konin Gr.114'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1765-1767 (53.17.0.-.Konin Gr.114)"

# (file, x of the fold or None for a single page, left page or the page, right
# page). The folds are a first proposal; the editor's saved folds
# (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('297.jpg', None, '0297_a2', None),
    ('297v.jpg', None, '0298_a1', None),
    ('334.jpg', 2772, '0334_a1', '0334_a2'),
    ('335.jpg', 2759, '0335_a1', '0335_a2'),
]
SKIP = ('0334_a1', '0335_a2')
LEAF = {'0297_a2': '297 recto', '0298_a1': '297 verso', '0334_a1': '333 verso', '0334_a2': '334 recto',
        '0335_a1': '334 verso', '0335_a2': '335 recto'}
DOCS = [(1, ['0297_a2', '0298_a1']), (2, ['0334_a2', '0335_a1'])]
FOLD_NOTE = 'Scans 336 to 345 are not shown: nothing on them is transcribed.'
WHERE = {'297': (1, '0297_a2'), '297v': (1, '0298_a1'), '334': (2, '0334_a2'), '334v': (2, '0335_a1')}


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*Gr.114) (Original).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head and [l for l, _ in leaves] == ['297', '297v', '334', '334v'], (head, [l for l, _ in leaves])
    return {WHERE[leaf]: paras for leaf, paras in leaves}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0298_a1', 'Bonorum Haeredis hic temporibus facta', 'Bonorum Haeredis his temporibus facta',
     'the scan has "his temporibus": done in these times'),
    ('0334_a2', 'Pro Praesente Haeredis Trąmpczyna Granitialis Visio', 'Pro Parte Haeredis Trąmpczyna Granitialis Visio',
     'the scan has "Pro Pte", as over the entry on leaf 297: for the party of the heir of Trąbczyn'),
    ('0334_a2', 'Providus Bartholomeus Szepczyński Ministerialis Regalis Generalis',
     'Providus Bartholomeus Szepczyński de Trąmpczyn Ministerialis Regalis Generalis',
     '"de Trąmpczyn" stands on the scan after the name and was left out'),
]

FIXES = [
    ('with its appurtenances, who on the Holy Saturday not long past had descended',
     'with its appurtenances — on the Holy Saturday not long past had descended',
     'it is the messenger who went to the ground ("ipse ... condescenderat"), not Prusimski'),
    ('which aforementioned things he asserted had been done here, at that time, by the people',
     'which aforementioned things he asserted had been done in these times by the people', '"his temporibus"'),
    ('Boundary Judicial Site Inspection — for the Heir of Trąmpczyn, Present',
     'Boundary Judicial Site Inspection — on behalf of the Heir of Trąmpczyn', '"Pro Parte"'),
    ('the Honest Bartłomiej Szepczyński, Royal Court Summoner, General,',
     'the Honest Bartłomiej Szepczyński of Trąmpczyn, Royal Court Summoner, General,', '"de Trąmpczyn"'),
    ('with its appurtenances, who on the Friday next after the Feast of Saint James the Apostle in the present year had descended',
     'with its appurtenances — on the Friday next after the Feast of Saint James the Apostle in the present year had descended',
     'as in the first entry: the messenger went to the ground'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*Gr.114) (English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [l for l, _ in leaves] == ['297', '297v', '334', '334v'], [l for l, _ in leaves]
    pages = courtbook.fix_english({l: p for l, p in leaves}, FIXES)
    return {1: ['\n\n'.join(pages['297']), '\n\n'.join(pages['297v'])],
            2: ['\n\n'.join(pages['334']), '\n\n'.join(pages['334v'])]}


S = {
 1: ('Bericht des Gerichtsboten Bartłomiej Szepczyński aus dem Dorf Trąbczyn, am 22. April 1767 in die Akten des Burggerichts Konin eingetragen. Auf Verlangen von Antoni Prusimski von Kolno, Erbherrn von Trąbczyn, ist er am Karsamstag mit zwei Adligen, Stanisław Lipiński und Józef Rudkowski, auf das Gut gegangen und hat einen Damm besichtigt, der vor kurzem am Ende des Teichgrunds aufgeschüttet wurde. Durch den Damm staute sich das Wasser, das aus dem Teichgrund durch die Trąbczyner Fluren fließt, zurück und überschwemmte die Olęder, die in den Trąbczyner Wäldern angesiedelt sind, samt ihren gedüngten Äckern und ihren Wiesen. Nach seiner Angabe haben das Leute des Nachbarguts Łukom auf Befehl von dessen Erbherrn getan.',
     'The report of the court messenger Bartłomiej Szepczyński of the village of Trąbczyn, entered in the records of the castle court at Konin on 22 April 1767. At the request of Antoni Prusimski of Kolno, heir of Trąbczyn, he went onto the estate on Holy Saturday with two noblemen, Stanisław Lipiński and Józef Rudkowski, and inspected an embankment lately raised at the end of the pond-ground. Because of the embankment the water that flows from the pond-ground through the Trąbczyn lands backed up and flooded the Olęder settlers living in the Trąbczyn woods, with their manured fields and their meadows. He states that this was done by people of the neighbouring estate of Łukom on the order of its heir.'),
 2: ('Zweiter Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn über denselben Damm, am 6. August 1767 in die Akten des Burggerichts Konin eingetragen. Auf Verlangen von Antoni Prusimski von Kolno ist er am Freitag nach St. Jakob mit zwei Adligen, Józef Gołembiewski und Rudkowski, wieder auf das Gut gegangen. Der Damm ist im Wald auf dem Teichgrund an der Grenze der Łukomer Fluren auf Trąbczyner Grund aufgeschüttet; das im Teich gestaute Wasser tritt auf die Äcker und Wiesen der Trąbczyner Olęder über, so dass die Wiesen von vier von ihnen überschwemmt sind und sich nicht mähen lassen. Der Bote erklärt mit den beiden Adligen, der Damm sei vor einigen Jahren von den Erbherren von Łukomia aufgeschüttet und jetzt ausgebessert worden.',
     'A second report of the court messenger Bartłomiej Szepczyński of Trąbczyn on the same embankment, entered in the records of the castle court at Konin on 6 August 1767. At the request of Antoni Prusimski of Kolno he went onto the estate again on the Friday after Saint James with two noblemen, Józef Gołembiewski and Rudkowski. The embankment is raised in the wood on the pond-ground, by the boundary of the Łukom lands, on Trąbczyn ground; the water dammed in the pond spills onto the fields and meadows of the Trąbczyn Olęder settlers, so that the meadows of four of them are flooded and cannot be mown. The messenger declares with the two noblemen that the embankment was raised some years ago by the heirs of Łukomia and has now been repaired.'),
}
HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
