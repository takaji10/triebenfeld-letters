# -*- coding: utf-8 -*-
"""Consolidate the annex rows into one table (annex_table.json).

Per row, the best representation wins, tiered:
  A: the geometric cells (annex_cells.json) where >= 6 of the spans carry
     text (the unwarped sheets);
  B: the '|' chunk parse (annex_final.json's raw chunks) where >= 4
     chunks;
  C: the recovery/strip raw text, unparsed.
The row keeps its tier and its witnesses; tier-C rows and rows whose
cells look broken (a cell carrying another row's number) are the spot
sheet's material.

Sections: a (kościański) rows 1-111 on 0139-0146; b (poznański) 1-156 on
0147-0157 (ends 'Razem' 20? | 30 484 - checked on the sheet's foot);
c (typu przejściowego) 1-9 on 0158; d (charakteru nieokreślonego) 1-11 on
0158-0159, with the closing 'Ogółem 2.216 | 38 | 514' (the strip read).
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ANNEX = [f'{i:04d}' for i in range(139, 160)]


def main():
    cells = json.load(open(os.path.join(OCR, 'annex_cells.json'),
                           encoding='utf-8'))
    final = json.load(open(os.path.join(OCR, 'annex_final.json'),
                           encoding='utf-8'))
    merged = json.load(open(os.path.join(OCR, 'annex_merged.json'),
                            encoding='utf-8'))
    out = {}
    stats = {'A': 0, 'B': 0, 'C': 0}
    for n in ANNEX:
        rows = {}
        geo = cells[n]['rows']
        fin = final[n]['rows']
        mer = merged[n]['rows']
        nums = sorted(set(int(k) for k in geo) | set(int(k) for k in fin))
        for num in nums:
            g = geo.get(num) or geo.get(str(num))
            f = fin.get(num) or fin.get(str(num))
            entry = {'num': num}
            geo_cells = None
            if g:
                cleaned = [c.replace('|', ' ').replace('¦', ' ')
                           .strip() for c in g['cells']]
                while cleaned and not cleaned[-1]:
                    cleaned.pop()
                if sum(1 for c in cleaned if c) >= 3:
                    geo_cells = cleaned
            if geo_cells and len(geo_cells) >= 5 and not any(
                    len(c) > 60 for c in geo_cells):
                entry['tier'] = 'A'
                entry['cells'] = geo_cells
                entry['witnesses'] = ['geo'] + (f['witnesses'] if f else [])
            elif f and f.get('raw') and len(f['raw']) >= 4:
                entry['tier'] = 'B'
                entry['cells'] = f['cells']
                entry['raw'] = f['raw']
                entry['witnesses'] = f['witnesses']
            else:
                entry['tier'] = 'C'
                w = (mer.get(str(num)) or {}).get('witnesses', {})
                rec = w.get('recovery')
                if rec:
                    entry['raw'] = rec['pol']
                elif f and f.get('raw'):
                    entry['raw'] = f['raw']
                elif geo_cells:
                    entry['cells'] = geo_cells
                    entry['tier'] = 'A'
                entry['witnesses'] = sorted(w) if w else ['?']
            stats[entry['tier']] += 1
            rows[num] = entry
        out[n] = {'rows': rows}
    with open(os.path.join(OCR, 'annex_table.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('tiers:', stats)


if __name__ == '__main__':
    main()
