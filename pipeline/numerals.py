# -*- coding: utf-8 -*-
"""Thousands grouping for the reading text and the English (editor, 2026-10-03).

    316000 -> 316,000      76000 -> 76,000      5000 rt -> 5,000 rt

The diplomatic text and the transcription keep the figures as the page writes
them; only the generated views group them. The comma is the documents' own
separator where they use one ("36,000 rtt", "80,000 écus").

What is grouped:
  - every number of five digits or more;
  - a number of four digits when a currency or measure follows it ("1800 rt",
    "2500 Morgen"), or when it cannot be a year (outside 1500-1999; the
    edition reached 1936 with Breyer's notebooks, 2026-10-14). For the
    medieval holdings the years start at 1100 (YEARS_FROM).
What is not:
  - a four-digit year standing alone ("1797", "in 1805");
  - a year in a Polish date before "r." (roku): "dnia 23 Lipca 1865 r." - the
    month in the genitive, or "dnia", just before it (2026-11-23); "1800 r."
    without one stays a sum (Reichsthaler);
  - a number already grouped, a decimal, a fraction or the "/m" thousands
    ("25/m"), and any number joined to another digit, full stop or comma;
  - a four-digit registry (journal) number at the foot of a line, outside the
    year range and with no unit after it: alone on its line or after a full
    stop and a space, followed by nothing but an optional full stop and closing
    quotes ("4980.", "on the 25th. 4168.") (the editor's report, 2026-11-22:
    registry numbers in Nr. 421); five digits and more keep the rule above;
  - an identifier: after No., Nr., N°, §, Bü, Rep., p., pag., fol., Litt., Kal.,
    line, page, letter, scan or document ("Nr. 12765", "Oe 1 Bü 9454").
"""
import re

# Units after which a four-digit number is a sum, not a year.
_UNIT = (r'(?:[Rr]\b|[Rr](?:eichs)?t(?:h|t)?(?:a?l)?(?:e?r)?s?\b|[Rr]thl|Thaler\w*|Taler\w*|'
         r'fl\b|[Ff]lorin\w*|Gulden|[Dd]ucat\w*|[Dd]ukat\w*|écus|Groschen|gg\b|'
         r'Morgen|Morg\b|M\b|Hufen|Pfund|Centz|Ctr|[Mm]ann\b|[Mm]en\b|[Ss]eelen|'
         r'souls|Stück|Klafter|Scheffel|Gr\b|Reichsthaler\w*|Rthaler\w*)')
_ID = re.compile(r'(?:\b(?:No|Nr|Num|N°|Rep|pag|fol|Litt|p|pp)\.?|\bKal\.|§|\bBü|\b(?:line|lines|page|pages|'
                 r'letter|letters|scan|document|documents|Nro)\b)\s*$', re.I)
# Alone on its line, or after a full stop whose word is a short abbreviation
# ("B.", "N.", "c.") or holds a digit (a day, "25." / "25th."): not after a
# word ("Seehausen. 5000", a sum) or an ellipsis ("... 7720"), checked 2026-11-22
# with pipeline/review/verify_numerals_diff.py.
_REG_BEFORE = re.compile(r'(?:^|\n)[ \t]*$|(?:^|[\s(])(?:[A-Za-z]{1,3}|[^\s.]*\d[^\s.]*)\. $')
# ... but not the total under a column of sums: the line above ends in a figure and a
# unit ("zu Gerathe = 800 rt" / "3631.", Oe 1 Bü 14525, doc. 23).
_SUM_ABOVE = re.compile(r'\d\s*' + _UNIT + r'[ .]*\n[ \t]*$')
_REG_AFTER = re.compile(r'\.?["\'’”»]*[ \t]*(?:\r?\n|$)')
# A Polish date: "dnia 23 Lipca 1865 r." (r. = roku, the year), not "1800 r."
# (Reichsthaler). The month in the genitive, or "dnia", just before the year
# (APŁ 39/98/0/-/1333 printed "1,865 r.", found 2026-11-23).
_PL_DATE_BEFORE = re.compile(r'(?:\bdnia\b|\b(?:[Ss]tycznia|[Ll]utego|[Mm]arca|[Kk]wietnia|[Mm]aja|[Cc]zerwca|'
                             r'[Ll]ipca|[Ss]ierpnia|[Ww]rze[sś]nia|[Pp]a[zź]dziernika|[Ll]istopada|[Gg]rudnia))'
                             r'[^\n]{0,25}$')
_BARE_R = re.compile(r'\s*[Rr]\.?(?![\w])')
_NUM = re.compile(r'(?<![\d.,/])(\d{4,})(?![\d/]|[.,]\d)')


def _group(s):
    return re.sub(r'(?<=\d)(?=(?:\d{3})+$)', ',', s)


# Holdings of medieval documents, where a four-digit number from this year on
# is a year: the Kodeks's texts and notes are full of years such as 1145 or
# 1411, and have no tables of sums (2026-10-16). Everywhere else the floor stays
# 1500, so that a figure such as 1302 in a table of the 1860s is still grouped.
YEARS_FROM = {'kdw': 1100}


def years_from(doc):
    """The first year expected in a document (`doc` a document id "kdw-016",
    or a holding's slug); 1500 when it is not given."""
    slug = (doc or '').rsplit('-', 1)[0] if '-' in (doc or '') else (doc or '')
    return YEARS_FROM.get(slug, 1500)


def group_digits(text, doc=None):
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
            if first_year <= v <= 1999 and _BARE_R.match(text, m.end()) and \
                    _PL_DATE_BEFORE.search(text[max(0, m.start() - 40):m.start()]):
                return num
            before = text[max(0, m.start() - 400):m.start()]
            if (not unit and _REG_AFTER.match(text, m.end())
                    and _REG_BEFORE.search(before) and not _SUM_ABOVE.search(before)):
                return num
        return _group(num)
    return _NUM.sub(f, text)
