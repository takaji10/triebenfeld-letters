# -*- coding: utf-8 -*-
"""Dates written between a letter's closing formula and its signature
(docs/DATE_ORDER_PLAN.md, the editor, 2026-11-23).

    python pipeline/review/date_order.py            # scan every holding, report
    python pipeline/review/date_order.py --unit X   # one holding

The editor transcribed many letters with the date where it stands on the page,
between "Ewr Hochfürstliche Durchlaucht" and "treu gehorsamster Knecht / v
Triebenfeld", which breaks the closing sentence in the reading text and the
English. The date belongs after the signature.

This step only READS. It looks at the end of every document for a date that is
followed by more text, and sorts each case:

- regular: salutation line, the date block, one or two closing lines, one
  signature line, all on one page, nothing else between; the signature is the
  document's last line or is followed only by other text (a postscript), which
  is reported. A proposed new order is given.
- irregular: anything else (a page break inside, no salutation, no closing
  line, more than one candidate block, a hyphenated line, ...). Read by hand.

Nothing is decided here: the report is the list a reader goes through. Output:
review/date_order/candidates.json and candidates.md.
"""
import difflib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
import unitlib  # noqa: E402

MON = (r'(Jan|Feb|Fe[bv]r|M[aä]r[tz]|Mer[tz]|Mert|Mart|Apr|Ma[iy]|Jun|Jul|Aug|Sep|Oct|Okt|Nov|Dec|Dez|Xbr|9br|8br|7br|'
       r'janv|f[ée]vr|mars|avril|juin|juil|ao[uû]t|d[ée]c|stycz|lut|marz|kwiet|maj|czerw|lip|sierp|wrze[sś]|'
       r'pa[zź]dz|listop|grud)')
DATE = re.compile(r'(\bden\b|\bd\.|\bd\b|\bam\b|\bce\b|\ble\b|\bdnia\b|\bdie\b).{0,14}\d{1,2}.{0,10}' + MON
                  + r'|\b' + MON + r'\w*\.?,?\s*1[5-9]\d\d\b'
                  + r'|\b\d{1,2}\s*(ten|te|t\.|ter)?\.?\s*' + MON, re.I)
YEAR = re.compile(r'^\s*(Anno\s*)?1[5-9]\d\d\s*\.?\s*$')
CLOSE = re.compile(r'gehorsam|unterth[aä]n|Knecht|Diener|dienstwillig|ergeben|treu|serviteur|s[łl]uga|'
                   r'ob[ée]issant|humble|Verehrung|Ehrfurcht|Freund|amy|ami\b|życzliw|uni[żz]on', re.I)
SAL = re.compile(r'(Ew|Eu|Ewr|Euer|Ewer|Ihr|Votre|V\.|Ja[śs]nie|J\.?\s?W|W\.\s?M|Wielmo)\b.*'
                 r'(Durchl|Excell|Exc|Hochw|Gnaden|Altesse|Excellence|Majest|Hochgeb|Wohlgeb|Pan|Dobrodz)'
                 r'|^\s*(de\s+)?Votre\b|^\s*Ewr\b|^\s*Euer\b', re.I)
NAME = re.compile(r'^\s*((v|von|de|d)\.?\s*)?[A-ZÄÖÜŁŚŻĆ][\wſ\-ąćęłńóśźż]+\.?'
                  r'(\s+((v|von|de)\.?\s*)?[A-ZÄÖÜŁŚŻĆ][\wſ\-ąćęłńóśźż]*\.?){0,3}\s*$')
PLACE = re.compile(r'^\s*[A-ZÄÖÜŁŚŻĆ][\wſąćęłńóśźż\-]+\.?,?\s*$')


def is_date(t):
    return bool(DATE.search(t) or YEAR.match(t))


