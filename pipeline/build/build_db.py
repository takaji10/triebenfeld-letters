# -*- coding: utf-8 -*-
"""Build the research database + chronological reading copy."""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import re, io, sys, json, csv, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus_pages import build_pages, load_decisions, PAGE_TAG
import unitlib
import schema
import sys

OUT = ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
# Each unit builds into its own directory; merge_corpus.py combines them into
# the corpus/ files the website and the review tools read.
UNIT_OUT = os.path.join(ROOT, 'corpus', 'units', UNIT.slug)
UNIT_REVIEW = os.path.join(ROOT, 'review', UNIT.slug)
os.makedirs(UNIT_OUT, exist_ok=True)
os.makedirs(UNIT_REVIEW, exist_ok=True)
SRC = UNIT.corpus_path
with open(SRC, encoding='utf-8') as f:
    lines = f.read().split('\n')

tag = re.compile(r'^\[DOC (\w+)\]$')
pos = {}
for i, l in enumerate(lines):
    m = tag.match(l.strip())
    if m: pos[m.group(1)] = i + 1

def sortkey(Lid):
    m = re.match(r'(\d+)([a-z]*)', Lid)
    return (int(m.group(1)), m.group(2))

nums = sorted(pos, key=sortkey)
bounds = {}
for i, L in enumerate(nums):
    end = pos[nums[i+1]] - 1 if i + 1 < len(nums) else len(lines)
    bounds[L] = (pos[L], end)
print(f"letters tagged: {len(nums)}  ({nums[0]}..{nums[-1]})")

def parent_of(Lid):
    m = re.match(r'(\d+)([a-z]*)', Lid)
    return m.group(1) if m.group(2) else ''

# ---------------- date parsing (v2, anchored on the year's own line) -------------
MONTHS = [(r'jan',1),(r'febr|feb',2),(r'm[äae]r[zc]|mrz',3),(r'apr',4),
          (r'ma[jiy]',5),(r'jun',6),(r'jul',7),(r'aug',8),
          (r'sept|sep|7br',9),(r'o[ck]tob|o[ck]t|8br',10),
          (r'novemb|novb|nov|9br',11),(r'de[cz]emb|decb|de[cz]|xbr|10br',12)]
YEAR = re.compile(r'(?<!\d)(1[78]\d\d)(?!\d)')
# Towns this project has met, used only to score a candidate dateline: a line
# that names one is likelier to be a dateline than one that does not. It is a
# hint, never an authority - the place itself is read off the dateline below,
# and a town not listed here costs nothing but three points.
# pipeline-check: a scoring hint, and a holding whose towns are absent loses
# nothing by it
PLACE_RE = re.compile(r'(Berlin|Breslau|Wien|Kontop|Glogau|Posen|Kalisz|Schlawenschitz|'
                      r'Trąbczyn|Zagorow\w*|Blizanow|Peisern|Kempen|Erfurt|Dresden|'
                      r'Öhringen|Paris|Franckfurth|Frankfurt|Neisse|Warschau|Küstrin|Betsche)', re.I)

# --- place of writing ------------------------------------------------------
# Derived from the DATELINE, not by scanning the closing prose for a known town.
# The old whitelist approach matched any listed name anywhere in the last 15
# lines, so "wider nach Neisse" one line above the real dateline "Blizanow" won,
# and towns not on the list produced nothing at all.
#
# The dateline takes two shapes:
#   "Breslau den 1ten Febr. 1799."      place and date on one line
#   "Kalisz" / "d. 29ten April"          place on its own line above the date
# Polish and some German letters put it at the head instead of the foot.

_MONTH = (r'Jan(?:uar|\.)?|Feb(?:r(?:uar)?|\.)?|M(?:ä|ae|a)r(?:z|tz|tii|\.)?|'
          r'Apr(?:il+|\.)?|May|Mai|Jun[iy]|Jul[iy]|Aug(?:ust|\.)?|'
          r'Sept?(?:br|ember|\.)?|Oct(?:br|ober|\.)?|Nov(?:br|ember|\.)?|'
          r'Dec(?:br|ember|\.)?|Xbr|7br|8br|9br|10br|11br|12br')
DATELINE = re.compile(r'\b(?:d\.?|den|dem|dnia)\s*\d{1,2}\s*(?:t|te|ten|tn|\.)?\b'
                      r'|\b(?:' + _MONTH + r')\b', re.I)
