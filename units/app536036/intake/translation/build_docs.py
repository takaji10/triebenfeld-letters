# -*- coding: utf-8 -*-
"""The editor's English of APP 53/6/0/-/36, cut to the edition's documents and pages.

    python units/app536036/intake/translation/build_docs.py            # check
    python units/app536036/intake/translation/build_docs.py --write    # doc1.yml, doc2.yml

The English is the editor's own translation. It was made from a first reading
of the Latin that had eighteen marks of doubt in 317 words, and its notes say
so at each. The Latin has since been read against the scan (../corrections.py)
and nearly every doubt is settled, so the English is changed wherever it
rested on a doubtful word. The editor's terms and sentences are kept where the
Latin under them did not change. FIXES gives each passage as it stood and as
it stands, with the reason.

Left out, as the editor's apparatus: the file's heading, its "Document
Outline", its glossary, the heading "Entry 2 ..." (the Latin has its own,
"Similis Contra Eosdem", which is translated), and "[612]", the heading of the
sitting, which has no scan. Of the 26 footnotes two are kept (6 and 22, on
phrases that stand); the others discuss readings that are now settled or
words the scan does not have.
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

KEEP_NOTES = {'6', '22'}
DROP_NOTES = {str(n) for n in range(1, 27)} - KEEP_NOTES

FIXES = [
    ("The Honourable Jerzy Chełmski, plaintiff, cites the Honourables Marcin, Wojciech, Władysław and Andrzej, full blood "
     "brothers of the Otto-Trąmpczyński family, sons of the late Stanisław, and likewise Anna of Słończyc, the same, widow "
     "of the late Stanisław Trąmpczyński, and lady administratrix and conductrix of the goods of the same, abandoned in the "
     "customary manner, of the goods of all their children — all before the present Konin land court — the minors, if any "
     "there be, together with their female guardian assigned to them — being cited, for the reason that they themselves, "
     "not content with the prior injuries, damages and grievances, through the sending in of their own sub-agents against "
     "that same plaintiff, into the woodland of that same plaintiff's own village of Łukom, made notches on trees after "
     "the manner of boundary marks, eighty on this side or beyond, and cut them, and procured others who did in fact cut "
     "them — intending by such an act to annex a great part of the estate of that same plaintiff, his own, and to "
     "appropriate it to their own estate — doing the aforementioned things to the serious detriment of the plaintiff — "
     "reckoning the same [siti] against them on the estate in [total] at one thousand Polish marks, and damages of the "
     "same amount, or [as] the court shall decree; and no less, the office of the Sub-chamberlain being directed, that "
     "they annul the same marks of this court under [the prescribed] penalties.",
     "The Trąmpczyńskis, in default\n\n"
     "The Honourable Jerzy Chełmski, plaintiff: the Honourables Marcin, Wojciech, Władysław and Andrzej, full blood "
     "brothers of the Otto-Trąmpczyński family, sons of the late Stanisław, and likewise Anna of Słończyce, widow of the "
     "same late Stanisław Trąmpczyński, and lady dower-holder and life-tenant of the goods left by his death, being cited "
     "before the present Konin land court in respect of all their goods generally — the minors, if any there be, together "
     "with their guardians [uncertain: assigned to them] — for the reason that they themselves, not content with the prior "
     "injuries, damages and grievances, through the sending in of their own subjects against that same plaintiff, into "
     "the woodland of that same plaintiff's own village of Łukom, made notches on trees after the manner of boundary "
     "marks, eighty on this side or beyond, and cut them, and procured others who did in fact cut them — intending by "
     "such an act to annex a great part of the ground of that same plaintiff, his own, and to appropriate it to their own "
     "ground — doing the aforementioned things to the serious detriment of the plaintiff, which he reckons for himself "
     "against them, the ground itself left untouched, at one thousand Polish marks, and damages of the same amount, or as "
     "the court shall decree; and that none the less, the office of the Sub-chamberlain having been brought out, they "
     "shall annul the same marks, the penalties being paid —",
     'the heading, "Trąmpczynscy Contumaces", is on the page and is now translated (the file had it as "Entry 1 — '
     'Trąmpczyński Concession"). In the sentence: "eiusdem ... consortem relictam bonorumque morte eiusdem derelictorum '
     'dominam reformatoriam et advitalem"; "de bonis ipsorum generaliter omnibus"; "cum tutoribus"; "per immissionem '
     'subditorum"; "quod sibi contra ipsos fundo intacto pensat"; "vel prout judicium decernet ac nihilominus educto '
     'officio succamerali eadem signa luitis paenis annihilent". The main verb comes only at the end of the entry '
     '("condemnavit"), so "cites" is taken out'),
    ("The [plaintiff] citing concerning the aforementioned matters, the fuller [citation] being extant, through the General "
     "Royal Messenger, the Honest Mikołaj Jaworowski of Karmin, under oath, proclaimed them; and their not appearing at "
     "the first term, the penalty of contumacy to be admitted before the same court, the court granted.",
     "the citation concerning the aforementioned matters being fuller — them, lawfully proclaimed through the General "
     "Royal Messenger, the Honest Mikołaj Jaworowski of Karmin, and not appearing at the first term, he has judicially "
     "condemned in the penalty of contumacy, the same court admitting it.",
     '"Citatione de praemissis latiori existente. Per Ministerialem Regni Generalem ... juridice clamatos et non '
     'comparentes in termino primo in paena contumaciae admittente judicio eodem judicialiter condemnavit": a default '
     'judgment, which the plaintiff obtains and the court admits'),
    ("And hereupon, [per[uncertain: o]t~] standing, the Worthy General Royal Messenger Bartłomiej Koelmarek of Łukom, as "
     "[the designated document], acknowledged that he had conveyed the dispatched citation of the aforementioned parties",
     "And here standing in person, the General Royal Messenger, the Worthy Bartłomiej Koelmarek of Łukom, openly "
     "acknowledged that he had laid the citation issued on account of the aforementioned matters, on the Monday last past,",
     '"Hicque personaliter stans ... palam recognovit se citationem ratione praemissorum editam feria secunda proxime '
     'praeterita": the day belongs to this page in the Latin'),
    ("on the Monday before the preceding [feast], and had placed it in the court of the citation of the village of "
     "Trąbczyn, the household of the estate being present.",
     "at the manor of the cited, in the village of Trąbczyn, in the presence of the household of the house.",
     '"in curia citatorum villae Trampczyno praesente familia domus posuisse"'),
    ("[Entry 2 — Similar \\[Action\\] Against the Same]\n\n", "",
     'the editor\'s heading; the Latin entry opens with its own, "Similis Contra Eosdem"'),
    ("A similar [action] against the same [defendants], in the same words. For the reason that they themselves, not "
     "content with prior injuries — adding injury to injury — to the desolation of the woodlands and forests belonging to "
     "the village and estate of Łukom, in those same woodlands and forests recently cut trees of various kinds suitable "
     "for building, especially pine, approximately one hundred, but for firewood three hundred cartloads, approximately "
     "or beyond, and converted them to whatever use they wished — doing the aforementioned things to the serious "
     "detriment of the plaintiff — reckoning the same [siti] against them on the estate in [total] at three hundred "
     "Polish marks. The remainder from the preceding [entry] to the end.",
     "A similar [judgment] against the same [defendants], in these words: for the reason that they themselves, not "
     "content with prior injuries — nay, adding injury to injury — to the desolation of the woodlands and forests "
     "belonging to the village and estate of Łukom, in those same woodlands and forests recently cut trees of various "
     "kinds suitable for building, especially pines, approximately one hundred, but for firewood three hundred cartloads, "
     "on this side or beyond, and converted them to whatever use they wished — doing the aforementioned things to the "
     "serious detriment of the plaintiff, which he reckons for himself against them, the ground itself left untouched, at "
     "three hundred Polish marks. The remainder from the preceding [entry] to the end.",
     '"Citra vel Ultra", as in the first entry; "Quod sibi contra ipsos pensat fundo intacto"'),
]


def build():
    f = glob.glob(os.path.join(glob.escape(B.RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0], DROP_NOTES)
    assert [l for l, _ in leaves] == ['612', '641v', '642'], [l for l, _ in leaves]
    pages = courtbook.fix_english({leaf: paras for leaf, paras in leaves[1:]}, FIXES)
    verso, recto = pages['641v'], pages['642']
    assert recto[0].startswith('at the manor of the cited') and recto[1].startswith('A similar [judgment]'), recto
    return {1: ['\n\n'.join(verso), recto[0]], 2: ['\n\n'.join(recto[1:])]}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    docs = build()
    for n, texts in docs.items():
        for i, t in enumerate(texts, 1):
            print('--- document %d, page %d' % (n, i))
            print(t)
    if '--write' in sys.argv:
        for n, texts in docs.items():
            courtbook.write_doc_yml(os.path.join(HERE, 'doc%d.yml' % n), texts)


if __name__ == '__main__':
    main()