def documents(unit):
    """[(letter, [(abs line no, page_id, text)])] for one unit's corpus."""
    out, cur, page = [], None, ''
    for n, t in enumerate(io.open(unit.corpus_path, encoding='utf-8').read().split('\n'), 1):
        m = re.match(r'\[DOC (\S+)\]$', t.strip())
        if m:
            cur = (m.group(1), [])
            out.append(cur)
            continue
        m = re.match(r'\[PAGE (\S+)\]$', t.strip())
        if m:
            page = m.group(1)
            continue
        if cur is not None and t.strip():
            cur[1].append((n, page, t))
    return out


def date_block(lines, i):
    """The date block around content line i: (start, end) inclusive indexes."""
    s = e = i
    while e + 1 < len(lines) and (YEAR.match(lines[e + 1][2]) or
                                  (is_date(lines[e + 1][2]) and len(lines[e + 1][2].split()) <= 6)):
        e += 1
    # a place on a line of its own just before "den ..." ("Trąbczyn / den 31ten März 1805")
    if s > 0 and PLACE.match(lines[s - 1][2]) and re.match(r'\s*(den|d\.|ce|le|dnia)\b', lines[s][2], re.I) \
            and not SAL.search(lines[s - 1][2]) and not CLOSE.search(lines[s - 1][2]):
        s -= 1
    return s, e


def classify(lines, s, e):
    why = []
    pages = {lines[k][1] for k in range(max(0, s - 1), min(len(lines), e + 4))}
    before = lines[s - 1][2] if s > 0 else ''
    after = lines[e + 1:]
    closing = []
    k = 0
    while k < len(after) and k < 3 and CLOSE.search(after[k][2]) and not is_date(after[k][2]):
        closing.append(after[k])
        k += 1
    sig = after[k] if k < len(after) else None
    rest = after[k + 1:] if sig else []
    if not SAL.search(before):
        why.append('the line before the date is not a salutation ("%s")' % before.strip()[:50])
    if not closing:
        why.append('no closing formula after the date')
    if sig is None:
        why.append('nothing after the closing')
    elif not NAME.match(sig[2]) or CLOSE.search(sig[2]):
        why.append('the line after the closing does not look like a signature ("%s")' % sig[2].strip()[:50])
    if sig:
        pages = {lines[j][1] for j in range(s - 1 if s > 0 else s, e + 2 + len(closing))}
    if len(pages) > 1:
        why.append('a page break inside the closing')
    for j in range(max(0, s - 1), min(len(lines), e + 2 + len(closing))):
        if lines[j][2].rstrip().endswith(('¬', '-')) and not YEAR.match(lines[j][2]):
            why.append('a hyphenated line inside the closing ("%s")' % lines[j][2].strip()[:40])
            break
    if rest:
        why.append('%d line(s) after the signature (postscript or note), first: "%s"'
                   % (len(rest), rest[0][2].strip()[:50]))
    # a postscript alone does not make a case irregular, but it is reported
    regular = all(w.startswith('%d line(s) after the signature' % len(rest)) for w in why)
    return regular, why, closing, sig, rest


