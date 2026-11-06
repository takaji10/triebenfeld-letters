# -*- coding: utf-8 -*-
"""ANEKS I row rebuild, v10 - final.

PHASE 1 (per sheet): boundaries + provisional count numbering.
  starts: number lines (NUMHINT, left<1300, not totals, hint=digit) +
  name-column candidates (1085<=left<=1135, gap>=55, not blocklisted)
  + editor-line repairs; everything ABOVE the sheet's totals row only.
  Hint-chain validation: a chain-breaking number line is a false
  positive (small gap + no editor mark + cell disagreement -> drop),
  a misread (number cell arbitrates -> corrected), or a NOTE (hint far
  below the expectation -> dropped, its top becomes a text CUT so the
  note's lines stay out of the last row).
  Pre-first-hint alignment: rows before the sheet's first hinted row
  number exactly H - prev - 1 (excess hintless starts = header debris,
  junkiest dropped; shortfall = missing rows, reported).

PHASE 2 (cross-sheet): tail reconciliation - when sheet N+1's first
hint H < prev+1, the excess hintless TAIL rows of sheet N are phantoms
and are dropped (renumbering N); when H == prev+1 all is well; when H
> prev+1 a row is missing (reported).

PHASE 3: a missing boundary inside a band (hint == counted+1) is
rescued by splitting at a line in that band matching the expected
number (or a name-column candidate); else reported.

Numbering is COUNT within the series (a: 0139-0146, b: 0147-0157,
c: 0158-0159; each from 1 in the print); the hints VALIDATE and the
disagreements are REPORTED as print anomalies / misreads (the count
reproduces the print's defects faithfully, e.g. the doubled 103).

Output: annex_rows3.json + annex_table.json (compose format, tier C,
raw, the row's own number stripped; unnumbered rows 'u<i>')."""
import json, os, io, re, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image, ImageOps

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
TMP = os.path.join(OCR, 'row_tmp.png')
SHEETS = ['%04d' % i for i in range(139, 160)]
SERIES = {'0139': 'a', '0147': 'b', '0158': 'c'}
# explicit start lists for the stubborn sheets, from the eyeball pass:
# scan -> [(line_top, hint or None)] (replaces the computed starts;
# override hints are eyeball-verified print readings)
OVERRIDES = {
    # series a continuation (p. 129): rows 74-86. The number column's
    # misreads ('99814 14'=74, '17'=77, "'Pis[og 78"=78) and the
    # 1955-2410 rescue band (rows 83 Słocińskie / 84 Snowidowo, whose
    # separator the editor's lines miss) fixed by explicit starts from
    # the print
    '0144': [(364, 74), (544, 75), (656, 76), (906, 77), (1107, 78),
             (1408, 79), (1506, 80), (1759, 81), (1863, 82), (1967, 83),
             (2072, 84), (2313, 85), (2418, 86)],
    # series b continuation (p. 137): rows 82-92. Row 85 'Niewiemko
    # Stare' (the 'ee)' misread; the old 84 span held both Niewiemko
    # rows) and row 90 'Nowe Dwory' recovered
    '0152': [(379, 82), (699, 83), (805, 84), (913, 85), (1236, 86),
             (1408, 87), (1655, 88), (2044, 89), (2149, 90), (2390, 91),
             (2496, 92)],
    # series b continuation (p. 139): rows 105-118. Rows 113
    # Różyńskie / 114 Rudka / 115 Sąpolna recovered (the old 114 was a
    # 4px sliver and 113 held row 112's tail)
    '0154': [(419, 105), (816, 106), (924, 107), (1262, 108), (1438, 109),
             (1545, 110), (1652, 111), (1827, 112), (2084, 113),
             (2279, 114), (2543, 115), (2650, 116), (2909, 117),
             (3014, 118)],
    # series b continuation (p. 141): rows 133-145. Row 142 'Wizany'
    # (the 'N 42' misread) recovered - the old 142 held row 141's
    # Wiewiórczyn content
    '0156': [(379, 133), (560, 134), (667, 135), (844, 136), (1023, 137),
             (1130, 138), (1534, 139), (1709, 140), (1955, 141),
             (2110, 142), (2391, 143), (2497, 144), (2759, 145)],
    # series c: the 'Osady typu przejściowego' table (rows 1-9) then its
    # notes 1-8 (excluded by the cut at 2350)
    '0158': [(527, 1), (703, 2), (902, 3), (1096, 4), (1290, 5),
             (1494, 6), (1666, 7), (1909, 8), (2082, 9)],
    # the table's continuation (10-11), the 4-row sub-table (1-4),
    # then the sub-table's notes (excluded)
    '0159': [(1339, 10), (1496, 11), (1660, 'T'), (1810, 'H'),
             (1917, 1), (2024, 2), (2124, 3), (2250, 4)],
}
# a text cut per sheet: row texts stop above it (the notes zone)
CUTS = {'0158': 2350, '0159': 2600,
        # the sheet footnotes leaked into the last row's span
        '0144': 2553, '0152': 2630, '0156': 3049}
