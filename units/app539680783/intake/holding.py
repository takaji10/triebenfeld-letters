# -*- coding: utf-8 -*-
"""APP 53/968/0/-/783: from the editor's scans and text to the edition.

    python units/app539680783/intake/holding.py            # check only
    ... --crop        cut the page images
    ... --sheet       the fold page for the editor
    ... --write       page files and corpus.txt from the editor's text (once)
    ... --correct     apply ROWS, the readings corrected against the scans (once)
    ... --english     write translation/doc1.yml from ENGLISH
    ... --cache       put it into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding. The steps are
those of courtbook.holding_main (pipeline/intake/courtbook.py); the script
has its own main because the archive's cover stands before the document as
front matter, as in APP 53/968/0/-/801, which courtbook does not know.

The unit is one printed summons of 1860 from the papers of Albert Breyer:
four printed pages and a fifth with the court summoner's note of service,
filled in and signed by hand. The editor has four images (2026-10-13):
the archive's cover (Image00004), page 1 (Image00005), pages 2 and 3 on one
opening (Image00006) and page 4 with the note of service (Image00007).
Page ids carry the image number: 0004_a (the cover), 0005_a, 0006_a1,
0006_a2, 0007_a1, 0007_a2. The folds are read off strips of the gutter;
first proposals for the editor.

The text. The editor's file is one Markdown file with the Polish and, below
it, an English translation. The Polish has no page marks: it is cut to the
pages here at the words where each page of the print ends (PAGES). It reads
like machine recognition of the print, corrected by hand in places. Two
things are taken out as it is read in:
- words the summoner struck out in pen (the file gives them between "~~":
  "Jerzego vel" before Bogusław Gerke in no. 24, and the whole of no. 58):
  the edition does not transcribe struck-out text (EDITORIAL_RULES);
- Markdown.
The print's "é" (naturalnéj, któréj, Łazińskiéj) is "e" in the editor's
text throughout and is left so: a text is not converted in either direction.

The check (2026-10-13). All five pages were read against the scans, the
print in strips at full size and the handwriting enlarged. ROWS has what
was corrected; ADDED has the lines the editor's text did not have (the
summoner's signature and note of costs under the print, the number at the
head of the note of service and the signature under it).

Left as the editor has them, although the scan raises a question (notes.md,
"For the editor's eye"):
- no. 7, "Jana Fryderyka Rasch": the printed second name is written over in
  pen; whether struck out or changed to another name was not made out;
- no. 55, "Henryka Celmer": the first letter is written over in pen and may
  now be a Z;
- no. 70, "Krystjana Grünwald": the letters "ja" are written over in pen.
Nos. 53 and 54: the print's letter before "kiego" is corrected in pen to a
c in both, "Rogackiego".

No. 58. The print's "Jerzego a raczej Bogusława Gerke" is struck out and a
name is written in the margin in its place, between insertion marks and
over the summoner's paraph: "Marcina" and a surname read as Hetke, with
doubt (Hetke, Hecke or Heck). It was given as "[Hetke?]"; the editor read
"Heck" on the spot sheet (2026-10-14, intake/spot_answers.py, which also
has no. 70, "Krystofa", and the costs, "47").

Not transcribed: the revenue stamp at the head of page 1 (the double eagle,
"7½ КОПѢЕКЪ", "KOP: SIEDM I PÓŁ"); a pen note "Odp" with a flourish beside
it; the red pencil underlinings; the summoner's paraph under his two
signatures and under the margin note.

The English. The editor's translation was a machine's and wrong in many
places of substance ("Zapozwałem", I have summoned, was "I have acquainted
myself with"; her father was "her husband"; the manor was "the court";
fourteen holdings were "eleven"; the masculine name Bogumił was a woman
five times). It is written again here from the corrected Polish, page by
page (ENGLISH), keeping the editor's wording where it was right, and in the
edition's terms: woźny is Court Summoner, holendrzy Hollanders, huba Hufe,
Prusiński Prusimski, Celmer Zelmer, Wejgel Weigel. "Kolonja" in the
argument is one colonist's holding, not the settlement, and is "holding".
intake/changes.yml lists what changed in substance.
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app539680783'
REF = 'APP 53/968/0/-/783'
RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Pozew dla Karoliny Fridenberg stawienia się przed Trybunałem Cywilnym w Kaliszu w sporze kolonistów (53.968.0.-.783)")

# (file, x of the fold or None for a single page, left page, right page). First proposals.
SCANS = [
    ('Image00004.jpg', None, '0004_a', None),
    ('Image00005.jpg', None, '0005_a', None),
    ('Image00006.jpg', 2520, '0006_a1', '0006_a2'),
    ('Image00007.jpg', 2520, '0007_a1', '0007_a2'),
]
LEAF = {'0004_a': 'the cover', '0005_a': 'page 1', '0006_a1': 'page 2', '0006_a2': 'page 3',
        '0007_a1': 'page 4', '0007_a2': 'the note of service'}
PAGE_IDS = ['0005_a', '0006_a1', '0006_a2', '0007_a1', '0007_a2']
DOCS = [(1, PAGE_IDS)]
FOLD_NOTE = 'Both halves are pages of the edition.'

# The archive's cover: front matter, before the document, as in 53/968/0/-/801.
# The title is the archivist's, in pencil and in square brackets on the cover.
COVER = ('0004_a', [
    'Spuścizna Alberta Breyera',
    '[Pozew dla Karoliny Fridenberg z kolonii Staro-Łozińskiej stawienia się przed Trybunałem Cywilnym w Kaliszu '
    'w sporze kolonistów kolonii Staro-Łozińskiej i Nowo-Łozińskiej w dobrach Trąbczyn osiadłych z Włodzimierzem '
    'Mięczyńskim, właścicielem tegoż Trąbczyna]',
    '1860. 7/19. X.',
    'Zespół: Spuśc. A Breyera',
    'Sygn. 783',
])

N_PARAS = 39
# Where each page of the print ends, in the editor's paragraphs: (index of the
# paragraph, the words after which the page ends, or None for the whole paragraph).
PAGES = [
    ('0005_a', 5, '80. Jana Kłodzińskiego, w tejże kolonji mieszkającego.'),
    ('0006_a1', 17, None),
    ('0006_a2', 26, 'prawo to nie może po szczególe służyć wszystkim'),
    ('0007_a1', 36, None),
    ('0007_a2', 38, None),
]
# Lines the editor's text does not have, read on the scans: (page, 'start' or 'end', line).
ADDED = [
    ('0007_a1', 'end', 'Michał Piechowski'),
    ('0007_a1', 'end', 'Koszta'),
    ('0007_a1', 'end', 'Raz Rs [47?] k 21.'),
    ('0007_a2', 'start', 'No 173.'),
    ('0007_a2', 'end', 'Michał Piechowski'),
]


def source_file():
    f = glob.glob(os.path.join(glob.escape(RAW), '*.md'))
    assert len(f) == 1, f
    return io.open(f[0], encoding='utf-8-sig').read().replace('\r\n', '\n')


def paragraphs():
    """The Polish of the editor's file as paragraphs: struck-out words and Markdown taken off."""
    pl = source_file().split('# **It happened as attested by the Bailiff.**')
    assert len(pl) == 2
    text = re.sub(r'~~.*?~~\s*', '', pl[0])
    out = []
    for raw in text.split('\n'):
        t = re.sub(r'^#+\s*', '', raw.strip())
        t = re.sub(r'\s+', ' ', courtbook.plain(t)).strip()
        if t:
            out.append(t)
    assert len(out) == N_PARAS, len(out)
    return out


