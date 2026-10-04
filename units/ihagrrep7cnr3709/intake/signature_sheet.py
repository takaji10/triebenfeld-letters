# -*- coding: utf-8 -*-
"""The paraphs and signatures of this file, cropped and laid side by side.

    python units/ihagrrep7cnr3709/intake/signature_sheet.py

Writes review/ihagrrep7cnr3709/signatures/index.html and the crops beside it.
The same method as units/iiihamdaiiinr12765/intake/signature_sheet.py; the
groups below are the sorting of 2026-10-04, and notes.md says what was
concluded and what was left alone.

A crop is (label, scan, box), the box as fractions of the staged page image.
"""
import glob
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
 ('Hand 1: the paraph on every paper issued in the Grand Chancellor\'s name. Read as Goldbeck',
  'Eight times, one hand: under "ad acta" on the two reports of summer 1800, under the decree and the '
  'drafts of 7 December, under the decree on the report of 18 December, and under the drafts of 31 '
  'December. The transcription had it as G[?], Gu[?], Gunz[?] and Q[?]nz[?]. The Prince addresses his '
  'petition to the "Groß Canzler", the reply is in the first person, and Heinrich Julius von Goldbeck '
  'held that office in 1800. The text now has G[oldbeck]. Does the mark read as a short form of Goldbeck?',
  [('doc 1, "ad acta", 23 June 1800', '0002', (.66, .27, .96, .36)),
   ('doc 3, "ad Acta", 1 Aug 1800', '0004', (.56, .24, .86, .32)),
   ('doc 7, decree, 7 Dec 1800', '0011', (.42, .43, .72, .51)),
   ('doc 10, 7 Dec 1800', '0013', (.80, .32, .96, .42)),
   ('doc 11, 7 Dec 1800', '0015', (.78, .77, 1, .85)),
   ('doc 12, decree, 31 Dec 1800', '0016', (.38, .09, .68, .17)),
   ('doc 13, 31 Dec 1800', '0017', (.68, .51, .94, .59)),
   ('doc 14, 31 Dec 1800', '0019', (.70, .42, .96, .50))]),
 ('The members of the Government at Poznań, under its three reports',
  'The same signatures three times. Read from the three together and against the list of its '
  'councillors in the state handbook for 1800 and 1801: Danckelman, v Götz, Hering (transcribed '
  '"ferner" and "H[...]"), Fromme, Diederichs, Dannenberg (transcribed "Darmenberg"), Schwarz, Bormann, '
  'v Fischer (transcribed "v Tischer"), Hoening, Leuchert, Richter, Dühring and Herford (the last four '
  'transcribed with doubt marks in several forms).',
  [('doc 1, 18 June 1800', '0002', (0, .78, 1, .97)),
   ('doc 3, 10 July 1800', '0004', (0, .66, 1, .90)),
   ('doc 12, 18 Dec 1800', '0016', (0, .68, 1, .90))]),
 ('Two chancery clerks under the rescripts',
  'Each signs with a day. The second is transcribed "Schwolner[?]" and "Khroener[?]" and is now '
  'Schroener in both places. The first, "Bamg[...]t" and "Bamuzut[?]", is left as transcribed '
  '(perhaps Baumgart).',
  [('doc 9, 10 and 11 Dec 1800', '0012', (0, .66, .6, .88)),
   ('doc 13, 3 and 4 Jan 1801', '0017', (0, .72, .6, .93))]),
 ('"im Bureau zu mundiren": the direction to make the fair copy',
  'Written beside both drafts to the Prince. Transcribed "zu munda[?]" and "nun dir."; now "mundiren" '
  'in both.',
  [('doc 11', '0014', (0, .5, .45, .72)),
   ('doc 14', '0018', (0, .2, .5, .36))]),
 ('Not read: the mark beside the journal number',
  'On each paper that came in, near the number: transcribed "H[?]B[?]", "h qu[?] B", "H qm B." and '
  'not at all on the report of 18 December. Left as transcribed. The number itself is written the '
  'same way each time and is transcribed "B. 3681." once, "No. 5957.", "Nr. 5957." and "Nro. 6334." '
  'elsewhere; those are left as they are too.',
  [('doc 1', '0002', (.20, .93, .60, 1)),
   ('doc 3', '0004', (.03, .55, .40, .63)),
   ('doc 5', '0007', (.03, .79, .45, .92)),
   ('doc 12', '0016', (0, .69, .35, .77)),
   ('doc 3, number', '0004', (0, .86, .45, .94)),
   ('doc 7, number', '0011', (0, .52, .4, .6)),
   ('doc 12, number', '0016', (0, .90, .4, .97))]),
]

PAGE = '''<!doctype html><meta charset="utf-8"><title>Signatures compared</title>
<style>body{font:16px/1.45 Georgia,serif;margin:2rem auto;max-width:70rem;padding:0 1rem;color:#222}
h2{font-size:1.15rem;margin:2.2rem 0 .2rem}p{margin:.2rem 0 1rem;max-width:48rem}
.g{display:flex;flex-wrap:wrap;gap:14px}figure{margin:0;width:330px}
img{width:330px;height:200px;object-fit:contain;background:#eee;border:1px solid #ccc}
figcaption{font:13px/1.3 sans-serif;color:#444}</style>
<h1>I. HA GR, Rep. 7 C, Nr. 3709: the signatures compared</h1>
%s
'''


def main():
    unit = unitlib.one_unit('ihagrrep7cnr3709')
    out = os.path.join(unitlib.review_dir(unit.slug), 'signatures')
    os.makedirs(out, exist_ok=True)
    pages = {os.path.basename(p)[21:25]: p
             for p in glob.glob(os.path.join(ROOT, 'pages', 'I_HA_Rep_7_C_Nr_3709_*.jpg'))}
    body, n = [], 0
    for title, note, crops in GROUPS:
        body.append(f'<h2>{html.escape(title)}</h2><p>{html.escape(note)}</p><div class="g">')
        for label, scan, (x0, y0, x1, y1) in crops:
            n += 1
            im = Image.open(pages[scan])
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
