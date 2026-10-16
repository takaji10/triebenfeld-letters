# -*- coding: utf-8 -*-
"""The spot sheet "Doubtful readings in the visitation of Trąbczyn" (2026-10-15).

    python units/adwl85/intake/spot_sheet.py
    python pipeline/review/queries.py --unit adwl85 --sheet readings.csv

All 12 marks of doubt in the holding, one row each, with a picture of the
place on the page. The picture is a box drawn on the page by eye (BOX: left,
top, right, bottom as parts of the page), found on enlarged strips of the
page. The first option of each row is what is built.

Writes review/adwl85/readings.csv and a picture for each row in
review/adwl85/spot_img/. A row names its line by a piece of it.
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
from holding import RAW  # noqa: E402

T = 'The parish of Trąbczyn (document 1), '
G = (' In this hand a capital G and a capital J look much alike: compare "Gnieznin:" and "Gniezna" on the '
     'same pages.')

# (key, document, page id, a piece of the line, the word as it stands, options, note, box)
ROWS = [
    ('s01', 1, '0023_b', 'Sariusza Kozierok[?]', 'Kozierok[?]', 'Kozierok[?]|Kozierok|struck out',
     T + 'leaf 23 verso, the bishop who ordained the priest: "Ignacego Augustyna Sariusza ... Kozierowskiego". '
     'The word at the start of the line before Kozierowskiego looks like "Kozierok", perhaps a first try at the '
     'name that the scribe abandoned. If it is struck out, the edition leaves it out.',
     (0, 0.525, 0.62, 0.585)),
    ('s02', 1, '0024_a', 'Folwark Uta[?] zwany', 'Uta[?]', 'Uta[?]|Uta|Ula',
     T + 'leaf 24, the villages of the parish: "Folwark ... zwany", the farm called ... Your transcript has '
     '"Uta"; the second letter could be t or l.',
     (0, 0.535, 0.62, 0.585)),
    ('s03', 1, '0024_b', 'oboki[?] od strony', 'oboki[?]', 'oboki[?]|obok|oboki',
     T + 'leaf 24 verso, the organ "with seven stops, three bellows, ... from the south side a door to the '
     'porch". The word reads "oboki" or "obok i"; the English gives it as "beside it". Your transcript had '
     '"oboli".',
     (0, 0.83, 0.62, 0.875)),
    ('s04', 1, '0028_b', 'z trumną[?]', 'trumną[?]', 'trumną[?]|trumną|tramną',
     T + 'leaf 28 verso, near the foot: "Katafalk dobry z tru-/mną", a good catafalque with a coffin. Your '
     'transcript has "tramną"; the letter after "tr" may be u or a.',
     (0, 0.88, 0.70, 0.935)),
    ('s05', 1, '0029_a', 'Bagusławskiego[?]', 'Bagusławskiego[?]', 'Bagusławskiego[?]|Bagusławskiego|Bogusławskiego',
     T + 'leaf 29, the foundation of 1668: "250 złoty placed by JMć Pan ...". The surname looks like '
     '"Bagusławskiego", with a, where the usual name is Bogusławski.',
     (0, 0.455, 0.70, 0.495)),
    ('s06', 1, '0029_a', 'Panią Golinską[?]', 'Golinską[?]', 'Golinską[?]|Golinską|Jolinską',
     T + 'leaf 29: "2000 złoty ... recorded by JMa Pani ... on the estate of Przespolew". Read "Golinską"; your '
     'transcript has "Jolinska". A Teresa Golińska married Krzysztof Prusimski (APP 53/17/0/-/Konin Gr.118), '
     'which is a reason to think of Golińska, not a proof.' + G,
     (0, 0.655, 0.70, 0.70)),
    ('s07', 1, '0029_a', 'Folwarku Drezgi[?]', 'Drezgi[?]', 'Drezgi[?]|Drezgi|Dręzgi',
     T + 'leaf 29, the decree of 1692: the tithe "from the farm of ...". The name of the farm, read "Drezgi"; '
     'there may be a hook under the e.',
     (0, 0.80, 0.70, 0.845)),
    ('s08', 1, '0029_a', 'Dekretem Illust:[?] Offła', 'Illust:[?]', 'Illust:[?]|Illust:|JMści',
     T + 'leaf 29, 1694: "the inn confirmed by a decree of the ... Official of Gniezno". The word before '
     '"Offła" (the Official) is a large flourished abbreviation, read "Illust:" (Illustrissimi).',
     (0, 0.85, 0.70, 0.89)),
    ('s09', 1, '0029_b', 'nazwana Jalewska[?]', 'Jalewska[?]', 'Jalewska[?]|Jalewska|Galewska',
     T + 'leaf 29 verso: "a meadow called ..., given long ago by the heirs".' + G,
     (0, 0.245, 0.72, 0.285)),
    ('s10', 1, '0029_b', 'ogrody sadowne[?]', 'sadowne[?]', 'sadowne[?]|sadowne',
     T + 'leaf 29 verso, the parsonage plot: "on it ... gardens and the parish buildings". The word after '
     '"ogrody" (gardens), read "sadowne" (orchard gardens) with doubt; its first letter is unclear.',
     (0, 0.735, 0.72, 0.79)),
    ('s11', 2, '0034_c', 'Miasto Zagurow', '58[?]', '58[?]|58|68',
     'The table of Zagórów (document 2), the first row, the town of Zagórów: the boys, the third figure. '
     'The first digit looks like a 6, but the clerk\'s total of the column (270) comes out only with 58. '
     'Compare his 5 in "275" and his 6 in "16" a line below.',
     (0, 0.125, 0.56, 0.16)),
    ('s12', 2, '0034_c', 'rozrządzone[?]', 'rozrządzone[?]', 'rozrządzone[?]|rozrządzone|porządzone',
     'The table of Zagórów (document 2), the note in the right margin by Myszakowko: "Tamze niewiasta '
     'maiąca lat 110. Ktorey prawnuki ...", at the same place a woman aged 110, whose great-grandchildren '
     'are ... The last word, read "rozrządzone" with doubt.',
     (0.72, 0.33, 1.0, 0.40)),
]

# Answered by the editor on 2026-10-16 and worked in (intake/spot_answers.py,
# intake/readings_answers.json). Answered rows are left off if the sheet is made again.
ANSWERED = {'s%02d' % i for i in range(1, 13)}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    rev = os.path.join(ROOT, 'review', 'adwl85')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for key, doc, pid, locate, word, options, note, box in ROWS:
        if key in ANSWERED:
            continue
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
        im = Image.open(os.path.join(RAW, 'processed', pid + '.jpg'))
        W, H = im.size
        crop = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H))).convert('L')
        if crop.width > 2400:
            crop = crop.resize((2400, int(crop.height * 2400 / crop.width)))
        name = '%s_%s.jpg' % (key, pid)
        crop.save(os.path.join(img_dir, name), quality=85)
        out.append({'key': key, 'letter': str(doc), 'line': line_no, 'word': word, 'options': options,
                    'note': note, 'image': name})
    with io.open(os.path.join(rev, 'readings.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print(len(out), 'rows')


if __name__ == '__main__':
    main()
