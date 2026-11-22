# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454: three words read again on the scans (2026-11-22).

    python units/oe1bu9454/intake/scripts/four_words_2026_11_22.py            # check only
    python units/oe1bu9454/intake/scripts/four_words_2026_11_22.py --write    # once

The edition-wide sweep of the English (docs/NR421_ENGLISH_PLAN.md, step 5) left
four words in this holding for the scans; the editor gave the folder
(J:\\...\\Hohenlohe-Zentralarchiv Neuenstein\\Oe 1_Bü 9454). Two Sonnet readers
read them independently from the openings, one blind, one told the context
(scratch/b9454/, not kept):

- letter 39, scan 0072 (right): "nach Königl. reisen" reads "nach Königs:
  reisen" (both readers; Königsberg abbreviated). The English: "Königsberg[?]".
- letter 170, scan 0320 (left): "die Wüsten mit der fahrenden Poß" reads "die
  Kisten" (both readers: the first letter a looped K, not W): the crates went
  off by the mail coach.
- letter 303, scan 0544 (left), row 64 of the creditors: "der p Über" reads
  "Dem p Über" (both: "Dem"); Über is a surname and stays.
- letter 21, scan 0034: "die Genuenſter Fürſt" not settled (both read
  "Fürſt", neither the word before): the English gives "the [...] Prince";
  the transcription is unchanged.

Changes in corpus.txt and the page files, logged in transcription_decisions.csv;
the English by reference/english_corrections.yml. Run again, it reports what is
already done.
"""
import csv
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))

# (pad, page, page file, corpus (old, new), page file (old, new), why)
CHANGES = [
    ('oe1bu9454-039', 1, '0106_Oe 1_Bue 9454_0072_b.txt',
     ('ungehindert nach Königl. reisen kan.', 'ungehindert nach Königs: reisen kan.'),
     ('ungehindert nach Königl. reisen kan.', 'ungehindert nach Königs: reisen kan.'),
     'two readers on the scan: "Königs:", Königsberg abbreviated, not "Königl."'),
    ('oe1bu9454-170', 2, '0495_Oe 1_Bue 9454_0320_a1.txt',
     ('daß heute die Wüsten mit der', 'daß heute die Kisten mit der'),
     ('daß heute die Wüsten mit der', 'daß heute die Kisten mit der'),
     'two readers on the scan: a looped K, "Kisten" (crates), not "Wüsten"'),
    ('oe1bu9454-303', 4, '0862_Oe 1_Bue 9454_0544_a1.txt',
     ('64,der p Über,', '64,Dem p Über,'),
     ('64,der p Über,', '64,Dem p Über,'),
     'two readers on the scan: "Dem", not "der"; Über a surname'),
]


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    edits, rows = [], []
    dp = os.path.join(UNIT, 'transcription_decisions.csv')
    log = io.open(dp, encoding='utf-8').read()
    for pad, page, pf, corp, pg, why in CHANGES:
        for path, (old, new) in ((os.path.join(UNIT, 'corpus.txt'), corp),
                                 (os.path.join(UNIT, 'transcriptions', pf), pg)):
            text = edits_text = None
            for p, t in edits:
                if p == path:
                    edits_text = t
            text = edits_text if edits_text is not None else io.open(path, encoding='utf-8', newline='').read()
            if text.count(old) == 0 and text.count(new) == 1:
                print('already done:', pad, os.path.basename(path))
                continue
            assert text.count(old) == 1, (path, old, text.count(old))
            edits = [(p, t) for p, t in edits if p != path] + [(path, text.replace(old, new))]
        key = hashlib.md5(('%s|%s|%s' % (pf, corp[0], corp[1])).encode()).hexdigest()[:8]
        if key not in log:
            rows.append([key, pad, page, corp[0], corp[1], '%s: %s -> %s' % (pf[:4], corp[0], corp[1]),
                         why + ' (2026-11-22)'])
    print('%d file(s) to change, %d decision(s) to log' % (len(edits), len(rows)))
    if not write:
        return
    for path, text in edits:
        io.open(path, 'w', encoding='utf-8', newline='').write(text)
    if rows:
        with io.open(dp, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f, lineterminator='\n').writerows(rows)
    print('written')


if __name__ == '__main__':
    main()
