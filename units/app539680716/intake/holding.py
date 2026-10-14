# -*- coding: utf-8 -*-
"""APP 53/968/0/-/716: Albert Breyer's notebook on Łazińsk, Emilienheim and Orlin, with a loose sheet of 1858.

    python units/app539680716/intake/holding.py            # check only
    ... --crop        cut the page images (photos.py first)
    ... --sheet       the fold page for the editor
    ... --write       page files and corpus.txt from text716.py
    ... --english     write translation/doc<N>.yml from english716.py
    ... --cache       put them into the translation cache (after a build)
    ... --summaries   write the summaries S everywhere they are kept

The unit (archive's title: "Łazińsk [pow. słupecki, woj. poznańskie -
notatki, statystyka] 1937") is a school exercise book of Breyer's, with a
loose sheet of 1858 laid in it. The editor photographed it in April 2023
(IMG_5159 to IMG_5180, raw files; photos.py makes the page images). IMG_5159
shows the archive's title page beside the notebook and the sheet: only the
title page is taken from it (editor, 2026-10-14).

What the notebook holds. Breyer copied into it, in Russian, the liquidation
tables of 1868 by which the peasants of Emilienheim, Łazińsk and Orliny were
given their land under the ukase of 1864, with the terms of their
servitudes in the forest; added in pencil who held the Łazińsk holdings in
1875, and the numbers of farmers and Morgen from 1840 to 1935; and wrote
his own notes of July 1935 and July 1936 in Orlin, Józefów and Obory. The
loose sheet is the Polish list of hearth tax due from the colony of
Emilienheim, dated at Kopojno on 3/15 December 1858 by the wójt.

Documents (by content, the editor's choice, 2026-10-14): 1 the sheet of
1858 (table); 2 the Emilienheim table (table); 3 notes on Emilienheim of
1870 and 1892; 4 the Łazińsk table (table); 5 the Łazińsk servitudes and
Breyer's counts; 6 farmers and Morgen of Łazińsk 1840 to 1935 (table); 7
Breyer's notes of 1935 on Huta Trąbczyńska, Orlin, Józefów and Obory; 8 the
farmers of Orlin and their Morgen (table); 9 notes on Orlin of 1936; 10 the
Orliny table (table); 11 Breyer's notes on the separation and the Orliny
servitudes. A page that holds the end of one and the start of the next
stands under both.

Pages: the photo number and the side. Front matter: 5159_a (the archive's
title page) and 5162_a (the notebook's cover: "Łazinsk", "Emilienheim",
"Ликвидац. табель" in coloured pencil, on a printed school-book form whose
blank fields and the printed "ZŁÓŻ GROSZ NA BUDOWĘ SZKÓŁ POWSZECHNYCH" are
not transcribed). The inside front cover (5163_a1) is blank; IMG_5168
repeats the opening of IMG_5169 and is not used; 5180_a is the last page,
the inside back cover beside it not photographed whole.

The reading (2026-10-14) was made in session from the photos, each page in
three strips at about three times the size: text716.py, whose docstring has
the conventions. The English: english716.py.
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
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
from photos import PHOTOS, RAW  # noqa: E402
from text716 import DOCS, FRONT, TABLES  # noqa: E402
from english716 import TEXT_EN, cell_en  # noqa: E402

SLUG = 'app539680716'
REF = 'APP 53/968/0/-/716'

# x of the fold in each cut photo (courtbook.find_fold, checked by eye)
FOLDS = {5163: 1612, 5164: 1651, 5165: 1634, 5166: 1609, 5167: 1617, 5169: 1601, 5170: 1606, 5171: 1645,
         5172: 1624, 5173: 1638, 5174: 1662, 5175: 1661, 5176: 1660, 5177: 1670, 5178: 1693, 5179: 1694}
SINGLE = (5159, 5160, 5161, 5162, 5180)
SKIP = {'5163_a1'}
SCANS = ([(PHOTOS + '/IMG_%d.jpg' % n, None, '%d_a' % n, None) for n in SINGLE]
         + [(PHOTOS + '/IMG_%d.jpg' % n, x, '%d_a1' % n, '%d_a2' % n) for n, x in sorted(FOLDS.items())])
LEAF = {'5159_a': "the archive's title page", '5162_a': 'the cover', '5160_a': 'the loose sheet, front',
        '5161_a': 'the loose sheet, back'}
FOLD_NOTE = 'Both halves are pages of the edition, except the blank inside front cover (5163, left).'

from summaries716 import S  # noqa: E402
HOW = 'written in the working session from the reading (intake/holding.py, 2026-10-14).'


def rows_to_csv(block):
    out = []
    for line in block.split('\n'):
        f = io.StringIO()
        csv.writer(f, lineterminator='').writerow(line.split('|'))
        out.append(f.getvalue())
    return out


def lines_of(n, block):
    return rows_to_csv(block) if n in TABLES else block.split('\n')


def write():
    """corpus.txt and one file per page: the front matter first, then the documents."""
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    corpus, whole, order = [], {}, []
    for pid, lines in FRONT:
        corpus += ['[PAGE %s]' % pid] + lines
        whole[pid] = list(lines)
        order.append(pid)
    for n in sorted(DOCS):
        corpus.append('[DOC %d]' % n)
        for pid, block in DOCS[n]:
            lines = lines_of(n, block)
            corpus += ['[PAGE %s]' % pid] + lines
            if pid not in whole:
                whole[pid] = []
                order.append(pid)
            whole[pid] += lines
    for pid in order:
        io.open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(whole[pid]) + '\n')
    io.open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(corpus) + '\n')
    print('wrote', len(order), 'page files and corpus.txt')


def english():
    out = {}
    for n in sorted(DOCS):
        pages = []
        for pid, block in DOCS[n]:
            if n in TABLES:
                rows = []
                for line in block.split('\n'):
                    cells = [cell_en(c, k) for k, c in enumerate(line.split('|'))]
                    f = io.StringIO()
                    csv.writer(f, lineterminator='').writerow(cells)
                    row = f.getvalue()
                    # The house forms group a figure of four digits in a
                    # sentence ("4420 roubles" -> "4,420 roubles"), which in an
                    # unquoted cell would split it: such cells are quoted.
                    if any(re.search(r'\d{4}', c) and not re.fullmatch(r'[\d\s.,-]*', c) for c in cells):
                        f = io.StringIO()
                        csv.writer(f, lineterminator='', quoting=csv.QUOTE_NONNUMERIC).writerow(cells)
                        row = f.getvalue()
                    rows.append(row)
                pages.append('\n'.join(rows))
            else:
                pages.append(TEXT_EN[(n, pid)])
        out[n] = pages
    return out


def check():
    marks = 0
    for n in sorted(DOCS):
        for pid, block in DOCS[n]:
            if n not in TABLES:
                assert (n, pid) in TEXT_EN, (n, pid)
            marks += block.count('?]')
    print(len(DOCS), 'documents,', sum(len(v) for v in DOCS.values()), 'document pages,', marks, 'marks of doubt')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    check()
    if '--crop' in arg:
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS), skip=SKIP)
    if '--sheet' in arg:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS), SKIP, LEAF, note=FOLD_NOTE)
    if '--write' in arg:
        write()
    if '--english' in arg:
        tdir = os.path.join(HERE, 'translation')
        os.makedirs(tdir, exist_ok=True)
        for n, pages in english().items():
            courtbook.write_doc_yml(os.path.join(tdir, 'doc%d.yml' % n), pages)
    if '--cache' in arg:
        courtbook.save_cache(ROOT, SLUG, os.path.join(HERE, 'translation'))
    if '--summaries' in arg:
        courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S, HOW)


if __name__ == '__main__':
    main()
