# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.116: from the editor's scans and texts to the edition.

    python units/app53170koningr116/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is a rough register of the castle court of Konin for 1775 to 1777,
the volume after Konin Gr.115: short entries, many to a page, each sitting
under a line "Actum in Conin ...". The editor photographed nine openings and
transcribed the entries on the boundary commission between Trąbczyn and
Łukom. Each entry is a document; the three notes of one sitting on leaves 78
verso and 79 are one document (docs/PRUSIMSKI_ERA_PLAN.md).

    doc  leaf        scan  page      what
    1    78v         082   0079_a1   note: the extract of the constitution brought in (August 1775)
    2    78v, 79     082   0079_a1,  three notes of 16 August 1775: the letters of notice and the
                           0079_a2   two sides' citations
    3    89v         093   0090_a1   five commissioners protest against Chełmski's unilateral act
    4    89v         093   0090_a1   Prusimski protests against the Gliszczyńskis, Chełmski and others
    5    90          093   0090_a2   Rajewicz protests
    6    94v         098   0095_a1   heading only: inspection of the boundary line (3 October 1775)
    7    95v         099   0096_a1   Chełmski's counter-protest (9 October 1775)
    8    131v, 132   134   0132_a1,  Prusimski's men ask for a decree given in default; not
                           0132_a2   brought in (16 February 1776)
    9    175         177   0175_a2   heading only: a search for Chełmski (1 July 1776)
    10   201v, 202   204   0202_a1,  heading only: a search for Chełmski (5 September 1776);
                           0202_a2   his signature under "Vacuum" on the next page
    11   266v        269   0267_a1   heading of a protest by Prusimski, closed for want of a text
    12   335v        338   0336_a1   Chełmski in person asks for the commission's decree; not found

The scans are photographs named by their number in a series, not by leaf.
Leaf numbers were read off the right-hand pages: 082 is leaves 78v|79, 093
is 89v|90, 098 is 94v|95, 099 is 95v|96, 134 is 131v|132, 177 is 174v|175,
204 is 201v|202, 269 is 266v|267, 338 is 335v|336. Page ids: leaf N recto is
<N>_a2, leaf N verso is <N+1>_a1. Five halves carry nothing transcribed and
are set apart. The folds were set by eye (courtbook.find_fold puts them too
far right on photographs); they are first proposals for the editor.

What read_source does to the editor's file beyond cutting it:
- signatures are added under seven entries (SIGN): the editor's file had
  only Prusimski's on leaf 266 verso. They are given as written; "[?]"
  stands for a word not read (three places);
- "Vacuum", the clerk's word across the space left for an entry that was
  never written, is added under the headings on leaves 175 and 201 verso,
  with the signature that stands under it (on leaf 202 for the second).

Not transcribed: the pen strokes that bar the space under the heading on
leaf 94 verso; a "Vacuum" signed by Chełmski at the top of leaf 95 verso,
above his counter-protest, whose heading is on a page not photographed.

The check (2026-10-07). The entries are short, and all of them were read
against the scans, enlarged, with every heading and date line. ROWS has what
was corrected. Left as the editor has them: "designat[o?]" (leaf 78 verso),
"Junivladislaviensi[?]", "[de?] Diligenter" (leaf 90), "int[?] ... [et?]"
(leaf 201 verso), the end of the entry on leaf 335 verso, which is faint,
and the endings the editor gave to abbreviated words.

The English is the editor's own. FIXES are the places where it followed a
reading that was corrected, and SIGN_EN the signatures.

The spot sheet of 2026-10-07. In Rajewicz's protest (document 5) the check
had read "Citraque Ejus Assensum", without his consent. The editor, against
the page, reads "Cumque". Their reading stands (full_check.json beside this
file, applied with --full after --correct), their own English "with his
consent [?]" is put back, and the summary no longer says anything about
consent.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

FULL = courtbook.full_check(HERE)

SLUG = 'app53170koningr116'
REF = 'APP 53/17/0/-/Konin Gr.116'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1775-1777 (53.17.0.-.Konin Gr.116)"