def read_source():
    P = paragraphs()
    parts, at, rest = {}, 0, None
    for pid, last, cut in PAGES:
        lines = [rest] if rest else []
        rest = None
        lines += P[at:last]
        if cut is None:
            lines.append(P[last])
        else:
            assert P[last].count(cut) == 1, cut
            head, tail = P[last].split(cut)
            lines.append((head + cut).strip())
            rest = tail.strip()
            assert rest
        at = last + 1
        parts[(1, pid)] = [l for l in lines if l]
    assert at == N_PARAS and rest is None
    for pid, where, line in ADDED:
        if where == 'start':
            parts[(1, pid)].insert(0, line)
        else:
            parts[(1, pid)].append(line)
    return parts


# (page, text as transcribed, text as on the scan, why)
ROWS = [
    ('0005_a', 'Ja niżej podpisany woźny przy Trybunale cywilnym w Kaliszu przez jaśnie wielmożnego prezesa tegoż Trybunału nominowany w Kaliszu nie p?ający',
     'Ja niżej podpisany woźny przy Trybunale Cywilnym w Kaliszu przez JW Prezesa tegoż Trybunału nominowany w Kaliszu mieszkający —',
     'the hand has "w Kaliszu mie-" at the end of the line and "szkający —" on the next: the set words of a summoner naming himself; "JW" stands as two letters and is not written out'),
    ('0005_a', '6. Karola Gośka.', '6. Karola Goska.', 'the print has "Goska", without a mark on the s'),
    ('0005_a', '9. Krzysztofa Scbonfisch.', '9. Krzysztofa Schönfisch.', 'the print has "Schönfisch", as in no. 8'),
    ('0005_a', '18. Józefa Gośka.', '18. Józefa Goska.', 'the print has "Goska"'),
    ('0005_a', 'SSrów Krystjana Drewie, jako to', 'SSrów Krystjana Drewle, jako to', 'the print has "Drewle"'),
    ('0005_a', 'Juljanny primo voto Drewie, obecnie', 'Juljanny primo voto Drewle, obecnie', 'the print has "Drewle"'),
    ('0005_a', '53. Pawła Bogackiego.', '53. Pawła Rogackiego.', 'the print has "Rogackiego", as in no. 54; the c is the summoner\'s correction in pen in both'),
    ('0005_a', '58. 59. Karola Merk.', '58. Marcina [Hetke?]. 59. Karola Merk.',
     'the printed name is struck out and "Marcina" with a surname is written in the margin in its place, between insertion marks; the surname is read as Hetke with doubt'),
    ('0005_a', 'po Janie Bandzert pozo-łą wdowę', 'po Janie Bandzert pozołą wdowę',
     'the print breaks the word at the line end and has "pozo-" and "łą": a slip of the printer for "pozostałą", given as printed, without the line-end hyphen'),
    ('0006_a1', '88. Krystiana Haupt.', '88. Krystjana Haupt.', 'the print has "Krystjana"'),
    ('0006_a1', '95. Michała Celmer. 90. Jakóba Zelek.', '95. Michała Celmer. 96. Jakóba Zelek.', 'the print has 96'),
    ('0006_a1', 'na wnioski rekon-weneyjnego powodu', 'na wnioski rekonwencyjnego powodu', 'the print has "rekon-" and "wencyjnego" over a line end'),
    ('0006_a1', 'konkluzji ad primum,', 'konkluzji ad 1um,', 'the print has "ad 1um"'),
    ('0006_a1', '1. Dla jakiej ilości bydła', 'A) Dla jakiej ilości bydła', 'the print letters the two questions A) and B)'),
    ('0006_a1', '2. Jaka ma być dozwolona', 'B) Jaka ma być dozwolona', 'the print letters the two questions A) and B)'),
    ('0006_a1', 'Regentem Kroszczyńskim zezna-nym', 'Regentem Kroszczyńskim zeznanym', 'a line-end hyphen'),
    ('0006_a1', 'w rewirze lasów Trąbczynskich, Studzianka zwanym', 'w rewirze lasów Tąbczyńskich, Studzianka zwanym',
     'the print has "Tąb-" and "czyńskich" over a line end, without the r: the printer\'s slip, given as printed'),
    ('0006_a1', 'jak niemej Towarzystwa Kredytowego', 'jak niemniej Towarzystwa Kredytowego',
     'the print is worn here ("niem" and "j" are left); the word is "niemniej", as five lines above and in the same sentence on page 4'),
    ('0006_a2', 'prawo pastwiska zawisie było od szczegółówej ugody każdego pojedynczego holendra',
     'prawo pastwiska zawisłe było od szczegółowej ugody każdego pojedyńczego holendra', 'the print has "zawisłe", "szczegółowej", "pojedyńczego"'),
    ('0006_a2', 'cjcu jej Antoniemu Prusińskiemu', 'ojcu jej Antoniemu Prusińskiemu', 'the print has "ojcu" with a worn o; "po ojcu" stands two lines on'),
    ('0006_a2', 'Michalina Hrabina Miączyńską domagała się', 'Michalina Hrabina Miączyńska domagała się', 'the print has "Miączyńska"'),
    ('0006_a2', 'okupnymi czynszowmkami', 'okupnymi czynszownikami', 'the print has "czynszownikami"'),
    ('0006_a2', 'znajduje się §111, obejmujący', 'znajduje się § III, obejmujący', 'the print has the paragraph sign and a Roman three'),
    ('0006_a2', 'Według lego więc', 'Według tego więc', 'the print has "tego"'),
    ('0007_a1', 'ani pod-dzierżawiać, ani podzielac', 'ani poddzierżawiać, ani podzielac', 'a line-end hyphen'),
    ('0007_a1', 'obstaje przy tein,', 'obstaje przy tem,', 'the print has "tem"'),
    ('0007_a1', 'z dnia 10/28 Czerwca 1830 roku', 'z dnia 16/28 Czerwca 1830 roku', 'the print has 16/28: the two calendars are twelve days apart'),
    ('0007_a1', 'a eventualnie dla 11stu kolonji', 'a eventualnie dla 14stu kolonji', 'the print has "14stu", the fourteen holdings of the contract of 1805'),
    ('0007_a1', 'Stu-dzianka zwanym', 'Studzianka zwanym', 'a line-end hyphen'),
    ('0007_a1', 'a ewentualnie dla 14.stu kolonji', 'a eventualnie dla 14stu kolonji', 'the print has "eventualnie dla 14stu"'),
    ('0007_a1', 'każdej pojedynczej kolonji, tak, jak gdyby ona w wjłącznem posiadaniu',
     'każdej pojedyńczej kolonji, tak, jak gdyby ona w wyłącznem posiadaniu', 'the print has "pojedyńczej" and "wyłącznem"'),
    ('0007_a1', 'jak niemu ej Towarzystwa', 'jak niemniej Towarzystwa', 'the print has "niemniej", the second n worn'),
    ('0007_a2', 'Stosownie do żądania powoda, kopie tego pozwu', 'Stósownie do żądania powoda, kopję tego pozwu', 'the print has "Stósownie" and "kopję"'),
    ('0007_a2', 'w zamieszkaniu tegoż.', 'w zamieszkaniu tegoż. do rąk własnych oddałem świadczę —',
     'the summoner\'s words in pen after the print, left out of the transcription'),
]

