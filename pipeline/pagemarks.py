# -*- coding: utf-8 -*-
"""
Printed page marks in a source text (the editor, 2026-11-24: one style for
every page number, set in the margin).

A newspaper or an article's text file may carry the print's page numbers as
lines of their own. This module finds them, conservatively, for the
generators (pipeline/newspapers/newspapers_site.py) and for the report
(pipeline/review/page_marks_report.py). A work of the literature is cut page
by page already (dataset/literature/<slug>/<page>.<lang>.txt), so its marks
are the passage files themselves; the generator draws those in the same
margin style (pipeline/literature/literature_site.py).

Forms recognised, each only as a line of its own:

  [720]            a bare number in brackets - accepted ONLY when the bare
                   numbers of the text form a run of consecutive pages
                   (720, 721, 722 ...; at least two): a lone "[3]" may be a
                   footnote, a year, a list number
  [s. 720] [p. 720] [S. 720] [str. 720] [Seite 720]     the page named
  - 720 -  (en or em dashes, "– 720 –", "— 720 —")      a running-head number
  s. 720, S. 720, p. 720, str. 720                       the page named

The named forms and the dashed form are unambiguous and accepted alone.
Everything else (a number in a sentence, a year in brackets, "[^5]"
footnote markers, the table cells of a literature page) is not a page mark.
"""
import re

# (form name, pattern, needs a consecutive run to be accepted)
FORMS = [
    ('[N]', re.compile(r'^\[(\d{1,4})\]$'), True),
    ('[s. N]', re.compile(r'^\[(?:s|S|p|pp|str|Seite|page)\.? ?(\d{1,4}(?:[-–]\d{1,4})?)\]$'), False),
    ('— N —', re.compile(r'^(?:[—–]|--) ?(\d{1,4}) ?(?:[—–]|--)$'), False),
    ('p. N', re.compile(r'^(?:s|S|p|str)\. ?(\d{1,4})$'), False),
]


def candidates(lines):
    """Every line that has the shape of a mark: [(index, page, form name)]."""
    out = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        for name, rx, _ in FORMS:
            m = rx.match(s)
            if m:
                out.append((i, m.group(1), name))
                break
    return out


def find_marks(lines):
    """The accepted page marks: {line index: (page, form name)}.

    A bare [N] counts only inside a run of consecutive numbers in order of
    appearance (each one more than the one before), the run at least two long."""
    cands = candidates(lines)
    ok = {i: (p, f) for i, p, f in cands if f != '[N]'}
    bare = [(i, int(p)) for i, p, f in cands if f == '[N]']
    run = []
    for item in bare + [None]:
        if item is not None and run and item[1] == run[-1][1] + 1:
            run.append(item)
            continue
        if len(run) >= 2:
            for i, n in run:
                ok[i] = (str(n), '[N]')
        run = [item] if item is not None else []
    return ok


def marker_html(page, label, anchor=True):
    """The margin marker: a block of no height whose label hangs in the left
    margin (assets/style.css, .pg). `label` is the text ("p. 720")."""
    pid = f' id="p{page}"' if anchor else ''
    return (f'<div class="pg"{pid} data-page="{page}">'
            f'<a href="#p{page}">{label}</a></div>')
