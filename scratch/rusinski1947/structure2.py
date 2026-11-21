# -*- coding: utf-8 -*-
"""Note parsing v6: strip lines ALIGNED to the page's own lines.

The v5 state machine grew too many interacting branches (digit-led,
artifact-led, lookalike, CIT, ends_sent, ABBR...) and every fix exposed
a new class. The structural fact it kept re-discovering: psm 4's strip
lines correspond to the PRINT's lines, and the page pass's rebuilt
lines (TSV reading order) are 1:1 with the print lines. So ALIGN the
strip lines to the page lines:

  - a strip line whose fold matches a page line's PREFIX begins that
    print line -> a note start iff its leading token is a 1-2 digit
    number, a strong artifact glyph, or a digit-1 lookalike ('l' = 1);
  - a strip line matching a page line's MIDDLE/SUFFIX is a psm-4 split
    artifact -> continuation of the previous note (this kills the
    '4 (VII)', '78, Wlosciejeskie', '1), Lubienskich' fragment class
    at the root);
  - psm4 sometimes MERGES two print lines into one strip line (0021's
    '5 Schumacher... 88. " Kaczmarczyk'): handled by the mid-line
    artifact split INSIDE the merged strip line (strong artifacts and
    chain-expected digits after a sentence end).

Marker-less notes (the OCR dropped the marker glyph; 0061's note 4):
a psm4 PARAGRAPH break + previous sentence end + citation opener.

The note tops come from the ALIGNMENT (the page line the note starts
on) - no separate matching step, no interpolation except when a strip
line matches nothing (garbled strips: 0036, 0105 - those pages fall
back to v5's heuristics).

Writes structure2.json.
"""
import json, os, re, difflib

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

CAP = r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]'
DIGIT = re.compile(r'^(\d{1,2})[.,)%/*!?+§$£]{0,2}\s+(.*)$', re.S)
ARTIFACT = re.compile(r'^([!%*+$§£|?»"?<>‚‘’”]{1,2})\s+(.*)$', re.S)
ONE = re.compile(r'^([lI1¡|UL]{1,2})\s+(.*)$', re.S)
CIT = re.compile(
    r'^(?:AW|AM|AGH|AGAD|Rel|Dom|Kat|Tp|KI|KL|Q|Por|Zob|Np|Lustr|Inscr'
    r'|Tod|MP|MG|GC|Syr|Sygn|Szk|Wil|Dziew|Urz|Inw|AP|BCh|Die|Der|Das'
    r'|In|Am|An|Vom|Uwaga|tj|Tj)\b|„', re.UNICODE)
ABBR = re.compile(
    r'(?:[A-ZĄĆĘŁŃÓŚŹŻ]{1,4}|fol|s|nr|vol|t|cz|it|nd|tj|d|j|w|m|z'
    r'|[IVX]+)\.$', re.UNICODE)


def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())


