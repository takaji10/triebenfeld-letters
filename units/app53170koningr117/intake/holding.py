# -*- coding: utf-8 -*-
"""APP 53/17/0/-/Konin Gr.117: from the editor's scans and texts to the edition.

    python units/app53170koningr117/intake/holding.py [--crop] [--sheet] [--write] [--correct]
                                                     [--english] [--cache] [--summaries]

The steps are courtbook.holding_main's (pipeline/intake/courtbook.py). This
file is the record of what was done to this holding.

The book is the register of the castle court of Konin for 1778 and 1779, the
volume after Konin Gr.116: each sitting under a line "Actum in Conin ...".
The editor photographed fifteen openings and transcribed the entries that
concern Trąbczyn. Each entry is a document (docs/PRUSIMSKI_ERA_PLAN.md).

Documents 2 and 3 share leaf 54 verso, and there the note of the protest
(3) stands above the report (2). They are numbered the other way because
the protest runs on to leaf 55, and the pages of the corpus must follow one
another: a page can be shared only by neighbouring documents.

    doc  leaf            scan       page       what
    1    35              039        0035_a2    report: Chełmski's citation of Prusimski to the sitting on
                                               the ground (7 March 1778)
    2    54v             059        0055_a1    report: Prusimski's citations to the Tribunal (30 March 1778)
    3    54v, 55, 55v    059, 060   0055_a1,   Prusimski's protest against Chełmski and the land court:
                                    0055_a2,   the note on 54v and its text "ex opposito" on leaf 55
                                    0056_a1    (March 1778)
    4    57v             062        0058_a1    Chełmski's protest against the act of Prusimski's
                                               commissioners (April 1778)
    5    58              062        0058_a2    Chełmski's protest "against Sokołowski" (April 1778)
    6    58v             063        0059_a1    report: a boundary pine cut down (April 1778)
    7    71, 71v         075, 076   0071_a2,   Prusimski's protest against Chełmski and the sub-judge
                                    0072_a1    (15 April 1778)
    8    72, 72v         076, 077   0072_a2,   report: Prusimski's second citations to the Tribunal
                                    0073_a1    (15 April 1778)
    9    78, 78v         082, 083   0078_a2,   report: Chełmski's citation of Prusimski to the land
                                    0079_a1    court (25 April 1778)
    10   82v             087        0083_a1    note: the decree of remission brought in (1778)
    11   272             253        0272_a2    report: pines cut by subjects of Rzgów, their axes shown
                                               (29 January 1779)
    12   359, 359v       340, 341   0359_a2,   Nosalski's protest (1 May 1779)
                                    0360_a1
    13   507v            489        0508_a1    note: Prusimski's protest against the Nosalskis (1779)

The scans are photographs named by their number in a series, not by leaf.
Leaf numbers were read off the pages: 039 is leaves 34v|35, 059 is 54v|55,
060 is 55v|56, 062 is 57v|58, 063 is 58v|59, 075 is 70v|71, 076 is 71v|72,
077 is 72v|73, 082 is 77v|78, 083 is 78v|79, 087 is 82v|83, 253 is 271v|272,
340 is 358v|359, 341 is 359v|360, 489 is 507v|508. Page ids: leaf N recto is
<N>_a2, leaf N verso is <N+1>_a1. Twelve halves carry nothing transcribed
and are set apart. The folds were set by eye; they are first proposals for
the editor.

What read_source does to the editor's file beyond cutting it:
- Chełmski's signature is added under his two protests (leaves 57 verso and
  58), where it stands on the scan (SIGN).

Not on the photographed pages: the text "ex Opposito Sub signo #" that the
note on leaf 82 verso points to (the top of leaf 83 is the end of another
entry); the heading of Chełmski's protest on leaf 57 verso, which begins
under a space barred with pen strokes and signed by him, with the words "in
vim Diligentiae" above its first line.

The check (2026-10-07) was the light one the plan sets for the long
holdings. Read against the scans, enlarged: every heading and date line; the
names of the judges in documents 2 and 8; and, word for word, five of the
eighteen pages: leaf 35 (document 1), leaf 58 verso (6), leaf 272 (11) and
leaves 359 and 359 verso (12). ROWS has what was corrected. The long Latin
of documents 2, 3, 4, 5, 7, 8 and 9 was NOT read through; it stands as the
editor has it, with its marks of doubt, apart from the names and from one
word: "Patrui", the uncle's, which the editor read "Patrii" or "Patris"
(seen on leaf 55, written "Patruj", three times; corrected on the same
ground in the twelve other places, which were not each looked at).

The English is the editor's own. FIXES are the places where it followed a
reading that was corrected. "father" was the English of "Patrii": all
fifteen are made "uncle" (english()).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app53170koningr117'
REF = 'APP 53/17/0/-/Konin Gr.117'
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes [protocollon] 1778-1779 (53.17.0.-.Konin Gr.117)"

# (file, x of the fold, left page, right page). First proposals, set by eye;
# the editor's saved folds (folds.json beside this file) are used instead
# where they exist.
SCANS = [
    ('039.jpg', 2166, '0035_a1', '0035_a2'),
    ('059.jpg', 2174, '0055_a1', '0055_a2'),
    ('060.jpg', 2174, '0056_a1', '0056_a2'),
    ('062.jpg', 2174, '0058_a1', '0058_a2'),
    ('063.jpg', 2174, '0059_a1', '0059_a2'),
    ('075.jpg', 2174, '0071_a1', '0071_a2'),
    ('076.jpg', 2184, '0072_a1', '0072_a2'),
    ('077.jpg', 2184, '0073_a1', '0073_a2'),
    ('082.jpg', 2180, '0078_a1', '0078_a2'),
    ('083.jpg', 2184, '0079_a1', '0079_a2'),
    ('087.jpg', 2184, '0083_a1', '0083_a2'),
    ('253.jpg', 2150, '0272_a1', '0272_a2'),
    ('340.jpg', 2108, '0359_a1', '0359_a2'),
    ('341.jpg', 2150, '0360_a1', '0360_a2'),
    ('489.jpg', 2068, '0508_a1', '0508_a2'),
]
SKIP = ('0035_a1', '0056_a2', '0059_a2', '0071_a1', '0073_a2', '0078_a1', '0079_a2', '0083_a2', '0272_a1', '0359_a1',
        '0360_a2', '0508_a2')
LEAF = {'0035_a1': '34 verso', '0035_a2': '35 recto', '0055_a1': '54 verso', '0055_a2': '55 recto',
        '0056_a1': '55 verso', '0056_a2': '56 recto', '0058_a1': '57 verso', '0058_a2': '58 recto',
        '0059_a1': '58 verso', '0059_a2': '59 recto', '0071_a1': '70 verso', '0071_a2': '71 recto',
        '0072_a1': '71 verso', '0072_a2': '72 recto', '0073_a1': '72 verso', '0073_a2': '73 recto',
        '0078_a1': '77 verso', '0078_a2': '78 recto', '0079_a1': '78 verso', '0079_a2': '79 recto',
        '0083_a1': '82 verso', '0083_a2': '83 recto', '0272_a1': '271 verso', '0272_a2': '272 recto',
        '0359_a1': '358 verso', '0359_a2': '359 recto', '0360_a1': '359 verso', '0360_a2': '360 recto',
        '0508_a1': '507 verso', '0508_a2': '508 recto'}
DOCS = [(1, ['0035_a2']), (2, ['0055_a1']), (3, ['0055_a1', '0055_a2', '0056_a1']), (4, ['0058_a1']), (5, ['0058_a2']),
        (6, ['0059_a1']), (7, ['0071_a2', '0072_a1']), (8, ['0072_a2', '0073_a1']), (9, ['0078_a2', '0079_a1']),
        (10, ['0083_a1']), (11, ['0272_a2']), (12, ['0359_a2', '0360_a1']), (13, ['0508_a1'])]
FOLD_NOTE = ('All fifteen scans are shown. On three, both halves are pages of the edition; on twelve, one half is a page '
             'and the other is left out.')

SIGN = 'Stanisław Scibor Chełmski'
COUNTS = [('35', 3), ('54v', 6), ('55', 2), ('55v', 1), ('57v', 1), ('58', 2), ('58v', 2), ('71', 4), ('71v', 2), ('72', 2),
          ('72v', 1), ('78', 2), ('78v', 1), ('82v', 2), ('272', 3), ('359', 2), ('359v', 2), ('507v', 2)]


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(Original).md'))
    assert len(f) == 1, f
    pre, leaves = courtbook.read_leaves(f[0])
    assert not pre, pre
    assert [(l, len(p)) for l, p in leaves] == COUNTS, [(l, len(p)) for l, p in leaves]
    L = dict(leaves)
    return {
        (1, '0035_a2'): L['35'],
        (2, '0055_a1'): L['54v'][3:],
        (3, '0055_a1'): L['54v'][:3],
        (3, '0055_a2'): L['55'],
        (3, '0056_a1'): L['55v'],
        (4, '0058_a1'): L['57v'] + [SIGN],
        (5, '0058_a2'): L['58'] + [SIGN],
        (6, '0059_a1'): L['58v'],
        (7, '0071_a2'): L['71'],
        (7, '0072_a1'): L['71v'],
        (8, '0072_a2'): L['72'],
        (8, '0073_a1'): L['72v'],
        (9, '0078_a2'): L['78'],
        (9, '0079_a1'): L['78v'],
        (10, '0083_a1'): L['82v'],
        (11, '0272_a2'): L['272'],
        (12, '0359_a2'): L['359'],
        (12, '0360_a1'): L['359v'],
        (13, '0508_a1'): L['507v'],
    }


UNCLE = ('the word is "Patrui", the uncle\'s: written "Patruj" where it was looked at on leaf 55, and the same protest has '
         '"Patruum" and "Patruo" of Paweł Prusimski; not "Patrii" or "Patris"')

# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0035_a2', 'Sanus [habens?] Recognovit[?] de Citt~', 'Sanus existens Recognovit se Citt~',
     'the scan has "Sanus" with "exns" written above the line, then "Recogt se Citt": the set phrase of the other reports'),
    ('0035_a2', 'de bonis [s?]uis mandamus', 'de bonis Tuis mandamus', 'the scan has "Tuis": the King addresses Prusimski'),
    ('0035_a2', 'in Decreti Terrestris Calissiensis', 'vi Decreti Terrestris Calissiensis', 'the scan has "vi": by force of the decree'),
    ('0035_a2', 'Elaps[u?]o Lati', 'Elapso Lati', 'the word is plain on the scan'),
    ('0035_a2', 'ac perem[?] p[t/l?]one Compareas', 'ac peremptorie Compareas', 'the scan has "perem|ptone" over the line end with a mark: peremptorie'),
    ('0035_a2', 'Qui se citatum seu potius', 'Qui Te Citat seu potius', 'the scan has "Qui Te Citat": who cites you'),
    ('0035_a2', 'Quatenus [s?]u in Termino', 'Quatenus Tu in Termino', 'the scan has "Tu"'),
    ('0035_a2', 'de bonis suis Subditos qui praesent[e?] Cittone~ apud se Arestant statim proquibus',
     'de bonis Tuis Subditos qui praesenti Cittone~ apud Te Arestantur Statuas proquibus',
     'the scan has "Tuis", "apud Te Arestant" with a mark, and "Statuas": that you produce your subjects, who by this '
     'citation are arrested in your keeping'),
    ('0055_a1', 'Nieszczevicen[sei?] [?] termino[?] M. Stanislaum', 'Nieszczevicen~ contra M. Stanislaum',
     'the scan has "Nieszczevicen" with a mark and "ctra": contra'),
    ('0055_a1', 'factu Manifestatio ex opposito Insuta.', 'facta Manifestatio ex opposito Inserta.', 'the scan has "facta" and "Inserta"'),
    ('0055_a1', 'contra MM. Chełmskiego Judicium Terreste Calissien[i?] ad Tribl[?]',
     'contra MM. Chełmski et Judicium Terrestre Calissien~ ad Tribunal Relatio',
     'the heading has "c. MM. Chełmski et Judm Trrle Calis. ad Tribl Relao"'),
    ('0055_a1', 'Francisco Morzyz[?] Wallenow[la?] Judici', 'Francisco Wierusz Walknowski Judici',
     'the scan has "Wierusz Walknowski": the judge of the land court named in the heading of the sitting of October 1777 (APP 53/6/0/-/46)'),
    ('0055_a1', 'Xaverio Miliorzlu[?] Notario Terrestribus Calissiens[i?] Causa Infrascriptae Judicibus Nostri Ordinarii Tribunalis '
     'Regni Petricoviens[i?] ac[?] data et positione praesentii',
     'Xaverio Mikorski Notario Terrestribus Calissiens[i?] Causae Infrascriptae Judicibus Gravaminosis De persona bonis ac Officio '
     'Vestris mandamus ut in Judiciis Nostris Ordinariis Tribunalis Regni Petricoviens[i?] a data et positione praesentis',
     'the scan has "Mikorski", and after "Judicibus" the words "Gravaminosis De persona bonis ac Officio Vestris mandamus ut in '
     'Judiciis", which the transcription passed over'),
    ('0055_a1', 'Relictae olim Patrii Acto~ factae', 'Relictae olim Patrui Acto~ factae', UNCLE),
    ('0055_a2', 'Relictae Patrii suc haerentibus', 'Relictae Patrui Sui haerentibus', UNCLE + '; the scan has "Sui"'),
    ('0055_a2', 'substantiam Patrii Sui necessariis', 'substantiam Patrui Sui necessariis', UNCLE),
    ('0055_a2', 'Relictae viduae Patris sui designato', 'Relictae viduae Patrui sui designato', UNCLE),
    ('0055_a2', 'Successoribus Relictae Patrii sui Commissio', 'Successoribus Relictae Patrui sui Commissio', UNCLE),
    ('0056_a1', 'relictae Patris sui Manifestantis', 'relictae Patrui sui Manifestantis', UNCLE),
    ('0056_a1', 'Relictae Patris sui Emanatis', 'Relictae Patrui sui Emanatis', UNCLE),
    ('0059_a1', 'na Granicy Dobr [T?]urnata Trąmpczyna Widział sosnę od Lat Kilku dziesiąt na Kopcu Granicznym zwanym Trąmpczyn',
     'na Granicy Dobr Trąmpczyna Widział sosnę od Lat Kilku dziesiąt na Kopcu [T?]urnata zwanym Granicznym Trąmpczyn',
     'the name and "zwanym" are written above the line, with marks that put them after "Kopcu": the mound called so; the '
     'name itself is left as the editor read it'),
    ('0071_a2', 'Prusimski Patriissui Manifestationis', 'Prusimski Patrui sui Manifestationis', UNCLE),
    ('0071_a2', 'universalem Patrii Sui Spectantum', 'universalem Patrui Sui Spectantum', UNCLE),
    ('0072_a1', 'Viduae Patriis Sui post', 'Viduae Patrui Sui post', UNCLE),
    ('0072_a2', 'Francisco Wieriss[?] Wallinoryki[?] Jud[?]a[i?] Stephano', 'Francisco Wierusz Walknowski Judici Stephano',
     'the scan has "Francisco Wierusz Walknowski Judici"'),
    ('0072_a2', 'Causae Judicio Xaverio [?]nilierski[?] Notario', 'Causae Judici Xaverio Mikorski Notario',
     'the scan has "Judici Xaverio Mikorski": Zielonacki is the sub-judge "and also judge" at the sitting on the ground; '
     'Mikorski the notary'),
    ('0072_a2', 'Successoribus Relictae Patrii Actoris cum olim', 'Successoribus Relictae Patrui Actoris cum olim', UNCLE),
    ('0072_a2', 'Ejusdem Relictae Patrii Actoris post Fata', 'Ejusdem Relictae Patrui Actoris post Fata', UNCLE),
    ('0072_a2', 'decessum tam Patrii Actoris quam', 'decessum tam Patrui Actoris quam', UNCLE),
    ('0072_a2', 'Successoribus Relictae Patrii Actoris Nempe', 'Successoribus Relictae Patrui Actoris Nempe', UNCLE),
    ('0072_a2', 'universalem Patrii Actoris spectantium', 'universalem Patrui Actoris spectantium', UNCLE),
    ('0078_a2', 'pro quidem Terrestribus Calissiens[ibus?]', 'pro Judiciis Terrestribus Calissiens[ibus?]', 'the scan has "pro Judijs Trribus"'),
    ('0272_a2', 'Recognovit qu[?]sio Ipse', 'Recognovit Quia Ipse', 'the scan has "Quia Ipse", the set phrase'),
    ('0272_a2', 'Offorand[um?] Requisitionem', 'Officiosam Requisitionem', 'the scan has "offosam" with a mark: officiosam'),
    ('0272_a2', 'zas La[?] kopcami', 'zas za kopcami', 'the scan has "za" written above the line: beyond the mounds'),
    ('0272_a2', 'poddanych pozunanych', 'poddanych pozcinanych', 'the scan has "pozcinanych": cut down'),
    ('0272_a2', 'Idem [v/r?]orlis eidem officio, praesentavit Secures in numero vig[o?]nti[?] Die superius Ea[pp?]a in Fundo',
     'Idem Ministerialis eidem officio, praesentavit Secures in numero viginti Die superius Expressa in Fundo',
     'the scan has "Mnlis" with a mark, "viginti" and "Exppa" with a mark: expressa'),
    ('0272_a2', 'pinaticis facientibus Intercepto', 'pinaticis fugientibus Interceptas',
     'the scan has "fugientibus Interceptas": the axes taken from the subjects as they fled with the pines'),
    ('0272_a2', 'et de recepit officium', 'et de receptis officium', 'the scan has "de receptis"'),
    ('0359_a2', 'Martinus [P?]alski Thesauranda', 'Martinus Nosalski Thesaurarida',
     'the scan has "Nosalski", as he signs; "Thesaurarida" is the son of a treasurer (skarbnikowicz), the "ri" written like an "n"'),
    ('0359_a2', 'Indemnitti [h?][?]ae ne quomodocunque[?] per depositionem [F/T?]estimonionem[?] ex Labris~',
     'Indemnitati Suae ne quomodocunque per depositionem Testimoniorum ex Laboriosis',
     'the scan has "Indemnitti Suae", "Testimoniorum" and "Labrus" with a mark: Laboriosis, the working men'),
    ('0359_a2', '[prae/pro]juditio[s/r?]um sibi inferre videlicet hanc Actis praesentibus in vini Diligentiae infer[i?]t querimoniam '
     'protestatur que[?] sequenti methodo Extend[u?] Su praesent[e?] [H/L?]abit~ Bartholomaeus',
     'praejudiciosum sibi inferre videatur hanc Actis praesentibus in vim Diligentiae infert querimoniam protestaturque sequenti '
     'methodo Etenim Supra praefati Laboriosi Bartholomaeus',
     'the scan has "videatur" written above the line, "in vim", "infert", "protestaturque", "Etenim Su prafati Labsi"'),
    ('0359_a2', 'auri [h/s?]ant ac [pro/prae]sampserunt[?] hominibus', 'ausi sunt ac praesumpserunt hominibus', 'the scan has "ausi sunt ac praesumpserunt"'),
    ('0360_a1', 'manif[?]tis de Sylvi Magnifici Chełmski haereditari[s?]s in [T?]ra[b?]ibus arboris vechen~ in via publica iter '
     '[pro/prae?]pedire. Eosdem Conditere ac Converberare [s?]ed bonaque Trąpczyn cum Trachibus adducere',
     'manifestantis de Sylvis Magnifici Chełmski haereditariis in Trahibus arbores vehentibus in via publica iter praepedire. '
     'Eosque Concutere ac Converberare ad bonaque Trąpczyn cum Trahibus adducere',
     'the scan has "in Trahibus arbores vehen" and "cum Trahibus": on sledges ("traha"), not beams; and "Eosque Concutere", "ad bonaque"'),
    ('0360_a1', 'in Complicitatem Facte intrate', 'in Complicitatem Facti intrare', 'the scan has "Facti intrare"'),
    ('0360_a1', 'paenas insetrahere non', 'paenas in se trahere non', 'written as one word on the scan: in se trahere, to draw upon themselves'),
    ('0360_a1', 'violenttarum Executoris', 'violentiarum Executores', 'the scan has "violentiarum Executores"'),
    ('0360_a1', 'per Ipsosmet peractis omnimoda Inquisitione deductiorum a per hibendoque hac in Causa Testimonio relegatarum '
     'Complicitatemque delicti S[e/c]orsivis punitis probaturum',
     'per Ipsosmet peractas omnimoda Inquisitione deducturum a perhibendoque hac in Causa Testimonio relegaturum '
     'Complicitatemque delicti Seorsivis punctis probaturum',
     'the scan has "peractas", "deducturum", "a perhibendoque ... Testimonio relegaturum" and "Seorsivis punctis": he will '
     'have them shut out from giving testimony and prove their complicity in separate points'),
    ('0508_a1', 'Contra Magnificis Wisalskie fact[o?]', 'Contra Magnificos Nosalskie facta', 'the scan has "Contra Mcos Nosalskie facta"'),
    ('0508_a1', 'Antoni Prusimski Star. Nieszczewicz', 'Antoni Prusimski Star: Nieszczewski', 'the signature ends "Nieszczewski"'),
]

FIXES = [
    ('regarding his estates we command', 'regarding your estates we command', '"de bonis Tuis"'),
    ('who, having presented himself as cited, or rather adhering to this prepared decree, cites you',
     'who cites you, or rather summons you to this prepared decree', '"Qui Te Citat seu potius ad paratum hocce Decretum adcitat"'),
    ('and to the effect that, insofar as you — in that same condescension term fixed and arising in the estates of Trąmpczyn — '
     'hold under arrest at their place forthwith upon the present citation the laboring subjects of his estates, namely: '
     'Albert Livoy, Andrzej Rataj, Kazimierz the Keeper, and Albert the Shepherd of Nowawieś;',
     'and to the effect that you — at that same condescension term fixed and arising in the estates of Trąmpczyn — produce '
     'the laboring subjects of your estates, who by the present citation are placed under arrest in your keeping, namely: '
     'Albert Livoy, Andrzej Rataj, Kazimierz the Keeper, and Albert the Shepherd of Nowawieś;',
     '"Quatenus Tu ... Laboriosos ... de bonis Tuis Subditos qui praesenti Citatione apud Te Arestantur Statuas": that you produce them'),
    (', [at the] [term] against the Honourable Stanisław Chełmski', ', against the Honourable Stanisław Chełmski', '"contra"'),
    ('Franciszek Morzyz of Wallenowla, Judge', 'Franciszek Wierusz Walknowski, Judge', '"Francisco Wierusz Walknowski Judici"'),
    ('Xawery Miliorzlu, Notary of the Kalisz Land Court — judges in the cause described below — of our Ordinary Crown Tribunal '
     'of the Realm at Piotrków: from the date',
     'Xawery Mikorski, Notary of the Kalisz Land Court — the judges complained of in the cause described below: regarding '
     'your persons, goods and office we command that in our Ordinary Courts of the Crown Tribunal of the Realm at Piotrków, '
     'from the date',
     '"Mikorski"; "Judicibus Gravaminosis De persona bonis ac Officio Vestris mandamus ut in Judiciis Nostris Ordinariis '
     'Tribunalis", words the transcription had passed over'),
    ('belonging to it, you are to appear in person and peremptorily, at the instance', 'belonging to it, you appear in person '
     'and peremptorily, at the instance', 'the sentence now runs on from "we command that"'),
    ("a right for which not the manifestant's late uncle but Chełmski himself had stood as debtor to the uncle",
     "to whom the manifestant's late uncle had not been debtor, but who had himself been debtor to the uncle",
     '"cui non olim Patruus Manifestantis sed Ipse Patruo Debitor Extitit": "cui" and "Ipse" are Tracholz, as the second '
     'citation says (sums "contracted by Tracholz and owed to" the uncle)'),
    ('being on the boundary of the estates of [uncertain: T]urnata and Trąmpczyn, he saw a pine tree — grown over several '
     'decades on the boundary mound known as dividing Trąmpczyn from Biskupia —',
     'being on the boundary of the estates of Trąmpczyn, he saw a pine tree — grown over several decades on the boundary '
     'mound called [uncertain: T]urnata, dividing Trąmpczyn from Biskupia —',
     'the name and "zwanym" are written above the line and belong after "Kopcu"'),
    ('Franciszek Wieriss of Wallinoryki, Judge; Stefan Zielonacki, Deputy Judge; and also the Condescension Court judge in the '
     'condescension term of the cause described below; and Xawery [?]nilierski, Notary',
     'Franciszek Wierusz Walknowski, Judge; Stefan Zielonacki, Deputy Judge and also judge at the condescension term of the '
     'cause described below; and Xawery Mikorski, Notary',
     '"Stephano Zielonacki Subjudici et etiam in Termino Condescensionis Infrascriptae Causae Judici Xaverio Mikorski Notario": '
     'the judge at the condescension is Zielonacki himself'),
    ('acknowledged the authenticated citation letter, indeed issued for the Kalisz Land Court sessions',
     'acknowledged the authenticated citation letter, issued for the Kalisz Land Court sessions', '"pro Judiciis", not "pro quidem"'),
    ('more — [felled] by people, subjects of the estates of Rzgów, recognised as such —',
     'more, cut down by people, subjects of the estates of Rzgów —', '"pozcinanych", cut down'),
    ('from those same subjects of the estates of Rzgów, at night-time, in the act of [felling] the aforesaid pine trees',
     'from those same subjects of the estates of Rzgów as they fled at night-time with the aforesaid pine trees',
     '"cum praemissis Arboribus pinaticis fugientibus Interceptas"'),
    ('The Honourable Nożalski — manifests by way of diligence', 'The Honourable Nosalski — manifests by way of diligence',
     'he signs "Nosalski"; the clerk wrote "Nozalski" in the heading'),
    ('the Honourable Marcin Nożalski, Thesaurarius [Treasurer] of Czernichów, hereditary owner',
     'the Honourable Marcin Nosalski, son of the Treasurer of Czernihów, hereditary owner',
     '"Thesaurarida Czerniechoviensis": skarbnikowicz czernihowski, the son of a holder of that titular office'),
    ('by means of testimony to be given from the lips of Bartłomiej Szepczyński and Mateusz Wąchnicki',
     'by means of testimony to be given by the labouring men Bartłomiej Szepczyński and Mateusz Wąchnicki', '"ex Laboriosis", not "ex labris"'),
    ('That Bartłomiej Szepczyński and Mateusz Wąchnicki, executing', 'That the aforesaid labouring men Bartłomiej Szepczyński '
     'and Mateusz Wąchnicki, executing', '"Etenim Supra praefati Laboriosi"'),
    ('as they were carrying timber from the hereditary woodland', 'as they were carting trees on sledges from the hereditary woodland',
     '"in Trahibus arbores vehentibus"'),
    ('seizing and beating those same [people]; bringing them to the estates of Trąmpczyn together with the timber;',
     'striking and beating those same [people]; bringing them to the estates of Trąmpczyn together with the sledges;',
     '"Eosque Concutere ac Converberare ad bonaque Trąpczyn cum Trahibus adducere"'),
    ('they did not blush to inflict penalties [on them].', 'they did not blush to draw the penalties wholly upon themselves.',
     '"omnino paenas in se trahere non Erubuerunt"'),
    ('offers that he will wish to prove the aforesaid acts of violence committed by them in person — through a full sworn '
     'inquiry of witnesses to be adduced and cited to give testimony in this cause — and the complicity in the offence, each '
     'to be punished separately;',
     'offers to establish the aforesaid acts of violence committed by them in person through a full sworn inquiry, to have '
     'them shut out from giving testimony in this cause, and to prove their complicity in the offence in separate points;',
     '"omnimoda Inquisitione deducturum a perhibendoque hac in Causa Testimonio relegaturum Complicitatemque delicti '
     'Seorsivis punctis probaturum"'),
    ('Martinus Nożalski', 'Martinus Nosalski', 'as he signs'),
    ('against the Honourables Wisalski', 'against the Honourables Nosalski', '"Contra Magnificos Nosalskie"'),
]
SIGN_EN = 'Stanisław Ścibor Chełmski'
COUNTS_EN = [('35', 5), ('54v', 10), ('55', 4), ('55v', 4), ('57v', 4), ('58', 5), ('58v', 4), ('71', 5), ('71v', 6), ('72', 7),
             ('72v', 2), ('78', 3), ('78v', 3), ('82v', 2), ('272', 5), ('359', 3), ('359v', 4), ('507v', 2)]


def english():
    f = glob.glob(os.path.join(glob.escape(RAW), '*(English).md'))
    assert len(f) == 1, f
    leaves = courtbook.read_english(f[0])
    assert [(l, len(p)) for l, p in leaves] == COUNTS_EN, [(l, len(p)) for l, p in leaves]
    # "Patrui", read as "Patrii", had become "father" in the English: Paweł Prusimski is the uncle
    n = sum(x.count('father') for _, p in leaves for x in p)
    assert n == 15, n
    L = courtbook.fix_english({l: [x.replace('father', 'uncle') for x in p] for l, p in leaves}, FIXES)
    j = '\n\n'.join
    return {
        1: [j(L['35'])],
        2: [j(L['54v'][3:])],
        3: [j(L['54v'][:3]), j(L['55']), j(L['55v'])],
        4: [j(L['57v'] + [SIGN_EN])],
        5: [j(L['58'] + [SIGN_EN])],
        6: [j(L['58v'])],
        7: [j(L['71']), j(L['71v'])],
        8: [j(L['72']), j(L['72v'])],
        9: [j(L['78']), j(L['78v'])],
        10: [j(L['82v'])],
        11: [j(L['272'])],
        12: [j(L['359']), j(L['359v'])],
        13: [j(L['507v'])],
    }


S = {
 1: ('Bericht des Gerichtsboten Jan Jankowski von Łukom vom 7. März 1778. Er hat Antoni Prusimski von Kolno, Starost von Niszczewice und Erbherr von Trąbczyn, eine königliche Ladung zugestellt: Prusimski soll zu dem Ortstermin (condescensio) erscheinen, den das Kalischer Landgericht in Konin mit seinem Dekret vom Montag nach St. Hedwig des Vorjahres angeordnet hat und der auf den Montag nach Invocavit auf dem Grund von Trąbczyn angesetzt ist, auf Betreiben von Stanisław Ścibor Chełmski, Erbherr von Łukom, als Kläger. Er soll dazu seine Untertanen Albert Livoy, Andrzej Rataj, Kazimierz den Hüter und Albert den Hirten von Nowa Wieś stellen. Die Ladung ist in Konin am Montag nach St. Matthias 1778 ausgestellt; der Bote hat sie im Gutsamt von Trąbczyn auf den Tisch gelegt.',
     'A report of the court messenger Jan Jankowski of Łukom of 7 March 1778. He has served a royal citation on Antoni Prusimski of Kolno, Starost of Niszczewice and heir of Trąbczyn: Prusimski is to appear at the sitting on the ground (condescensio) that the Kalisz land court at Konin ordered by its decree of the Monday after St Hedwig of the year before, fixed for the Monday after Invocavit Sunday on the ground of Trąbczyn, at the instance of Stanisław Ścibor Chełmski, heir of Łukom, as plaintiff. He is to produce there his subjects Albert Livoy, Andrzej Rataj, Kazimierz the keeper and Albert the shepherd of Nowa Wieś. The citation is dated at Konin on the Monday after St Matthias 1778; the messenger left it on the table in the estate office at Trąbczyn.'),
 3: ('Protest von Antoni Prusimski, Starost von Niszczewice, eingetragen in Konin im März 1778: ein Vermerk mit seiner Unterschrift und, auf dem gegenüberliegenden Blatt, der Text nach einer vorbereiteten Abschrift. Er richtet sich gegen Stanisław Chełmski, Erbherr von Łukom, und gegen die Richter des Kalischer Landgerichts. Chełmski habe von dem Bürger Jan Tracholz eine unrechtmäßige Forderung erworben, die aus einem 1744 mit Prusimskis verstorbenem Onkel Paweł Prusimski geschlossenen Geschäft über Eichenholz stamme, und verfolge sie nun gegen ihn. Ihm fehlten die nötigen Urkunden: Sie lägen bei den Erben der Witwe seines Onkels, und er habe sie eingeklagt, aber noch nicht erhalten. Das Landgericht habe die Sache mit Tracholz früher auf einen Ortstermin mit diesen Erben verwiesen; dennoch sei auf Chełmskis Betreiben ein entgegengesetztes Dekret ergangen, das einen Ortstermin auf dem Grund von Trąbczyn anordnet. Prusimski erklärt dieses Dekret, ergangen in Konin am 20. Oktober des Vorjahres, für nichtig und protestiert gegen die Übertragung der Forderung auf Chełmski.',
     "A protest of Antoni Prusimski, Starost of Niszczewice, entered at Konin in March 1778: a note with his signature and, on the facing leaf, the text from a prepared copy. It is directed against Stanisław Chełmski, heir of Łukom, and against the judges of the Kalisz land court. Chełmski, he says, has acquired from the townsman Jan Tracholz an unlawful claim arising from a contract for oak timber made in 1744 with Prusimski's late uncle Paweł Prusimski, and now pursues it against him. He lacks the papers he needs: they are with the heirs of his uncle's widow, and he has sued for them but not yet received them. The land court had earlier sent the cause with Tracholz to a sitting on the ground with those heirs; yet at Chełmski's instance a contrary decree was given, ordering a sitting on the ground of Trąbczyn. Prusimski declares that decree, given at Konin on 20 October of the year before, null, and protests against the transfer of the claim to Chełmski."),
 2: ('Bericht der Gerichtsboten Bartłomiej Szepczyński von Trąbczyn und Mateusz Matuszkiewicz von Szetlewek vom 30. März 1778. Sie haben zwei Ausfertigungen einer königlichen Ladung vor das Krontribunal in Petrikau zugestellt, ausgestellt in Petrikau am Samstag nach Reminiscere 1778. Geladen sind Stanisław Chełmski, Erbherr von Łukomia, und die Richter des Kalischer Landgerichts: der Richter Franciszek Wierusz Walknowski, der Unterrichter Stefan Zielonacki und der Notar Xawery Mikorski, auf Betreiben Prusimskis. Das Dekret des Landgerichts vom 20. Oktober des Vorjahres, das dem früheren widerspreche, soll aufgehoben und die Sache an das Tribunal verwiesen werden; Prusimski verlangt, von der Forderung befreit zu werden, die Chełmski von Jan Tracholz erworben hat. Eine Ausfertigung wurde in Konin im Haus des Bürgers Palszewicz hinterlegt, die andere im Gutshof von Łukom.',
     "A report of the court messengers Bartłomiej Szepczyński of Trąbczyn and Mateusz Matuszkiewicz of Szetlewek of 30 March 1778. They have served two copies of a royal citation before the Crown Tribunal at Piotrków, dated at Piotrków on the Saturday after Reminiscere Sunday 1778. Cited are Stanisław Chełmski, heir of Łukomia, and the officers of the Kalisz land court: the judge Franciszek Wierusz Walknowski, the sub-judge Stefan Zielonacki and the notary Xawery Mikorski, at Prusimski's instance. The land court's decree of 20 October of the year before, said to contradict its earlier one, is to be lifted and the cause sent to the Tribunal; Prusimski asks to be freed from the claim that Chełmski acquired from Jan Tracholz. One copy was left at Konin in the house of the townsman Palszewicz, the other at the manor of Łukom."),
 4: ('Protest von Stanisław Ścibor Chełmski, Schatzmeister von Wschowa, Erbherr von Łukomia, Łomów, Imielno und Bukowo, eingetragen in Konin im April 1778 und von ihm unterschrieben. Er beruft sich auf das Felddekret, das die von seiner Seite beigezogenen Kommissare 1775 zwischen Łukom und Trąbczyn erlassen haben: gestützt auf Urkunden und namentlich auf die Besichtigung von 1592, am letzten Grenzhügel mit benachbarten Zeugen bekräftigt und rechtzeitig zu den Akten der eigenen Woiwodschaft eingereicht. Dagegen sei die Handlung, die die von Prusimski beigezogenen Kommissare später, nach der Grenzziehung und nach Errichtung der Hügel, privat und mit größter Gunst abgefasst hätten, unrechtmäßig. Prusimski habe sie weder zu den Akten der eigenen Woiwodschaft eingereicht noch ihre Auflagen befolgt und sie damit selbst als ungültig behandelt. Damit sein Schweigen nicht als Anerkennung gelte, erklärt Chełmski sie für ungültig und kündigt an, ihre Aufhebung zu betreiben.',
     'A protest of Stanisław Ścibor Chełmski, Treasurer of Wschowa, heir of Łukomia, Łomów, Imielno and Bukowo, entered at Konin in April 1778 and signed by him. He relies on the field decree that the commissioners brought in on his side gave in 1775 between Łukom and Trąbczyn: resting on documents and in particular on the inspection of 1592, confirmed at the last boundary mound with neighbouring witnesses, and brought in good time to the records of its own province. Against it, he says, the act that the commissioners engaged by Prusimski drew up later, after the boundary had been drawn and the mounds raised, privately and with the greatest favour, is unlawful. Prusimski neither brought it to the records of his own province nor carried out what it prescribed, and so himself treated it as invalid. So that his silence should not pass for acceptance, Chełmski declares it invalid and announces that he will seek to have it quashed.'),
 5: ('Protest von Stanisław Ścibor Chełmski, Schatzmeister von Wschowa, eingetragen in Konin im April 1778 und von ihm unterschrieben; die Überschrift nennt als Gegner einen Sokołowski, den der Text nicht erwähnt. Chełmski nimmt seine früheren Proteste auf: Das Grenzdekret zwischen seinem Łukom und Prusimskis Trąbczyn sei durch die von seiner Seite beigezogenen Kommissare nach der Besichtigung von 1592 und nach zwei Tribunalsdekreten von 1766 und 1768 ergangen, und die Grenzhügel seien errichtet. Prusimskis Kommissare hätten davon gewusst und dennoch ihre Befugnis missbraucht: Sie hätten Albert Czarnecki, Grenzkämmerer von Kalisz, den Prusimski angenommen hatte, die Besichtigung des Grenzzugs, die Errichtung der Hügel und die Abnahme des Eides überlassen. Czarnecki habe das Dekret erst einige Wochen nach der Abreise der Kommissare schreiben lassen. Prusimski habe Eid gegen Eid angeboten und als Mitschwörer einen selbst geladenen Nachbarn, einen Mann aus Czarneckis Dienst, der nie in der Gegend gewesen sei, und andere unbedeutende Leute herangezogen. Chełmski beschuldigt Prusimski all dessen und bietet an, es durch Zeugenverhör zu beweisen.',
     "A protest of Stanisław Ścibor Chełmski, Treasurer of Wschowa, entered at Konin in April 1778 and signed by him; the heading names as his opponent one Sokołowski, whom the text does not mention. Chełmski takes up his earlier protests: the boundary decree between his Łukom and Prusimski's Trąbczyn was given by the commissioners brought in on his side, following the inspection of 1592 and two Tribunal decrees of 1766 and 1768, and the boundary mounds were raised. Prusimski's commissioners knew of this and nonetheless abused their power: they left to Albert Czarnecki, boundary chamberlain of Kalisz, whom Prusimski had engaged, the inspection of the boundary line, the raising of the mounds and the taking of the oath. Czarnecki had the decree written only some weeks after the commissioners had left. Prusimski offered oath against oath and took as fellow-swearers a neighbour who was himself cited, a man in Czarnecki's service who had never been in those parts, and other persons of no account. Chełmski accuses Prusimski of all this and offers to prove it by an inquiry of witnesses."),
 6: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn, eingetragen in Konin im April 1778, für Antoni Prusimski von Kolno, Starost von Niszczewice. Mit zwei Adligen, Piotr Gostarski und Tomasz Jachimowicz, war er am Samstag, dem 21. Februar des laufenden Jahres, an der Grenze von Trąbczyn. Dort sah er, dass eine mehrere Jahrzehnte alte Kiefer auf dem Grenzhügel, der Trąbczyn von Biskupie scheidet, mit drei Kreuzen als Grenzzeichen versehen, gefällt und weggeschafft war, nach seiner Angabe bei Nacht durch Herrn Bogusławski, Erbherrn eines Teils von Kurów.',
     'A report of the court messenger Bartłomiej Szepczyński of Trąbczyn, entered at Konin in April 1778, for Antoni Prusimski of Kolno, Starost of Niszczewice. With two noblemen, Piotr Gostarski and Tomasz Jachimowicz, he was at the boundary of Trąbczyn on Saturday 21 February of the current year. There he saw that a pine several decades old, standing on the boundary mound that divides Trąbczyn from Biskupie and marked with three crosses as boundary signs, had been cut down and carried off, by his account at night by Mr Bogusławski, heir of a part of Kurów.'),
 7: ('Protest von Antoni Prusimski von Kolno, Starost von Niszczewice, vom 15. April 1778, nach einer vorbereiteten Abschrift eingetragen und von ihm unterschrieben. Er richtet sich gegen Stanisław Chełmski und gegen Stefan Zielonacki, Unterrichter des Kalischer Landgerichts, wegen des vollen Landgerichts wie wegen des Ortstermins auf dem Grund von Trąbczyn. Prusimski verweist auf seinen Protest und seine Ladung gegen das Dekret des Landgerichts vom 20. Oktober des Vorjahres. Der Streit um die Herausgabe der Urkunden mit den Erben der Witwe seines Onkels Paweł Prusimski sei beim Tribunal anhängig; ohne diese Urkunden könne über die Forderung, die Chełmski von Jan Tracholz erworben hat, nicht entschieden werden. Der Unterrichter habe die Sache auf Betreiben Chełmskis an das volle Landgericht verwiesen, obwohl dieses vor das Tribunal geladen sei, und Prusimski damit unnütze Kosten verursacht; Prusimski erklärt diese Verweisung für nichtig.',
     "A protest of Antoni Prusimski of Kolno, Starost of Niszczewice, of 15 April 1778, entered from a prepared copy and signed by him. It is directed against Stanisław Chełmski and against Stefan Zielonacki, sub-judge of the Kalisz land court, in respect both of the full land court and of the sitting on the ground of Trąbczyn. Prusimski refers to his protest and his citation against the land court's decree of 20 October of the year before. The suit for the surrender of the papers, against the heirs of the widow of his uncle Paweł Prusimski, is pending before the Tribunal; without those papers the claim that Chełmski acquired from Jan Tracholz cannot be judged. The sub-judge, at Chełmski's instance, sent the cause to the full land court although that court stands cited before the Tribunal, and so caused Prusimski useless costs; Prusimski declares that remission null."),
 8: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 15. April 1778. Er hat drei Ausfertigungen einer königlichen Ladung vor das Krontribunal in Petrikau zugestellt, ausgestellt in Petrikau am Montag nach Laetare 1778: an Stanisław Chełmski, an den Richter Franciszek Wierusz Walknowski, an den Unterrichter Stefan Zielonacki, zugleich Richter des Ortstermins, und an den Notar Xawery Mikorski. Auf Betreiben Prusimskis soll die Sache an das Tribunal verwiesen und das Dekret vom 20. Oktober des Vorjahres aufgehoben werden; sie lasse sich nicht entscheiden ohne die Urkunden, die Prusimski von den Erben der Witwe seines Onkels, Katarzyna Prusimska, geborene Rozdrażewska, zurückfordert. Erweise sich daraus die Forderung von Tracholz und Chełmski als unrechtmäßig, soll die Übertragung aufgehoben werden; ergebe sich vielmehr eine Schuld von Tracholz gegenüber dem Onkel, soll Chełmski sie samt Zinsen zahlen. Die Ausfertigungen wurden in Trąbczyn, in Konin im Haus des Bürgers Paulszewicz, wo die Kanzlei des Landgerichts ihre Akten hat, und im Gutshof von Łukom hinterlegt.',
     "A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 15 April 1778. He has served three copies of a royal citation before the Crown Tribunal at Piotrków, dated at Piotrków on the Monday after Laetare Sunday 1778: on Stanisław Chełmski, on the judge Franciszek Wierusz Walknowski, on the sub-judge Stefan Zielonacki, who was also judge at the sitting on the ground, and on the notary Xawery Mikorski. At Prusimski's instance the cause is to be sent to the Tribunal and the decree of 20 October of the year before lifted; it cannot be decided, he says, without the papers that Prusimski is claiming back from the heirs of his uncle's widow, Katarzyna Prusimska, born Rozdrażewska. If the papers show the claim of Tracholz and Chełmski to be unlawful, the transfer is to be quashed; if they show instead a debt of Tracholz to the uncle, Chełmski is to pay it with interest. The copies were left at Trąbczyn, at Konin in the house of the townsman Paulszewicz, where the chancery of the land court keeps its records, and at the manor of Łukom."),
 9: ('Bericht des Gerichtsboten Jan Jankowski von Łukom, eingetragen in Konin am 25. April 1778. Er hat Antoni Prusimski eine königliche Ladung vor das Kalischer Landgericht in Konin zugestellt, ausgestellt in Kalisz am Karfreitag 1778, auf Betreiben von Stanisław Chełmski, Erbherr von Łukomia. Prusimski soll das Dekret hören, mit dem das Gericht des Ortstermins in Trąbczyn die Sache an das volle Gericht verwiesen hat; Chełmski verlangt, dass ihm die von Jan Tracholz auf ihn übertragene Summe samt Zinsen und Kosten zugesprochen wird. Der Bote hat die Ladung im Gutsamt von Trąbczyn in Gegenwart des Verwalters hinterlegt.',
     'A report of the court messenger Jan Jankowski of Łukom, entered at Konin on 25 April 1778. He has served on Antoni Prusimski a royal citation before the Kalisz land court at Konin, dated at Kalisz on Good Friday 1778, at the instance of Stanisław Chełmski, heir of Łukomia. Prusimski is to hear the decree by which the court of the sitting on the ground at Trąbczyn sent the cause to the full court; Chełmski asks that the sum made over to him by Jan Tracholz be adjudged to him with interest and costs. The messenger left the citation in the estate office at Trąbczyn in the presence of the steward.'),
 10: ('Registervermerk von 1778: Das Dekret, mit dem das Gericht des Ortstermins auf dem Grund von Trąbczyn die Sache zwischen Chełmski und Prusimski, Starost von Niszczewice, verwiesen hat, wird zur Eintragung vorgelegt. Der Vermerk verweist auf einen Text gegenüber unter dem Zeichen #.',
     'A register note of 1778: the decree by which the court of the sitting on the ground of Trąbczyn remitted the cause between Chełmski and Prusimski, Starost of Niszczewice, is brought in for entry. The note points to a text opposite, under the sign #.'),
 11: ('Bericht des Gerichtsboten Bartłomiej Szepczyński von Trąbczyn vom 29. Januar 1779, für Antoni Prusimski von Kolno, Starost von Niszczewice. Mit zwei Adligen war er am 23. des laufenden Monats in den Kiefernwäldern von Trąbczyn: Auf eigenem Trąbczyner Grund zählte er zwölf Stümpfe frisch gefällter Kiefern, hinter und zwischen den Grenzhügeln weitere, nach seiner Angabe von Untertanen des Gutes Rzgów geschlagen. Er legt dem Amt zwanzig Äxte vor, die an jenem Tag auf dem Grund von Szetlewek diesen Untertanen abgenommen wurden, als sie bei Nacht mit den Kiefern flohen, nimmt sie wieder an sich und quittiert dem Amt.',
     "A report of the court messenger Bartłomiej Szepczyński of Trąbczyn of 29 January 1779, for Antoni Prusimski of Kolno, Starost of Niszczewice. With two noblemen he was in the pine woods of Trąbczyn on the 23rd of the current month: on Trąbczyn's own ground he counted twelve stumps of freshly felled pines, and more beyond and between the boundary mounds, cut by his account by subjects of the estate of Rzgów. He lays before the office twenty axes taken that day on the ground of Szetlewek from those subjects as they fled at night with the pines, takes them back, and gives the office a quittance."),
 12: ('Protest von Marcin Nosalski, Erbherr und Besitzer von Rzgów, eingetragen in Konin am 1. Mai 1779 und von ihm unterschrieben. Er legt ihn vorsorglich ein, damit ihm die Aussagen von Bartłomiej Szepczyński und Mateusz Wąchnicki in seiner Sache mit Prusimski vor dem Kalischer Landgericht in Konin nicht schaden. Die beiden hätten auf Befehl von Tomasz Joachimowicz seine Leute, die auf Schlitten Bäume aus den Erbwäldern Chełmskis fuhren, auf öffentlicher Straße angehalten, geschlagen, mit den Schlitten nach Trąbczyn gebracht und ihnen die Äxte mit Gewalt abgenommen. Nosalski protestiert gegen sie als Urheber der Gewalt, bietet an, die Gewalttaten durch Zeugenverhör zu beweisen, und will sie vom Zeugnis in dieser Sache ausschließen lassen.',
     "A protest of Marcin Nosalski, heir and possessor of Rzgów, entered at Konin on 1 May 1779 and signed by him. He enters it as a precaution, so that the testimony of Bartłomiej Szepczyński and Mateusz Wąchnicki in his cause with Prusimski before the Kalisz land court at Konin shall not harm him. The two, he says, on the orders of Tomasz Joachimowicz, stopped his people on the public road as they were carting trees on sledges from Chełmski's hereditary woods, beat them, took them with the sledges to Trąbczyn and seized their axes by force. Nosalski protests against them as the authors of the violence, offers to prove the acts of violence by an inquiry of witnesses, and means to have them shut out from giving testimony in this cause."),
 13: ('Registervermerk von 1779: Eine Abschrift des Protests, den Prusimski gegen die Nosalski eingelegt hat, liegt bei den vorgelegten Schriftstücken. Antoni Prusimski, Starost von Niszczewice, hat unterschrieben.',
     'A register note of 1779: a copy of the protest that Prusimski made against the Nosalskis is among the documents produced. Antoni Prusimski, Starost of Niszczewice, signed.'),
}
HOW = ('written in the working session from the Latin and Polish as checked\n# (intake/holding.py, 2026-10-07).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
