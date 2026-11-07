# -*- coding: utf-8 -*-
"""spot_annex.csv: the ANEKS I structural state after the full
noise-removal pass - resolved rulings (for the record) + open knots."""
import csv

ROWS = [
    ('0139-0159 (ANEKS I)', 'OUT OF SCOPE for now',
     'the editor will edit aneks_i.xlsx (282 rows, print segment '
     'structure marked) and reinsert the tables later; the '
     'markdown transcription is frozen as-is until then'),
]
with open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\spot_annex.csv',
          'w', encoding='utf-8', newline='\n') as fh:
    w = csv.writer(fh)
    w.writerow(['sheet', 'issue', 'detail'])
    w.writerows(ROWS)
print('spot_annex.csv:', len(ROWS), 'rows')
