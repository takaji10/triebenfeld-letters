# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.136: from the editor's scans and texts to the edition.

    python units/app53170koningr136/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The images. Three from the archive, named after leaves:

    121.jpg   leaf 121 recto, one page
    122.jpg   an opening: leaf 121 verso | leaf 122 recto
    123.jpg   an opening: leaf 122 verso | leaf 123 recto

Page ids: leaf N recto is <N>_a2, leaf N verso is <N+1>_a1. Leaf 122 recto
(0122_a2) carries none of the transcribed text and is set apart (SKIP).

The text, and what is NOT in it. The entry is an inspection of the Trąbczyn
estate of 9 July 1754 with the court messenger's report of it. The editor
transcribed: the manor's buildings (leaf 121 and the first paragraph of leaf
121 verso); then, from "Wieś Nowa:" halfway down leaf 122 verso, the Olęder
plots and the count of dependent people; and leaf 123, the witnesses'
statement on the woods and the Latin record. Between those two parts the
scans have a numbered description of the village houses, one by one: the
rest of leaf 121 verso, all of leaf 122 and the top of leaf 122 verso. It is
in neither the editor's transcription nor their English. The holding is built
from what is transcribed; the question is held for the editor
(docs/PRUSIMSKI_QUESTIONS.md).

The check (2026-10-07). Read against the scans, enlarged: the heading on leaf
121; the count of people on leaf 122 verso; all of leaf 123. Not compared:
the description of the manor buildings on leaf 121 and leaf 121 verso (about
540 words of building terms). ROWS has what was corrected.

The English is the editor's. FIXES are the places where it followed a reading
that was corrected. Of the 51 footnotes three are left out (DROP_NOTES); the
others are the editor's explanations of terms and are kept as translator's
notes. A line in square brackets marks the place of the untranscribed list.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr136'
REF = 'APP 53/17/0/-/Konin Gr.136'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes-oblatae [protocollon] 1754 (53.17.0.-.Konin Gr.136)"

# (file, x of the fold or None for a single page, left page or the page, right
# page). The folds are a first proposal; the editor's saved folds
# (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('121.jpg', None, '0121_a2', None),
    ('122.jpg', 2390, '0122_a1', '0122_a2'),
    ('123.jpg', 2358, '0123_a1', '0123_a2'),
]
SKIP = ('0122_a2',)
LEAF = {'0121_a2': '121 recto', '0122_a1': '121 verso', '0122_a2': '122 recto', '0123_a1': '122 verso',
        '0123_a2': '123 recto'}