# (file, x of the fold, left page, right page). First proposals, set by eye;
# the editor's saved folds (folds.json beside this file) are used instead
# where they exist.
SCANS = [
    ('082.jpg', 1950, '0079_a1', '0079_a2'),
    ('093.jpg', 1968, '0090_a1', '0090_a2'),
    ('098.jpg', 1974, '0095_a1', '0095_a2'),
    ('099.jpg', 1980, '0096_a1', '0096_a2'),
    ('134.jpg', 1938, '0132_a1', '0132_a2'),
    ('177.jpg', 1926, '0175_a1', '0175_a2'),
    ('204.jpg', 1956, '0202_a1', '0202_a2'),
    ('269.jpg', 1959, '0267_a1', '0267_a2'),
    ('338.jpg', 2061, '0336_a1', '0336_a2'),
]
SKIP = ('0095_a2', '0096_a2', '0175_a1', '0267_a2', '0336_a2')
LEAF = {'0079_a1': '78 verso', '0079_a2': '79 recto', '0090_a1': '89 verso', '0090_a2': '90 recto',
        '0095_a1': '94 verso', '0095_a2': '95 recto', '0096_a1': '95 verso', '0096_a2': '96 recto',
        '0132_a1': '131 verso', '0132_a2': '132 recto', '0175_a1': '174 verso', '0175_a2': '175 recto',
        '0202_a1': '201 verso', '0202_a2': '202 recto', '0267_a1': '266 verso', '0267_a2': '267 recto',
        '0336_a1': '335 verso', '0336_a2': '336 recto'}
DOCS = [(1, ['0079_a1']), (2, ['0079_a1', '0079_a2']), (3, ['0090_a1']), (4, ['0090_a1']), (5, ['0090_a2']),
        (6, ['0095_a1']), (7, ['0096_a1']), (8, ['0132_a1', '0132_a2']), (9, ['0175_a2']),
        (10, ['0202_a1', '0202_a2']), (11, ['0267_a1']), (12, ['0336_a1'])]
FOLD_NOTE = ('All nine scans are shown. On four, both halves are pages of the edition; on five, one half is a page and '
             'the other is left out.')