# start-list patches for the digit-audit findings (the print's own
# number-column digits arbitrate): 'drop_y' = a pseudo-row (the table
# header filed as a row), 'insert_before_y' = a row the lineation
# start detectors missed, 'append_row' = a swallowed last row
PATCHES = {
    # p. 123: the header span [1178,1538] is print furniture; the
    # print's row 1 = Albertowskie (line 1546, digit band verified)
    '0139': [('drop_y', 1190), ('insert_before_y', 1653, 1546)],
    # p. 127: the last slot swallowed print row 61 (Nowawieś, line
    # 2968; digit bands 2864-2916='60' / 2970-3020='61')
    '0142': [('append_row', 2968)],
    # p. 131: the sheet opens with the repeated table header (the
    # print's rows here are 62-73; row 61 sits on 0142)
    '0143': [('drop_y', 1057)],
    # p. 132: the header span [1074,1436] + the missed row 2
    # Białężyńskie (line 1622; print digits Barcinek=1, Białężyńskie=2,
    # Białokoskie=3 ... Chmielinka=13, Chorzępowa=14 on 0148)
    '0147': [('drop_y', 1086), ('insert_before_y', 1728, 1622)],
}

NUMHINT = re.compile(r'^[lI|]?\s*(\d{1,3})[.)]?\s+\S')
TOTALS = re.compile(r'^(Razem|Uwagi|Wszelkie|Og[oó]łem|W tym)\b')
BLOCK = re.compile(
    r'^(Nazwa|Charakter|Przywilej|Rok|parafia|dzisiejsza|rozbior[oó]w|'
    r'L\.|w\s|W\s|Tp\.|sygn\.|osady|Dymy|Okres|Grunt|Ludn\.|ANEKS)',
    re.UNICODE)
rowlines = json.load(open(os.path.join(OCR, 'rowlines.json'),
                          encoding='utf-8'))
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                   encoding='utf-8'))
imgs = {}


def img(n):
    if n not in imgs:
        with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
            imgs[n] = Image.open(io.BytesIO(fh.read())).convert('L')
        imgs[n].load()
    return imgs[n]


def cell_cands(n, top):
    out = []
    for (x0, x1, sc, ac) in ((860, 1140, 5, False), (840, 1160, 6, False),
                             (860, 1140, 7, True)):
        c = img(n).crop((x0, max(0, top - 8), x1, top + 68))
        c = c.resize((c.size[0] * sc, c.size[1] * sc), Image.LANCZOS)
        if ac:
            c = ImageOps.autocontrast(c)
        c.save(TMP)
        for lang in ('pol', 'pol-std'):
            try:
                tt = read(TMP, lang=lang, psm=7).strip()
            except Exception:
                continue
            for m in re.finditer(r'\d{1,3}', tt):
                v = int(m.group(0))
                if 1 <= v <= 200 and v not in out:
                    out.append(v)
    return out


