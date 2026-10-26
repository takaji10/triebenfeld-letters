# -*- coding: utf-8 -*-
"""Append the new people of APP 53/20/0/-/Poznań Gr.1181 to
reference/people.yml (before seed_not_in:) and their bios to
reference/people_bios.yml. Run once (2026-10-26).

The hit map was counted first (WORKING_NOTES, mistake 7): the surnames added
hit only this holding and its siblings of the same suit (Konin Gr.115, 118,
145, 153; Kalisz Tab.21; ADWl 85 for the Golinskis' exclusion), so the index
changes are the document's own. Each new entry is sampled against its hits
after the build.
"""
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PEOPLE = '''
# --- APP 53/20/0/-/Poznań Gr.1181 (added 2026-10-26) ---

skarbek-gora:
  display: "Eugeniusz de Góra Skarbek, castellan of Uniejów"
  render: "Eugeniusz Skarbek"
  match: "Skarbek\\\\w*"
  tier: "Text-confirmed"
  variants: []
  identity: "Eugeniusz de Góra Skarbek, castellan [written 'Castellanida'] of Uniejów (Junivladislavia), a witness at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181). The castellany of Uniejów sat in the palatinate of Łęczyca; the scribe's 'Junivladislaviensis' is its Latin. Not known further to the edition. Added 2026-10-26."
  merge: false

zelislawski:
  display: "Tomasz Zelisławski, burgrave of Konin"
  render: "Tomasz Zelisławski"
  match: "Zelisławsk\\\\w*"
  tier: "Text-confirmed"
  variants: []
  identity: "Tomasz Zelisławski, burgrave of the castellany of Konin, a witness at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181). Not known further to the edition; the diacritic-less 'Zelislawski' of I. HA Rep. 162 Nr. 295 is not matched to him (NEEDS_CONFIRMATION). Added 2026-10-26."
  merge: false

zakrzewski:
  display: "Zakrzewski"
  render: "Zakrzewski"
  match: "Zakrzewsk\\\\w*"
  tier: "Named in the documents (a family entry)"
  variants: []
  identity: "The Zakrzewski party of the Prusimski succession suit: the heirs of the sisters' line. Kazimierz Zakrzewski, judge territorial of Brześć in Kujawy, father of Joanna Nepomucena (judge castellany of Radziejów); his sons Ignacy, ensifer [miecznik] of Przedecz, and Ludwik, acted as the first actors of the suit at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181); Ignacy took the parties' oath on the bringing of the documents. Kazimierz Zakrzewski named (without the office) in Konin Gr.115 and Gr.118; Zakrzewskis in the Konin Gr.145 register and the Kalisz table (Tab. 21) and in Oe 1 Bü 9454 are not known to be of this family. Added 2026-10-26."
  merge: false

tomicki:
  display: "Tomicki"
  render: "Tomicki"
  match: "Tomick\\\\w*"
  tier: "Named in the documents (a family entry)"
  variants: []
  identity: "The Tomicki party of the Prusimski succession suit, heirs of Mariana de Prusimski Tomicka, the third daughter of Krzysztof Prusimski and Teresa Golińska: Paweł and Józef, brothers german, actors at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181), through the Magnificent Jakub, parent of Józef, regent territorial of Wieluń. Mariana's dowry and the decree of 1738 obtained by the Kowalskis for the sisters' betterment are recited in the decree. Tomickis in Konin Gr.118 and Gr.145 and in AGAD 1/169/0/1/1745 are not known to be of this family. Added 2026-10-26."
  merge: false

taczanowski:
  display: "Taczanowski"
  render: "Taczanowski"
  match: "Taczanow\\\\w*"
  tier: "Named in the documents (a family entry)"
  variants: []
  identity: "The Taczanowski party of the Prusimski succession suit: Rafał, Wincenty and Mikołaj, sons of the late Magnificent Elżbieta de Tworowicz, brothers german among the Taczanowskis, actors at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181), acting through the Magnificent Józef Taczanowski, regent territorial of Wieluń. Taczanowskis in Konin Gr.118 (a royal huntsman of the family) are not known to be these. Added 2026-10-26."
  merge: false

kolaczkowski:
  display: "Kołaczkowski"
  render: "Kołaczkowski"
  match: "Kołaczkow\\\\w*"
  tier: "Named in the documents (a family entry)"
  variants: []
  identity: "The Kołaczkowski party of the Prusimski succession suit, heirs of Wiktoria de Prusimski, the second daughter of Krzysztof Prusimski and Teresa Golińska: Piotr Kołaczkowski and his wife Kunegunda de Kowalski, actors at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181). Kołaczkowskis in Konin Gr.118 are not known to be these. Added 2026-10-26."
  merge: false

tworowicz:
  display: "Tworowicz"
  render: "Tworowicz"
  match: "Tworowicz\\\\w*"
  tier: "Named in the documents (a family entry)"
  variants: []
  identity: "The Tworowicz party of the Prusimski succession suit: Franciszek Tworowicz, actor at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181), of the family of the late Magnificent Elżbieta de Tworowicz, whose sons by Taczanowski acted beside him, and of Michał Tworowicz, the third husband of Wiktoria de Prusimski. Tworowiczes in Konin Gr.118 are not known to be these. Added 2026-10-26."
  merge: false

lubstowski:
  display: "Benedykt Lubstowski, abbot of Ląd"
  render: "Benedykt Lubstowski"
  match: "Lubstowsk\\\\w*"
  tier: "Text-confirmed"
  variants: []
  identity: "Benedykt Lubstowski, abbot of the Cistercian abbey of Ląd, cited with his convent at the condescensio of 29 March 1784 on the Trąbczyn grounds over the reproduction of the quietation of the 3,500 Hungarian ducats and the silver of the Prusimski house lodged in the convent's treasury (Poznań Gr.1181); the convent appeared through its procurator. Abbot of Ląd in the Konin Gr.118 and Gr.153 records (named there without this document's spelling being compared). Added 2026-10-26."
  merge: false

wybieralski:
  display: "Paweł Wybieralski, prior of Ląd"
  render: "Paweł Wybieralski"
  match: "Wybieralsk\\\\w*"
  tier: "Text-confirmed"
  variants: []
  identity: "Paweł Wybieralski, prior of the Cistercian convent of Ląd, cited with the abbot at the condescensio of 29 March 1784 on the Trąbczyn grounds (Poznań Gr.1181). A Wybieralski in Konin Gr.153 is not known to be he. Added 2026-10-26."
  merge: false

radolinski:
  display: "Radoliński"
  render: "Radoliński"
  match: "Radolinsc?\\\\w*"
  tier: "Named in the documents (a family entry)"
  variants: ["Radolinski", "Radolenski", "Radolensian"]
  identity: "The Radoliński family of Radolin, subchamberlains (podskarbi) territorial of Wschowa, holders of the 43,000-florins-Polish claim on the estates of Trąbczyn that the decree of 1784 leaves undecided: the obligation of 1736 upon the brothers Prusimski (Józef and Stefan Radoliński of the same name), the complanatio of 1744 with Teresa de Suinarska and her sons Mikołaj, Andrzej, Albert and Jan, the manual quietation of 1748 at Krethowo for 22,600 florins Polish, and the dispute whether the ultimate script of the citation is in Andrzej Radoliński's hand (Poznań Gr.1181). The spelling of the family name in this document is 'Radolinsk-'; the diacritic form Radoliński is the standard. Added 2026-10-26."
  merge: false

bienicki:
  display: "Andrzej Bienicki, parish priest of Zagórów"
  render: "Andrzej Bienicki"
  match: "Bienick\\\\w*"
  tier: "Text-confirmed"
  variants: ["Bienicki", "Bienickij"]
  identity: "Andrzej Bienicki, Most Honourable Reverend, parish priest of Zagórów: by the inscription of 1647 (Marcin Strzałkowski's 2,000 florins Polish over Szetlewo) and his own separate inscription of 1661 the 2,000 were given to the parish church of Zagórów in perpetuum, as the decree of 1784 recites from the acts of Pyzdry (Poznań Gr.1181). Added 2026-10-26."
  merge: false

golinski:
  display: "Goliński"
  render: "Goliński"
  match: "Golinsk\\\\w*"
  not_in: ["adwl85-1"]
  tier: "Named in the documents (a family entry)"
  variants: []
  identity: "The Goliński family, the maternal line of the Prusimski succession: Jan Łoso Golinski, burgrave of Konin (his purchases of Oporowo, Prusinowo and Szetlewek recited back to 1647), his wife Konstancja Krusińska, their daughter Teresa, wife of Krzysztof Prusimski, whose maternal estate the sisters' claim in the decree of 1784 works out (Poznań Gr.1181); Anna de Bojanowska, the mother of Paweł Golinski, and Apollonia, wife of Zygmunt Obiesierski, of the same house. The 'Golinska' of ADWł 85 is excluded from this entry and remains its own. Added 2026-10-26."
  distinct_from: ["golinska"]
  merge: false
'''

