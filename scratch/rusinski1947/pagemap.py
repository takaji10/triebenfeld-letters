# -*- coding: utf-8 -*-
"""The printed-page <-> scan map of tom5 (Rusinski 1947).

Established 2026-11-05 from the chapter anchors (ROZDZIAŁ I at scan 0027 =
p. 12; II at 0037 = p. 22; III at 0052 = p. 37; IV at 0070 = p. 55; V at
0126 = p. 111; Uwagi końcowe at 0136 = p. 121; ANEKS II at 0160 = p. 145;
ANEKS III at 0166 = p. 151 — all scan - 15) and the roman front matter
(title page scan 0006 = I, contents 0008-0009 = III-IV, Wykaz skrótów
0010-0015 = V-X — scan - 5). The running heads' own digits are unreliable
(7 reads as 1 on the 70s, 5 as 0), so the labels come from the offset and
are verified at the anchors, not from the heads.

The four annex-table landscape sheets (0140, 0142, 0144, 0146, 0148, 0150,
0152, 0154, 0156 — the even scans between 0139 and 0157) continue the table
rows of the portrait sheets around them; their printed numbers are taken
from the rotated re-reads in table_rebuild.py.
"""
from functools import lru_cache

# scan -> printed label; the ranges, computed once
FRONT = {f'{i:04d}': i - 5 for i in range(6, 16)}      # I-X (roman)
BODY = {f'{i:04d}': i - 15 for i in range(16, 138)}    # 1-122
# 0138: the ANEKSY divider leaf (unnumbered)
# 0139-0159: Aneks I; the portrait sheets carry printed numbers that
# continue 123ff. The landscape sheets' labels are set by table_rebuild.py.
# 0160-0165: Aneks II, 145-150 (scan - 15 again: 160-15=145 ✓, 165-15=150 ✓)
# 0166-0171: Aneks III, 151-156 (166-15=151 ✓)
ANEKS2 = {f'{i:04d}': i - 15 for i in range(160, 166)}
ANEKS3 = {f'{i:04d}': i - 15 for i in range(166, 172)}
# 0172-0175: the plans and the map (plates, not transcribed)

LANDSCAPE = {f'{i:04d}' for i in range(140, 159, 2)}
PORTRAIT_A = {f'{i:04d}' for i in range(139, 160, 2)}


@lru_cache(maxsize=None)
def label(scan):
    """The printed label of a scan, or None where the plate carries none
    settled yet."""
    if scan in FRONT:
        return to_roman(FRONT[scan])
    if scan in BODY:
        return str(BODY[scan])
    if scan == '0138':
        return None            # ANEKSY divider, unnumbered
    if scan in PORTRAIT_A:
        return str(int(scan) - 15)   # continues 123ff. (0139 = 124? verified
                                     # against its header page in the rebuild)
    if scan in LANDSCAPE:
        return None            # settled by the rotated re-read
    if scan in ANEKS2 or scan in ANEKS3:
        return str(int(scan) - 15)
    return None


def to_roman(n):
    vals = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    out = ''
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out
