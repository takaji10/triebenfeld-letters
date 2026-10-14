# -*- coding: utf-8 -*-
"""The spot sheet "Readings in Breyer's notebook" for the editor (2026-10-14). Answered the same
day; the answers are in TEXT (holding.py docstring). The ROWS below are the questions as asked.

    python units/app539680669/intake/spot_sheet.py
    python pipeline/review/queries.py --unit app539680669 --sheet readings.csv

Writes review/app539680669/readings.csv and a picture for each row in
review/app539680669/spot_img/. Only the readings a name, a date or a number
rests on; the inside covers, which are barely legible, are not asked about
line by line. The picture is cut round the line's place on the page,
worked out from its position among the page's lines, so it shows that line
and a few round it.
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
from holding import RAW, TEXT  # noqa: E402

# (key, page id, the word as it stands, options, note)
ROWS = [
    ('r01', '0005_a2', '[Wagels?]', '[Wagels?]|Wagels',
     'Old Krüger has made over 4 Morgen of land to his daughter, "to" someone: a surname, read Wagels with doubt.'),
    ('r02', '0008_a1', '[IV?]', '[IV?]|IV|VI|XI',
     'The gravestone of Agnes Schütz, née Neumann, in the cemetery of Józefów: born 17 ... 1832. The month in Roman figures, read IV (April) with doubt.'),
    ('r03', '0011_a2', '[Halwege?]', '[Halwege?]|Halwege|halwege',
     '"Was ... war, ging nach Deutschland": read as halwege (Low German for halfway, the halfway well-off), with doubt.'),
    ('r04', '0012_a2', '[Gullat?]', '[Gullat?]|Gullat',
     'In the old German script: "Ein ..., Hossmann nach Russland." A surname, read Gullat with doubt.'),
    ('r05', '0012_a2', '[Hossmann?]', '[Hossmann?]|Hossmann',
     'The same line: the second surname, read Hossmann with doubt.'),
    ('r06', '0015_a1', '[1928?]', '[1928?]|1928|1888',
     'Old Schultz, teacher and cantor: 1889 to ... The second year is written over; read 1928.'),
    ('r07', '0015_a1', '18[?]9', '18[?]9|1829|1839',
     'The teacher Neumann L.: 18.9 to 1849. The third figure was not read.'),
    ('r08', '0015_a2', '[Wlodziemen?]', '[Wlodziemen?]|Wlodziemen|Włodzimierow',
     'The places of the school community: Augustynów, ..., Michalinów, Drzewce. Read Wlodziemen; it may be meant for Włodzimierow, the parcelled manor (page 26 of the notebook).'),
    ('r09', '0015_a2', '[Wolwachówka?]', '[Wolwachówka?]|Wolwachówka',
     'Four brothers of Schulz emigrated to Volhynia, "in the neighbourhood of ..., district of Żytomierz". A place, read Wolwachówka with doubt.'),
    ('r10', '0005_a2', '[Bärwinkel?]', '[Bärwinkel?]|Bärwinkel',
     'A field name at the head of the page, read Bärwinkel with doubt; the same name is plain on the next opening (page 13).'),
]

# Where the line stands lower than the even pitch puts it (in lines), as
# seen on the pictures: the gravestone lines and the foot of 0011_a2.
SHIFT = {'r02': 1.5, 'r03': 2.5}


def page_lines(pid):
    return TEXT[pid].split('\n')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    start = {l[len('[PAGE '):-1]: i for i, l in enumerate(corpus, 1) if l.startswith('[PAGE ')}
    rev = os.path.join(ROOT, 'review', 'app539680669')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for key, pid, word, options, note in ROWS:
        lines = page_lines(pid)
        k = [i for i, l in enumerate(lines) if word in l]
        assert len(k) == 1, (key, pid, word, k)
        k = k[0]
        line_no = start[pid] + 1 + k
        assert word in corpus[line_no - 1], (key, corpus[line_no - 1])
        im = Image.open(os.path.join(RAW, 'processed', pid + '.jpg'))
        W, H = im.size
        top, bottom = int(H * 0.06), int(H * 0.95)
        # one line of writing to a ruled line; a full page has about 18, and a
        # page written only at the top has its lines at the same pitch
        y = top + (bottom - top) * (k + 0.5 + SHIFT.get(key, 0)) / max(len(lines), 18)
        box = (0, max(0, int(y - H * 0.10)), W, min(H, int(y + H * 0.10)))
        name = '%s_%s.jpg' % (key, pid)
        im.crop(box).convert('L').save(os.path.join(img_dir, name), quality=85)
        out.append({'key': key, 'letter': '1', 'line': line_no, 'word': word, 'options': options,
                    'note': note, 'image': name})
    with io.open(os.path.join(rev, 'readings.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print(len(out), 'rows')


if __name__ == '__main__':
    main()
