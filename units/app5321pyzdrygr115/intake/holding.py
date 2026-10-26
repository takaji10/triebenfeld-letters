# -*- coding: utf-8 -*-
"""APP 53/21/0/-/Pyzdry Gr.115: the editor's transcription of page 543 into the edition.

    python units/app5321pyzdrygr115/intake/holding.py     # check the table
    ... --crop        place the page image (the scan is one page already)
    ... --write       the page file and corpus.txt from table.csv
    ... --correct     apply ROWS, the editor's rulings given in chat (once)
    ... --english     write translation/doc1.yml
    ... --cache       put it into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

The model is APP 53/64/0/-/Kalisz Tab.21
(units/app53640kalisztab21/intake/holding.py), the hearth-tax register: this
holding is one entry of the same kind of source, a table of the parish of
Trąbczyn, on page 543 of the Relationes [protocollon] of 1791-1792.

The folder holds two images. Only 543_trim.jpg is used - the editor's word
(2026-10-26): 542v-543.jpg, the spread, stays out; page 543 is the page of the
unit in focus. The trim is the editor's own crop of the page, so there is no
fold to place and crop_scans.py is not run: cut() copies the one page whole as
0543_a.jpg.

The transcription is intake/table.csv, the editor's file kept as received: one
heading row and seven rows of the parish of Trąbczyn, five cells each. The
only change is ROWS below: the editor ruled in chat (2026-10-26) that the
heading's first cell reads "Parafie"; table.csv keeps their "Parofie" and
--correct applies the ruling and logs it in transcription_decisions.csv.

The table has no column of entry numbers: the parish stands in the first cell
(filled on the village's own row, left empty under it) and the figures follow.
unitlib.table_of sorts such a table with every figure row in the body and the
rows above the first of them in the head (2026-10-26); the check that the
change touches no existing table is pipeline/review/verify_table_of_diff.py.

Only the first half of the page is transcribed - the editor's word: the
relevant information is the table, and the rest of the page belongs to the
entry after it.
"""
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app5321pyzdrygr115'
REF = 'APP 53/21/0/-/Pyzdry Gr.115'
RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Relationes [protocollon] 1791-1792 (53.21.0.-.Pyzdry Gr.115)")

SCANS = [('543_trim.jpg', None, '0543_a', None)]
DOCS = [(1, ['0543_a'])]

# The editor's ruling given in chat (2026-10-26), applied by --correct and
# logged; table.csv keeps their transcription as received.
ROWS = [('0543_a', 'Parofie', 'Parafie',
         'the editor, in chat, 2026-10-26: the heading reads Parafie')]

# The same table in English: the common words rendered, the names as written,
# the two sheaf columns as written until the editor rules what they are.
HEAD_EN = ['Parish', 'Names of towns, villages and demesne farms',
           'Agricultural hearths', 'gara of rye', 'gara owcza']
WORDS = [
    (r'^Wies ', 'Village '),
    (r'^Plebania$', 'The parsonage'),
    (r'^Kuznia ', 'The smithy of '),
    (r'^Hollendry Luzne Stare i nowe z Hutą$',
     'The Hollander settlements scattered, the old and the new, with the Huta'),
]


def table():
    with io.open(os.path.join(HERE, 'table.csv'), encoding='utf-8-sig',
                 newline='') as f:
        return [r for r in csv.reader(f) if r]


def line(cells):
    out = io.StringIO()
    csv.writer(out, lineterminator='').writerow(cells)
    return out.getvalue()


def read_source():
    """The table as the page carries it: the heading row opens the page."""
    return {(1, '0543_a'): [line(r) for r in table()]}


def check(rows):
    """The shape of the table, and the doubling of the figures.

    In six of the seven rows the figures double from column to column
    (h, 2h, 4h); the village's own row reads 21, 22, 84, where the doubling
    would give 42. Figures are never corrected from arithmetic: the row stands
    as written and the editor is to resolve it (2026-10-26).
    """
    bad = []
    if len(rows) != 8:
        bad.append(f'{len(rows)} rows, 8 expected (the heading and seven)')
    for i, r in enumerate(rows):
        if len(r) != 5:
            bad.append(f'row {i} has {len(r)} cells, 5 expected')
    doubles = 0
    for r in rows[1:]:
        a, b, c = (int(x) for x in r[2:5])
        if b == 2 * a and c == 2 * b:
            doubles += 1
        else:
            print(f'  not doubled: {r[1]}: {a}, {b}, {c}')
    print(f'{doubles} of {len(rows) - 1} rows double from column to column')
    return bad


