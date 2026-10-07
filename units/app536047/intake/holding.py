# -*- coding: utf-8 -*-
"""APP 53/6/0/-/47: from the editor's scans and texts to the edition.

    python units/app536047/intake/holding.py [--crop] [--sheet] [--write] [--correct] [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

A book of decrees of the land court of Kalisz sitting at Konin, 1781 to
1791. The editor has three frames of a microfilm, each an opening, and
transcribed one entry: no. 26 of the sitting that opened on 20 October 1783.
The entry fills leaf 239 verso and leaf 240 (248.jpg) and, for want of room,
ends on leaf 236 verso, under entry no. 22 (245.jpg, left); the clerk wrote
"Videatur Continuatio sub No 22do" at the foot of leaf 240 and "Continuatio
ex No 26to" over the end. The editor's file has the last part under
"[236v]".

The edition keeps a document's pages in the order of their names, so the
three pages are named in reading order and not by the usual rule (as for
53/6/0/-/46): 0240_b1 is leaf 239 verso, 0240_b2 leaf 240 recto, 0240_b3
leaf 236 verso. The right half of 245.jpg (leaf 237 recto) is set apart.
306.jpg (leaves 295 verso and 296) has entry no. 43 of the sitting of May
1784, between the same parties; the editor's file has only its leaf mark
and the heading of that sitting, with no text. It is not used.

The heading of the sitting of October 1783 is on leaf 213, which is not
among the scans. The editor transcribed it; it dates the entry
(rulings.yml) and is quoted on the holding's page, and is not part of the
document.

What read_source does to the editor's file beyond cutting it:
- the clerk's two directions are added where they stand (DIRECTION,
  CONTINUATION).

The check (2026-10-07). The whole entry was read against the microfilm,
enlarged. ROWS has what was corrected; a line the transcription had skipped
on leaf 239 verso is restored. Left as the editor has them: "[T/F?]eromski"
(the first letter is the clerk's T; no such name is known to me),
"procuratorem" (the scan has "procurat~m", which could be "procuratorium", a
power of attorney), "ex monte", "gasam". The last sentence, from "in
Cancellaria", has pen lines drawn along its two lines of writing; they are
taken for the rule that closes the entry and not for a deletion, since the
sentence cannot end without those words.

The English is the editor's own. FIXES are the places where it followed a
reading that was corrected. Its "[T.N.]" marks and notes are the editor's
apparatus and are left out (courtbook.read_english); most discussed
readings that are now settled.

Entry no. 43 (document 2, added 2026-10-07 at the editor's word). 306.jpg is
leaves 295 verso and 296: entry no. 43 of the sitting that opened on 3 May
1784 (heading on leaf 273, in the editor's file; not among the scans). The
editor's file has no text of it. It was transcribed from the film, enlarged
(NO43A, NO43B), and translated in the editor's terms (EN43A, EN43B). It is
in the clearer of the two hands. Marked as doubtful: the first letter of
"[K?]rolikowa", "ex [o?]re", the abbreviations left with a tilde ("Terr~",
"praeven~", "Condescens~"), the end of "subjic[it]" at the edge of the
page, and the first of the three letters at the close, "[S?]PK". The fold
of 306.jpg (1741) is set by eye: the editor has not placed it.

Seen while reading it, and not followed up: the proxy who is "[T/F?]eromski"
in document 1 is written "Zeromski" here, twice, plainly; and the penalty
is "medium Vadii Capitalis", half of a capital bail, where document 1 has
"Capit~" read as the Starost's.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app536047'
REF = 'APP 53/6/0/-/47'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Decreta [protocollon] 1781-1791 (53.6.0.-.47)"

# (file, x of the fold, left page, right page). First proposals, set by eye;
# the editor's saved folds (folds.json beside this file) are used instead
# where they exist.
SCANS = [
    ('245.jpg', 1734, '0240_b3', '0237_a2'),
    ('248.jpg', 1750, '0240_b1', '0240_b2'),
    ('306.jpg', 1741, '0296_a1', '0296_a2'),
]
SKIP = ('0237_a2',)
LEAF = {'0240_b1': '239 verso', '0240_b2': '240 recto', '0240_b3': '236 verso', '0237_a2': '237 recto',
        '0296_a1': '295 verso', '0296_a2': '296 recto'}
DOCS = [(1, ['0240_b1', '0240_b2', '0240_b3']), (2, ['0296_a1', '0296_a2'])]
FOLD_NOTE = ('All three frames are shown. The first document is read in this order: the left and the right half of '
             '248.jpg, then the left half of 245.jpg. The second is on both halves of 306.jpg.')

DIRECTION = 'Videatur Continuatio sub No 22do'
CONTINUATION = 'Continuatio ex No 26to.'


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Latin).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == [('213', 1), ('239v', 1), ('240', 2), ('236v', 1), ('273', 1), ('295v', 0)], leaves
    L = dict(leaves)
    return {(1, '0240_b1'): L['239v'], (1, '0240_b2'): L['240'] + [DIRECTION], (1, '0240_b3'): [CONTINUATION] + L['236v']}


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0240_b1', 'ad objectam Condescensionem in fundo', 'ad objectam Condemnationem in fundo',
     'the film has "Cond~nem": condemnationem. It is the condemnation "obtentam et publicatam" at Grab, which the Tribunal\'s decree '
     'of 1782 names in the same words (APP 53/17/0/-/Konin Gr.153)'),
    ('0240_b1', 'Decreto Tribunalis obtentam', 'Decreto Tribunalitio obtentam', 'the word is added in the margin: "Triblio"'),
    ('0240_b1', 'censet et quoniam [n~?]d[a/o?]cet Imo moderamini Judicii sui se subiecet proinde',
     'censet et quoniam reproducit Ideo Teneri Illustrem M. Prusimski docere de Loco Standi adinvenit Et quoniam non docet Imo '
     'moderamini Judicii sui se subiicit proinde',
     'a line was skipped between the first "et quoniam" and the second: the film has "et quoniam reproducit Ideo Teneri Illrem M. '
     'Prusimski docere de Loco Standi adinvenit Et quoniam n~ docet"; and "se subiicit", in the present'),
    ('0240_b1', 'loci standi medius vadii', 'loci standi medium vadii', 'the film has "medium"'),
    ('0240_b1', 'per mediu[s?] in instanti', 'per medium in instanti', 'the film has "per medi|um" over the line end'),
    ('0240_b1', 'in experiment[o?] s[i?] quidem', 'in experimento siquidem', 'the film has "in experimento si|quidem"'),
    ('0240_b1', 'Termini Partes Actoreae et manifestationem utrarum', 'Termini Partis Actoreae et manifestationum utrarum',
     'the film has "Partis" and "ma~onum" with a mark: the plaintiff\'s citation and the protests of both parties'),
    ('0240_b1', 'praeciis conscribendas et abi[n/r?][?]ie[s?] super incorrupt[o?] testium',
     'praeciis conscribendis et ab invicem communicandis Interrogatoriis ac praestando super incorrupto testium',
     'the film has "Conscribendis et ab invicem Communicandis Interrogatoriis ac praestando super incorrupto": two words were passed over'),
    ('0240_b1', 'statuitionem In[?]tpator[um?] Termino', 'statuitionem Inculpatorum Termino',
     'the film has "Inculpator~": the production of the accused named in the plaintiff\'s citation'),
    ('0240_b2', 'Juramenthus super incorrupto testium Judicialiter praestiterun[t?]', 'Juramenthum super incorrupto testium Judicialiter praestiterunt',
     'the film has "Juramenthum" and "praestiterunt"'),
    ('0240_b2', 'Hollandos hoscem et ad Magnificum', 'Hollandos hoscemet ad Magnificum', 'one word on the film: hoscemet, these very ones'),
    ('0240_b2', 'au[f?]ugisse', 'aufugisse', 'the word is plain on the film'),
    ('0240_b2', 'prolatum famulum', 'praefatum famulum', 'the film has "p~fatum": the aforesaid servant'),
    ('0240_b2', 'superiusdescr[ipt?]a', 'superiusdescripta', 'the film has "superiusdescr~a" with a mark'),
    ('0240_b3', '[b?]iv[ic?] et ab actu', 'hinc et ab actu', 'the film has "hinc et ab actu": from now and from this act'),
    ('0240_b3', 'ad praesens [?]ductas in', 'ad praesens eductas in', 'the film has "eductas": the inquiries now conducted'),
    ('0240_b3', 'declarat D [R?] Robore', 'declarat D P Robore', 'two capital letters before "Robore", the second a P: the closing formula "Decreti Praesentis Robore"'),
]

FIXES = [
    ('inasmuch as he did not forestall the arrest, on the part of the Right Honourable Chełmski, of the Laboriosi Józef the Coachman and Walenty the Under-coachman, nor has he',
     'that the arrest on the part of the Right Honourable Chełmski did not reach the Laboriosi Józef the Coachman and Walenty the Under-coachman, nor has he',
     '"Arestum ex parte Magnifici Chełmski non praevenit": the arrest is the subject, as in "aresto praeventi non extitere" just before, and in the protest of Prusimski (Konin Gr.119, document 7)'),
    ('regarding the objected Condescension in the estate of the village of Grab, Monday after',
     'regarding the objected condemnation at the estate of the village of Grab, on Monday after', '"ad objectam Condemnationem"'),
    ('to his advantage, a contravention of the Decree of the Tribunal, obtained and published:',
     "to his advantage, for contravention of the Tribunal's Decree, obtained and published:", '"in lucro contraven~ Decreto Tribunalitio obtentam et publicatam"'),
    ('the Court holds that, for his part, he is bound to produce a proxy [as required] by the objecting party; and since he shows no cause, '
     'but rather shall submit himself to the moderation',
     'the Court holds that a proxy is to be produced on the part of the objecting party; and since he produces one, it therefore finds the '
     'Illustrious Right Honourable Prusimski bound to show his right of standing; and since he does not show it, but rather submits himself '
     'to the moderation', 'the skipped line is restored; "se subiicit"'),
    ('the Parties shall draw up Inquisitions concerning the contents of the Term of the Plaintiff Party and the manifestation of both Parties, '
     'during the continuance of their preceding court sessions, and shall thence conduct and dispatch the same upon the uncorrupted oath of '
     'the witnesses — with a Court Summoner appointed for the pronouncing of the Oath, and for the form of the appointment of the matters '
     'interposed, comprehended within the Term of the Plaintiff Party.',
     'the Parties shall conduct and dispatch Inquisitions concerning the contents of the Term of the Plaintiff Party and the manifests of '
     'both Parties, during the continuance of its court sessions, interrogatories having first been drawn up and communicated to each '
     'other, and the oath on the uncorrupted [state] of the witnesses having been taken — with a Court Summoner appointed for the '
     'pronouncing of the form of the Oath; the production of the accused comprehended within the Term of the Plaintiff Party',
     '"conscribendis et ab invicem communicandis Interrogatoriis ac praestando super incorrupto testium Juramentho educant et expediant"; '
     '"statuitionem Inculpatorum", which the next page\'s first words govern'),
    ('The Court adjourned proceedings until the reading of the Inquisitions.', 'the Court suspends until the reading of the Inquisitions.',
     '"statuitionem Inculpatorum ... ad lectionem inquisitionum Judicium suspendit": one sentence over the page break'),
    ('reported that these Hollanders also belonged to', 'reported that these very Hollanders belonged to', '"hoscemet"'),
    ('the servant, having been released, returned home', 'the aforesaid servant returned home', '"praefatum famulum"'),
    ('Starost of Niszczewice, from the present act, within six weeks', 'Starost of Niszczewice, from now and from the present act, within six weeks',
     '"hinc et ab actu praesenti"'),
    ('But the Inquisitions, at present, the Court holds and declares are to remain in the Chancellery of this place, and to be handed over to '
     'the Parties upon prior Acquittance.',
     'But the Inquisitions now conducted the Court holds and declares are to remain in the Chancellery of this place, and to be handed over '
     'to the Parties upon prior Acquittance, [by force of the present decree].', '"eductas"; "D P Robore"'),
]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [(l, len(p)) for l, p in leaves] == [('213', 1), ('239v', 1), ('240', 2), ('236v', 1)], leaves
    E = courtbook.fix_english({l: p for l, p in leaves}, FIXES)
    j = '\n\n'.join
    return {1: [j(E['239v']), j(E['240'] + ['See the continuation under No. 22.']), j(['Continuation of No. 26.'] + E['236v'])]}


S = {1: ('Dekret des Kalischer Landgerichts in Konin von 1783, Eintrag Nr. 26 seiner Sitzung, zwischen Stanisław Chełmski, Schatzmeister des Landes Wschowa, als Kläger und Antoni Prusimski von Kolno, Starost von Niszczewice, als Geladenem. Chełmski hält Prusimski eine Verurteilung entgegen, die er 1780 beim Ortstermin auf dem Gut Grab wegen Verstoßes gegen ein Tribunalsdekret gegen ihn erwirkt hat. Prusimski weist sein Recht, gehört zu werden, nicht nach und unterwirft sich dem Ermessen des Gerichts; es legt ihm eine Geldbuße auf, lässt ihn zur Sache zu und ordnet Verhöre beeideter Zeugen an, weil es um Gewalttaten geht. Aus den Verhören ergibt sich: Leute vom Hof Prusimskis aus Trąbczyn kamen, vom Weg abgeirrt, zur Wüstung Smoleniec, die zu Chełmskis Erbgut Łukom gehört, ließen sich den Weg zeigen und fragten den Olęder Jan Kłonica, wem das Dorf gehöre. Als Kłonica sagte, diese Olęder gehörten Chełmski, schalt ihn Prusimskis Unterkutscher einen Lügner und schlug ihn mit der Peitsche; der Kutscher schlug ihn mit einem Kiefernstock, der dabei zerbrach, und der Unterkutscher schrie, man solle ihn totschlagen; Kłonica floh in ein Erlengehölz. Die Leute wandten sich darauf zum Haus des Olęders, holten dort gewaltsam einen Knecht, schlugen ihn und schlugen ihn weiter auf dem Weg zum Krug von Tomice; er kam erst am folgenden Tag nach Hause. Ein Zeuge beschwerte sich noch am selben Tag bei Prusimski, der denselben Weg kam; Prusimski versprach, die Sache zu Hause zu bereinigen. Die Taten geschahen auf Chełmskis eigenem Grund; ob mit Wissen oder auf Befehl Prusimskis, klären die Verhöre nicht, und Kutscher und Unterkutscher sind in Trąbczyn nicht zu finden. Beschuldigt sind nach den Verhören nur der Kutscher Józef und der Unterkutscher Walenty; Prusimski erklärt, er könne sie nicht stellen, und bietet einen Reinigungseid an. Das Gericht legt ihm auf, binnen sechs Wochen vor dem Burgamt Konin zu beschwören, dass der von Chełmski erwirkte Arrest die beiden nicht erreicht hat und er sie nicht stellen kann, bei Strafe der Verbannung. Die Verhörprotokolle bleiben in der Kanzlei und werden den Parteien gegen Quittung herausgegeben.',
     "A decree of the Kalisz land court at Konin of 1783, entry no. 26 of its sitting, between Stanisław Chełmski, Treasurer of the land of Wschowa, as plaintiff, and Antoni Prusimski of Kolno, Starost of Niszczewice, as the party cited. Chełmski raises against Prusimski a condemnation that he obtained against him in 1780, at the sitting on the ground at the estate of Grab, for breach of a Tribunal decree. Prusimski does not show his right to be heard and submits to the court's discretion; it lays a money penalty on him, admits him to the cause, and orders examinations of sworn witnesses, because the cause concerns acts of violence. The examinations show: men of Prusimski's household from Trąbczyn, having strayed from their road, came to the deserted settlement of Smoleniec, which belongs to Chełmski's hereditary estate of Łukom, had the way shown to them, and asked the Olęder settler Jan Kłonica whose village it was. When Kłonica said that these settlers belonged to Chełmski, Prusimski's under-coachman called him a liar and struck him with a whip; the coachman beat him with a pine stick, which broke, and the under-coachman shouted that he should be struck dead; Kłonica fled into an alder grove. The men then turned to the settler's house, took a servant from it by force, beat him, and went on beating him on the way to the tavern of Tomice; he came home only the next day. A witness complained the same day to Prusimski, who came along the same road; Prusimski promised to put the matter right at home. The acts were done on Chełmski's own ground; whether with Prusimski's knowledge or at his order the examinations do not show, and the coachman and under-coachman are not to be found at Trąbczyn. By the examinations only the coachman Józef and the under-coachman Walenty are accused; Prusimski declares that he cannot produce them and offers an oath to clear himself. The court orders him to swear within six weeks before the castle office at Konin that the arrest Chełmski obtained did not reach the two men and that he cannot produce them, on pain of banishment. The records of the examinations stay in the chancery and are given out to the parties against a receipt.")}
HOW = ('written in the working session from the Latin as checked\n# (intake/holding.py, 2026-10-07).')

# Entry no. 43, document 2: transcribed and translated in the working session (see the docstring).
NO43A = "No. 43tio Inter Illustrem Magnificum Michaelem Drogosław Skorzewski Succamerarium Terr~ Posnaniensis Insignium Sancti Stanislai et Sanctae Annae Equitem, Bonorum Biskupie seu Bystrzyca haeredem Actorem et Citatum per Generosum Josephum Stablewski Magnificum Stanislaum Ścibor Chełmski Thesaurarium Vschovensem Bonorum Łukomia et Łomowa haeredem Citatum et Actorem per Generosum Constantinum Suchodolski Illustrem Magnificum Franciscum Comitem de Stadniki Stadnicki Capitaneum Ostrzeszoviensem Insignis Sancti Stanislai equitem Bonorum [K?]rolikowa Bialla, et Lądek tum Successores olim Magnificae Theresiae de Wężyki cum eodem Illustri Magnifico Stadnicki procreatos Bonorum Suprascriptorum haeredes et possessores Citatos per Generosum Antonium Miroszewski Illustrem Magnificum Prusimski Capitaneum Nieszczevicensem Insignis Sancti Stanislai Equitem Bonorum Trąpczyna cum attinentiis haeredem Citatum per Generosum Albertum Żeromski Ad Objectam Condemnationem in Termino Condescensionis in Fundo Bonorum Villae Grab die Undecima mensis Septembris Anno 1780 agitatae ex [o?]re Magnifici Chełmski Thesaurarii Vschovensis super Illustri Magnifico Prusimski Capitaneo Nieszczevicensi in lucro contraventionis Decreto Tribunalitio Obtentam et publicatam teneri producere ad Objiciendam Condemnationem a Magnifico Chełmski Objicientem procuratorium Judicium censet, Et quoniam procuratorium Feria quinta post Dominicam Cantate Anno 1783tio coram Actis Castrensibus Pyzdrensibus factum reponitur proinde Sufficienti procuratorio adinvento decernit Judicium quatenus Is Idem Illustris Magnificus Prusimski Capitaneus Nieszczevicensis de loco standi doceat instantanee et quoniam non docet Imo se moderamini Judicii Sui subjic[it]"
NO43B = "ideo in Constitutionem Sibi loci standi Solvat parti objicienti salva apud eandem repetitione reservata medium Vadii Capitalis Judicio vero medium medii Vadii in instanti sub paena bannitionis in determinatione Judiciorum publicanda Interea habere eundem locum Standi Judicium declarat, et Experimentum demandat, in Experimento Terminos partium decidendo et Controversiis earundem exauditis Quoniam Partes pro dislimitatione Bonorum Biskupice seu Bystrzyca cum Bonis Łomowa seu Łukom mutuo se, praesens ad Judicium conveniunt proinde in Ordine dislimitationis Bonorum eorundem necessariam esse Condescensionem ad Campum in Fundum Controversum Inter praeallegata Bona in et pro die 16ta mensis Julii in anno praesenti proxime ventura adinvenit, Sententiando quatenus Partes pro Termino suprascripto Illustrem Magnificum Succamerarium Districtus Calissiensis aut ejus Officium Campestre impetrent, quo vero ad Causam Violentiarum et damnorum Judicium suum Unius duorumve Absentia non obstante aut unum ex Generosis Camerariis legitime praeven~ pro eodem Termino conducant, Quod sive qui Condescens~ de violentiis damnis Inquiret Et Juramenta excipiet Bonificationem cui a quo et quanta provenerit praestandam decernet Et Inquisitiones expediet Terminos praefiget rigores annectet, Causamque praesentem ad Contenta Terminorum et Manifestationum Partium decidet disjudicabit et moderabitur Quorum decisioni et quidem ad Causam Granitialem Illustris Magnifici Succamerarii quo vero ad Causam Facti Judicii sui aut Generosorum Camerariorum sub paena bannitionis super Parte Contraveniente illo in Termino coram eisdem Condescensionis publicanda parere et acquiescere debebunt ac tenebuntur Luita paena quatuordecim Marcarum pollonicalium Parti per Partem compensanda Judicio vero suo per medium ab utraque Parte sub Solito ex Regestro paenalium extendendo rigore solvenda Pro quo Condescensionis Termino Partes quos negotium exigerit tum et Collaterales Adcitent Adcitati sub Suprascripta paena bannitionis Compareant [S?]PK."
EN43A = "No. 43: Between the Illustrious Right Honourable Michał Drogosław Skórzewski, Sub-chamberlain of Poznań, Knight of the Orders of Saint Stanislaus and Saint Anne, heir of the estates of Biskupie or Bystrzyca, Plaintiff and Cited, through the Honourable Józef Stablewski; the Right Honourable Stanisław Ścibor Chełmski, Treasurer of Wschowa, heir of the estates of Łukomia and Łomowa, Cited and Plaintiff, through the Honourable Konstanty Suchodolski; the Illustrious Right Honourable Franciszek, Count of Stadniki, Stadnicki, Starost of Ostrzeszów, Knight of the Order of Saint Stanislaus, [heir] of the estates of [uncertain: Królików], Biała and Lądek, and the successors of the late Right Honourable Teresa, born Wężyk, begotten with the same Illustrious Right Honourable Stadnicki, heirs and possessors of the above-written estates, Cited, through the Honourable Antoni Miroszewski; [and] the Illustrious Right Honourable Prusimski, Starost of Niszczewice, Knight of the Order of Saint Stanislaus, heir of the estates of Trąbczyn with appurtenances, Cited, through the Honourable Wojciech Żeromski —\n\nregarding the objected condemnation, obtained and published at the condescension term held on the ground of the estates of the village of Grab on the eleventh day of the month of September in the year 1780, [uncertain: on the part] of the Right Honourable Chełmski, Treasurer of Wschowa, against the Illustrious Right Honourable Prusimski, Starost of Niszczewice, to his advantage, for contravention of the Tribunal's Decree: the Court holds that the party objecting on behalf of the Right Honourable Chełmski is bound to produce a proxy in order to object the condemnation. And since a proxy made before the records of the Pyzdry Municipal Court on Thursday after Cantate Sunday in the year 1783 is laid down, a sufficient proxy being therefore found, the Court decrees that the same Illustrious Right Honourable Prusimski, Starost of Niszczewice, shall show his right of standing forthwith; and since he does not show it, but rather submits himself to the moderation of its judgement,"
EN43B = "therefore, for the establishment of his right of standing, he shall pay: to the objecting party, with recovery from the same reserved, half of a capital bail; but to the Court half of a half bail, forthwith, under penalty of banishment, to be published at the close of the sessions. Meanwhile the Court declares that he has the right of standing, and orders the trial.\n\nIn the trial, deciding the terms of the parties, and their controversies having been heard: since the parties bring one another before the present Court for the delimitation of the estates of Biskupice or Bystrzyca from the estates of Łomowa or Łukom, the Court therefore finds that, for the delimitation of those estates, a condescension to the field, on the disputed ground between the aforesaid estates, is necessary, on and for the 16th day of the month of July next coming in the present year — ruling that the parties shall obtain for the above-written term the Illustrious Right Honourable Sub-chamberlain of the District of Kalisz, or his field office; but, as to the cause of the acts of violence and damages, shall bring for the same term its own Court, the absence of one or two notwithstanding, or one of the Honourable Boundary Surveyors [two words not fully read: \"legitime praeven~\"]. Which court, or he who comes to the condescension, shall inquire into the acts of violence and damages, and shall receive oaths; shall decree the compensation to be made, to whom, by whom and how much shall be due; and shall conduct inquisitions, fix terms, attach rigours, and shall decide, adjudge and moderate the present cause according to the contents of the parties' terms and manifests. Whose decision — as to the boundary cause, that of the Illustrious Right Honourable Sub-chamberlain; as to the cause of fact, that of its own Court or of the Honourable Boundary Surveyors — they shall be bound and obliged to obey and acquiesce in, under penalty of banishment, to be published upon the contravening party at that term, before the same [judges] of the condescension. The penalty of fourteen Polish marks having been paid — to be set off party against party, and to its own Court paid by halves by each party, under the usual rigour, to be extended from the register of penalties. For which condescension term the parties shall cite those whom the matter requires, and also the neighbours; those cited shall appear under the above-written penalty of banishment."
_source1, _english1 = read_source, english


def read_source():
    d = _source1()
    d[(2, '0296_a1')] = [NO43A]
    d[(2, '0296_a2')] = [NO43B]
    return d


def english():
    d = _english1()
    d[2] = [EN43A, EN43B]
    return d


S[2] = ("Dekret des Kalischer Landgerichts in Konin, Eintrag Nr. 43 der Sitzung, die am 3. Mai 1784 begann. Parteien sind Michał Drogosław Skórzewski, Unterkämmerer von Posen und Erbherr von Biskupie oder Bystrzyca, und Stanisław Ścibor Chełmski, Schatzmeister von Wschowa und Erbherr von Łukomia und Łomowa, jeder zugleich Kläger und Geladener; mit ihnen geladen sind Franciszek Stadnicki, Starost von Ostrzeszów, samt seinen Kindern mit der verstorbenen Teresa, geborene Wężyk, und Prusimski, Starost von Niszczewice und Erbherr von Trąbczyn. Prusimski wird die Verurteilung entgegengehalten, die Chełmski beim Ortstermin in Grab am 11. September 1780 wegen Zuwiderhandlung gegen das Tribunalsdekret erwirkt hat. Eine am Donnerstag nach Cantate 1783 in Pyzdry ausgestellte Vollmacht wird als ausreichend befunden; Prusimski weist sein Recht, gehört zu werden, nicht nach und unterwirft sich dem Gericht, das ihn gegen Zahlung einer halben Buße an die Gegenseite und einer Viertelbuße an das Gericht zulässt. Zur Sache: Weil die Parteien einander wegen der Abgrenzung von Biskupice oder Bystrzyca gegen Łomowa oder Łukom vor Gericht gebracht haben, hält das Gericht einen Ortstermin auf dem strittigen Grund für nötig, am 16. Juli des laufenden Jahres. Für die Grenze sollen die Parteien den Unterkämmerer des Kalischer Distrikts oder sein Feldamt gewinnen; für die Gewalttaten und Schäden sollen sie das Gericht selbst oder einen der Kämmerer beiziehen, der untersuchen, Eide abnehmen und den Ersatz festsetzen soll. Die Parteien haben bei Strafe der Verbannung zu gehorchen und auch die Anrainer zu laden.",
        "A decree of the land court of Kalisz sitting at Konin, entry no. 43 of the sitting that opened on 3 May 1784. The parties are Michał Drogosław Skórzewski, sub-chamberlain of Poznań and heir of Biskupie or Bystrzyca, and Stanisław Ścibor Chełmski, Treasurer of Wschowa and heir of Łukomia and Łomowa, each both plaintiff and cited; cited with them are Franciszek Stadnicki, Starost of Ostrzeszów, with his children by the late Teresa, born Wężyk, and Prusimski, Starost of Niszczewice and heir of Trąbczyn. Against Prusimski the condemnation is raised that Chełmski obtained at the sitting on the ground at Grab on 11 September 1780 for contravention of the Tribunal's decree. A power of attorney made at Pyzdry on the Thursday after Cantate Sunday 1783 is found sufficient; Prusimski does not show his right to be heard and submits to the court, which admits him on payment of half a penalty to the other side and a quarter to the court. On the cause itself: because the parties have brought each other before the court over the boundary between Biskupice or Bystrzyca and Łomowa or Łukom, the court finds a sitting on the disputed ground necessary, on 16 July of the current year. For the boundary the parties are to obtain the sub-chamberlain of the district of Kalisz or his field office; for the acts of violence and the damage they are to bring the court itself or one of the chamberlains, who is to inquire, take oaths and fix the compensation. The parties are to obey on pain of banishment and to cite the neighbours too.")

if __name__ == '__main__':
    courtbook.holding_main(globals())
