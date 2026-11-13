# -*- coding: utf-8 -*-
"""The spot sheet for APŁ 39/98/0/-/1333: the readings of the letters that stayed doubtful (2026-11-13).

The index's open entries are not asked: the editor ruled them minor
uncertainties that change little (2026-11-13), and Osiny is theirs. What is
asked: the words of the four petitions and of the office's note on folio 88
that two readers and Claude could not settle on the image. Each row has a
picture of the region (cut with margins from the photograph) and the
readings to choose from; the first is what the text now has.

    python units/apl399801333/intake/spot_sheet.py            # cut the pictures, write the sheet's rows
    python pipeline/review/queries.py --unit apl399801333     # serve the sheet
    python pipeline/review/queries.py --unit apl399801333 --read

Answers go to review/apl399801333/query_answers.json and are applied by hand
to intake/text1333.py (and the English) with the build after it.
"""
import csv
import io
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from holding import RAW, SCANS  # noqa: E402

REV = os.path.join(ROOT, 'review', 'apl399801333')
IMG = os.path.join(REV, 'spot_img')
os.makedirs(IMG, exist_ok=True)
FILE = {pid: name for name, pid in SCANS.items()}

# key, document, corpus line, word as the text has it, options, picture: (page id, box as fractions of
# the photograph: x0, y0, x1, y1), note
ROWS = [
    ('q01', 5, 236, '[uszgłębonem?]', 'uszgłębonem|najgłębszem|głębokiem',
     ('0163_a', (0.38, 0.80, 1.0, 0.93)),
     'The colonists\' petition of 1867, the closing formula above the signatures: "Z ... uszanowaniem" '
     '(with ... respect). Your transcription had "u[?]głąbonem". The letters look to me like u-s-z-g-ł-ę-b-o-n-e-m, '
     'not a word I know; the sense is "deepest". What does the page have?'),
    ('q02', 6, 247, '[gajć?]', 'gajć|gaić',
     ('0176_a', (0.15, 0.63, 1.0, 0.73)),
     'The colonists\' petition of 1868: "wolno nam także ... się w Boru furami 2 dni w tydzień" (we may also ... '
     'in the forest with carts two days a week). Your transcription had "gając"; the checker and I read "gajć". '
     'Which, and do you know the word? Later the letter speaks of "ugaj" (ugaju ... nie dozwala).'),
    ('q03', 3, 177, '[обмѣнѣ?]', 'обмѣнѣ',
     ('0088_a', (0.0, 0.40, 0.47, 0.60)),
     'The Russian note of the office in the left margin of folio 88, first line: "Объ ... признать земли". '
     'I read "обмѣнѣ" (on the exchange). The first word of the sixth line, after "поручить", I could not read '
     '(I wrote [Комм…?]); if you can read it, type it under "Something else" with this word.'),
    ('q04', 3, 178, '[oddane?]', 'oddane|dostarczone',
     ('0088_a', (0.0, 0.58, 0.47, 0.73)),
     'The Polish receipt below the Russian note on folio 88: "Dowody ... odebrałem" (I received the ... proofs). '
     'The two readers had "oddane" and "dostarczone". The same picture shows the date line ("Kalisz dnia 11 ...", '
     'I read the month as Paźdz. with doubt) and the signature ("A. Kowal..."): type what you read of them in the note.'),
    ('q05', 3, 184, '[czynionem?]', 'czynionem|czynnem',
     ('0088_b', (0.38, 0.30, 1.0, 0.42)),
     'Folio 88v: "na mylnem przedstawieniu ... przez włościan" (on a mistaken account ... by the peasants). '
     'The word after "przedstawieniu".'),
    ('q06', 4, 221, '11.', '11.|ii.|14.',
     ('0115_a', (0.12, 0.32, 1.0, 0.42)),
     'Folio 115 (the pages I transcribed): "podług przepisów art 1. 5. 11. i innych Najwyższego Ukazu". '
     'The third article number is written with two dotted strokes, like "ii". Is it 11?'),
    ('q07', 4, 207, 'majem', 'majem|mojem',
     ('0113_a', (0.12, 0.48, 1.0, 0.60)),
     'Folio 113, your transcription: "bydła rogatego na majem territorium" (on my land). '
     'I left "majem" as you have it; the checker read "majen". Is it "majem", "mojem", or another?'),
]

lines = io.open(os.path.join(ROOT, 'units', 'apl399801333', 'corpus.txt'), encoding='utf-8').read().split('\n')
out = io.open(os.path.join(REV, 'open_queries.csv'), 'w', encoding='utf-8', newline='')
w = csv.writer(out, lineterminator='\n')
w.writerow(['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
for key, doc, line, word, options, (pid, box), note in ROWS:
    assert word in lines[line - 1], (key, line, word)
    im = Image.open(os.path.join(RAW, 'processed', pid + '.jpg'))
    W, H = im.size
    crop = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    crop.thumbnail((1600, 1600))
    name = '%s_%s.jpg' % (key, pid)
    crop.save(os.path.join(IMG, name), quality=88)
    w.writerow([key, doc, line, word, options, note, name])
out.close()
print(len(ROWS), 'rows written to', os.path.join(REV, 'open_queries.csv'))