def junkness(text):
    return len(re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{4,}', text))


residuals = []
all_rows = {}
state = {'prev': 0}
for n in SHEETS:
    lines = sorted(s[n]['lines'], key=lambda l: l['top'])
    els = rowlines.get(n, [])
    tops = [l['top'] for l in lines]

    def prev_top(t):
        below = [x for x in tops if x < t - 15]
        return below[-1] if below else None

    if SERIES.get(n):
        state['prev'] = 0
    tot_top = next((l['top'] for l in lines if TOTALS.match(l['text'])),
                   10 ** 9)
    # the sheet's own number/name separator: the first sustained
    # vertical rule in x [900, 1400] over the table's y-range
    im_l = img(n)
    W, H = im_l.size
    pxl = im_l.load()
    yA = min(t for t in tops if t > 300) if tops else 300
    yB = tot_top if tot_top < 10 ** 9 else H - 60
    rx = None
    for x in range(900, 1400):
        vals = [pxl[x, y] for y in range(yA, max(yA + 1, yB), 6)]
        if sum(1 for v in vals if v < 140) / len(vals) > 0.5:
            rx = x
            break
    lo_w = (rx + 35) if rx else 1085
    hi_w = (rx + 95) if rx else 1135
    starts, cuts = [], set()
    for l in lines:
        if l['top'] >= tot_top:
            continue
        m = NUMHINT.match(l['text'])
        if m and (l.get('left') or 10 ** 9) < 1300:
            starts.append({'top': l['top'], 'hint': int(m.group(1)),
                           'src': 'line'})
    for l in lines:
        if l['top'] >= tot_top:
            continue
        left = l.get('left') or 10 ** 9
        if not (lo_w <= left <= hi_w):
            continue
        if NUMHINT.match(l['text']) or BLOCK.match(l['text']) \
                or TOTALS.match(l['text']):
            continue
        if not (l['text'][:1].isupper() or l['text'][:1] in '|„"'):
            continue  # a row's name cell starts capitalized; notes do not
        pt = prev_top(l['top'])
        gap = l['top'] - pt if pt else 10 ** 9
        if gap < 55:
            continue
        if any(abs(st['top'] - l['top']) <= 60 for st in starts):
            continue
        starts.append({'top': l['top'], 'hint': None, 'src': 'name'})
    for el in els:
        if el >= tot_top or any(abs(st['top'] - el) <= 90 for st in starts):
            continue
        below = [l for l in lines
                 if el - 25 <= l['top'] <= el + 60]
        pref = [l for l in below if (l.get('left') or 10 ** 9) < 1300]
        fall = [l for l in below
                if (l.get('left') or 10 ** 9) < 3200
                and junkness(l['text']) >= 2]
        cand = (pref or fall or [None])[0]
        if cand is None:
            continue
        if any(abs(st['top'] - cand['top']) <= 60 for st in starts):
            continue
        starts.append({'top': cand['top'], 'hint': None, 'src': 'editor?'})
    starts.sort(key=lambda x: x['top'])
    ded = []
    for st in starts:
        if ded and abs(st['top'] - ded[-1]['top']) <= 60:
            continue
        ded.append(st)
    starts = ded
    if n in OVERRIDES:
        starts = [{'top': t, 'hint': h, 'src': 'override'}
                  for (t, h) in OVERRIDES[n]]
    for op in PATCHES.get(n, []):
        if op[0] == 'drop_y':
            starts = [st for st in starts if st['top'] != op[1]]
        elif op[0] == 'insert_before_y':
            i = next((j for j, st in enumerate(starts)
                      if st['top'] == op[1]), len(starts))
            starts.insert(i, {'top': op[2], 'hint': None,
                              'src': 'patch'})
        elif op[0] == 'append_row':
            starts.append({'top': op[1], 'hint': None, 'src': 'patch'})
    l_text_by_top = {l['top']: l['text'] for l in lines}
    # hint-chain validation (false lines dropped, misreads corrected,
    # notes dropped with a text cut)
    clean = []
    exp_hint = None
    for st in starts:
        if st['src'] == 'line':
            h = st['hint']
            if exp_hint is not None and h != exp_hint:
                pt = prev_top(st['top'])
                small_gap = pt is not None and st['top'] - pt < 45
                no_editor = not any(abs(el - st['top']) <= 90 for el in els)
                v = cell_cands(n, st['top'])
                if exp_hint in v:
                    st['hint'] = h = exp_hint  # line misread, cell confirms
                else:
                    vc = min(v, key=lambda x: abs(x - exp_hint)) if v \
                        else None
                    if vc is not None and vc != h \
                            and abs(vc - exp_hint) <= 12:
                        st['hint'] = h = vc  # the cell read outranks
                    elif h < exp_hint - 3:
                        # note or row? notes are full-width prose: the
                        # 2nd token lowercase, a lowercase start, or a
                        # totals word; rows carry names
                        after = re.sub(
                            r'^[lI|]?\s*\d{1,3}[.)]?\s*', '',
                            l_text_by_top.get(st['top'], '')).strip()
                        tk = after.split()
                        if not after or after[:1].islower() \
                                or TOTALS.match(after) \
                                or (len(tk) >= 2 and tk[1][:1].islower()):
                            cuts.add(st['top'])  # a note's number
                            continue
                        # else: a misread row number - keep, rebase
                    elif small_gap and no_editor:
                        continue  # false number line
            exp_hint = h + 1 if h is not None else None
        clean.append(st)
    starts = clean
    rows = []
    for i, st in enumerate(starts):
        y0 = max(0, st['top'] - 12)
        y1 = starts[i + 1]['top'] - 8 if i + 1 < len(starts) \
            else (tot_top if tot_top < 10 ** 9 else s[n]['height'] - 30)
        # the notes zone: the sheet's footnotes must not widen the
        # table's last row
        if n in CUTS and y0 < CUTS[n] < y1:
            y1 = CUTS[n]
        ytext = min([y1] + [t - 8 for t in cuts if y0 < t < y1]
                    + ([CUTS[n]] if n in CUTS and y0 < CUTS[n] < y1 else []))
        text = ' '.join(l['text'] for l in lines
                        if y0 <= l['top'] < ytext)
        flat = re.sub(r'\s+', ' ', text).strip()
        rows.append({'hint': st['hint'], 'y0': y0, 'y1': y1, 'ytext': ytext,
                     'src': st['src'], 'text': flat,
                     'totals': bool(TOTALS.match(flat))})
    # empty/junk phantom rows (sliver starts): drop
    rows = [r for r in rows
            if r['totals'] or junkness(r['text']) >= 1
            or len(r['text']) >= 15]

    def renumber(rws, p0):
        p = p0
        for r in rws:
            if r['totals']:
                r['num'], r['how'] = None, 'totals'
                continue
            p += 1
            r['num'], r['how'] = p, 'count'

    p0 = state['prev']
    renumber(rows, p0)
    if n not in OVERRIDES:
        # pre-first-hint alignment
        fh_i = next((i for i, r in enumerate(rows) if r['hint'] is not None),
                    None)
        if fh_i is not None:
            H = rows[fh_i]['hint']
            want = H - state['prev'] - 1
            before = [i for i in range(fh_i) if rows[i]['hint'] is None]
            if len(before) > want:
                excess = min(len(before) - want, len(before))
                order = sorted(before, key=lambda i: junkness(rows[i]['text']))
                drop = {order[i] for i in range(excess)}
                rows = [r for i, r in enumerate(rows) if i not in drop]
                renumber(rows, p0)
            elif len(before) < want:
                residuals.append((n, 'MISSING %d row(s) before the first '
                                  'hinted row (hint %d, prev %d)'
                                  % (want - len(before), H, state['prev'])))
        # targeted dispute loop: drain all phantom-drops first
        for _ in range(15):
            disp = [(i, r['num'], r['hint']) for i, r in enumerate(rows)
                    if r['hint'] is not None and r['num'] is not None
                    and r['hint'] != r['num']]
            if not disp:
                break
            acted = False
            for (i, counted, hint) in disp:
                if hint == counted - 1 and i > 0:
                    del rows[i - 1]
                    renumber(rows, p0)
                    acted = True
                    break
            if acted:
                continue
            i, counted, hint = disp[0]
            if hint < counted:
                k = counted - hint
                seen_hints = set()
                before = []
                for j in range(i):
                    hj = rows[j]['hint']
                    if hj is None or hj in seen_hints:
                        before.append(j)  # hintless or duplicate-hinted
                    else:
                        seen_hints.add(hj)
                if len(before) >= k:
                    for j in sorted(before[-k:], reverse=True):
                        del rows[j]
                    renumber(rows, p0)
                    continue
                residuals.append((n, 'hint %d at counted %d: %d row(s) '
                                  'missing/unresolvable before it: %s'
                                  % (hint, counted, k, rows[i]['text'][:40])))
                break
            if hint == counted + 1:
                # missing boundary inside the previous band: rescue
                j = i - 1
                band_lines = [l for l in lines
                              if rows[j]['y0'] < l['top'] < rows[j]['y1']]
                split = None
                for want_v in (hint - 1, hint - 2, hint - 3):
                    for l in band_lines:
                        m = NUMHINT.match(l['text'])
                        if m and int(m.group(1)) == want_v:
                            split = l['top']
                            break
                    if split is not None:
                        break
                if split is None:
                    # the most row-start-like line in the band: the
                    # largest gap above (a lost row's start line)
                    best = None
                    for l in band_lines[1:]:
                        pt = max((x['top'] for x in band_lines
                                  if x['top'] < l['top'] - 15),
                                 default=None)
                        g = l['top'] - pt if pt else 0
                        if best is None or g > best[0]:
                            best = (g, l['top'])
                    if best and best[0] >= 50:
                        split = best[1]
                if split is None:
                    # the editor's own lines inside the band are split
                    # points (the lineation missed the row's start line)
                    inner = [el for el in els
                             if rows[j]['y0'] + 30 < el < rows[j]['y1'] - 20
                             and abs(el - rows[j]['y0']) > 40
                             and abs(el - rows[j]['y1']) > 40]
                    split = min(inner, key=lambda e: abs(e - (
                        rows[j]['y0'] + rows[j]['y1']) / 2)) if inner else None
                if split is None:
                    cand = [l for l in band_lines
                            if 1085 <= (l.get('left') or 0) <= 1135
                            and not BLOCK.match(l['text'])]
                    split = cand[0]['top'] if cand else None
                if split is not None:
                    old_y1 = rows[j]['y1']
                    rows[j]['y1'] = split - 8
                    rows[j]['text'] = re.sub(
                        r'\s+', ' ',
                        ' '.join(l['text'] for l in lines
                                 if rows[j]['y0'] <= l['top']
                                 < min(rows[j]['y1'], rows[j]['ytext']))).strip()
                    rows.insert(i, {'hint': hint, 'y0': split - 12,
                                    'y1': old_y1, 'ytext': old_y1,
                                    'src': 'rescue', 'text': '',
                                    'totals': False})
                    nr = rows[i]
                    nr['text'] = re.sub(
                        r'\s+', ' ',
                        ' '.join(l['text'] for l in lines
                                 if nr['y0'] <= l['top'] < nr['ytext'])).strip()
                    nr['totals'] = bool(TOTALS.match(nr['text']))
                    renumber(rows, p0)
                    continue
                residuals.append((n, 'MISSING row before counted %d '
                                  '(hint %d) - no rescue line'
                                  % (counted, hint)))
                break
            residuals.append((n, 'hint misread at counted %d (hint %d): %s'
                              % (counted, hint, rows[i]['text'][:44])))
    if n in OVERRIDES:
        p = p0
        for r in rows:
            if r['src'] == 'override' and isinstance(r['hint'], str):
                # 'T' = the series totals row, 'H' = a section title:
                # print furniture, unnumbered
                r['num'], r['how'] = None, 'furniture'
                continue
            if r['num'] is None:
                continue
            if r['src'] == 'override' and r['hint'] is not None:
                p = r['hint']
                r['num'] = r['hint']
            else:
                p += 1
                r['num'] = p
    # systematic-shift fix: when the hint disputes share a constant
    # offset (hint = count - d, d >= 3 disputes), the boundary set has
    # d undroppable phantoms - shift the whole sheet's numbering by -d
    disp = [(r['num'], r['hint']) for r in rows
            if r['hint'] is not None and r['num'] is not None
            and r['hint'] != r['num']]
    if len(disp) >= 3 and n not in OVERRIDES:
        from collections import Counter
        offs = Counter(h - c for (c, h) in disp)
        off, n_off = offs.most_common(1)[0]
        if n_off >= 3 and off < 0:
            for r in rows:
                if r['num'] is not None:
                    r['num'] += off
            residuals.append((n, 'systematic shift %+d applied '
                              '(%d/%d disputes)' % (off, n_off, len(disp))))
    state['prev'] = p0 + sum(1 for r in rows if r['num'])
    # merged-lineation repair: a band whose text embeds the NEXT row's
    # number ('…dto 1749 16 106 Psarskie…') means the lineation merged
    # the wrap with the next row's start line - move the boundary to
    # that line's top (the merged line belongs to the next row)
    for i in range(len(rows) - 1):
        m = re.search(r'(?:^|[\s|])(\d{1,3})\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)',
                      rows[i]['text'])
        if not m:
            continue
        v = int(m.group(1))
        exp = rows[i]['num'] + 1 if rows[i]['num'] else None
        if exp and v >= exp and rows[i + 1]['hint'] in (None, v):
            # find the line carrying the embedded number
            for l in lines:
                if rows[i]['y0'] < l['top'] < rows[i]['y1'] and \
                        re.search(r'(?:^|[\s|])%d\s+[A-ZĄĆĘŁŃÓŚŹŻ]' % v,
                                  l['text']):
                    rows[i]['y1'] = l['top'] - 8
                    rows[i + 1]['y0'] = l['top'] - 12
                    rows[i + 1]['text'] = re.sub(
                        r'\s+', ' ',
                        ' '.join(ll['text'] for ll in lines
                                 if rows[i + 1]['y0'] <= ll['top']
                                 < rows[i + 1]['ytext'])).strip()
                    break
    all_rows[n] = rows
    print('%s: %2d rows, count ends %s' %
          (n, len(rows),
           [r['num'] for r in rows if r['num']][-1:]
           if any(r['num'] for r in rows) else '-'))

# PHASE 2: cross-sheet tail reconciliation
for i in range(len(SHEETS) - 1):
    n, nxt = SHEETS[i], SHEETS[i + 1]
    rows_n = all_rows[n]
    numbered = [r for r in rows_n if r['num']]
    if not numbered:
        continue
    prev_last = numbered[-1]['num']
    first_hint = next((r['hint'] for r in all_rows[nxt]
                       if r['hint'] is not None), None)
    if first_hint is None or first_hint == prev_last + 1:
        continue
    if nxt in SERIES:
        continue  # a series restart: the count reset is expected
    if all_rows[nxt] and all_rows[nxt][0]['hint'] is None:
        continue  # the next sheet's first row is hintless: cannot judge
    if first_hint <= prev_last:
        # droppable tail = the rows after the sheet's last HINTED row
        # (rescue/editor/name phantoms there inflate the count)
        li = max((j for j, r in enumerate(rows_n) if r['hint'] is not None
                  and r['src'] != 'rescue'), default=-1)
        excess = prev_last - first_hint + 1
        tail = list(range(li + 1, len(rows_n)))
        drop = tail[-excess:] if len(tail) >= excess else tail
        for j in sorted(drop, reverse=True):
            del rows_n[j]
        p0 = numbered[0]['num'] - 1
        p = p0
        for r in rows_n:
            if r['num'] is None:
                continue
            p += 1
            r['num'] = p
        residuals.append((n, 'tail trimmed by %d (next sheet hints %d, '
                          'counted ended %d)' %
                          (len(drop), first_hint, prev_last)))
    else:
        residuals.append((n, 'sheet %s starts at hint %d but the count '
                          'ended at %d - a row may be missing'
                          % (nxt, first_hint, prev_last)))

# PHASE 3: build the tables
table = {}
for n in SHEETS:
    sheet = {}
    u = 0
    for r in all_rows[n]:
        text = re.sub(r'^[lI|]?\s*\d{1,3}[.)]?\s*', '', r['text']).strip()
        key = str(r['num']) if r['num'] else 'u%d' % u
        if not r['num']:
            u += 1
        sheet[key] = {'tier': 'C', 'cells': [], 'raw': text,
                      'y': [r['y0'], r['y1']], 'how': r['how'],
                      'hint': r['hint']}
    table[n] = sheet

print()
print('== residuals ==')
for n, msg in residuals:
    print('   %s: %s' % (n, msg))
json.dump(all_rows, open(os.path.join(OCR, 'annex_rows3.json'), 'w',
                         encoding='utf-8', newline='\n'), ensure_ascii=False)
json.dump({n: {'rows': table[n]} for n in SHEETS},
          open(os.path.join(OCR, 'annex_table.json'), 'w',
               encoding='utf-8', newline='\n'), ensure_ascii=False)
print('annex_table.json rewritten (v10)')
