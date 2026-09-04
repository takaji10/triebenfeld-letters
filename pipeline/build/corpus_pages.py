# -*- coding: utf-8 -*-
"""
Page structure and the generated reading text.

A letter is a sequence of manuscript pages (the corpus marks page breaks with a
blank line). Each page carries three views:

    diplomatic  - the archival lines, exactly as transcribed        [canonical]
    reading     - lines flowed together, wraps resolved             [generated]
    translation - English                                           [added later]

plus a `scan` slot for the page image, empty for now.

Reading text NEVER flows across a page break, so text always stays alongside the
right scan and the page breaks stay visible.

Whether a line-end mark really joins two halves of a word is decided in
resolve_linebreaks.py and recorded in linebreak_decisions.csv, which is
hand-editable. This module only applies those decisions.
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


def split_pages(body):
    """
    body: [(abs_line_no, text)] for one letter, blank lines included.
    Returns [[(abs_line_no, text), ...], ...] - one list per page, blanks dropped.
    """
    pages, cur = [], []
    for lineno, text in body:
        if text.strip() == '':
            if cur:
                pages.append(cur)
                cur = []
        else:
            cur.append((lineno, text))
    if cur:
        pages.append(cur)
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


def page_reading(page, letter_id, decisions, is_register=False):
    """Flow one page's lines into readable text, applying the wrap decisions."""
    if is_register:
        # Tabular: one entry per line. Flowing it would destroy the table.
        return '\n'.join(t.strip() for _, t in page)

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
        elif mark == '¬':
            # Spurious continuation mark: a transcription artefact. Remove the
            # mark, but keep the two words apart.
            s = s[:-1].rstrip()
        # mark == '-' with a split decision: the hyphen is real punctuation, kept.

        if not buf:
            buf = s
        elif join_next:
            buf += s
        elif s:
            buf += ' ' + s

        join_next = bool(mark and decision == 'join')

    return re.sub(r'[ \t]+', ' ', buf).strip()


def build_pages(body, letter_id, decisions, is_register=False):
    """
    Returns a list of page dicts:
      page, line_start, line_end, n_lines, diplomatic, reading, scan
    """
    out = []
    for i, page in enumerate(split_pages(body), 1):
        out.append({
            'page': i,
            'line_start': page[0][0],
            'line_end': page[-1][0],
            'n_lines': len(page),
            # 'diplomatic' is the archival text, untouched - kept as the record
            # against which everything else is checked.
            'diplomatic': '\n'.join(t for _, t in page),
            'transcription': page_transcription(page, letter_id, decisions),
            'reading': page_reading(page, letter_id, decisions, is_register),
            'scan': '',
        })
    return out