# closing/signature vocabulary - marks a line as not a place
PLACE_NOISE = re.compile(
    r'\b(?:diener|knecht|treu\w*|unterth\w*|gehorsam\w*|ergeben\w*|durchlaucht|'
    r'ewr|euer|ehrfurcht|hochachtung|ersterbe|verharren|freund|fürst|herr\w*|'
    r'hochwohlgeb\w*|submission|respect|nachschrift|bekomme|sorgen|übrigens|'
    r'rthl|thl|capital|zinsen)\b', re.I)

# Manuscript spellings -> the canonical form. Extraction stays faithful to the
# page; normalisation happens here, so both remain inspectable.
# ---------------- editorial rulings ----------------
# Decisions live in units/<slug>/rulings.yml, keyed by the archive's own
# document number, and the place canon is shared in reference/places.yml.
# Adding a unit means writing those files, not editing this one.
_R = unitlib.load_rulings(UNIT)
PLACE_CANON     = _R['PLACE_CANON']
PLACE_REJECT    = _R['PLACE_REJECT']
PLACE_OVERRIDE  = _R['PLACE_OVERRIDE']
SUPPLIED        = _R['SUPPLIED']
DATE_READ       = _R['DATE_READ']
TWIN            = _R['TWIN']
NO_DATE         = _R['NO_DATE']
DOC_TYPE        = _R['DOC_TYPE']
DOC_LANGUAGE    = _R['DOC_LANGUAGE']
INFERRED        = _R['INFERRED']
DUP_OF          = _R['DUP_OF']
SPLIT_NOTE      = _R['SPLIT_NOTE']
DAMAGE_LETTERS  = _R['DAMAGE_LETTERS']
RELATIONS       = _R['RELATIONS']
# Readings too corrupt to be a place. Blanked and sent to the review list.

# Your rulings. These win over anything derived.


# Sender and recipient, derived from the salutation and signature by
# derive_correspondents.py. Only readings it was confident about are taken:
# an unsigned letter stays unattributed rather than being guessed at, even
# where one correspondent would be overwhelmingly likely.
def load_correspondents():
    p = os.path.join(UNIT.dir, 'correspondents.json')
    if not os.path.isfile(p):
        return {}
    out = {}
    for lid, d in json.load(open(p, encoding='utf-8')).items():
        if d.get('confidence') in ('high', 'body'):
            out[lid] = (d.get('sender', ''), d.get('recipient', ''))
    return out


CORRESPONDENTS = load_correspondents()


