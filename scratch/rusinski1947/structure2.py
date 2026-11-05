# -*- coding: utf-8 -*-
"""Note parsing v4: the block anchored by the 3x STRIP's note openings.

Witness history:
  v1 required note 1 to read as '1' - one misread digit dropped whole
     blocks (336 -> 549 notes when fixed).
  v2 anchored at the foot's largest gap - a mid-page gap before a
     section heading swallowed body stretches (0018, 0075, 0077, 0079).
  v3 added a type-size gate (footnote type < body type) - right idea,
     wrong threshold: the book's footnote type is only ~10-20% smaller
     than body, pages vary (0052's note h=62 vs body ~70), and the gate
     lost genuine notes (0036, 0052, 0078, 0114).
  v4: the page's 3x note strip (notestrips/, psm 6, both models) is the
     highest-quality read of the foot region. Its note openings
     (strip_notes: digit- or artifact-led paragraphs continuing 1..k)
     are MATCHED to the page's own lines (folded prefix); matched lines
     are the note starts - geometry from the page, segmentation from
     the strip, each filtering the other's noise (a strip paragraph
     that matches no page line is a psm-6 artifact; a page line the
     strip did not see needs the gap+type fallback). The topmost match
     is note 1; the block extends to the page bottom. Pages with no
     strip match fall back to the v2/v3 gap+type heuristic (0075's
     heading still fails the type test: body-size type).

Also: lines rebuilt in TSV READING ORDER (the v1 top-sort orphaned
first words on warped pages: 'we wcześniejszym' lost its 'we').

The pure table pages (0077, 0079) and the annexes stay in NO_NOTES.
Writes structure2.json.
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
NO_NOTES = ({f'{i:04d}' for i in range(6, 16)}
            | {f'{i:04d}' for i in range(138, 172)} | {'0138'}
            # the pure table pages (inspection 2026-11-05): their rows
            # parsed as 'notes' and dropped out of the body flow
            | {'0077', '0079'}
            # 0075 (wide strip 2026-11-05): the foot region holds the
            # section heading '2. Sklad spoleczny' + its paragraph, the
            # body flows through it to the page end; no note numbers
            # anywhere in the 3x read - no notes on the page
            | {'0075'})


def lines_of(page):
    """Lines from the TSV words, in TSV (reading) ORDER.

    The earlier top-sort grouping broke on warped pages: the first word
    of a line ('we wcześniejszym...' on 0018) can carry a top 30-40px
    off its line's bucket (baseline warp), was sorted into its own
    'line', and the body lost its first words. Tesseract emits words
    line by line, so the array order IS the line membership: a new line
    starts only when the left edge drops back (a wrapped/indented line
    never starts left of the previous word) or the top jump exceeds
    ~0.75x the word height (within-line warp drift stays below that).
    """
    ws = [x for x in page['words'] if x[5].strip()]
    lines = []
    prev = None
    for x in ws:
        l, t, w_, h, txt = x[0], x[1], x[2], x[3], x[5].strip()
        new = prev is None
        if not new:
            pl, pt, ph = prev
            if l < pl - 60 or abs(t - pt) > 0.75 * max(ph, h, 40):
                new = True
        if new:
            lines.append({'top': t, 'text': txt, 'left': l, 'hs': [h]})
        else:
            lines[-1]['text'] += ' ' + txt
            lines[-1]['hs'].append(h)
        prev = (l, t, h)
    for ln in lines:
        hs = sorted(ln.pop('hs'))
        ln['h'] = hs[len(hs) // 2] if hs else 0
    return lines


def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())


def strip_openings(n):
    """The WIDE strip's note paragraphs for one page: the whole foot
    region at 3x (the old notestrips began at v2's block start and so
    could never witness the boundary). Returns the better model's
    [{num_read, text}] - note starts are paragraphs led by a 1-2 digit
    number or an artifact glyph before a capital/quote; other paragraphs
    continue the previous note. Numbered by ORDER (the reads ride
    along as num_read)."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sp = os.path.join(OCR, 'widestrips', n + '.json')
    if not os.path.isfile(sp):
        return []
    d = json.load(open(sp, encoding='utf-8'))

    def parse(text):
        ART = '!%*+$§£|»"”?()<>‚‘’„-—,'
        CAP = r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]'
        # digit-lookalike misreads seen in the strips ('ll' = 11,
        # 'Iż' = 12, 'U' = 4...)
        LOOK = re.compile(r'^[iIlLsSzZżźćńółąę?*BqgOo]{1,2}$')
        # LINE-level segmentation: psm 4 preserves the print's line
        # breaks, and note starts are line events; blank-line paragraphs
        # glued neighbouring notes (0021's 6-7 merged). Guards against
        # false splits inside a note's wrapped lines:
        #   - digit-led: the read should continue the chain (expected =
        #     previous read + 1); a non-continuing digit is accepted as
        #     a misread only when the previous line ended a sentence;
        #   - artifact/lookalike-led: same sentence-end requirement (a
        #     wrapped quotation opens mid-sentence).
        lines = [l.strip() for l in text.split('\n') if l.strip()]

        def ends_sent(idx):
            if idx <= 0:
                return True
            return bool(re.search(r'[.!?]”?[,:;]?\s*$', lines[idx - 1]))
        starts = []
        expected = None
        for idx, l in enumerate(lines):
            m = re.match(r'^(\d{1,2})[.,)%/*!?+§$£]{0,2}\s+(' + CAP +
                         r'.*)$', l)
            if m:
                num = int(m.group(1))
                if expected is None or num == expected:
                    starts.append({'read': num,
                                   'text': m.group(2).strip()})
                    expected = num + 1
                    continue
                if starts and ends_sent(idx):
                    # a misread of the expected number: position decides,
                    # the read rides along
                    starts.append({'read': num, 'text': m.group(2).strip()})
                    expected = num + 1
                    continue
                if starts:
                    starts[-1]['text'] += ' ' + l
                continue
            tok = l.split()[0] if l.split() else ''
            rest = l[len(tok):].lstrip()
            if tok and len(tok) <= 2 and rest and re.match(CAP, rest):
                artifact = all(c in ART for c in tok)
                lookalike = bool(LOOK.match(tok))
                if starts and (artifact or lookalike) and ends_sent(idx):
                    starts.append({'read': None, 'text': rest})
                    expected = (expected + 1) if expected is not None \
                        else None
                    continue
            if starts:
                starts[-1]['text'] += ' ' + l
        # MID-LINE splits: psm 4 sometimes merges two print lines into
        # one strip line; a note start hidden mid-line shows as a
        # sentence end + artifact/lookalike token + capital
        out = []
        for s in starts:
            parts = re.split(
                r'(?<=[.!?»”])\s+([!%*+$§£»"?()<>‚‘’,iIlLsSzZż]{1,2}|'
                r'[!%*+$§£»"?()<>‚‘’]\s?)\s+'
                r'(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])', s['text'])
            if len(parts) >= 3:
                out.append({'read': s['read'], 'text': parts[0].strip()})
                for j in range(1, len(parts) - 1, 2):
                    out.append({'read': None,
                                'text': (parts[j] + ' ' +
                                         parts[j + 1]).strip()})
            else:
                out.append(s)
        return out

    a, b = parse(d['pol']), parse(d['std'])
    # the better model: more starts; tie -> the one whose reads ascend
    def score(starts):
        reads = [s['read'] for s in starts if s['read'] is not None]
        asc = sum(1 for x, y in zip(reads, reads[1:]) if y > x)
        return (len(starts), asc)
    return a if score(a) >= score(b) else b


