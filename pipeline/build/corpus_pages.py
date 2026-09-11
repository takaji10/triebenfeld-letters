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


def page_reading(page, letter_id, decisions, is_register=False, paras=None):
    """
    Flow one page's lines into readable text, applying the wrap decisions.

    Returns a LIST of paragraphs. `paras` is the set of absolute line numbers
    that begin one, from paragraph_decisions.csv; with none supplied the page
    comes back as a single paragraph, which is what it always used to be.

    Reading text still never crosses a page break, so a paragraph that runs on
    from the previous page starts a new entry here. build_pages records that
    with continues_previous / continues_next, and the site renders such a
    paragraph without an indent so the false break does not show.
    """
    if is_register:
        # Tabular: one entry per line. Flowing it would destroy the table.
        return ['\n'.join(t.strip() for _, t in page)]

    paras = paras or set()
    out = []
    buf = ''
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
        if buf and not join_next and lineno in paras:
            out.append(re.sub(r'[ \t]+', ' ', buf).strip())
            buf = ''

        if not buf:
            buf = s
        elif join_next:
            buf += s
        elif s:
            buf += ' ' + s

        join_next = bool(mark and decision == 'join')

    if buf.strip():
        out.append(re.sub(r'[ \t]+', ' ', buf).strip())
    return out


def build_pages(body, letter_id, decisions, is_register=False, paras=None):
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
    for i, (page_id, page) in enumerate(pages, 1):
        paragraphs = page_reading(page, letter_id, decisions, is_register, paras)
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
            'continues_previous': cont_prev,
            'continues_next': cont_next,
            'scan': '',
        })
    # A second, reader-facing line number that restarts at 1 in every document.
    #
    # `line_start` and `line_end` count from the top of the unit's corpus.txt,
    # which is what the tooling needs and what a reader cannot use: the letters
    # run to line 20455, so page 1 of document 269a is headed "archival lines
    # 19117-19150" and means nothing to anyone. The absolute numbers stay, and
    # stay authoritative - the `@<line> old -> new` fixes in
    # transcription_decisions.csv, the `line` on every mention in
    # corpus/index/people.json, and the scan pairing are all keyed to them, and
    # a document's first line moves whenever a document before it gains or
    # loses one. So this is derived and additional, never a replacement.
    if out:
        base = out[0]['line_start'] - 1
        for pg in out:
            pg['doc_line_start'] = pg['line_start'] - base
            pg['doc_line_end'] = pg['line_end'] - base
    return out