def extract_place(body):
    """(place, how). '' where the letter names no place of writing."""
    idx = [i for i, l in enumerate(body) if l.strip()]
    if not idx:
        return '', 'empty'
    fallback = None  # first "found a date but no place" reason, for reporting
    for window, where in ((idx[-14:], 'foot'), (idx[:6], 'head')):
        for i in (reversed(window) if where == 'foot' else window):
            line = body[i].strip()
            m = DATELINE.search(line)
            if not m:
                continue
            short = len(line) <= 64
            head = line[:m.start()].strip(' ,.;:-–—')
            head = re.sub(r'^(?:w|in|zu|aus)\s+', '', head, flags=re.I)  # "w Warszawie"
            if head.startswith('[') and head.endswith(']'):
                # A wholly-bracketed guess like "[Wien]" - unwrap it, but only
                # when the brackets wrap the whole head. A partial bracket
                # like "Bre[slau?]" or "B[erlin?]" must be left alone: it is
                # PLACE_CANON's own key for that uncertain reading, and
                # stripping the brackets here would break that lookup below.
                head = head[1:-1]
            # A bare day-number ("16ten", "2[9?]") before a month abbreviation
            # like "8br." matched via the MONTH alternative, not the "d./den"
            # one - head is then just the ordinal, not a place. Treat it as
            # empty so the line-above check below still runs. Foot only: at
            # the head of a letter this fires on document-type openers like
            # "P[ro]. M[emoria]." above "26. Juni 1812", which pass the
            # line-above checks (short, capitalised, no digit) despite being
            # a heading, not a place - the head-position "place above date"
            # letters already work via the "d./den" prefix branch, so nothing
            # is lost by not covering the bare-month case there too.
            if where == 'foot' and re.fullmatch(r'[\d\[\]?]{1,6}(?:t|te|ten|tn)?\.?', head):
                head = ''
            if short and head and not PLACE_NOISE.search(head) and re.match(r'^[A-ZÄÖÜ]', head):
                return re.sub(r'\s+', ' ', head), where + ':same line'
            if head and ',' in head:
                # "v. Triebenfeld, Breslau den 2ten April 1804" - signer's name
                # before the comma, place after it, both on the dateline. Kept
                # even when the whole line runs long (prose and dateline often
                # share one line with no break, e.g. "...erhalten. - v.
                # Triebenfeld, Breslau den 2ten April 1804"), unlike the plain
                # same-line case above which needs the line to be just the
                # dateline.
                tail_seg = head.rsplit(',', 1)[-1].strip()
                if (tail_seg and not PLACE_NOISE.search(tail_seg)
                        and re.match(r'^[A-ZÄÖÜ][^\W\d_]*$', tail_seg)):
                    return tail_seg, where + ':same line, after signer'
            if not short:
                continue
            if not head:
                for j in range(i - 1, max(-1, i - 3), -1):
                    prev = body[j].strip() if j >= 0 else ''
                    if not prev:
                        continue
                    if (len(prev) <= 34 and re.match(r'^[A-ZÄÖÜ]', prev)
                            and not PLACE_NOISE.search(prev)
                            and not DATELINE.search(prev)
                            and not re.search(r'\d', prev)):
                        return re.sub(r'\s+', ' ', prev.strip(' ,.;:-')), where + ':line above'
                    break
            # Keep scanning the rest of the window rather than giving up here:
            # a postscript's own incidental date ("die Rükkunft nach Breslau
            # ist ohnfehlbar d 25ten bestimmt!") can sit closer to the end of
            # the letter than the real "Place den Date" + signature above it,
            # and used to shadow it by returning empty on the first match.
            if fallback is None:
                fallback = where + ':date, no place'
    return '', (fallback or 'no dateline')


def resolve_place(letter_id, body):
    """(place, how). Override -> extract -> normalise -> reject."""
    if letter_id in PLACE_OVERRIDE:
        return PLACE_OVERRIDE[letter_id], 'ruling'
    raw, how = extract_place(body)
    if not raw:
        return '', how
    key = raw.lower().strip(' .')
    if key in PLACE_REJECT:
        return '', 'unreadable: ' + raw
    return PLACE_CANON.get(key, raw), how


def month_in(s):
    low, best = s.lower(), None
    for pat, num in MONTHS:
        m = re.search(r'(?<![a-zäöüſ])(' + pat + r')', low)
        if m and (best is None or m.start() < best[1]): best = (num, m.start())
    return best

def day_near(s, mpos):
    pre = s[:mpos].rstrip()
    for pat in (r'(?<!\d)(\d{1,2})\s*(?:t[ei]?[nm]|te|\.)?\s*$',
                r'den\s+(\d{1,2})\s*(?:t[ei]?[nm]|te)?\s*\.?\s*$',
                r'd\.?\s*(\d{1,2})\s*(?:t[ei]?[nm]|te)?\s*\.?\s*$'):
        m = re.search(pat, pre, re.I)
        if m: return int(m.group(1))
    return None

def score(text, in_tail):
    s = 0
    if len(text.strip()) <= 45: s += 3
    if PLACE_RE.search(text): s += 3
    if re.search(r'\bden\b|\bd\.\s*\d|\bd\s+\d', text, re.I): s += 2
    if in_tail: s += 4
    if re.search(r'zinsen|capital|Rthl|schuld|contract|vom\s+\d', text, re.I): s -= 4
    return s

def parse_letter(L):
    s, e = bounds[L]
    idxs = [j for j in range(s+1, e+1) if lines[j-1].strip()]
    if not idxs: return None
    tail = set(idxs[-12:]); cands = []
    for j in idxs:
        t = lines[j-1]
        for ym in YEAR.finditer(t):
            year = int(ym.group(1))
            if not (1780 <= year <= 1820): continue
            mon = day = None
            mi = month_in(t)
            if mi:
                mon, mp = mi; day = day_near(t, mp)
            else:
                for nb in (j-1, j+1, j-2, j+2):
                    if s < nb <= e and lines[nb-1].strip():
                        mi2 = month_in(lines[nb-1])
                        if mi2:
                            mon, mp = mi2; day = day_near(lines[nb-1], mp); break
            sc = score(t, j in tail) + (2 if mon else 0) + (1 if day else 0)
            cands.append((sc, j, year, mon, day))
    if not cands: return None
    cands.sort(key=lambda c: (-c[0], -c[1]))
    sc, j, year, mon, day = cands[0]
    if day is not None and not (1 <= day <= 31): day = None
    return (year, mon, day, j)