# Signatures, as written. "[?]" is a word not read.
SIGN = {
    3: ['Ludwik Dąmbski Wojewoda Brzeski Kujawski Jako Kommissarz Prezes mp',
        'Jo Brzezinski Sta [?] jako kommissarz mp',
        'Stanisław Dąmbski [?] Komisarz mp',
        'Jan na Kwilczu Kwilecki Czesnik Wschowski iako komisarz mp',
        'Kaietan Uminski Czesnik Kowalski Podwoie: [?] Komisarz'],
    4: ['Antoni na Kolnie Prusimski Sta: Nieszczew: mp'],
    5: ['Petrus Rajewicz mp'],
    7: ['Stanisław Chełmski mp'],
    8: ['Antoni Lipinski Mikołaj Ostroski'],
    9: ['Vacuum', 'Fr Zielonacki'],
    12: ['Stanisław Scibor Chełmski mp'],
}
VACUUM_201V = ['Vacuum']
LEAF_202 = ['Vacuum', 'Stanisław Scibor Chełmski']


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == [
        ('78v', 7), ('79', 2), ('89v', 4), ('90', 2), ('94v', 2), ('95v', 2), ('131v', 3), ('132', 1), ('175', 1),
        ('201v', 1), ('266v', 3), ('335v', 2)], [(l, len(p)) for l, p in leaves]
    L = dict(leaves)
    return {
        (1, '0079_a1'): L['78v'][:2],
        (2, '0079_a1'): L['78v'][2:],
        (2, '0079_a2'): L['79'],
        (3, '0090_a1'): L['89v'][:2] + SIGN[3],
        (4, '0090_a1'): L['89v'][2:] + SIGN[4],
        (5, '0090_a2'): L['90'] + SIGN[5],
        (6, '0095_a1'): L['94v'],
        (7, '0096_a1'): L['95v'] + SIGN[7],
        (8, '0132_a1'): L['131v'],
        (8, '0132_a2'): L['132'] + SIGN[8],
        (9, '0175_a2'): L['175'] + SIGN[9],
        (10, '0202_a1'): L['201v'] + VACUUM_201V,
        (10, '0202_a2'): LEAF_202,
        (11, '0267_a1'): L['266v'],
        (12, '0336_a1'): L['335v'] + SIGN[12],
    }


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0079_a1', 'Prusimski Lu~ Innotescen~', 'Prusimski Litt~ Innotescen~',
     'the scan has "Litt" with a mark of abbreviation, as "Litt~ Innotescentialium" in the note itself: the letters of notice'),
    ('0079_a1', 'p~r Commissione ad Campun~ editarium Relatio', 'pro Commissione ad Campum editarum Relatio',
     'the scan has "pro" and "Campum editarum"'),
    ('0090_a1', 'Illustrissimi Prezes Magnifici Commissarii Campestres Inter Trąmpczyn et Łukom contra Actum Granitt~ Illn [?]str~',
     'Illustres Magnifici Commissarii Campestres Inter Trąmpczyn et Łukom contra Actum Granitt~ Manifestantur',
     'the heading has "Illustres. Mfci. Commissarij Campestres ... con. Actum. Granitt. Mnfstr." with a mark: no "Prezes"; the '
     'last word is Manifestantur, they protest'),
    ('0090_a1', 'Illustrissimos Magnificos Dąmbski Palatinati Bresto', 'Illustrium Magnificorum Dąmbski Palatini Bresto',
     'the scan has "Palatini": Dąmbski is the palatine (voivode), as he signs below, "Wojewoda"; the titles before the name '
     'are abbreviated genitives'),
    ('0090_a1', 'Brzetinski', 'Brzezinski', 'the scan has "Brzezinski", as he signs below'),
    ('0090_a1', 'et Alios [Anfso~?]', 'et Alios Manifestatur', 'the heading ends "Mnfstr" with a mark: Manifestatur'),
    ('0090_a1', 'Tomic Pdpesmie[?] Stanislaus', 'Tomic Possessores[?] Stanislaus',
     'the scan has a word beginning "Poss" and ending "es", abbreviated in the middle; the heading has "PP. Tomic". Read as '
     'Possessores and left marked'),
    ('0090_a1', 'Haeredes [&?] Idque', 'Haeredes &c. Idque', 'the scan has the sign for "et cetera"'),
    ('0090_a2', 'Diligentiae Ilorfstr[?]', 'Diligentiae Manifestatur', 'the heading ends "Mnfstr" with a mark: Manifestatur'),
    ('0090_a2', 'prout se se nullo modo', 'prout se de nullo modo', 'the scan has "se de nullo modo"'),
    ('0090_a2', 'Involverat [U?]tr?g[em?] Ejus Assensam res Sunt gesta [de?]', 'Involverat Citraque Ejus Assensum res Sunt gestae [de?]',
     'the scan has "Citr" at the end of the line and "que Ejus Assensum res sunt gestae" on the next: citraque ejus assensum, '
     'and without his consent'),
    ('0096_a1', 'Trąmpczyno Remnsstr[?]', 'Trąmpczyno Remanifestatur', 'the heading ends "Remnfstr" with a mark: Remanifestatur'),
    ('0132_a1', 'Recogno[si?]verunt', 'Requisiverunt', 'the scan has "Requisi|verunt" over the line end, the first part written over a correction'),
    ('0132_a2', 'ac Diem hodiernam hic Irreperibile extradens Nequit', 'ad Diem hodiernam hic Irreperibile extradere Nequit',
     'the scan has "ad Diem" (up to this day, exclusive) and "extradere"'),
    ('0175_a2', 'Łukom Lat[i/e?] Requisitio', 'Łukom Lati Requisitio', 'the scan has "Lati"'),
    ('0202_a1', 'Trąmpczyn La[?] Requisitio', 'Trąmpczyn Lati Requisitio', 'the scan has "Lati", as in the heading on leaf 175'),
    ('0336_a1', 'Sibi qui Extradi Petivit Decretum quidam Commissoriale', 'Sibique Extradi Petiit Decretum quoddam Commissoriale',
     'the scan has "Sibique", "Petijt" and "quoddam"'),
    ('0336_a1', 'ac si [?]eore oblatae in statis Officii seperibile', 'ac si More oblatae in Actis Officii reperibile',
     'the scan has "More oblatae in Actis Officij reperibile": as if to be found in the records of the office, entered as an oblata'),
]