def scan(units):
    cases = []
    for u in units:
        if not os.path.isfile(u.corpus_path) or not os.path.getsize(u.corpus_path):
            continue
        for letter, lines in documents(u):
            if len(lines) < 3:
                continue
            tail_from = max(3, len(lines) - 15)
            seen = set()
            for i in range(tail_from, len(lines) - 1):
                if i in seen or not is_date(lines[i][2]):
                    continue
                s, e = date_block(lines, i)
                seen.update(range(s, e + 1))
                if e >= len(lines) - 1:
                    continue  # the date is the document's last text
                regular, why, closing, sig, rest = classify(lines, s, e)
                case = {
                    'unit': u.slug, 'letter': letter,
                    'pad': '%s-%03d' % (u.slug, int(letter)) if letter.isdigit() else '%s-%s' % (u.slug, letter),
                    'page': lines[s][1],
                    'date_lines': [[lines[k][0], lines[k][2]] for k in range(s, e + 1)],
                    'window': [[lines[k][0], lines[k][2]] for k in range(max(0, s - 3),
                                                                      min(len(lines), e + 6))],
                    'regular': regular, 'why': why,
                }
                if regular:
                    case['proposed'] = {
                        'salutation': lines[s - 1][0],
                        'closing': [c[0] for c in closing],
                        'signature': sig[0],
                        'postscript': len(rest),
                    }
                case['context'] = context(lines, max(0, s - 5), min(len(lines), e + 12))
                cases.append(case)
            # A closing interrupted by something that is not part of it, whatever
            # it is: a salutation line, then one to three lines with no closing
            # word, then a closing line. Catches a date the patterns above do not
            # know (a numeric one, say). Listed for reading, never moved by this.
            for i in range(tail_from - 1, len(lines) - 2):
                if not SAL.search(lines[i][2]) or CLOSE.search(lines[i][2]):
                    continue
                for gap in (1, 2, 3):
                    j = i + gap + 1
                    if j >= len(lines):
                        break
                    mid = range(i + 1, j)
                    if any(CLOSE.search(lines[k][2]) or SAL.search(lines[k][2]) for k in mid):
                        break
                    if CLOSE.search(lines[j][2]):
                        if not set(mid) & seen:
                            cases.append({
                                'unit': u.slug, 'letter': letter,
                                'pad': '%s-%03d' % (u.slug, int(letter)) if letter.isdigit()
                                else '%s-%s' % (u.slug, letter),
                                'page': lines[i][1], 'date_lines': [], 'regular': False,
                                'why': ['an interrupted closing: %d line(s) between "%s" and "%s"'
                                        % (gap, lines[i][2].strip()[:30], lines[j][2].strip()[:30])],
                                'window': [[lines[k][0], lines[k][2]] for k in range(i, min(len(lines), j + 3))],
                                'context': context(lines, max(0, i - 3), min(len(lines), j + 10)),
                            })
                        break
    return cases


def context(lines, a, z):
    """The lines a..z with their corpus numbers, a page marker where the page changes."""
    out, page = [], None
    for k in range(a, z):
        if lines[k][1] != page:
            page = lines[k][1]
            out.append('          [PAGE %s]' % page)
        out.append('%9d  %s' % (lines[k][0], lines[k][2]))
    return out


# ---- the move (docs/DATE_ORDER_PLAN.md, Method 3) ------------------------------
#
# units/<slug>/intake/date_order.yml:
#   moves:
#   - letter: '76'
#     date: ['Breslau den 23ten Aug. 1798.']   # the date lines, exactly as in corpus.txt
#     after: 'v Triebenfeld'                     # the line the date goes after
#     note: ...                                  # who read it, anything odd
#
# Every check below refuses the entry, and nothing of it is written. An entry
# already carried out (the date found directly after its anchor) is skipped.

NL = chr(10)
HYPHEN = ('¬', '-', '=', '⸗')
SET_APART = ('sideways.yml', 'office_notes.yml', 'margin_notes.yml', 'hand_notes.yml')
PCOLS = ['letter', 'line', 'decision', 'confidence', 'cue', 'ratio', 'prev_len', 'page_measure',
         'prev_line', 'context']


def _yaml(path):
    import yaml
    return (yaml.safe_load(io.open(path, encoding='utf-8')) or {}) if os.path.isfile(path) else {}


def _csv(path):
    import csv
    if not os.path.isfile(path):
        return []
    return list(csv.DictReader(io.open(path, encoding='utf-8-sig')))


