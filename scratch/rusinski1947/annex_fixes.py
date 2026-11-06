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
    # ---- date pass (datedec.txt per-blob decode; see notes.md) ----
    ('0140', 17, 7): '2 IV 1757',    # 2,I,V,1,7,5,7 blobs; strip
    ('0140', 22, 7): '25 III 1747',  # 2,5,III(3 narrow),1,7,4,7; strip '251111747'
    ('0141', 31, 7): '10 XI 1746',   # 1,0,X,I,1,7,4,6; strip '10 X11746'
    ('0142', 47, 7): '1 V 1781',     # 1,V,1,7,8,1; strip 'i V 1781'
    ('0142', 57, 7): '—',            # dash only
    ('0143', 65, 7): '—',
    ('0143', 65, 4): 'ok. 1762',     # draft 'ok. 1702' = 6->0 glitch; strip
    ('0143', 66, 7): '1 V 1713',     # 1,V,1,7,1,5(3-as-5); strip
    ('0143', 66, 8): '31',           # draft 51: 199/31=6.4 hits 6.05 law
    ('0143', 67, 7): '18 IV 1785',   # 8 blobs 1,8,I,V,1,7,8,5; strip '||8IV'=|+1+8
    ('0143', 68, 7): '—',
    ('0143', 69, 7): '11 XI 1729',   # strip '|11 XI1729|'; rok 1729
    ('0143', 71, 7): '18 VIII 1736', # 1,8,V,I,I,I + 1,7,3,0(6-as-0)
    ('0143', 72, 7): '—',
    ('0144', 80, 7): '29 X 1728',    # 2,9,X,1,7,2,8
    ('0145', 87, 7): '1742',         # 4 blobs 1,7,4,2 in data cell
    ('0145', 87, 6): 'DWZP nr 29, s. 211',  # draft 'nr ZY' glitch
    ('0145', 90, 7): '1712',         # 1,7,1,2(4-as-2); strip '1712'
    ('0146', 104, 7): '1 XI 1719',   # 1,X,I,1,7,1,9; strip
    ('0146', 107, 7): '15 III 1783', # 9 blobs incl. III; strip '15 HI'
    ('0147', 1, 7): '1781',          # bare year; strip 'AW. B. 1 1781'
    ('0147', 1, 6): 'AW. B. 1',      # b-sigla use digits
    ('0147', 2, 7): '29 IV 1748',    # 2,9,I,V,1,7,4,8
    ('0147', 2, 6): 'AW. B. 59—60',  # draft '99—6U' glitch
    ('0147', 3, 7): '1792',          # 4 blobs @1.00; strip
    ('0147', 7, 7): '—',
    ('0148', 19, 7): '1 XI 1751',    # 1,X,I,1,7,5,1
    ('0148', 25, 7): '1 V 1677',     # 1,V,1,6,7,7
    ('0149', 38, 7): '1746',         # 1,7,4,6 in data cell
    ('0149', 38, 4): '1746 (?)',     # draft 'L/40(*)' glitch
    ('0149', 39, 7): '5 XI 1744',    # 5,X,I,1,7,4,4 (2-as-4 ties)
    ('0149', 39, 4): '1744',         # draft '1/44' glitch
    ('0149', 40, 7): '—',
    ('0149', 42, 7): '2 II 1701',    # 2,I,I,1,7,0,1
    ('0149', 42, 4): '1701',         # draft 'L/UI' glitch
    ('0149', 45, 7): '—',
    ('0150', 50, 7): '—',
    ('0150', 52, 7): '—',
    ('0150', 55, 7): '—',
    ('0150', 56, 7): '30 X 1744',    # 3,0,X,1,7,4,4(merged); strip '30TX'
    ('0150', 57, 7): '—',
    ('0150', 58, 7): '3 XI 1730',    # 3,X,I,1,7,3,0; strip 'X1T1730'
    ('0150', 59, 7): '—',
    ('0150', 60, 7): '8 XII 1742',   # l1 '8 XII' + l2 '1742'
    ('0150', 62, 7): '2 II 1732',    # 2,I,I,1,7,3,2; rok 1732
    ('0150', 64, 7): '—',
    ('0151', 71, 7): '26 I 1701',    # blob2 = true-6 signature (6@.95/0@.63); strip '26'
    ('0154', 106, 7): '1749',        # 1,7,4,9; strip 'dto 1749'
    ('0154', 107, 7): '1744',        # 1,7,4,4 (2-as-4); strip '1744'
    ('0154', 108, 7): '1 XI 1751',   # 1,X,I,1,7,5,1; strip '1 XT 1751'
    ('0154', 112, 7): '1 I 1624',    # 1,I,1,6,2,4; strip
    ('0155', 121, 7): '1 I 1707',    # 1,I,1,7,0,7
    ('0155', 128, 7): '1 V 1753',    # 1,V,1,7,5,3
    ('0156', 140, 7): '10 XI 1718',  # 4 narrow + 4 wide; l1 '10 XI' l2 '1718'
    ('0157', 148, 7): '4 VI 1771',   # 4,V,I,1,7,7,1; strip
    ('0157', 152, 7): '1704',        # 1,7,0,4 (2-as-4); strip second 1704
    ('0159', 4, 7): '—',
    ('0159', 11, 7): '4 III 1754',   # 4,I,I,I,1,7,[54 merged]
    # xz max-zoom round decisions
    ('0142', 49, 7): '7 VII 1754',   # 7,V,I,I,1,7,5,4; strip 'TVII 1754'
    ('0151', 77, 7): '21 I 1713',    # 7 blobs = 2,1,I,1,7,1,3; strip '21I11713'
    ('0153', 95, 7): '4 X 1723',     # true-4 signature; strip '4 TX 1723'
    ('0153', 103, 7): '1 IV 1708',   # 1,I,V,1,7,0,8; strip '1 IV1708'
    ('0157', 156, 7): '—',           # strip: no date; band glue artifacts
    # date pass batch 2 (datedec + strip + xz max-zoom)
    ('0141', 42, 7): '17 XI 1772',   # 1,7,X,I,1,7,7,2; strip '17Xrt772'
    ('0143', 70, 7): '27 VII 1729',  # strip '27 VII 17'; 110 = ludn
    ('0144', 76, 7): '12 11 1781',   # 8 glyphs @1.00; print's numeric style
    ('0144', 77, 7): '27 VII 1729',  # strip '27 VII'
    ('0145', 88, 7): '1 III 1743',   # 8 glyphs: 1,III,1,7,4,3; strip
    ('0145', 89, 7): '—',            # strip: no date
    ('0145', 91, 7): '—',            # strip: no date
    ('0145', 92, 7): '20 II 1742',   # 2,0,I,I,1,7,4,2; strip
    ('0145', 93, 7): '—',            # strip: no date
    ('0145', 97, 7): '—',            # strip: no date
    ('0146', 110, 7): '—',           # strip: no date
    ('0146', 111, 7): '—',           # rok 1778 only; strip
    ('0147', 10, 7): '18 IV 1692 1 XI 1751',  # strip '18 IV 1692'+'1 XT 1751'
    ('0147', 12, 7): '2 III 1732 11 XI 1740',  # strip '2 III 1732'/'11 XT1740'
    ('0149', 34, 7): '3 XI 1730',    # strip 'AW. C. 3 | 3 XT 1730'
    ('0149', 35, 7): '—',            # strip: no date (Huta row)
    ('0149', 37, 7): '—',            # strip: no date
    ('0149', 41, 7): '20 IV 1735',   # strip '20 TV'; rok 1735
    ('0149', 46, 7): '28 III 1748',  # strip '28 III ... 1748'
    ('0149', 47, 7): '26 IV 1714',   # strip '26 IV 17|1714'; 6@0.91
    ('0150', 51, 7): '8 I 1746',     # strip '8 I 1746'
    ('0150', 54, 7): '18 XI 1772',   # strip '18 XI ... 1772'
    ('0150', 61, 7): '—',            # Lasek: no date in strip
    ('0150', 65, 7): '10 XI 1773',   # strip '10111773'
    ('0150', 66, 7): '6 V 1736',     # strip '6 V 1736'
    ('0151', 67, 7): '16 IV 1764',   # 1,6,I,V,1,7,6,4
    ('0151', 70, 7): '14 IV 1763 i 1782',  # strip '14IV1763'/'i 1782'
    ('0152', 90, 7): '21 II 1601 i 1 V 1677',  # strip
    ('0153', 94, 7): '—',            # strip: no date
    ('0153', 96, 7): '11 XI 1701',   # strip '11 XI'; rok 1701
    ('0153', 97, 7): '—',            # strip: no date
    ('0153', 98, 7): '20 V 1730',    # strip '20 V 1730'
    ('0153', 101, 7): '—',           # strip: no date
    ('0154', 117, 7): '—',           # strip: no date
    ('0155', 132, 7): '2 II 1720 12 X 1720',  # strip '2 11 1720'/'12 X 1720'
    ('0156', 138, 7): '16 IV 1597; 20 I 1637; 4 I 1701 i 1763',  # strip
    ('0156', 145, 7): '11 XI 1721',  # strip 'M XI ... 1721' = 11 XI
    ('0157', 146, 7): '—',           # Wyssogotowo: no date (r147 glue)
    ('0157', 147, 7): '11 XI 1747',  # strip '11 XI ... 1747'
    ('0157', 149, 7): '1 XI 1751',   # strip 'I X1 1751'
    ('0157', 151, 7): '—',           # Zdroje: no date
    ('0157', 154, 7): '26 III 1752',  # strip '26 III'; 9 blobs = 2,6,III,1752
    ('0158', 2, 7): '2 XI 1743',     # strip '2 XI1743'
    ('0158', 3, 7): '20 XII 1697',   # strip '20 XII'; rok 1697
    ('0158', 4, 7): '11 X 1727',     # strip '11 X 1727'
    ('0158', 7, 7): '8 V 1697',      # strip '8 V 1697'
    ('0158', 8, 7): '11 XI 1781',    # strip '11 XI ... 1781'
    ('0159', 10, 7): '15 IV 1755',   # strip '15 IV ... 1755'
    # ---- date pass batch 3: 0154 glue cluster (top-alignment law:
    # row content prints at the band TOP edge) + rok-column repairs ----
    ('0145', 96, 4): '1745',         # 1,7,4,5 matcher; strip 'r. 1756' = repert. year
    ('0145', 96, 7): '1 I 1750',     # 6 small glyphs 1,I,1,7,5,0 (I=w21 tpl match)
    ('0150', 63, 4): '1783',         # strip 'AW. Paproć, 1783 C. 2'
    ('0150', 63, 7): '1783',         # 4 digits + faint mark
    ('0152', 88, 7): '18 VII 1661; 29 II 1672; 23 II 1691; XII 1700 i 1 III 1701',
        # 5 print lines decoded from blob rows; 29 II valid (1672 leap);
        # strip '81 II!' = 2-as-8 + 9-as-1; w51 blobs = merged 69 / 00
    ('0153', 102, 7): '—',           # digits = źródło overflow '10820, 1766'
    ('0154', 108, 4): '1700',        # 1,7,0,0 matcher (data 1 XI 1751)
    ('0154', 110, 7): '20 III 1777', # two lines y1621/y1693 (72px line pitch)
    ('0154', 110, 8): '13 *',        # same print line as data l1; strip
    ('0154', 111, 4): '—',           # cross-ref row: c4/c7/c8 empty
    ('0154', 111, 7): '—',           # strip '1777' = r110 data l2 crossed
    ('0154', 111, 8): '—',
    ('0154', 112, 4): '1624',        # 1,6,2,4 matcher; strip 'Poręba 1624'
    ('0154', 113, 4): '1705',        # 1,7,0@0.97,5; strip '1765' = 0-as-6 OCR
    ('0154', 113, 7): '21 XI 1767',  # l1 2,1,X@0.90,I; l2 1,7,6,7; strip
    ('0154', 114, 4): '1775',        # 1,7,7,5; strip 'Rudka pod 1775'
    ('0154', 114, 7): '22 V 1775',   # 2,2,V,1,7,7,5 matcher
    ('0154', 115, 4): '—',           # c4 empty y2531-2630; strip no rok
    ('0154', 115, 7): '—',           # tiny glue marks only
    ('0154', 116, 4): '1700',        # 1,7-as-1,0,0; strip '1700 i fol. 53'
    ('0154', 116, 7): '11 XI 1700',  # l1 1,1,X,I; l2 1,7,0,0
    ('0154', 118, 7): '24 XI 1791',  # l1 2,4,X,I; l2 1791 (9 faint desc.); strip
    ('0157', 148, 4): '1771',        # strip 'Zamorze 1771'
    ('0157', 149, 4): '1751',        # strip 'Zatom Nowy 1751'
    ('0157', 150, 4): '1745',        # l2 1,7,4,5 matcher; strip '1745'
    ('0157', 150, 7): '25 VI 1745',  # l1 2,5(5->9 bias),V+I; l2 1745
    ('0157', 151, 4): '—',           # strip dashes (Zdroje)
    ('0157', 152, 4): '1704',        # strip 'Przyłęk 1704'
    ('0157', 152, 8): '48',          # 4,8 blobs at r152's line; strip '1704 48'
    ('0157', 154, 4): '1751',        # strip 'Złotkowo 1751'; data year 1752
    ('0157', 156, 4): '—',           # strip dashes (Zwierzyniec)
    ('0158', 1, 4): '1747',          # strip 'Głuszyna 1747'
    ('0158', 1, 7): '1747',          # full-size 1,7,4,7; smalls = glue
    ('0158', 2, 4): '1743',          # strip 'Głębocko 1743'
    ('0158', 3, 4): '1697',          # data 20 XII 1697
    ('0158', 4, 4): '1727',          # strip 'Kruteczck 1727'
    ('0158', 5, 4): '1786',
    ('0158', 5, 7): '10 XI 1786',    # strip; '1786' full-size line
    ('0158', 6, 4): '1750',
    ('0158', 6, 7): '1 VI 1750',     # strip r5 tail '1 VI11750'
    ('0158', 7, 4): '1697',          # strip 'Rzecień 1697'
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
