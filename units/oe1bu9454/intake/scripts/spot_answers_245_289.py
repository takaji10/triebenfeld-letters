# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letter 245: the editor's answers on the spot sheet "Letters 245 and 289", applied.

    python units/oe1bu9454/intake/scripts/spot_answers_245_289.py            # check only
    python units/oe1bu9454/intake/scripts/spot_answers_245_289.py --write    # once

The editor answered rows 1 to 6 of the sheet (letter 245) against the new
scans on 2026-10-07; the answers are in review/oe1bu9454/rescan_245_289_answers.json
and are copied here (ANSWERS). Rows 7 to 10 (letter 289) wait: the editor
could not find those lines, and the sheet now shows a picture of each.

    r01  praeciat     "praedikat" (typed). Both places: "praedikat" on page 1, "Praedikat" on page 2.
    r02  Inträgen     stands.
    r03  darin        no reading given; "Looks like dringen?". The editor's word, with their doubt: "dringen[?]".
    r04  Ersaz        stands.
    r05  Erröthen     can't tell. The word stays and takes a mark of doubt: "Erröthen[?]".
    r06  aus der Casse   can't tell; "Aus der B___ Casse is what I see". So a word beginning with B stands
                      between, and it is given as "B[...]": "aus der B[...] Casse".

CHANGES are made in corpus.txt and the page files and logged in
transcription_decisions.csv; ENGLISH in intake/translation/doc245.yml, which
write_cache.py then puts into the cache.
"""
import csv
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
SHEET = 'the editor, against the new scan, on the spot sheet of 2026-10-07'

ANSWERS = {'r01': 'other: praedikat', 'r02': 'Inträgen', 'r03': 'other: (not given); note: Looks like dringen?', 'r04': 'Ersaz',
           'r05': "can't tell", 'r06': "can't tell; note: Aus der B___ Casse is what I see"}
# (page id, page of the letter, page file, text as it stood, text now, why)
CHANGES = [
    ('0455_a', 1, '0722_Oe 1_Bue 9454_0455_a.txt', 'als ein praeciat zur Berichtigung', 'als ein praedikat zur Berichtigung', 'r01: the editor reads "praedikat"'),
    ('0456_a', 2, '0723_Oe 1_Bue 9454_0456_a.txt', 'August als Praeciat erhalten soll', 'August als Praedikat erhalten soll',
     'r01: the same word as on page 1, where the editor reads "praedikat"'),
    ('0455_a', 1, '0722_Oe 1_Bue 9454_0455_a.txt', 'dennoch einzudringen, darin nach', 'dennoch einzudringen, dringen[?] nach',
     'r03: the editor gives no reading but notes "Looks like dringen?"; their word, with their doubt, in place of mine'),
    ('0455_a', 1, '0722_Oe 1_Bue 9454_0455_a.txt', 'alles ohne Erröthen —', 'alles ohne Erröthen[?] —', 'r05: the editor cannot tell; the word takes a mark of doubt'),
    ('0456_a', 2, '0723_Oe 1_Bue 9454_0456_a.txt', 'dem Fürsten aus der Casse vorgeschoßene', 'dem Fürsten aus der B[...] Casse vorgeschoßene',
     'r06: the editor sees "Aus der B___ Casse": a word beginning with B stands between'),
]
ENGLISH = [
    ('as a [uncertain: praeciat] toward the settling of his debts', 'as a "Praedikat" toward the settling of his debts'),
    ('is to receive as a [uncertain: Praeciat] could', 'is to receive as a "Praedikat" could'),
    ('to dispose in them at his own will', 'to [uncertain: dringen] dispose at his own will'),
    ('he bears it all without blushing —', 'he bears it all without [uncertain: blushing] —'),
    ('formerly advanced to the Prince out of the treasury.', 'formerly advanced to the Prince out of the B[text lost] treasury.'),
]
# marker_count of the two pages after ENGLISH: page 1 had 5 (one goes, two come), page 2 had 3 (one goes, one comes)
MARKERS = {1: 6, 2: 3}


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    cp = os.path.join(UNIT, 'corpus.txt')
    corpus = io.open(cp, encoding='utf-8').read()
    log = []
    files = {}
    for pid, page, fn, old, new, why in CHANGES:
        assert corpus.count(old) == 1, (corpus.count(old), old)
        corpus = corpus.replace(old, new)
        p = os.path.join(UNIT, 'transcriptions', fn)
        s = files.get(p) or io.open(p, encoding='utf-8', newline='').read()
        assert s.count(old) == 1, (fn, old)
        files[p] = s.replace(old, new)
        key = hashlib.md5(('%s|%s|%s' % (pid, old, new)).encode()).hexdigest()[:8]
        log.append([key, 'oe1bu9454-245', page, old, new, '%s: %s -> %s' % (pid, old, new), '%s: %s' % (SHEET, why)])
    dp = os.path.join(HERE, '..', 'translation', 'doc245.yml')
    doc = io.open(dp, encoding='utf-8', newline='').read()
    for old, new in ENGLISH:
        assert doc.count(old) == 1, (doc.count(old), old)
        doc = doc.replace(old, new)
    for page, was, now in ((1, 5, MARKERS[1]), (2, 3, MARKERS[2])):
        a = '- page: %d\n  confidence: medium\n  marker_count: %d\n' % (page, was)
        assert doc.count(a) == 1, a
        doc = doc.replace(a, '- page: %d\n  confidence: medium\n  marker_count: %d\n' % (page, now))
    print(len(CHANGES), 'changes to the text,', len(ENGLISH), 'to the English: all apply')
    if not write:
        return
    io.open(cp, 'w', encoding='utf-8', newline='\n').write(corpus)
    for p, s in files.items():
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
    io.open(dp, 'w', encoding='utf-8', newline='').write(doc)
    lp = os.path.join(UNIT, 'transcription_decisions.csv')
    head = next(csv.reader(io.open(lp, encoding='utf-8-sig')))
    print('log columns:', head)
    with io.open(lp, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        for row in log:
            w.writerow(row if len(head) == 7 else row[:len(head)])
    print('written and logged')


if __name__ == '__main__':
    main()