PAGE_OF = {'121': '0121_a2', '121v': '0122_a1', '122v': '0123_a1', '123': '0123_a2'}
DOCS = [(1, ['0121_a2', '0122_a1', '0123_a1', '0123_a2'])]
FOLD_NOTE = ('Leaf 122 recto is marked "left out" because none of it is transcribed: it is the middle of the list of '
             'village houses.')


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*Original.md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert len(head) == 3 and head[0].startswith('# Relationes-oblatae'), head    # the file's own heading: not text
    assert [l for l, _ in leaves] == ['121', '121v', '122v', '123'], [l for l, _ in leaves]
    return {(1, PAGE_OF[leaf]): paras for leaf, paras in leaves}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0121_a2', 'przyległościach[?] należących', 'przyległościach należących', 'the word is plain on the scan'),
    ('0123_a1', 'drugi [zs?] tyłko budy', 'drudzy tylko budy', 'the scan has "drudzy tylko": the others have only huts in the ground'),
    ('0123_a1', 'każdy bydła do roboty 6 pańskiego wołów 4 koni 4', 'każdy bydła do roboty 8 pańskiego wołów 4 koni 4',
     'the figure is 8, the four oxen and four horses that follow'),
    ('0123_a1', 'wozy 2 świnie zelaga wszystkie', 'wozy 2 świnie żelaza wszystkie',
     'the scan has "Zelaza": ironware, the iron gear of a farm. "Zelaga" is no word'),
    ('0123_a1', 'Półrolników 5 na z nich każdy', 'Półrolników 5 ma z nich każdy', 'the scan has "ma"'),
    ('0123_a1', 'świnię, wół, zelaga wszystkie', 'świnię, wół, żelaza wszystkie', 'as above: "Zelaza"'),
    ('0123_a1', 'Komornie wszystkiem 6.', 'Komornic wszystkich 8.',
     'the scan has "Komornic wszystkich. 8.": women lodgers, eight in all; the figure is written like the 8 four lines above'),
    ('0123_a1', 'tak ma zuprzag jak i insi', 'tak ma zaprzęg jak i insi', 'the scan has "zaprzęg", a team'),
    ('0123_a2', 'nad Szeklejowkiem ku Łazom', 'nad Szetlejowkiem ku Łazom',
     'the scan has "Szetleiowkiem": Szetlewek, the neighbouring estate, not a stream'),
    ('0123_a2', 'personaliter veniens … Providus Bartholomaeus', 'personaliter veniens Ministerialis Regni Generalis Providus Bartholomaeus',
     'the scan has "Mlis Rni Gnlis" with marks of abbreviation where the editor left a gap: he is the court messenger'),
    ('0123_a2', 'officio praesenti mentus sanus ear[umque] recognovit', 'officio praesenti notus sanus existens recognovit',
     'the scan has "notus sanus exns": known to the office, being of sound mind'),
    ('0123_a2', 'habitis secum Nobilibus Honestis Casimiro', 'habitis secum Nobilibus Generosis Casimiro',
     'the scan has "Gnosis": Generosis'),
    ('0123_a2', 'ab eodemque olim Magnifico[?] Marito', 'ab eodemque olim Magnifico Marito', 'the word is plain on the scan'),
    ('0123_a2', 'condescenderat pertinentiis ad Bona eadem Trąmpczyn principaliter cum villas',
     'condescenderat personaliter ad Bona eadem Trąmpczyn principaliter tum villas',
     'the scan has "personlr ... principaliter tum villas ... tum Borras": he went in person to Trąbczyn first, then to the '
     'villages, then to the woods'),
    ('0123_a2', 'Chuta attinentes cum Borras', 'Chuta attinentes tum Borras', 'as above: "tum"'),
    ('0123_a2', 'fecit facitque praesenti.', 'fecit facitque praesentem.', 'the scan has "praesentem"'),
]

DROP_NOTES = {
    '2': 'on a doubt at "przyległościach", which is plain on the scan',
    '34': 'on "zelaga" as an unknown word; the scan has "żelaza"',
    '44': 'on "Szeklejowek" as a watercourse; the scan has Szetlewek',
}
FIXES = [
    ('Full farmers: 4. Each of them has — working cattle: 6 of the lord\'s; oxen: 4; horses: 4; cows: 2; wagons: 2; pigs; '
     'zelaga — all as is proper',
     'Full farmers: 4. Each of them has — working cattle: 8 of the lord\'s; oxen: 4; horses: 4; cows: 2; wagons: 2; pigs; '
     'ironware — all as is proper', 'the figure is 8; "żelaza" is the iron gear of a farm'),
    ('a cow; a pig; an ox; zelaga — all as is proper', 'a cow; a pig; an ox; ironware — all as is proper', '"żelaza"'),
    ('Lodgers: in all, 6.', 'Female lodgers: in all, 8.', '"Komornic wszystkich 8"'),
    ('along the Szeklejowek toward Łazy', 'above Szetlewek toward Łazy', '"nad Szetlejowkiem": the neighbouring estate'),
    ('appearing in person — the Honest Bartłomiej Szeptycki [Szepczyński] of Trąmpczyn — of sound mind, declared before the '
     'present office: having with him',
     'appearing in person — the General Court Summoner of the Realm, the Honest Bartłomiej Szeptycki [Szepczyński] of '
     'Trąmpczyn, known to the present office, being of sound mind — declared: having with him',
     '"Ministerialis Regni Generalis Providus Bartholomaeus Szeptycki ... officio praesenti notus sanus existens recognovit"'),
    ('had made a formal descent to the appurtenances of the Trąmpczyn estate, principally to the villages of Osiny, Łazy, '
     'Nowa Wieś, the olędry, and the Huta, with the pine forests and woodlands pertaining to those same goods',
     'had made a formal descent in person to the same Trąmpczyn estate first, then to the villages of Osiny, Łazy, '
     'Nowa Wieś, the olędry, and the Huta belonging to it, then to the pine forests and woodlands pertaining to those same goods',
     '"condescenderat personaliter ad Bona eadem Trąmpczyn principaliter tum villas ... tum Borras ac Sylvas"'),
]
GAP = ('[The description of the village houses, one by one, which follows here on the rest of leaf 121 verso, on leaf 122 '
       'and at the top of leaf 122 verso, is not transcribed.]')


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*English Translation.md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0], DROP_NOTES)
    assert [l for l, _ in leaves] == ['121', '121v', '122v', '123'], [l for l, _ in leaves]
    order = [PAGE_OF[l] for l, _ in leaves]
    pages = {PAGE_OF[l]: p for l, p in leaves}
    # the editor's section headings stand before the leaf mark of the page they head
    for a, b in zip(order, order[1:]):
        if pages[a] and pages[a][-1].startswith('[Section'):
            pages[b].insert(0, pages[a].pop())
    pages['0122_a1'].append(GAP)
    pages = courtbook.fix_english(pages, FIXES)
    return {1: ['\n\n'.join(pages[p]) for p in order]}


