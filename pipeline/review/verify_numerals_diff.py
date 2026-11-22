# -*- coding: utf-8 -*-
"""Measure the effect of the registry-number rule of pipeline/numerals.py
(editor's report, 2026-11-22): runs the old and the new group_digits over every
English page text in site/_data/translations/*.yml and every units/*/corpus.txt,
and writes review/numerals_diff.tsv (source_file, doc, line_text, old, new).
"""
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
import numerals
from numerals import _ID, _NUM, _UNIT, _group, years_from

group_digits = numerals.group_digits


def _group_digits_old(text, doc=None):
    """`text` with its sums grouped by thousands, as the module says. `doc`
    (document id or holding slug) sets the first year expected (YEARS_FROM)."""
    first_year = years_from(doc)
    if not text or not re.search(r'\d{4}', text):
        return text

    def f(m):
        num = m.group(1)
        if num.startswith('0') or _ID.search(text[max(0, m.start() - 12):m.start()]):
            return num
        if len(num) == 4:
            v = int(num)
            unit = re.match(r'\s*' + _UNIT, text[m.end():])
            if first_year <= v <= 1999 and not unit:
                return num
        return _group(num)
    return _NUM.sub(f, text)


def changed(text, doc):
    """(line_text, old number, new number) for each number the two versions
    treat differently, reported line by line. The text is grouped whole, as the
    pipeline groups it (a reading-text paragraph, an English page): the rule
    looks at the line above (a total under a column of sums), so grouping line
    by line would report numbers the pipeline leaves alone (2026-11-22)."""
    out = []
    whole_a, whole_b = _group_digits_old(text, doc), group_digits(text, doc)
    for line, a, b in zip(text.split(chr(10)), whole_a.split(chr(10)), whole_b.split(chr(10))):
        if a != b:
            ta = re.findall(r'\d[\d,]*\d', a)
            tb = re.findall(r'\d[\d,]*\d', b)
            for x, y in zip(ta, tb):
                if x != y:
                    out.append((line, x, y))
    return out


def en_texts(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == 'en' and isinstance(v, str):
                yield v
            else:
                yield from en_texts(v)
    elif isinstance(data, list):
        for v in data:
            yield from en_texts(v)


def main():
    rows = []
    counts = {'translations': 0, 'corpus': 0}
    for f in sorted(glob.glob(os.path.join(ROOT, 'site', '_data', 'translations', '*.yml'))):
        doc = os.path.basename(f)[:-4]
        with open(f, encoding='utf-8') as fh:
            data = yaml.safe_load(fh)
        for t in en_texts(data):
            for line, a, b in changed(t, doc):
                rows.append((os.path.relpath(f, ROOT), doc, line, a, b))
                counts['translations'] += 1
    # the reading text, paragraph by paragraph, as corpus_pages.py groups it
    for f in sorted(glob.glob(os.path.join(ROOT, 'dataset', 'units', '*', 'letters.json'))):
        doc = os.path.basename(os.path.dirname(f))
        with open(f, encoding='utf-8') as fh:
            letters = json.load(fh)
        for letter in letters:
            # the stored reading text is already grouped by one of the two rules:
            # strip the commas of four-digit groups back to the page's figures first
            t = re.sub(r'(?<![\d,])(\d),(\d{3})(?![\d,])', r'\1\2', letter.get('text_reading') or '')
            for para in t.split(chr(10) * 2):
                for line, a, b in changed(para, doc):
                    rows.append((os.path.relpath(f, ROOT), doc, line, a, b))
                    counts['corpus'] += 1
    os.makedirs(os.path.join(ROOT, 'review'), exist_ok=True)
    with open(os.path.join(ROOT, 'review', 'numerals_diff.tsv'), 'w', encoding='utf-8', newline='') as fh:
        fh.write('\t'.join(['source_file', 'doc', 'line_text', 'old', 'new']) + '\n')
        for r in rows:
            fh.write('\t'.join(c.replace('\t', ' ').replace('\n', ' ') for c in r) + '\n')
    for k, v in counts.items():
        print(k, v)


if __name__ == '__main__':
    main()
