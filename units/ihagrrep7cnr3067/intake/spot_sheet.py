# -*- coding: utf-8 -*-
"""The editor's spot sheet for I. HA GR, Rep. 7 C, Nr. 3067: the readings the
two readings and Claude could not settle from the scans. Written 2026-11-19.

    python units/ihagrrep7cnr3067/intake/spot_sheet.py        # write the sheet and the pictures
    python pipeline/review/queries.py --unit ihagrrep7cnr3067  # serve it (port 4101)
    python pipeline/review/queries.py --unit ihagrrep7cnr3067 --read

The first option of each row is what the transcription has now. Answers are
applied afterwards through intake/build_pages.py (CORRECTIONS), never here.
"""
import csv
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
REV = os.path.join(ROOT, 'review', 'ihagrrep7cnr3067')
IMG = os.path.join(REV, 'spot_img')
SRC = r'C:/Users/Tersnaus/Downloads/74344_Lacko/I_HA_Rep_7_C_Nr_3067/Process/processed/I_HA_Rep_7_C_Nr_3067_%s.jpg'

# key, document, corpus line, word as written, options, note, (page, box)
ROWS = [
    ('q1', '1', 33, 'befreyt', 'befreyt|befragt',
     'The end of the word broken after "be-" ("von 387. Insurgenten, welche be- / ... worden"). '
     'All three readings saw "freyt"; the figures that follow are sentences, not releases. What does the page have?',
     ('0005_a', (300, 2620, 2598, 2840))),
    ('q2', '2', 101, 'Untersuchung', 'Untersuchung|Erwegung|Betrachtung',
     'The King\'s first line, the word after "Nach genauer". The transcription had "Betrachtung"; '
     'one reading and Claude see "Untersuchung", the other "Erwegung". Marked doubtful [?] for now.',
     ('0006_a2', (0, 1280, 2505, 1560))),
    ('q3', '2', 101, 'verbrach[en?]', 'verbrach[en?]|verbrechen',
     'The last word of the King\'s first line: "verbrach..." or "verbrech..."?',
     ('0006_a2', (1100, 1280, 2505, 1460))),
    ('q4', '2', 105, 'erlegung', 'erlegung|erkennen',
     'The King\'s fifth line, after "seindt zu". The transcription had "erkennen[?]"; Claude reads "erlegung" '
     '(the payment of the fines). Marked doubtful [?] for now.',
     ('0006_a2', (0, 1850, 2505, 2080))),
    ('q5', '2', 106, 'da', 'da|die|die schon',
     'The end of the King\'s sixth line, after "angehalten oder". One reading saw "die schon".',
     ('0006_a2', (0, 1960, 2505, 2250))),
    ('q6', '3', 116, 'dererjenigen', 'dererjenigen|derjenigen',
     'The title of the list, its first word. One reading saw "derjenigen".',
     ('0007_a', (300, 1100, 1400, 1260))),
    ('q7', '3', 162, 'Pistrzkowski', 'Pistrzkowski|Pistzkowski',
     'Entry C 3 of the list. One reading saw no r after "Pist".',
     ('0008_a1', (0, 2580, 1100, 2720))),
    ('q8', '3', 291, 'Mißbrauch', 'Mißbrauch|Mißbrauchs',
     'Entry C 23. Entry C 5 has "Mißbrauchs seines"; one reading saw the s here too.',
     ('0008_a2', (800, 2520, 1600, 2640))),
]


def main():
    os.makedirs(IMG, exist_ok=True)
    out = []
    for key, doc, line, word, opts, note, (pid, box) in ROWS:
        name = f'{key}.jpg'
        Image.open(SRC % pid).crop(box).save(os.path.join(IMG, name), quality=88)
        out.append({'key': key, 'letter': doc, 'line': line, 'word': word,
                    'options': opts, 'note': note, 'image': name})
    with open(os.path.join(REV, 'open_queries.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(out)
    print(f'{len(out)} rows -> review/ihagrrep7cnr3067/open_queries.csv')


if __name__ == '__main__':
    main()
