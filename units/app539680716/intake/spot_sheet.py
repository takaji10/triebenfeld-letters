# -*- coding: utf-8 -*-
"""The spot sheet "Readings in Breyer's Łazińsk notebook" (2026-10-14).

    python units/app539680716/intake/spot_sheet.py
    python pipeline/review/queries.py --unit app539680716 --sheet readings.csv

The readings of the 68 marks of doubt that a name, a place, a heading or the
sense of a note rests on, each with a picture of its line (the machinery of
53/968/0/-/669's spot_sheet2.py, for a holding whose pages can stand under
two documents). Left out: the names in the Russian tables that only one
letter or the ending makes doubtful, and the pencil additions of 1875 in the
Łazińsk table; they are listed in the holding's notes.

Writes review/app539680716/readings.csv and a picture for each row in
review/app539680716/spot_img/. A row names its line by a piece of it.
"""
import csv
import io
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, HERE)
from photos import RAW  # noqa: E402

# (key, document, page id, a piece of the line, the word as it stands, options, note)
ROWS = [
    ('r01', 1, '5160_a', '[7.?] 1858', '[7.?]', '[7.?]|7.|1.',
     'The loose sheet of 1858, its first line, above "Emilienheim": a figure before the year, read 7. with doubt. It may be a number or a month.'),
    ('r02', 3, '5165_a1', '[переименов.?]', '[переименов.?]', '[переименов.?]|переименов.',
     'Breyer\'s note on Emilienheim, in Russian: "The Kalisz governorate board ... 29 Sept. 1892 Emilienheim to the local name Michalinów." The word was read переименов. (renamed) with doubt; the summary does not rest on it.'),
    ('r03', 4, '5165_a1', '[Тромбчинъ?]', '[Тромбчинъ?]', '[Тромбчинъ?]|Тромбчинъ',
     'The heading of the Łazińsk table, in Russian: "... Pyzdry circuit, commune ...". The last word, the commune, read Тромбчинъ (Trąbczyn) with doubt.'),
    ('r04', 5, '5169_a2', '[паленный?]', '[паленный?]', '[паленный?]|паленный',
     'The servitudes of Łazińsk, in Russian: "to graze all their ... cattle in the forest Studzianki". A word before "cattle", read паленный with doubt; the sense is not clear.'),
    ('r05', 7, '5172_a2', '[Jäke?], Becker', '[Jäke?]', '[Jäke?]|Jäke',
     'Notes of July 1935: "In Józefów ..., Becker, Wegert, ... the first farmers." The first surname, read Jäke with doubt.'),
    ('r06', 7, '5172_a2', '[Jesswein?]', '[Jesswein?]', '[Jesswein?]|Jesswein',
     'The same line: the last of the first farmers of Józefów, read Jesswein with doubt.'),
    ('r07', 7, '5173_a1', '[Mądrosza?]', '[Mądrosza?]', '[Mądrosza?]|Mądrosza',
     'A list of places: "Czarny Bród, Little Orlin, Great Orlin, ..., Bystrzyca". A place, read Mądrosza with doubt.'),
    ('r08', 7, '5173_a2', '[Hufe?] an 40', '[Hufe?]', '[Hufe?]|Hufe',
     '"In Little Orlin 1 ... each to 40 farmers": a measure of land, read Hufe with doubt.'),
    ('r09', 7, '5173_a2', '[Holędry?] Orliny', '[Holędry?]', '[Holędry?]|Holędry',
     'The heading over Breyer\'s notes on thieving, poverty and marriages: "... Orliny Biskupicki". The first word, read Holędry with doubt. It says which village the notes are about.'),
    ('r10', 7, '5174_a1', '[Zwrsze?]', '[Zwrsze?]', '[Zwrsze?]',
     '"The German fellow countrymen robbed the teacher on ...": a word, perhaps a place, read Zwrsze with doubt.'),
    ('r11', 8, '5174_a2', 'Orliner Hauland', '[?] von dem Orliner Hauland Biskupice [?] [?] [?] [?] [?]',
     '[?] von dem Orliner Hauland Biskupice [?] [?] [?] [?] [?]|[?] von dem Orliner Hauland Biskupice gehörig, sämtlich auf das Buch [?]',
     'The heading of the list of farmers with their Morgen, four lines in the old German script at the top of the page. Read: "... von dem Orliner Hauland Biskupice ..." (of the Orlin Hauland Biskupice). Read again on a closer picture: "gehörig, sämtlich auf das Buch ..." (belonging, all in the book ...), offered as the second choice. The first word, a long one, and the end of the last line are not read; please type what you can.'),
    ('r12', 8, '5175_a1', '[Skrzydlewski?]', '[Skrzydlewski?]', '[Skrzydlewski?]|Skrzydlewski',
     'The list of farmers of Orlin, no. 14, 28 Morgen: a surname, read Skrzydlewski with doubt.'),
    ('r13', 8, '5175_a2', '[Tilson?]', '[Tilson?]', '[Tilson?]|Tilson',
     'The same list, no. 31, 7 Morgen: a surname, read Tilson with doubt.'),
    ('r14', 8, '5176_a1', '[Seling?]', '[Seling?]', '[Seling?]|Seling',
     'The same list, an unnumbered entry, 7 Morgen: a surname, read Seling with doubt.'),
    ('r15', 8, '5176_a1', '[Rohrfuss?]', '[Rohrfuss?]', '[Rohrfuss?]|Rohrfuss',
     'The same list, an unnumbered entry, 18 Morgen: a surname, read Rohrfuss with doubt.'),
    ('r16', 8, '5176_a1', '[Jaschek?]', '[Jaschek?]', '[Jaschek?]|Jaschek',
     'The same list, an unnumbered entry, 15 Morgen: a surname, read Jaschek with doubt.'),
    ('r17', 9, '5176_a1', '[gemorden?]', '[gemorden?]', '[gemorden?]|geworden',
     'Notes on Orlin: "Because of the wet years in Orlin bankrupt ...". The last word, read gemorden with doubt; geworden (became) would make sense.'),
]

