# -*- coding: utf-8 -*-
"""How the scans and the editor's transcriptions of I. HA GR, Rep. 7 C, Nr. 421
became this unit's page images and page files.

    python units/ihagrrep7cnr421/intake/holding.py            # check only
    ... --crop     cut the page images (raw_dir/processed/), with the editor's folds if saved
    ... --sheet    the fold page for the editor (review/ihagrrep7cnr421/folds/index.html)
    ... --write    the page files and corpus.txt

A record as much as a tool, on the model of units/ihagrrep7cnr3132/intake/holding.py:
the one place that says which part of which scan is a page, which source line
went where, and which readings were corrected against the scans. The editor's
saved folds in intake/folds.json win over the numbers here, which are first
proposals (courtbook.find_fold for the folds, the edges set by eye to leave off
the ruler and the dark ground).

The scans. The editor gave twenty-one files (Downloads\\74344_Lacko\\I_HA_Rep_7_C_Nr_421,
2026-11-21) with transcriptions of seventeen. 0015, 0018 and 0019 have none and
are left out (the editor: "For pages without a transcription, don't include
them in the project"; 0015 and 0018 are a blank side and the archive's slip
"Es folgen leere Seiten", 0019 the back cover). 0014 is the opening that the
editor's own crops 0014a (its left side) and 0014b (its right side) replace:
their transcriptions are of those, so 0014 is left out and 0014a and 0014b are
each one page, not cut. Their pages are named 0014_a1 and 0014_a2, the left and
right sides of scan 0014, because the scan matching takes a capture of four digits
(match_scans, relabel_scans); SOURCE_OF says which of the editor's files each
reads. 0001 is the cover, one page. The others are openings
photographed whole; the blank sides and the archive's slips are not cut out at
all (SKIP; the editor: "When you split pages, don't include the blank sides").
0016 is a large blank sheet with a small slip beside it; the slip is the page.

The text. The editor's files in <raw_dir>/txt, one per scan, line by line, the
broken word marked "¬". SPEC says, for each page, which source lines it takes.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'ihagrrep7cnr421'
REF = 'I. HA GR, Rep. 7 C, Nr. 421'
PREFIX = 'I_HA_Rep_7_C_Nr_421_'
RAW = r'C:\Users\Tersnaus\Downloads\74344_Lacko\I_HA_Rep_7_C_Nr_421'
TXT = os.path.join(RAW, 'txt')


def _p(s):
    return PREFIX + s


# (file, x of the fold or None for one page, left page, right page). First proposals
# (courtbook.find_fold; 0016 the edge of the large sheet, where the slip begins).
SCANS = [
    (_p('0001.jpg'), None, _p('0001_a'), None),
    (_p('0002.jpg'), 2544, _p('0002_a1'), _p('0002_a2')),
    (_p('0003.jpg'), 2512, _p('0003_a1'), _p('0003_a2')),
    (_p('0004.jpg'), 2557, _p('0004_a1'), _p('0004_a2')),
    (_p('0005.jpg'), 2559, _p('0005_a1'), _p('0005_a2')),
    (_p('0006.jpg'), 2570, _p('0006_a1'), _p('0006_a2')),
    (_p('0007.jpg'), 2588, _p('0007_a1'), _p('0007_a2')),
    (_p('0008.jpg'), 2600, _p('0008_a1'), _p('0008_a2')),
    (_p('0009.jpg'), 2601, _p('0009_a1'), _p('0009_a2')),
    (_p('0010.jpg'), 2628, _p('0010_a1'), _p('0010_a2')),
    (_p('0011.jpg'), 2633, _p('0011_a1'), _p('0011_a2')),
    (_p('0012.jpg'), 2473, _p('0012_a1'), _p('0012_a2')),
    (_p('0013.jpg'), 2639, _p('0013_a1'), _p('0013_a2')),
    (_p('0014a.jpg'), None, _p('0014_a1'), None),
    (_p('0014b.jpg'), None, _p('0014_a2'), None),
    (_p('0016.jpg'), 2640, _p('0016_a1'), _p('0016_a2')),
    (_p('0017.jpg'), 2629, _p('0017_a1'), _p('0017_a2')),
]
# The blank sides, and the archive's slips (the user sheet on the left of 0002,
# "Es folgen leere Seiten" on the right of 0010): not pages of the edition.
SKIP = {_p(x) for x in ('0002_a1', '0006_a1', '0008_a1', '0010_a2', '0011_a1', '0016_a1', '0017_a1')}
# First proposals for the page edges, in pixels of the scan: the dark ground on
# the left, the ruler on the right.
EDGES = {
    _p('0001.jpg'): (0, 2700),
    _p('0002.jpg'): (None, 5100),
    _p('0003.jpg'): (90, 5090),
    _p('0004.jpg'): (90, 5100),
    _p('0005.jpg'): (90, 5100),
    _p('0006.jpg'): (None, 5120),
    _p('0007.jpg'): (90, 5150),
    _p('0008.jpg'): (None, 5130),
    _p('0009.jpg'): (90, 5160),
    _p('0010.jpg'): (90, None),
    _p('0011.jpg'): (None, 5070),
    _p('0012.jpg'): (90, 5030),
    _p('0013.jpg'): (90, 5180),
    _p('0014a.jpg'): (70, None),
    _p('0014b.jpg'): (None, 2570),
    _p('0016.jpg'): (None, 3960),
    _p('0017.jpg'): (None, 5110),
}
# What each page is, for the fold page.
LEAF = {_p(k): v for k, v in {
    '0001_a': 'the cover', '0002_a1': 'the archive\'s user sheet',
    '0002_a2': 'Chełmski\'s petition, side 1',
    '0003_a1': 'petition, side 2', '0003_a2': 'petition, side 3',
    '0004_a1': 'petition, side 4', '0004_a2': 'petition, side 5',
    '0005_a1': 'petition, side 6', '0005_a2': 'petition, side 7 (signature)',
    '0006_a1': 'blank side', '0006_a2': 'copies of the two decrees, side 1',
    '0007_a1': 'copies of the two decrees, side 2', '0007_a2': 'draft resolution of 21 Oct. 1799',
    '0008_a1': 'blank side', '0008_a2': 'Mondio\'s petition, side 1',
    '0009_a1': 'Mondio\'s petition, side 2', '0009_a2': 'Mondio\'s petition, side 3',
    '0010_a1': 'Mondio\'s petition, side 4', '0010_a2': 'the archive\'s slip',
    '0011_a1': 'blank side', '0011_a2': 'copy dated 1 Dec. 1799, side 1',
    '0012_a1': 'copy dated 1 Dec. 1799, side 2', '0012_a2': 'copy of the suit of 19 March 1799, side 1',
    '0013_a1': 'the suit, side 2', '0013_a2': 'the suit, side 3',
    '0014_a1': 'the suit, side 4 (the editor\'s crop)', '0014_a2': 'copy of the Polish bond (the editor\'s crop)',
    '0016_a1': 'blank sheet', '0016_a2': 'the office\'s slip',
    '0017_a1': 'blank side', '0017_a2': 'draft to Mondio, 23 Dec. 1799'}.items()}
FOLD_NOTE = 'A blank side is left out; the green lines are the page edges kept.'

# page id -> [(first line, last line), ...] of the source file of its scan.
SPEC = [
    ('0001_a', [(1, 5)]),            # the cover: front matter
    # the petition's first side; the two notes in its left margin (the office's,
    # and the decision of 21 Oct.) first, so that the column's last line "von Kö-"
    # and the catchword "nigl:" at its foot stay together for the line-end pass
    ('0002_a2', [(34, 54), (1, 33)]),
    ('0003_a1', [(1, 34)]),
    ('0003_a2', [(35, 66)]),
    ('0004_a1', [(1, 35)]),
    ('0004_a2', [(36, 69)]),
    ('0005_a1', [(1, 35)]),
    ('0005_a2', [(36, 44)]),
    ('0006_a2', [(1, 29)]),
    ('0007_a1', [(1, 12)]),
    ('0007_a2', [(13, 47)]),
    ('0008_a2', [(1, 38)]),
    ('0009_a1', [(1, 42)]),
    ('0009_a2', [(43, 83)]),
    ('0010_a1', [(1, 25)]),
    ('0011_a2', [(1, 33)]),
    ('0012_a1', [(1, 17)]),
    ('0012_a2', [(18, 50)]),
    ('0013_a1', [(1, 33)]),
    ('0013_a2', [(34, 64)]),
    ('0014_a1', [(1, 14)]),
    ('0014_a2', [(1, 37)]),
    ('0016_a2', [(1, 7)]),
    ('0017_a2', [(1, 27)]),
]
FRONT = ['0001_a']                 # the cover, front matter before document 1
# Pages whose text is in a source file not named after their capture: the editor's
# crops of scan 0014 (files ..._0014a.txt and ..._0014b.txt).
SOURCE_OF = {'0014_a1': '0014a', '0014_a2': '0014b'}

# Seven documents (the editor, 2026-11-21, asked before the cut: "Seven: bond
# with the suit"). The decision in the margin of the petition's first side stays
# with the petition; the office's slip of 23 Dec. (0016, bound after the suit)
# stands with Mondio's petition, the paper it decides, out of the file's order,
# as the slip of Nr. 3132; the Polish copy of the bond is the enclosure of the
# copy of the suit and one document with it.
# Each: (number, [(page, first line, last line or None), ...]).
DOCS = [
    (1, [('0002_a2', 1, None), ('0003_a1', 1, None), ('0003_a2', 1, None), ('0004_a1', 1, None),
         ('0004_a2', 1, None), ('0005_a1', 1, None), ('0005_a2', 1, None)]),   # Chełmski's petition, 8 Oct 1799
    (2, [('0006_a2', 1, None), ('0007_a1', 1, None)]),     # copies of the decrees of 10 and 27 Sept 1799
    (3, [('0007_a2', 1, None)]),                           # draft resolution to Chełmski, 21 Oct 1799
    (4, [('0008_a2', 1, None), ('0009_a1', 1, None), ('0009_a2', 1, None), ('0010_a1', 1, None),
         ('0016_a2', 1, None)]),                           # Mondio's petition, 7 Dec 1799, with the office's slip
    (5, [('0011_a2', 1, None), ('0012_a1', 1, None)]),     # copy of the petition, dated 1 Dec 1799
    (6, [('0012_a2', 1, None), ('0013_a1', 1, None), ('0013_a2', 1, None),
         ('0014_a1', 1, None),                             # copy of the suit, Posen, 19 March 1799,
         ('0014_a2', 1, None)]),                           # with the copy of Prusimski's bond, Łukom, 16 June 1794 (Polish)
    (7, [('0017_a2', 1, None)]),                           # draft to Mondio, 23 Dec 1799
]
# (scan, line, reason): source lines that are not text.
OMIT = []

# (page id, old, new, reason). From the check against the scans (2026-11-21): four
# Sonnet readers (1: the clean hands and copies; 2: Chełmski's petition; 3: Mondio's
# petition and the suit; 4, independently, image first: the Polish bond, the margin
# of the petition, the slip, the registry notes), and Claude, who read the pages the
# readers left unopened (0009_a2, 0010_a1, 0005_a2) and settled the rest. A reading
# is changed only on a plain page, a witness in the file (Mondio's petition and its
# clean copy, 0008-0010 and 0011-0012; the margin decision of 0002_a2 and the clean
# draft of 0007_a2; the suit and the bond it describes) or the one possible sense;
# where the readers disagree and the editor's word is possible it stands, and the
# question goes on the spot sheet (WORKING_NOTES, from Nr. 3067). Rows marked
# "spot sheet" are changes the editor is asked to confirm.
CORRECTIONS = [
    # Cover
    ('0001_a', 'd. 24 Octobr 1799', 'd. 21 Octobr 1799',
     '21 (reader 1, sure), the date of the resolution, document 3; spot sheet'),
    # Document 1: Chełmski's petition
    ('0002_a2', '[V?]erers', 'Revers',
     '"Revers" (reader 2), the word of 0004_a1 ("blosen Rever-se"), the bond Prusimski gave'),
    ('0002_a2', 'd[u?][r?]y', 'durch', '"durch das gegen ihn ergangene Confiscations Urtel" (reader 2), the one sense'),
    ('0002_a2', 'von Erste[?]', 'von Kö¬',
     '"von Kö-/nigl: Majestät Allerhöchsten Person geschenkt" (reader 2): the catchword at the foot and the first line of 0003_a1 continue it'),
    ('0002_a2', '\neigl.', '\nnigl:', 'the catchword "nigl:" at the foot of the column (reader 2), repeated at the head of 0003_a1'),
    ('0002_a2', 'nur zugestellten', 'mir zugestellten', '"mir" (readers 2 and 4)'),
    ('0002_a2', 'der Regierung noch 10 Sept. c.', 'der Regierung vom 10 Sept. c.',
     '"vom" (readers 2 and 4), as the draft of 0007_a2 "der dortigen Regierung vom 10. Sept: c."'),
    ('0002_a2', 'langt seine Bewerde behalte,', 'lediglich sein Bewenden behalte,',
     '"lediglich sein Bewenden" (readers 2 and 4, sure), the words of the draft on 0007_a2'),
    ('0002_a2', 'Krieges Kosten[?] due', 'Kriegs Kosten die', '"Kriegs Kosten die" (readers 2 and 4), the draft "Kriegskosten"'),
    ('0002_a2', 'ganze mahl[?] eines seb[?]', 'ganze Masse eines solchen',
     '"Masse eines solchen" (readers 2 and 4), the draft "die ganze Maße eines solchen Insurgenten"; a short word struck out before "Masse" is not transcribed'),
    ('0002_a2', 'Insurgente weit übersei[?]', 'Insurgenten weit übersteigen',
     '"Insurgenten weit übersteigen" (reader 2; reader 4 "übersteig-"), the draft "weis übersteigen"'),
    ('0002_a2', '8br[?].', '8br.', 'the date "d 21 8br 99" is plain (reader 4)'),
    ('0002_a2', 'ita conclusus eodem', 'ita conclusum eodem', '"conclusum" (readers 2 and 4), the formula'),
    ('0003_a1', 'vigl: Majestät', 'nigl: Majestät', 'the catchword of 0002_a2 repeated, "Kö-/nigl:" (reader 2)'),
    ('0003_a1', 'för[?]¬\nderung an den fiscund[?]', 'för¬\nderung an den fiscum',
     '"an den fiscum verwiesen" (reader 2), the one sense; the writer spells "Förderung" (line 23)'),
    ('0003_a1', 'briefi[?]¬', 'beifü¬', '"in Abschrift beifüge" (reader 2), as "abschriftlich überreiche" on 0003_a2'),
    ('0003_a1', 'son[?] werden', 'sen werden', '"nachgewie-/sen werden" (reader 2)'),
    ('0003_a1', 'reststand', 'feststand', '"bereits feststand" (reader 2), f for r'),
    ('0003_a2', 'forderung[?]', 'forderung', 'plain (reader 2)'),
    ('0003_a2', 'umstatthaft', 'unstatthaft', '"nicht unstatthaft" (reader 2); "umstatthaft" is no word'),
    ('0003_a2', '14ten Septbr. 1746.', '14ten Septbr. 1796.',
     '1796 (reader 2): the 9 is that of "1796" on 0004_a2; the cabinet order on the insurgents\' debts, Mondio\'s petition "vom 16ten deß. M. u. Jahres" after the rescript of 17 Sept. 1796'),
    ('0003_a2', 'dran[g?]', 'drang', 'plain (reader 2)'),
    ('0003_a2', 'noch¬\nnals', 'noch¬\nmals', '"nochmals" (reader 2)'),
    ('0003_a2', 's[en?].', 'sen.', '"abgewie-/sen" (reader 2)'),
    ('0004_a1', 'Allersüchst', 'Allerhöchst', '"Allerhöchst" (reader 2), the formula'),
    ('0004_a1', 're[?]¬\nordnet', 'ver¬\nordnet', '"verordnet" (reader 2)'),
    ('0004_a1', 'Schu¬\ndens Ersages', 'Scha¬\ndens Ersazes', '"Schadens Ersazes" (reader 2), the writer\'s z for tz'),
    ('0004_a1', 'und assön[?]', 'und alsdann', '"und alsdann soll er ... nachstehen" (reader 2), the one sense'),
    ('0004_a1', 'mein blosen Perer[?]¬\nste', 'meinem blosen Rever¬\nse',
     '"meinem blosen Reverse" (reader 2), the bond (0002_a2 "gegen einen Revers")'),
    ('0004_a1', 'der Plage deshalb', 'der Klage deshalb', 'K, the suit (reader 2, sure)'),
    ('0004_a2', '[H/G?]ufko[sc/z?]ript', 'Hofrescript',
     'Mondio\'s petition, the witness: "das HofRescript vom 17ten Septbr. 1796" (0011_a2; reader 2)'),
    ('0004_a2', 'Allershöch¬', 'Allerhöch¬', '"Allerhöchste" (reader 2)'),
    ('0004_a2', 'Willensweinung', 'Willensmeinung', 'm (reader 2)'),
    ('0004_a2', 'Pla¬\nvon[?] Inhalt', 'kla¬\nren Inhalt', '"gegen den klaren Inhalt" (reader 2), the one sense'),
    ('0004_a2', 'dem Chett[?]\nder Justiz gestöhet', 'dem Chef\nder Justiz zustehet',
     '"nicht aber dem Chef der Justiz zustehet" (reader 2), the one sense: the Grand Chancellor'),
    ('0004_a2', 'sezt\nrest,', 'sezt\nfest,', '"festsezt" (reader 2, sure), as "vest sezt" in Mondio\'s petition'),
    ('0005_a1', 'haften[fachten?]', 'haften', '"in solidum haften" (reader 2), the editor\'s alternative not on the page'),
    ('0005_a1', 'Vermögender', 'Vermögen der', 'two words (reader 2)'),
    ('0005_a1', 'höreichend', 'hinreichend', '"hinreichend" (reader 2)'),
    ('0005_a1', 'von fiscum', 'den fiscum', '"wider den fiscum" (reader 2)'),
    ('0005_a1', '[P/K?]la¬', 'Kla¬', 'K, the suit (reader 2, sure)'),
    # Document 2: the copies of the decrees
    ('0006_a2', 'auch das Vorstellen des p Chełmski', 'auf das Vorstellen des v Chełmski',
     '"auf das Vorstellen des v Chełmski" (reader 1): the decree answers his petition; "p" is the writer\'s v'),
    ('0006_a2', 'Ca. Rath', 'Cr. Rath', '"Cr. Rath", Criminal Rath (reader 1), as Mondio is called throughout'),
    ('0007_a1', '[k?]laren', 'klaren', 'plain (reader 1)'),
    ('0007_a1', 'Re¬\nmissions', 'Re¬\nvisions', '"Revisions Erkenntnisses" (reader 1, the strokes v-i-s), the judgment of revision the petition names'),
    ('0007_a1', 'nach [e?]mehr,', 'umsomehr,', '"umsomehr" (reader 1), the one sense'),
    ('0007_a1', 'eine[?] per¬', 'eine per¬', 'plain (reader 1)'),
    ('0007_a1', 'behandret', 'behandelt', '"behandelt" (reader 1)'),
    # Document 3: the draft resolution
    ('0007_a2', 'Staß\nrosten', 'Sta¬\nrosten', 'a line-end hyphen, not ß (reader 1, sure)'),
    ('0007_a2', 'Prusimeki', 'Prusimski', 'not "meki" (reader 1, sure)'),
    ('0007_a2', 'Resoluß\ntion', 'Resolu¬\ntion', 'a line-end hyphen (reader 1, sure)'),
    ('0007_a2', 'Glaubiger', 'Glæubiger', 'the clerk\'s æ, as "Dæmpfung", "Schæden" (reader 1)'),
    ('0007_a2', 'vermögen eines', 'Vermögen eines', 'capital V (reader 1)'),
    ('0007_a2', 'Personal-Anß\nsprüche', 'Personal-An¬\nsprüche', 'a line-end hyphen (reader 1, sure)'),
    # Document 4: Mondio's petition
    ('0008_a2', 'unter den\n9ten', 'unter dem\n9ten', '"unter dem" (reader 3), the clean copy 0011_a2'),
    ('0008_a2', 'per Ungeliehr', 'zur Ungebühr', '"zur Ungebühr" (reader 3), the clean copy'),
    ('0008_a2', '[P/K?]la¬', 'Kla¬', 'K (reader 3), the clean copy "Klage"'),
    ('0008_a2', 'betreffendei[?]¬\nan[?] Forderung', 'betreffend ei¬\nne Forderung',
     '"betreffend eine Forderung" (reader 3), the clean copy'),
    ('0008_a2', 'Anteriora[?]', 'Anteriora', 'plain (reader 3)'),
    ('0009_a1', 'erdr[?]u¬\ncte[?]', 'erdreu¬\nste', '"erdreuste" (reader 3); the clean copy "erdreiste"'),
    ('0009_a1', 'solentlich', 'holentlich', '"wiederholentlich" (reader 3), the clean copy'),
    ('0009_a1', 'Mißverw[ct?]ändniß', 'Mißverständniß', 'plain (reader 3, sure); the clean copy'),
    ('0009_a1', 'als von\nmehrigen Eigentümer', 'als nun¬\nmehrigen Eigenthümer',
     '"nunmehrigen Eigenthümer" (reader 3), the clean copy'),
    ('0009_a1', 'verweis[?]¬', 'verwech¬', '"verwechselt" (reader 3), the clean copy'),
    ('0009_a1', 'das [H?]öchtegricht[?]', 'das Hofrescript', '"Hofrescript" (reader 3); the clean copy "HofRescript"'),
    ('0009_a1', 'Ins[?]¬', 'Jah¬', '"Jahres" (reader 3), the clean copy'),
    ('0009_a2', 'an[?] sich vererbind¬', 'an sich unverbind¬', '"an sich unverbindlichen" (Claude on the image), the clean copy'),
    ('0009_a2', 'HochRescripts[?]', 'HofRescripts', '"HofRescripts" (Claude), the clean copy'),
    ('0009_a2', 'er[?]geachtet', 'ungeachtet', '"ungeachtet" (Claude), the clean copy'),
    ('0009_a2', 'die selbst dieses', 'da selbst dieses', '"da selbst" (Claude), the clean copy'),
    ('0009_a2', 's[z?]ript ausdrüklich rest[?]', 'script ausdrüklich vest',
     '"Rescript ausdrüklich vest sezt" (Claude), the clean copy "vest setzt"'),
    ('0009_a2', 'berasiget', 'beruhiget', '"beruhiget" (Claude), the clean copy'),
    ('0009_a2', 'Erme[?]¬\nsters', 'Erme¬\nssens', '"Ermessens" (Claude), the clean copy'),
    ('0009_a2', 'Ich föge', 'Ich füge', 'ü (Claude), the clean copy'),
    ('0009_a2', 'bemerk[e?]n', 'bemerken', 'plain (Claude), the clean copy'),
    ('0010_a1', 'langer verzögert', 'länger verzögert', 'ä (Claude), the clean copy'),
    ('0010_a1', 'Köngl:', 'Königl:', 'plain (Claude)'),
    ('0010_a1', 'schleunigst[?]', 'schleunigst', 'plain (Claude), the clean copy'),
    # Document 5: the copy dated 1 Dec.
    ('0011_a2', 'angestellet', 'angestellte', '"angestellte" (reader 1), the original 0009_a1 "ange-/stellte"'),
    ('0011_a2', 'Allerhöchste\nCabinets', 'Allerhöchsten\nCabinets', '"Allerhöchsten" (reader 1)'),
    ('0012_a1', 'bei, nur', 'bei, - nur', 'a dash (reader 1), as the original 0009_a2 "bei, - nur"'),
    # Document 6: the copy of the suit, with the bond
    ('0012_a2', 'ex Mirographa', 'ex Chirographo', '"ex Chirographo" (reader 3: Ch-), the formula: on the strength of a note of hand'),
    ('0012_a2', 'Prasimski', 'Prusimski', 'u (reader 3)'),
    ('0012_a2', 'Anto¬\nnuis v Brzeradzki', 'Anto¬\nnius v Przeradzki',
     '"Antonius v Przeradzki" (reader 3), the witness who signs the bond "Antoni Przeradzki" (0014_a2)'),
    ('0012_a2', 'werde zwischen nur', 'wurde zwischen mir', '"wurde zwischen mir" (reader 3), the one sense'),
    ('0012_a2', 'profixo', 'praefixo', '"in Termino solutionis praefixo" (reader 3), the formula'),
    ('0013_a1', 'antechreticam[?]', 'antichreticum', '"Contractum antichreticum" (reader 3), the pledge of land for a loan'),
    ('0013_a1', 'auf gefahrten', 'aufgeführten', '"von den aufgeführten Gütern" (reader 3)'),
    ('0013_a1', 'er[g?]ä[f?]¬\n[ct?]en', 'ergrif¬\nfen', '"den Besiz ... ergriffen" (reader 3), as "Besiz Ergreifung" below'),
    ('0013_a1', 'in[z?]iri¬\nschon mein Schuldverwegen', 'inzwi¬\nschen mein Schuldner wegen',
     '"inzwischen mein Schuldner wegen" (reader 3), the one sense'),
    ('0013_a1', 'angeklagt werden', 'angeklagt worden', '"worden" (reader 3)'),
    ('0013_a1', 'der\nich blos', 'dem\nich blos', '"dem ich blos durch meine Besiz Ergreifung ... zuvor gekommen war" (reader 3)'),
    ('0013_a1', 'E[x?]mich[?].', 'Exmiss.', '"Exmiss. Klage", the suit to evict (reader 3)'),
    ('0013_a1', 'Termin auch den', 'Termin auf den', '"auf den 27ten" (reader 3)'),
    ('0013_a2', 'zwischen ein[?]', 'zwischen mir', '"zwischen mir und dem Fisco" (reader 3)'),
    ('0013_a2', 'aequistriren', 'sequestriren', '"sequestriren" (reader 3): the settlement put the estates in his sequestration'),
    ('0013_a2', 'vorzugs zinsen', 'Verzugs zinsen', '"Verzugs zinsen" (reader 3), as "Verzugs Zinsen mit 7. proC." below'),
    ('0013_a2', 'Bei [F?] MM[?]', 'Bei E K M', '"Bei E K M", Ew. Königl. Majestät (reader 3), as the signature block of 0014_a1'),
    ('0013_a2', 'p Luctto[?]', 'Bitte', '"mit der Bitte, Term. instr. anzusagen" (reader 3), the one sense'),
    ('0013_a2', 'nicht willen dazu', 'nicht nur dazu', '"nicht nur dazu vorfordern, sondern" (reader 3)'),
    ('0013_a2', 'reta[s?]is expensis verer¬', 'refusis expensis verur¬', '"refusis expensis verurteilen" (reader 3), the formula'),
    ('0013_a2', '[ei?]n', 'in', 'the catchword "in", repeated at the head of 0014_a1 (reader 3)'),
    ('0014_a1', 'ein[?] Nichtzalungs', 'in Nichtzalungs', '"in" (reader 3), the catchword of 0013_a2'),
    ('0014_a1', 'stunten', 'stimmten', '"bestimmten Terminen" (reader 3, sure)'),
    ('0014_a1', 'ich mich auch obige', 'ich mich auch auf obige', '"auf" is on the page (reader 3)'),
    ('0014_a1', 'der gehörig', 'für gehörig', '"für gehörig substantiirt" (reader 3)'),
    ('0014_a1', '[w?]äge', 'möge', '"möge" (reader 3)'),
    ('0014_a1', '[F M M?]', 'E K M', '"E K M" (reader 3), as on 0013_a2'),
    ('0014_a2', 'Termin[?]', 'Termin', 'plain (reader 4, sure)'),
    ('0014_a2', 'duię', 'daię', '"daię" (reader 4)'),
    ('0014_a2', 'wyrazonych', 'wyrażonych', 'the dotted ż (reader 4)'),
    ('0014_a2', 'baż Prowizyi', 'bez Prowizyi', '"bez Prowizyi", without interest (reader 4)'),
    ('0014_a2', 'pozwałam', 'pozwalam', 'no ł (reader 4)'),
    ('0014_a2', 'Lazów tudzież Holandrów wszystkach', 'Łazow tudzież Hollendrow wszystkich',
     'Ł struck, "Hollendrow", "wszystkich" (reader 4)'),
    ('0014_a2', 'w[?]iętnośći', 'Maiętnośći', '"Maiętnośći", the estate (reader 4)'),
    ('0014_a2', 'żadnzey', 'żadney', 'plain (reader 4, sure)'),
    ('0014_a2', 'exacj[?]muiąc', 'exceptuiąc', '"nie exceptuiąc", not excepting (reader 4)'),
    ('0014_a2', 'Magazonu', 'Magazynu', 'y (reader 4)'),
    ('0014_a2', 'wyżeywy\nrazone', 'wyżey wy¬\nrażone', 'two words, "wy-/rażone" (reader 4, sure)'),
    ('0014_a2', 'bez zadney', 'bez żadney', 'ż (reader 4)'),
    ('0014_a2', 'wyrażana a na uzytek woy[?]', 'wyrażona a na uzytek moy',
     '"wyrażona" (reader 4, sure), "na użytek moy", for my use (reader 4)'),
    ('0014_a2', 'obracona, i w gotawiżnie', 'obrócona, i w gotowiźnie', '"obrócona", "gotowiźnie", in cash (reader 4)'),
    ('0014_a2', 'wypołucona', 'wypłacona', '"wypłacona", repaid (reader 4, sure)'),
    ('0014_a2', 'chac iakoby przy, sądowey osobie [u?]ozy', 'chąc iakoby przy, sądowey osobie moy',
     '"chąc", "moy" (reader 4)'),
    ('0014_a2', 'ni[?][?]a była', 'miana była', '"miana była" (reader 4)'),
    ('0014_a2', 'Jakub Bienkowski', 'Jakub Bieńkowski', 'ń (reader 4)'),
    ('0014_a2', 'przytomny Przyiacioł[?', 'przytomny Przyiaciół', '"Przyiaciół" (reader 4); the editor\'s bracket was not closed'),
    ('0014_a2', 'Antonii Przeradzki', 'Antoni Przeradzki', 'one i (reader 4, sure)'),
    ('0014_a2', 'tomny Przyiacioł.', 'tomny Przyiaciół.', '"Przyiaciół" (reader 4)'),
    # Document 7: the draft to Mondio
    ('0017_a2', 'e. Fiscum', 'c. Fiscum', '"c." = contra (reader 1, sure), as "contra Fiscum" below'),
    ('0017_a2', 'A[u?] liegen', 'Anl. liegen', '"Anl." (readers 1 and 4), the enclosure'),
    ('0017_a2', '[Gs?].', 'Gr.', '"Gr." (readers 1 and 4), the mark of 0007_a2'),
    ('0017_a2', 'Criminae-Rath', 'Criminal-Rath', 'plain (reader 1, sure)'),
]


def source():
    out = {}
    for f in sorted(os.listdir(TXT)):
        if not f.endswith('.txt'):
            continue
        scan = os.path.splitext(f)[0].rsplit('_', 1)[1]
        out[scan] = io.open(os.path.join(TXT, f), encoding='utf-8-sig').read() \
            .replace('\r\n', '\n').rstrip('\n').split('\n')
    return out


def build():
    """(pages {id: lines}, corpus text, problems)."""
    src = source()
    pages, problems = {}, []
    used = {}
    for s, n, _ in OMIT:
        used.setdefault(s, []).append(n)
    for pid, ranges in SPEC:
        scan = SOURCE_OF.get(pid, pid.split('_')[0])
        lines = []
        for a, b in ranges:
            lines.extend(src[scan][a - 1:b])
            used.setdefault(scan, []).extend(range(a, b + 1))
        if any(not l.strip() for l in lines):
            problems.append(f'{pid}: a blank line')
        pages[pid] = lines
    for scan, u in used.items():
        if sorted(u) != list(range(1, len(src[scan]) + 1)):
            problems.append(f'{scan}: the source has {len(src[scan])} lines, SPEC and OMIT use {sorted(u)}')
    if sorted(src) != sorted(used):
        problems.append('the source files and SPEC do not name the same scans: %s / %s' % (sorted(src), sorted(used)))
    for pid, old, new, why in CORRECTIONS:
        text = '\n'.join(pages[pid])
        n = text.count(old)
        if n != 1:
            problems.append(f'{pid}: {old!r} found {n} times')
            continue
        after = text.replace(old, new).split('\n')
        if len(after) != len(pages[pid]):
            problems.append(f'{pid}: the correction {old!r} changes the number of lines')
        pages[pid] = after
    # every line of every page in exactly one document (or the front matter)
    out, seen = [], {}
    for pid in FRONT:
        out.append('[PAGE %s]' % pid)
        out.extend(pages[pid])
        seen[pid] = list(range(1, len(pages[pid]) + 1))
    for n, parts in DOCS:
        out.append('[DOC %d]' % n)
        for pid, a, b in parts:
            lines = pages[pid]
            b = b or len(lines)
            out.append('[PAGE %s]' % pid)
            out.extend(lines[a - 1:b])
            seen.setdefault(pid, []).extend(range(a, b + 1))
    for pid, lines in pages.items():
        if sorted(seen.get(pid, [])) != list(range(1, len(lines) + 1)):
            problems.append(f'{pid}: not every line is in exactly one document')
    return pages, '\n'.join(out) + '\n', problems


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    scans = courtbook.placed(HERE, SCANS, EDGES)
    if '--crop' in arg:
        courtbook.cut(RAW, scans, SKIP, keep_skipped=False)   # the blank sides not kept (the editor)
    if '--sheet' in arg:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, scans, SKIP, LEAF, note=FOLD_NOTE)
    if '--crop' in arg or '--sheet' in arg:
        return
    pages, corpus, problems = build()
    if problems:
        sys.exit('NOT WRITTEN' + chr(10) + chr(10).join(problems))
    print(f'{len(pages)} pages, {len(DOCS)} documents, {len(CORRECTIONS)} corrections; '
          f'every source line placed exactly once')
    for n, parts in DOCS:
        print('  doc %d: %s' % (n, ', '.join('%s %d-%s' % (p, a, b or 'end') for p, a, b in parts)))
    if '--write' not in arg:
        return
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    for pid, lines in pages.items():
        with open(os.path.join(tdir, PREFIX + pid + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(chr(10).join(lines) + chr(10))
    with open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(corpus)
    print('wrote transcriptions/ and corpus.txt')


if __name__ == '__main__':
    main()
