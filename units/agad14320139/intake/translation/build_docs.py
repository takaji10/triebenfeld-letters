# -*- coding: utf-8 -*-
"""The in-session English of 1/432/0/1/139, as doc<N>.yml (the shape of the
submit_translation tool), made by Claude in a Claude Code session, no paid run.

First written 2026-11-11 with every "[...]" of the German as "[text lost]" and
every broken word kept as written, which made the English hard to read
("Herrn General-Superin[text lost]"). Rewritten 2026-11-13 at the editor's
word ("easier to read while still following the transcription ... fill in
minor pieces ... keep it light"):

  * A word broken at the burnt edge whose sense the legible part fixes is
    translated whole, with no mark ("Superin[...]" is "Superintendent";
    "vorzustel[...]" is "submit"). Most of these are the A and B rows of
    supplied.yml; the transcription keeps its [...].
  * Whole words taken from the other report, the form or the grammar are in
    square brackets with no question mark ("[To His Reverence]",
    "[collected]") - the convention of G[oldbeck] (EDITORIAL_RULES).
  * What adds a fact stays "[text lost]": a figure, a name, a place, a date,
    a negation, whether a thing is present or absent, good or bad
    (docs/CONSISTORY_1882_PLAN.md, section 3). A word-level doubt the editor
    has not settled stays marked ("[uncertain: ...]", "[?]"); a letter-level
    doubt that does not change the word's sense is not carried.

So the English has fewer marks than the German on every page; check_translations
reports that as marker-check, and the rows are cleared in
reference/translation_rulings.json with the reason.

    python units/agad14320139/intake/translation/build_docs.py
"""
import os, re, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DE = re.compile(r'\[[^\]]*\?\]|\[\.\.\.\]')
EN = re.compile(r'\[illegible\]|\[uncertain(?::[^\]]*)?\]|\[text lost\]|\[[^\]]*\?\]')

P_0318 = """[To His] Reverence the General Superintendent
of the Warsaw Evangelical-Augsburg
Consistorial District.

The Pastor-Administrator [of the]
Evangelical-Augsburg [congregation of]
Zagórow.

In consequence of [Your Reverence's] order
of the 30th of October [text lost],
No. 267, I have the honour to submit the following annual report
concerning the parish of Zagórow.

I. Church affairs.

a.) External church affairs.– The congregation of Zagórow possesses a brick-built church; for its complete furnishing it still lacks a baptismal font, an organ and bells.– Both the parsonage and the cantor's house are very small and low, and in very poor condition.– The schoolroom is adequately spacious for the number of children.– Besides the religious school in Zagórow there are 7 more schools combined with prayer houses in the congregation, among them only one elementary school, at Michalinowo.– The number of children in the 8 schools of the congregation may come to about 240.– There is no separate dwelling for the sexton[?].– As for the cemeteries, of which there are 8 in the congregation, they are [text lost] in good condition and provided with crosses.–

b.) Inner church affairs.– Church spirit and church attendance satisfactory.– Baptisms are mostly performed by the pastor.– Open despisers of the Lord's Supper: none known.– The number of communicants: men 726, women 871, total 1597, [text lost]"""

P_0322a = """[text lost] 45 more.– [uncertain: A demand] for still more schools [text lost] is not present, since almost every larger colony has a [text lost].– For the mission to the heathen, 10 roubles 71 kopecks were [collected] in the course of the year at the mission services, which the Pastor-Administrator sent on to Superintendent Pastor Manitius at Warsaw.– Morality and domestic life are in general very satisfactory.– Baptists, Irvingians or other sects there are none.– Particular vices[?] in the congregation are [text lost]t present. Conversions to other confessions [text lost] take place.–

Remarkable events.– None have taken place.–

Number of confirmed.– Boys 36, girls 31, together 67.–

Candidates living in the congregation.– None.–

Collections.– For the benefit of the congregation itself nothing was collected, but for other purposes the following: 1.) For the support of grammar-school pupils who intend to study theology, [text lost] 4 roubles 61 kopecks, which the Pastor-Administrator sent to his High Consistory at Warsaw.– 2.) For the widows' and orphans' fund 2 roubles 36 kopecks were collected, and the same sent [text lost] to Superintendent von Boerner.–

E. Erdmann
Pastor"""

