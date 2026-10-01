# -*- coding: utf-8 -*-
"""
Page structure and the generated reading text.

A document is a sequence of manuscript pages. Each page carries three views:

    diplomatic  - the archival lines, exactly as transcribed        [canonical]
    reading     - lines flowed together, wraps resolved             [generated]
    translation - English                                           [added later]

plus a `scan` slot for the page image, empty for now.

Reading text NEVER flows across a page break, so text always stays alongside the
right scan and the page breaks stay visible.

Whether a line-end mark really joins two halves of a word is decided in
resolve_linebreaks.py and recorded in linebreak_decisions.csv, which is
hand-editable. This module only applies those decisions.

Where a page break falls is decided here, and there are two mechanisms. A
`[PAGE <id>]` marker on its own line names the manuscript page the lines below
it come from; that is a declaration, carried through to the database as the
page's citable identity and used to pair it with its scan. Older units have no
markers and mark their breaks with a blank line instead, so both are supported
and the marker wins wherever it appears. Mixing them within one document is an
error, because it would mean the page boundaries were being asserted twice by
mechanisms that can disagree.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import os, re, csv
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# The caller passes the unit's decisions file; this module is imported by
# build_db.py and has no business choosing a unit of its own.
DECISIONS = None

WORD = re.compile(r'[A-Za-zÀ-ÿĄąĘęŁłŃńÓóŚśŹźŻżſ]+')


def load_decisions(path=None):
    """(letter_id, line_no) -> decision. Missing file means 'join nothing'."""
    out = {}
    if not path or not os.path.isfile(path):
        return out
    with open(path, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            out[(row['letter'], int(row['line']))] = row['decision'].strip()
    return out


PAGE_TAG = re.compile(r'^\[PAGE ([^\]\s][^\]]*)\]$')


def load_sideways(path, lines, bounds):
    """Absolute line numbers of text written sideways on the page.

    units/<slug>/sideways.yml names each block by its letter, its first line
    (exactly as it stands in corpus.txt) and its length. The text itself is
    ordinary corpus text; this only says which lines were written sideways, so
    the site can set them apart rather than let them read as if they ran on in
    order. Keyed by text rather than line number, so edits elsewhere in the
    corpus do not move it. A block that cannot be found stops the build: a
    silent miss would publish the text unmarked.
    """
    out = set()
    if not path or not os.path.isfile(path):
        return out
    import yaml
    for b in (yaml.safe_load(open(path, encoding='utf-8')) or {}).get('blocks') or []:
        s, e = bounds[str(b['letter'])]
        hits = [j for j in range(s + 1, e + 1) if lines[j - 1] == b['first']]
        if len(hits) != 1:
            sys.exit(f'{os.path.basename(path)}: letter {b["letter"]}: first line found '
                     f'{len(hits)} times: {b["first"]!r}')
        block = range(hits[0], hits[0] + int(b['lines']))
        if block[-1] > e or any(not lines[j - 1].strip() or PAGE_TAG.match(lines[j - 1].strip())
                                for j in block):
            sys.exit(f'{os.path.basename(path)}: letter {b["letter"]}: block of {b["lines"]} lines '
                     f'runs past a page or document end: {b["first"]!r}')
        out.update(block)
    return out


# The kinds of text a page sets apart under a label, and the file each is
# listed in. Both files have the same shape and are read by load_sideways().
#   sideways  written sideways on the page (9454)
#   office    written on the letter by the office that received it: received
#             marks, directions for the reply, paraphs (III. HA MdA, III Nr. 12765)
SET_APART = (('sideways', 'sideways.yml'), ('office', 'office_notes.yml'))


def load_set_apart(unit_dir, lines, bounds):
    """{absolute line number: kind} for every line a page sets apart."""
    out = {}
    for kind, fn in SET_APART:
        for j in load_sideways(os.path.join(unit_dir, fn), lines, bounds):
            if j in out:
                sys.exit(f'{fn}: line {j} is already listed as {out[j]} text')
            out[j] = kind
    return out


def split_pages(body):
    """
    body: [(abs_line_no, text)] for one document, blanks and markers included.
    Returns [(page_id, [(abs_line_no, text), ...]), ...] - one entry per page.

    page_id is the declared identity where the document carries `[PAGE <id>]`
    markers, and None where it does not. Marker lines and blank lines are both
    dropped from the page's text: neither is part of the transcription.
    """
    marked = any(PAGE_TAG.match(t.strip()) for _, t in body)
    pages, cur, cur_id = [], [], None

    if marked:
        for lineno, text in body:
            m = PAGE_TAG.match(text.strip())
            if m:
                if cur:
                    pages.append((cur_id, cur))
                cur, cur_id = [], m.group(1)
            elif text.strip():
                cur.append((lineno, text))
        if cur:
            pages.append((cur_id, cur))
        return pages

    for lineno, text in body:
        if text.strip() == '':
            if cur:
                pages.append((None, cur))
                cur = []
        else:
            cur.append((lineno, text))
    if cur:
        pages.append((None, cur))
    return pages


def _wrap_mark(s):
    """Return the trailing wrap mark of a line, or None."""
    s = s.rstrip()
    if s.endswith('¬'):
        return '¬'
    if re.search(r'\w-$', s) and not s.endswith('--'):
        return '-'
    return None


def page_transcription(page, letter_id, decisions):
    """
    The reading text of the page, but with the manuscript's line breaks kept.

    Only the line-end marks change, and only as the recorded decisions say:

        ¬ where the word really is broken   ->  a plain hyphen
        ¬ where it is not (a stray mark)    ->  removed, the words stand apart
        ¬ on a catchword                    ->  removed; the fragment stays,
                                                since it is on the page
        a real hyphen                       ->  left exactly as written

    Nothing else is touched, so this stays a faithful line-by-line record of the
    page - it just stops asserting word breaks that the evidence contradicts.
    """
    out = []
    for lineno, text in page:
        s = text.rstrip()
        mark = _wrap_mark(s)
        decision = decisions.get((letter_id, lineno), '')
        if mark == '¬':
            if decision == 'join':
                s = s[:-1] + '-'
            else:                      # spurious mark, or a catchword
                s = s[:-1].rstrip()
        out.append(s)
    return '\n'.join(out)


def page_reading(page, letter_id, decisions, is_register=False, paras=None,
                 sideways=None, flags=None):
    """
    Flow one page's lines into readable text, applying the wrap decisions.

    Returns a LIST of paragraphs. `paras` is the set of absolute line numbers
    that begin one, from paragraph_decisions.csv; with none supplied the page
    comes back as a single paragraph, which is what it always used to be.

    Reading text still never crosses a page break, so a paragraph that runs on
    from the previous page starts a new entry here. build_pages records that
    with continues_previous / continues_next, and the site renders such a
    paragraph without an indent so the false break does not show.

    Lines in `sideways` (text the page sets apart: written sideways, or written
    by the receiving office) always make paragraphs of their own, so they never
    merge with the text around them. It is {line: kind}, or a plain set, which
    means sideways text. `flags`, where given, receives one entry per returned
    paragraph: the kind, or False.
    """
    sideways = sideways or {}
    if not isinstance(sideways, dict):
        sideways = dict.fromkeys(sideways, 'sideways')
    if flags is None:
        flags = []
    if is_register:
        # Tabular: one entry per line. Flowing it would destroy the table. A
        # catchword is still the scribe's note of the page overleaf rather than
        # an entry, so it is dropped here exactly as it is from prose.
        rows = []
        for lineno, text in page:
            s = text.strip()
            if decisions.get((letter_id, lineno), '') == 'catchword':
                if not _wrap_mark(text):
                    continue
                s = s[:-1].rstrip()
                hits = list(WORD.finditer(s))
                if hits:
                    s = s[:hits[-1].start()].rstrip()
            rows.append(s)
        flags.append(False)
        return ['\n'.join(rows)]

    paras = paras or set()
    out = []
    buf = ''
    buf_side = False           # the paragraph in `buf` is sideways text
    join_next = False          # this line ended mid-word: append with no space

    for lineno, text in page:
        s = text.strip()
        mark = _wrap_mark(text)
        decision = decisions.get((letter_id, lineno), '')

        if mark and decision == 'join':
            s = s[:-1].rstrip() if mark == '¬' else s[:-1]
        elif mark and decision == 'catchword':
            # The scribe's note of the next page's first word - a navigation
            # device, not text. Drop the fragment and its mark.
            s = s[:-1].rstrip()
            hits = list(WORD.finditer(s))
            if hits:
                s = s[:hits[-1].start()].rstrip()
        elif not mark and decision == 'catchword':
            # An unmarked catchword: the whole line is the scribe's note of the
            # word overleaf, not a fragment hanging off a sentence. Drop the
            # line from the reading text - it stays in the diplomatic view and
            # in the transcription, because it is on the page.
            s = ''
        elif mark == '¬':
            # Spurious continuation mark: a transcription artefact. Remove the
            # mark, but keep the two words apart.
            s = s[:-1].rstrip()
        # mark == '-' with a split decision: the hyphen is real punctuation, kept.

        # A recorded paragraph break starts a new one - but never in the middle
        # of a word carried over the line end, which would put half a word in
        # one paragraph and half in the next.
        side = sideways.get(lineno, False)
        if buf and not join_next and (lineno in paras or side != buf_side):
            out.append(re.sub(r'[ \t]+', ' ', buf).strip())
            flags.append(buf_side)
            buf = ''

        if not buf:
            buf = s
            buf_side = side
        elif join_next:
            buf += s
        elif s:
            buf += ' ' + s

        join_next = bool(mark and decision == 'join')

    if buf.strip():
        out.append(re.sub(r'[ \t]+', ' ', buf).strip())
        flags.append(buf_side)
    return out


def build_pages(body, letter_id, decisions, is_register=False, paras=None,
                sideways=None):
    """
    Returns a list of page dicts:
      page, page_id, line_start, line_end, n_lines, diplomatic, reading,
      paragraphs, continues_previous, continues_next, scan

    `reading` stays the whole page as one string, so anything that only wants
    the text is unaffected. `paragraphs` is the same text divided, and is what
    the site renders.
    """
    out = []
    pages = split_pages(body)
    sideways = sideways or {}
    if not isinstance(sideways, dict):
        sideways = dict.fromkeys(sideways, 'sideways')
    for i, (page_id, page) in enumerate(pages, 1):
        flags = []
        paragraphs = page_reading(page, letter_id, decisions, is_register, paras,
                                  sideways, flags)
        # A paragraph runs on across a page break unless the first line of this
        # page was itself ruled a paragraph start. The reading text still never
        # crosses the break - the flag only tells the reader that it did.
        cont_prev = i > 1 and page[0][0] not in (paras or set())
        cont_next = False
        if i < len(pages):
            nxt = pages[i][1]
            cont_next = nxt[0][0] not in (paras or set())
        out.append({
            'page': i,
            # The manuscript page this text was read from, where the corpus
            # declares it. Stable across relabelling, so it is what the dataset
            # cites and what the scan pairing is built from.
            'page_id': page_id or '',
            'line_start': page[0][0],
            'line_end': page[-1][0],
            'n_lines': len(page),
            # 'diplomatic' is the archival text, untouched - kept as the record
            # against which everything else is checked.
            'diplomatic': '\n'.join(t for _, t in page),
            'transcription': page_transcription(page, letter_id, decisions),
            'reading': '\n\n'.join(paragraphs),
            'paragraphs': paragraphs,
            # Text written sideways on the page (sideways.yml): which of this
            # page's lines (0-based) and which of its paragraphs. Empty for
            # almost every page.
            'sideways_lines': [k for k, (ln, _) in enumerate(page)
                               if sideways.get(ln) == 'sideways'],
            'sideways_paragraphs': [k for k, f in enumerate(flags) if f == 'sideways'],
            'continues_previous': cont_prev,
            'continues_next': cont_next,
            'scan': '',
        })
        # Text the receiving office wrote on the letter (office_notes.yml), in
        # the same two forms. Present only on a page that has some, so a unit
        # without any builds exactly as it did.
        if any(sideways.get(ln) == 'office' for ln, _ in page):
            out[-1]['office_lines'] = [k for k, (ln, _) in enumerate(page)
                                       if sideways.get(ln) == 'office']
            out[-1]['office_paragraphs'] = [k for k, f in enumerate(flags) if f == 'office']
    # A second, reader-facing line number that restarts at 1 in every document.
    #
    # `line_start` and `line_end` count from the top of the unit's corpus.txt,
    # which is what the tooling needs and what a reader cannot use: the letters
    # run to line 20455, so page 1 of document 269a was headed "archival lines
    # 19117-19150" and meant nothing to anyone. The absolute numbers stay, and
    # stay authoritative - the `@<line> old -> new` fixes in
    # transcription_decisions.csv, the `line` on every mention in
    # corpus/index/people.json, and the scan pairing are all keyed to them, and
    # a document's first line moves whenever a document before it gains or
    # loses one. So this is derived and additional, never a replacement, and it
    # stays out of the published page entirely.
    #
    # Counted over CONTENT lines, so the numbering is contiguous across a page
    # break: the absolute range skips the [PAGE ...] marker, and a reader
    # should not see page 1 end at 36 and page 2 begin at 38. The mapping back
    # to an archival line is per page, and lives in the dataset.
    n = 0
    for pg in out:
        pg['doc_line_start'] = n + 1
        n += pg['n_lines']
        pg['doc_line_end'] = n
    return out
