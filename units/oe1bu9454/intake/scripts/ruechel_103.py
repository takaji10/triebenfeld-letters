# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letter 103, page 4: "Ruchts" is "Ruchels", General Rüchel.

    python units/oe1bu9454/intake/scripts/ruechel_103.py            # check only
    python units/oe1bu9454/intake/scripts/ruechel_103.py --write    # once

In the list of gifts Triebenfeld sets beside the Prince's (13 March 1799) the
transcription read "des Gen[eral]. Ruchts sollten 940 rt jährlich tragen".
Claude took the general to be Rüchel, whose gift the black register lists
(literature/links.yml, `register-other-gifts`); the whole-letter reading of
2026-09-29 had already marked the word "possibly Rüchel". The editor agreed
on 2026-10-19 ("Ruchts is probably Rüchel. Possibly a transcription error.
Fix"). The site's scan (Oe_1_Bu_9454_0215_a-L103_04.jpg, line 11) reads
"Ruchels": the "el" was read as "t". His spelling (u, not ü) is kept.

CHANGES are made in corpus.txt and the page file and logged in
transcription_decisions.csv. The English follows by
reference/english_corrections.yml; the name pair of the page in
site/_data/translations/oe1bu9454-103.yml is changed here, because the
corrections reach only the text. The whole-letter reading's mark of doubt on
the word ("possibly Rüchel") is taken out of reading.json: it is settled.
Run again, it reports what is already done and changes nothing.
"""
import csv
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
WHY = ('the editor, 2026-10-19: "Ruchts is probably Rüchel. Possibly a transcription error. Fix"; '
       'the scan reads "Ruchels" (General Rüchel, whose gift the black register lists)')

PAGE_FILE = '0316_Oe 1_Bue 9454_0215_a.txt'
CORPUS = ('des Gen[eral]. Ruchts sollten 940 rt', 'des Gen[eral]. Ruchels sollten 940 rt')
PAGE = ('des Gen. Ruchts sollten 940 rt', 'des Gen. Ruchels sollten 940 rt')
NAMES = ('  - de: Gen[eral]. Ruchts\n    en: General Ruchts\n',
         '  - de: Gen[eral]. Ruchels\n    en: General Rüchel\n')


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    edits = []
    for path, (old, new) in ((os.path.join(UNIT, 'corpus.txt'), CORPUS),
                             (os.path.join(UNIT, 'transcriptions', PAGE_FILE), PAGE),
                             (os.path.join(ROOT, 'site', '_data', 'translations', 'oe1bu9454-103.yml'), NAMES)):
        text = io.open(path, encoding='utf-8', newline='').read()
        if '\r\n' in text:      # the working copy's line ends (git's autocrlf)
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        if text.count(old) == 0 and text.count(new) == 1:
            print('already done:', os.path.basename(path))
            continue
        assert text.count(old) == 1, (path, old)
        edits.append((path, text.replace(old, new)))
    old, new = CORPUS
    key = hashlib.md5(('0215_a|%s|%s' % (old, new)).encode()).hexdigest()[:8]
    row = [key, 'oe1bu9454-103', 4, old, new, '0215_a: %s -> %s' % (old, new), WHY]
    dp = os.path.join(UNIT, 'transcription_decisions.csv')
    logged = key in io.open(dp, encoding='utf-8').read()
    rdp = os.path.join(UNIT, 'reading.json')
    rraw = io.open(rdp, encoding='utf-8', newline='').read()
    reading = json.loads(rraw)
    doubt = reading['oe1bu9454-103']['doubtful_words']
    kept = [d for d in doubt if d['word'] != 'Ruchts']
    print('%d file(s) to change; decision %s; mark of doubt %s'
          % (len(edits), 'logged' if logged else 'to log', 'to drop' if len(kept) < len(doubt) else 'gone'))
    if not write:
        return
    for path, text in edits:
        io.open(path, 'w', encoding='utf-8', newline='').write(text)
    if not logged:
        with io.open(dp, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow(row)
    if len(kept) < len(doubt):
        reading['oe1bu9454-103']['doubtful_words'] = kept
        head = rraw[:8].replace('\r\n', '\n')
        indent = 1 if head.startswith('{\n "') else (2 if head.startswith('{\n  "') else None)
        out = json.dumps(reading, ensure_ascii=False, indent=indent)
        if '\r\n' in rraw:
            out = out.replace('\n', '\r\n')
        io.open(rdp, 'w', encoding='utf-8', newline='').write(
            out + ('\r\n' if rraw.endswith('\r\n') else '\n' if rraw.endswith('\n') else ''))
    print('written')


if __name__ == '__main__':
    main()
