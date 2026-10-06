# -*- coding: utf-8 -*-
"""APP 53/15/0/-/Kalisz Gr.424: from the editor's scan and texts to the edition.

    python units/app53150kaliszgr424/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                      [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The image. One photograph, 355.jpg (numbered in a series, not by leaf): leaf
322 verso on the left, with the date line of the sitting halfway down, and
leaf 323 recto on the right, with the entry in the middle of the page. Both
halves are pages of the edition: 0323_a1 and 0323_a2. The many other entries
on them are not transcribed. One document.

The check (2026-10-07). The whole entry and its date line were read against
the scan, at the size of a reduced view of the opening: enough for the words,
not for every ending. ROWS has what was corrected. The signature under the
entry, "A. L. Mierzewski mppa", is added (SIGNATURE).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53150kaliszgr424'
REF = 'APP 53/15/0/-/Kalisz Gr.424'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1776 (53.15.0.-.Kalisz Gr.424)"

# (file, x of the fold, left page, right page). A first proposal, set by eye;
# the editor's saved fold (folds.json beside this file) is used instead where
# it exists.
SCANS = [('355.jpg', 2125, '0323_a1', '0323_a2')]
SKIP = ()
LEAF = {'0323_a1': '322 verso', '0323_a2': '323 recto'}
DOCS = [(1, ['0323_a1', '0323_a2'])]
FOLD_NOTE = 'Both pages carry many other entries; they are kept whole.'
SIGNATURE = 'A. L. Mierzewski mppa'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head and [l for l, _ in leaves] == ['322v', '323'], (head, [l for l, _ in leaves])
    return {(1, '0323_a1'): leaves[0][1], (1, '0323_a2'): leaves[1][1] + [SIGNATURE]}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0323_a2', 'ab Officio praesen~ [ul/al]rum Decretum', 'ab Officio praesen~ utrum Decretum',
     'the scan has "utrum": he asks whether the decree has been brought in ("... sit porrectum vel ne")'),
    ('0323_a2', 'inter eadem Bona prolat[i?] ad Acta', 'inter eadem Bona prolatum ad Acta', 'the scan has "prolatum"'),
    ('0323_a2', 'Revisionem Prothocollorum Relationem ubi Oblata suscipi', 'Revisionem Prothocollorum Relationum ubi Oblatae suscipi',
     'the scan has "Relationum ... Oblatae": the books of reports, where papers brought in are received'),
    ('0323_a2', 'inter suprascripta Bona Pocillatores Magnificus Commissarios', 'inter suprascripta Bona per Illustres Magnificos Commissarios',
     'the scan has "p Illres Mgcos Commissarios" with marks of abbreviation, the words used of them five lines above. No cup-bearers'),
]

FIXES = [
    ('requisitioned from the present Office a certain Commissorial Boundary Decree concerning the estates',
     'asked of the present Office whether the Commissorial Boundary Decree between the estates', '"requisivit ... utrum"'),
    ('and issued between those same estates — whether it had been submitted to the present Records by oblata or not.',
     'and issued between those same estates, had been submitted to the present Records by oblata or not.', 'the same sentence'),
    ('issued by the Right Honourable Cup-bearer Commissioners designated', 'issued by the Illustrious Right Honourable Commissioners designated',
     '"per Illustres Magnificos Commissarios"'),
    ('and brought to the fund of those estates', 'and brought onto the ground of those estates', '"in Fundum Eorundem Bonorum conductos"'),
]
SIGN_EN = 'A. L. Mierzewski, by his own hand'


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [l for l, _ in leaves] == ['322v', '323'], [l for l, _ in leaves]
    pages = courtbook.fix_english({l: p for l, p in leaves}, FIXES)
    return {1: ['\n\n'.join(pages['322v']), '\n\n'.join(pages['323']) + '\n\n' + SIGN_EN]}


S = {
 1: ('Bescheinigung des Burgamts Kalisz vom 23. November 1776. Antoni Leszczyc Mierzewski fragt das Amt, ob das Grenzdekret zwischen den Gütern der Dörfer Łukom, Trąbczyn und anderen, das die von den Ständen der Republik bestellten Kommissare aufseiten von Antoni Prusimski von Kolno, Starost von Niszczewice und Erbherrn von Trąbczyn, erlassen haben, zur Eintragung vorgelegt worden sei. Das Amt sieht seine Berichtsbücher, in die solche Vorlagen aufgenommen werden, vom 17. Oktober 1776 bis zum heutigen Tag durch und antwortet, in seinen Akten finde sich kein solches Dekret. Es bescheinigt das; Mierzewski unterschreibt.',
     'A certificate of the castle office at Kalisz of 23 November 1776. Antoni Leszczyc Mierzewski asks the office whether the boundary decree between the estates of the villages of Łukom, Trąbczyn and others, given by the commissioners appointed by the Estates of the Commonwealth on the part of Antoni Prusimski of Kolno, Starost of Niszczewice and heir of Trąbczyn, has been brought in for entry. The office goes through its books of reports, in which such papers are received, from 17 October 1776 to the present day, and answers that no such decree is found in its records. It certifies this; Mierzewski signs.'),
}
HOW = ('written in the working session from the Latin as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
