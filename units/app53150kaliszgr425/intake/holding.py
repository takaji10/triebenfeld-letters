# -*- coding: utf-8 -*-
"""APP 53/15/0/-/Kalisz Gr.425: from the editor's scans and texts to the edition.

    python units/app53150kaliszgr425/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                      [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The images. Three photographs of the book, numbered in a series (not by
leaf); the leaf numbers are read off the pages:

    502.jpg   a blank verso | leaf 497 recto
    503.jpg   leaf 497 verso | leaf 498 recto
    504.jpg   leaf 498 verso | leaf 499 recto     (not used)

Leaf 497 is the original of the adjournment, a smaller sheet sewn into the
book, signed and sealed by five commissioners; leaf 498 has the office's
record of its being brought in. Three pages are pages of the edition:
0497_a2, 0498_a1, 0498_a2 (leaf N recto is <N>_a2, leaf N verso is
<N+1>_a1). One document.

Not transcribed, and so not used: on 504.jpg, the docket on the back of the
sewn sheet ("Actus Limitationis Causae inter M. Chełmski ... et M. Prusimski
...") and, at the foot of leaf 499, a register note that the adjournment was
brought in.

The check (2026-10-07). Read against the scans: the closing line and the
five signatures on leaf 497 verso, and the whole record on leaf 498. The
body of the adjournment on leaf 497 and the head of leaf 497 verso (about
170 words of clear Polish) was not compared. ROWS has what was corrected.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53150kaliszgr425'
REF = 'APP 53/15/0/-/Kalisz Gr.425'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1776 (53.15.0.-.Kalisz Gr.425)"

# (file, x of the fold, left page, right page). First proposals, set by eye
# on small views: the automatic finder was 40 to 70 pixels to the right on
# these photographs. The editor's saved folds (folds.json beside this file)
# are used instead where they exist.
SCANS = [
    ('502.jpg', 2065, '0497_a1', '0497_a2'),
    ('503.jpg', 2030, '0498_a1', '0498_a2'),
]
SKIP = ('0497_a1',)
LEAF = {'0497_a1': 'a blank verso', '0497_a2': '497 recto', '0498_a1': '497 verso', '0498_a2': '498 recto'}
PAGE_OF = {'497': '0497_a2', '497v': '0498_a1', '498': '0498_a2'}
DOCS = [(1, ['0497_a2', '0498_a1', '0498_a2'])]
FOLD_NOTE = 'A third photograph (leaves 498 verso and 499) has nothing that is transcribed and is not shown.'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert not head and [l for l, _ in leaves] == ['497', '497v', '498'], (head, [l for l, _ in leaves])
    return {(1, PAGE_OF[leaf]): paras for leaf, paras in leaves}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0498_a1', 'Działo się w Rezydencyach Na[st?][??] Dnia', 'Działo się w Rezydencyach Nasz[ych] Dnia',
     'the scan has "Nasz" running into the fold: Naszych, at our residences. It is not a place name'),
    ('0498_a1', 'Stefan Leszczy[ńsk]i Zielonacki', 'Stefan Leszczyc Zielonacki',
     'the signature has "Leszczyc", the name of his arms, as "Antonius Leszczyc Mierzewski" is written out in Kalisz Gr.424'),
    ('0498_a1', 'Maci Leszczy[ńsk]i Mierzewski', 'Maci Leszczyc Mierzewski', 'the signature has "Leszczyc"'),
    ('0498_a2', 'Generosus Antonius Czyewski nomine', 'Generosus Antonius Czyżewski nomine', 'the scan has "Czyzewski"'),
    ('0498_a2', 'ac alios in Comparationem intrantes', 'ac alios in Comparitionem intrantes', 'the scan has "Comparitionem", an appearance'),
    ('0498_a2', 'sigillisque eorum [praescriptis?] Tenoris Talis', 'sigillisque eorum gentilitiis communitam Tenoris Talis',
     'the scan has, written above the line, "sigillisque eorum gentilitiis communitam": secured with the seals of their arms'),
]

FIXES = [
    ('Done at the Residences [location illegible], on the Twenty-Eighth Day', 'Done at our Residences, on the Twenty-Eighth Day',
     '"w Rezydencyach Naszych"'),
    ('Stefan Leszczyński Zielonacki, Deputy Judge', 'Stefan Leszczyc Zielonacki, Deputy Judge', 'the signature'),
    ('Maciej Leszczyński Mierzewski, Commissioner', 'Maciej Leszczyc Mierzewski, Commissioner', 'the signature'),
    ('the Honourable Antoni Czyewski, in the name', 'the Honourable Antoni Czyżewski, in the name', 'the name on the scan'),
    ('and with their [aforementioned] seals, of the following tenor', 'and secured with the seals of their arms, of the following tenor',
     '"sigillisque eorum gentilitiis communitam"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [l for l, _ in leaves] == ['497', '497v', '498'], [l for l, _ in leaves]
    pages = courtbook.fix_english({l: p for l, p in leaves}, FIXES)
    return {1: ['\n\n'.join(pages[l]) for l in ('497', '497v', '498')]}


S = {
 1: ('Vertagung in der Grenzsache zwischen Prusimski, Starost von Niszczewice und Erbherrn von Trąbczyn, und Stanisław Ścibor Chełmski, Erbherrn von Łukomia, ausgestellt am 28. September 1776 und am 30. September in die Akten des Burggerichts Kalisz eingetragen; das Original ist in das Buch eingenäht. Fünf von den Ständen der Republik bestellte Kommissare erklären, sie könnten die Sache im jetzt fälligen Termin nicht durch ein Endurteil abschließen, weil einige von ihnen beim Reichstag in Warschau, andere beim Krontribunal in Piotrków zu tun haben. Der Termin geht auf die Vertagung im Dekret vom 13. September des Vorjahres zurück. Sie vertagen die Zusammenkunft auf den ersten Montag nach Dreikönig 1777 und erhalten den Parteien den letzten Termin zum Erscheinen vor dem Kommissionsgericht auf dem Grund von Łukomia. Es unterzeichnen und siegeln Stefan Leszczyc Zielonacki, Unterrichter des Kalischer Landgerichts, Maciej Leszczyc Mierzewski, Tomasz Radoński, Grenzvermesser von Kalisz, Stanisław Jabłkowski und Stanisław Otto-Trąmpczyński.',
     'An adjournment in the boundary cause between Prusimski, Starost of Niszczewice and heir of Trąbczyn, and Stanisław Ścibor Chełmski, heir of Łukomia, made on 28 September 1776 and entered in the records of the castle court at Kalisz on 30 September; the original is sewn into the book. Five commissioners appointed by the Estates of the Commonwealth declare that they cannot end the cause by a final judgment at the term now due, because some of them have business at the parliament in Warsaw and others at the Crown Tribunal in Piotrków. The term goes back to the adjournment in the decree of 13 September of the year before. They put the meeting off to the first Monday after Epiphany 1777 and keep for the parties the final term for appearing before the commission\'s court on the ground of Łukomia. Stefan Leszczyc Zielonacki, deputy judge of the Kalisz land court, Maciej Leszczyc Mierzewski, Tomasz Radoński, boundary surveyor of Kalisz, Stanisław Jabłkowski and Stanisław Otto-Trąmpczyński sign and seal.'),
}
HOW = ('written in the working session from the Polish and Latin as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
