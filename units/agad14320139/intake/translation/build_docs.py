# -*- coding: utf-8 -*-
"""The in-session English of 1/432/0/1/139, as doc<N>.yml (the shape of the
submit_translation tool), made by Claude in a Claude Code session
(2026-11-11), no paid run. Every "[...]" of the German is "[text lost]", every
"[word?]" "[uncertain: word]", and a letter-level "[?]" stays as it is; a
broken word is kept as written with the mark after it. Nothing lost is
completed: the reconstruction layer (supplied.yml) is never used here
(docs/CONSISTORY_1882_PLAN.md).

    python units/agad14320139/intake/translation/build_docs.py
"""
import os, re, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DE = re.compile(r'\[[^\]]*\?\]|\[\.\.\.\]')
EN = re.compile(r'\[illegible\]|\[uncertain(?::[^\]]*)?\]|\[text lost\]|\[[^\]]*\?\]')

P_0318 = """[text lost]ner
[text lost] Herrn General-Superin[text lost]
of the Warsaw Evangelical-Augsburg[text lost]
Consistorial District.

Pastor-Administrat[text lost]
gelical-Augsburg [text lost]
Zagórow.

In consequence of the order [uncertain: Ho][text lost]
würden of the 30th of October [text lost]
No. 267, I have the honour [uncertain: Ho][text lost]
den the parish of Zagórow be[text lost]
fenden annual report vorzustel[text lost]

I. Church affairs.

a.) External church affairs.– The congregation of Zagórow possesses a brick-built church; for the complete furnishing of the same [uncertain: en] [text lost] len still baptismal font, organ and bells.– Both the Pastora[text lost] and the cantor's house are very small and low and in[?] [text lost] very poor condition.– The school room, in proportion to the [text lost] number of children, is correspondingly spacious.– Besides the Religions-Sch[text lost]le in Zagórow there are 7 further schools combined with Beth[text lost] in the congregation, of which only one is an elementary school at Michalinowo.– The number of the children in the 8 schools of the [text lost] congregation may amount to about 240.– For the sexton[?] there is no special dwelling.– The condition of the d[?][text lost] cemeteries, of which there are 8 in the congregation, is [text lost] good and they are provided with crosses[?].–

b.) Inner church affairs.– Churchliness and church attendance satisfactory.– The baptisms are[?] mostly performed by the pastor voll[text lost] Open despisers of the Lord's Supper [uncertain: unbewußt].– The number of the d[?][text lost] municants: male 72[6?] female 871, total 1597 dar[?] [text lost]"""

P_0322a = """[text lost]r more 45.– for [uncertain: Verlangen] still more schools [text lost] not[?] present, since almost every larger colony has a [text lost]lich has.– For the heathen mission there were in the course of the [text lost] the mission services 10 roubles 71 kopecks ge[text lost] worden, which the Pastor-Administrator to the [text lost] Superintendent Pastor Manitius at Warsaw über[text lost] hat.– Morality as well as the domestic living together are [text lost]A[?]llgemeinen very satisfactory.– Baptists, Irvingians or [text lost]dere sects there are none.– Special vices[?] in the congregation [text lost]t present. Conversions to other confessions take place [text lost] statt.–

Remarkable events.– Have not taken place.–

Number of the confirmed.– Boys 36 girls 31, together 67.–

Candidates living in the congregation.– None present.–

Collections.– For the benefit of the congregation's own were not [text lost]mmelt[?], but for other purposes the following: 1.) For the support [text lost]g of grammar-school pupils who are inclined to study theology [text lost] –[?] 4 roubles 61 kopecks, which the Pastor-Administra[text lost]tor sent to his High Consistory at Warsaw.– 2.) For [text lost] widows' and orphans' fund 2 roubles 36 kopecks were collected [text lost]elt and the same sent to the Superintendent von Boerner [text lost]er[?]gesandt.–

E. Erdmann
Pastor"""

P_0322b = """[text lost]ner
Hochwürden dem Herrn General-Superinten[text lost]
of the Warsaw Evangelical-Augsburgisch[text lost]
Consistorial District.

Pastor-Administrator [text lost]
gelical-Augsburg [text lost]
Lissewo-Pyzdry.

In consequence of the order [text lost]
würden of the 30th of October [text lost]
No. 267, I have the honour folge[text lost]
das Filial Lissewo-Pyzdry [text lost]
fenden annual report vorzu[text lost]

I. Church affairs.

a.) External church affairs.– The filial possesses neither a church nor a [text lost] sexton's house.– Divine service in Pyzdry is held in a rented [text lost]ten premises.– In the filial there are five [uncertain: Religi][text lost] schools combined with prayer houses, all in good condi[text lost] sind.– The number of the children in the five schools of the filial [text lost] amounts to about 120.– Cemeteries there are in the filial [text lost] five, all fenced and provided with crosses.–

b.) Inner church affairs.– Churchliness and church attendance satis[text lost] digend.– The baptisms are performed by the cantors concerned [text lost] in the prayer houses, the pastor confirms [uncertain: bei] his [text lost] presence in the prayer houses, those perfor[text lost] genen baptisms, and holds with the women the church [uncertain: Kirchengan?] gen [text lost] Open despisers of the Lord's Supper unbewußt. [text lost] number [text lost] communicants: male 326 female 408 total 73[4?] [text lost] year 1881 gegen über more 131.– The inhabitants [uncertain: von] of Pyzdry [text lost] ten gladly an Evangelical school for themselves ein[text lost] sind [text lost] too poor for it, since the little town counts only 9 families[?], and [text lost]"""

P_0345a = """[text lost]d lay people dazu beigezogen werden können, as the [text lost]olonien have their own teachers and prayer houses.–

[text lost]en mission were collected in the course of the year at the Mis[text lost]diensten 3 roubles 40 kopecks, [text lost]stor-Administrator to the Herr Superintenden[text lost]stor Manitius at Warsaw has sent on.– Morality [text lost] das häusliche Zusammenleben are in general satisfac[text lost]nd.– Special vices in the congregation not present.– Bap[text lost]en, Irwingians etc. there are none.– Conversions to other [text lost]fessionen do not take place.–

M[?]erkwürdige events.– Have not taken place.–

Number of the confirmed.– Boys 13 girls 10, together 23.–

Candidates living in the congregation.– None present.–

Collections.– For the benefit of the congregation's own were not [text lost]sammelt, but for other purposes the following: 1.) For the sup[text lost]zung of grammar-school pupils who are inclined to study theology [text lost] sind 1 rouble 76 kopecks, which the Pastor-Administra[text lost] his High Evangelical-Augsburg Consistory at [text lost]arschau sent.– 2.) For the widows' and orphans' fund [text lost] roubles 36 kopecks collected and the same to the Herr [text lost]uperintendenten of Boerner to Plock sent.–

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
            print(f'doc {doc} page {i} ({src}): German {de_n}, English {en_n}')
            bad |= en_n != de_n
            out['pages'].append({'page': i, 'confidence': 'medium',
                                 'marker_count': en_n, 'en': en + '\n'})
        with open(os.path.join(HERE, f'doc{doc}.yml'), 'w', encoding='utf-8',
                  newline='\n') as f:
            yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=1000)
    if bad:
        print('MARKER COUNTS DIFFER - fix the English')
