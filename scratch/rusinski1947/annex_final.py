# -*- coding: utf-8 -*-
"""Consolidate the annex rows: valid row numbers, cells -> columns.

The row numbers restart at 1 within each section (a. kościański 1-90;
b. poznański 1-160; c. the 'Osady typu przejściowego' 1-9; d. the 'Osady
o charakterze nieokreślonym' 1-11, per the sheet headings read on 0158
and 0159). A candidate number is valid only where it continues its
section's chain (prev+1, or 1 for a section head); the dates misparsed
as row numbers (167, 174, 191, 199...) break the chain and drop out.

Cell mapping (the print's nine columns):
  1 L.b. | 2 Nazwa osady (rozbiorów) | 3 Ówczesna parafia | 4 Nazwa
  dzisiejsza | 5 Rok założ. + charakter | 6 Przywilej: sygn. źródła +
  data | 7 L. dymów Tp. 89/90 | 8 L. dymów szacunkowo | 9 Ludn. osad
The rule: the row's '|' chunks are walked from the end - the last chunk
carrying an integer (or '—') is Ludn., the one before it szacunkowo, the
one before it Tp.; the chunk carrying a siglum (AW., Rel., AGH, KI., Dom.,
MG, MGd, TV, TW, VO, Q, O, Szk., Kat., AM., Inser.) or a day-month-year
date is the privilege; the chunk carrying a year 1500-1800 (+ charakter
words: las, zarośla, wieś, rola..., folwark, młyn, karczma) is the
foundation year; the first chunks in order are name, parish, modern name.

Output: annex_final.json: per scan, per row {num, cells: [9 strings],
witnesses}. Single-witness rows keep a flag for the spot sheet.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ANNEX = [f'{i:04d}' for i in range(139, 160)]

SIGLA = re.compile(
    r'\b(AW\.?|AGH\.?|Rel\.?\s*(Cost\.?|Posn\.?|Valc\.?|Vsch\.?)?|KI\.?|'
    r'Kl\.?|Dom\.?|MGd?|TV|TW|VO\s*\d+|Q\b|O\s*\d+|Szk\.?|Kat\.?|AM\.?|'
    r'Inser\.?|Sf\.?|Tp\.?|Kośc\.?|Landr\.?|M\.?\s*Schr\.?|M\s*\d+|'
    r'Goldmann|G\b)', re.UNICODE)
DATE = re.compile(r'\b\d{1,2}\s*[IVX]{1,4}\s*\d{3,4}\b|\b\d{1,2}[IVX]{2,4}\d{3,4}\b')
YEAR = re.compile(r'\b1[5-8]\d{2}\b')
NUMCOL = re.compile(r'^[—\-0-9.*\s/,%]*$')


def chunks_of(row_witness, num):
    """The row's cells: the merged '|' chunks of its best witness.
    A recovery band may carry the row's neighbours (bands overlap); its
    text is re-split by leading numbers and the requested row's segment
    is used."""
    for key in ('recovery', 'strip', 'psm4'):
        w = row_witness.get(key)
        if not w:
            continue
        if key == 'recovery':
            text = w['pol']
            # split into row segments, keep the requested one; the band's
            # own reading of the row number may drop a leading digit
            # ('17' for 77) or lose it, so a segment qualifies when its
            # number's last digit(s) match the wanted row and the wanted
            # number is not itself present
            segs = {}
            cur = None
            for l in text.split('\n'):
                l = l.strip().strip('|').strip()
                if not l:
                    continue
                m = re.match(r'^\|?\s*(\d{1,3})\s*[\|.,;]?\s*(.*)$', l)
                if m and 1 <= int(m.group(1)) <= 200:
                    cur = int(m.group(1))
                    segs.setdefault(cur, []).append(m.group(2))
                elif cur is not None:
                    segs[cur].append(l)
            if num in segs:
                text = ' '.join(segs[num])
            else:
                hit = None
                for k in segs:
                    if k % 100 == num % 100 and (k == num
                                                 or k // 100 != num // 100
                                                 or abs(k - num) <= 60):
                        hit = k
                        break
                if hit is None:
                    continue
                text = ' '.join(segs[hit])
        elif key in ('strip', 'psm4'):
            if 'cells' in w and w['cells']:
                return w['cells']
            text = ' '.join(w.get('lines', [])) if 'lines' in w \
                else w.get('raw', '')
        parts = [p.strip(' |') for p in text.split('|')]
        parts = [p for p in parts if p]
        if parts:
            return parts
    return []


def map_columns(cells):
    """Assign the row's chunks to the nine columns."""
    out = [''] * 9
    if not cells:
        return out
    cells = list(cells)
    # 9, 8, 7: walk from the end for the three number columns
    idx = len(cells) - 1
    for col in (9, 8, 7):
        while idx >= 0 and not cells[idx].strip():
            idx -= 1
        if idx < 0:
            break
        c = cells[idx]
        if NUMCOL.match(c) or re.fullmatch(r'\d{1,4}[.*]?', c.strip()):
            out[col - 1] = c
            idx -= 1
        else:
            break
    # 6: privilege - the chunk with a siglum or a date, near idx
    for j in range(idx, -1, -1):
        c = cells[j]
        if SIGLA.search(c) or DATE.search(c):
            out[5] = c
            # fold following chunks that continue the siglum (dates, fol.)
            k = j + 1
            while k <= idx and k < len(cells) and not YEAR.search(cells[k]) \
                    and not re.match(r'^\d', cells[k]):
                out[5] += ' ' + cells[k]
                k += 1
            idx = j - 1
            break
    # 5: the foundation year + charakter
    for j in range(idx, -1, -1):
        c = cells[j]
        if YEAR.search(c):
            out[4] = c
            idx = j - 1
            break
    # 2, 3, 4(name): the leading chunks in order
    lead = [c for c in cells[:idx + 1]]
    if lead:
        out[1] = lead[0]
        if len(lead) > 1:
            out[2] = lead[1]
        if len(lead) > 2:
            out[3] = ' '.join(lead[2:])
    return out


def main():
    merged = json.load(open(os.path.join(OCR, 'annex_merged.json'),
                            encoding='utf-8'))
    final = {}
    problems = []
    for n in ANNEX:
        rows = merged[n]['rows']
        # chain-filter the numbers (JSON keys are strings): the longest
        # chain where each next number continues (prev+1..prev+8, gaps
        # allowed for OCR misses) or restarts at 1 after a section end
        # (>= 5 above). Junk numbers (dates misparsed: 167, 174, 1152...)
        # never fit and drop out.
        cands = sorted(int(k) for k in rows if str(k).isdigit())
        best = []
        for start in range(len(cands)):
            chain = [cands[start]]
            for num in cands[start + 1:]:
                prev = chain[-1]
                if 1 <= num - prev <= 8 or (num == 1 and prev >= 5):
                    chain.append(num)
            if len(chain) > len(best):
                best = chain
        valid = best
        outrows = {}
        for num in valid:
            w = rows[str(num)]['witnesses']
            cells = chunks_of(w, num)
            cols = map_columns(cells)
            outrows[num] = {'cells': cols, 'witnesses': sorted(w),
                            'raw': cells}
            if len(w) == 1:
                problems.append((n, num, sorted(w)))
        final[n] = {'rows': outrows}
        print(n, 'rows kept:', len(outrows),
              'span:', (min(outrows), max(outrows)) if outrows else '-')
    with open(os.path.join(OCR, 'annex_final.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(final, fh, ensure_ascii=False)
    print('single-witness rows:', len(problems))


if __name__ == '__main__':
    main()