def parse_notes(lns, lp_by_top=None, n=None):
    lp_by_top = lp_by_top or {}
    if not lns:
        return lns, []
    H = lns[-1]['top'] + 100
    body_hs = sorted(l['h'] for l in lns
                     if l['top'] < H * 0.45 and l['h'] >= 30)
    BH = body_hs[len(body_hs) // 2] if body_hs else 80
    foot = [l for l in lns if l['top'] > H * 0.45]
    if not foot:
        return lns, []
    pitch = pitch_of(foot)

    # PRIMARY: the wide strip's note paragraphs, matched to foot lines.
    # The strip paragraphs carry the note TEXTS (3x quality); the page
    # lines carry the geometry; each filters the other's noise.
    wstarts = strip_openings(n) if n else []
    if wstarts:
        notes = []
        cursor = 0
        suspects = []
        for si, s in enumerate(wstarts):
            f = fold(s['text'])[:20]
            hit = None
            for i in range(cursor, len(foot)):
                lt = re.sub(r'^[\d!%*+$§£|.,)»\s\-—–]+', '',
                            foot[i]['text'])
                lf = fold(lt)[:20]
                if len(lf) >= 8 and min(len(lf), len(f)) >= 8 and \
                        (lf.startswith(f) or f.startswith(lf)):
                    hit = i
                    break
            if hit is not None:
                cursor = hit + 1
                top = foot[hit]['top']
                if foot[hit].get('h', 0) > 0.88 * BH:
                    suspects.append((s.get('read'), top,
                                     foot[hit]['text'][:50]))
            else:
                # unmatched (garbled opening): interpolate between the
                # previous note's top and the NEXT start's matched top
                prev_top = notes[-1]['top'] if notes else foot[0]['top']
                nxt = None
                for s2 in wstarts[si + 1:]:
                    f2 = fold(s2['text'])[:20]
                    for i in range(cursor, len(foot)):
                        lt = re.sub(r'^[\d!%*+$§£|.,)»\s\-—–]+', '',
                                    foot[i]['text'])
                        lf = fold(lt)[:20]
                        if len(lf) >= 8 and min(len(lf), len(f2)) >= 8 \
                                and (lf.startswith(f2)
                                     or f2.startswith(lf)):
                            nxt = foot[i]['top']
                            break
                    if nxt:
                        break
                top = (prev_top + nxt) / 2 if nxt else prev_top + pitch
                if top <= prev_top:
                    top = prev_top + pitch // 2
            notes.append({'num_read': s['read'], 'top': top,
                          'text': s['text']})
        for i, x in enumerate(notes):
            x['num'] = i + 1
        if suspects:
            print(n, 'TYPE-SUSPECT notes:', suspects)
        body = [l for l in lns if l['top'] < min(x['top'] for x in notes)]
        return body, notes

    # FALLBACK: gap + type-size heuristic (garbled strips)
    cands = []
    for i, l in enumerate(foot):
        lp = lp_by_top.get(l['top'], '')
        toks = lp.split() if lp else []
        lp_hit = (len(toks) >= 2
                  and re.fullmatch(r'[\d!%*+$§£|.,)»-]{1,3}', toks[0])
                  and re.match(r'([A-ZĄĆĘŁŃÓŚŹŻ„"(]|AW\.|Rel\.|AGH|KI\.|'
                               r'Dom\.|Por\.|Np\.|Q\b)', toks[1]))
        m = re.match(r'^(\d{1,2})[.,)]?\s*(\S.*)$', l['text'])
        pg_hit = bool(m and len(m.group(2)) > 3
                      and re.match(r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]', m.group(2)))
        if lp_hit or pg_hit:
            # the type-size test, relative to the page's own body: a
            # section heading is body-size type, a footnote is smaller
            if l.get('h', 0) > 0.88 * BH:
                continue
            gap = l['top'] - foot[i - 1]['top'] if i else 10 ** 9
            cands.append((gap, i))
    if not cands:
        return lns, []
    cands.sort(reverse=True)
    block_at = None
    for gap, i in cands:
        if gap <= pitch_of(foot) * 1.1 and gap != 10 ** 9:
            continue
        block_at = i
        break
    if block_at is None:
        return lns, []
    block = foot[block_at:]
    notes = tolerant_notes(block, lp_by_top)
    if not notes:
        return lns, []
    body = lns[:len(lns) - len(block)]
    return body, notes


def pitch_of(foot):
    tops = [l['top'] for l in foot]
    ds = [b - a for a, b in zip(tops, tops[1:]) if b - a > 20]
    return min(ds) if ds else 90


def tolerant_notes(block, lp_by_top):
    starts2 = []
    for i, l in enumerate(block):
        m = re.match(r'^(\d{1,2})[.,)]?\s*(\S.*)$', l['text'])
        hit = bool(m and len(m.group(2)) > 3)
        if not hit:
            lp = lp_by_top.get(l['top'])
            if lp:
                toks = lp.split()
                if len(toks) >= 2 and re.fullmatch(r'[\d!%*+$§£|.]',
                                                   toks[0]) \
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
    for j, x in enumerate(out):
        x['num_read'] = x['num']
        if nums != list(range(1, len(out) + 1)):
            x['num'] = j + 1
    return out


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
        # every page gets its lines REBUILT with the order-preserving
        # grouping (the v1 top-sort orphaned first words on warped
        # pages - 'we wcześniejszym' lost its 'we')
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        lns = lines_of(d)
        if n in NO_NOTES:
            out[n] = {'lines': lns, 'notes': [],
                      'height': page['height']}
            continue
        lp_path = os.path.join(OCR, 'lines', n + '.json')
        lp_by_top = {}
        if os.path.isfile(lp_path):
            for r in json.load(open(lp_path, encoding='utf-8')):
                if not r.get('skipped'):
                    lp_by_top[r['top']] = (r.get('line_pol') or '')
        body, notes = parse_notes(lns, lp_by_top, n=n)
        # v1's notes stay where v3 found fewer (its geometry can miss a
        # block the chain caught); v1's notes are geometry-checked first
        v1 = page['notes']
        if len(notes) < len(v1):
            # v1's notes are only kept when they pass three checks:
            #   a) the nearest REBUILT line is footnote-size type
            #      relative to the page's body;
            #   b) when the strip exists and saw NO note chain, the v1
            #      note's opening must NOT appear in the strip text -
            #      an opening the 3x strip reads as an unnumbered
            #      paragraph is body text (0075's swallowed heading),
            #      not a note;
            #   c) they sit in the lower part of the page.
            body_hs = sorted(l['h'] for l in lns
                             if l['top'] < page['height'] * 0.45
                             and l['h'] >= 30)
            BH_page = body_hs[len(body_hs) // 2] if body_hs else 80
            sp = os.path.join(OCR, 'notestrips', n + '.json')
            strip_txt = ''
            if os.path.isfile(sp):
                sd = json.load(open(sp, encoding='utf-8'))
                strip_txt = sd['pol'] + '\n' + sd['std']
            ops = strip_openings(n)
            ok_v1 = True
            for x in v1:
                if x['top'] <= page['height'] * 0.40:
                    ok_v1 = False
                    break
                near = min(lns, key=lambda l: abs(l['top'] - x['top']),
                           default=None)
                if near is None or near['h'] > 0.88 * BH_page:
                    ok_v1 = False
                    break
                if not ops and strip_txt:
                    of = fold(re.sub(r'^[\d!%*+$§£|.,)»\s\-—–]+', '',
                                     x['text']))[:20]
                    if len(of) >= 12 and fold(strip_txt).find(of) >= 0:
                        ok_v1 = False
                        break
            if ok_v1:
                notes = v1
        out[n] = {'lines': lns, 'notes': notes,
                  'height': page['height']}
        o = len(page['notes'])
        if o != len(notes):
            changed.append((n, o, len(notes)))
    with open(os.path.join(OCR, 'structure2.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('pages:', len(out), 'changed vs v1:', len(changed))
    total = sum(len(p['notes']) for p in out.values())
    print('notes:', total)


if __name__ == '__main__':
    main()
