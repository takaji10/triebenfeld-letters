# -*- coding: utf-8 -*-
"""The spot sheet "Letters 245 and 289" (2026-10-07): the words the new scans did not let me settle.

    python units/oe1bu9454/intake/scripts/spot_245_289.py
    python pipeline/review/queries.py --unit oe1bu9454 --sheet rescan_245_289.csv --port 4102

Writes review/oe1bu9454/rescan_245_289.csv. Each row is a word left as found
in the text; the first button is what stands now. The four rows of letter 289
carry a picture of their lines, cut from the new scan into
review/oe1bu9454/spot_img/ (CROPS): the editor could not find those lines by
their numbers (2026-10-08). The editor answered rows 1 to 6 on 2026-10-07;
spot_answers_245_289.py applies the answers.
"""
import csv
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
NEW = 'C:/Users/Tersnaus/Downloads/Oe 1_Bue 9454 Nr. 289, Nr. 245'
P1 = 'Oe 1_Bü 9454 Nr. 289/Oe 1_Bü 9454_0522_b.jpg'
# row key -> (scan, top and bottom of the band as fractions of its height)
CROPS = {'r07': (P1, 0.497, 0.540), 'r08': (P1, 0.672, 0.710), 'r09': (P1, 0.395, 0.432), 'r10': (P1, 0.497, 0.540)}

# (letter, words of the line as it stood when the sheet was made, the word, options, note)
ROWS = [
    ('245', 'als ein praeciat zur Berichtigung', 'praeciat', 'praeciat|praecipuum|praesent',
     'Page 1, about five lines from the foot: "100/m rt als ein ... zur Berichtigung". A term for what the son was to be paid first. I read '
     'p-r-ae-c-i-a-t and do not know the word; the same word stands on page 2 ("als Praeciat erhalten soll").'),
    ('245', 'ist der Inbegrif aller Inträgen', 'Inträgen', 'Inträgen|Intrigen|Intriguen',
     'Page 1, two-thirds down: "Dieser Transact ist der Inbegrif aller ...". Page 2 writes "diesen Intrigen bald abhelfen".'),
    ('245', 'dennoch einzudringen, darin nach', 'darin', 'darin|drin|die',
     'Page 1, the end of the line "... rechtlichen Schrankken dennoch einzudringen, ... nach / Willkühr zu schalten". A short word at the edge.'),
    ('245', 'wo die Möglichkeit den Ersaz von Cos:', 'Ersaz', 'Ersaz|Ersten',
     'Page 1, three lines from the foot: "wo die Möglichkeit den ... von Cos: zu erlangen?" The old reading was "den Ersten von los zu erkennen".'),
    ('245', 'alles ohne Erröthen', 'Erröthen', 'Erröthen|Errathen',
     'Page 1, the last line, at the torn foot: "er leidet / alles ohne ..." (he bears it all without blushing).'),
    ('245', 'dem Fürsten aus der Casse vorgeschoßene', 'aus der Casse', 'aus der Casse|und der Casse|leave the insertion out',
     'Page 2, about twelve lines from the end: words written above the line between "dem Fürsten" and "vorgeschoßene 35000 rt". One word '
     'in the insertion is struck out and is not transcribed. Is the first word "aus" or "und", and is "Casse" struck too?'),
    ('289', 'Mandatarius Eberhard zu bring angedeutet', 'zu bring', 'zu bring|zu Brieg|zu bringen',
     'The middle line of the picture: "in Berlin dem Curischen Mandatarius Eberhard zu ... angedeutet". Your new reading has "zu bring". '
     'Could it be the town, "zu Brieg"? An e and an n look alike in this hand.'),
    ('289', 'Mandant so schrecklich bitte', 'bitte', 'bitte|litte',
     'The third line of the picture: "nicht mein Fürstl. Mandant so schrecklich ..., denn auf den Grund". Both transcriptions have "bitte"; '
     '"litte" (suffered) would make the sentence. Look at the first letter.'),
    ('289', 'nach welchen leztere Circa 112/m rt.', 'Circa', 'Circa|mit',
     'The third line of the picture: "Vergleich einzuschreiten, nach welchen leztere ... 112/m rttl. zufrieden sein". Both transcriptions '
     'have "Circa", and looking again I read "Circa" too.'),
    ('289', 'hat der Justiz rath Heneberg[?]', 'Heneberg[?]', 'Heneberg[?]|Heneberg|Henneberg',
     'The second line of the picture, its last word, at the edge of the page: "hat der Justiz rath ...". The name of the councillor of '
     'justice in Berlin. The mark of doubt is yours.'),
]


def main():
    corpus = io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read().split('\n')
    old = {}
    dest = os.path.join(ROOT, 'review', 'oe1bu9454', 'rescan_245_289.csv')
    if os.path.isfile(dest):
        old = {r['key']: r for r in csv.DictReader(io.open(dest, encoding='utf-8-sig'))}
    out, doc, where = [], None, {}
    for i, l in enumerate(corpus, 1):
        if l.startswith('[DOC '):
            doc = l[5:-1]
        else:
            where.setdefault(doc, []).append((i, l))
    Image.MAX_IMAGE_PIXELS = None
    for n, (letter, words, word, options, note) in enumerate(ROWS, 1):
        key, image = 'r%02d' % n, ''
        hits = [i for i, l in where[letter] if words in l]
        if len(hits) == 1 and corpus[hits[0] - 1].count(word) == 1:
            line = str(hits[0])
        else:                       # an answered row whose word has since been changed: keep the row as it was put
            assert key in old, (key, words)
            line, word = old[key]['line'], old[key]['word']
        if key in CROPS:
            scan, y0, y1 = CROPS[key]
            im = Image.open(os.path.join(NEW, scan)).convert('RGB')
            c = im.crop((int(im.width * 0.18), int(im.height * y0), im.width, int(im.height * y1)))
            c = c.resize((c.width * 2 // 5, c.height * 2 // 5), Image.LANCZOS)
            os.makedirs(os.path.join(ROOT, 'review', 'oe1bu9454', 'spot_img'), exist_ok=True)
            image = 'L289_%s.jpg' % key
            c.save(os.path.join(ROOT, 'review', 'oe1bu9454', 'spot_img', image), quality=88)
        out.append({'key': key, 'letter': letter, 'line': line, 'word': word, 'options': options, 'note': note, 'image': image})
    with io.open(dest, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print('wrote', dest, len(out), 'rows;', sum(1 for r in out if r['image']), 'with a picture')


if __name__ == '__main__':
    main()
