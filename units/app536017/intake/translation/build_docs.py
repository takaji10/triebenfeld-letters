# -*- coding: utf-8 -*-
"""The English of APP 53/6/0/-/17, for the edition's two pages.

    python units/app536017/intake/translation/build_docs.py            # check
    python units/app536017/intake/translation/build_docs.py --write    # doc1.yml

The editor's English of this entry was made from a first reading of the Latin
in which most words of the court's order were unread, and it carried 33 notes
saying so. The Latin has now been read again from the scans
(../corrections.py), and the English below follows that reading. It is
Claude's revision, in the editor's terms wherever the Latin under them stands:
"judicial site inspection", "woodland and pine forest", "barren pastures",
"Hungarian florins of pure gold and of just weight", "peremptory term", "with
no party's right harmed", and the editor's rendering of the Polish words.

What differs in substance from the editor's English (WAS / NOW below):

- the heading: Łukomski is to carry out the inspection (was: the inspections
  are pending);
- the court adds one of its messengers, whom the defendant chooses, to see
  where and on whose ground the wrong was done and whether it was done (was:
  "a mutual term which the cited party shall have chosen");
- the defendant hires the messenger at his own cost (was: "a [mutual
  surveyor]");
- both parties must attend the inspection (was: "both parties having
  appeared");
- at the next court terms the parties have a peremptory term to hear the
  outcome before the court through the messenger.

The editor's 33 notes are not used: each discusses a word that was then
unread. The second reading of leaf 27 verso in the editor's files, and
"[2]", the heading of the sitting, which has no scan, are not pages.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INTAKE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(INTAKE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

PAGES = [
    # leaf 27
    "Łukomski shall carry out the judicial site inspection\n\n"
    "Disputes having arisen between the underwritten parties upon a written citation of the Konin land court, whereby "
    "the Honourable Albertus Thrąmpczyński Otha, acting from his own interest as Plaintiff, has cited the Honourable "
    "Thomas Łukomski for the second time after the penalty of contumacy — for this reason: that he himself, in the "
    "present year, having constructed a pond together with his other neighbours, against whom the Plaintiff has reserved "
    "to himself his right of action intact, in the estate of the village of Łukom — by which pond he has flooded, so far "
    "as concerns the interest of that same Plaintiff, an enormous quantity of woodland and pine forest, of barren "
    "pastures and also of meadowlands, through the excessive retention of water, in the same estates of the villages of "
    "Trąbczyn, Nowa Wieś and Osiny — namely: drowned and killed, through that flooding, the timber of common productive "
    "oak, beech and ash, suitable for building and for bee-trees —\n\n"
    "doing the aforesaid to the grave damage and injury of the Plaintiff, of the value of ten thousand Hungarian florins "
    "of pure gold and of just weight, and as much again in damages; the citation itself, with its copy, setting out the "
    "aforesaid more fully.\n\n"
    "The present land court of Konin, having heard the disputes of the aforesaid parties made before the present court, "
    "at the legal request of the cited party, adhering to the common law, has decreed and by these presents decrees a "
    "judicial site inspection; and none the less it has added, as by these presents it adds, a land court Messenger, "
    "whom the cited party shall choose for itself, namely to see and to inspect in what place and on whose ground the "
    "aforesaid injury was inflicted, and whether it was done or not. Which judicial site inspection the cited party, at "
    "its own expense, having hired the Messenger, from the date of the present decree, within exactly six",
    # leaf 27 verso
    "weeks, the consent of the parties being added thereto, is bound to carry out at the place of the differences, "
    "under the penalties [uncertain: raised], to be won and lost by the cited party in default of the carrying out. At "
    "which inspection both parties are bound to be present. And so, whether the inspection has been carried out as "
    "aforesaid or not, both the aforesaid parties shall have, at the next future land court terms of Konin, to be held "
    "next and immediately at Konin, a peremptory term to hear, upon the aforesaid inspection, the restitution of right "
    "before the court through the Messenger, and to do all else that shall be of law in the present cause — the present "
    "decree of inspection, the keeping of the term, and the record, with no party's right harmed.",
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for i, t in enumerate(PAGES, 1):
        print('--- page', i)
        print(t)
    if '--write' in sys.argv:
        courtbook.write_doc_yml(os.path.join(HERE, 'doc1.yml'), PAGES)


if __name__ == '__main__':
    main()
