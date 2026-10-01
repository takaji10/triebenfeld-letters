# -*- coding: utf-8 -*-
"""The paraphs and signatures of this file, cropped and laid side by side.

    python units/iiihamdaiiinr12765/intake/signature_sheet.py

Writes review/iiihamdaiiinr12765/signatures/index.html and the crops beside it.
The officials of this file sign with a few letters and a date, and no one mark
can be read alone; set beside each other they sort into four hands. The groups
below are that sorting (2026-10-01), and notes.md says what was concluded.

A crop is (label, scan, box), the box as fractions of the unsplit scan.
"""
import html
import io
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GROUPS = [
 ('Hand 1: a tall initial and a date. Read "Hbg." by the editor on document 5: Hardenberg',
  'On every draft written in the State Chancellor\'s name (N. S. D.), 1814 to 1816, each time '
  'with the day and month. Absent from the two drafts of 1820, when he no longer led the ministry.',
  [('doc 2, Nov 1814', '0003', (0.655, 0.74, 0.73, 0.82)),
   ('doc 4, "14/3" 1815', '0005', (0.76, 0.095, 0.92, 0.165)),
   ('doc 5, March 1815 (the editor\'s Hbg.)', '0006', (0.72, 0.76, 0.84, 0.88)),
   ('doc 6, margin, "28/4" 1815', '0007', (0.50, 0.215, 0.62, 0.27)),
   ('doc 7, "30/4" 1815', '0010', (0.70, 0.75, 0.84, 0.83)),
   ('doc 10, "3 Jun" 1815', '0013', (0.08, 0.30, 0.20, 0.40)),
   ('doc 11, "21/5" 1815', '0014', (0.38, 0.46, 0.50, 0.56)),
   ('doc 16, "28/4" 1816', '0022', (0.38, 0.385, 0.50, 0.44)),
   ('doc 17, "28/4" 1816', '0023', (0.79, 0.115, 0.92, 0.18)),
   ('doc 26, "21/12" 1816', '0037', (0.70, 0.615, 0.80, 0.675))]),
 ('Hand 2: "St" in one stroke, then g. Read "Stg." by the editor on document 5: Stägemann',
  'Beside Hardenberg\'s on the Vienna drafts, and under the two opinions written in the margins '
  'in April and May 1816, the second time as "Stgm".',
  [('doc 2, Nov 1814', '0003', (0.585, 0.74, 0.655, 0.82)),
   ('doc 5, March 1815 (the editor\'s Stg.)', '0006', (0.62, 0.76, 0.74, 0.88)),
   ('doc 14, margin, "13 April" [1816]', '0018', (0.78, 0.90, 0.92, 0.955)),
   ('doc 19, margin, "7 Mai 16"', '0026', (0.54, 0.54, 0.64, 0.61))]),
 ('Hand 3: "Hoffm" and a date. Read "Hoffm." by the editor on document 22',
  'On the Berlin drafts of 1816 and 1820.',
  [('doc 22, "1 Jul" 1816', '0031', (0.30, 0.60, 0.42, 0.70)),
   ('doc 24, "12/8" 1816', '0033', (0.74, 0.755, 0.825, 0.84)),
   ('doc 29, "12/5" 1820', '0043', (0.32, 0.79, 0.43, 0.88)),
   ('doc 30, "30/5" 1820', '0044', (0.66, 0.675, 0.78, 0.765))]),
 ('Hand 4: two tall strokes joined. Written out "Bal" on document 29: Balan',
  'Closes the decrees and initials the drafts from 1816. The transcription has it as "B.", once as "St.".',
  [('doc 15, 20 Apr 1816', '0020', (0.74, 0.715, 0.84, 0.76)),
   ('doc 17, 1816', '0023', (0.74, 0.115, 0.80, 0.17)),
   ('doc 20, after "18 Juny 16" (read "St.")', '0029', (0.38, 0.175, 0.50, 0.22)),
   ('doc 22, 1816', '0031', (0.40, 0.60, 0.47, 0.70)),
   ('doc 23, margin, "3 Aug 16"', '0032', (0.52, 0.60, 0.64, 0.66)),
   ('doc 24, 1816', '0033', (0.815, 0.755, 0.87, 0.84)),
   ('doc 25, "9/12 16"', '0036', (0.58, 0.47, 0.80, 0.53)),
   ('doc 26, 1816', '0037', (0.79, 0.615, 0.86, 0.675)),
   ('doc 29, 1820 (the editor\'s "Bal")', '0043', (0.42, 0.78, 0.50, 0.90)),
   ('doc 30, 1820, right-hand mark', '0044', (0.80, 0.675, 0.90, 0.76))]),
 ('Not a signature: "B." before a date is Berlin',
  'The decrees end with the place and date and then the initial of hand 4: "B. 18. Juny 16." and '
  'the two strokes. The first letter here is the place, not a name.',
  [('doc 25, "B 9/12 16"', '0036', (0.58, 0.47, 0.70, 0.53)),
   ('doc 30, "B. 29/5 20"', '0044', (0.55, 0.675, 0.70, 0.76))]),
]

PAGE = '''<!doctype html><meta charset="utf-8"><title>Signatures compared</title>
<style>body{font:16px/1.45 Georgia,serif;margin:2rem auto;max-width:70rem;padding:0 1rem;color:#222}
h2{font-size:1.15rem;margin:2.2rem 0 .2rem}p{margin:.2rem 0 1rem;max-width:48rem}
.g{display:flex;flex-wrap:wrap;gap:14px}figure{margin:0;width:230px}
img{width:230px;height:170px;object-fit:contain;background:#eee;border:1px solid #ccc}
figcaption{font:13px/1.3 sans-serif;color:#444}</style>
<h1>III. HA MdA, III Nr. 12765: the signatures compared</h1>
%s
'''


def main():
    unit = unitlib.one_unit('iiihamdaiiinr12765')
    out = os.path.join(unitlib.review_dir(unit.slug), 'signatures')
    os.makedirs(out, exist_ok=True)
    body, n = [], 0
    for title, note, crops in GROUPS:
        body.append(f'<h2>{html.escape(title)}</h2><p>{html.escape(note)}</p><div class="g">')
        for label, scan, (x0, y0, x1, y1) in crops:
            n += 1
            im = Image.open(os.path.join(unit.raw_dir, f'III_HA_MdA_III_Nr_12765_{scan}.jpg'))
            w, h = im.size
            fn = f'{n:02d}_{scan}.jpg'
            im.convert('RGB').crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))) \
              .save(os.path.join(out, fn), quality=90)
            body.append(f'<figure><img src="{fn}" alt=""><figcaption>{html.escape(label)}'
                        f'<br>scan {scan}</figcaption></figure>')
        body.append('</div>')
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(PAGE % '\n'.join(body))
    print(f'{n} crops ->', os.path.join(out, 'index.html'))


if __name__ == '__main__':
    main()
