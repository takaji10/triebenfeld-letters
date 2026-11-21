# -*- coding: utf-8 -*-
"""Assemble SPOT_SHEET.md: the decision items for the editor, with the
data tables (orphan definitions, number-context marker placements,
short marker pages, annex row faults) collected from the pipeline
products."""
import json, os, re, csv
from collections import defaultdict

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
HERE = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947'
T = open(os.path.join(HERE, 'original.md'), encoding='utf-8').read()

labels = set(re.findall(r'\[\^([\w.-]+)\](?!:)', T))
defs = re.findall(r'\[\^([\w.-]+)\]:\s*([^\n]*)', T)
defmap = dict(defs)
orphans = [(lbl, defmap.get(lbl, '')) for lbl, _ in defs
           if lbl not in labels]

# num_ctx placements from markers.json
mk = json.load(open(os.path.join(OCR, 'markers.json'),
                    encoding='utf-8'))
numctx = []
for n, lst in mk.items():
    for x in lst:
        if x.get('num_ctx'):
            numctx.append((str(int(n) - 15), x['label'], x['tok']))

# short pages
shorts = []
for n in sorted(mk):
    want = 0
    got = len(mk[n])
    shorts.append((str(int(n) - 15), got, want)) if False else None
s4 = json.load(open(os.path.join(OCR, 'structure4.json'),
                    encoding='utf-8'))
shorts = [(str(int(n) - 15), len(mk[n]), len(s4[n]['notes']))
          for n in mk if len(mk[n]) < len(s4[n]['notes'])]

L = []
L.append('# SPOT SHEET — Rusiński 1947, OCR draft review')
L.append('')
L.append('Crops: `literature/rusinski1947/spot_crops/S<n>_*.png`.')
L.append('Each item: what the draft says, what is doubtful, my reading,')
L.append('the alternatives. A tick or a correction per item is all I need.')
L.append('')
L.append('## A. Boundaries / note structure')
L.append('')
L.append('**S01 — p. 50 (scan 0065): the quotation after "W nielicznych wypadkach".**')
L.append('The body ends mid-sentence ("…W nielicznych wypadkach", the sentence')
L.append('resumes on p. 51 "wybór wymagał zatwierdzenia…"). Then follows the')
L.append('old-Polish quotation "z pierwszego małżeństwa dzieci równo należeć maią…",')
L.append('and then note "1 Kar. II, fol. 239.". I read the quotation as NOTE 1 of')
L.append('p. 50 (the wilkierz quote; its marker + first words sit on a line that')
L.append('defeats OCR even at 6x — left as body text in the draft). If it is a')
L.append('note, it also needs its marker\'s anchor in the body (which word carries')
L.append('marker 1?). Crop: S01.')
L.append('')
L.append('**S02 — p. 14 (scan 0029): is the long commentary ONE note or several?**')
L.append('Note 1 = "Podaną cyfrę trudno skontrolować…" runs ~9 printed lines of')
L.append('settlement commentary (Dąbrowo, Grabowiec, Łoskońskie… Goraj) set solid,')
L.append('no readable marker digits. I take it as one note; if the print splits it')
L.append('(2., 3. …), the split points are in the crop. Crop: S02.')
L.append('')
L.append('## B. Numbers (each could change a figure)')
L.append('')
items_b = [
    ('S03', 'p. 24', '"wynosi 13.915 dymów… brak zatem 552 dymów"',
     '13.915 conflicts with the arithmetic (13.353+552=13.905); 552×6,41=3.538 fits the given person-count',
     '13.905 (the total is the misread digit)'),
    ('S04', 'p. 26', '"514 dymów… współczynnik 6.05, otrzymamy 3.122 osoby"',
     '514×6,05=3.110, not 3.122', 'either "516 dymów" or "3.110 osób"'),
    ('S05', 'p. 68', '"na włókę liczono 50 lub nawet 608 morgów"',
     '608 impossible (a włóka = 60 morgów); the trailing 8 looks like a footnote marker fused to "60"',
     '"60 morgów" (the 8 = marker 4?)'),
    ('S06', 'p. 66 (Tabela V)', '"kościański … 45,5 | 6,8 | 41,7"',
     'the row must sum to 100 and 41.7% of 44 settlements ≠ 21',
     'third value "47,7" (21/44)'),
    ('S07', 'p. 43, note', '"W r. 1043 olędrom Marianowa przedłużono dzierżawę na lat 30"',
     'impossible year; the same note\'s context is 1677+', '"r. 1643"'),
    ('S08', 'p. 30, note', '"Inwentarz z r. 1053 odróżnia wsie polskie…"',
     'impossible year; the parallel note cites the same inventory as r. 1653', '"r. 1653"'),
    ('S09', 'p. 16', '"Tp. 89, 90 — Wymysłowo, 1889 — 1 dym, 1890 — 1 dym"',
     'impossible years; the passage is about Tp. 89/90 = 1789/1790', '"1789 — 1 dym, 1790 — 1 dym"'),
    ('S10a', 'p. 98', '"Jest jednak od niego 21 razy większa. Czynsz wynosił 2627 zł."',
     '6588/2627 ≈ 2.5, not 21', '"2½ razy większa"'),
    ('S10b', 'p. 98', '"na włókę przypadnie: w Nowych Dworach 8814 zł"',
     'larger than the 3187 zł total', '"88 zł 14 gr"'),
    ('S11', 'p. 86', '"wahając się… od 301 do 70? tynfów"',
     'range must be 30–70 (przeciętnie 50)', '"od 30 do 70 tynfów"'),
    ('S12', 'p. 77', '"wyszynk roczny wynosił 229 beczek 56 garncy piwa, oraz 12 beczek -12121/ garnca wódki"',
     'digit mush; the beer/wódka ratio suggests 12 beczek i 12½ garnca',
     'verify both numbers'),
    ('S13', 'p. 78', '"garnca berlińskiego, który zawierał 4:58 litra"',
     'the colon is not a decimal separator in this book', '"3,58" or "4,58 litra"'),
    ('S14', 'p. 68', 'the inline table: włóka area per pręt length',
     'the draft reduced it to glyph soup; recoverable: 7½ łokci→16,80 ha; 8→19,10; 8½→21,58; 9→24,20 (math checks)',
     'confirm the four pairs'),
    ('S15', 'p. 98', '"przyorali sobie 52/5, a w Folsztynie 4%/, włóki"',
     'fraction glyphs; the Folsztyn figure fits ~4¾', 'read both fractions'),
    ('S16', 'p. 47', '"wyjątkowo 59/, sumy sprzedażnej"',
     '"5%" or "5/9 of the sale sum" — different meanings', 'carried from the earlier sitting'),
    ('S17', 'p. 100', '"nie przekroczy 109%/; kwoty czynszowej"',
     '109% of the rent is odd; possibly 1/9 or 10%', 'read the glyph'),
    ('S18', 'p. 43', '"W Ol. Ujskich dzierżawa wynosiła 44 lata 3, w Ol. Nowe Dwory 60 lat"',
     'the stray "3," after "lata" — marker 3 riding the number?',
     'confirm "44 lata" and the "3"'),
]
for tag, page, says, why, guess in items_b:
    L.append('**%s — %s.** Draft: %s' % (tag, page, says))
    L.append('Why doubtful: %s. My guess: %s. Crop: %s.' % (why, guess, tag))
    L.append('')
