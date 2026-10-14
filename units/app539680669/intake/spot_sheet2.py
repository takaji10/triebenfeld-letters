# -*- coding: utf-8 -*-
"""The second spot sheet, "More readings in Breyer's notebook" (2026-10-14).

    python units/app539680669/intake/spot_sheet2.py
    python pipeline/review/queries.py --unit app539680669 --sheet readings2.csv

The editor asked for the remaining doubtful readings, the most uncertain of
the 83 left after the first sheet. Chosen: 29 in the body of the
notebook that a name, a place, a field name or the sense of a note rests on.
Left out: the 29 on the two inside covers (pages 2 and 35), which are barely
legible lists, and the 7 in the photograph log, which record only the
subject and the camera's settings; three readings the editor kept with
their doubt on the first sheet (Gullat, 1928, Wolwachówka).

Writes review/app539680669/readings2.csv and a picture for each row in
review/app539680669/spot_img/ (keys s01 ...). A row names its line by a
piece of it (LOCATE) where the word itself is not unique on the page.
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

# (key, page id, a piece of the line, the word as it stands, options, note)
ROWS = [
    ('s01', '0002_a2', '[Lodz.?] Sem.', '[Lodz.?]', '[Lodz.?]|Lodz.|Łódź',
     'The teacher Kampel in Obory: "... Sem." The seminary where he trained; read Lodz. with doubt.'),
    ('s02', '0002_a2', '[Kb.?]-Bücher', '[Kb.?]', '[Kb.?]|Kb.|Ld.|Kr.',
     'The cantor Mathys in Józefów has the records: "...-Bücher ab 1907", books from 1907. Read Kb. (Kirchenbücher, church books) with doubt.'),
    ('s03', '0004_a1', '[Müller?]', '[Müller?]', '[Müller?]|Müller|Mühle',
     'Michalinów: "1 Morgen of meadow for the ...". Read Müller (the miller) with doubt.'),
    ('s04', '0004_a2', 'Wohnhäuser in [?] Fachwerk', '[?]', '[?]',
     '"Dwelling houses in ... half-timbering": a word written above the line, not read.'),
    ('s05', '0005_a1', 'Wirtschaften:', '[Gehege?]', '[Gehege?]|Gehege',
     'In the old German script: a field name of the farms in Łazińsk, read Gehege with doubt.'),
    ('s06', '0005_a1', '[Kavelung?]', '[Kavelung?]', '[Kavelung?]|Kavelung|Kaveln',
     'In the old German script: a field name, "Die ...", read Kavelung (the strips) with doubt.'),
    ('s29', '0005_a1', '„[Rot…?]"', '[Rot…?]', '[Rot…?]|Rotkopp',
     'In the old German script: a field name, the line above "Die ...". Only "Rot" read.'),
    ('s07', '0005_a1', '[Kroge?]', '[Kroge?]', '[Kroge?]|Kroge|Krage',
     'In the old German script: a field name, "Die ...", read Kroge with doubt.'),
    ('s08', '0005_a2', '[grob?]', '[grob?]', '[grob?]|grob',
     '"In Emilienheim they do not speak as ... as in Łazińsk": read grob (coarsely) with doubt.'),
    ('s09', '0008_a1', '[Kühnstubben?]', '[Kühnstubben?]', '[Kühnstubben?]|Kühnstubben|Kienstubben',
     '"Old ... are still found (dug out)": read Kühnstubben with doubt; Kienstubben, pine stumps, would make sense.'),
    ('s10', '0008_a1', '[Lieder?]', '[Lieder?]', '[Lieder?]|Lieder',
     '"1929 ... in the Breslau book": read Lieder (hymns) with doubt.'),
    ('s11', '0010_a2', '[Oborscher?]', '[Oborscher?]', '[Oborscher?]|Oborscher',
     'A nickname: "... Kirschknacker" (cherry-crackers), after "The people of Obory: Hockerling" on the page before. Read Oborscher with doubt.'),
    ('s12', '0010_a2', '[Züchten?]', '[Züchten?]', '[Züchten?]|Züchten',
     '"Of the girls they say ..., marriageable": a dialect word, read Züchten with doubt.'),
    ('s13', '0010_a2', 'in [?].', '[?]', '[?]',
     'The same note: "they say ... in ...", the place where it is said. Not read.'),
    ('s14', '0012_a1', '[Kaveln?]', '[Kaveln?]', '[Kaveln?]|Kaveln',
     'In the old German script: field name no. 3, "Grüne ...", read Kaveln with doubt.'),
    ('s15', '0012_a1', '5) [?]', '[?]', '[?]',
     'In the old German script: field name no. 5. Not read.'),
    ('s16', '0012_a1', '[Gr…berge?]', '[Gr…berge?]', '[Gr…berge?]',
     'In the old German script: field name no. 6. Only "Gr" and "berge" read.'),
    ('s17', '0012_a2', '[gekauft?]', '[gekauft?]', '[gekauft?]|gekauft',
     'In the old German script: "... to Russia. Budendorf ..., 50 years ago." Read gekauft (bought) with doubt.'),
    ('s18', '0012_a2', '[?] Holl. Kein', '[?]', '[?]',
     '"Myślibórz Holland, Węglewo ... Holland. No marsh." The name of a Holland settlement, not read.'),
    ('s19', '0013_a1', '[Smięcer?]', '[Smięcer?]', '[Smięcer?]|Smięcer',
     '"The people in the marsh speak in the ... way, everything short": read Smięcer (of Smięcia) with doubt.'),
    ('s20', '0013_a1', '[Schabeln?]', '[Schabeln?]', '[Schabeln?]|Schabeln',
     '"... do not thrive, poor land": a crop, read Schabeln with doubt.'),
    ('s21', '0014_a1', '[Olszewo?]', '[Olszewo?]', '[Olszewo?]|Olszewo',
     '"How do they speak in Emilienheim? As in Tarszewo, ...?" A village, read Olszewo with doubt.'),
    ('s22', '0014_a1', '[?] i. Brasilien', '[?]', '[?]',
     'After the aunt of Krüger who went to Brazil with her husband: "... in Brazil." A word or two, not read.'),
    ('s23', '0015_a2', '[vorläufig?]', '[vorläufig?]', '[vorläufig?]|vorläufig',
     'Written above "um 1876", under the places of the school community: read vorläufig (provisionally) with doubt.'),
    ('s24', '0015_a2', '[Parkre?]', '[Parkre?]', '[Parkre?]|Parkre',
     '"A son of Schultz\'s in ... is a farmer", after America: a place, read Parkre with doubt.'),
    ('s25', '0016_a1', '[Krainik?]', '[Krainik?]', '[Krainik?]|Krainik',
     '"...: in the village, the only Pole, a shopkeeper, pays no taxes." A name broken across two lines, "Krai-" / "nik", read with doubt.'),
    ('s26', '0018_a1', 'Vor 54 Jahren', '[Sm…?]', '[Sm…?]|Smięcia',
     '"54 years ago from ... to Germany to work." A place; only "Sm" read.'),
    ('s27', '0018_a1', '[Paprot…?]', '[Paprot…?]', '[Paprot…?]',
     '"Neu Czarkow, Briesen, ..., also Brücher": a place; only "Paprot" read.'),
    ('s28', '0018_a1', '[Izbitz?]', '[Izbitz?]', '[Izbitz?]|Izbitz|Izbica',
     '"surveyed: Dornstein, towards ... on the estate Grochowisko": a place, read Izbitz with doubt.'),
]

# Where the line stands lower than the even pitch puts it (in lines), as
# seen on the pictures.
SHIFT = {'s03': 5, 's04': 1, 's06': 2, 's07': 4.5, 's29': 3.5, 's08': 1.5, 's10': 1, 's16': 1, 's21': 3, 's22': 5, 's25': 1}


def main(rows=None, shift=None, sheet='readings2.csv'):
    rows, shift = rows or ROWS, SHIFT if shift is None else shift
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    start = {l[len('[PAGE '):-1]: i for i, l in enumerate(corpus, 1) if l.startswith('[PAGE ')}
    rev = os.path.join(ROOT, 'review', 'app539680669')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for key, pid, locate, word, options, note in rows:
        lines = TEXT[pid].split('\n')
        k = [i for i, l in enumerate(lines) if locate in l]
        assert len(k) == 1, (key, pid, locate, k)
        k = k[0]
        line_no = start[pid] + 1 + k
        assert word in corpus[line_no - 1], (key, corpus[line_no - 1])
        im = Image.open(os.path.join(RAW, 'processed', pid + '.jpg'))
        W, H = im.size
        top, bottom = int(H * 0.06), int(H * 0.95)
        y = top + (bottom - top) * (k + 0.5 + shift.get(key, 0)) / max(len(lines), 18)
        box = (0, max(0, int(y - H * 0.10)), W, min(H, int(y + H * 0.10)))
        name = '%s_%s.jpg' % (key, pid)
        im.crop(box).convert('L').save(os.path.join(img_dir, name), quality=85)
        out.append({'key': key, 'letter': '1', 'line': line_no, 'word': word, 'options': options,
                    'note': note, 'image': name})
    with io.open(os.path.join(rev, sheet), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print(len(out), 'rows')


if __name__ == '__main__':
    main()