# Where the line stands lower than the even pitch puts it (in lines), as
# seen on the pictures.
SHIFT = {'r01': -1.5, 'r03': 4.5, 'r04': 2, 'r07': 4, 'r09': 3.5, 'r13': 1, 'r14': 0.5, 'r15': 0.5, 'r16': 0.7, 'r17': 3}
# Where a row's picture is set by hand: the middle and half the height, as
# parts of the page (the heading of the Orlin list is four lines at the top
# of a page whose other column carries the end of document 7).
BOX = {'r11': (0.19, 0.13)}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    rev = os.path.join(ROOT, 'review', 'app539680716')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for key, doc, pid, locate, word, options, note in ROWS:
        # the corpus line: within the document, within the page
        d = p = None
        hits = []
        for i, l in enumerate(corpus, 1):
            if l.startswith('[DOC '):
                d = l[5:].split(']')[0].strip()
            elif l.startswith('[PAGE '):
                p = l[6:-1]
            elif d == str(doc) and p == pid and locate in l:
                hits.append(i)
        assert len(hits) == 1, (key, hits)
        line_no = hits[0]
        assert word in corpus[line_no - 1], (key, corpus[line_no - 1])
        # the picture: the line's place among the page's lines
        lines = [l for l in io.open(os.path.join(UNIT_DIR, 'transcriptions', pid + '.txt'),
                                    encoding='utf-8').read().split('\n') if l.strip()]
        k = [i for i, l in enumerate(lines) if locate in l]
        assert len(k) == 1, (key, pid, k)
        k = k[0]
        im = Image.open(os.path.join(RAW, 'processed', pid + '.jpg'))
        W, H = im.size
        top, bottom = int(H * 0.06), int(H * 0.95)
        y = top + (bottom - top) * (k + 0.5 + SHIFT.get(key, 0)) / max(len(lines), 18)
        half = 0.10
        if key in BOX:
            y, half = H * BOX[key][0], BOX[key][1]
        box = (0, max(0, int(y - H * half)), W, min(H, int(y + H * half)))
        name = '%s_%s.jpg' % (key, pid)
        im.crop(box).convert('L').save(os.path.join(img_dir, name), quality=85)
        out.append({'key': key, 'letter': str(doc), 'line': line_no, 'word': word, 'options': options,
                    'note': note, 'image': name})
    with io.open(os.path.join(rev, 'readings.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print(len(out), 'rows')


if __name__ == '__main__':
    main()
