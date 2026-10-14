# -*- coding: utf-8 -*-
"""The spot sheet "Three more in Breyer's second notebook" (2026-10-14).

    python units/app539680669/intake/spot_sheet5.py
    python pipeline/review/queries.py --unit app539680669 --sheet readings5.csv

On the sheet readings4 the editor could not read two rows because the
picture cut the line off at its foot (u07, u09); they are asked again with
the picture moved down. And the editor read "Firstgugge[?]" where Claude had
"Siebzigjährige", so the word on the line under it, read "Dreissigjährige"
by the same reasoning, is asked too.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spot_sheet2  # noqa: E402
from notebook2 import TEXT2  # noqa: E402

ROWS = [
    ('v01', '5198_a2', '[Rheinwochenmarkt?]', '[Rheinwochenmarkt?]', '[Rheinwochenmarkt?]',
     'Asked again: the last picture cut the line off. In the old German script, the line after the divider: "Es gibt auf ... im Dorfe?" Read Rheinwochenmarkt with doubt.'),
    ('v02', '5199_a1', '[Sachsengänger?]', '[Sachsengänger?]', '[Sachsengänger?]|Sachsengänger',
     'Asked again: the last picture cut the line off. The page in the old German script: "Die ... ... gehen, die Mädchen bringen sehr oft Kinder mit." The two words before "gehen" were read Holländer and Sachsengänger, both with doubt; type the line as you read it.'),
    ('v03', '5203_a1', '[Dreissigjährige?]', '[Dreissigjährige?]', '[Dreissigjährige?]',
     'In the old German script, under the word you read "Firstgugge[?]": the next line, read Dreissigjährige with doubt by the same reasoning as the line above, which you did not confirm.'),
]
SHIFT = {'v01': 1.5, 'v02': 1.5, 'v03': 8.5}

if __name__ == '__main__':
    assert all(r[1] in TEXT2 for r in ROWS)
    spot_sheet2.TEXT.update(TEXT2)
    spot_sheet2.main(ROWS, SHIFT, 'readings5.csv')