def plan_move(unit, letter, lines, entry, corpus):
    """(new corpus lines, report) for one entry, or (None, reason)."""
    date = [str(x) for x in entry['date']]
    after = str(entry['after'])
    texts = [t for _, _, t in lines]
    hits = [i for i in range(len(texts) - len(date) + 1) if texts[i:i + len(date)] == date]
    if len(hits) != 1:
        return None, 'the date lines are found %d times, not once' % len(hits)
    s = hits[0]
    e = s + len(date) - 1
    if s == 0:
        return None, 'the date is the first line of the document'
    anchor = [j for j in range(e + 1, min(len(texts), e + 7)) if texts[j] == after]
    if not anchor:
        if texts[s - 1] == after:
            return None, 'already moved'
        return None, 'the anchor "%s" is not within six lines after the date' % after
    a = anchor[0]
    if lines[a][0] - lines[s - 1][0] != a - (s - 1):
        return None, 'a blank line among the moved lines'
    pages = {lines[j][1] for j in range(s - 1, a + 1)}
    if len(pages) != 1:
        return None, 'a page break between the salutation and the anchor'
    # A word split across two lines may stay split only where both halves move
    # together, among the lines between the date and the anchor ("gehor¬ /
    # samstes", Michaelis, letters 78, 81, 92): resolve_linebreaks.py finds
    # its decision again by the two lines' text. Anywhere else, refused.
    together = range(e + 1, a)          # a line here and the next one move as a pair
    for j in range(s - 1, a + 1):
        if texts[j].rstrip().endswith(HYPHEN) and j not in together:
            return None, 'a hyphenated line among the moved lines ("%s")' % texts[j].strip()[:40]
    abs_lo, abs_hi = lines[s - 1][0], lines[a][0]
    moved = range(s, a + 1)
    pair_lines = {lines[j][0] for j in together}
    lb = _csv(os.path.join(unit.dir, 'linebreak_decisions.csv'))
    for r in lb:
        if r.get('letter') == letter and abs_lo <= int(r['line']) <= abs_hi \
                and int(r['line']) not in pair_lines:
            return None, 'a line-break decision on line %s ("%s")' % (r['line'], r.get('context', '')[:40])
    # transcription_decisions.csv is a record of word corrections already made,
    # keyed by document; its "@n" line numbers are those of the day and go stale
    # (2026-11-23: three of them pointed at other documents' lines). Moving a
    # line does not undo a correction: a correction of this document in the
    # moved lines is only noted.
    notes = []
    pad = '%s-%03d' % (unit.slug, int(letter)) if letter.isdigit() else '%s-%s' % (unit.slug, letter)
    for r in _csv(os.path.join(unit.dir, 'transcription_decisions.csv')):
        if r.get('pad') == pad and r.get('proposed') and \
                any(re.search(r'(?<!\w)' + re.escape(r['proposed']) + r'(?!\w)', texts[j])
                    for j in range(s - 1, a + 1)):
            notes.append('a recorded correction in the moved lines: %s' % r.get('decision', '')[:60])
    cw = _yaml(os.path.join(unit.dir, 'catchwords.yml'))
    for r in (cw if isinstance(cw, list) else cw.get('catchwords') or []):
        if str(r.get('letter')) == letter and abs_lo <= int(r.get('line', 0)) + 1 and int(r.get('line', 0)) <= abs_hi:
            return None, 'a catchword at line %s' % r.get('line')
    for fn in SET_APART:
        for b in _yaml(os.path.join(unit.dir, fn)).get('blocks') or []:
            if str(b.get('letter')) != letter:
                continue
            st = [k for k, t in enumerate(texts) if t.strip() == str(b['first']).strip()]
            for k in st:
                if set(range(k, k + int(b['lines']))) & set(moved) or (k <= s - 1 < k + int(b['lines'])):
                    return None, 'a block of %s covers the moved lines' % fn
    order = list(range(e + 1, a + 1)) + list(range(s, e + 1))
    new = corpus[:]
    for k, src in zip(moved, order):
        new[lines[k][0] - 1] = corpus[lines[src][0] - 1]   # the line exactly as stored
    old_seg = sorted(corpus[lines[s][0] - 1:lines[a][0]])
    new_seg = sorted(new[lines[s][0] - 1:lines[a][0]])
    if old_seg != new_seg or len(new) != len(corpus):
        return None, 'not a pure reordering (internal error)'
    return new, {'s': s, 'e': e, 'a': a, 'page': lines[s][1], 'date': date,
                 'between': [texts[j] for j in range(e + 1, a + 1)], 'salutation': texts[s - 1],
                 'after_next': texts[a + 1] if a + 1 < len(texts) else None,
                 'abs': (lines[s][0], lines[a][0]), 'notes': notes}


