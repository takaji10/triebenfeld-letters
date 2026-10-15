# -*- coding: utf-8 -*-
"""The spot sheet "Doubtful readings in the liquidation table of Łazińsk" (2026-10-15).

    python units/apl399806603/intake/spot_sheet.py
    python pipeline/review/queries.py --unit apl399806603 --sheet readings.csv

All 21 marks of doubt in the holding, on 16 rows, each with a picture of
its place on the page. The signatures of the Permanent Member and the
Secretary under the copies of 1900 and 1901 and the statement (scans 032,
033, 036) are one hand each and are asked once (rows t11, t12); the answer
goes to all three. Unlike the notebook's sheets, the picture is placed by a
box drawn on the page by eye (BOX: left, top, right, bottom as parts of the
page), since the lines of a printed table form do not fall at an even pitch.

Writes review/apl399806603/readings.csv and a picture for each row in
review/apl399806603/spot_img/. A row names its line by a piece of it.
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

T1 = 'The table of 1868 (document 1)'
T2 = 'The copy of 1869 (document 2)'
ST = 'The statement after the survey of 1896 (document 6)'
SIG = ' Signatures are often not legible; type the letters you can see, or say you can\'t tell.'

# (key, document, page id, a piece of the line, the word as it stands, options, note, box)
ROWS = [
    ('t01', 1, '0003_a', '[Стурценбехеръ?] Кристіянъ', '[Стурценбехеръ?]',
     '[Стурценбехеръ?]|Стурценбехеръ|Штирценбехеръ',
     T1 + ', no. 19, ... Kristiian: the surname, read Стурценбехеръ (Sturtsenbekher) with doubt. '
     'Nos. 41 and 84 of the same table are Штирценбехеръ (Shtirtsenbekher); Breyer copied no. 19 as '
     'Стирценбехеръ, the statement has Стирценбекеръ.',
     (0, 0.38, 0.62, 0.44)),
    ('t02', 1, '0013_a', '[10055 70?]', '[10055 70?]', '[10055 70?]|10055 70',
     T1 + ', the last page: two pencil figures at the foot of the right-hand page, "603 34 20/6" and '
     'under it a figure read 10055 70 with doubt (the redemption sum of the table, 10,055 roubles 70 '
     'kopecks, would agree).',
     (0.78, 0.58, 1, 0.73)),
    ('t03', 2, '0016_a', '[Глебель?] Мартинъ', '[Глебель?]', '[Глебель?]|Гебель|Глебель',
     T2 + ', no. 2, ... Martin: the surname, read Глебель (Glebel) with doubt. The table of 1868 has '
     'Гебель (Gebel) here.',
     (0, 0.415, 0.45, 0.465)),
    ('t04', 2, '0016_a', '[Холмъ?] Даніилъ', '[Холмъ?]', '[Холмъ?]|Холмъ',
     T2 + ', no. 4, ... Daniil: the surname, read Холмъ (Kholm, Holm) with doubt, as in the table of 1868.',
     (0, 0.48, 0.45, 0.53)),
    ('t05', 2, '0018_a', '[Стурценбекеръ?] Кристіанъ', '[Стурценбекеръ?]',
     '[Стурценбекеръ?]|Стурценбекеръ|Штирценбекеръ',
     T2 + ', no. 19, ... Kristian: the same man as t01, here read Стурценбекеръ (Sturtsenbeker) with doubt.',
     (0, 0.38, 0.62, 0.43)),
    ('t06', 2, '0028_a', '[Предсѣдатель?]: [?]', '[Предсѣдатель?]: [?]',
     '[Предсѣдатель?]: [?]|Предсѣдатель: [?]',
     T2 + ', under the confirmation of Kalisz, September 1869: "Chairman: ..." The title read '
     'Предсѣдатель (Chairman) with doubt; the signature after it not read.' + SIG,
     (0.28, 0.6, 0.72, 0.68)),
    ('t07', 2, '0028_a', 'Секретарь: [Бергъ?]', '[Бергъ?]', '[Бергъ?]|Бергъ',
     T2 + ', the same page, below the seal: "Secretary: ...", the signature read Бергъ (Berg) with doubt.' + SIG,
     (0.4, 0.75, 0.68, 0.84)),
    ('t08', 3, '0030_a', 'Вице-Губернаторъ [?]', '[?]', '[?]',
     'The inscription of March 1884 (document 3), its signatures: "Vice-Governor ...". The signature '
     'after the title not read.' + SIG,
     (0.08, 0.58, 0.9, 0.665)),
    ('t09', 3, '0030_a', 'Совѣтникъ [?]', '[?]', '[?]',
     'The same page: "Councillor ...", the large signature to the right of the title, not read.' + SIG,
     (0.15, 0.64, 0.85, 0.75)),
    ('t10', 3, '0030_a', 'за Стар. Дѣлопроизводителя [?]', '[?]', '[?]',
     'The same page, at the foot: "for the Senior Clerk ...", the signature not read.' + SIG,
     (0.05, 0.85, 0.85, 0.92)),
    ('t11', 4, '0032_a', 'Присутствія, Н. [?]', '[?]', '[?]',
     'The certified copy of 1900 (document 4): "Permanent Member of the Board, N. ...". The signature '
     'with the large loop, not read. The same signature stands under the copy of 1901 and the '
     'statement; the answer is used for all three.' + SIG,
     (0.08, 0.37, 0.92, 0.51)),
    ('t12', 4, '0032_a', 'Секретарь, А. [?]', '[?]', '[?]',
     'The same page, at the foot: "Secretary, A. ...", the signature not read. It stands under the copy '
     'of 1901 and the statement too; the answer is used for all three.' + SIG,
     (0.15, 0.84, 0.75, 0.91)),
    ('t13', 5, '0033_a', '[Пелзуцкимъ?]', '[Пелзуцкимъ?]', '[Пелзуцкимъ?]|Пелзуцкимъ',
     'The certified copy of 1901 (document 5): "the survey carried out in 1896 by the surveyor ...". '
     'His name, read Пелзуцкимъ (Pelzutskim, i.e. by Pelzutski) with doubt.',
     (0.05, 0.245, 0.97, 0.29)),
    ('t14', 6, '0034_a', '[оказавшагося?]', '[оказавшагося?]', '[оказавшагося?]|оказавшагося',
     ST + ', the heading over the figures: "the amount of the allotment ... by this survey". A word read '
     'оказавшагося (found to be) with doubt.',
     (0.48, 0.14, 0.98, 0.2)),
    ('t15', 6, '0034_a', '[Сливинскій?] Готлибъ', '[Сливинскій?]', '[Сливинскій?]|Сливинскій',
     ST + ', no. 12, ... Gotlib: the surname, read Сливинскій (Slivinskii, Śliwiński) with doubt, the '
     'name of no. 12 in the table of 1868.',
     (0, 0.495, 0.55, 0.535)),
    ('t16', 6, '0034_a', '[Проминсъ?] Щепанъ', '[Проминсъ?]', '[Проминсъ?]|Проминсъ|Промистъ',
     ST + ', no. 25, ... Shchepan: the surname, read Проминсъ (Promins) with doubt. The table of 1868 '
     'has Промистъ (Promist) for no. 25.',
     (0, 0.79, 0.55, 0.83)),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    rev = os.path.join(ROOT, 'review', 'apl399806603')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for key, doc, pid, locate, word, options, note, box in ROWS:
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
