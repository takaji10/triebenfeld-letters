# -*- coding: utf-8 -*-
"""Thousands grouping for the reading text and the English (editor, 2026-10-03).

    316000 -> 316,000      76000 -> 76,000      5000 rt -> 5,000 rt

The diplomatic text and the transcription keep the figures as the page writes
them; only the generated views group them. The comma is the documents' own
separator where they use one ("36,000 rtt", "80,000 écus").

What is grouped:
  - every number of five digits or more;
  - a number of four digits when a currency or measure follows it ("1800 rt",
    "2500 Morgen"), or when it cannot be a year (outside 1500-1899).
What is not:
  - a four-digit year standing alone ("1797", "in 1805");
  - a number already grouped, a decimal, a fraction or the "/m" thousands
    ("25/m"), and any number joined to another digit, full stop or comma;
  - an identifier: after No., Nr., N°, §, Bü, Rep., p., pag., fol., Litt.,
    line, page, letter, scan or document ("Nr. 12765", "Oe 1 Bü 9454").
"""
import re

# Units after which a four-digit number is a sum, not a year.
_UNIT = (r'(?:[Rr]\b|[Rr](?:eichs)?t(?:h|t)?(?:a?l)?(?:e?r)?s?\b|[Rr]thl|Thaler\w*|Taler\w*|'
         r'fl\b|[Ff]lorin\w*|Gulden|[Dd]ucat\w*|[Dd]ukat\w*|écus|Groschen|gg\b|'
         r'Morgen|Morg\b|M\b|Hufen|Pfund|Centz|Ctr|[Mm]ann\b|[Mm]en\b|[Ss]eelen|'
         r'souls|Stück|Klafter|Scheffel|Gr\b|Reichsthaler\w*|Rthaler\w*)')
_ID = re.compile(r'(?:\b(?:No|Nr|Num|N°|Rep|pag|fol|Litt|p|pp)\.?|§|\bBü|\b(?:line|lines|page|pages|'
                 r'letter|letters|scan|document|documents|Nro)\b)\s*$', re.I)
_NUM = re.compile(r'(?<![\d.,/])(\d{4,})(?![\d/]|[.,]\d)')


def _group(s):
    return re.sub(r'(?<=\d)(?=(?:\d{3})+$)', ',', s)


def group_digits(text):
    """`text` with its sums grouped by thousands, as the module says."""
    if not text or not re.search(r'\d{4}', text):
        return text

    def f(m):
        num = m.group(1)
        if num.startswith('0') or _ID.search(text[max(0, m.start() - 12):m.start()]):
            return num
        if len(num) == 4:
            v = int(num)
            unit = re.match(r'\s*' + _UNIT, text[m.end():])
            if 1500 <= v <= 1899 and not unit:
                return num
        return _group(num)
    return _NUM.sub(f, text)
