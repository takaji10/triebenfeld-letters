# -*- coding: utf-8 -*-
"""The third spot sheet, "Sm or Sw in Breyer's notebook" (2026-10-14).

    python units/app539680669/intake/spot_sheet3.py
    python pipeline/review/queries.py --unit app539680669 --sheet readings3.csv

On the second sheet the editor read "Swięcer" where Claude had "Smięcer",
and "St[?]pin" where Claude had "Sm…". Three more readings rest on the same
letters: the two "Smięcia" on the page of field names (0012_a1), which
Claude read without doubt, and the second "[Sm…?]" on 0018_a1. Swięcia is a
place of the edition (reference/places.yml, `swiecia`), with a farm
Broniki; the first field name on 0012_a1 is "Bronikel". Made with the
machinery of spot_sheet2.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spot_sheet2 import main  # noqa: E402

ROWS = [
    ('t01', '0012_a1', 'Aus Smięcia', 'Smięcia', 'Smięcia|Swięcia',
     'At the head of the page of field names, in the old German script: "Aus ...", from .... Read Smięcia without doubt. On the last sheet you read "Swięcer" for what was read "Smięcer". Swięcia is a place in the edition, an estate with a farm called Broniki, and the first field name below is "Bronikel".'),
    ('t02', '0012_a1', 'Budendorf stammt aus Smięcia', 'Smięcia', 'Smięcia|Swięcia',
     'The note at the right of the same line: "Budendorf comes from ...".'),
    ('t03', '0018_a1', 'In [Sm…?] bei 6 Stücke', '[Sm…?]', '[Sm…?]|St[?]pin|Swięcia',
     '"In ... 6 pieces each: about 1868." On the last sheet you read St[?]pin for the same-looking word four lines above ("54 years ago from ...").'),
]
SHIFT = {'t01': 0, 't02': 0, 't03': 0}

if __name__ == '__main__':
    main(ROWS, SHIFT, 'readings3.csv')
