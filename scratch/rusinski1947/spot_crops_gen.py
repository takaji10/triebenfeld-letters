# -*- coding: utf-8 -*-
"""Generate the spot-sheet crops: one PNG per item, named S<n>.png,
cropped generously (the full line + neighbours, 3x)."""
import sys, os, json, io, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
OUT = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\spot_crops'
os.makedirs(OUT, exist_ok=True)

# items: (name, scan, needle-or-None, y0, y1) - when a needle is given,
# the band centres on the word's line (+-1 line); else the band is used
ITEMS = [
    ('S01_0065_quote_note',   '0065', None, 3380, 4220),
    ('S02_0029_note1_extent', '0029', None, 1950, 3060),
    ('S03_p24_13915',         '0039', '13.915', 0, 0),
    ('S04_p26_514_dymow',     '0041', '514', 0, 0),
    ('S05_p68_608_morgow',    '0083', '608', 0, 0),
    ('S06_p66_tabelaV_row',   '0081', 'kościański', 0, 0),
    ('S07_p43fn_r1043',       '0058', '1043', 0, 0),
    ('S08_p30fn_r1053',       '0045', '1053', 0, 0),
    ('S09_p16_wysylowo',      '0031', 'Wymysłowo', 0, 0),
    ('S10a_p98_21_razy',      '0113', '21 razy', 0, 0),
    ('S10b_p98_8814',         '0113', '8814', 0, 0),
    ('S11_p86_301_70',        '0101', '301', 0, 0),
    ('S12_p77_beczki',        '0092', 'beczek', 0, 0),
    ('S13_p78_litra',         '0093', '4:58', 0, 0),
    ('S14_p68_wloka_table',   '0083', None, 4150, 4750),
    ('S15_p98_fol(Const unknown', '0113', 'przyorali', 0, 0),
    ('S16_p47_59_sumy',       '0062', 'sprzedażnej', 0, 0),
    ('S17_p100_109kwoty',     '0115', '109', 0, 0),
    ('S18_p43_44_lata',       '0058', 'Ujskich', 0, 0),
    ('S19_p97_german',        '0112', 'Allergnädigst', 0, 0),
    ('S20_annex_0142_dupes',  '0142', None, 0, 5936),
    ('S21_annex_0144_dupes',  '0144', None, 0, 5936),
    ('S22_annex_0146_totals', '0146', None, 0, 5936),
]


def find_band(scan, needle):
    d = json.load(open(os.path.join(OCR, scan + '.json'),
                       encoding='utf-8'))
    for x in d['words']:
        if needle in x[5]:
            return x[1]
    return None


def main():
    cache = {}
    for (name, scan, needle, y0, y1) in ITEMS:
        if needle:
            if scan not in cache:
                with open(os.path.join(SRC, f'tom5_{scan}.tif'),
                          'rb') as fh:
                    cache[scan] = Image.open(io.BytesIO(fh.read()))
                cache[scan].load()
            im = cache[scan]
            t = find_band(scan, needle)
            if t is None:
                print('MISS', name, needle)
                continue
            y0, y1 = max(0, t - 160), t + 220
        if scan not in cache:
            with open(os.path.join(SRC, f'tom5_{scan}.tif'), 'rb') as fh:
                cache[scan] = Image.open(io.BytesIO(fh.read()))
            cache[scan].load()
        im = cache[scan]
        W, H = im.size
        y1 = min(H, y1)
        c = im.crop((0, y0, W, y1))
        scale = 3 if (y1 - y0) < 1200 else 2
        c = c.resize((W * scale, (y1 - y0) * scale), Image.LANCZOS)
        c.save(os.path.join(OUT, name + '.png'))
        print('crop', name, scan, y0, y1, 'x%d' % scale)


if __name__ == '__main__':
    main()