FIXES = [
    ('Prusimski Lu[...] — Innotescentia — Oblata', 'Prusimski — Letters of Innotescence — Oblata',
     '"Litt~ Innotescen~": the abbreviation is Litterarum, the letters'),
    ('against the [uncertain: H] Collaterals and Trąbczyn', 'against the [Heirs], Collaterals and Trąbczyn',
     '"HH." is plain on the scan: Haeredes, as on leaf 78 verso'),
    ('against [uncertain: H] Trąbczyn, Drzewce', 'against the [Heirs] of Trąbczyn, Drzewce', 'the same'),
    ('The Most Illustrious President and Right Honourable Field Commissioners between Trąbczyn and Łukom, against the '
     'Boundary Act — [Manifestatio of the] Most Illustrious [?]',
     'The Most Illustrious Right Honourable Field Commissioners between Trąbczyn and Łukom protest against the Boundary Act',
     'the heading has no "Prezes" and ends "Manifestantur"'),
    ('Dąmbski, of the Palatinate of Brest-Kuyavia; Brzetiński,', 'Dąmbski, Palatine of Brest-Kuyavia; Brzeziński,',
     '"Palatini": he is the palatine (voivode); "Brzezinski"'),
    ('Łukom and Trąbczyn — made and in the original submitted among the Produced Documents.',
     'Łukom and Trąbczyn — made, among the Produced Documents.',
     'this note has only "facta in Productis"; "et in Originali Porrecta" is in the next one'),
    ('Right Honourable Prusimski against the Right Honourables [of] Tomic and Others — [?]',
     'Right Honourable Prusimski against the [Possessors of] Tomic and Others — Protest', '"PP. Tomic et Alios Manifestatur"'),
    ('heirs of the goods of Tomic [and] [uncertain: Pdpesmie], and Stanisław Chełmski, heir of the goods of Łukomia',
     '[uncertain: possessors] of the goods of Tomic, and Stanisław Chełmski, heir of the goods of Łukomia, etc.',
     '"Bonorum Tomic Possessores[?] Stanislaus Chełmski Bonorum Łukomia Haeredes &c."'),
    ('The Honourable Rajewicz — by force of due diligence — [?]', 'The Honourable Rajewicz — by force of due diligence — Protest',
     'the heading ends "Manifestatur"'),
    ('— yet things were done with his consent [?] —', '— and that things were done without his consent —',
     '"Citraque Ejus Assensum res Sunt gestae": citra, without'),
    ('Commission Act at Trąbczyn — Counter-Protest [?]', 'Commission Act at Trąbczyn — Counter-Protest', 'the heading ends "Remanifestatur"'),
    ('acknowledged and requested from the present Office', 'requisitioned and requested from the present Office',
     '"Requisiverunt", as in the entry on leaf 335 verso'),
    ('Field Decree between the goods of Łukom and Trąbczyn [?issued]', 'Field Decree issued between the goods of Łukom and Trąbczyn',
     '"Lati" is plain on the scan'),
]
VACUUM_EN = 'Vacuum ["empty": the space left for the entry was not filled]'
SIGN_EN = {
    3: ['Ludwik Dąmbski, Voivode of Brest-Kuyavia, as commissioner and president, by his own hand',
        'Jo. Brzeziński, Starost of [illegible], as commissioner, by his own hand',
        'Stanisław Dąmbski, [illegible], commissioner, by his own hand',
        'Jan Kwilecki of Kwilcz, Cup-bearer of Wschowa, as commissioner, by his own hand',
        'Kajetan Umiński, Cup-bearer of Kowal, deputy voivode [illegible], commissioner'],
    4: ['Antoni of Kolno Prusimski, Starost of Niszczewice, by his own hand'],
    5: ['Petrus Rajewicz, by his own hand'],
    7: ['Stanisław Chełmski, by his own hand'],
    8: ['Antoni Lipiński, Mikołaj Ostroski'],
    9: [VACUUM_EN, 'Fr. Zielonacki'],
    12: ['Stanisław Ścibor Chełmski, by his own hand'],
}


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [(l, len(p)) for l, p in leaves] == [
        ('78v', 7), ('79', 2), ('89v', 4), ('90', 2), ('94v', 2), ('95v', 2), ('131v', 3), ('132', 1), ('175', 1),
        ('201v', 1), ('266v', 3), ('335v', 2)], [(l, len(p)) for l, p in leaves]
    L = courtbook.fix_english(dict(leaves), FIXES + FULL['FIXES'])
    j = '\n\n'.join
    return {
        1: [j(L['78v'][:2])],
        2: [j(L['78v'][2:]), j(L['79'])],
        3: [j(L['89v'][:2] + SIGN_EN[3])],
        4: [j(L['89v'][2:] + SIGN_EN[4])],
        5: [j(L['90'] + SIGN_EN[5])],
        6: [j(L['94v'])],
        7: [j(L['95v'] + SIGN_EN[7])],
        8: [j(L['131v']), j(L['132'] + SIGN_EN[8])],
        9: [j(L['175'] + SIGN_EN[9])],
        10: [j(L['201v'] + [VACUUM_EN]), j(['Vacuum', 'Stanisław Ścibor Chełmski'])],
        11: [j(L['266v'])],
        12: [j(L['335v'] + SIGN_EN[12])],
    }