def page_file_move(unit, info):
    """Find the same lines in exactly one page file; return (path, new text) or (None, reason)."""
    d = os.path.join(unit.dir, 'transcriptions')
    old = [info['salutation']] + info['date'] + info['between']
    found = []
    # The page's own file first, by the page id at the end of its name
    # ("..._0463_a.txt", "0003_a2.txt"): the firmest key, where there is one.
    names = sorted(os.listdir(d)) if os.path.isdir(d) else []
    own = [fn for fn in names if fn == info['page'] + '.txt' or fn.endswith('_' + info['page'] + '.txt')]
    if len(own) == 1:
        p = os.path.join(d, own[0])
        ls = io.open(p, encoding='utf-8', newline='').read().split(NL)
        strip = [l.rstrip('\r').strip() for l in ls]
        scored = []
        for i in range(len(strip) - len(old) + 1):
            rs = [difflib.SequenceMatcher(None, strip[i + k], old[k].strip()).ratio() for k in range(len(old))]
            scored.append((sum(rs) / len(rs), min(rs), i))
        scored.sort(reverse=True)
        # the best place must be good on every line and clearly the best
        nd0 = len(info['date'])

        def exact_core(i):
            # the date lines and the anchor word for word (letter 251: only its
            # salutation, "E h[?] d", differs from the expanded corpus form)
            return [x.strip() for x in strip[i + 1:i + 1 + nd0]] == [x.strip() for x in info['date']] and \
                strip[i + len(old) - 1] == old[-1].strip()
        cores = [i for _, _, i in scored if exact_core(i)]
        if len(cores) == 1 and cores[0] != (scored[0][2] if scored else None):
            scored.sort(key=lambda x: x[2] != cores[0])
        if scored and ((len(cores) == 1 and cores[0] == scored[0][2]) or
                       (scored[0][0] >= 0.75 and scored[0][1] >= 0.4 and
                        (len(scored) == 1 or scored[0][0] - scored[1][0] >= 0.15))):
            i = scored[0][2]
            for k in range(len(old)):
                if ls[i + k].strip() != old[k].strip():
                    info['notes'].append('the page file %s differs from corpus.txt: "%s" / corpus "%s"'
                                         % (own[0], ls[i + k].strip(), old[k].strip()))
            nd, nb = len(info['date']), len(info['between'])
            seg = ls[i + 1:i + 1 + nd + nb]
            ls[i + 1:i + 1 + nd + nb] = seg[nd:] + seg[:nd]
            return p, NL.join(ls)
        return None, 'the page file %s does not clearly hold these lines (best %.2f)' % (
            own[0], scored[0][0] if scored else 0)
    for fn in names:
        p = os.path.join(d, fn)
        raw = io.open(p, encoding='utf-8', newline='').read()
        ls = raw.split('\n')
        strip = [l.rstrip('\r') for l in ls]
        for i in range(len(strip) - len(old) + 1):
            if [x.strip() for x in strip[i:i + len(old)]] == [x.strip() for x in old]:
                found.append((p, ls, i))
    if not found:
        # The page file and corpus.txt can already differ by a correction made
        # in one only (2026-11-23: letter 182's "zu" stands as "z[u?]" in its
        # page file). Take the page file's own lines at the one place where
        # every line is nearly the same, and report each difference.
        near = []
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            ls = io.open(p, encoding='utf-8', newline='').read().split(NL)
            strip = [l.strip() for l in ls]
            for i in range(len(strip) - len(old) + 1):
                if all(difflib.SequenceMatcher(None, strip[i + k], old[k].strip()).ratio() >= 0.85
                       for k in range(len(old))):
                    near.append((p, ls, i))
        if len(near) != 1:
            return None, 'the page file under transcriptions/ holds these lines %d times, not once' % len(near)
        p, ls, i = near[0]
        for k in range(len(old)):
            if ls[i + k].strip() != old[k].strip():
                info['notes'].append('the page file %s differs from corpus.txt: "%s" / corpus "%s"'
                                     % (os.path.basename(p), ls[i + k].strip(), old[k].strip()))
        found = near
    if len(found) != 1:
        return None, 'the page file under transcriptions/ holds these lines %d times, not once' % len(found)
    p, ls, i = found[0]
    nd, nb = len(info['date']), len(info['between'])
    seg = ls[i + 1:i + 1 + nd + nb]
    ls[i + 1:i + 1 + nd + nb] = seg[nd:] + seg[:nd]
    return p, '\n'.join(ls)