def lines_of(page):
    """Lines from the TSV words: sort by top (ties by left), group with
    a HEIGHT-RELATIVE gap threshold, then order each line's words by
    left.

    Neither pure order works alone: the TSV reading order follows
    Tesseract's BLOCK order, which interleaves on pages where a short
    body line forms its own block placed after the footnote block
    (0022: 'dzierzawy wieczystej.' came after the notes); a fixed
    top-bucket (v1: 30px) orphaned first words on warped baselines
    (0018: 'we' displaced 31px). The gap threshold scales with the
    line's own height (warp displacement is a fraction of the x-height;
    adjacent print lines are ~1.4x the height apart, so 0.55*h never
    merges neighbours), and superscript markers (top ~30px above the
    line) still join their line while left-ordering keeps them at
    their true position.
    """
    ws = [x for x in page['words'] if x[5].strip()]
    ws.sort(key=lambda x: (x[1], x[0]))
    groups = []
    for x in ws:
        l, t, w_, h, txt = x[0], x[1], x[2], x[3], x[5].strip()
        if groups:
            g = groups[-1]
            hs = sorted(z[2] for z in g)
            gh = hs[len(hs) // 2]
            thr = max(30, min(55, 0.55 * gh))
            if t - g[0][1] <= thr:
                g.append((l, t, h, txt))
                continue
        groups.append([(l, t, h, txt)])
    lines = []
    for g in groups:
        g.sort(key=lambda z: z[0])
        lines.append({'top': g[0][1], 'left': g[0][0],
                      'text': ' '.join(z[3] for z in g),
                      'hs': [z[2] for z in g]})
    for ln in lines:
        hs = sorted(ln.pop('hs'))
        ln['h'] = hs[len(hs) // 2] if hs else 0
    return lines


def strip_lines(n):
    """The better strip model's lines with paragraph flags."""
    sp = os.path.join(OCR, 'widestrips', n + '.json')
    if not os.path.isfile(sp):
        return None
    d = json.load(open(sp, encoding='utf-8'))

    def parse(text):
        out = []
        blanks = 0
        for l in text.split('\n'):
            if not l.strip():
                blanks += 1
                continue
            out.append({'text': l.strip(), 'para': blanks > 0})
            blanks = 0
        return out

    a, b = parse(d['pol']), parse(d['std'])
    lines = a if len(a) >= len(b) else b
    return {'lines': lines, 'y0': d['y0']}


def align(strip, foot):
    """Align strip lines to page foot lines. Returns per strip line:
    (page_index, 'start'|'mid'|'none'). Garbage strip lines (OCR debris
    at 3x: 'LYZKA YZEWYY...', fold too short, too few real words) take
    NO page line - they used to consume one in the opcode run and
    shift every later alignment by a line or two."""
    def garbage(s):
        f = fold(s)
        toks = [t for t in re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{2,}',
                                      s)]
        # short REAL note lines ('5 Tamże.') carry a word of length
        # >= 4 or a sigla token ('AW. A. 1—4.')
        if len(f) < 12 and not any(
                len(t) >= 4 or re.fullmatch(
                    r'[A-ZĄĆĘŁŃÓŚŹŻ]{1,4}\.?', t, re.UNICODE)
                for t in toks):
            return True
        return len(toks) < 1
    sf_all = [fold(s['text'])[:36] for s in strip]
    pf = [fold(p['text'])[:36] for p in foot]
    keep = [i for i in range(len(strip)) if not garbage(strip[i]['text'])]
    sm = difflib.SequenceMatcher(None, [sf_all[i] for i in keep], pf,
                                 autojunk=False)
    assign = {}
    for tag, a1, a2, b1, b2 in sm.get_opcodes():
        if tag in ('equal', 'replace'):
            for k in range(min(a2 - a1, b2 - b1)):
                assign[keep[a1 + k]] = (b1 + k, 'start')
        elif tag == 'delete':
            # kept strip lines with no page line: fuzzy per-line match
            for k in range(a1, a2):
                i = keep[k]
                best, br = None, 0.0
                for j in range(len(pf)):
                    if j in {v[0] for v in assign.values()}:
                        continue
                    r = difflib.SequenceMatcher(None, sf_all[i],
                                                pf[j]).ratio()
                    if r > br:
                        br, best = r, j
                if br >= 0.72:
                    assign[i] = (best, 'start')
    # every pair must EARN its similarity: the opcode's positional
    # 'replace' pairing otherwise binds debris strip lines to real page
    # lines (0116: '- —— w——' ate '1 Rel. Cost. nr 224' and '2 AW.
    # Blinek', leaving the real note lines homeless)
    for i in list(assign):
        j, kind = assign[i]
        r = difflib.SequenceMatcher(None, sf_all[i], pf[j]).ratio()
        if r < 0.55:
            del assign[i]
    # reassign the orphaned strip lines to their best UNCLAIMED page
    # line (fuzzy; these are real lines whose opcode partner was junk)
    claimed = {v[0] for v in assign.values()}
    for i in range(len(strip)):
        if i in assign or garbage(strip[i]['text']):
            continue
        best, br = None, 0.0
        for j in range(len(pf)):
            if j in claimed:
                continue
            r = difflib.SequenceMatcher(None, sf_all[i], pf[j]).ratio()
            if r > br:
                br, best = r, j
        if br >= 0.6:
            assign[i] = (best, 'start')
            claimed.add(best)
    # second pass: strip lines matched to the SAME page line as an
    # earlier strip line, or fuzzy-matching a page line's SUFFIX, are
    # psm-4 split artifacts -> 'mid'
    used = {}
    for i in sorted(assign):
        j, kind = assign[i]
        if j in used:
            assign[i] = (j, 'mid')
        else:
            used[j] = i
    for i in range(len(strip)):
        if i not in assign:
            # try suffix/middle match against any page line
            best, bj, bkind = None, None, 'none'
            for j in range(len(pf)):
                if not sf_all[i] or not pf[j]:
                    continue
                if pf[j].endswith(sf_all[i][:24]) or sf_all[i] in pf[j]:
                    bkind, bj = 'mid', j
                    break
            if bj is not None:
                assign[i] = (bj, bkind)
    # a 'start' strip line whose fold is a strict SUBSTRING (not a
    # prefix) of its page line's fold is the second half of a print
    # line that psm 4 broke in two (0050's 'C.' / '4 (VII), r. 1793')
    # - REMOVED: it also demoted legit note lines whose page twin
    # carries the unread marker digit ('5 "Tamze, s. 143.' ->
    # 'Tamze, s. 143.', 0020 note 5); the psm4-split cases it was
    # written for are handled by the same-page-line demotion above.
    return assign


def parse_strip(strip, foot, BH=80):
    """Note starts from aligned strip lines. Returns (notes, dbg)."""
    assign = align(strip, foot)
    # MERGED-LINE REPAIR: psm 4 sometimes fuses the body's last line
    # with note 1's first line into ONE strip line ('Tak samo trudno
    # tutaj 1 Przywilej lokacyjny...'). The page tells the truth: a
    # BODY-type page line followed by a NOTE-type page line whose folds
    # together match the strip line. Split the strip text at the
    # proportional offset; the second half carries split=True - its
    # digit/artifact/one-led token starts a note on the type-boundary
    # evidence alone (no prev_ok needed: the page-line pair IS the
    # boundary).
    claimed = {}
    for i in sorted(assign):
        j, kind = assign[i]
        if kind == 'start' and j not in claimed:
            claimed[j] = i
    work = []
    for i, s in enumerate(strip):
        j, kind = assign.get(i, (None, 'none'))
        if kind == 'start' and j is not None and j + 1 < len(foot) \
                and (j + 1) not in claimed:
            f_all = fold(s['text'])
            f1 = fold(foot[j]['text'])
            f2 = fold(foot[j + 1]['text'])
            if f_all and f1 and f2 and len(f_all) > len(f1) + 12:
                r1 = difflib.SequenceMatcher(None, f_all, f1).ratio()
                r12 = difflib.SequenceMatcher(
                    None, f_all, (f1 + f2)[:len(f_all)]).ratio()
                if r12 >= 0.75 and r12 > r1 + 0.05:
                    pos = round(len(s['text']) * len(f1)
                                / max(1, len(f1) + len(f2)))
                    # snap to the nearest space
                    sp = s['text'].find(' ', max(0, pos - 15), pos + 15)
                    if sp > 0:
                        work.append({'text': s['text'][:sp],
                                     'para': s['para'], 'j': j,
                                     'split': False})
                        work.append({'text': s['text'][sp + 1:],
                                     'para': False, 'j': j + 1,
                                     'split': True})
                        claimed[j + 1] = i
                        continue
        work.append({'text': s['text'], 'para': s['para'], 'j': j,
                     'split': False})
    starts = []
    for i, s in enumerate(work):
        j = s['j']
        l = s['text']
        is_boundary_start = (j is not None)
        small = j is not None and foot[j].get('h', 0) <= 0.88 * BH
        smallish = j is not None and foot[j].get('h', 0) <= 0.95 * BH
        # leading-token classes
        md, ad, od = DIGIT.match(l), ARTIFACT.match(l), ONE.match(l)
        prev = work[i - 1]['text'] if i else ''
        prev_ok = bool(re.search(r'[.!?»:;][”"]?\s*$', prev)) and not (
            prev.split() and ABBR.match(prev.split()[-1]))
        if not starts and s['para'] and smallish:
            # FIRST-NOTE rule, marker-glyph-independent: the wide strip
            # includes body lines (y >= y0), so the decisive witnesses
            # are the psm4 PARAGRAPH break + a citation opener after a
            # <=2-char token ('U Por. daty...', 'l Ludkiewicz...') +
            # footnote-size type on the matched page line (body
            # paragraphs are body-size type; 0023's solid-set note 1
            # had no readable marker digit even at 6x).
            tok0 = l.split()[0] if l.split() else ''
            rest0 = l[len(tok0):].lstrip()
            # the type-transition witness: the PREVIOUS page line is
            # body-type and this line is footnote-size - the boundary
            # (0029's long notes run h 47-63 against body ~67, too
            # close for a fixed ratio, but the STEP down marks the
            # block)
            trans = (j is not None and j > 0
                     and foot[j - 1].get('h', 0) > 0.95 * BH
                     and foot[j].get('h', 0) <= 0.93 * BH)
            if len(tok0) <= 2 and rest0 and (re.match(CAP, rest0)
                                             or CIT.match(rest0)) \
                    and (CIT.match(rest0) or trans):
                starts.append((i, None, rest0))
                continue
        if s.get('split') and small and (md or ad or od):
            # SPLIT-start: the page-line pair (body type -> note type)
            # is itself the boundary evidence; the digit/artifact/one
            # token in the second half starts the note without prev_ok
            if md:
                starts.append((i, int(md.group(1)), md.group(2).strip()))
            else:
                starts.append((i, None, (ad or od).group(2).strip()))
            continue
        if md and is_boundary_start and int(md.group(1)) <= 40 and small:
            # digit-led starts require footnote-size type: a numbered
            # section heading or a body enumeration is body-size type
            # (0075's '2. Sklad spoleczny', 0073's '3. do warunkow...')
            starts.append((i, int(md.group(1)), md.group(2).strip()))
        elif (ad or od) and is_boundary_start and (prev_ok or small):
            starts.append((i, None, (ad or od).group(2).strip()))
        else:
            # GLUED one-lookalike: the marker digit fused with the
            # note's first word ('LKremmer u. Dalchow...' = '1 Kremmer')
            go = re.match(r'^[lI1¡|UL]([A-ZĄĆĘŁŃÓŚŹŻ]\S*)\s+(.*)$', l)
            if go and is_boundary_start and (prev_ok or small
                                             or (not starts and s['para']
                                                 and smallish)):
                starts.append((i, None,
                               go.group(1) + ' ' + go.group(2)))
            elif s['para'] and is_boundary_start and prev_ok \
                    and CIT.match(l) and len(l) > 12 and starts:
                starts.append((i, None, l))
    if not starts:
        return [], []
    notes = []
    for k, (i, read, text) in enumerate(starts):
        last = starts[k + 1][0] if k + 1 < len(starts) else len(work)
        # the note's FULL text: its strip lines from the start to the
        # next start (the earlier code stored only the start line's
        # remainder - every multi-line note was truncated to its first
        # line)
        joined = ' '.join(work[j]['text'] for j in range(i, last))
        # strip the leading marker token once (digit / artifact /
        # one-lookalike, up to 2 chars + a quote-class suffix)
        joined = re.sub(r'^(?:\d{1,2}[.,)%/*!?+§$£]{0,2}|[!%*+$§£|?»"?<>‚‘’”]'
                        r'{1,2}|[lI1¡|UL]{1,2})\s+', '', joined, count=1)
        top = None
        j0 = work[i]['j']
        if j0 is not None:
            top = foot[j0]['top']
        notes.append({'read': read, 'top': top, 'text': joined.strip()})
    # the mid-line split inside merged strip lines
    out = []
    expected = None
    for nt in notes:
        # STRONG artifacts only - digits here cut volume numbers out of
        # citations ('C. 4 (VII), r. 1793' lost its '4 (VII)...')
        parts = re.split(
            r'(?<=[.!?»”])\s+([!%*+$§£»"?<>‚‘’]{1,2})\s+'
            r'(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])', nt['text'])
        if len(parts) >= 3 and nt['read'] is not None:
            out.append({'read': nt['read'], 'top': nt['top'],
                        'text': parts[0].strip()})
            j = 1
            while j < len(parts) - 1:
                tok = parts[j]
                rest = parts[j + 1].strip()
                read = None
                if tok.isdigit():
                    read = int(tok)
                out.append({'read': read, 'top': None, 'text': rest})
                j += 2
        else:
            out.append(nt)
    # split-produced notes have no top of their own: interpolate half a
    # pitch below the last known top (0124's '+ T.w.')
    last_top = None
    for x in out:
        if x['top'] is None and last_top is not None:
            x['top'] = last_top + 45
        if x['top'] is not None:
            last_top = x['top']
    for i, x in enumerate(out):
        x['num'] = i + 1
    # ONE-LINE NUDGE: the page lines are the authority for the note
    # tops; when a note's matched top sits one line high (its text's
    # opening matches the line BELOW better), shift it down
    for nt in out:
        if nt['top'] is None:
            continue
        j = next((i for i, l in enumerate(foot)
                  if l['top'] == nt['top']), None)
        if j is None or j + 1 >= len(foot):
            continue
        f_note = fold(nt['text'])[:20]
        f_here = fold(re.sub(r'^[\d!%*+$§£|.,)»\s\-—–]+', '',
                             foot[j]['text']))[:20]
        f_below = fold(re.sub(r'^[\d!%*+$§£|.,)»\s\-—–]+', '',
                              foot[j + 1]['text']))[:20]
        r_here = difflib.SequenceMatcher(None, f_here, f_note).ratio()
        r_below = difflib.SequenceMatcher(None, f_below, f_note).ratio()
        if r_below > r_here and r_below >= 0.7:
            nt['top'] = foot[j + 1]['top']
    return out, []


def parse_notes(lns, n=None):
    if not lns:
        return lns, []
    H = lns[-1]['top'] + 100
    body_hs = sorted(l['h'] for l in lns
                     if l['top'] < H * 0.45 and l['h'] >= 30)
    BH = body_hs[len(body_hs) // 2] if body_hs else 80
    foot = [l for l in lns if l['top'] > H * 0.45]
    if not foot:
        return lns, []
    strip = strip_lines(n) if n else None
    if strip:
        # the alignment set = the lines the strip actually covers (its
        # y0) - a fixed 0.45H foot threshold excludes the notes of
        # note-heavy pages (0029's notes begin at 34% of the page
        # height) and the strip lines then match nothing
        fseen = [l for l in lns if l['top'] >= strip['y0'] - 20]
        notes, _ = parse_strip(strip['lines'], fseen, BH)
        if notes:
            body = [l for l in lns if l['top'] < min(
                x['top'] for x in notes if x['top'] is not None)]
            return body, notes
    return lns, []


def main():
    files = sorted(f for f in os.listdir(OCR)
                   if f.endswith('.json') and len(f) == 9
                   and f[:4].isdigit())
    old = json.load(open(os.path.join(OCR, 'structure.json'),
                         encoding='utf-8'))
    out = {}
    fallbacks = []
    for fn in files:
        n = fn[:4]
        page = old[n]
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        lns = lines_of(d)
        if n in NO_NOTES:
            out[n] = {'lines': lns, 'notes': [],
                      'height': page['height']}
            continue
        body, notes = parse_notes(lns, n=n)
        if not notes and page['notes']:
            # garbled-strip backstop: the v1 geometry parse's notes,
            # when they all sit in the foot. The texts are rebuilt from
            # the REBUILT lines between the v1 tops, dropping debris
            # lines (h < 30: the tiny artifact rows like 0036's
            # '1 " LYS 1:...' that the v1 grouping glued into the text)
            H = lns[-1]['top'] + 100
            v1n = page['notes']
            if all(x['top'] > H * 0.45 for x in v1n):
                notes = []
                for i, x in enumerate(v1n):
                    nxt = v1n[i + 1]['top'] if i + 1 < len(v1n) else 10 ** 9
                    part = [l['text'] for l in lns
                            if x['top'] - 40 <= l['top'] < nxt - 40
                            and l['h'] >= 30]
                    notes.append({'num': i + 1,
                                  'num_read': x.get('num_read'),
                                  'top': x['top'],
                                  'text': ' '.join(part) or x['text']})
                fallbacks.append(n)
        out[n] = {'lines': lns,
                  'notes': [{'num': x['num'],
                             'num_read': x.get('read'),
                             'top': x['top'], 'text': x['text']}
                            for x in notes],
                  'height': page['height']}
    with open(os.path.join(OCR, 'structure2.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    total = sum(len(p['notes']) for p in out.values())
    print('pages:', len(out), 'notes:', total,
          '| v1-fallback pages:', fallbacks)


if __name__ == '__main__':
    main()
