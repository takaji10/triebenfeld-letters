# -*- coding: utf-8 -*-
"""APŁ 39/98/0/-/1333: the index of the file on the liquidation tables of Trąbczyn, a plan of 1865 and four petitions.

    python units/apl399801333/intake/holding.py            # check only
    ... --crop        copy the scans into processed/ under their page ids (the plan turned upright)
    ... --write       page files and corpus.txt (index.csv and text1333.py)
    ... --english     write translation/doc<N>.yml (index.csv and english1333.py)
    ... --cache       put them into the translation cache (after a build)
    ... --summaries   write the summaries S everywhere they are kept

The unit, in the State Archive in Łódź (Archiwum Państwowe w Łodzi), fonds 39/98
"Urząd Gubernialny Kaliski do Spraw Włościańskich", is the first part of the
file "О составлении ликвидационных табелей по имению Тромбчин владельца
Миончинскаго, Слупецкаго уезда" (on the drawing up of the liquidation tables
of the estate of Trąbczyn, owner Miączyński, Słupca district). The editor
photographed the file's index (14 scans, 39_98_0_0_1333_001 to _014) and
some of the papers it lists, named by their number in the index and their
folio (No.59_..._88.jpg); the folder's map image (_mapa.jpg) is not used.

Documents (the editor's choice, 2026-11-13):
1 the index ("Опись бумагамъ, къ дѣлу № 167"), 145 entries, 1864-1870, a
  table (scans 001-014, pages 0001_a-0014_a);
2 the plan of the village of Trąbczyn, 15 May 1865 (index no. 30, folio 41,
  page 0041_a), shown as an image and not transcribed;
3 Count Włodzimierz Miączyński's petition of 10/22 August 1865 on six
  farmsteads of Nowa Wieś (no. 59, folios 88-89v);
4 his petition of 23 July 1865 against the servitude of pasture granted to
  Krystian Lippeldt (no. 75, folios 113-115v; the image named 116 is 115v);
5 the petition of the colonists of Łazińsk of 6/18 December 1867 (no. 102,
  folio 163);
6 the petition of the colonists of Łazińsk of 10/22 August 1868 (no. 112,
  folios 176-177v).

Page ids: the index pages "0001_a" to "0014_a" (the scan's number); the
others the folio and the side, "0088_a" for 88, "0088_b" for 88 verso.

The readings: the index in review (two Sonnet readers and Claude's rulings,
2026-11-13), kept as intake/index.csv with its English, the state of each
entry (both readers / ruled / open) and the note; the letters in
text1333.py, whose docstring says where each part of the text comes from.
The English: english1333.py. The summaries: summaries1333.py.
"""
import csv
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
from text1333 import DOCS as LETTERS, PLAN  # noqa: E402
from english1333 import TEXT_EN, HEAD_EN  # noqa: E402

SLUG = 'apl399801333'
REF = 'APŁ 39/98/0/-/1333'
RAW = ('J:/Documents/Archive/Genealogy/References/Łódź State Archives/'
       'О составлении ликвидационных... Тромбчин, Слупецкаго уезда ч. I (39.98.0.-.1333)')

# raw file -> page id
SCANS = {'39_98_0_0_1333_%03d.jpg' % n: '%04d_a' % n for n in range(1, 15)}
for name, pid in [('No.30_39_98_0_0_1333_41.jpg', '0041_a'),
                  ('No.59_39_98_0_0_1333_88.jpg', '0088_a'), ('No.59_39_98_0_0_1333_88v.jpg', '0088_b'),
                  ('No.59_39_98_0_0_1333_89.jpg', '0089_a'), ('No.59_39_98_0_0_1333_89v.jpg', '0089_b'),
                  ('No.75_39_98_0_0_1333_113.jpg', '0113_a'), ('No.75_39_98_0_0_1333_113v.jpg', '0113_b'),
                  ('No.75_39_98_0_0_1333_114.jpg', '0114_a'), ('No.75_39_98_0_0_1333_114v.jpg', '0114_b'),
                  ('No.75_39_98_0_0_1333_115.jpg', '0115_a'), ('No.75_39_98_0_0_1333_116.jpg', '0115_b'),
                  ('No.102_39_98_0_0_1333_163.jpg', '0163_a'),
                  ('No.112_39_98_0_0_1333_176.jpg', '0176_a'), ('No.112_39_98_0_0_1333_176v.jpg', '0176_b'),
                  ('No.112_39_98_0_0_1333_177.jpg', '0177_a'), ('No.112_39_98_0_0_1333_177v.jpg', '0177_b')]:
    SCANS[name] = pid