# The English, page by page, written from the corrected Polish (see the docstring).
ENGLISH = {
 '0005_a': """Done as in the Court Summoner's attestation.

At the request of Włodzimierz Count Miączyński, heir of the Trąbczyn estate, residing in the village of Trąbczyn, Pyzdry District, for whom Stanisław Karasiński and Roman Ostapowicz, advocates of the Tribunal, will appear.

I, the undersigned Court Summoner at the Civil Tribunal in Kalisz, appointed by the Honourable President of that Tribunal, residing in Kalisz —

In connection with the summons issued on 6/18 August 1859 at the request of the colonists on the Trąbczyn estate against Włodzimierz Miączyński, by way of counterclaim —

I have summoned:

1. Daniel Hom. 2. Jan Mertz. 3. Krystjan Haupt. 4. The heirs of Krystjan Kitke, namely: a) Karolina, b) August, c) Ernestyna, d) Karol Wilhelm, minor children, in the person of their mother and natural guardian Karolina née Rutching, by her first marriage Kitke, now the wife of Gotlib Szreter, who is to act with the assistance and by the authority of that husband. 5. Marcin Merk. 6. Karol Goska. 7. Jan Fryderyk Rasch. 8. Ferdinand Wilhelm Schönfisch. 9. Krzysztof Schönfisch. 10. Wilhelm Kinast. 11. Marcin Merk. 12. Krystjan Kinast. 13. Krystjan Merk. 14. Bogumił Rybicki. 15. Wilhelm Knakfus. 16. Krystjan Friedenberg. 17. Wilhelm Haupt. 18. Józef Goska. 19. Wilhelm Haupt. 20. Marcin Falkenberg. 21. Wilhelm Fogel. 22. Antoni Przystański. 23. Karol Gibel. 24. Bogusław Gerke. 25. Ludwik Bartel. 26. Wojciech Runga. 27. Marcin Lipelt. 28. Andrzej Bytner. 29. Szczepan Prombs. 30. Krystjan Sehr. 31. Michał Tarnowski. 32. Piotr Malinowski. 33. Daniel Sehr. 34. Karolina Friedenberg, widow. 35. Jan Grzegorz Herman. 36. Krystjan Betka. 37. The heirs of Krystjan Drewle, namely: Paulina and Ernestyna, minor daughters, in the person of their mother and principal guardian Juljanna, by her first marriage Drewle, now the wife of Krzysztof Schönfisch, who is to act with the assistance and by the authority of that husband. 38. Daniel Przygoda. 39. Maciej Kinast. 40. Ludwik Stürtzenbecher. 41. Krystjan Stürtzenbecher. 42. Jan Stürtzenbecher. 43. Krystjan Hirsch. 44. Wilhelm Hohm. 45. Rozyna Kryger, widow of Jan Kryger, as mother and natural guardian of her minor children Krystjan, Dorota and Fryderik, born of her marriage with Jan Kryger. 46. August Falg. 47. Bogumił Runge. 48. Bogumił Haupt. 49. Wilhelm Runge. 50. Marcin Runge. 51. Karolina Moritz, widow of Krystjan Moritz, as mother and natural guardian of her minor children Karol and Krystyna Moritz, born of her marriage with Krystjan Moritz. 52. Jan Morelski. 53. Paweł Rogacki. 54. Stanisław Rogacki. 55. Henryk Zelmer. 56. Bogumił Haupt. 57. Antoni Strzyżykowski. 58. Marcin Heck. 59. Karol Merk. 60. Elżbieta Bandzert, widow of Jan Bandzert. 61. Bogumił Kinast. 62. Jan Peda. 63. Emanuel Bandzert. 64. Karol Giebel. 65. Samuel Szmigelski. 66. Marcin Giebel. 67. Jakób Kopczyński. 68. Józef Sapichowski. 69. Marcin Sapichowski. 70. Krystof Grünwald. 71. Godfrid Hübner. 72. Józef Sapichowski. 73. Szczepan Kopczyński. 74. Marcin Rogowicz. 75. Antoni Rythomer. 76. Gotfryd Haupt. 77. Juljanna Runge, widow of Gotfryd Runge, now the wife of Bogusław Kluge, who is to act with the assistance and by the authority of that husband, as mother and natural guardian of her minor children Krystjan and Karolina, born of her marriage with Gotfrid Runge. 78. Anna Elżbieta Zelmer, widow of Daniel Zelmer, as mother and natural guardian of her minor children Karolina, Krystyna, Julja, Krystjan and August, left by the said Daniel Zelmer. 79. Bogusław Kuhn — all residing in the Staro-Łazińska colony. 80. Jan Kłodziński, residing in the same colony.""",

 '0006_a1': """81. August Stark. 82. Bogusław Moritz. 83. Wojciech Kinast. 84. Bogumił Betka. 85. Michał Kinast. 86. Krystjan Rejch. 87. Jan Schwebs. 88. Krystjan Haupt. 89. Marcin Schmechel. 90. Marcin Lipeldt. 91. Marcin Gother. 92. August Zelmer. 93. Krystjan Haupt. 94. Krystjan Haupt. 95. Michał Zelmer. 96. Jakób Zelek. 97. Krystjan Kinast — residing in the Nowo-Łazińska colony, commune of Trąbczyn, Pyzdry District; to appear within eight days of the service of this summons, not counting the time the law allows for distance, at 10 o'clock in the morning, or when this case is called, at the hearing of the Civil Tribunal of the Warsaw Governorate in Kalisz, which holds its sittings in the government palace in Józefina Street, and to answer the motions of the counterclaiming plaintiff, who will demand:

1. That, the actions being joined, the contract concluded on 18 May 1805 between the Prince of Hohenlohe-Ingelfingen and fourteen colonists of the commune of Trąbczyn, before the Patrimonial Court of the Prince of Hohenlohe at Zagórów, be declared not binding on the counterclaiming plaintiff and lapsed in its effects, and thereby as giving the defendants to the counterclaim no right of free pasture and wood-gathering in the Studzianka district, which belongs to the forests of the Trąbczyn estate.

2. That the servitude of pasture and wood-gathering in the Studzianka district be awarded only to those holdings which were the subject of the contract concluded before the notary Kroszczyński on 21 December 1828 between Michalina née Prusimska, Countess Miączyńska, and seven colonists; and in the alternative:

3. Should the first conclusion be rejected, that the servitude of pasture and wood-gathering be awarded only to the 14 holdings that are named one by one in the contract concluded on 18 May 1805 between the Prince of Hohenlohe-Ingelfingen and fourteen colonists.

4. That, to find for how many cattle grazing in the Studzianka district is to be allowed for each holding separately, a report of experts be ordered on these questions of fact:

A) For how many cattle, of what kind and in what parts of the Studzianka district, pasture is to be allowed in the district of the Trąbczyn forests called Studzianka for the seven holdings granted by the deed of grant of 21 December 1828, declared by Michalina Countess Miączyńska before the notary Kroszczyński, and in the alternative for the fourteen holdings covered by the contract of 18 May 1805, without regard to the number of settlers now on each of these holdings through their subdivision, having regard to the extent of the holdings, to the meadows and pastures belonging to them, and to the needs of the Trąbczyn estate and the forest management introduced in the Studzianka district.

B) What is to be the greatest quantity of wood that may be gathered, and in what parts of the Studzianka district, on each forest day, for each of the seven holdings granted by the contract of 21 December 1828, and in the alternative for the fourteen holdings granted by the contract of 18 May 1805, having regard to the needs of each single holding as if it were in the sole possession of one settler, and likewise to the needs of the Trąbczyn estate, to the forest management introduced in the Studzianka district, and to the requirements of the Bank of Poland on account of the Treasury loan it has granted, and likewise of the Credit Society on account of the highest loan that is to be taken up.

5. That a member of the Tribunal be delegated to take the experts' oath, and to appoint them by virtue of office should the parties not agree on choosing them freely.

6. That all the other defendants, to whom the right to exercise the servitude of pasture and wood-gathering is not awarded in these proceedings, be forbidden to graze and to gather wood in the Studzianka district.

7. That judgment be given with provisional enforcement. Lastly:

8. That the costs of the proceedings be awarded to the plaintiff against the defendants.

Facts and grounds.

Paweł Prusimski of Kolno and his wife Katarzyna Prusimska, née Rozdrażewska, heirs of the Trąbczyn estate, in the year 1746 granted the Hollanders on the lands of the Trąbczyn estate a privilege settling their mutual relations, in which they said among other things:""",

 '0006_a2': """“I do not forbid pasture for all their livestock, which they shall enjoy on coming to an agreement.”

By this privilege, then, the right of pasture depended on a particular agreement of each single Hollander with the owner of the Trąbczyn estate.

When, in consequence of political events, the part of the Polish country within which the Trąbczyn estate lay passed under Prussian rule, this estate, then the property of Antoni Prusimski, Starost of Niszczewice, was confiscated and given to the Prince of Hohenlohe-Ingelfingen, who on 18 May 1805 concluded with fourteen Hollanders of the commune of Trąbczyn, named one by one in that contract, a contract of sale of a part of the pine forest and marshes adjoining the lands they held, 42 Hufen of Magdeburg measure in area. In § 4 of that contract it is said:

“They take free pasture, without payment, in the part of the pine forest on the Biskupice boundary called the Zarzyński district, and likewise in that part of theirs the free gathering of wood on the customary forest days.”

The Trąbczyn estate remained in the possession of the Prince of Hohenlohe-Ingelfingen until the time when, after the change of government that followed, the Governing Commission, as the highest authority in the country, by its resolution of 21 July 1807 restored Michalina Dąbska, née Prusimska, to the ownership of the Trąbczyn estate, which had been confiscated from her father Antoni Prusimski. With Dąbska restored to the rights that were hers after her father, all acts and obligations entered into by the Prince of Hohenlohe were annulled. This question of principle was decided by the judgment of the Court of the Highest Instance given on 7 July 1826 in the case between Michalina née Prusimska, by her first marriage Dąbska, by her second the wife of Stanisław Miączyński, and Bogumił Karol Weigel. In those proceedings Weigel claimed interest on a capital of 200,000 Polish złoty which the Prince of Hohenlohe-Ingelfingen had raised as a loan on the Trąbczyn estate, and Michalina Countess Miączyńska for her part demanded that this capital be struck out of the mortgage register. The Court of the Highest Instance adopted these principles:

That the passing of the Trąbczyn estate into the ownership of the Prince of Hohenlohe-Ingelfingen had force only so long as the same state of things lasted as before; that the owner of the estate was restored, by the will and resolution of the Highest Authority, to such rights in respect of his estate as were his when it was taken from him; that a debt contracted by the donee, once he proved to be a conditional possessor, ceased with the fall of his title to bind the estate charged with it — and in consequence of these principles the Court of the Highest Instance dismissed Weigel's demand that interest on the capital of 200,000 Polish złoty be awarded to him, and ordered the capital itself to be struck out.

On the same principles, then, adopted in that judgment, the contract concluded on 18 May 1805 between the Prince of Hohenlohe-Ingelfingen and the 14 Hollanders did not bind Michalina Countess Miączyńska in the least and must be held to have lapsed in its effects, like all the obligations entered into by the Prince of Hohenlohe in respect of the Trąbczyn estate.

Neither the Hollanders themselves nor Michalina Countess Miączyńska understood the matter otherwise when on 21 December 1828, before the notary Mikołaj Kroszczyński, an agreement settling their mutual relations was concluded between Michalina née Prusimska, Countess Miączyńska, and seven rent-payers holding by purchase, named one by one in that deed. Although in that contract the parties cited the contract of 18 May 1805, they did not confirm it in the least; they only carried some conditions of that contract over into the new agreement. Among these conditions is § III, which reserves the right of common pasture and of gathering wood in the Zarzyński district, or Studzianka, on the side of the Biskupice estate. By this last deed, then, only the settlers named in it had the right to free pasture and the free gathering of wood in the Studzianka district, since for all the other colonists the grant of the Prince of Hohenlohe-Ingelfingen of 18 May 1805 had lost all force, on the principles adopted in the judgment of the Highest Court of 7 July 1826.

In the alternative: should it be held that the colonists covered by the contract of 18 May 1805 also have the right to exercise pasture and to gather wood in the Studzianka district, this right cannot belong separately to all the""",

 '0007_a1': """colonists now in being, but only to those holdings which were created by that grant and are named in the contract of the year 1805. For in the contract of the Prince of Hohenlohe a certain number of colonists is set down by number, and so only that number of them ought to exist and only for them could the use of pasture and wood-gathering be awarded; for that contract did not empower the colonists to divide the lands they occupy into parts. Through the subdivision of the holdings an incomparably greater number of hearths, inhabitants and livestock has arisen — and all this has increased the need for pasture and wood, to the evident harm of the manor. Thus the resolution of the Administrative Council in the year 1858 laid down:

1. That perpetual leaseholders ought to occupy themselves with farming alone.

2. That a perpetual leaseholder is not allowed to hold two farms.

3. That a perpetual leaseholder may neither sublet the farm granted to him nor divide it into parts without the express permission of the manor. From this it follows that, at the worst, only those holdings have the right to pasture and wood-gathering which existed at the time of the contract of 18 May 1805, and all the others, which arose through subdivision, cannot enjoy this right; although the plaintiff chiefly maintains that the number of holdings is fixed by the deed of 21 December 1828, and only in the alternative by the contract of 18 May 1805.

With the Trąbczyn forests and their management put in order, the servitude of pasture and wood-gathering, exercised in the manner described above, is exceedingly burdensome. Count Miączyński has the right, under article 4 of the law on servitudes of pasture and felling of 16/28 June 1830, to demand that the number of cattle to be grazed in the Studzianka district be limited to what the land needed when this servitude was established. This servitude can therefore be awarded only to the 7 holdings that acceded to the deed of 21 December 1828, and in the alternative only to the 14 holdings that were the subject of the contract of the year 1805; that is, it can be awarded only in proportion to the need of each of these holdings, and never in proportion to the number of settlers on them and the number of cattle they keep. To establish this number, therefore, a report of experts ought to be ordered on this question of fact:

For how many cattle, of what kind and in what parts of the Studzianka district, pasture is to be allowed in the district of the Trąbczyn forests called Studzianka for the 7 holdings granted by the deed of grant of 21 December 1828, declared by Michalina Countess Miączyńska before the notary Kroszczyński — and in the alternative for the 14 holdings covered by the contract of 18 May 1805, without regard to the number of settlers on each of these holdings through their subdivision, having regard to the extent of the holdings, to the meadows and pastures belonging to them, and to the needs of the Trąbczyn estate and the forest management introduced in the Studzianka district.

The same applies to the right of gathering wood, to determine which the plaintiff proposes the following question of fact:

What is to be the greatest quantity of wood that may be gathered, and in what parts of the Studzianka district, on each forest day, for each of the seven holdings granted by the contract of 21 December 1828, and in the alternative for the 14 holdings granted by the contract of 18 May 1805, having regard to the needs of each single holding as if it were in the sole possession of one settler, and equally to the needs of the Trąbczyn estate, to the forest management introduced in the Studzianka district, and to the requirement of the Bank of Poland on account of the Treasury loan it has granted, and likewise of the Credit Society on account of the highest loan that is to be taken up.

The plaintiff's conclusion is thus fully justified. Costs are due under article 130, and provisional enforcement under article 135, of the Code of Judicial Procedure.

I reserve the development of the grounds, and judgment by default.

Date as above.

Michał Piechowski

Costs

In all 47 silver roubles 21 kopecks.""",

 '0007_a2': """No. 173.

In accordance with the plaintiff's request I have handed a copy of this summons, the original of which is printed on stamped paper of the value of 7½ kopecks, to Karolina Fridenberg, residing in the Staro-Łazińska colony in the Pyzdry District, which belongs to the Trąbczyn estate, at that person's dwelling. I delivered it into her own hands; I attest it —

In the Staro-Łazińska colony, 7/19 October 1860.

Michał Piechowski""",
}


