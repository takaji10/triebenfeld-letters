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

Entry no. 17 (document 2, added 2026-10-07 at the editor's word). It stands
on leaf 183 recto, the right half of 193.jpg (page 0183_a2), and is the next
entry of the same sitting, between the same parties. The editor's file has a
first reading of it under "[182v] N. 16to", with more than forty marks of
doubt and no English. It was transcribed again from the film, enlarged, with
the editor's reading beside it (NO17), and translated in the editor's terms
(EN17). Three words are marked as doubtful: the town of the merchant
Tracholz ("Vit[k?]ovien~"), "initi[?]" and the two abbreviations left with a
tilde. A word struck out before "Pyzdrensibus" is not transcribed (the
ruling of 2026-10-05). The day of the hearing reads "Laetare"; the citation
to that hearing in Konin Gr.117 (document 1) has "Invocavit". Not resolved.
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
SKIP = ('0182_a1',)
LEAF = {'0182_a1': '181 verso', '0182_b2': '182 recto', '0182_b1': '182 verso', '0183_a2': '183 recto'}
DOCS = [(1, ['0182_b1', '0182_b2']), (2, ['0183_a2'])]
FOLD_NOTE = ('Entry no. 16 begins on the left page of the second scan and ends at the foot of the right page of the first; entry no. 17 '
             'is on the right page of the second. '
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

# Entry no. 17, document 2: transcribed and translated in the working session (see the docstring).
NO17 = "N. 17mo Inter Eundem Actorem per Eundem et Eundem Citatum personaliter Judicium etc. Terminum Partis Actoreae ad Judicium suum editum Decidendo controversiis exauditis Licet si Magnificus Stanislaus Chełmski virtute transfusionis coram actis Castrensibus Pyzdrensibus Feria 4ta in Vigilia Festi Nativitatis Beatissimae Virginis Mariae anno 1768 per Excellentem Joannem Tracholz mercatorem et Incolam Vit[k?]ovien~ super summas varias ab olim Magnifico Paulo Prusimski praetensas in Personam Ejusdem Magnifici Chełmski recognitae actoratum Magnifico Prusimski Capitaneo Nieszczevicen~ instituendo Comportationem contractus respectu Divenditionis Borrae Trąbczynen~ cum honorato Tracholz et olim M. Paulum Prusimski initi[?] praetendit Cum vero Judicio suo Deducitur Decretum in anteactis Judiciis suis Feria 2da post Dominicam Septuagesimae anno 1766 Inter honoratum Joannem Tracholz et M. Antonium Prusimski modernum Citatum remissionis causae ad Terminum Condescensionis intercessisse et non effectuatum esse proinde suspenso toto negotio necessariam esse Condescensionem in Fundum Bonorum Trąbczyn affectan~ Partibus Judicii sui In et pro Feria 2da post Dominicam Laetare Quadragesimalem in anno futuro venturam adinvenit Decernendo Quatenus Partes hoc Idem Judicium absentia Duorum uniusve non obstante Conducant Quod sive Qui Conducendus Comportationem contractus superius specificati per M. Prusimski Capitaneum Nieszczevicen~ demandabit Causamque praesentem pro exigentia Legis Justitiae nexus Documentorum contenta Partis actoreae Terminorum resolutis quibusvis dubiis et Intervenien~ finaliter decidet et disjudicabit satisfactionem cui quanta et a quo intererit Decernet Inquisitiones pro oportunitate negotii expediet Juramenta ubi necesse fuerit et a quo intererit excipiet rigores annectet. Cujus Judicii Condescensuri Partes parere et acquiescere sub paena banitionis coram Eodem Conducendo Judice super Parte contraveniente In casu contraventionis publicanda debebunt et tenebuntur. Luita paena 14 marcarum Polonicalium Parti per Partem compensanda Judicio in instanti sub solito rigore per medium solvenda pro quo Condescensionis Termino Partes quos negotium exigent adcitent adcitati sub rigore suprascripto compareant."
EN17 = "No. 17: Between the same Plaintiff, through the same, and the same Cited, in person — the Court, etc., deciding the term of the Plaintiff party brought before it, the controversies having been heard:\n\nAlthough the Right Honourable Stanisław Chełmski — by virtue of a transfer, acknowledged before the records of the Pyzdry Municipal Court on Wednesday, the Eve of the Feast of the Nativity of the Most Blessed Virgin Mary, in the year 1768 by the Excellent Jan Tracholz, merchant and inhabitant of [a town: the name is not surely read], of various sums claimed from the late Right Honourable Paweł Prusimski, into the person of the same Right Honourable Chełmski — instituting a suit against the Right Honourable Prusimski, Starost of Niszczewice, claims the production of the contract concerning the sale of the Trąbczyn pine forest entered into with the Honest Tracholz and the late Right Honourable Paweł Prusimski;\n\nsince, however, it is shown to the Court that in its earlier sessions, on Monday after Septuagesima Sunday in the year 1766, a decree of remission of the cause to a condescension term had intervened between the Honest Jan Tracholz and the Right Honourable Antoni Prusimski, the present Cited, and has not been carried out: the Court therefore, the whole matter being suspended, finds a condescension of its court to the ground of the estates of Trąbczyn to be necessary, the parties requesting it, on and for the Monday after Laetare Sunday in Lent next coming in the coming year — decreeing that the parties shall bring this same court, the absence of two or of one notwithstanding; which court, or he who is to be brought, shall order the production of the contract specified above by the Right Honourable Prusimski, Starost of Niszczewice, and shall finally decide and adjudge the present cause as law, justice, the tenor of the documents and the contents of the Plaintiff party's terms require, all doubts and interventions being resolved; shall decree satisfaction, to whom, how much and from whom it shall be due; shall conduct inquisitions as the matter requires; shall receive oaths where necessary and from whom it shall be due; and shall attach rigours.\n\nThe parties shall be bound and obliged to obey and to acquiesce in that court of the condescension, under penalty of outlawry, to be published before the same judge who is to be brought, upon the contravening party in case of contravention. The penalty of fourteen Polish marks having been paid — to be set off party against party, and paid to the Court forthwith, under the usual rigour, by halves. For which condescension term the parties shall cite those whom the matter requires; those cited shall appear under the rigour written above."
_source1, _english1 = read_source, english


def read_source():
    d = _source1()
    d[(2, '0183_a2')] = [NO17]
    return d


def english():
    d = _english1()
    d[2] = [EN17]
    return d


S[2] = ("Dekret des Kalischer Landgerichts in Konin, Eintrag Nr. 17 der Sitzung, die am 20. Oktober 1777 begann, zwischen denselben Parteien wie der Eintrag davor: dem Kläger und dem Geladenen, der persönlich erschienen ist. Stanisław Chełmski klagt aus einer Übertragung, die am Mittwoch, dem Vorabend von Mariä Geburt 1768, vor dem Burggericht Pyzdry anerkannt wurde: Der Kaufmann Jan Tracholz hat ihm darin verschiedene Summen abgetreten, die er vom verstorbenen Paweł Prusimski forderte. Chełmski verlangt, dass Prusimski, Starost von Niszczewice, den Vertrag über den Verkauf des Trąbczyner Kiefernwaldes vorlegt, der mit Tracholz und Paweł Prusimski geschlossen wurde. Dem Gericht wird nachgewiesen, dass ein Dekret seiner früheren Sitzung vom Montag nach Septuagesima 1766 zwischen Tracholz und Antoni Prusimski die Sache auf einen Ortstermin verwiesen hat und dass es nicht ausgeführt worden ist. Das Gericht setzt deshalb die ganze Sache aus und hält auf Antrag der Parteien einen Ortstermin des Gerichts auf dem Grund von Trąbczyn für nötig, am Montag nach Laetare des kommenden Jahres. Der Richter, der dorthin geholt wird, soll Prusimski die Vorlage des Vertrags auferlegen, die Sache endgültig entscheiden, Zeugen verhören und Eide abnehmen. Die Parteien haben ihm bei Strafe der Acht zu gehorchen und zu laden, wen die Sache erfordert.",
        "A decree of the land court of Kalisz sitting at Konin, entry no. 17 of the sitting that opened on 20 October 1777, between the same parties as the entry before it: the plaintiff and the man cited, who has appeared in person. Stanisław Chełmski sues under a transfer acknowledged before the castle court of Pyzdry on the Wednesday, the eve of the Nativity of the Virgin, 1768: by it the merchant Jan Tracholz made over to him various sums that he claimed from the late Paweł Prusimski. Chełmski demands that Prusimski, Starost of Niszczewice, produce the contract for the sale of the Trąbczyn pine wood that was made with Tracholz and Paweł Prusimski. It is shown to the court that a decree of its earlier sitting, of the Monday after Septuagesima Sunday 1766, between Tracholz and Antoni Prusimski, had sent the cause to a sitting on the ground, and that it has not been carried out. The court therefore suspends the whole matter and, at the parties' request, finds a sitting of the court on the ground of Trąbczyn necessary, on the Monday after Laetare Sunday of the coming year. The judge who is brought there is to order Prusimski to produce the contract, decide the cause finally, hold inquiries and take oaths. The parties are to obey him on pain of outlawry and to cite whom the matter requires.")

if __name__ == '__main__':
    courtbook.holding_main(globals())
