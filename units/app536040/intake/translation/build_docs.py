# -*- coding: utf-8 -*-
"""The editor's English of APP 53/6/0/-/40, cut to the edition's pages.

    python units/app536040/intake/translation/build_docs.py            # check
    python units/app536040/intake/translation/build_docs.py --write    # doc1.yml

The English is the editor's own translation and is not made again. It is cut
at the editor's leaf marks. The file's heading, its "Document Outline", its
notes and its glossary are the editor's apparatus and are left out; so is the
heading "Decree of Location: ..." that the editor put before leaf 372, since
the Latin has its own heading there, which is translated. The marks "[T.N.n]"
in the text pointed to the notes and go with them.

FIXES are the places where the Latin was corrected against the scans
(../corrections.py) and the English had rested on the earlier reading. Each
says why.
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

FIXES = [
    ("\n\n[Decree of Location: Between the Honourable Chełmski and the Honourable Prusimski]", "",
     "the editor's heading; the Latin has its own on leaf 372"),
    ("Between the Honourable Chełmski and the Honourable Prusimski — Decree of Location.",
     "Between the Honourables Chełmski and the Honourable Prusimski — Decree of Location.",
     'the heading has "GG. Chełmskie", more than one'),
    ("on the Monday nearest after the [feast of the] Most Holy and Undivided Trinity",
     "on the Monday nearest after the feast of the Most Holy and Undivided Trinity",
     'the word is read: "post Festum"'),
    ("the instigator of the present court, its present bearers, namely the Honourables Franciszek and Józef Ścibor Chełmscy, "
     "hereditary owners and possessors of the goods of the villages of Łukom, Łomowo, and others belonging thereto, "
     "plaintiffs — have cited before the present Kalisz land court and before the three decreed particular land terms of "
     "Konin —",
     "the instigator of the present court and his informants, the Honourables Franciszek and Józef Ścibor Chełmscy, "
     "heirs and possessors of the goods of the villages of Łukom, Łomowo, and others belonging thereto, "
     "plaintiffs — have cited before the present Kalisz land court and the particular land terms of the district of "
     "Konin —",
     '"instigator judicii praesentis ejusque delatores"; "haeredes et possessores"; "terminosque terrestres particulares '
     'districtus Coninensis": there are no "three decreed" terms'),
    ("the sons together with the retainers and subjects of the parent, under a decree ordering them to adhere to the protest",
     "the sons with their parents, the retainers and subjects with their lords, to adhere to the protest",
     '"filiis ... cum parentibus famulis et subditis cum dominis ipsorum ad inhaerendum protestationi": the set phrase; '
     'there is no decree in it'),
    ("not content with prior injurious acts, injuries, and grievances, for the sake of preserving",
     "not content with prior damages, acts of violence, injuries, and grievances — which, for the sake of preserving",
     '"non contentus anterioribus damnis violentiis iniuriis et gravaminibus"'),
    ("— in virtue of a declaration of neighbourly friendship not yet submitted to the public records of the Kingdom up to "
     "this time — expressing [it] most particularly at that time, in a certain third session, ordered shingles, otherwise "
     "called Szkudeł, one hundred and sixty of them, prepared",
     "the friendship that belongs to living as neighbours, have up to this time not yet been submitted to the public "
     "records of the Kingdom and set out — most particularly, at a certain time to be stated at the hearing of the cause, "
     "ordered shingles, otherwise called Szkudeł, a hundred threescore of them, prepared",
     '"propter conservandam in virtute vicinae commansionis amicitiam ad hoc usque tempus nondum ad acta publica regni '
     'oblata expressis": the earlier wrongs had been kept out of the public records for friendship\'s sake. "In termino '
     'termini exprimendo" is the phrase the page before uses for names to be given at the hearing. "Centum sexagenas" is a '
     'hundred sixties, six thousand shingles'),
    ("on the plaintiff's own estate during the same violent armed and group invasion,",
     "on the plaintiff's own estate, during his violent invasion of it in arms and in a band,",
     '"circa violentam ejus armatim et turmatim super invasionem"'),
    ("to seize the hay gathered into carts from that same estate, to see to it that [it be conveyed] to the goods of "
     "Trąbczyn, and thereby to carry out the destruction of the inventory of the cause and other acts of violence to be "
     "proven by full inquisition",
     "to seize the hay gathered into carts from that same estate, in no small number of cartloads, to see to it that it "
     "be [uncertain: conveyed] to the goods of Trąbczyn, and thereby to cause the loss of livestock, and to carry out "
     "other acts of violence to be proven by full inquisition",
     '"in non postrema quantitate curruum"; "devehi[?] curare"; "decessum inventarii causare": inventarium is the '
     'livestock of an estate, lost for want of the hay'),
    ("the present Kalisz land court, in the particular land terms decreed at Konin, [examining]",
     "the present Kalisz land court, in the particular land terms of the district of Konin, [examining]",
     '"districtus Coninensis"'),
    ("and the cited party of the Honourables Prusimski and their wives",
     "and the cited party of the Honourables Prusimski, husband and wife,",
     '"Generosorum Prusimskich conjugum", with no "et"'),
    ("and contesting the matter before the court — having heard the facts of the court in the foregoing — finds that a "
     "decision must be reached, and that the term sought by the plaintiff party for the appropriation of the estate and "
     "for the violence and damages caused is properly instituted before the present court, since the cause of the estate "
     "is being ventilated before the same court; and finds that a commissarial descent",
     "and contesting judicially — having heard what was judicially done in the foregoing — deciding the term of the "
     "plaintiff party, instituted before the present court on account of the appropriation of the estate and of the "
     "violence and damages caused: since the cause of the estate is being ventilated before its own court, it finds "
     "that a commissarial descent",
     '"judicialiter controvertentium in praemissis judicialiter factis exauditis decidendo terminum partis actoreae ... '
     'quoniam causa fundi suo coram judicio ventilatur necessariam esse condescensionem ... adinvenit": one finding, that '
     'the descent is needed; "suo coram judicio" is its own, proper court'),
    ("to and at the estate whence a certain controversy between the inheritances of the goods of Łukom and Trąmpczyn "
     "[arises]",
     "to and at the estate from which the controversy between the inheritances of the goods of Łukom and Trąmpczyn has "
     "arisen",
     '"ex quo orta controversia"'),
    ("and the said Honourable Commissioners and arbitrators shall inquire",
     "and the said Honourable Commissioner and arbitrators shall inquire", '"qui Generosus Commissarius ac amici": one commissioner'),
    ("as set out in the protest of both parties", "as set out in the protests of both parties", '"protestationum"'),
    ("the present cause together with its [effect] and the parties themselves",
     "the present cause together with its whole effect and the parties themselves", '"cum toto suo effectu"'),
]


def build():
    f = glob.glob(os.path.join(glob.escape(B.RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [l for l, _ in leaves] == ['368', '372', '372v', '373', '373v'], [l for l, _ in leaves]
    pages = courtbook.fix_english({B.PAGE_OF[leaf]: paras for leaf, paras in leaves}, FIXES)
    assert all('T.N.' not in ' '.join(p) for p in pages.values())
    return pages


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