def english():
    return {1: [ENGLISH[pid] for pid in PAGE_IDS]}


S = {
 1: ('Gedruckte Vorladung in polnischer Sprache, die der Gerichtsbote Michał Piechowski am 7./19. Oktober 1860 Karolina Fridenberg in der Kolonie Staro-Łazińska zustellte; die Liste der Geladenen nennt unter Nummer 34 eine Witwe Karolina Friedenberg. Graf Włodzimierz Miączyński, Erbherr von Trąbczyn, den die Kolonisten seines Gutes am 6./18. August 1859 verklagt hatten, erhebt vor dem Zivilgericht des Gouvernements Warschau in Kalisch Widerklage und lässt die Beklagten unter 97 Nummern laden: 80 aus der Kolonie Staro-Łazińska und 17 aus der Kolonie Nowo-Łazińska, darunter Henryk, August und Michał Zelmer (im Druck „Celmer“) sowie die Witwe und die Kinder des Daniel Zelmer. Er verlangt, den Vertrag vom 18. Mai 1805 zwischen dem Fürsten zu Hohenlohe-Ingelfingen und vierzehn Kolonisten für ihn unverbindlich zu erklären und das Recht auf Weide und Holzsammeln im Revier Studzianka des Trąbczyner Waldes nur den sieben Stellen des Vertrags vom 21. Dezember 1828 zuzusprechen, hilfsweise den vierzehn Stellen von 1805; Sachverständige sollen sagen, für wie viel Vieh und wie viel Holz. Zur Begründung führt er an: Nach dem Privileg von Paweł und Katarzyna Prusimski von 1746 hing die Weide von der Einigung jedes Olęders mit dem Gutsherrn ab. Als die Regierungskommission das konfiszierte Gut am 21. Juli 1807 Michalina Dąbska zurückgab, seien die Verpflichtungen des Fürsten erloschen; so habe das höchste Gericht am 7. Juli 1826 gegen Weigel entschieden, der Zinsen von 200.000 polnischen Gulden forderte. Durch die Teilung der Stellen hätten sich Feuerstellen, Bewohner und Vieh zum Schaden der Gutsherrschaft vermehrt; ein Beschluss des Administrationsrats von 1858 verbiete Erbpächtern, einen Hof ohne Erlaubnis des Gutshofs zu teilen. Unter dem Druck stehen die Unterschrift des Gerichtsboten und ein Kostenvermerk.',
     'A printed summons in Polish, served on 7/19 October 1860 by the court messenger Michał Piechowski on Karolina Fridenberg in the Staro-Łazińska colony; the list of the summoned has a widow Karolina Friedenberg as its number 34. Count Włodzimierz Miączyński, heir of Trąbczyn, whom the colonists on his estate had sued on 6/18 August 1859, counterclaims before the Civil Tribunal of the Warsaw Governorate at Kalisz and has the defendants summoned under 97 numbers: 80 of the Staro-Łazińska colony and 17 of the Nowo-Łazińska colony, among them Henryk, August and Michał Zelmer (the print has "Celmer") and the widow and children of Daniel Zelmer. He asks the court to declare that the contract of 18 May 1805 between the Prince of Hohenlohe-Ingelfingen and fourteen colonists does not bind him, and to award the right of pasture and of gathering wood in the Studzianka district of the Trąbczyn forest only to the seven holdings of the contract of 21 December 1828, or failing that to the fourteen holdings of 1805; experts are to say for how many cattle and how much wood. His grounds: under the privilege of Paweł and Katarzyna Prusimski of 1746, pasture depended on each Olęder\'s agreement with the owner of the estate. When the Governing Commission gave the confiscated estate back to Michalina Dąbska on 21 July 1807, the Prince\'s obligations lapsed, as the highest court held on 7 July 1826 against Weigel, who claimed interest on 200,000 Polish złoty. The division of the holdings has multiplied hearths, inhabitants and livestock to the harm of the manor; a resolution of the Administrative Council of 1858 forbids perpetual leaseholders to divide a farm without the manor\'s permission. Under the print are the messenger\'s signature and a note of costs.'),
}
HOW = ('written in the working session from the Polish as checked\n# (intake/holding.py, 2026-10-13).')


