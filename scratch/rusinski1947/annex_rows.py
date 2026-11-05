# -*- coding: utf-8 -*-
"""Annex-table row extraction for Aneks I of tom5, v2 - from the text.

Orientation findings (2026-11-05):
  - all annex sheets are landscape TIFFs (5936x3999);
  - the odd scans' row-major text comes from the DIRECT read (the main
    OCR job's JSON, 'pol'); the even scans' row-major text comes from the
    rotate(-90) read (rot/<n>.txt, cached by table_rebuild.py);
  - the even scans' DIRECT read is column-major (Tesseract blocks by the
    grid's columns) - kept as the per-column cross-check of the numbers;
  - in the row-major text the grid lines surface as '|' characters, which
    split the row into its cells.

A row starts with its L.b. number leading the line; wrapped cells
continue on lines that do not begin with a number, until the next row
number. Output annex_rows.json: per scan the rows with their cell texts
split on '|', plus the sheet's trailing head lines (the printed page
number and the section title, e.g. 'a. Osady olęderskie ...').
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ANNEX = [f'{i:04d}' for i in range(139, 160)]
EVEN = {f'{i:04d}' for i in range(140, 160, 2)}


def rowmajor_text(n):
    """The row-major text of an annex sheet: psm 4 ('a single column of
    text of variable sizes'), which segments the table's rows instead of
    its columns (the finding of 2026-11-05, after psm 3 blocked the grid
    by columns on several sheets)."""
    cache = os.path.join(OCR, 'rot', n + '.psm4.txt')
    if os.path.isfile(cache):
        return open(cache, encoding='utf-8').read()
    sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
    from pipeline.ocr import read
    t = read(os.path.join(SRC, f'tom5_{n}.tif'), lang='pol', psm=4)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(t)
    return t


def parse(text):
    """Split the text into rows keyed by the leading number."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    rows = []
    head = []
    cur = None
    for l in lines:
        ls = l.lstrip('| ').lstrip()
        m = re.match(r'^(\d{1,3})\s*\|?(.*)$', ls)
        if m and (cur is None or int(m.group(1)) == cur['num'] + 1):
            if cur is not None:
                rows.append(cur)
            cur = {'num': int(m.group(1)), 'lines': [m.group(2)]}
        elif cur is not None:
            cur['lines'].append(l)
        else:
            head.append(l)
    if cur is not None:
        rows.append(cur)
    for r in rows:
        joined = ' '.join(r['lines'])
        cells = [c.strip(' |') for c in joined.split('|')]
        r['cells'] = [c for c in cells if c]
        del r['lines']
    return head, rows


def main():
    out = {}
    for n in ANNEX:
        head, rows = parse(rowmajor_text(n))
        out[n] = {'rows': rows, 'head': head}
        nums = [r['num'] for r in rows]
        gaps = [(a, b) for a, b in zip(nums, nums[1:]) if b != a + 1]
        print(n, 'rows:', len(rows), 'first/last:', nums[:1], nums[-1:],
              'gaps:', gaps)
    with open(os.path.join(OCR, 'annex_rows.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
