# -*- coding: utf-8 -*-
"""Print-verified cell fixes for the ANEKS I tables (annex_md.json
layer). Each entry: (sheet, row, cell_index 0-10) -> the cell text as
read from the print (pixel/high-zoom verified). Applied by compose.py
after loading annex_md.json.

The date cells (index 7) carry the strip OCR's l->1 / doubled-1 glue:
'11757'->'1757', '11735'->'1735' (the doubled leading 1 - same
artifact as the pixel-verified 0140 r23), 'VII1762'->'VII 1702'
(0139 r9: pixel-verified 1702), plus the missing space after the
month ('XI1720'->'XI 1720')."""

CELL_FIXES = {
    ('0139', 7, 7): '11 XI 1720',
    ('0139', 9, 7): '6 VII 1702',
    ('0139', 11, 7): '18 IV 1785',
    ('0140', 18, 7): '10 X 1721',
    ('0140', 21, 7): '18 XI 1748',
    ('0140', 23, 7): '11 X 1757',
    ('0140', 26, 7): '13 X 1765',
    ('0141', 39, 7): '20 XI 1729 20 I 1749',
    ('0141', 44, 7): '14 X 1735',
    ('0144', 84, 7): '3 VII 1760',
    ('0147', 13, 7): '28 VII 1776',
    ('0148', 17, 7): '1 IV 1781',
    ('0148', 27, 7): '11 XI 1735 20 X 1744',
    ('0151', 68, 7): '24 V 1737',
    ('0151', 69, 7): '9 VII 1701',
    ('0151', 72, 7): '3 III 1614 1 V 1677',
    ('0152', 83, 7): '11 XI 1723',
    ('0156', 136, 7): '1 XI 1751',
    # numeric cells (digit_read.py template matching against same-print
    # digit glyphs; correlations >=0.88 unless noted; raw-strip agreement
    # where the strip OCR caught the same value)
    ('0139', 4, 8): '5',
    ('0139', 5, 8): '5',
    ('0139', 8, 8): '51',        # '511' refuted by the a-series column
                                 # sum (2386); the third glyph is a
                                 # raised mark (SPOT)
    ('0143', 65, 10): '120',
    ('0143', 67, 10): '104',
    ('0143', 68, 8): '14',
    ('0143', 71, 8): '19',
    ('0145', 92, 8): '10',
    ('0149', 37, 8): '2',
    ('0153', 99, 8): '14',
    # dash cells the OCR had garbled into junk (pixel-verified dashes)
    ('0142', 54, 10): '—',
    ('0143', 62, 10): '—',
    ('0145', 95, 8): '—',
    ('0145', 96, 9): '—',
    ('0148', 28, 9): '—',
    ('0148', 31, 9): '—',
    ('0148', 33, 10): '—',
    ('0149', 45, 10): '—',
    ('0150', 60, 8): '—',
    ('0153', 94, 8): '—',
    # 0140 r28/r29 (Dymaczewskie Nowe/Stare): r29's band had swallowed
    # the sheet's note line; the row's cells re-read from the true band
    ('0140', 28, 8): '48',
    ('0140', 28, 10): '266',
    # r14: the cells' dashes are pixel-verified; the tall glyph beside
    # each dash (and the marks in dymyTp/ludn) are unresolved ->
    # SPOT (see notes.md); rok/char/zrodlo/data = '—'
    ('0140', 14, 4): '—',
    ('0140', 14, 5): '—',
    ('0140', 14, 6): '—',
    ('0140', 14, 7): '—',
    ('0140', 29, 1): 'Dymaczewskie Stare Ol.',
    ('0140', 29, 2): 'Łódź',
    ('0140', 29, 3): 'St. Dymaczewo',
    ('0140', 29, 4): '1751',
    ('0140', 29, 5): 'las',
    ('0140', 29, 6): 'Rel. Posn. nr 489, fol. 69',
    ('0140', 29, 7): '13 V 1751',
    # numeric-cell verifications (digit template matching + glyph art)
    ('0145', 88, 8): '22',       # '4' was a scale artifact; note's 'd. 22' agrees
    ('0145', 94, 10): '159',     # middle digit '5' (top-bar glyph), not '9'
    ('0150', 61, 8): '24',       # blob1 = '2' (arc top + base), blob2 = '4'
    # line_read batch 1 (correlations >= 0.88, digit-distinct)
    ('0140', 16, 8): '11',
    ('0140', 25, 10): '122',
    ('0142', 59, 10): '50',
    ('0143', 62, 9): '10',
    ('0143', 63, 8): '11',
    ('0143', 63, 10): '80',
    ('0143', 64, 8): '30',
    ('0143', 66, 8): '51',
    ('0143', 67, 8): '17',
    ('0143', 70, 8): '17',
    ('0143', 70, 10): '110',
    ('0143', 71, 10): '129',
    ('0143', 72, 9): '—',
    ('0143', 72, 10): '—',
    ('0145', 87, 9): '11',
    ('0145', 87, 10): '—',
    ('0142', 60, 8): '21',       # ludn 117 clean -> ratio 5.6 agrees
    ('0142', 61, 10): '41',
    ('0145', 88, 10): '159',     # d2's left stem (art) = '5', not '3'
    ('0140', 19, 10): '73',      # raw '73' position agrees; dymy 9 ok
    ('0145', 92, 10): '50',      # art: top-bar '5' (the matcher's 9-bias)
    # b-series batch (raws agree with the pixel reads; small type h~28-40)
    ('0147', 3, 8): '5',
    ('0147', 6, 10): '9',
    ('0147', 6, 7): '16 II 1753',
    ('0147', 8, 8): '5',
    ('0147', 8, 7): '1 XI 1751',
    ('0147', 9, 8): '31',
    ('0147', 9, 7): '2 IV 1746',
    ('0147', 9, 6): 'AW. B. 108',
    ('0149', 38, 8): '12',
    ('0150', 64, 8): '22',
    ('0153', 95, 8): '10',
    ('0153', 100, 8): '2',
    ('0145', 93, 8): '18',       # raw '18'; ludn 115 -> ratio 6.4
    ('0154', 107, 8): '39 *',    # raw '39 *'
    # audit_cells round: band-crop blob reads confirmed against raws
    # and body ratios; raised small marks after dymy values are
    # transcribed separately (see notes.md)
    ('0139', 3, 10): '87',       # was 7; 8@0.94+7@0.97; 87/17=5.1
    ('0142', 49, 8): '44',       # was 4; two 4s; 284/44=6.5
    ('0142', 59, 8): '13',       # was 3; 1@0.94+3@0.95
    ('0143', 72, 8): '9',        # raw '9'; bowl+tail glyph
    ('0143', 73, 10): '83',      # raw '83'
    ('0143', 73, 7): '17 V 1746',  # raw
    ('0145', 94, 8): '31',       # raw '31' (data 29 X 1738)
    ('0145', 94, 7): '29 X 1738',  # raw
    ('0145', 95, 7): '6 VIII 1724',  # raw
    ('0145', 98, 7): '5 VI 1712',  # raw
    ('0146', 102, 7): '21 X 1744',  # raw
    # dashes where the pixel bar is unambiguous
    ('0142', 51, 9): '—',
    ('0142', 60, 9): '—',
    ('0143', 62, 8): '—',
    ('0144', 81, 9): '—',
    ('0145', 87, 8): '—',
    ('0145', 95, 10): '—',
    ('0148', 19, 10): '—',
    ('0150', 57, 10): '—',
    ('0152', 90, 8): '—',
    ('0153', 93, 9): '—',
    ('0153', 100, 10): '—',
    ('0153', 101, 8): '—',
    ('0153', 102, 8): '6',       # raw '6'; 0/6 tie -> raw
    ('0154', 106, 9): '—',
    # tiebreak round: strip-raw + size-matched pixels + ratios
    ('0145', 90, 8): '45',       # raw '45'; 5@0.76 same-sheet ref
    ('0145', 90, 10): '282',     # raw '282'; 8@0.88+2@0.96; ratio 6.27
    ('0145', 91, 10): '36',      # raw '36' (strip reliable at this size)
    ('0145', 96, 8): '16',       # ratio 97/16 = 6.06 = body's 6.05!
    ('0145', 96, 10): '97',      # raw '16 97'
    ('0145', 97, 9): '22',       # SUM LAW: col10 total 92 = 70+22
    ('0145', 97, 10): '356',     # raw '356'; 3 glyphs in pixels
    ('0146', 102, 10): '206',    # raw '206' (draft 200; 6@0.88 2nd)
    ('0146', 111, 10): '226',    # 3 digit-blobs 2,2,6; draft 2206 glitch
    ('0149', 36, 8): '30',       # raw '30'; 3-reads-as-5 bias
    ('0149', 39, 8): '16',       # raw tail '5 XI 1744 16'; 1+6/0
    ('0149', 40, 8): '3',        # raw '3'; single glyph
    ('0149', 41, 8): '24',       # raw '24'; 2@0.92/4@0.86 tie -> raw
    ('0149', 42, 8): '36',       # raw '36'
    ('0149', 43, 7): '10 XII 1643',  # strip '10 XII 16 43' = split 1643
    ('0149', 43, 8): '—',        # pixel dash; strip's '16' was the year
    ('0149', 46, 10): '14',      # strip '— 14 —'; 1+4/2 pixels
    ('0150', 50, 8): '11',       # two narrow 1-glyphs
    ('0150', 58, 9): '—',        # pixel dash
    ('0150', 59, 8): '17',       # 1@0.92 + 7@0.95 narrow glyphs
    ('0152', 92, 9): '6',        # 6@0.95 full blob in obl cell
    ('0153', 97, 8): '38',       # raw '38'; 3-reads-as-5, 8@0.70
    ('0154', 106, 8): '16',      # raw 'dto 1749 16'; digits 1+6
    ('0154', 108, 8): '35',      # raw '35'; 3-reads-as-5 twice
    ('0154', 113, 8): '28',      # raw '21 XI 28'; 2@0.94+8@0.77
    ('0154', 114, 8): '16 *',    # raw '22 V 1775 16 *'; 1+6/0
    ('0154', 117, 8): '43',      # raw '43'; 4-reads-as-2, 3-as-5
    ('0157', 148, 8): '20',      # raw '20'; 2@0.91+0@0.89 agree
    ('0157', 149, 8): '16',      # raw '16'; 1@0.94+6/0@0.84
    ('0159', 11, 9): '—',        # pixel dash
    ('0149', 35, 8): '—',        # dash + weak mark; strip shows no dymy
    ('0149', 47, 8): '—',        # dash + smalls (strip: dashes)
    ('0150', 52, 8): '—',        # dash + weak mark
    ('0151', 67, 8): '28',       # 2@0.94+8@0.94; strip 'maj. 28!'
    # the print's '*' markers (body p. 23-24: dymy given 'zbiorowo' in
    # Tp. 89, estimated per Tp. 90) - star on the dymyTp value
    ('0139', 9, 8): '20 *',
    ('0140', 21, 8): '22 *',
    ('0140', 26, 8): '12 *',
    ('0141', 36, 8): '38 *',
    ('0142', 48, 8): '21 *',
    ('0142', 54, 8): '7 *',
    ('0144', 77, 8): '5 *',
    ('0144', 78, 8): '17 *',
    ('0147', 1, 8): '4 *',
    ('0147', 12, 8): '24 *',
    ('0148', 15, 8): '5 *',
    ('0148', 17, 8): '13 *',
    ('0148', 22, 8): '22 *',
    ('0148', 24, 8): '8 *',
    ('0149', 44, 8): '6 *',
    ('0149', 48, 8): '4 *',
    ('0150', 62, 8): '36 *',
    ('0151', 74, 8): '8 *',
    ('0151', 75, 8): '22 *',
    ('0151', 77, 8): '21 *',
    ('0151', 79, 8): '2 *',
    ('0152', 82, 8): '7 *',
    ('0152', 83, 8): '10 *',
    ('0152', 84, 8): '10 *',
    ('0152', 85, 8): '5 *',
    ('0152', 87, 8): '5 *',
    ('0152', 91, 8): '38 *',
    ('0153', 103, 8): '13 *',
    ('0155', 119, 8): '22 *',
    ('0155', 123, 8): '12 *',
    ('0155', 127, 8): '15 *',
    ('0158', 1, 8): '12 *',
    ('0159', 1, 8): '9 *',
    ('0159', 3, 8): '7 *',
}


def apply(amd):
    n_fixed = 0
    for (n, num, ci), txt in CELL_FIXES.items():
        for r in amd.get(n, {}).get('rows', []):
            if r['num'] == num:
                if ci >= len(r['cells']):
                    print('WARN: %s r%d c%d out of range (%d cells)'
                          % (n, num, ci, len(r['cells'])))
                    break
                if r['cells'][ci] != txt:
                    r['cells'][ci] = txt
                    n_fixed += 1
                break
    return n_fixed
