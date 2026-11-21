# -*- coding: utf-8 -*-
"""tabele_body.xlsx: the five body tables (TABELA I-V) as checkable
grids. Each sheet: (1) my parsed grid with values in cells (uncertain
cells carry '?' and a comment), (2) the raw transcription lines below
for verification."""
import os, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

HERE = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947'
t = open(os.path.join(HERE, 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
lines = t.splitlines()

wb = Workbook()
F = 'Arial'
hf = Font(name=F, size=10, bold=True)
tf = Font(name=F, size=10)
sf = Font(name=F, size=9, italic=True, color='808080')
warn = Font(name=F, size=10, color='C00000')
hfill = PatternFill('solid', fgColor='D9E2F3')
rfill = PatternFill('solid', fgColor='FDF3D0')
thin = Side(style='thin', color='B0B0B0')
bd = Border(left=thin, right=thin, top=thin, bottom=thin)


def sheet(name, title, grid, widths, raw_start, raw_end, notes=None):
    """grid = list of rows; each row = (style, [cells]); style in
    h( header) / d( data) / s( sub) / t( total)."""
    ws = wb.create_sheet(name)
    c = ws.cell(row=1, column=1,
                value=title + '   —   parsed grid for checking; the raw '
                'transcription lines follow below the grid. Cells '
                'marked "?" are garbled in the scan; red cells = '
                'OCR-garbled values that need the print.')
    c.font = sf
    r = 3
    for style, cells in grid:
        cc = 1
        for v in cells:
            cell = ws.cell(row=r, column=cc, value=v)
            cell.font = hf if style == 'h' else (tf if style != 'w' else warn)
            if style == 'h':
                cell.fill = hfill
                cell.alignment = Alignment(wrap_text=True, vertical='top')
            elif style == 'w':
                cell.fill = rfill
            if style in ('h', 'd', 't'):
                cell.border = bd
            cc += 1
        r += 1
    r += 1
    ws.cell(row=r, column=1, value='--- raw transcription '
            'lines (verbatim from the OCR) ---').font = sf
    r += 1
    for j in range(raw_start - 1, raw_end):
        if lines[j].strip():
            ws.cell(row=r, column=1,
                    value=lines[j]).alignment = Alignment(wrap_text=False)
            ws.cell(row=r, column=1).font = Font(name='Consolas', size=9)
            r += 1
    if notes:
        r += 1
        for nt in notes:
            ws.cell(row=r, column=1, value=nt).font = sf
            r += 1
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    return ws


# ---- TABELA I (p. 26): ludność wiejska / olęderska ----
grid = [
    ('h', ['Powiat', 'Ludność wiejska ogółem',
           'Ludność olęderska (cyfry absolutne)',
           'procentowo']),
    ('d', ['kościański', '105.000', '14.987', '14,3']),
    ('d', ['poznański', '93.500', '13.637', '14,6']),
    ('w', ['z wschowski', '10.900', '?', '?']),
    ('t', ['Województwo poznańskie (w granicach po I rozbiorze)',
           '209.400', '28.624', '13,7']),
]
sheet('TABELA I (p. 26)', 'TABELA I — Ludność wiejska / w tym ludność '
      'olęderska', grid, (44, 22, 26, 12), 765, 790,
      ['The wschowski row shows only 10.900 in the scan; its olęderska '
       'cells print as dashes per the raw line.'])

# ---- TABELA II (p. 61): skład zawodowy, pow. kościański ----
grid = [
    ('h', ['Zawody', 'osoby trudniące się zawodem głównym',
           'osoby trudniące się tym zawodem obok (ubocznie)',
           '% zatrudnionych (jako zaw. głównym)']),
    ('d', ['I. Rolnictwo', '12.643', '162', '97,5']),
    ('s', ['a. gospodarze ol.', '8.805', '—', '69,6']),
    ('s', ['b. komornicy', '1.542', '122', '12,2 (?)']),
    ('s', ['c. czeladź', '1.513', '—', '12,0']),
    ('s', ['d. luźni za robotą', '491', '—', '3,9']),
    ('s', ['e. żebracy', '292', '—', '2,3']),
    ('d', ['2. Karczmarze', '155', '156 (?)', '1,2']),
    ('d', ['3. Młynarze', '14', '42', '0,1']),
    ('d', ['4. Rzemiosło', '142', '—', '1,1']),
    ('d', ['5. Hutnictwo', '7', '—', '0,1']),
    ('w', ['6. Szkolni', '6', '140 (?)', '?']),
    ('t', ['Razem', '12.967', '500', '100,0']),
]
sheet('TABELA II (p. 61)', 'TABELA II — Skład zawodowy ludności 94 osad '
      'pow. kościańskiego wg Tol.', grid, (26, 30, 34, 22), 1296, 1330,
      ['The b. komornicy obok-figure (122) and the Karczmarze/Szkolni '
       'cells are garble-prone in the scan - verify against the print.'])

# ---- TABELA III (p. 62): skład zawodowy, pow. poznański ----
grid = [
    ('h', ['Kategorie', 'osób (zawód główny)',
           'osób (zawód uboczny)', 'liczba rodzin',
           '7 osad maj. kosi- ckiej(?)', '8 osad klasyfikowanych 1773',
           '28 wsi sierakowskiej', 'Razem']),
    ('d', ['I. Rolnictwo', '653', '100', '122 (?)', '601', '—',
           '753 | 3863 | 73 | 91,9', '602 (?)']),
    ('s', ['a. gospodarze ol.', '418', '85', '—', '454', '—',
           '503 | 2888', '—']),
    ('t', ['Razem', '717', '61', '122', '672', '13', '839 | 4204 | 74',
           '100,0']),
]
sheet('TABELA III (p. 62)', 'TABELA III — Skład zawodowy ludności 36 '
      'osad olęderskich powiatu poznańskiego (Zawodowo czynni i bierni)'
      ' — HEAVILY GARBLED; the parse below is a best guess; this table '
      'gets a dedicated pixel repair pass (SPOT S51)',
      grid, (22, 16, 16, 14, 18, 22, 22, 12), 1319, 1332,
      ['Known print markers (editor): b. chałupnicy[^1]; on the '
       'Rolnictwo line: 60[^2] and 13[^2]; on the Ośw. line: 5[^3]; '
       'notes: 1 = źródło miesza chałupników z komornikami; 2 '
       'Karczmarze i młynarze; 3 nauczyciel, 4 lektorów (Vorleser).'])

# ---- TABELA IV (p. 64): uwarstwienie ----
grid = [
    ('h', ['Kompleksy terytorialne', 'Liczba osad',
           'gospod. samodz. (osób)', 'pośrednich (osób)',
           'niesamodz. (osób)', 'razem']),
    ('d', ['Pow. kościański', '94', '8.974', '149 (?)', '3.844',
           '12.967']),
    ('s', ['z pow. poznańskiego: a. osady klasyfikowane wr. 1773',
           '28', '2.494', '90', '948', '3.532']),
    ('s', ['b. maj. sierakowska (r. 1759)', '8', '467', '9', '196',
           '672']),
    ('t', ['Ogółem', '130', '11.935', '248 (?)', '4.988 (?)', '17.171']),
    ('h', ['Cyfry procentowe', '', '', '', '', '']),
    ('d', ['Pow. kościański', '—', '69,2', '1,1', '29,7', '100,00']),
    ('d', ['a. osady klasyfikowane wr. 1773', '—', '70,7', '2,5',
           '26,8', '100,00']),
    ('d', ['b. maj. sierakowska (r. 1759)', '—', '69,5', '1,3', '29,2',
           '100,00']),
    ('t', ['Ogółem', '—', '69,5', '1,4', '29,1', '100,00']),
]
sheet('TABELA IV (p. 64)', 'TABELA IV — Społeczne uwarstwienie ludności '
      'osad olęderskich', grid, (40, 12, 20, 18, 18, 12), 1344, 1375)

# ---- TABELA V (p. 66): charakter gruntów ----
grid = [
    ('h', ['', 'Ogólna liczba osad zapisanych w źródłach',
           'osady na gruntach już uprawianych (wieś/folwark)',
           'osady na gruntach częściowo zarosłych',
           'osady na gruntach zarośniętych (karczunek)']),
    ('d', ['kościański (cyfry absolutne)', '44', '20', '3', '21']),
    ('d', ['poznański (cyfry absolutne)', '78', '17', '3', '58']),
    ('t', ['Razem (absolutne)', '122', '37', '6', '79']),
    ('d', ['kościański (procentowo)', '—', '45,5', '6,8', '47,7']),
    ('d', ['poznański (procentowo)', '—', '21,8', '3,8', '74,4']),
    ('t', ['Razem (procentowo)', '—', '30,3', '4,9', '64,8']),
]
sheet('TABELA V (p. 66)', 'TABELA V — Charakter gruntów, na których '
      'powstały osady olęderskie (column HEADERS are my inference from '
      'body pp. 23-24 - verify against the print)',
      grid, (30, 26, 30, 24, 28), 1381, 1396)

del wb['Sheet']
out = os.path.join(HERE, 'literature', 'rusinski1947', 'tabele_body.xlsx')
wb.save(out)
print('saved', out)