P_0322b = """[To His] Reverence the General Superintendent
of the Warsaw Evangelical-Augsburg
Consistorial District.

The Pastor-Administrator [of the]
Evangelical-Augsburg [congregation of]
Lissewo-Pyzdry.

In consequence of [Your Reverence's] order
of the 30th of October [text lost],
No. 267, I have the honour to submit the following annual report
concerning the filial Lissewo-Pyzdry.

I. Church affairs.

a.) External church affairs.– The filial possesses neither a church [text lost] sexton's house.– Divine service in Pyzdry is held in rented premises.– In the filial there are five religious schools combined with prayer houses, all of them in good condition.– The number of children in the five schools of the filial comes to about 120.– There are five cemeteries in the filial, all fenced and provided with crosses.–

b.) Inner church affairs.– Church spirit and church attendance satisfactory.– Baptisms are performed by the cantors concerned in the prayer houses; the pastor, when he is present in the prayer houses, confirms the baptisms performed by the cantors, and holds the churching[?] with the women [text lost].– Open despisers of the Lord's Supper: none known.– The number of communicants: men 326, women 408, total 734, [text lost] compared with the year 1881, 131 more.– The inhabitants of Pyzdry would gladly set up an Evangelical school among themselves, [but] are too poor for it, since the little town counts only 9 families[?], and [text lost]"""

P_0345a = """[text lost] lay people can be brought in for it, since the [text lost] colonies have their own teachers and prayer houses.–

For the mission to the heathen, 3 roubles 40 kopecks were collected in the course of the year at the mission services, which the Pastor-Administrator sent on to Superintendent Pastor Manitius at Warsaw.– Morality and domestic life are in general satisfactory.– Particular vices in the congregation not present.– Baptists, Irvingians etc. there are none.– Conversions to other confessions do not take place.–

Remarkable events.– None have taken place.–

Number of confirmed.– Boys 13, girls 10, together 23.–

Candidates living in the congregation.– None.–

Collections.– For the benefit of the congregation itself nothing was collected, but for other purposes the following: 1.) For the support of grammar-school pupils who intend to study theology, 1 rouble 76 kopecks, which the Pastor-Administrator sent to his High Evangelical-Augsburg Consistory at Warsaw.– 2.) For the widows' and orphans' fund [text lost] roubles 36 kopecks were collected, and the same sent to Superintendent von Boerner at Plock.–

E. Erdmann
Pastor"""

DOCS = {1: (P_0318, P_0322a), 2: (P_0322b, P_0345a)}
SOURCES = {1: ('0318_a', '0322_a'), 2: ('0322_b', '0345_a')}

if __name__ == '__main__':
    base = os.path.join(HERE, '..', '..', 'transcriptions')
    bad = False
    for doc, pages in DOCS.items():
        out = {'pages': []}
        for i, (en, src) in enumerate(zip(pages, SOURCES[doc]), 1):
            de_n = len(DE.findall(open(os.path.join(base, src + '.txt'),
                                       encoding='utf-8').read()))
            en_n = len(EN.findall(en))
            print(f'doc {doc} page {i} ({src}): German {de_n} marks, English {en_n}')
            bad |= en_n > de_n
            out['pages'].append({'page': i, 'confidence': 'medium',
                                 'marker_count': en_n, 'en': en + '\n'})
        with open(os.path.join(HERE, f'doc{doc}.yml'), 'w', encoding='utf-8',
                  newline='\n') as f:
            yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=1000)
    if bad:
        print('MORE MARKS IN THE ENGLISH THAN THE GERMAN - check')