TURN = {'0041_a': 180}       # the plan was photographed upside down

TABLES = {1}
HEAD = [['', 'Опись бумагамъ, къ дѣлу № 167', '', ''],
        ['№ по порядку', 'Отъ кого бумага поступила; число и номеръ бумаги', 'На сколькихъ листахъ',
         '№№ страницъ въ дѣлѣ']]

from summaries1333 import S  # noqa: E402
HOW = 'written in the working session from the settled text (intake/holding.py, 2026-11-13).'


def index_rows():
    """{page id: [row cells]} of the index, from intake/index.csv; and the same in English."""
    ru, en = {}, {}
    with io.open(os.path.join(HERE, 'index.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            ru.setdefault(r['page'], []).append([r['no'], r['russian'], r['leaves'], r['folio']])
            en.setdefault(r['page'], []).append([r['no'], r['english'], r['leaves'], r['folio']])
    return ru, en


def csv_line(cells):
    f = io.StringIO()
    csv.writer(f, lineterminator='').writerow(cells)
    return f.getvalue()


def docs():
    """{document: [(page id, [lines])]} for the whole holding, the index first."""
    ru, _ = index_rows()
    out = {1: []}
    for k, pid in enumerate(sorted(ru)):
        rows = (HEAD if k == 0 else []) + ru[pid]
        out[1].append((pid, [csv_line(r) for r in rows]))
    for n, pages in LETTERS.items():
        out[n] = [(pid, text.split('\n')) for pid, text in pages]
    return out


def crop():
    """Each scan into processed/<page id>.jpg, turned where TURN says."""
    from PIL import Image
    processed = os.path.join(RAW, 'processed')
    os.makedirs(processed, exist_ok=True)
    for name, pid in SCANS.items():
        dst = os.path.join(processed, pid + '.jpg')
        if pid in TURN:
            Image.open(os.path.join(RAW, name)).rotate(TURN[pid], expand=True).save(dst, quality=92)
        else:
            shutil.copyfile(os.path.join(RAW, name), dst)
    print('copied', len(SCANS), 'scans into processed/')


def write():
    """corpus.txt and one file per page."""
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    corpus = []
    for n, pages in sorted(docs().items()):
        corpus.append('[DOC %d]' % n)
        for pid, lines in pages:
            corpus += ['[PAGE %s]' % pid] + lines
            io.open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    io.open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(corpus) + '\n')
    print('wrote', sum(len(p) for p in docs().values()), 'page files and corpus.txt')


def english():
    _, en = index_rows()
    out = {1: []}
    for k, pid in enumerate(sorted(en)):
        rows = ([HEAD_EN[:4], HEAD_EN[4:]] if k == 0 else []) + en[pid]
        out[1].append('\n'.join(csv_line(r) for r in rows))
    for n, pages in LETTERS.items():
        out[n] = [TEXT_EN[(n, pid)] for pid, _ in pages]
    return out


def check():
    d = docs()
    for n, pages in LETTERS.items():
        for pid, _ in pages:
            assert (n, pid) in TEXT_EN, (n, pid)
    assert set(SCANS.values()) == {pid for pages in d.values() for pid, _ in pages}, 'scans and pages differ'
    marks = sum(line.count('?]') for pages in d.values() for _, lines in pages for line in lines)
    print(len(d), 'documents,', sum(len(v) for v in d.values()), 'pages,', marks, 'marks of doubt')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    arg = sys.argv[1:]
    check()
    if '--crop' in arg:
        crop()
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