S = {
 1: ('Registervermerk im Buch des Burggerichts Konin, August 1775: Vorgelegt wird ein Auszug der Konstitution, mit der die Stände der Republik eine Kommission auf den Grund von Trąbczyn angeordnet haben, um dieses Gut gegen Łukom abzugrenzen; der Auszug ist den Akten des königlichen Hofes in Warschau entnommen und liegt bei den vorgelegten Schriftstücken.',
     'A register note in the book of the castle court at Konin, August 1775: an extract is brought in of the constitution by which the Estates of the Republic ordered a commission to the ground of Trąbczyn, to mark that estate off from Łukom; the extract was drawn from the records of the royal court at Warsaw and is among the documents produced.'),
 2: ('Drei Registervermerke vom 16. August 1775 zur Bekanntmachung der Grenzkommission. Für Prusimski wird das Bekanntmachungsschreiben für die auf den Grund von Trąbczyn angesetzte Kommission vorgelegt, eingereicht vom ersten der Unterzeichner. Vermerkt wird ferner der Bericht über die Ladungen, die Antoni Prusimski, Starost von Niszczewice und Erbherr von Trąbczyn, an die Erbherren und Besitzer von Łukom, Podbiele und Szetlew sowie an Abt und Konvent von Ląd hat ergehen lassen, und der Bericht über die Ladungen, die Chełmski, Erbherr von Łukom, an die Erbherren von Trąbczyn, Drzewce und Biskupice zum Termin der Grenzkommission zwischen Trąbczyn und Łukom hat ergehen lassen.',
     'Three register notes of 16 August 1775 on the announcement of the boundary commission. For Prusimski the letters of notice for the commission appointed to the ground of Trąbczyn are brought in, handed in by the first of those who signed them. Also noted are the report of the citations that Antoni Prusimski, Starost of Niszczewice and heir of Trąbczyn, had served on the heirs and possessors of Łukom, Podbiele and Szetlew and on the abbot and convent of Ląd, and the report of the citations that Chełmski, heir of Łukom, had served on the heirs of Trąbczyn, Drzewce and Biskupice for the term of the boundary commission between Trąbczyn and Łukom.'),
 3: ('Registervermerk über einen Protest, eingetragen in Konin im September 1775. Fünf Kommissare der Feldkommission zwischen Trąbczyn und Łukom sind persönlich erschienen: Dąmbski, Woiwode von Brześć Kujawski, Brzeziński, Starost von Inowrocław, Dąmbski, Fähnrich von Brześć Kujawski, Kwilecki und Umiński. Sie protestieren gegen Chełmski und die von seiner Seite beigezogenen Kommissare wegen einer Handlung, die diese einseitig auf dem strittigen Grund von Łukom und Trąbczyn vorgenommen haben. Alle fünf haben eigenhändig unterschrieben, Ludwik Dąmbski als Kommissar und Präses.',
     'A register note of a protest, entered at Konin in September 1775. Five commissioners of the field commission between Trąbczyn and Łukom appeared in person: Dąmbski, voivode of Brześć Kujawski, Brzeziński, Starost of Inowrocław, Dąmbski, standard-bearer of Brześć Kujawski, Kwilecki and Umiński. They protest against Chełmski and the commissioners brought in on his side, for an act that these made unilaterally on the disputed ground of Łukom and Trąbczyn. All five signed in their own hands, Ludwik Dąmbski as commissioner and president.'),
 4: ('Registervermerk über einen Protest, eingetragen in Konin im September 1775. Antoni Prusimski, Starost von Niszczewice und Erbherr von Trąbczyn, ist persönlich erschienen und protestiert gegen die Gliszczyński von Tomice, gegen Stanisław Chełmski von Łukomia und andere, wegen der Verwicklung des Grenzverfahrens im Feld und anderer Umstände. Der Protest wurde im Original eingereicht und liegt bei den vorgelegten Schriftstücken. Prusimski hat unterschrieben.',
     'A register note of a protest, entered at Konin in September 1775. Antoni Prusimski, Starost of Niszczewice and heir of Trąbczyn, appeared in person and protests against the Gliszczyńskis of Tomice, Stanisław Chełmski of Łukomia and others, for the entangling of the boundary proceedings in the field and for other circumstances. The protest was handed in in the original and is among the documents produced. Prusimski signed.'),
 5: ('Registervermerk über einen Protest, eingetragen in Konin im September 1775. Piotr Rajewicz ist persönlich erschienen und erklärt vorsorglich, er habe sich in das zwischen Łukom und Trąbczyn betriebene Grenzverfahren in keiner Weise eingelassen. Er hat unterschrieben.',
     'A register note of a protest, entered at Konin in September 1775. Piotr Rajewicz appeared in person and declares, as a precaution, that he in no way took part in the boundary proceedings conducted between Łukom and Trąbczyn. He signed.'),
 6: ('Überschrift eines Eintrags vom 3. Oktober 1775: für den Erbherrn von Trąbczyn, Besichtigung des Grenzzugs. Der Eintrag selbst wurde nicht geschrieben.',
     'The heading of an entry of 3 October 1775: for the heir of Trąbczyn, an inspection of the boundary line. The entry itself was not written.'),
 7: ('Registervermerk über einen Gegenprotest vom 9. Oktober 1775. Stanisław Ścibor Chełmski, Erbherr des Gebiets von Łukomia, ist persönlich erschienen und protestiert seinerseits gegen Antoni Prusimski, Starost von Niszczewice, und gegen die Handlung der Grenzkommission zwischen Trąbczyn und Łukom. Der Gegenprotest liegt bei den vorgelegten Schriftstücken. Chełmski hat unterschrieben.',
     'A register note of a counter-protest of 9 October 1775. Stanisław Ścibor Chełmski, heir of the Łukomia lands, appeared in person and protests in his turn against Antoni Prusimski, Starost of Niszczewice, and against the act of the boundary commission between Trąbczyn and Łukom. The counter-protest is among the documents produced. Chełmski signed.'),
 8: ('Eintrag vom 16. Februar 1776. Antoni Lipiński und Nicolaus Ostrowski erscheinen mit dem Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vor dem Burgamt Konin. Im Namen von Antoni Prusimski von Kolno, Starost von Niszczewice und Erbherr von Trąbczyn, verlangen sie die Herausgabe eines Kommissionsdekrets, das kraft der neuen Konstitution auf dem strittigen Grund von Trąbczyn und Łukom als Versäumnisdekret gegen Prusimski ergangen und angeblich dem Amt zur Eintragung eingereicht worden sei. Das Amt hat sein Protokoll durchgesehen: Das Dekret ist bis zum heutigen Tag nicht eingereicht worden; das Amt kann es nicht herausgeben und bescheinigt die Nachsuche. Die beiden haben unterschrieben.',
     'An entry of 16 February 1776. Antoni Lipiński and Nicolaus Ostrowski appear before the castle office at Konin with the court messenger Bartłomiej Szepczyński of Trąbczyn. In the name of Antoni Prusimski of Kolno, Starost of Niszczewice and heir of Trąbczyn, they ask to be given a commission decree that was pronounced under the new constitution on the disputed ground of Trąbczyn and Łukom in default of Prusimski and is claimed to have been brought in to the office for entry. The office has looked through its register: the decree has not been brought in up to this day; the office cannot give it out and certifies the search. Both men signed.'),
 9: ('Überschrift eines Eintrags vom 1. Juli 1776: für Chełmski, Nachsuche nach dem in Trąbczyn und Łukom ergangenen Kommissionsdekret. Der Eintrag wurde nicht geschrieben; über dem leeren Platz steht „Vacuum“, darunter die Unterschrift Fr. Zielonacki.',
     'The heading of an entry of 1 July 1776: for Chełmski, a search for the commission decree given at Trąbczyn and Łukom. The entry was not written; "Vacuum" stands across the empty space, and under it the signature Fr. Zielonacki.'),
 10: ('Überschrift eines Eintrags vom 5. September 1776: für Chełmski, Nachsuche nach dem Mandat und dem Felddekret, die zwischen den Gütern Łukom und Trąbczyn ergangen sind. Der Eintrag wurde nicht geschrieben; über dem leeren Platz steht „Vacuum“, auf der folgenden Seite unterschrieben von Stanisław Ścibor Chełmski.',
      'The heading of an entry of 5 September 1776: for Chełmski, a search for the mandate and the field decree given between the estates of Łukom and Trąbczyn. The entry was not written; "Vacuum" stands across the empty space, signed on the following page by Stanisław Ścibor Chełmski.'),
 11: ('Überschrift eines Protests von Prusimski gegen Chełmski, ohne Datum, wohl 1777. Darunter vermerkt der Schreiber, dass die Angaben dazu nicht geliefert wurden und dass auf Verlangen der Partei nach Ablauf von drei Tagen „limitiert“ wird. Antoni Prusimski von Kolno, Starost von Niszczewice, hat unterschrieben.',
      'The heading of a protest by Prusimski against Chełmski, undated, probably of 1777. Under it the clerk notes that the information for it was not supplied and that, at the party\'s request and three days having passed, it "is limited". Antoni Prusimski of Kolno, Starost of Niszczewice, signed.'),
 12: ('Eintrag ohne Datum, wohl vom Oktober 1777. Stanisław Ścibor Chełmski, Erbherr von Łukom, erscheint persönlich vor dem Burgamt Konin und verlangt die Herausgabe eines Feldkommissionsdekrets, das zwischen den Erbherren der Dörfer Nowa Wieś, Łazy, Osiny, Trąbczyn, Łukom und anderer ergangen sei, kraft der von den Ständen mit der Konstitution von 1775 erteilten Kommission, und das die Kommissare auf Seiten Prusimskis unterschrieben hätten. Das Amt findet es in seinen Akten nicht, kann es nicht herausgeben und bescheinigt die Nachsuche. Chełmski hat unterschrieben.',
      'An undated entry, probably of October 1777. Stanisław Ścibor Chełmski, heir of Łukom, appears in person before the castle office at Konin and asks to be given a field commission decree pronounced between the heirs of the villages of Nowa Wieś, Łazy, Osiny, Trąbczyn, Łukom and others, under the commission granted by the Estates in the constitution of 1775, and signed by the commissioners on Prusimski\'s side. The office does not find it in its records, cannot give it out, and certifies the search. Chełmski signed.'),
}
HOW = ('written in the working session from the Latin as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