L.append('## C. Markers and labels')
L.append('')
L.append('The print sets its footnote markers as inline full-size digits, so a')
L.append('standalone digit in text is ambiguous (marker vs number). Where the')
L.append('context looked number-like I KEPT the digit and placed the label after')
L.append('it — those placements are listed in `spot_numctx.csv` (%d items) and' % len(numctx))
L.append('deserve a glance: if a listed digit is actually the marker, the label')
L.append('sits one token late (harmless); if it is a real number, all good.')
L.append('')
L.append('%d footnote definitions lack their in-text anchor' % len(orphans))
L.append('(`spot_orphan_defs.csv`: printed page, note no., text). They are real')
L.append('notes; their markers were lost by OCR. Locating them needs the print')
L.append('(the page crops on request).')
L.append('')
L.append('Pages whose recovered markers fall short of the note count:')
L.append('%s — the missing markers\' positions are the crop targets.' %
         ', '.join(p for p, g, w in shorts))
L.append('')
L.append('## D. ANEKS I tables')
L.append('')
L.append('Column splitting is a separate open task; what needs YOUR eyes is row')
L.append('IDENTITY: duplicated rows, merged rows, broken numbering (the list is')
L.append('in `spot_annex.csv`, worst: sheet 0142 rows 48–61; sheet 0144 rows')
L.append('75–86 doubled; sheet 0146 the Razem row merged into row 111; sheet')
L.append('0143\'s 85/80 misreads as 65/60). Full-sheet crops: S20, S21, S22.')
L.append('')
L.append('## E. The German petition, p. 97')
L.append('')
L.append('The 1743 petition of the Ujskie Olędry is quoted in German at length;')
L.append('the OCR is heavily corrupted ("Allcrgnidigst", "gintzlich"). If the')
L.append('quote matters for the edition, it needs a careful re-read (crop S19);')
L.append('otherwise mark it "quote, corrected against nothing" and I leave it')
L.append('as-is with a sic.')
L.append('')
L.append('## F. Resolved without you (for the record)')
L.append('')
L.append('- p. 8: the solid-set note block = ONE long note (verified by a 6x')
L.append('  read of the number column: single marker "1", then 2, 3, 4 —')
L.append('  Beheim/Kremmer/Zmiany are notes 2-4).')
L.append('- p. 8/9, 14, 18, 28, 43, 50/51: the "footnote merged into body" class')
L.append('  — all traced to psm4 line fusions and marker-glyph misreads; fixed')
L.append('  in the parse, verified by band reads.')
L.append('- The percent/fraction artifact family: 99 tokens each re-read at 5x,')
L.append('  the glyph itself decided; 92 fixes applied. The residue is in §B.')
L.append('- "44 lata / 60 lat" (p. 43), "co 4 tygodnie" (p. 53) — the numbers the')
L.append('  earlier draft had lost behind footnote labels are back in the text.')
L.append('- The wilkierz clause numbering (ANEKS III): the print\'s markers')
L.append('  2.-44. are largely unread — flagged in §D-adjacent, crops on request.')
L.append('')

with open(os.path.join(HERE, 'SPOT_SHEET.md'), 'w', encoding='utf-8',
          newline='\n') as fh:
    fh.write('\n'.join(L))

with open(os.path.join(HERE, 'spot_orphan_defs.csv'), 'w', encoding='utf-8',
          newline='\n') as fh:
    w = csv.writer(fh)
    w.writerow(['page_note', 'text'])
    for lbl, txt in orphans:
        w.writerow([lbl, txt[:160]])

with open(os.path.join(HERE, 'spot_numctx.csv'), 'w', encoding='utf-8',
          newline='\n') as fh:
    w = csv.writer(fh)
    w.writerow(['page', 'label', 'digit_token'])
    w.writerows(numctx)

print('SPOT_SHEET.md written; orphans:', len(orphans),
      'numctx:', len(numctx), 'short pages:', len(shorts))
