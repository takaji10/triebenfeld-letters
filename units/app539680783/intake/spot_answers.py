# -*- coding: utf-8 -*-
"""The editor's answers on the spot sheet "Pen marks on the summons" (2026-10-14), applied once.

    python units/app539680783/intake/spot_answers.py

A record, not to be run again (it asserts the old readings). It changes the
page files and corpus.txt, logs each change in transcription_decisions.csv,
and the English is changed in ENGLISH in holding.py beside it (then
holding.py --english --cache).

The answers (review/app539680783/pen_marks_answers.json):
- no. 58, the name in the margin: "Marcina Heck" (was "Marcina [Hetke?]");
- no. 7, "Fryderyka": stands; no. 55, "Celmer": stands; nos. 53 and 54,
  "Rogackiego": stands;
- no. 70: the editor typed "Krystof". The pen covers the printed "ja" of
  "Kry-/stjana" and leaves the ending "a"; the list gives every name in the
  accusative, so the line is "Krystofa Grünwald" (Krystof Grünwald);
- the note of costs: "47" without doubt.
"""
import csv
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)

CHANGES = [
    ('0005_a', '58. Marcina [Hetke?].', '58. Marcina Heck.',
     'the editor read the surname in the margin on the spot sheet: Heck (2026-10-14)'),
    ('0005_a', '70. Krystjana Grünwald.', '70. Krystofa Grünwald.',
     'the editor read the pen over the printed "ja" on the spot sheet: Krystof; the printed ending "a" stands, the accusative of the list (2026-10-14)'),
    ('0007_a1', 'Raz Rs [47?] k 21.', 'Raz Rs 47 k 21.',
     'the editor read the blotted figure on the spot sheet: 47 (2026-10-14)'),
]


def main():
    log = os.path.join(UNIT_DIR, 'transcription_decisions.csv')
    with io.open(log, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    corpus_p = os.path.join(UNIT_DIR, 'corpus.txt')
    corpus = io.open(corpus_p, encoding='utf-8').read()
    for pid, old, new, why in CHANGES:
        page_p = os.path.join(UNIT_DIR, 'transcriptions', pid + '.txt')
        page = io.open(page_p, encoding='utf-8').read()
        assert page.count(old) == 1 and corpus.count(old) == 1, old
        io.open(page_p, 'w', encoding='utf-8', newline='\n').write(page.replace(old, new))
        corpus = corpus.replace(old, new)
        rows.append({'key': hashlib.md5((pid + old).encode('utf-8')).hexdigest()[:8], 'pad': 'app539680783-001',
                     'page': '1' if pid == '0005_a' else '4', 'transcribed': old, 'proposed': new,
                     'decision': '%s: %s -> %s' % (pid, old, new), 'why': why})
    io.open(corpus_p, 'w', encoding='utf-8', newline='\n').write(corpus)
    with io.open(log, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(len(CHANGES), 'changes applied and logged')


if __name__ == '__main__':
    main()
