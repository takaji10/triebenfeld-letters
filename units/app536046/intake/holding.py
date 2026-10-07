# -*- coding: utf-8 -*-
"""APP 53/6/0/-/46: from the editor's scans and texts to the edition.

    python units/app536046/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                            [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The images. Two frames of a microfilm, black and white, numbered in a series:

    192.jpg   leaf 181 verso | leaf 182 recto
    193.jpg   leaf 182 verso | leaf 183 recto

Entry no. 16 begins halfway down leaf 182 verso and fills it. At its foot the
clerk wrote "sub nro 15 ...": for want of room he went back and wrote the
end of the entry on the other side of the same leaf, at the foot of leaf 182
recto, under entry no. 15. So the document is read verso first. The edition
keeps a document's pages in the order of their names, so the two pages of
this leaf are named in reading order and not by the usual rule: 0182_b1 is
leaf 182 verso (the left half of 193.jpg), 0182_b2 is leaf 182 recto (the
right half of 192.jpg). The other two halves are set apart.

The editor's Latin file has three parts, marked "[182v]", "[182]" and
"[182v]" again, and a heading with no mark:
- the heading of the sitting (20 October 1777, with the names of the judge,
  the deputy judge and the notary): on a page not among the scans; quoted on
  the holding's page; the ground of the date;
- "[182v]" and "[182]": entry no. 16, the document;
- the second "[182v]", headed "N. 16to": this is entry no. 17, on leaf 183
  recto. The editor's English file does not translate it, and its Latin is a
  first reading with more than forty doubts. It is not built; the question is
  held for the editor.

The check (2026-10-07). The whole of entry no. 16 was read against the
microfilm, enlarged. The film is sharp enough for the words but not for every
ending, and the hand abbreviates nearly everything. ROWS has the passages
where the reading changed; four doubts of the editor's are kept, and the
document is marked as a rough transcription (rulings.yml). The clerk's
direction at the foot of leaf 182 verso is added (CONTINUED).

The English. The editor's English of this entry rested on the first reading
and marked ten places as unresolved. It is revised here throughout (PAGES),
in the editor's terms. What differs in substance is listed in changes.yml.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app536046'
REF = 'APP 53/6/0/-/46'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Decreta [protocollon] 1773-1777 (53.6.0.-.46)"

# (file, x of the fold, left page, right page). First proposals; the editor's
# saved folds (folds.json beside this file) are used instead where they exist.
SCANS = [
    ('192.jpg', 1727, '0182_a1', '0182_b2'),
    ('193.jpg', 1701, '0182_b1', '0183_a2'),
]
SKIP = ('0182_a1', '0183_a2')
LEAF = {'0182_a1': '181 verso', '0182_b2': '182 recto', '0182_b1': '182 verso', '0183_a2': '183 recto'}
DOCS = [(1, ['0182_b1', '0182_b2'])]
FOLD_NOTE = ('The entry begins on the left page of the second scan and ends at the foot of the right page of the first. '
             'The wide dark margins are the microfilm frame.')
CONTINUED = 'sub nro 15. P. alt[?]'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    head, leaves = courtbook.read_leaves(f[0])
    assert len(head) == 2 and head[0].startswith('Actum in Judiciis Terrestribus'), head       # the heading of the sitting
    assert [l for l, _ in leaves] == ['182v', '182', '182v'] and all(len(p) == 1 for _, p in leaves), leaves
    assert leaves[2][1][0].startswith('N. 16to: Inter Eundem'), leaves[2][1][0][:30]              # entry no. 17: not built
    return {(1, '0182_b1'): leaves[0][1] + [CONTINUED], (1, '0182_b2'): leaves[1][1]}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0182_b1', 'Capitaneum Nieszczevicensem Actum personaliter Judicialiter et Terminum Partes Actorae ad Judicialite[r?] suum editur '
                'Decretum controversiis exauditis',
     'Capitaneum Nieszczevicensem Citatum personaliter Judicium et Terminum Partis Actoreae ad Judicium suum editum '
     'Decidendo controversiis exauditis',
     'the set opening of a decree, as in the decree of 1728 and in entry no. 17 below it: the court, "deciding the term of '
     'the plaintiff party brought before it"; Prusimski is "Citatus", the one cited'),
    ('0182_b1', '[L?]i[c?]et[?] si[?] Magnificus Chełmski Terminum cen~[?] Magnificu[s?] Prusimski Edita comportata actis cujusdam ac si '
                'Granicialis per Commissarios a statibus Regni designatos et per m[?] Capit~ conductos Inter Bona Łukom et '
                'Trąbczyn prolati pr[?]tendi[?] Requisit[o?]que trinas Ejusdem Actis Granitialis [s??] coram',
     'Licet si[?] Magnificus Chełmski Terminum cen~[?] Magnificu[s?] Prusimski Eden~ comportat~ actus cujusdam ac si '
     'Granitialis per Commissarios a statibus Regni designatos et per Magnificum Capitaneum conductos Inter Bona Łukom et '
     'Trąbczyn prolati praetendit Requisitionesque trinas Ejusdem Actus Granitialis primam coram',
     'the scan has "actus cujusdam ... prolati praetendit Requisitionesque trinas Ejusdem actus Granitialis primam": he '
     'claims the production of a certain act, and (lays down) three searches for it, the first ... "Licet", the commissioners '
     '"brought in by the Starost" and "praetendit" are plain; two words before stay in doubt'),
    ('0182_b1', 'nomine Magnifici Chełmki secunda[s?] coram actis Castrensia Costenensia', 'nomine Magnifici Chełmski secundam coram actis Castrensibus Costenensibus',
     'the scan has "secundam coram actis Castren Costen" with marks of abbreviation'),
    ('0182_b1', 'tertia coram actis Castren~ Coninen~', 'tertiam coram actis Castren~ Coninen~', 'as "primam" and "secundam"'),
    ('0182_b1', 'factas reponitas Actusque Eundem Campestres Co[m?]porta[m?] praetensas in actis proprii Palatinatus [n/r?]e[?]tasse probat',
     'factas reponendo Actumque Eundem Campestrem Comportari praetensum in actis proprii Palatinatus non extasse probat',
     'the scan has "reponendo actumque Eundem Campestrem Comportari praetensum ... non extasse probat": laying the searches '
     'down, he proves that the field act whose production is claimed was NOT in the records of its own province'),
    ('0182_b1', 'eliberando[?] se a praetensa comportatione Requis[?] per Generosum Ludovicum [T?]anski nomine partes cujus in[s?]e[?]it '
                'Decreti Commissoriales Granitiales',
     'eliberando se a praetensa comportatione Requisitionem per Generosum Ludovicum [T?]anski nomine partis cujus interest '
     'Decreti Commissorialis Granitialis',
     'the scan has "Requisitm ... nne Partis Cujus interest Decreti Commissorialis Granitialis": a search for the decree, made '
     'in the name of the party concerned'),
    ('0182_b1', 'nowy wsi et Ł[ukom??]', 'nowy wsi et Łu[kom]', 'the page ends "et Łu"; the word is finished on the other page'),
    ('0182_b2', 'coram actis Castren[??] Bresten~ [c?]u[p?][u?][r?][ae?] se~ 10 mensis [prae…?] 8bris anno praesen~ facta et actis Castrensibus '
                'Coninensibus die 1[6?] mensis Ejusdem anno itidem praesen~ oblatuata erronee extradita',
     'coram actis Castrensibus Bresten~ Cujaviae Die 10 mensis praesentis 8bris anno praesen~ factam et actis Castrensibus '
     'Coninensibus die 16 mensis Ejusdem anno itidem praesen~ oblatuatam Data~ erronee extraditam',
     'the scan has "Bresten Cujaviae Die 10 mensis praesentis 8bris ... factam ... Die 16 ... oblatuatam Data erronee '
     'extraditam": the search was made at Brześć in Kuyavia on 10 October and entered at Konin on the 16th'),
    ('0182_b2', 'Brestensibus cuju[i?]s[iae?] oblatuatum', 'Brestensibus Cujaviae oblatuatum', 'the scan has "Cujaviae"'),
    ('0182_b2', 'in proprio Palatinatus oblatam porrigi Debent Id eo Decernit [?][uis?] Quatenus',
     'in proprio Palatinatu oblatam porrigi Debent Ideo Decernit Judicium Quatenus',
     'the scan has "in Proprio Palatinatu ... Ideo Decernit Judm" with a mark of abbreviation'),
]

PAGES = [
    # leaf 182 verso
    'No. 16: Between the Right Honourable Stanisław Chełmski, heir of the estates of Łukomia with their appurtenances, '
    'Plaintiff, through Melchior Krzyzanowski, and the Right Honourable Antoni Prusimski, Starost of Niszczewice, cited, in '
    'person — the Court, deciding the term of the Plaintiff party brought before it, the controversies having been heard:\n\n'
    'Although the Right Honourable Chełmski [uncertain: by this term] claims from the Right Honourable Prusimski the '
    'production of a certain act, as though a Boundary act, issued between the estates of Łukom and Trąbczyn by '
    'Commissioners designated by the Estates of the Realm and brought in by the Right Honourable Starost; and, laying before '
    'the court three searches for that same Boundary act — the first made before the records of the Kalisz Municipal Court '
    'on the Saturday after the Feast of the Presentation of the Most Glorious Virgin Mary in the year 1776, through the '
    'Right Honourable Antoni Mierzejewski in the name of the Right Honourable Chełmski; the second before the records of the '
    'Kościan Municipal Court on the 2nd day of the month of January, through the Honourable Antoni Smoliński likewise in the '
    'name of the Right Honourable Chełmski; the third before the records of the Konin Municipal Court on the 28th day of '
    'the month of October in the present year, by the Right Honourable Chełmski alone — proves that the said field act, '
    'whose production is claimed, was not in the records of its proper palatinate;\n\n'
    'the Right Honourable Prusimski, Starost of Niszczewice, for his part, freeing himself from the production claimed, '
    '[lays down] a search, made through the Honourable Ludwik [uncertain: Łański] in the name of the party concerned, for '
    'the Commissorial Boundary Decree issued between the hereditary estates of the villages of Trąbczyn Minus, or Nowa Wieś, '
    'and Łukom\n\n'
    '[uncertain: under no. 15, on the other page]',
    # leaf 182 recto, foot
    'and Drzewce — a search made before the records of the Municipal Court of Brest in Kuyavia on the 10th day of the '
    'present month of October in the present year, and entered as an oblata in the records of the Konin Municipal Court on '
    'the 16th day of the same month in the present year likewise, [uncertain: its date wrongly given out] — and shows that '
    'this Commissorial Decree was entered as an oblata under the act of Tuesday after the Feast of Saint Matthew, Apostle '
    'and Evangelist, in the past year 1776, before the records of the Municipal Court of Brest in Kuyavia.\n\n'
    'Since, however, rights, all settlements, and decrees ought to be submitted by oblata in their own palatinate — the '
    'Court therefore decrees that the Right Honourable Prusimski, Starost of Niszczewice, shall submit the Decree specified '
    'above by way of oblata to the records of the Konin Municipal Court within the space of four weeks from the present '
    'act, under penalty of outlawry in case of contravention, to be published before those same records.',
]


def english():
    return {1: PAGES}


S = {
 1: ('Dekret des Landgerichts in Konin aus der Sitzung, die am 20. Oktober 1777 begann, Eintrag Nr. 16. Stanisław Chełmski, Erbherr von Łukomia, verlangt als Kläger von Antoni Prusimski, Starost von Niszczewice, die Vorlage eines Akts, der wie ein Grenzakt zwischen den Gütern Łukom und Trąbczyn von Kommissaren der Stände erlassen worden sei. Er legt drei Nachsuchen vor, in Kalisz vom Samstag nach Mariä Opferung 1776, in Kościan vom 2. Januar und in Konin vom Oktober des laufenden Jahres, und beweist damit, dass der Akt nicht in den Akten der eigenen Woiwodschaft steht. Prusimski legt seinerseits eine Nachsuche vor, die am 10. Oktober 1777 beim Burggericht Brześć Kujawski vorgenommen und am 16. Oktober in Konin eingetragen wurde, und zeigt, dass das Dekret der Kommission 1776 in Brześć Kujawski eingetragen worden ist. Weil Rechte, Vergleiche und Dekrete in der eigenen Woiwodschaft vorzulegen sind, verpflichtet das Gericht Prusimski, das Dekret binnen vier Wochen bei den Burgakten in Konin eintragen zu lassen, bei Strafe der Acht. Die Lesung beruht auf einem Mikrofilm und ist an mehreren Stellen unsicher.',
     'A decree of the land court at Konin, of the sitting that opened on 20 October 1777, entry no. 16. Stanisław Chełmski, heir of Łukomia, as plaintiff demands of Antoni Prusimski, Starost of Niszczewice, the production of an act said to have been given, as though a boundary act, between the estates of Łukom and Trąbczyn by commissioners of the Estates. He lays down three searches, at Kalisz of the Saturday after the Presentation of the Virgin 1776, at Kościan of 2 January and at Konin of October of the current year, and proves by them that the act is not in the records of its own province. Prusimski for his part lays down a search made at the castle court of Brześć Kujawski on 10 October 1777 and entered at Konin on 16 October, and shows that the commission\'s decree was entered at Brześć Kujawski in 1776. Because rights, settlements and decrees are to be brought in in their own province, the court orders Prusimski to have the decree entered in the castle records at Konin within four weeks, on pain of outlawry. The reading rests on a microfilm and is uncertain in several places.'),
}
HOW = ('written in the working session from the Latin as read on the microfilm\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
