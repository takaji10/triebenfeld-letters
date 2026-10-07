# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.121: from the editor's scans and texts to the edition.

    python units/app53170koningr121/intake/holding.py [--crop] [--sheet] [--write] [--correct] [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is the register of the castle court of Konin for 1787 and 1788.
The editor photographed two openings and transcribed one entry, which
begins on leaf 563 (570.jpg, right) and ends on leaf 563 verso (571.jpg,
left). Page ids: 0563_a2 and 0564_a1. The other two halves are set apart.
The folds are courtbook.find_fold's; first proposals for the editor.

The check (2026-10-07). The entry was read whole against the scans. ROWS
has what was corrected. Left as the editor has them: "płony" and
"przekobiały" in the Polish description of the oxen, and "szybowanemi".
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr121'
REF = 'APP 53/17/0/-/Konin Gr.121'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1787-1788 (53.17.0.-.Konin Gr.121)"

# (file, x of the fold, left page, right page). First proposals.
SCANS = [
    ('570.jpg', 2103, '0563_a1', '0563_a2'),
    ('571.jpg', 2105, '0564_a1', '0564_a2'),
]
SKIP = ('0563_a1', '0564_a2')
LEAF = {'0563_a1': '562 verso', '0563_a2': '563 recto', '0564_a1': '563 verso', '0564_a2': '564 recto'}
DOCS = [(1, ['0563_a2', '0564_a1'])]
FOLD_NOTE = 'Both scans are shown. On each, one half is a page of the edition and the other is left out.'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == [('563', 3), ('563v', 1)], leaves
    L = dict(leaves)
    return {(1, '0563_a2'): L['563'], (1, '0564_a1'): L['563v']}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0563_a2', 'Officio Eidem Currentem cum', 'Officio Eidem Currum cum', 'the scan has "Currum": a cart'),
    ('0563_a2', 'als zbosemi przedmiemi Kołami', 'als z bosemi przedniemi Kołami', 'the scan has "z bosemi przedniemi": with bare front wheels'),
    ('0563_a2', 'nec non Vacam pili', 'nec non Vaccam pili', 'the scan has "Vaccam"'),
    ('0563_a2', 'z bura potrey sierci', 'z bura pstrey sierci', 'the scan has "pstrey", mottled, the word used of the ox a line above'),
    ('0563_a2', 'Currui suprascripti cum', 'Currui suprascripto cum', 'the scan has "suprascripto"'),
    ('0564_a1', 'praesentatos I[d?] Idem', 'praesentatos Is Idem', 'the scan has "Is Idem"'),
    ('0564_a1', 'ad statim[?] Extraditionem', 'ad statim Extraditionem', 'the word is plain on the scan'),
    ('0564_a1', 'fusius nisi edisserit) reliquit reliquitque plus[?] praesentia', 'fusius in se edisserit) reliquit relinquitque per praesentia',
     'the scan has "fusius in se edisserit" and "reliquit relinquitque per praesentia": the receipt sets it out more fully; he left them and leaves them by these presents'),
]

FIXES = [
    ('presented to the said Office the vehicle', 'presented to the said Office a cart', '"Currum"'),
    ('that is of dun, [potrey] coat', 'that is of dun mottled coat', '"z bura pstrey sierci"'),
    (', will set forth more fully, unless [he] shall have explained otherwise)', ', sets forth more fully)', '"fusius in se edisserit"'),
    ('and left and left [them] further with the present [Chancellery].', 'and left, and leaves [them], by these presents.', '"reliquit relinquitque per praesentia"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [(l, len(p)) for l, p in leaves] == [('563', 3), ('563v', 1)], leaves
    E = courtbook.fix_english(dict(leaves), FIXES)
    j = '\n\n'.join
    return {1: [j(E['563']), j(E['563v'])]}

S = {
 1: ('Eintrag vom 9. Juni 1788 im Buch des Burggerichts Konin. Ludwik Żurawski, im Dienst von Antoni Prusimski von Kolno, Starost von Niszczewice und Erbherr von Trąbczyn, führt dem Amt ein Gespann vor: einen Wagen, vorn mit unbeschlagenen und hinten mit beschlagenen Rädern, zwei Ochsen, eine Kuh und eine kastanienbraune Stute. Das Gespann gehört Marcin Gryndel, einem Bauern aus Łomowo, einem Gut von Chełmski, Schatzmeister von Wschowa, das zu dessen Hauptgut Łukom gehört. Gryndel war in den Kiefernwald gefahren, der zu Prusimskis Erbgut Trąbczyn gehört und nie strittig war, und fuhr von dort schon einen gefällten, zum Bauen tauglichen Baum nach Hause; der Trąbczyner Waldhüter hielt ihn im Wald an. Nach der Vorführung überlässt Żurawski Tiere und Wagen bei der Kanzlei zur Herausgabe an Gryndel, der sie sofort verlangt; darüber ist am selben Tag eine Quittung eingetragen.',
     "An entry of 9 June 1788 in the book of the castle court at Konin. Ludwik Żurawski, in the service of Antoni Prusimski of Kolno, Starost of Niszczewice and heir of Trąbczyn, brings a team before the office: a cart with unshod front wheels and iron-shod rear wheels, two oxen, a cow and a chestnut mare. The team belongs to Marcin Gryndel, a peasant of Łomowo, an estate of Chełmski, Treasurer of Wschowa, which belongs to his principal estate of Łukom. Gryndel had driven into the pine wood that belongs to Prusimski's hereditary estate of Trąbczyn and was never in dispute, and was already carting home from it a felled tree fit for building; the Trąbczyn forest keeper stopped him in the wood. After showing them, Żurawski leaves the animals and the cart at the chancery to be given back to Gryndel, who asks for them at once; a receipt for this was entered the same day."),}

HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