def en_words(s):
    for pat, new in WORDS:
        s = re.sub(pat, new, s)
    return s


def english():
    """The English of the table, in the shape the translator saves."""
    rows = table()
    out = [line(HEAD_EN)]
    for r in rows[1:]:
        out.append(line([r[0], en_words(r[1]), r[2], r[3], r[4]]))
    return {1: ['\n'.join(out)]}


# ---------------------------------------------------------------- the summaries

S = {
 1: ('Seite 543 des Relationes [protocollon] von 1791-1792, des Registers des '
     'Burggerichts und -amts Pyzdry: der Kopf einer Tabelle der Pfarrei '
     'Trąbczyn, auf des Herausgebers eigenem Zuschnitt der fotografierten '
     'Seite, in polnischer Sprache. Die Tabelle hat fünf Spalten: die Pfarrei '
     '(„Parofie“, für Parafie), die Namen der Städte, Dörfer und Vorwerke, die '
     'Rauchfangstände (dymy rolne) und zwei Spalten von Abgaben, die ihre '
     'Köpfe „gara zyta“ und „gara owcza“ nennen. Sieben Zeilen stehen unter '
     'der Pfarrei Trąbczyn: das Dorf Trąbczyn selbst mit 21 Rauchfangständen, '
     '22 und 84; die Pfarrei (Plebania) mit 4, 8 und 16; Nowawieś mit 5, 10 '
     'und 20; Osiny mit 6, 12 und 24; Łazy mit 5, 10 und 20; Kuznia '
     'Maryantów, die Schmiede, mit 1, 2 und 4; und Hollendry Luzne Stare i '
     'nowe z Hutą, die verstreuten Holländersiedlungen alte und neue mit der '
     'Huta, mit 31, 62 und 124. In jeder Zeile außer der ersten verdoppeln '
     'sich die Zahlen von Spalte zu Spalte; in der ersten steht in der '
     'mittleren Spalte 22, wo die Verdoppelung 42 gäbe - als geschrieben '
     'behalten. Die Tabelle trägt kein Datum; sie steht auf der Seite 543 '
     'eines Registerbandes, dessen Titel die Jahre 1791 bis 1792 nennt.',
     'Page 543 of the Relationes [protocollon] of 1791-1792, the register of '
     'the grod court and office of Pyzdry: the head of a table of the parish '
     'of Trąbczyn, on the editor\'s own trim of the photographed page, in '
     'Polish. The table has five columns: the parish (Parofie, for Parafie), '
     'the names of the towns, villages and demesne farms, the agricultural '
     'hearths (dymy rolne), and two columns of dues whose headings read gara '
     'zyta and gara owcza. Seven rows stand under the parish of Trąbczyn: the '
     'village of Trąbczyn itself with 21 hearths, 22 and 84; the parsonage '
     '(Plebania) with 4, 8 and 16; Nowawieś with 5, 10 and 20; Osiny with 6, '
     '12 and 24; Łazy with 5, 10 and 20; Kuznia Maryantów, the smithy, with '
     '1, 2 and 4; and Hollendry Luzne Stare i nowe z Hutą, the scattered '
     'Hollander settlements old and new with the Huta, with 31, 62 and 124. '
     'In every row but the first the figures double from column to column; in '
     'the first the middle figure is read 22 where the doubling would give '
     '42 - kept as written. The table carries no date; it stands on page 543 '
     'of a register volume whose title names the years 1791 to 1792.'),
}
HOW = ('written in the working session from the editor\'s transcription '
       '(intake/table.csv, 2026-10-26).')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    rows = table()
    bad = check(rows)
    if bad:
        for b in bad:
            print('  ', b)
        sys.exit('the table does not have the shape expected')
    if '--crop' in arg:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS))
    if '--write' in arg:
        assert not os.path.exists(os.path.join(UNIT_DIR, 'transcription_decisions.csv')), \
            'corrections are already logged: --write would put the uncorrected text back'
        courtbook.write_pages(UNIT_DIR, DOCS, read_source())
    if '--correct' in arg:
        courtbook.correct(UNIT_DIR, SLUG, DOCS, ROWS, True,
                          source='the editor, in chat')
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
