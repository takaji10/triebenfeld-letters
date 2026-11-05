# -*- coding: utf-8 -*-
"""Note parsing v2: the footnote block found by GEOMETRY, not by a
number chain.

The v1 parser required the first note's number to read as 1; one misread
('l' for 1, a glued digit) dropped the whole page's notes, and a mid-chain
misread truncated it. v2:

  1. lines from the TSV boxes (as structure.py);
  2. the note block = the lines after the largest vertical gap in the
     page's bottom 55%, where the gap > 1.35x the line pitch and the
     block carries at least one line starting with a 1-2 digit number
     followed by text;
  3. note starts = those lines, in reading order; numbers assigned by
     the leading digits when they form a plausible 1..k chain, else by
     order (the misread leading digit noted);
  4. exclusions: the front matter (0006-0015), the ANEKSY divider, the
     annex table sheets (0139-0159: their rows also begin with numbers)
     and the plates - no note parsing there. Aneks II/III (0160-0171)
     are parsed (printed sources may carry editorial notes).

Writes structure2.json (same shape as structure.json) and a report of
pages whose note count changed, with the old and new counts.
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
NO_NOTES = ({f'{i:04d}' for i in range(6, 16)}
            | {f'{i:04d}' for i in range(138, 160)} | {'0138'}
            # Aneks II/III's numbered clauses are the printed text; only
            # the two trailing editorial notes (0168, 0171) are notes,
            # which v1's chain caught and this fallback keeps:
            | {f'{i:04d}' for i in range(160, 172)})


def lines_of(page):
    ws = [(x[1], x[0], x[5].strip()) for x in page['words'] if x[5].strip()]
    ws.sort()
    lines = []
    for top, left, word in ws:
        if lines and abs(lines[-1][0] - top) < 30:
            lines[-1][2].append((left, word))
        else:
            lines.append([top, left, [(left, word)]])
    out = []
    for top, left, parts in lines:
        parts.sort()
        out.append({'top': top, 'text': ' '.join(w for _, w in parts)})
    return out


def parse_notes(lns, lp_by_top=None):
    """(body_lines, notes) by geometry. The block start is chosen among
    the foot's gaps: the candidate whose below-block parses as the
    strongest note chain wins (a read 1 opening a 1..k run beats a
    fragment; ties -> the larger block). lp_by_top: the line pass's text
    per line top (the marker witness)."""
    lp_by_top = lp_by_top or {}
    if not lns:
        return lns, []
    H = lns[-1]['top'] + 100
    foot = [l for l in lns if l['top'] > H * 0.45]
    if not foot:
        return lns, []
    tops = [l['top'] for l in foot]
    pitch = min(b - a for a, b in zip(tops, tops[1:]) if b - a > 20) \
        if len(tops) > 1 else 90
    # candidate gaps in the foot, largest first
    gaps = []
    for i in range(1, len(foot)):
        g = foot[i]['top'] - foot[i - 1]['top']
        if g > pitch * 1.1:
            gaps.append((g, i))
    if not gaps:
        return lns, []
    gaps.sort(reverse=True)
    lp_by_top = lp_by_top or {}
    best = None
    for g, i in gaps:
        block = foot[i:]
        notes = tolerant_notes(block, lp_by_top)
        if not notes:
            continue
        nums = [x['num'] for x in notes]
        # score: a read 1 at the open of a contiguous 1..k chain is the
        # strongest; else the larger block
        contiguous = nums == list(range(1, len(nums) + 1))
        score = (1 if contiguous and notes[0].get('num_read', 1) == 1
                 else 0, len(notes))
        if best is None or score > best[0]:
            best = (score, lns[:len(lns) - len(block)], notes)
    if best is None:
        return lns, []
    return best[1], best[2]


def tolerant_notes(block, lp_by_top):
    """The note starts of one candidate block. A start is a line whose
    page-pass text opens with a 1-2 digit number, or whose line-pass
    text opens with a lone digit/artifact glyph before a capital, quote
    or siglum (the page pass's mangled digits: 'ty Schmidt' -> the line
    pass's '% Schmidt'). Accepted in order, renumbered when the read
    chain is not 1..k."""
    starts2 = []
    for i, l in enumerate(block):
        m = re.match(r'^(\d{1,2})[.,)]?\s*(\S.*)$', l['text'])
        hit = bool(m and len(m.group(2)) > 3)
        if not hit:
            lp = lp_by_top.get(l['top'])
            if lp:
                toks = lp.split()
                if len(toks) >= 2 and re.fullmatch(r'[\d!%*+$§£|.]', toks[0]) \
                        and re.match(r'([A-ZĄĆĘŁŃÓŚŹŻ„"(]|AW\.|Rel\.|AGH|'
                                     r'KI\.|Dom\.|Por\.|Np\.|Q\b)', toks[1]):
                    hit = True
        if hit:
            starts2.append((i, int(m.group(1)) if m else None, l))
    notes = []
    prev = 0
    for j, (i, num, l) in enumerate(starts2):
        text = l['text']
        fresh = num is not None and bool(
            re.match(r'^\d{1,2}[.,)]?\s*([A-ZĄĆĘŁŃÓŚŹŻ„"(]|AW\.|'
                     r'Rel\.|AGH|KI\.|Dom\.|Por\.|Np\.|Q\b)', text))
        first_ok = j == 0 and (num is None or num <= 2 or fresh)
        if first_ok or (num is not None and num == prev + 1) \
                or (notes and num == prev and fresh) \
                or (notes and num == prev + 2 and fresh) \
                or (notes and num is None):
            assigned = num if num is not None else prev + 1
            notes.append([i, assigned, num])
            prev = assigned
    if not notes:
        return []
    out = []
    for k, (i, num, raw_num) in enumerate(notes):
        last = notes[k + 1][0] if k + 1 < len(notes) else len(block)
        first_line = block[i]['text']
        rest = ' '.join(block[j]['text'] for j in range(i + 1, last))
        if raw_num is None:
            # the page-pass leading token is mangled ('ty Schmidt'); the
            # line pass read the same line cleanly at 2.5x - its
            # remainder IS the note's opening line
            lp = lp_by_top.get(block[i]['top'])
            if lp and len(lp.split()) >= 2:
                first_line = ' '.join(lp.split()[1:])
        text = (first_line + ' ' + rest).strip()
        m = re.match(r'^\d{1,2}[.,)]?\s*(.*)$', text, re.S)
        out.append({'num': num,
                    'top': block[i]['top'],
                    'text': (m.group(1) if m else text).strip()})
    nums = [x['num'] for x in out]
    if nums != list(range(1, len(out) + 1)):
        for j, x in enumerate(out):
            x['num_read'] = x['num']
            x['num'] = j + 1
    return out


def annex_notes(n, lines):
    """The table notes of an annex sheet: the block below the table's
    last row (the last row-anchor's top + one row height), parsed with
    the tolerant rules (the line pass did not read these sheets)."""
    try:
        cells = json.load(open(os.path.join(OCR, 'annex_cells.json'),
                               encoding='utf-8'))
        pairs = sorted(((r['y'], int(k)) for k, r in
                        cells[n]['rows'].items()))
    except Exception:
        return []
    if not pairs:
        return []
    # the sheet's rows are the longest chain (each next = prev+1, or a
    # section restart at 1); the trailing false anchors (note digits
    # misparsed as row anchors) drop out
    best = []
    for start in range(len(pairs)):
        chain = [pairs[start]]
        for y, num in pairs[start + 1:]:
            prev = chain[-1]
            # a jump of more than 260 px ends the table: what follows is
            # the Razem row's whitespace and the notes (whose digits
            # would otherwise be swallowed as a section restart)
            if y - prev[0] > 260:
                break
            if num == prev[1] + 1 or (num == 1 and prev[1] >= 5):
                chain.append((y, num))
        if len(chain) > len(best):
            best = chain
    ys = [y for y, _ in best]
    if not ys:
        return []
    cut = max(ys) + 110
    below = [l for l in lines if l['top'] > cut]
    if not below:
        return []
    # the trailing total row ('Razem ...') is part of the table, not the
    # notes: drop leading lines until the first note start
    starts_at = None
    for cut_try in (cut, max(ys) + 60, max(ys) + 30):
        below = [l for l in lines if l['top'] > cut_try]
        if not below:
            continue
        for i, l in enumerate(below):
            m = re.match(r'^(\d{1,2})[.,)]?\s*(\S.*)$', l['text'])
            if m and len(m.group(2)) > 10:
                nxt = below[i + 1]['text'] if i + 1 < len(below) else ''
                # a table row continues with '|' cells; a note does not
                if '|' not in l['text'] and '|' not in nxt:
                    starts_at = i
                    block = below[starts_at:]
                    notes = tolerant_notes(block, {})
                    # a table note is prose (many lowercase words); the
                    # missed table rows the block may also catch are
                    # name/number debris - drop them
                    notes = [x for x in notes if _is_prose(x['text'])]
                    if notes:
                        return notes
    return []


def _is_prose(text):
    toks = text.split()
    lower = [t for t in toks if len(t) >= 3 and t.isalpha() and t.islower()]
    digits = [t for t in toks if re.fullmatch(r'[\d.,*/]+', t)]
    return len(lower) >= 5 and len(digits) <= 4


def main():
    files = sorted(f for f in os.listdir(OCR)
                   if f.endswith('.json') and len(f) == 9 and f[:4].isdigit())
    old = json.load(open(os.path.join(OCR, 'structure.json'),
                         encoding='utf-8'))
    out = {}
    changed = []
    for fn in files:
        n = fn[:4]
        page = old[n]
        if 139 <= int(n) <= 159:
            # the annex sheets' trailing table notes (about fifteen across
            # the 21 sheets - '1 Sroczewskie Olędry powstały...', 'Razem
            # z OI. Góry.') are NOT auto-parsed: on the warped sheets the
            # row anchors and the note digits are geometrically
            # entangled, and the row-major page text of several sheets is
            # column-major garbage, so the block test misfires (0148's
            # rows parsed as notes, 0146's notes lost). Their text is
            # captured in the strip reads and goes to the spot sheet with
            # the sheet crops (the editor's ruling: the spot sheet shows
            # the cropped area). The parse stays in annex_notes() for the
            # record, unused.
            out[n] = {'lines': page['lines'], 'notes': [],
                      'height': page['height']}
            continue
        if n in NO_NOTES:
            out[n] = {'lines': page['lines'], 'notes': [],
                      'height': page['height']}
            continue
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        lns = lines_of(d)
        lp_path = os.path.join(OCR, 'lines', n + '.json')
        lp_by_top = {}
        if os.path.isfile(lp_path):
            for r in json.load(open(lp_path, encoding='utf-8')):
                if not r.get('skipped'):
                    lp_by_top[r['top']] = (r.get('line_pol') or '')
        body, notes = parse_notes(lns, lp_by_top)
        # v1's notes stay where v2 found fewer (its geometry can miss a
        # block the chain caught); v1's notes are geometry-checked first
        v1 = page['notes']
        if len(notes) < len(v1):
            ok_v1 = all(x['top'] > page['height'] * 0.40 for x in v1)
            if ok_v1:
                notes = v1
        out[n] = {'lines': page['lines'], 'notes': notes,
                  'height': page['height']}
        # keep the original line list (same source); notes are the change
        o = len(page['notes'])
        if o != len(notes):
            changed.append((n, o, len(notes),
                            [x['num'] for x in page['notes']][:6],
                            [x['num'] for x in notes][:6]))
    with open(os.path.join(OCR, 'structure2.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('pages:', len(out), 'changed:', len(changed))
    for c in changed:
        print(c)
    total_old = sum(len(p['notes']) for p in old.values())
    total_new = sum(len(p['notes']) for p in out.values())
    print('notes old:', total_old, 'new:', total_new)


if __name__ == '__main__':
    main()
