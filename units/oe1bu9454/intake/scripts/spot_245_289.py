# -*- coding: utf-8 -*-
"""The spot sheet "Letters 245 and 289" (2026-10-07): the words the new scans did not let me settle.

    python units/oe1bu9454/intake/scripts/spot_245_289.py
    python pipeline/review/queries.py --unit oe1bu9454 --sheet rescan_245_289.csv --port 4102

Writes review/oe1bu9454/rescan_245_289.csv. Each row is a word left as found
in the text; the first button is what stands now.
"""
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))

# (letter, words of the line, the word, options, note)
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
     'Page 1, the middle: "dem Curischen Mandatarius Eberhard ... angedeutet, sofort alle Vergleichs Verhandlungen abzubrechen". Your new '
     'reading has "zu bring". Could it be the town, "zu Brieg"?'),
    ('289', 'Mandant so schrecklich bitte', 'bitte', 'bitte|litte',
     'Page 1: "wenn nicht mein Fürstl. Mandant so schrecklich ..., denn auf den Grund dieser Schuld". Both transcriptions have "bitte"; '
     '"litte" (suffered) would make the sentence.'),
    ('289', 'nach welchen leztere Circa 112/m rt.', 'Circa', 'Circa|mit',
     'Page 1, upper third: "nach welchen leztere ... 112/m rt. zufrieden sein". Both transcriptions have "Circa".'),
    ('289', 'hat der Justiz rath Heneberg[?]', 'Heneberg[?]', 'Heneberg[?]|Heneberg|Henneberg',
     'Page 1, the middle: the name of the councillor of justice in Berlin. The mark of doubt is yours.'),
]


def main():
    corpus = io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read().split('\n')
    out, doc = [], None
    where = {}
    for i, l in enumerate(corpus, 1):
        if l.startswith('[DOC '):
            doc = l[5:-1]
        else:
            where.setdefault(doc, []).append((i, l))
    for n, (letter, words, word, options, note) in enumerate(ROWS, 1):
        hits = [i for i, l in where[letter] if words in l]
        assert len(hits) == 1, (letter, words, hits)
        assert corpus[hits[0] - 1].count(word) == 1, (word, corpus[hits[0] - 1])
        out.append({'key': 'r%02d' % n, 'letter': letter, 'line': str(hits[0]), 'word': word, 'options': options, 'note': note})
    dest = os.path.join(ROOT, 'review', 'oe1bu9454', 'rescan_245_289.csv')
    with io.open(dest, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note'])
        w.writeheader()
        w.writerows(out)
    print('wrote', dest, len(out), 'rows')


if __name__ == '__main__':
    main()