S = {
 1: ('Bericht des Gerichtsboten Bartłomiej Szeptycki von Trąbczyn, am 12. Juli 1754 in die Akten des Burggerichts Konin eingetragen, mit der Besichtigung, die er am 9. Juli auf Verlangen der Katarzyna Prusimska, geborene Rozdrażewska, vorgenommen hatte. Sie ist die Witwe des kurz zuvor verstorbenen Paweł Prusimski, königlichen Kämmerers und Erbherrn von Trąbczyn, und hat an allen seinen Gütern ihr Leibgedinge und ein lebenslanges Nutzungsrecht. Die Besichtigung beschreibt die Gebäude des Gutshofs in Trąbczyn eines nach dem anderen: Das alte Herrenhaus ist nicht mehr zu reparieren, ein neues ist im Rohbau fertig; es folgen Küche, vier Scheunen, Schafstall, Speicher, Ställe, Brennerei und Mälzerei mit ihrem Gerät. In Nowa Wieś sitzen fünfzehn Olęder, die sechzehnte Hufe ist leer. Eine Aufstellung zählt die dienstpflichtigen Leute in Trąbczyn, Osiny, Łazy und Nowa Wieś nach Vollbauern, Halbbauern, Häuslern und Einliegern. Zwei Adlige, Kazimierz Świerczewski und Józef Puchalski, bezeugen mit ihrer Unterschrift, dass in den Kiefernwäldern von Trąbczyn von Osiny bis zur Grenze von Biskupice und um Łazy die besseren Stämme gefällt oder herausgesucht sind und nur Ausschuss steht, ebenso bei den Eichen, außer wo die Olęder das Holz auf ihren Hufen genommen haben. Die Beschreibung der Dorfhäuser im mittleren Teil des Eintrags ist nicht transkribiert.',
     'The report of the court messenger Bartłomiej Szeptycki of Trąbczyn, entered in the records of the castle court at Konin on 12 July 1754, with the inspection he had made on 9 July at the request of Katarzyna Prusimska, born Rozdrażewska. She is the widow of Paweł Prusimski, the King\'s chamberlain and heir of Trąbczyn, who had died shortly before, and holds her dower and a life interest in all his estates. The inspection describes the buildings of the manor farm at Trąbczyn one by one: the old manor house is past repair and a new one stands finished in the frame; then come the kitchen, four barns, the sheepfold, the granary, the stables and sties, the distillery and the malthouse with their gear. At Nowa Wieś there are fifteen Olęder settlers, and the sixteenth plot is empty. A list counts the people who owe labour in Trąbczyn, Osiny, Łazy and Nowa Wieś as full farmers, half-farmers, cottagers and lodgers. Two noblemen, Kazimierz Świerczewski and Józef Puchalski, state over their signatures that in the pine woods of Trąbczyn, from Osiny to the Biskupice boundary and round Łazy, the better trees have been felled or picked out and only the leavings stand, and the same of the oaks, except where the Olęder settlers have taken the timber on their plots. The description of the village houses in the middle of the entry is not transcribed.'),
}
HOW = ('written in the working session from the Polish and Latin as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
