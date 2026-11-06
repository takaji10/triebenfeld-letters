# -*- coding: utf-8 -*-
"""Print-verified cell fixes for the ANEKS I tables (annex_md.json
layer). Each entry: (sheet, row, cell_index 0-10) -> the cell text as
read from the print (pixel/high-zoom verified). Applied by compose.py
after loading annex_md.json.

The date cells (index 7) carry the strip OCR's l->1 / doubled-1 glue:
'11757'->'1757', '11735'->'1735' (the doubled leading 1 - same
artifact as the pixel-verified 0140 r23), 'VII1762'->'VII 1702'
(0139 r9: pixel-verified 1702), plus the missing space after the
month ('XI1720'->'XI 1720')."""

CELL_FIXES = {
    ('0139', 7, 7): '11 XI 1720',
    ('0139', 9, 7): '6 VII 1702',
    ('0139', 11, 7): '18 IV 1785',
    ('0140', 18, 7): '10 X 1721',
    ('0140', 21, 7): '18 XI 1748',
    ('0140', 23, 7): '11 X 1757',
    ('0141', 39, 7): '20 XI 1729 20 I 1749',
    ('0141', 44, 7): '14 X 1735',
    ('0144', 84, 7): '3 VII 1760',
    ('0147', 13, 7): '28 VII 1776',
    ('0148', 17, 7): '1 IV 1781',
    ('0148', 27, 7): '11 XI 1735 20 X 1744',
    ('0151', 68, 7): '24 V 1737',
    ('0151', 69, 7): '9 VII 1701',
    ('0151', 72, 7): '3 III 1614 1 V 1677',
    ('0152', 83, 7): '11 XI 1723',
    ('0156', 136, 7): '1 XI 1751',
    # the print's '*' markers (body p. 23-24: dymy given 'zbiorowo' in
    # Tp. 89, estimated per Tp. 90) - star on the dymyTp value
    ('0139', 9, 8): '20 *',
    ('0140', 21, 8): '22 *',
    ('0140', 26, 8): '12 *',
    ('0141', 36, 8): '38 *',
    ('0142', 48, 8): '21 *',
    ('0142', 54, 8): '7 *',
    ('0144', 77, 8): '5 *',
    ('0144', 78, 8): '17 *',
    ('0147', 1, 8): '4 *',
    ('0147', 12, 8): '24 *',
    ('0148', 15, 8): '5 *',
    ('0148', 17, 8): '13 *',
    ('0148', 22, 8): '22 *',
    ('0148', 24, 8): '8 *',
    ('0149', 44, 8): '6 *',
    ('0149', 48, 8): '4 *',
    ('0150', 62, 8): '36 *',
    ('0151', 74, 8): '8 *',
    ('0151', 75, 8): '22 *',
    ('0151', 77, 8): '21 *',
    ('0151', 79, 8): '2 *',
    ('0152', 82, 8): '7 *',
    ('0152', 83, 8): '10 *',
    ('0152', 84, 8): '10 *',
    ('0152', 85, 8): '5 *',
    ('0152', 87, 8): '5 *',
    ('0152', 91, 8): '38 *',
    ('0153', 103, 8): '13 *',
    ('0155', 119, 8): '22 *',
    ('0155', 123, 8): '12 *',
    ('0155', 127, 8): '15 *',
    ('0158', 1, 8): '12 *',
    ('0159', 1, 8): '9 *',
    ('0159', 3, 8): '7 *',
}


def apply(amd):
    n_fixed = 0
    for (n, num, ci), txt in CELL_FIXES.items():
        for r in amd.get(n, {}).get('rows', []):
            if r['num'] == num:
                if r['cells'][ci] != txt:
                    r['cells'][ci] = txt
                    n_fixed += 1
                break
    return n_fixed
