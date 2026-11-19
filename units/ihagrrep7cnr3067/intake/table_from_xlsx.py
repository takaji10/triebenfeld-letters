# -*- coding: utf-8 -*-
"""The list of the condemned (document 3) as a table: the editor's spreadsheet
I_HA_Rep_7_C_Nr_3067_tables.xlsx turned into intake/table.csv, the cells
build_pages.py fills. Written 2026-11-19 at the editor's word ("It should
already be in table format in the Downloads folder as
I_HA_Rep_7_C_Nr_3067_tables.xlsx"). Run once; the CSV is the record.

    python units/ihagrrep7cnr3067/intake/table_from_xlsx.py [path to the .xlsx]

The spreadsheet has one sheet per block of the page 0008, its cells holding
the editor's lines (line breaks inside a cell, "¬" kept): the column heads; the
sections A and B, each entry in one cell (number and name on the first line,
the offence below); the heading of C and C 1-9; the heads repeated and C
10-26. Nothing in a cell is changed here. Three things are structured:

- A and B: each entry's first line "1, Franz von Wittwicki," is split into the
  number and the name, the lines below are the offence. A 1 and 2 share one
  offence, joined on the page by a brace: it stands in the row of 1, and 2's
  offence cell is empty.
- C 20 and 21 share one row of the sheet, one offence and one month, joined by
  braces: two rows, the offence and the month in 20's.
- The title page (0007_a), which the spreadsheet does not hold, is not part of
  the table: it is text, line by line (the editor, 2026-11-19).

Columns: page, then the five of the list (Nummer, Nahmen, Art des
Verbrechens, Dauer der Strafe, Anfang derselben).
"""
import csv
import io
import os
import re
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Tersnaus\Downloads\I_HA_Rep_7_C_Nr_3067_tables.xlsx'
OUT = os.path.join(HERE, 'table.csv')


def cells(ws):
    rows = [[('' if c is None else str(c)) for c in r] for r in ws.iter_rows(values_only=True)]
    rows = [r for r in rows if any(c.strip() for c in r)]
    assert rows[0][0].startswith('I_HA_Rep_7_C_Nr_3067_0008'), rows[0]
    return [(r + [''] * 5)[:5] for r in rows[1:]]     # the first row names the scan


def main():
    wb = openpyxl.load_workbook(XLSX)
    s1, s2, s3, s4 = wb.worksheets
    out = []
    (head,) = cells(s1)
    out.append(['0008_a1'] + head)
    for (cell, *rest) in cells(s2):
        assert not any(c.strip() for c in rest)
        lines = cell.split('\n')
        if re.match(r'^[AB]\. ', lines[0]):
            assert len(lines) == 1
            out.append(['0008_a1', '', cell, '', '', ''])
            continue
        heads = [l for l in lines if re.match(r'^\d+, ', l)]
        body = lines[len(heads):]
        assert heads and lines[:len(heads)] == heads, lines
        for k, h in enumerate(heads):
            no, name = h.split(' ', 1)
            out.append(['0008_a1', no, name, '\n'.join(body) if k == 0 else '', '', ''])
    for r in cells(s3):
        if not re.match(r'^\d', r[0]) and not any(c.strip() for c in r[1:]):
            # the heading of C, a merged cell across the sheet: a section
            # heading of the table, in the name column as A's and B's
            out.append(['0008_a1', '', r[0], '', '', ''])
            continue
        out.append(['0008_a1'] + r)
    for r in cells(s4):
        if '\n' in r[0]:                                  # 20 and 21
            nos, names, lens = r[0].split('\n'), r[1].split('\n'), r[3].split('\n')
            assert len(nos) == len(names) == len(lens) == 2, r
            out.append(['0008_a2', nos[0], names[0], r[2], lens[0], r[4]])
            out.append(['0008_a2', nos[1], names[1], '', lens[1], ''])
        else:
            out.append(['0008_a2'] + r)
    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['page', 'no', 'name', 'offence', 'length', 'begin'])
        w.writerows(out)
    print(f'{len(out)} rows -> {OUT}')


if __name__ == '__main__':
    main()