parsed = {L: parse_letter(L) for L in nums}

# ---------------- user-supplied + derived dates ----------------

MN = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
def iso(y, m, d):
    if y is None: return ''
    if m is None: return f"{y:04d}"
    if d is None: return f"{y:04d}-{m:02d}"
    try: datetime.date(y, m, d); return f"{y:04d}-{m:02d}-{d:02d}"
    except ValueError: return f"{y:04d}-{m:02d}"

DECISIONS = load_decisions(os.path.join(UNIT.dir, 'linebreak_decisions.csv'))


def load_paragraphs(path):
    """Absolute line numbers that begin a paragraph, from resolve_paragraphs.py.

    Absent file means no paragraph structure yet: every page then comes back as
    one block, exactly as it did before this existed.
    """
    out = set()
    if not os.path.isfile(path):
        return out
    import csv as _csv
    with open(path, encoding='utf-8-sig', newline='') as f:
        for row in _csv.DictReader(f):
            if (row.get('decision') or '').strip() == 'break':
                try:
                    out.add(int(row['line']))
                except (KeyError, ValueError):
                    pass
    return out


PARAS = load_paragraphs(os.path.join(UNIT.dir, 'paragraph_decisions.csv'))
print(f'paragraph breaks loaded: {len(PARAS)}')
print(f"line-break decisions loaded: {len(DECISIONS)}")

records = []
PLACE_TRACE = []   # (letter_id, place, how) - feeds place_review.md
for L in nums:
    s, e = bounds[L]
    # A [PAGE ...] marker declares which manuscript page the lines below it came
    # from. It is structure, not transcription, so it is stripped out of the
    # archival text here and never reaches the record, the site or the exports;
    # split_pages() has already read it by the time this matters.
    body = [l for l in (lines[j-1] for j in range(s+1, e+1))
            if not PAGE_TAG.match(l.strip())]
    text = '\n'.join(body).strip('\n')
    # Page structure: (abs_line_no, text) so every page keeps its archival range.
    numbered = [(j, lines[j-1]) for j in range(s+1, e+1)]
    pages = build_pages(numbered, L, DECISIONS,
                        is_register=(DOC_TYPE.get(L, 'letter') == 'register'),
                        paras=PARAS)
    text_reading = '\n\n'.join(p['reading'] for p in pages if p['reading'])
    missing = text.strip() == '(missing)' or text.strip() == '(skipped)'
    y = m = d = None; prec = 'unknown'; srcv = 'none'; basis = ''; dline = ''
    if L in NO_DATE:
        prec, srcv = 'unknown', 'none'
        # Derived from the document's own kind, not from its number: L == '303'
        # named one holding's register and said nothing about any other.
        basis = ('register/ledger document, no date given in the source'
                 if DOC_TYPE.get(L) == 'register'
                 else 'letter missing/skipped in the archive')
    elif L in SUPPLIED:
        y, m, d, prec = SUPPLIED[L]; srcv = 'supplied'; basis = 'supplied by researcher'
    elif L in DATE_READ:
        y, m, d, prec = DATE_READ[L]; srcv = 'dateline'
        basis = "read from the document's own dateline"
    elif L in TWIN:
        y, m, d, prec = TWIN[L]; srcv = 'twin'
        # Name the actual twin. This used to read "same document as letter 48"
        # for every twinned date in the project.
        _tw = DUP_OF.get(L) or next((k for k, v in DUP_OF.items() if v == L), '')
        basis = f'same document as {_tw}' if _tw else 'same document as its duplicate'
    elif L in INFERRED:
        y, m, d, prec, basis = INFERRED[L]; srcv = 'inferred'
    else:
        p = parsed.get(L)
        if p:
            y, m, d, j = p; srcv = 'signature'; dline = lines[j-1].strip()[:70]
            prec = 'day' if d else ('month' if m else 'year')
    # place of writing - from the dateline; see resolve_place above
    place, place_how = resolve_place(L, [t for _, t in numbered])
    PLACE_TRACE.append((L, place, place_how))
    unc = len(re.findall(r'\[\?\]|\[\.\.\.\]|\[[^\]]{1,12}\?\]', text))
    parent = parent_of(L)
    note = SPLIT_NOTE.get(L, '')
    records.append(dict(
        letter_id=L, seq_archival=nums.index(L)+1, parent_letter=parent,
        unit=UNIT.slug, uid=UNIT.uid(L), pad=UNIT.pad(L),
        permalink=UNIT.permalink(L),
        doc_type=DOC_TYPE.get(L, 'letter'),
        date_iso=iso(y,m,d), date_precision=prec, date_source=srcv,
        # Brackets mean "not read from the document". A `dateline` date WAS
        # read from it - the parser simply could not reach it - so it shows
        # plain. Without this branch it fell through to `dline`, which is empty
        # for those, and every such document announced itself as undated.
        date_display=(f"[{iso(y,m,d)}]" if srcv in ('inferred', 'supplied', 'twin')
                      else (iso(y, m, d) if srcv == 'dateline' else dline)),
        date_inferred_from=(basis or note),
        year=y or '', month=m or '', day=d or '',
        place=place,
        sender=CORRESPONDENTS.get(L, ('', ''))[0],
        recipient=CORRESPONDENTS.get(L, ('', ''))[1],
        line_start=s, line_end=e,
        uncertainty_count=unc,
        has_damage=int('[...]' in '\n'.join(body) or L in DAMAGE_LETTERS),
        language=DOC_LANGUAGE.get(L, 'de'),
        duplicate_of=DUP_OF.get(L, ''),
        # Typed links to other documents in this holding. Editorial assertions,
        # each recorded in rulings.yml with the evidence for it.
        relations=RELATIONS.get(L, []),
        is_missing=int(missing),
        n_lines=len(body), n_pages=len(pages),
        text=text, text_reading=text_reading, pages=pages))

