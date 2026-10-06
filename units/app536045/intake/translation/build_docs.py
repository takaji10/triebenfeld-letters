# -*- coding: utf-8 -*-
"""The editor's English of APP 53/6/0/-/45, cut to the edition's pages.

    python units/app536045/intake/translation/build_docs.py            # check
    python units/app536045/intake/translation/build_docs.py --write    # doc1.yml

The English is the editor's own translation and is not made again. It is cut
at the editor's leaf marks; "[638]", the heading of the sitting, has no scan
and is not a page (see ../build_pages.py). The file's heading, its glossary
and its empty "Translator's Notes" section are the editor's apparatus and are
left out.

FIXES are the places where the Latin was corrected against the scan
(../corrections.py) and the English had rested on the earlier reading. Each
says which words changed and why. Five of the editor's seven footnotes are
left out (DROP_NOTES): they comment on readings that the scan does not have.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INTAKE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(INTAKE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, INTAKE)
import courtbook  # noqa: E402
import build_pages as B  # noqa: E402

DROP_NOTES = {
    '1': 'on the form "actoralibus"; the scan has "Actoratibus", the form the note expected',
    '2': 'on "testibus juratus" as a slip; the scan has "juratis"',
    '3': 'on two words left unread; they are read now (Ministerialem ad pronuntiandam)',
    '4': 'the same note again',
    '5': 'on an irregular construction and on "quando quiae"; the scan has "quandoquidem", and the sentence is plain once '
         'Prusimska is taken as the one who sent the potash-burners',
}

FIXES = [
    ('having heard their disputes, combined from their numerous plaintiff claims and charges, considers',
     'having heard their disputes and joined the plaintiff claims and charges of the several of them, considers',
     'the Latin is now "combinatis earumque plurium actoratibus et reatibus"'),
    ('by sworn witnesses regarding the contents of past matters',
     'by sworn witnesses regarding the contents of the protestations',
     'the Latin is now "super contenta protestationum"'),
    ('and of sessions, during their respective court proceedings, shall produce and expedite it, and shall add to these '
     'present [——] to [——] for the incorporation of the said third roll of the sworn inquiry — as the said sworn inquiry '
     'has been resolved and granted between the parties — and therefore orders the same parties to produce witnesses. '
     'They produced, presented, and expedited the sworn inquiry on their respective behalf, and the same court proceeded '
     'to the fourth session. Upon these being read out, and the following being established for the record: that it is '
     'not established at what time, in the year 1761, the potash-burners made arrangements concerning the Right '
     'Honourable Prusimska\'s potash prepared at that time; and that the Right Honourable Chełmski, departing for Poznań, '
     'overtook the same departing for Gdańsk near the town of Pyzdry;',
     'and of the terms, while its sittings last, shall produce and expedite it; and by these presents it assigns them '
     'the Court Summoner to pronounce the formula of the oath for the swearing-in of their witnesses — which oath, since '
     'the parties have mutually conceded it to one another, it therefore orders the same parties to bring in their '
     'witnesses. They brought them in and produced them, and expedited the sworn inquiries each on its own behalf; to the '
     'reading of which this same court proceeded. These having been read — whereas it is shown that the Right Honourable '
     'Prusimska, in the year 1761, dispatched the potash-burners with potash, prepared at what time is not established; '
     'and that the Right Honourable Chełmski, departing for Poznań, came upon them, as they were departing for Gdańsk, '
     'near the town of Pyzdry;',
     'the Latin is now "addit praesentibus eisdem Ministerialem ad pronuntiandam super incorporationem eorum testium '
     'juramenti rotham quod juramentum quoniam per partes sibi mutuo est indultum ... inquisitiones ... expediverunt ad '
     'quarum lectionem hoc idem judicium accessit". "Rotha juramenti" is the formula of an oath, not a roll. In the '
     'sentence that follows, "Magnificam Prusimska ... cineatores disposuisse", Prusimska is the one who sent the '
     'potash-burners off'),
    ('although the Right Honourable customs officer opposed it', 'although the notary of the customs post opposed it',
     'the Latin is now "opponente se Notario Thelonei"'),
    ('conveyed it to Gdańsk. However, since between these parties a case regarding the boundaries between the estates of '
     'Trąbczyn and Łukom, along with acts lodged therein, is being heard undecided before the Crown Tribunal, and on which '
     'estate the potash was prepared is to be determined from the forthcoming demarcation of the estates, as is to be '
     'established in the present proceeding — for that reason',
     'conveyed it to Gdańsk — since, however, between these parties a case regarding the boundaries between the estates '
     'of Trąbczyn and Łukom, and other matters, is being heard undecided before the Crown Tribunal, and on whose ground '
     'the potash was prepared will be shown only from the demarcation of the estates that is to follow — for that reason',
     'the Latin is now "ac alia in Judicio Tribunalis Regni ventilatur indecisa"; "modo" is "only then"'),
    ('orders that the sworn inquiries for the parties be extracted from the land chancery in the enclosed sealed roll',
     'orders that the sworn inquiries be handed out to the parties from the land chancery in a closed roll',
     'the Latin is now "in occluso rothulo extradendas"'),
]


def build():
    f = glob.glob(os.path.join(glob.escape(B.RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0], DROP_NOTES)
    assert [l for l, _ in leaves] == ['638', '653v', '654'], [l for l, _ in leaves]
    pages = {B.PAGE_OF[leaf]: paras for leaf, paras in leaves[1:]}
    return courtbook.fix_english(pages, FIXES)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    pages = build()
    for pid in B.DOCS[0][1]:
        print('---', pid)
        print('\n\n'.join(pages[pid]))
    if '--write' in sys.argv:
        courtbook.write_doc_yml(os.path.join(HERE, 'doc1.yml'), ['\n\n'.join(pages[pid]) for pid in B.DOCS[0][1]])


if __name__ == '__main__':
    main()