def para_rows(unit, letter, info, rows, lines_after):
    """Held rows for the moved lines (DATE_ORDER_PLAN, Method 3)."""
    lo, hi = info['abs'][0] - 1, info['abs'][1] + 1

    def find(ctx):
        hit = [r for r in rows if r['letter'] == letter and r['context'] == ctx]
        if len(hit) > 1:
            # the same words twice in one document (letter 156: "1805." in the
            # letter and in its enclosure): the row inside this closing
            hit = [r for r in hit if str(r.get('line', '')).isdigit() and lo <= int(r['line']) <= hi]
        return hit
    d1 = info['date'][0].strip()[:70]
    old = find(d1)
    old_dec = old[0]['decision'] if old else 'run'
    nd, nb = len(info['date']), len(info['between'])
    s = info['s']
    want = []  # (index in lines_after, decision)
    want.append((s, old_dec))                         # the first closing line
    want.append((s + nb, 'break'))                    # the date, after the anchor
    for k in range(1, nd):
        want.append((s + nb + k, 'run'))              # its further lines joined
    # the line after the date (a postscript, a note), if on the same page, begins
    # a paragraph: it may have run on from the signature, and must not run on
    # into the date (letter 167, 2026-11-23)
    nxt = s + nb + nd + len(info.get('join') or [])
    if nxt < len(lines_after) and lines_after[nxt][1] == lines_after[s][1]:
        want.append((nxt, 'break'))
    # `join:` in the entry: lines that already stood after the anchor and belong
    # to the date (letter 151: the year after the signature), joined to it
    for k, t in enumerate(info.get('join') or [], 1):
        idx = s + nb + nd - 1 + k
        if idx >= len(lines_after) or lines_after[idx][2] != t:
            return 'the line to join, "%s", does not follow the date' % t
        want.append((idx, 'run'))
    for idx, dec in want:
        n, _, t = lines_after[idx]
        ctx, prev = t.strip()[:70], lines_after[idx - 1][2].strip()[:60]
        hit = find(ctx)
        if len(hit) > 1:
            return 'the line "%s" has %d rows in the paragraph sheet' % (ctx, len(hit))
        if hit:
            r = hit[0]
            r.update({'decision': dec, 'confidence': 'held', 'cue': 'hand', 'line': str(n), 'prev_line': prev})
        else:
            rows.append({'letter': letter, 'line': str(n), 'decision': dec, 'confidence': 'held', 'cue': 'hand',
                         'ratio': '0', 'prev_len': '0', 'page_measure': '0', 'prev_line': prev, 'context': ctx})
    return None


