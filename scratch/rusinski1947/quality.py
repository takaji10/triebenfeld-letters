# -*- coding: utf-8 -*-
"""Candidate doubtful words of tom5 by aligned two-pass diff, v3.

v2's excess-counting flagged every occurrence of a word when one pass lost
one instance. v3 aligns the two passes' token sequences with difflib
(the Dorow 1843 method): words inside changed blocks are the real
disagreements; words aligned in equal blocks are trusted.

Candidates per page = best-pass words inside changed blocks (difflib,
length > 3), plus best-pass words of conf 1..75. Punctuation-only tokens
and the conf-0 quirk (Tesseract reads 0.0 on words it reads perfectly)
are dropped.

Writes doubtful.csv (scan, left, top, width, height, conf, word, kind).
"""
import sys, os, json, csv, re, difflib
from collections import Counter

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
THRESH = 75.0


def fold(w):
    """Fold for alignment: strip edge punctuation, lower."""
    return re.sub(r'^\W+|\W+$', '', w).lower()


def main():
    files = sorted(f for f in os.listdir(OCR) if f.endswith('.json'))
    rows = []
    for fn in files:
        n = fn[:4]
        with open(os.path.join(OCR, fn), encoding='utf-8') as fh:
            d = json.load(fh)
        tsv = [(x[0], x[1], x[2], x[3], x[4], x[5].strip())
               for x in d['words'] if x[5].strip()]
        ttoks = []
        for (_, _, _, _, _, w) in tsv:
            f = fold(w)
            if f and len(f) >= 2 and re.search(r'\w', f, re.UNICODE):
                ttoks.append(f)
        stoks = [fold(w) for w in d['std'].split() if fold(w)]
        sm = difflib.SequenceMatcher(None, ttoks, stoks, autojunk=False)
        matched = set()
        for a, b, size in sm.get_matching_blocks():
            for i in range(a, a + size):
                matched.add(i)
        bad = set(range(len(ttoks))) - matched
        ti = 0
        for (l, t, w_, h, conf, word) in tsv:
            f = fold(word)
            if not f or len(f) < 2 or not re.search(r'\w', f, re.UNICODE):
                continue
            # bad = the indices outside the matching blocks = the words in
            # changed blocks; those are the disagreements
            disagree = ti in bad and len(f) > 3
            midconf = 0.0 < conf < THRESH
            if disagree or midconf:
                kind = ('disagree' if disagree else '') + \
                       ('|lowconf' if midconf else '')
                rows.append([n, l, t, w_, h, round(conf, 1), word, kind])
            ti += 1
    with open(os.path.join(OCR, 'doubtful.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        wr = csv.writer(fh)
        wr.writerow(['scan', 'left', 'top', 'width', 'height', 'conf',
                     'word', 'kind'])
        wr.writerows(rows)
    per = Counter(r[0] for r in rows)
    print('candidates:', len(rows), 'mean/page:',
          round(len(rows) / max(1, len(files)), 1))
    print('worst:', per.most_common(15))


if __name__ == '__main__':
    main()
