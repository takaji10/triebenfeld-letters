# -*- coding: utf-8 -*-
"""The book's lexicon and the artifact classes, from the two page passes.

Lexicon: every token (folded) that BOTH page passes emit on some page -
the empirical contextual dictionary for the word settlement. With counts
and one sample page each.

Artifact classes sampled with full sentence context (not counted blind):
  - the percent forms (40%, 409/,, 40%/, ...)
  - the fraction forms (71/,, 3/g, 24'/s ...)
  - the glued footnote markers in body text (Ujskich1)
"""
import json, os, re
from collections import Counter, defaultdict

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
BODY = {f'{i:04d}' for i in range(16, 138)} | \
       {f'{i:04d}' for i in range(160, 172)}


def fold(w):
    return re.sub(r'^\W+|\W+$', '', w).lower()


def main():
    lex = Counter()
    sample = {}
    pct = []
    frac = []
    for fn in sorted(os.listdir(OCR)):
        if not (fn.endswith('.json') and len(fn) == 9):
            continue
        n = fn[:4]
        if n not in BODY:
            continue
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        cpol = Counter(fold(w) for w in d['pol'].split() if fold(w))
        cstd = Counter(fold(w) for w in d['std'].split() if fold(w))
        for w, c in cpol.items():
            if cstd.get(w):
                if w not in sample:
                    sample[w] = n
                lex[w] += c
        # contexts
        for m in re.finditer(r'[^\n.]{0,50}[\d.,]+\s*[%/][^\n]{0,30}',
                             d['pol']):
            if '%' in m.group(0) or ('/' in m.group(0) and ',' in m.group(0)):
                pct.append((n, m.group(0).strip()))
        for m in re.finditer(
                r'[^\n.]{0,40}\b\w{0,4}\d{0,3}\s*[/\u2019]'
                r'[.,]?\s+[a-ząćęłńóśźż][^\n]{0,30}', d['pol']):
            s = m.group(0).strip()
            if re.search(r'\d\s*/', s):
                frac.append((n, s))
    with open(os.path.join(OCR, 'lexicon.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump({'words': dict(lex), 'sample': sample}, fh,
                  ensure_ascii=False)
    print('lexicon size:', len(lex))
    print()
    print('=== percent contexts (first 12) ===')
    for n, s in pct[:12]:
        print(n, '|', s)
    print()
    print('=== fraction contexts (first 14) ===')
    for n, s in frac[:14]:
        print(n, '|', s)


if __name__ == '__main__':
    main()