bios = '''szepczynski: ← keep anchor above; insertions go after the file's last entry
'''

# people.yml: insert before the seed_not_in comment block
p = 'reference/people.yml'
s = open(p, encoding='utf-8').read()
anchor = '# Long-tail names (reference/name_seeds.json) shut out of named documents.'
assert anchor in s and 'skarbek-gora:' not in s
s = s.replace(anchor, PEOPLE.strip('\n') + '\n\n' + anchor)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('people.yml: 12 entries appended')

# people_bios.yml: append at the end
b = 'reference/people_bios.yml'
s = open(b, encoding='utf-8').read()
assert 'skarbek-gora:' not in s
BIO = '''
skarbek-gora:
  bio: Eugeniusz de Góra Skarbek, castellan of Uniejów, a witness at the condescensio of 29 March 1784 on the Trąbczyn grounds.
  bio_de: Eugeniusz de Góra Skarbek, Kastellan von Uniejów, Zeuge bei der Kondeszension vom 29. März 1784 auf dem Grund von Trąbczyn.
zelislawski:
  bio: Tomasz Zelisławski, burgrave of the castellany of Konin, a witness at the condescensio of 29 March 1784 on the Trąbczyn grounds.
  bio_de: Tomasz Zelisławski, Burggraf der Kastellanei Konin, Zeuge bei der Kondeszension vom 29. März 1784 auf dem Grund von Trąbczyn.
zakrzewski:
  bio: The Zakrzewski family, heirs of the sisters' line in the Prusimski succession suit: Kazimierz, judge territorial of Brześć in Kujawy; his sons Ignacy, ensifer of Przedecz, and Ludwik, the first actors of the suit.
  bio_de: Die Familie Zakrzewski, Erben der Linie der Schwestern im Erbstreit der Prusimskis: Kazimierz, Landrichter von Brześć in Kujawy; seine Söhne Ignacy, Schwertträger von Przedecz, und Ludwik, die ersten Akteure des Rechtsstreits.
tomicki:
  bio: The Tomicki family, heirs of Mariana de Prusimski Tomicka, the third daughter of Krzysztof Prusimski and Teresa Golińska; Paweł and Józef, brothers german, acted in the suit.
  bio_de: Die Familie Tomicki, Erben der Mariana de Prusimski Tomicka, der dritten Tochter von Krzysztof Prusimski und Teresa Golińska; Paweł und Józef, leibliche Brüder, traten im Rechtsstreit auf.
taczanowski:
  bio: The Taczanowski family, heirs of the line of Elżbieta de Tworowicz: Rafał, Wincenty and Mikołaj, brothers german, acted in the suit through Józef Taczanowski, regent territorial of Wieluń.
  bio_de: Die Familie Taczanowski, Erben der Linie der Elżbieta de Tworowicz: Rafał, Wincenty und Mikołaj, leibliche Brüder, traten im Rechtsstreit durch Józef Taczanowski, Landregent von Wieluń, auf.
kolaczkowski:
  bio: The Kołaczkowski family, heirs of Wiktoria de Prusimski: Piotr Kołaczkowski and his wife Kunegunda de Kowalski acted in the suit.
  bio_de: Die Familie Kołaczkowski, Erben der Wiktoria de Prusimski: Piotr Kołaczkowski und seine Frau Kunegunda de Kowalski traten im Rechtsstreit auf.
tworowicz:
  bio: The Tworowicz family of the succession suit: Franciszek Tworowicz acted in it; Michał Tworowicz was the third husband of Wiktoria de Prusimski.
  bio_de: Die Familie Tworowicz des Erbstreits: Franciszek Tworowicz trat in ihm auf; Michał Tworowicz war der dritte Gemahl der Wiktoria de Prusimski.
lubstowski:
  bio: Benedykt Lubstowski, abbot of the Cistercian abbey of Ląd, cited at the condescensio of 1784 over the quietation of the 3,500 ducats and the silver of the Prusimski house in the convent's treasury.
  bio_de: Benedykt Lubstowski, Abt der Zisterzienserabtei Ląd, zitiert zur Kondeszension von 1784 wegen der Quittung über 3500 Dukaten und des Silbers des Prusimski-Hauses im Schatz des Konvents.
wybieralski:
  bio: Paweł Wybieralski, prior of the Cistercian convent of Ląd, cited with the abbot at the condescensio of 1784.
  bio_de: Paweł Wybieralski, Prior des Zisterzienserkonvents Ląd, mit dem Abt zur Kondeszension von 1784 zitiert.
radolinski:
  bio: The Radoliński family of Radolin, subchamberlains territorial of Wschowa, holders of the 43,000-florins-Polish claim on Trąbczyn that the decree of 1784 leaves undecided; Józef and Stefan Radoliński bound the brothers Prusimski in 1736.
  bio_de: Die Familie Radoliński aus Radolin, Unterkämmerer von Wschowa, Inhaber der Forderung von 43 000 Florin polnisch auf Trąbczyn, die das Dekret von 1784 unentschieden lässt; Józef und Stefan Radoliński verpflichteten die Brüder Prusimski 1736.
bienicki:
  bio: Andrzej Bienicki, parish priest of Zagórów; the 2,000 florins Polish of Szetlewo were given to the parish church of Zagórów in perpetuum by his inscription of 1661.
  bio_de: Andrzej Bienicki, Pfarrer von Zagórów; die 2000 Florin polnisch von Szetlewo wurden durch seine Eintragung von 1661 der Pfarrkirche von Zagórów in perpetuum geschenkt.
golinski:
  bio: The Goliński family, the maternal line of the Prusimski succession: Jan Łoso Golinski, burgrave of Konin, his wife Konstancja Krusińska, and their daughter Teresa, wife of Krzysztof Prusimski.
  bio_de: Die Familie Goliński, die mütterliche Linie der Prusimski-Erbschaft: Jan Łoso Golinski, Burggraf von Konin, seine Frau Konstancja Krusińska, und ihre Tochter Teresa, Gemahlin von Krzysztof Prusimski.
'''
open(b, 'w', encoding='utf-8', newline='\n').write(s.rstrip('\n') + '\n' + BIO.lstrip('\n'))
print('people_bios.yml: 12 bios appended')
