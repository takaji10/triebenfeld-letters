# -*- coding: utf-8 -*-
"""Aneks I rows -> markdown HTML tables, from the psm 4 row-major texts.

The print's columns (the header, scanned 0139: 'Rok | Charakter |
Przywilej lub wzmianka | L. dy- | L. dy- | Ludn.' over 'Nazwa osady w
okresie rozbiorów Polski | Ówczesna parafia | Nazwa dzisiejsza osady |
założ. | terenu założ. na nim sygn. źródła | źródł. o lokacji data lub
przyw. | L. dymów wg Tp. 89 lub 90 | L. dymów oblicz. szacunkowo | Ludn.
osad'):
  1. L.b. (the row number)
  2. Nazwa osady w okresie rozbiorów Polski
  3. Ówczesna parafia
  4. Nazwa dzisiejsza osady
  5. Rok założ. (with 'las'/'role'/'wieś' etc. = Charakter)
  6. Przywilej: sygn. źródła + data (one merged cell in the print)
  7. L. dymów wg Tp. 89/90 (z* = with a star)
  8. L. dymów oblicz. szacunkowo
  9. Ludn. osad

The psm 4 text's cell marks ('|') do not map one-to-one to the columns:
wraps inside a cell also carry them, and some columns merge. The mapping
rule (from the read rows): the last two-three integer-ish tokens of a row
are the three number columns (dymy Tp, dymy szac., ludn.), the leading
tokens before the first '|' are the name columns...

This renderer is written against the real rows once annex_rows.json has
the psm 4 texts; it is a stub until then (see TODO).
"""
