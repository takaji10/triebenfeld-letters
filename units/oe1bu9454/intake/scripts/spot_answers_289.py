# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letter 289: the editor's answers on the spot sheet "Letters 245 and 289", applied.

    python units/oe1bu9454/intake/scripts/spot_answers_289.py            # check only
    python units/oe1bu9454/intake/scripts/spot_answers_289.py --write    # once

The editor answered rows 7 to 10 of the sheet on 2026-10-08, each against a
picture of its line cut from the new scan (the answers are in
review/oe1bu9454/rescan_245_289_answers.json and copied here):

    r07  zu bring      "zu Brieg": the town; the mandatary Eberhard is at Brieg.
    r08  bitte         stands.
    r09  Circa         stands.
    r10  Heneberg[?]   "Heneberg": the mark of doubt goes.

CHANGES are made in corpus.txt and the page file and logged in
transcription_decisions.csv; ENGLISH in intake/translation/doc289.yml, which
write_cache.py then puts into the cache.
"""
import csv
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
SHEET = 'the editor, against the new scan, on the spot sheet of 2026-10-08'

ANSWERS = {'r07': 'zu Brieg', 'r08': 'bitte', 'r09': 'Circa', 'r10': 'Heneberg'}
PAGE_FILE = '0828_Oe 1_Bue 9454_0522_b.txt'
CHANGES = [
    ('Mandatarius Eberhard zu bring angedeutet,', 'Mandatarius Eberhard zu Brieg angedeutet,', 'r07: the editor reads "zu Brieg"'),
    ('hat der Justiz rath Heneberg[?]', 'hat der Justiz rath Heneberg', 'r10: the editor reads "Heneberg" and takes the mark of doubt away'),
]
ENGLISH = [
    ('the councillor of justice [uncertain: Heneberg] in Berlin has intimated to the Courland mandatary Eberhard [uncertain: zu bring] at once to break off',
     'the councillor of justice Heneberg in Berlin has intimated to the Courland mandatary Eberhard at Brzeg at once to break off'),
    ('were my princely client not so dreadfully [uncertain: bitte], for', 'were my princely client not entreating so dreadfully, for'),
]


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    cp = os.path.join(UNIT, 'corpus.txt')
    corpus = io.open(cp, encoding='utf-8').read()
    pp = os.path.join(UNIT, 'transcriptions', PAGE_FILE)
    page = io.open(pp, encoding='utf-8', newline='').read()
    log = []
    for old, new, why in CHANGES:
        assert corpus.count(old) == 1 and page.count(old) == 1, old
        corpus, page = corpus.replace(old, new), page.replace(old, new)
        key = hashlib.md5(('0522_b|%s|%s' % (old, new)).encode()).hexdigest()[:8]
        log.append([key, 'oe1bu9454-289', 1, old, new, '0522_b: %s -> %s' % (old, new), '%s: %s' % (SHEET, why)])
    dp = os.path.join(HERE, '..', 'translation', 'doc289.yml')
    doc = io.open(dp, encoding='utf-8', newline='').read()
    for old, new in ENGLISH:
        assert doc.count(old) == 1, old
        doc = doc.replace(old, new)
    a = '- page: 1\n  confidence: medium\n  marker_count: 3\n'
    assert doc.count(a) == 1
    doc = doc.replace(a, '- page: 1\n  confidence: high\n  marker_count: 0\n')
    print(len(CHANGES), 'changes to the text,', len(ENGLISH), 'to the English: all apply')
    if not write:
        return
    io.open(cp, 'w', encoding='utf-8', newline='\n').write(corpus)
    io.open(pp, 'w', encoding='utf-8', newline='').write(page)
    io.open(dp, 'w', encoding='utf-8', newline='').write(doc)
    with io.open(os.path.join(UNIT, 'transcription_decisions.csv'), 'a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(log)
    print('written and logged')


if __name__ == '__main__':
    main()
