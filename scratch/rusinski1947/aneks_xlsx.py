# -*- coding: utf-8 -*-
"""aneks_i.xlsx: ANEKS I laid out for the editor's formatting pass.
One sheet, rows in print order, with the print's segment structure
(pages 124-131 for table a, 132-144 for table b per the editor's map)
marked by separator rows; the footnote defs on a second sheet."""
import os, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

HERE = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947'
t = open(os.path.join(HERE, 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()

# parse the annex rows + the note defs
rows = []           # (sheet, num, cells[11])
notes = []          # (label, text)
cur = None
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur and '0139' <= cur <= '0159':
        c = [x.strip() for x in ln.split('|')][1:-1]
        if len(c) >= 11:
            rows.append((cur, int(c[0]), c[:11]))
    m = re.match(r'\[\^(\d+-\d+)\]: (.*)', ln)
    if m and 124 <= int(m.group(1).split('-')[0]) <= 144:
        notes.append((m.group(1), m.group(2).strip()))

# the print's page for each sheet (label = scan - 15)
PAGE = {s: int(s) - 15 for s in
        ['%04d' % i for i in range(139, 160)]}
# the print's segment structure (editor's map + the band inventory):
# (page, kind)  kind: 'title' | 'rows' | 'notes'
SEGMENTS = [
    (124, 'title'), (124, 'rows'), (125, 'rows'), (125, 'notes'),
    (126, 'rows'), (127, 'rows'), (128, 'rows'), (129, 'rows'),
    (129, 'notes1'), (130, 'rows'), (131, 'rows'),
    (131, 'razem'), (131, 'notes12'),
    (132, 'title7'), (132, 'rows'), (133, 'rows'), (134, 'rows'),
    (135, 'rows'), (136, 'rows'), (137, 'rows'), (138, 'rows'),
    (139, 'rows'), (140, 'rows'), (141, 'rows'), (142, 'rows'),
    (143, 'titlec'), (143, 'rows'), (144, 'rows'),
]
sheet_rows = {PAGE[s]: [] for s in PAGE}
for s, num, cells in rows:
    sheet_rows[PAGE[s]].append((num, cells))

HEAD = ['Lp.', 'Nazwa osady w okresie rozbiorów', 'Ówczesna parafia',
        'Nazwa dzisiejsza', 'Rok założ. osady',
        'Charakter terenu przed założ. osady',
        'Przywilej lub wzmianka — sygn. źródła', 'Data',
        'L. dymów wg Tp. 89 lub 90 *', 'dymów oblicz. szacunkowo',
        'Ludn. osad wg Tołł.']

wb = Workbook()
ws = wb.active
ws.title = 'Aneks I'
F = 'Arial'
hf = Font(name=F, size=10, bold=True)
tf = Font(name=F, size=10)
sf = Font(name=F, size=9, italic=True, color='808080')
bfill = PatternFill('solid', fgColor='D9E2F3')
sfill = PatternFill('solid', fgColor='F2F2F2')
thin = Side(style='thin', color='B0B0B0')
bd = Border(left=thin, right=thin, top=thin, bottom=thin)

r = 1
c0 = ws.cell(row=r, column=1, value='ANEKS I — laid out for the '
             'formatting pass; the print repeats the column header on '
             'every page (marked "— header —"); footnote refs kept '
             'inline as [^strona-n].')
c0.font = Font(name=F, size=10, italic=True)
r += 2

SEP = {  # separator-row texts per segment kind
    'title': '[p. %d]  TABELA VI — Osady olęderskie w byłym powiecie '
             'kościańskim w okresie rozbiorów  (title wording pending '
             'SPOT S45)',
    'title7': '[p. %d]  TABELA VII — Osady olęderskie w byłym powiecie '
              'poznańskim w okresie rozbiorów  (title wording pending '
              'SPOT S46)',
    'titlec': '[p. %d]  (the c-series table title — pending SPOT S47)',
    'notes': '[p. %d]  footnotes 1-3 (the "Razem z..." notes — see the '
             'Przypisy sheet)',
    'notes1': '[p. %d]  footnote 1 (the asterisk note — text pending '
              'SPOT S43)',
    'notes12': '[p. %d]  footnotes 1-2 — texts pending SPOT S44',
}

for page, kind in SEGMENTS:
    if kind in SEP:
        ws.cell(row=r, column=1,
                value=SEP[kind] % page).font = sf
        for cc in range(1, 12):
            ws.cell(row=r, column=cc).fill = sfill
        r += 1
        continue
    if kind == 'razem':
        ws.cell(row=r, column=1, value='RAZEM').font = hf
        ws.cell(row=r, column=9, value='2.386').font = hf
        ws.cell(row=r, column=10, value='92').font = hf
        ws.cell(row=r, column=11, value='12.967').font = hf
        for cc in range(1, 12):
            ws.cell(row=r, column=cc).fill = bfill
        r += 1
        continue
    # the header row (the print repeats it on every page)
    for cc, h in enumerate(HEAD, 1):
        cell = ws.cell(row=r, column=cc, value=h)
        cell.font = hf
        cell.fill = bfill
        cell.border = bd
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    r += 1
    for num, cells in sheet_rows.get(page, []):
        ws.cell(row=r, column=1, value=num).font = tf
        for cc, v in enumerate(cells, 2):
            cell = ws.cell(row=r, column=cc, value=v)
            cell.font = tf
            cell.border = bd
            cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=1).border = bd
        r += 1

widths = (6, 34, 16, 18, 10, 20, 34, 14, 12, 10, 12)
for i, w in enumerate(widths, 1):
    ws.column_dimensions[chr(64 + i)].width = w
ws.freeze_panes = 'A4'

# ---- the notes sheet ----
ws2 = wb.create_sheet('Przypisy')
ws2.cell(row=1, column=1, value='label').font = hf
ws2.cell(row=1, column=2, value='text (as transcribed)').font = hf
rr = 2
for lab, txt in notes:
    ws2.cell(row=rr, column=1, value=lab).font = tf
    c = ws2.cell(row=rr, column=2, value=txt)
    c.font = tf
    c.alignment = Alignment(wrap_text=True, vertical='top')
    rr += 1
ws2.column_dimensions['A'].width = 10
ws2.column_dimensions['B'].width = 120

out = os.path.join(HERE, 'literature', 'rusinski1947', 'aneks_i.xlsx')
wb.save(out)
print('saved', out, '| rows:', len(rows), '| annex notes:', len(notes))