def with_cover(fn):
    """Run a step of courtbook on corpus.txt without the cover, and put the cover back before the document."""
    path = os.path.join(UNIT_DIR, 'corpus.txt')
    head = '[PAGE %s]\n%s\n' % (COVER[0], '\n'.join(COVER[1]))
    if os.path.exists(path):
        s = io.open(path, encoding='utf-8').read()
        if s.startswith(head):
            io.open(path, 'w', encoding='utf-8', newline='\n').write(s[len(head):])
    try:
        return fn()
    finally:
        s = io.open(path, encoding='utf-8').read()
        if s.strip() and not s.startswith(head):
            io.open(path, 'w', encoding='utf-8', newline='\n').write(head + s)
        io.open(os.path.join(UNIT_DIR, 'transcriptions', COVER[0] + '.txt'), 'w', encoding='utf-8',
                newline='\n').write('\n'.join(COVER[1]) + '\n')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    parts = read_source()
    print(len(parts), 'pages,', sum(len(' '.join(p).split()) for p in parts.values()), 'words in the text as read in')
    logged = os.path.exists(os.path.join(UNIT_DIR, 'transcription_decisions.csv'))
    if '--crop' in arg:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS))
    if '--sheet' in arg:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS), (), LEAF, note=FOLD_NOTE)
    if '--write' in arg:
        assert not logged, 'corrections are already logged: --write would put the uncorrected text back'
        with_cover(lambda: courtbook.write_pages(UNIT_DIR, DOCS, parts))
    if '--correct' in arg:
        assert not logged, 'the corrections are already applied'
        with_cover(lambda: courtbook.correct(UNIT_DIR, SLUG, DOCS, ROWS, True))
    if '--english' in arg:
        tdir = os.path.join(HERE, 'translation')
        os.makedirs(tdir, exist_ok=True)
        courtbook.write_doc_yml(os.path.join(tdir, 'doc1.yml'), english()[1])
    if '--cache' in arg:
        courtbook.save_cache(ROOT, SLUG, os.path.join(HERE, 'translation'))
    if '--summaries' in arg:
        courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S, HOW)


if __name__ == '__main__':
    main()