def move(unit, write):
    import csv
    spec = _yaml(os.path.join(unit.dir, 'intake', 'date_order.yml'))
    entries = spec.get('moves') or []
    if not entries:
        print('%s: no intake/date_order.yml entries' % unit.slug)
        return []
    corpus = io.open(unit.corpus_path, encoding='utf-8', newline='').read().split('\n')
    prows = _csv(os.path.join(unit.dir, 'paragraph_decisions.csv'))
    page_writes, done, changes = {}, [], []
    for ent in entries:
        letter = str(ent['letter'])
        docs = dict(documents_from(corpus))
        if letter not in docs:
            print('  !! %s: no document %s' % (unit.slug, letter))
            continue
        new, info = plan_move(unit, letter, docs[letter], ent, corpus)
        if new is not None:
            info['join'] = [str(x) for x in ent.get('join') or []]
        if new is None:
            print('  %s %s: %s' % ('--' if info == 'already moved' else '!!', letter, info))
            continue
        pf = page_file_move(unit, info) if os.path.isdir(os.path.join(unit.dir, 'transcriptions')) else (None, 'no page files')
        if pf[0] is None and pf[1] != 'no page files':
            print('  !! %s: %s' % (letter, pf[1]))
            continue
        after_docs = dict(documents_from(new))
        trial = [dict(r) for r in prows]
        bad = para_rows(unit, letter, info, trial, after_docs[letter])
        if bad:
            print('  !! %s: %s' % (letter, bad))
            continue
        corpus, prows = new, trial
        if pf[0]:
            page_writes[pf[0]] = pf[1]
        done.append(letter)
        changes.append({'importance': 'wording', 'new': '2026-11-23',
                        'what': 'Document %s, page %s: the date moved from between the closing\'s salutation and the '
                                'rest of the closing to after the signature (the editor, 2026-11-23: the date goes '
                                'after the signature). No word changed.' % (letter, info['page']),
                        'was': ' / '.join([info['salutation']] + info['date'] + info['between']),
                        'now': ' / '.join([info['salutation']] + info['between'] + info['date'])})
        print('  ok %s (%s): "%s" now after "%s"' % (letter, info['page'], ' / '.join(info['date']), ent['after']))
        for n in info['notes']:
            print('     note: ' + n)
    if write and done:
        with io.open(unit.corpus_path, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(corpus))
        for p, txt in page_writes.items():
            with io.open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(txt)
        with io.open(os.path.join(unit.dir, 'paragraph_decisions.csv'), 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=PCOLS, lineterminator='\n', extrasaction='ignore')
            w.writeheader()
            w.writerows(prows)
        write_changes(unit, changes)
    return done


def documents_from(corpus):
    out, cur, page = [], None, ''
    for n, t in enumerate(corpus, 1):
        s = t.strip()
        m = re.match(r'\[DOC (\S+)\]$', s)
        if m:
            cur = (m.group(1), [])
            out.append(cur)
            continue
        m = re.match(r'\[PAGE (\S+)\]$', s)
        if m:
            page = m.group(1)
            continue
        if cur is not None and s:
            cur[1].append((n, page, t.rstrip('\r')))
    return out


def write_changes(unit, changes):
    import yaml
    p = os.path.join(unit.dir, 'intake', 'changes.yml')
    if os.path.isfile(p):
        raw = io.open(p, encoding='utf-8').read().rstrip('\n') + '\n'
    else:
        raw = ('# What changed in the transcription, for the page of changes\n'
               '# (pipeline/review/changes_page.py). importance: significant | fact | wording.\n\n'
               'unit: "%s"\nchanges:\n' % unit.get('title', unit.slug).replace('"', "'"))
    body = yaml.safe_dump(changes, allow_unicode=True, sort_keys=False, width=1000)
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(raw + body)


# ---- nothing else may change (Method 4) ------------------------------------------

FIELDS = ('date_iso', 'date_precision', 'date_display', 'date_source', 'place', 'sender', 'recipient',
          'n_pages', 'n_lines', 'uncertainty_count', 'estates', 'relations', 'language', 'doc_type')


def snapshot(unit):
    recs = json.load(io.open(os.path.join(ROOT, 'dataset', 'units', unit.slug, 'letters.json'), encoding='utf-8'))
    out = {}
    for r in recs:
        d = {k: r.get(k) for k in FIELDS}
        d['lines'] = sorted(l for p in r['pages'] for l in p['diplomatic'].split('\n'))
        # the reading text's words, counted: a move changes their order and
        # paragraphs, never the words (2026-11-23)
        d['reading_words'] = sorted(w for p in r['pages'] for w in p.get('reading', '').split())
        out[str(r['letter_id'])] = d
    return out


