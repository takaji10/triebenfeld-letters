# -*- coding: utf-8 -*-
"""The spot sheet "The faint word in the Kuryer Polski" (2026-10-16).

    python units/kuryerpolski1754075/intake/spot_sheet.py
    python pipeline/review/queries.py --unit kuryerpolski1754075 --sheet readings.csv

The one mark of doubt in the holding, with a picture of its line (a box drawn
by eye: left, top, right, bottom as parts of the page). The first option is
what is built.
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

ROWS = [
    ('k01', 1, '0002_a', '[Cleri?] Sæcularis', '[Cleri?]', '[Cleri?]|Cleri|[?]',
     'The guests at the funeral: "... of related houses, ... Sæcularis; the Cistercian fathers of the convent '
     'of Ląd". The word before "Sæcularis" is faint: a stroke at its start and an italic i at its end. Read '
     '"Cleri" (Cleri Sæcularis, the secular clergy) with doubt, as the usual phrase.',
     (0.03, 0.525, 0.53, 0.585)),
]
# Answered by the editor on 2026-10-16: "[Cleri?]" kept as it stands, with its doubt
# (intake/readings_answers.json). Nothing in the text changed.
ANSWERED = {'k01'}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    rev = os.path.join(ROOT, 'review', 'kuryerpolski1754075')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for key, doc, pid, locate, word, options, note, box in ROWS:
        if key in ANSWERED:
            continue
        hits = [i for i, l in enumerate(corpus, 1) if locate in l]
        assert len(hits) == 1, (key, hits)
        im = Image.open(os.path.join(RAW, 'processed', pid + '.jpg'))
        W, H = im.size
        crop = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H))).convert('L')
        crop = crop.resize((crop.width * 3, crop.height * 3))
        name = '%s_%s.jpg' % (key, pid)
        crop.save(os.path.join(img_dir, name), quality=90)
        out.append({'key': key, 'letter': str(doc), 'line': hits[0], 'word': word, 'options': options,
                    'note': note, 'image': name})
    with io.open(os.path.join(rev, 'readings.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print(len(out), 'rows')


if __name__ == '__main__':
    main()