print(f"records: {len(records)}")
from collections import Counter
print("date_source:", Counter(r['date_source'] for r in records))
print("precision  :", Counter(r['date_precision'] for r in records))
undated = [r['letter_id'] for r in records if not r['date_iso']]
print("still undated:", undated)

# ---------------- write outputs ----------------
# CSV carries the flat fields (pages are nested, so JSON only).
cols = schema.DOCUMENT_FLAT_FIELDS
with open(os.path.join(UNIT_OUT, 'letters.csv'),'w',encoding='utf-8-sig',newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in records: w.writerow(r)
with open(os.path.join(UNIT_OUT, 'letters.json'),'w',encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=1)

# Page-level table: one row per manuscript page, for scan matching later.
with open(os.path.join(UNIT_OUT, 'pages.csv'),'w',encoding='utf-8-sig',newline='') as f:
    w = csv.writer(f)
    w.writerow(schema.PAGE_FLAT_FIELDS)
    for r in records:
        for p in r['pages']:
            w.writerow([r['letter_id'], p['page'], p['line_start'], p['line_end'],
                        p['n_lines'], p['scan'], p['reading']])
print(f"pages: {sum(len(r['pages']) for r in records)}")

# Reading copy - generated, page by page, each labelled with its archival lines.
with open(os.path.join(UNIT_OUT, 'reading.txt'),'w',
          encoding='utf-8',newline='\n') as f:
    f.write(f"{UNIT.get('ref') or UNIT.slug} - READING COPY (generated)\n")
    f.write("Line-wraps resolved for readability. Page breaks preserved; each page is\n")
    f.write("labelled with its line range in the archival file, which stays canonical.\n")
    f.write("Do not edit this file - edit the archival text or linebreak_decisions.csv.\n\n\n")
    for r in records:
        f.write(f"[DOC {r['letter_id']}]")
        if r['date_iso']: f.write(f"  {r['date_iso']}")
        if r['place']: f.write(f"  {r['place']}")
        f.write("\n")
        for p in r['pages']:
            f.write(f"\n[page {p['page']} | archival lines {p['line_start']}-{p['line_end']}]\n")
            f.write(p['reading'] + "\n")
        f.write("\n\n")

# review table (no full text)
with open(os.path.join(UNIT_REVIEW, 'parsed_dates_review.csv'),'w',encoding='utf-8-sig',newline='') as f:
    w = csv.writer(f)
    w.writerow(['letter_id','date_iso','precision','source','basis_or_dateline','place','n_lines'])
    for r in records:
        w.writerow([r['letter_id'], r['date_iso'], r['date_precision'], r['date_source'],
                    r['date_inferred_from'] or r['date_display'], r['place'], r['n_lines']])

# chronological reading copy
def sortkey(r):
    if not r['date_iso']: return (1, 9999, 99, 99, r['letter_id'])
    y = int(r['date_iso'][:4]); m = int(r['date_iso'][5:7]) if len(r['date_iso'])>=7 else 0
    d = int(r['date_iso'][8:10]) if len(r['date_iso'])>=10 else 0
    return (0, y, m, d, r['letter_id'])
chron = sorted(records, key=sortkey)
with open(os.path.join(UNIT_OUT, 'chronological.txt'),'w',
          encoding='utf-8',newline='\n') as f:
    f.write(f"{UNIT.get('ref') or UNIT.slug} - CHRONOLOGICAL ORDER\n")
    f.write("Derived from the archival-order file. [DOC n] = archival number (citation key).\n")
    f.write("Dates in [brackets] are supplied or inferred, not read from the letter.\n\n\n")
    # carry over the original title page (sits before letter 1, so outside all bounds)
    front = '\n'.join(lines[:pos[nums[0]]-1]).strip('\n')
    if front.strip():
        f.write(front + "\n\n\n")
    for r in chron:
        disp = r['date_display'] if r['date_display'] else '(no date)'
        if r['date_source'] == 'signature' and r['date_iso']:
            disp = r['date_iso'] + '  |  ' + r['date_display']
        f.write(f"[DOC {r['letter_id']}]  {disp}\n")
        f.write(r['text'] + "\n\n\n")
print("wrote letters.csv / letters.json / parsed_dates_review.csv / chronological.txt")

# ---------------- verification ----------------
def content(fn):
    with open(fn, encoding='utf-8') as fh:
        return sorted(l.strip() for l in fh
                      if l.strip()
                      and not re.match(r'^\[DOC \w+\]', l.strip())
                      and not PAGE_TAG.match(l.strip()))
a = content(SRC)
b = content(os.path.join(UNIT_OUT, 'chronological.txt'))
b = [x for x in b if not x.startswith((f"{UNIT.get('ref') or UNIT.slug} -",
                                       'Derived from the archival',
                                       'Dates in [brackets]'))]

# --- place-of-writing review list ------------------------------------------
# Everything the dateline heuristic could not settle, listed for adjudication.
# A blank is frequently correct - plenty of these letters simply never say where
# they were written - so the point is to make the absence a decision rather than
# an oversight.
_open = [(L, how) for L, pl, how in PLACE_TRACE if not pl]
_ruled = sum(1 for L, pl, how in PLACE_TRACE if how == 'ruling')
_derived = sum(1 for L, pl, how in PLACE_TRACE if pl and how != 'ruling')
_byid = {str(r['letter_id']): r for r in records}  # pipeline-check: records is this unit's only
_lines = [
    '# Place of writing - needs review',
    '',
    "Derived from each letter's own dateline (`Blizanow d 8ten Nov.`), not by",
    'scanning the closing prose for a known town name - the old whitelist matched',
    '`wider nach Neisse` one line above the real dateline `Blizanow`, and returned',
    'nothing at all for towns it did not list. Manuscript spellings are normalised',
    'after extraction, so what is on the page stays inspectable.',
    '',
    f'- **{_ruled}** set by explicit ruling',
    f'- **{_derived}** derived from a dateline',
    f'- **{len(_open)}** with no place found, listed below',
    '',
    'A blank is often the correct answer. These are listed so that absence is a',
    'decision rather than an oversight.',
    '',
    '| Letter | Why nothing was found | Closing lines |',
    '|---|---|---|',
]
for _L, _how in _open:
    _r = _byid.get(_L)
    _tail = ''
    if _r:
        _bl = [x.strip() for x in _r['text'].split('\n') if x.strip()][-3:]
        _tail = ' / '.join(_bl)[:110].replace('|', '/')
    _lines.append(f'| {_L} | {_how} | {_tail} |')
with open(os.path.join(UNIT_REVIEW, 'place_review.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(_lines) + '\n')
print(f'place: {_ruled} ruled, {_derived} derived, '
      f'{len(_open)} unresolved -> place_review.md')

# --- page + reading-copy verification -------------------------------------
# 1. Pages must reconstruct the archival text of every letter exactly.
# 2. The reading copy must contain the same letters, in the same order, as the
#    archival text - the only permitted losses are the wrap marks themselves and
#    the catchword fragments we deliberately drop.
ALPHA = re.compile(r'[^A-Za-zÀ-ÿĄąĘęŁłŃńÓóŚśŹźŻżſ]+')
def alpha(s): return ALPHA.sub('', s).replace('ſ', 's').lower()

bad_pages = bad_reading = 0
catchword_pages = 0
for r in records:
    if not r['pages']:
        continue
    rebuilt = '\n\n'.join(p['diplomatic'] for p in r['pages'])
    if alpha(rebuilt) != alpha(r['text']):
        bad_pages += 1
        print(f"  PAGE MISMATCH letter {r['letter_id']}")
    for p in r['pages']:
        # A catchword is dropped from the reading text on purpose, so the page
        # cannot be compared as it stands. Where the catchword is a whole line -
        # the unmarked kind - we know exactly what was dropped and can take it
        # off the archival side too, which keeps the page inside the check. Only
        # the marked kind, where part of a line goes, is still exempt: there the
        # fragment cannot be reconstructed from the decision alone.
        dip_lines, exempt = [], False
        for ln, txt in zip(range(p['line_start'], p['line_end'] + 1),
                           p['diplomatic'].split('\n')):
            if DECISIONS.get((r['letter_id'], ln)) != 'catchword':
                dip_lines.append(txt)
                continue
            t = txt.rstrip()
            if t.endswith('¬') or (re.search(r'\w-$', t) and not t.endswith('--')):
                exempt = True             # marked: part of a line goes
                break
            # unmarked: the whole line goes, so simply leave it out
        if exempt:
            catchword_pages += 1
            continue
        if alpha('\n'.join(dip_lines)) != alpha(p['reading']):
            bad_reading += 1
            if bad_reading <= 5:
                print(f"  READING MISMATCH letter {r['letter_id']} page {p['page']}")

# 3. The transcription layer keeps the manuscript's lines. It may differ from
#    the archival text ONLY on lines carrying a recorded decision, and only in
#    the line-end mark - never in a word.
bad_trans = 0
for r in records:
    for p in r['pages']:
        # NB: distinct names - `a`/`b` below hold the archival/chronological
        # comparison, and shadowing them silently voids that check.
        arch_lines = p['diplomatic'].split('\n')
        tran_lines = p['transcription'].split('\n')
        if len(arch_lines) != len(tran_lines):
            bad_trans += 1
            print(f"  TRANSCRIPTION line count differs, letter {r['letter_id']} p{p['page']}")
            continue
        for k, (x, y) in enumerate(zip(arch_lines, tran_lines)):
            if x.rstrip() == y:
                continue
            lineno = p['line_start'] + k
            dec = DECISIONS.get((r['letter_id'], lineno), '')
            expected = (x.rstrip()[:-1] + '-') if dec == 'join' else x.rstrip()[:-1].rstrip()
            if not dec or y != expected:
                bad_trans += 1
                if bad_trans <= 5:
                    print(f"  TRANSCRIPTION unexpected change at line {lineno}: "
                          f"{x!r} -> {y!r} (decision {dec!r})")

print(f"\nVERIFY transcription differs only where decided : {bad_trans == 0}")
assert bad_trans == 0, "the transcription layer changed something it should not have"

print(f"VERIFY pages reconstruct letters : {bad_pages == 0}")
print(f"VERIFY reading copy lossless     : {bad_reading == 0} "
      f"({catchword_pages} catchword page(s) excluded by design)")
assert bad_pages == 0, "page split lost text"
assert bad_reading == 0, "reading copy altered the text"

print(f"\nVERIFY archival content lines : {len(a)}")
print(f"VERIFY chronological lines    : {len(b)}")
print(f"VERIFY identical content      : {a == b}")
# Convenience dump for hand checking. Keyed by uid and written under the
# unit's own review folder: it used to be keyed by archival number and dropped
# in whatever directory the build happened to run from, which two units share.
json.dump({r['uid']: r['date_iso'] for r in records},
          open(os.path.join(UNIT_REVIEW, "final_dates.json"), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
