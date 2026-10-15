# -*- coding: utf-8 -*-
"""APŁ 39/98/0/-/6603: the liquidation table of the Łazińsk colony, its copy of 1869 and the later entries.

    python units/apl399806603/intake/holding.py            # check only
    ... --crop        cut each scan to its page edges and join the openings
    ... --sheet       the fold page for the editor (the green lines are the page edges)
    ... --write       page files and corpus.txt from text6603.py
    ... --english     write translation/doc<N>.yml from english6603.py
    ... --cache       put them into the translation cache (after a build)
    ... --summaries   write the summaries S everywhere they are kept

The unit, in the State Archive in Łódź (Archiwum Państwowe w Łodzi), fonds 39/98
"Urząd Gubernialny Kaliski do Spraw Włościańskich" (the Kalisz Governorate
Board for Peasant Affairs), is the file of the liquidation table of the
village "Колонія Лазинская" in the commune of Trąbczyn: 27 scans of the
archive, 000 to 036 (only the written sides were scanned). Added at the
editor's request on 2026-10-15; their notes beside the scans give some
passages in modern spelling with an English rendering, read against the
scans and not used as the text.

Documents (the editor's choice of six, 2026-10-15; the second set of the
table is labelled the copy, as it calls itself one): 1 the liquidation
table, approved by the Central Commission for Peasant Affairs on 8 February
1868 (000 to 014; table); 2 its copy made at Kalisz on 10 September 1869
for the Governorate Government (015 to 029; table); 3 the inscription of
March 1884 on the servitudes of fuel and pasture, entered into the copy
(the end of 028/029 and 030); 4 the certified copy (1900) of the
inscription of 12 October 1894 on the giving up of the servitudes for 393
Morgen of land (031, 032); 5 the certified copy (1901) of the inscription
of 29 November 1897 after the survey of 1896 (033); 6 the statement of each
holding's land after that survey (034 to 036; table).

Pages: the scan's number and side, "0001_a" for scan 001. Where the writing runs across an opening (the
editor: 013/014, 026/027, 028/029; also 016/017, where the servitudes
stand on the right-hand page beside the first entries), the two scans are
cut at their page edges (EDGES; each scan shows a strip of the facing page)
and joined side by side into one page, which takes the left scan's id
("0013_a" for 013 and 014); the right half goes to processed/_not_staged/. The edges are the first proposal: the editor moves
the green lines on the fold page and their saved file wins.

The reading (2026-10-15) was made in session from the scans, each page in
strips at about twice the size: text6603.py, whose docstring has the
conventions. Its checks: copy A's land adds up to the total, 1691 Morgen
219 rods, and its payments to 603 roubles 34⅕ kopecks; every row of the
statement was added across and every column down to the totals at its
foot, which found the misreadings and four slips of the clerk (holding
notes). The English: english6603.py.
"""
import csv
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
from text6603 import DOCS, TABLES  # noqa: E402
from english6603 import TEXT_EN, cell_en  # noqa: E402

SLUG = 'apl399806603'
REF = 'APŁ 39/98/0/-/6603'
RAW = ('J:/Documents/Archive/Genealogy/References/Łódź State Archives/'
       'Ликвидационная табель селения Лазинская Слупецкий уездъ гмина Тромбчинъ (39.98.0.-.6603)')
NUMS = ['000', '001', '003', '005', '007', '009', '011', '013', '014', '015', '016', '017', '018', '020', '022',
        '024', '026', '027', '028', '029', '030', '031', '032', '033', '034', '035', '036']
FILE = '39_98_0_0_6603_%s.jpg'
JOIN = [('013', '014'), ('016', '017'), ('026', '027'), ('028', '029')]
# Page edges, the first proposal (in pixels of the scan): the left page of an
# opening ends at its outer edge, the right one begins after the strip of
# the facing page the scan shows.
EDGES = {FILE % '013': (None, 2730), FILE % '014': (190, None), FILE % '016': (None, 2730), FILE % '017': (90, None),
         FILE % '026': (None, 2726), FILE % '027': (35, None), FILE % '028': (None, 2690), FILE % '029': (100, None)}
PID = lambda n: '%04d_a' % int(n)       # the page id: capture number and side, as match_scans.py reads it
SCANS = [(FILE % n, None, PID(n), None) for n in NUMS]
LEAF = {PID('000'): 'the title page of the table', PID('015'): 'the title page of the copy'}
for a, b in JOIN:
    LEAF[PID(a)] = 'left half of the opening %s/%s' % (a, b)
    LEAF[PID(b)] = 'right half of the opening %s/%s' % (a, b)
FOLD_NOTE = ('The green lines are the page edges; the halves of an opening are joined after cutting. '
             'There is no fold to place: each scan is one page.')

from summaries6603 import S  # noqa: E402
HOW = 'written in the working session from the reading (intake/holding.py, 2026-10-15).'


def join():
    """The halves of each opening, cut at their edges, side by side in one page image."""
    from PIL import Image
    processed = os.path.join(RAW, 'processed')
    apart = os.path.join(processed, '_not_staged')
    os.makedirs(apart, exist_ok=True)
    for a, b in JOIN:
        A = Image.open(os.path.join(processed, PID(a) + '.jpg')).convert('RGB')
        B = Image.open(os.path.join(processed, PID(b) + '.jpg')).convert('RGB')
        J = Image.new('RGB', (A.width + B.width, max(A.height, B.height)), (38, 38, 38))
        J.paste(A, (0, 0))
        J.paste(B, (A.width, 0))
        J.save(os.path.join(processed, PID(a) + '.jpg'), quality=92)
        shutil.move(os.path.join(processed, PID(b) + '.jpg'), os.path.join(apart, PID(b) + '.jpg'))
    print('joined', len(JOIN), 'openings')


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
    """corpus.txt and one file per page."""
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    corpus, whole, order = [], {}, []
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
                    # a cell with a figure of four digits among words is quoted,
                    # as the house forms group the figure (53/968/0/-/716)
                    quote = any(re.search(r'\d{4}', c) and not re.fullmatch(r'[\d\s.,-]*', c) for c in cells)
                    f = io.StringIO()
                    csv.writer(f, lineterminator='', quoting=csv.QUOTE_NONNUMERIC if quote else csv.QUOTE_MINIMAL).writerow(cells)
                    rows.append(f.getvalue())
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
        courtbook.cut(RAW, courtbook.placed(HERE, SCANS, EDGES))
        join()
    if '--sheet' in arg:
        courtbook.fold_sheet(ROOT, SLUG, REF, RAW, courtbook.placed(HERE, SCANS, EDGES), (), LEAF, note=FOLD_NOTE)
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