def restamp(unit, letters):
    """The cached English was made from the same words in another order: stamp it current."""
    tag = str(unit.get('published_tag') or '')
    saved = sys.argv[:]
    sys.argv = ['translate.py', '--unit', unit.slug]
    sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'translate'))
    import translate
    sys.argv = saved
    recs = {str(r['letter_id']): r for r in
            json.load(io.open(os.path.join(ROOT, 'dataset', 'units', unit.slug, 'letters.json'), encoding='utf-8'))}
    for lid in letters:
        p = translate.out_path(lid, tag or None)
        if not os.path.isfile(p):
            print('  %s: no cached translation at %s' % (lid, os.path.relpath(p, ROOT)))
            continue
        d = json.load(io.open(p, encoding='utf-8'))
        d['source_hash'] = translate.source_hash(recs[lid])
        d['source_note'] = 'restamped 2026-11-23: the date moved after the signature, no word changed'
        with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print('  %s: restamped' % lid)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    units = unitlib.load_units(unitlib.unit_arg())
    snapdir = os.path.join(ROOT, 'review', 'date_order')
    os.makedirs(snapdir, exist_ok=True)
    if '--move' in sys.argv:
        for u in units:
            done = move(u, '--write' in sys.argv)
            print('%s: %d document(s) %s' % (u.slug, len(done), 'moved' if '--write' in sys.argv else 'would move'))
        return
    if '--snapshot' in sys.argv or '--compare' in sys.argv:
        for u in units:
            p = os.path.join(snapdir, 'snapshot_%s.json' % u.slug)
            now = snapshot(u)
            if '--snapshot' in sys.argv:
                json.dump(now, io.open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False)
                print('%s: %d documents recorded' % (u.slug, len(now)))
                continue
            was = json.load(io.open(p, encoding='utf-8'))
            diffs = [(lid, k, was[lid].get(k), now.get(lid, {}).get(k)) for lid in was for k in was[lid]
                     if now.get(lid, {}).get(k) != was[lid].get(k)]
            if set(now) != set(was):
                diffs.append(('*', 'documents', sorted(was), sorted(now)))
            for d in diffs:
                print('  !! %s %s: %r -> %r' % d)
            print('%s: %s' % (u.slug, 'nothing else changed' if not diffs else '%d difference(s)' % len(diffs)))
        return
    if '--restamp' in sys.argv:
        letters = [a for a in sys.argv[sys.argv.index('--restamp') + 1].split(',')]
        for u in units:
            restamp(u, letters)
        return
    cases = scan(units)
    out = os.path.join(ROOT, 'review', 'date_order')
    os.makedirs(out, exist_ok=True)
    with io.open(os.path.join(out, 'candidates.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(cases, f, ensure_ascii=False, indent=1)
    md = ['# Dates followed by more text at the end of a document', '']
    for c in cases:
        md.append('## %s %s (%s) - %s' % (c['unit'], c['letter'], c['page'],
                                          'regular' if c['regular'] else 'IRREGULAR'))
        for w in c['why']:
            md.append('- ' + w)
        md.append('```')
        dl = {n for n, _ in c['date_lines']}
        md += ['%s %6d  %s' % ('>' if n in dl else ' ', n, t) for n, t in c['window']]
        md.append('```')
        md.append('')
    with io.open(os.path.join(out, 'candidates.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md))
    by = {}
    for c in cases:
        k = by.setdefault(c['unit'], [0, 0])
        k[0 if c['regular'] else 1] += 1
    print('%d cases in %d documents: %d regular, %d irregular' % (
        len(cases), len({c['pad'] for c in cases}), sum(c['regular'] for c in cases),
        sum(not c['regular'] for c in cases)))
    for u, (r, i) in sorted(by.items(), key=lambda x: -sum(x[1])):
        print('  %-24s regular %3d  irregular %3d' % (u, r, i))
    print('review/date_order/candidates.md')


if __name__ == '__main__':
    main()
