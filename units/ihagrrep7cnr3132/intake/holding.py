# -*- coding: utf-8 -*-
"""How the scans and the editor's transcriptions of I. HA GR, Rep. 7 C, Nr. 3132
became this unit's page images and page files.

    python units/ihagrrep7cnr3132/intake/holding.py            # check only
    ... --crop     cut the page images (raw_dir/processed/), with the editor's folds if saved
    ... --sheet    the fold page for the editor (review/ihagrrep7cnr3132/folds/index.html)
    ... --write    the page files and document_boundaries.csv

A record as much as a tool: it is the one place that says which part of which
scan is a page, which source line went where, and which readings were
corrected against the scans. Follows units/ihagrrep7cnr3067/intake/build_pages.py
for the text and courtbook.cut/fold_sheet/placed for the images (the fold
page, with page edges; the editor's saved folds in intake/folds.json win over
the numbers here, which are first proposals: courtbook.find_fold for the
folds, the edges set by eye to leave off the ruler and the dark ground).

The scans. The editor gave eighteen (Downloads\\74344_Lacko\\I_HA_Rep_7_C_Nr_3132,
2026-11-20) with transcriptions of fifteen; 0003, 0017 and 0018 have none and
are left out unlooked-at (the editor: "some pages do not have transcriptions -
leave them out. No need to look at them"). 0001 is the cover, one page. The
others are openings of the file, photographed whole; many have one written
side, the other blank or the archive's slip, and that side is not staged
(SKIP). On 0013 and 0014 one side is a small slip bound in (the archive's
folio 9), recto on 0013, verso on 0014.

The text. The editor's files in <raw_dir>/txt, one per scan, line by line, the
broken word marked "¬". SPEC says, for each page, which source lines it
takes; OMIT the lines that are not text, with the reason.

CORRECTIONS are the readings changed against the scans after the Sonnet
readers and Claude checked every line (notes.md, "The transcription
checked"). The script checks that every source line is used exactly once
(or omitted) and that every correction finds its text exactly once.
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

SLUG = 'ihagrrep7cnr3132'
REF = 'I. HA GR, Rep. 7 C, Nr. 3132'
PREFIX = 'I_HA_Rep_7_C_Nr_3132_'
RAW = r'C:\Users\Tersnaus\Downloads\74344_Lacko\I_HA_Rep_7_C_Nr_3132'
TXT = os.path.join(RAW, 'txt')


def _p(s):
    return PREFIX + s


# (file, x of the fold or None for one page, left page, right page). First proposals.
SCANS = [
    (_p('0001.jpg'), None, _p('0001_a'), None),
    (_p('0002.jpg'), 2594, _p('0002_a1'), _p('0002_a2')),
    (_p('0004.jpg'), 2607, _p('0004_a1'), _p('0004_a2')),
    (_p('0005.jpg'), 2616, _p('0005_a1'), _p('0005_a2')),
    (_p('0006.jpg'), 2620, _p('0006_a1'), _p('0006_a2')),
    (_p('0007.jpg'), 2615, _p('0007_a1'), _p('0007_a2')),
    (_p('0008.jpg'), 2630, _p('0008_a1'), _p('0008_a2')),
    (_p('0009.jpg'), 2643, _p('0009_a1'), _p('0009_a2')),
    (_p('0010.jpg'), 2632, _p('0010_a1'), _p('0010_a2')),
    (_p('0011.jpg'), 2634, _p('0011_a1'), _p('0011_a2')),
    (_p('0012.jpg'), 2639, _p('0012_a1'), _p('0012_a2')),
    (_p('0013.jpg'), 2633, _p('0013_a1'), _p('0013_a2')),
    (_p('0014.jpg'), 2142, _p('0014_a1'), _p('0014_a2')),
    (_p('0015.jpg'), 2650, _p('0015_a1'), _p('0015_a2')),
    (_p('0016.jpg'), 2654, _p('0016_a1'), _p('0016_a2')),
]
# The blank sides (and the archive's slip on the left of 0002): not pages of the edition.
SKIP = {_p(x) for x in ('0002_a1', '0004_a1', '0005_a1', '0006_a2', '0007_a1', '0008_a1',
                        '0010_a2', '0011_a1', '0012_a1', '0015_a2', '0016_a1')}
# First proposals for the page edges, in pixels of the scan: the dark ground on
# the left, the ruler on the right.
EDGES = {
    _p('0001.jpg'): (0, 2670),
    _p('0002.jpg'): (None, 5130),
    _p('0004.jpg'): (110, 5130),
    _p('0005.jpg'): (110, 5130),
    _p('0006.jpg'): (110, 5130),
    _p('0007.jpg'): (110, 5130),
    _p('0008.jpg'): (110, 5130),
    _p('0009.jpg'): (110, 5130),
    _p('0010.jpg'): (110, 5130),
    _p('0011.jpg'): (110, 5070),
    _p('0012.jpg'): (110, 5140),
    _p('0013.jpg'): (110, 4740),
    _p('0014.jpg'): (110, 4650),
    _p('0015.jpg'): (110, 5130),
    _p('0016.jpg'): (110, 5130),
}
# The archive's pencil folio of each page, for the fold page.
LEAF = {_p(k): v for k, v in {
    '0001_a': 'the cover', '0002_a1': 'the archive\'s slip', '0002_a2': 'fol. 1r', '0004_a2': 'fol. 2r',
    '0005_a2': 'fol. 3r', '0006_a1': 'fol. 3v', '0007_a2': 'fol. 4r', '0008_a2': 'fol. 5r',
    '0009_a1': 'fol. 5v', '0009_a2': 'fol. 6r', '0010_a1': 'fol. 6v', '0011_a2': 'fol. 7r',
    '0012_a2': 'fol. 8r', '0013_a1': 'fol. 8v', '0013_a2': 'fol. 9r (the slip)',
    '0014_a1': 'fol. 9v (the slip)', '0014_a2': 'fol. 10r', '0015_a1': 'fol. 10v', '0016_a2': 'fol. 11r'}.items()}
FOLD_NOTE = 'A blank side is left out; the green lines are the page edges kept.'

# page id -> (document number or None to continue, first line on the page of
# that document, [(first line, last line), ...] of the source file)
# A page with a second document starting on it is given twice, the second
# entry naming the document and its first line on the page.
SPEC = [
    ('0001_a', [(1, 7)]),           # the cover: front matter
    ('0002_a2', [(1, 24)]),
    ('0004_a2', [(1, 17)]),
    ('0005_a2', [(1, 28), (30, 30), (29, 29)]),   # the office note before the catchword "eine" (WORKING_NOTES)
    ('0006_a1', [(1, 13)]),
    ('0007_a2', [(1, 20)]),
    ('0008_a2', [(1, 33)]),
    ('0009_a1', [(1, 29)]),
    ('0009_a2', [(30, 57)]),
    ('0010_a1', [(1, 11)]),
    ('0011_a2', [(1, 16)]),
    ('0012_a2', [(1, 19), (21, 28)]),
    ('0013_a1', [(1, 13)]),
    ('0013_a2', [(14, 30)]),
    ('0014_a1', [(1, 9)]),
    ('0014_a2', [(10, 51)]),
    ('0015_a1', [(1, 14)]),
    ('0016_a2', [(1, 29)]),
]
FRONT = ['0001_a']                 # the cover, front matter before document 1

# Eleven documents (the editor, 2026-11-20, asked before the cut: "11: slip
# with no. 4"). Each: (number, [(page, first line, last line or None), ...]),
# lines of the page as built. The office's slip (fol. 9; its "Acto 1261" is
# the registry number "B No 1261" of document 4) is not a document of its own
# but the office's notes on Goldbeck's letter of 11 May: its two sides stand
# after that letter's page, out of the file's order, and are listed in
# office_notes.yml. corpus.txt is written here in this order, not by
# import_pages.py, which keeps the order of the page files.
DOCS = [
    (1, [('0002_a2', 1, None)]),                       # Goldbeck to Haugwitz, 19 Feb 1803
    (2, [('0004_a2', 1, None)]),                       # Goldbeck to Haugwitz, 22 Apr 1803
    (3, [('0005_a2', 1, None), ('0006_a1', 1, None)]),  # Haugwitz to Goldbeck, draft, 29 Apr 1803
    (4, [('0007_a2', 1, None),                          # Goldbeck to Haugwitz, 11 May 1803,
         ('0013_a2', 1, None), ('0014_a1', 1, None)]),  # with the office's slip
    (5, [('0008_a2', 1, None), ('0009_a1', 1, None),    # copy of the joint report to the King, 30 Apr 1803
         ('0009_a2', 1, None), ('0010_a1', 1, None)]),
    (6, [('0011_a2', 1, None)]),                       # copy of the cabinet order, 10 May 1803
    (7, [('0012_a2', 1, 19)]),                         # copy of the rescript to the Posen government, 11 May 1803
    (8, [('0012_a2', 20, None), ('0013_a1', 1, None)]),  # copy of the resolution to the two, 11 May 1803
    (9, [('0014_a2', 1, 27)]),                         # Haugwitz to Voss, draft, 30 May 1803
    (10, [('0014_a2', 28, None), ('0015_a1', 1, None)]),  # Haugwitz to Goldbeck, draft, 30 May 1803
    (11, [('0016_a2', 1, None)]),                      # the rescript to the Posen chamber, draft, 30 May 1803
]
# (scan, line, reason): source lines that are not text.
OMIT = [
    ('0012', 20, 'the "–" the editor put for the flourish between the two copies; not text'),
]

# (page id, old, new, reason). Filled from the check against the scans.
CORRECTIONS = [
    # Document 1
    ('0002_a2', 'eines Xawer Jezierski', 'eines Xaver Jezierski',
     'v, not w (reader 1); "Xaver" throughout the file'),
    ('0002_a2', 'Finanz Ministre Herrn', 'Finanz Ministers Herrn',
     '"Ministers" (reader 1), the same address formula as documents 2 and 4'),
    ('0002_a2', 'solches gefälligst mitzuziehnen,', 'solches gefälligst mitzuzeichnen,',
     'the formula of document 2, "solches gefälligst mitzuzeichnen"; "mitzuziehnen" is no word (Claude; spot sheet)'),
    # Document 3 (Haugwitz's draft)
    ('0005_a2', 'die Keinschrift,', 'die Reinschrift,',
     'R (readers 3 and 4); "Keinschrift" is no word, the fair copy is meant'),
    ('0005_a2', 'gens confiscation und,\nänderlich', 'gens confiscation unab¬\nänderlich',
     '"unab-/änderlich" (readers 3 and 4); document 5 has the same words "wobey es unabänderlich verbleiben muß"'),
    ('0006_a1', 'Geschäfts Kreises liegen[?]', 'Geschäfts Kreises liegt',
     '"liegt" (readers 3 and 4); the sentence reads only so'),
    ('0006_a1', '[da?] mir geneigte\nConiudiciertz[?]', 'Die mir geneigtest\nCommunicirten',
     'read independently by readers 3 and 4 (reader 4 from the image before the text): "Die mir geneigtest Communicirten Acta"; the same words on 0014_a2'),
    ('0006_a1', 'sagus[?] hier wieder\nbey[?]', 'sagung hier wieder\nbey',
     '"Danksagung ... bey" (readers 3 and 4)'),
    ('0006_a1', '[Haugwitz?]', 'Haug[witz]',
     'the signature reads "Haug" with a long tail (readers 3 and 4); the rest from the writer, the co-signer of the report, as "A[lvensleben]" in Nr. 1414'),
    # Document 4: the office's slip
    ('0013_a2', 'Acta\n/26/', 'Cito\n1261',
     '"Cito" (readers 3 and 4, Claude), and the registry number 1261 of document 4 ("B No 1261" at its head)'),
    ('0013_a2', '1, An[?] munda sind zu Sie\nBal Unterschrift Koppe\nso ein das Concept.',
     '1, Die munda sind zu Sr[?]\n[?] Unterschrift vorzulegen[?]\nso wie das Concept.',
     '"Die" (Claude), "Unterschrift" sure, "so wie" (reader 3, Claude); the rest doubtful (spot sheet)'),
    ('0013_a2', 'ret. Cop. der Lab. O.', 'act. Cop. der Cab. O.',
     '"act." (reader 3, Claude); "Cab." as "Cab Ordre" the line above (readers 3 and 4)'),
    ('0013_a2', 'Frf. v. Goldbeck depart', 'Sr Exc v. Goldbeck depart',
     '"Sr Exc" (readers 3 and 4, Claude)'),
    ('0013_a2', 'neml. einem hieb', 'neml. einem [?]',
     'the word does not begin with h (readers 3 and 4); not read (spot sheet)'),
    ('0013_a2', 'an [?] Goldbeck aus dieses,', 'an Sr v. Goldbeck aus dieses[?],',
     'the margin note "an Sr v. Goldbeck" (readers 3 and 4); the next words doubtful'),
    ('0013_a2', 'notificatorium[?] an\nd[ie?] Cammer[?] cum mand\ndieses[?]',
     'notificatorium an\ndie Cammer cum mand.\n[?]',
     'plain on the page (readers 3 and 4); the last mark is a short flourished word and a cross-shaped paraph, not "dieses"'),
    ('0014_a1', 'Haldgass[?] und Leisten', 'Huldigungseid leisten',
     '"Huldigungseid leisten" (readers 3 and 4, Claude), the words of document 11 "den Huldigungseid leisten zu laßen"'),
    ('0014_a1', 'Erschehen sey anhero', 'geschehen sey anhero',
     '"geschehen" (reader 4, Claude), as document 11 "wie solches geschehen anhero zu berichten" (spot sheet)'),
    ('0014_a1', 'zu[?]gejen\n4, Camm[?] Exp. 3[?] [?].\nWoll[?]heit[?]\nInus[?] Man\nv. Maj korden[?]',
     'zeigen\n4, Camm. Exp. 3. [?]\nv. Voss zur Mit¬\n[?] Haug[witz]\n27 May [?]',
     '"zeigen", "v. Voss zur Mit-" and the tailed "Haug" (readers 3 and 4, Claude); "27 Mai" (reader 3, Claude); the rest doubtful'),
    # Document 5: the copy of the joint report
    ('0008_a2', 'bey ihm an¬\n21 Aug.', 'bey ihm am\n21 Aug:',
     '"am" written out, no break, and "Aug:" (reader 2, Claude)'),
    ('0009_a1', 'ergab\ngenen', 'ergan¬\ngenen',
     '"ergan-/genen" (reader 2); "ergab" is no word'),
    ('0009_a1', '[k?]ehrt', 'kehrt', 'the k is plain (reader 2)'),
    ('0009_a1', 'vorgeladen\nwerden,', 'vorgeladen\nworden,',
     '"worden" (reader 2); "ist ... vorgeladen worden" is the one reading'),
    ('0009_a1', 'Confiscationsartel', 'Confiscations Urtel',
     '"Urtel" (reader 2), the word of the next page ("durch das Urtel")'),
    ('0009_a1', 'eiter kein Vermögen', 'weiter kein Vermögen', 'the w is there (reader 2)'),
    ('0009_a1', 'Cujavischen Inserrection', 'Cujavischen Insurrection',
     '"Insurrection" (reader 2), as everywhere in the file'),
    ('0009_a2', 'nun nachher anderweitig', 'und nachher anderweitig', '"und" (reader 2)'),
    ('0009_a2', 'Des Aldels', 'Des Adels', 'no l (reader 2)'),
    ('0009_a2', 'Lebensstrafe\nsagen sie festgesetzt', 'Lebensstrafe\ngegen sie festgesetzt',
     '"noch sonst eine Lebensstrafe gegen sie festgesetzt oder vorbehalten" is the one reading of the sentence (Claude; spot sheet)'),
    ('0009_a2', 'ihrer Theilmann', 'ihrer Theilname',
     '"Theilname" (reader 2), the same word five lines below'),
    ('0009_a2', 'eine Gjährige[?]\nVerbauung', 'eine 9jährige\nVerbannung',
     '"9jährige Verbannung" (reader 2, Claude); the cabinet order (document 6) has "eine neunjährige Verbannung"'),
    ('0009_a2', 'sich meine\nmäßigen', 'sich einer\nmäßigen', '"einer" (reader 2, Claude)'),
    ('0009_a2', 'cha[?]¬\nrecterisirt[?]', 'cha¬\nracterisirt', '"cha-/racterisirt", plain (reader 2)'),
    # Documents 6 to 8: the copies
    ('0011_a2', 'des vormaligen Straßen von', 'des vormaligen Starosten von',
     'the title, as in every other paper of the file (reader 1)'),
    ('0011_a2', 'Goldbeck und Grafen v. Haugwitz.', 'v. Goldbeck und Grafen v. Haugwitz.',
     'the "v." is on the page (reader 1, Claude)'),
    ('0012_a2', 'Vaterland urtheilt,', 'Vaterland ertheilt,',
     '"ertheilt" (reader 1); "die gebetene Erlaubniß ... ertheilt" is the one reading, as in document 6'),
    ('0012_a2', 'Preußen [U?]. A. B. laßen', 'Preußen U. A. H. laßen',
     'the fixed formula "Se. Königl. Majestät von Preußen, Unser allergnädigster Herr, laßen ... bekannt machen"; B for H a Kurrent confusion (Claude; spot sheet)'),
    ('0012_a2', 'Bewunden behalten, auch er der von', 'Bewenden behalten, auch an dem von',
     '"sein Bewenden behalten", the formula; "an dem" (reader 1, Claude)'),
    ('0013_a1', 'Starosten Antoni', 'Starosten Anton', '"Anton" (reader 1, Claude), as in documents 5 to 8'),
    # Documents 9 and 10 (the drafts of 30 May)
    ('0014_a2', 'vom 10t m[c?]. geruhet', 'vom 10t m. c. geruhet', '"m. c." (reader 4)'),
    ('0014_a2', 'erbethe¬\nner Erlaubniß zur Rückkühr', 'erbethe¬\nne Erlaubniß zur Rückkehr',
     '"erbethene" and "Rückkehr" (reader 4; reader 3 for Rückkehr)'),
    ('0014_a2', 'so re¬\nfehle ich', 'so ver¬\nfehle ich',
     '"ver-/fehle" (readers 3 and 4), the formula of documents 2 and 4 ("verfehle ich nicht")'),
    ('0014_a2', 'anheim ab.', 'anheim ob.', '"ob" (readers 3 and 4)'),
    ('0014_a2', 'telß[?] geehrtesten', 'telst geehrtesten', '"mittelst" (reader 3), as "vermittelst" above'),
    ('0014_a2', 'vom 11. m. e. von', 'vom 11. m. c. von', '"m. c." as above (reader 3)'),
    ('0014_a2', 'gewi[?]¬\ntest communicaten', 'geneig¬\ntest communicirten',
     '"geneigtest communicirten" (readers 3 and 4), the words of 0006_a1'),
    ('0015_a1', 'stüge noch', 'füge noch', '"füge" (readers 3 and 4)'),
    ('0015_a1', 'Königl. fl[?]. Nun', 'Königl. Et. Min.',
     '"Et. Min." (readers 3 and 4), the address formula of 0014_a2 ("des König. Et. Min. p von Voss")'),
    ('0015_a1', 'nu[n?]mehro', 'nunmehro', 'plain (reader 3)'),
    ('0015_a1', 'den Huldigungs und ableisten', 'den Huldigungseid ableisten',
     'the "und" is "eid", its i dotted (reader 3, Claude on an enlarged crop); document 11 "den Huldigungseid leisten"'),
    ('0015_a1', '[Haugwitz?]', 'Haug[witz]', 'the same tailed signature as 0006_a1'),
    # Document 11
    ('0016_a2', 'c. als z Post.', 'c. abg. z Post.', '"abg." (reader 3), the office\'s mark for sent (GOVERNMENT_FILES)'),
    ('0016_a2', 'zu ſtertigen', 'zu fertigen', '"fertigen" (readers 3 and 4), as "zufertigen" in document 7'),
    ('0016_a2', 'bestohlen', 'befehlen', '"befehlen" (readers 3 and 4), the formula "befehlen Euch"'),
    ('0016_a2', 'hier p\n', 'Sind p\n', '"Sind p" (readers 3 and 4, Claude), the closing formula of document 7'),
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
        scan = pid.split('_')[0]
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
        courtbook.cut(RAW, scans, SKIP)
    if '--sheet' in arg:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, scans, SKIP, LEAF, note=FOLD_NOTE)
    if '--crop' in arg or '--sheet' in arg:
        return
    pages, corpus, problems = build()
    if problems:
        sys.exit('NOT WRITTEN' + chr(10) + '\n'.join(problems))
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
            f.write('\n'.join(lines) + '\n')
    with open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(corpus)
    print('wrote transcriptions/ and corpus.txt')


if __name__ == '__main__':
    main()
