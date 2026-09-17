# -*- coding: utf-8 -*-
"""
Where the paragraphs fall, decided once and recorded.

The reading text flows a page's lines together into continuous prose. Until now
it flowed them into a single block, so a page of a contract arrived as one
undivided slab however many clauses it contained. This proposes where the
paragraphs begin, you adjudicate, and the build applies what is recorded.

    units/<slug>/paragraph_decisions.csv   one row per candidate, hand-editable
    review/<slug>/paragraph_report.md      what was decided and what to look at

A decision is `break` (this line begins a new paragraph) or `run` (it does not).
Rows are keyed by document and by the absolute line the paragraph would begin
at, and a decision you change is carried over on the next run.

Two cues, and they are different in kind:

  short_line   The line BEFORE this one is materially shorter than the page's
               usual measure. A scribe filling a page to the margin leaves a
               short line only where a paragraph ends, so the next line starts
               one. The page's own median line length is the measure, because
               hand, page size and hand-ruled margins differ from page to page.

               Deliberately not counted: the last line of a page, which is short
               because the page ended rather than because the sense did; a line
               ending in a wrap mark, which is short of nothing since the word
               runs on; and a line whose predecessor is itself a section rubric.

  rubric       The line announces a clause in its own right - `§. VII.`, `§ 3,`,
               a roman or arabic numeral, `a.,` `b.,` `1mo`, `2do`. This volume
               is title deeds and marks its own divisions; 9454's letters do
               not, and rely on the short-line cue and on salutations.

  salutation   An opening or closing formula of a letter.

Cue confidence is reported, never applied silently: `high` where both cues agree
or a rubric is unmistakable, `review` where only a weak short line suggests it.
Nothing here alters the archival text.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import io, sys, os, re, csv, statistics
from collections import Counter
from corpus_pages import split_pages, PAGE_TAG, load_decisions
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
SRC = UNIT.corpus_path
DECISIONS = os.path.join(UNIT.dir, 'paragraph_decisions.csv')
REPORT = os.path.join(ROOT, 'review', UNIT.slug, 'paragraph_report.md')
os.makedirs(os.path.join(ROOT, 'review', UNIT.slug), exist_ok=True)

TAG = re.compile(r'^\[DOC (\w+)\]$')
WORD = re.compile(r'[A-Za-zÀ-ÿĄąĘęŁłŃńÓóŚśŹźŻżſ]+')

# A line that is only a clause marker, or opens with one.
RUBRIC = re.compile(r"""^\s*(
      §+\s*\.?\s*[IVXLC]+\b            # §. VII
    | §+\s*\.?\s*\d+                   # § 3
    | [IVXLC]{1,5}\s*[.,)]             # VII.
    | \d{1,3}\s*[.,)]                  # 3.  17)
    | [a-h]\s*[.,)]                    # a.,  b)
    | \d\s*(mo|do|tio|to|mus)\b        # 1mo 2do 3tio
    | ad\s+\d                          # ad 2
)""", re.X | re.I)

# Letter furniture: an opening address or a closing formula stands alone.
#
# `Sr` and `Ew` are deliberately absent. They look like the start of an address
# but in a volume of deeds they are honorifics that fall anywhere in a sentence
# - "Sr Hochfürstl. Durchlauchten und deren Nachfolger im Besitze" is the middle
# of a clause, not a salutation - and matching them opened a paragraph on almost
# every page. A salutation is only credited below when the previous line has
# actually closed a sentence.
SALUTATION = re.compile(r"""^\s*(
      (Durchlauchtigster|Gnädigster|Hochgebohrner|Wohlgebohrner)\b
    | P\.?\s*S\.?\b
    | (Ich|Wir)\s+(verharre|beharren|habe\s+die\s+Ehre)
    | (Actum|Geschehen|So\s+geschehen|Datum)\b
)""", re.X)

# A sentence that has actually closed. Used to gate the weaker cues: a rubric
# announces itself, but an address or a short line only begins a paragraph if
# what came before it finished.
ENDS_SENTENCE = re.compile(r'[.!?:]\s*$')

# How short is short. A line under this fraction of the page's median length
# reads as the end of a paragraph rather than as text running to the margin.
SHORT = 0.72
# Below this it is unmistakable; between the two it is worth a look.
SHORT_STRONG = 0.55

# Opt-in rules from unit.yml `paragraphs:`. A unit without them keeps exactly
# the candidates it was adjudicated under.
#
#   few_words   a short line must also hold no more than this many words. On a
#               narrow page three words fill the line ("geleisteten
#               ausgezeichneten und" runs to the margin at 25 characters), so
#               length against the page is not enough on its own.
#   column_words  where few_words is set, a run of short lines breaks on its
#               own only if both lines hold no more than this many words;
#               otherwise it is left for review. Absent, it is always left.
#   page_ends   test the last line of a page as well, so that a paragraph can
#               begin overleaf. A catchword at the foot is the commonest short
#               line in a volume and never ends a sentence, so it is set aside.
#
# Either one also skips registers, whose entries are not paragraphs, and never
# proposes a break at a catchword line, which the reading text drops anyway.
_CFG = UNIT.get('paragraphs') or {}
FEW_WORDS = _CFG.get('few_words')
COLUMN_WORDS = _CFG.get('column_words')
PAGE_ENDS = bool(_CFG.get('page_ends'))
DOC_TYPE = unitlib.load_rulings(UNIT)['DOC_TYPE'] if _CFG else {}
CATCHWORDS = ({k for k, v in load_decisions(
    os.path.join(UNIT.dir, 'linebreak_decisions.csv')).items() if v == 'catchword'}
    if _CFG else set())


def load_corpus():
    with open(SRC, encoding='utf-8') as f:
        lines = f.read().split('\n')
    docs, cur = {}, None
    for i, raw in enumerate(lines):
        m = TAG.match(raw.strip())
        if m:
            cur = m.group(1)
            docs[cur] = []
            continue
        # Keep the [PAGE ...] markers: split_pages reads them to find the page
        # boundaries. Stripping them here leaves it nothing to split on, so a
        # whole document collapses into one "page" - the line measure is then
        # taken across the document instead of the page, and the rule that the
        # last line of a page is short because the page ended never fires.
        if cur is not None:
            docs[cur].append((i + 1, raw))
    return docs


def _wrap(s):
    s = s.rstrip()
    return s.endswith('¬') or (re.search(r'\w-$', s) and not s.endswith('--'))


def _short(text, measure):
    """The line stopped early: under the page's measure and, where the unit
    sets `few_words`, no more than that many words. A line ending in a wrap mark
    is short of nothing, since the word runs on.

    A line that closes its sentence is exempt from the word count. The limit is
    there for lines that stop mid-sentence on a narrow page; a dateline
    (`Berlin den 1. Decembr. 1797.`) or a title (`von Preussen p. p.`) has
    four or five words and ends its paragraph all the same."""
    t = text.strip()
    if _wrap(text) or len(t) >= SHORT * measure:
        return False
    return (FEW_WORDS is None or ENDS_SENTENCE.search(t) is not None
            or len(t.split()) <= FEW_WORDS)


def _repeats_overleaf(last, first):
    """A one-word foot line that the next page's first word begins or ends with.

    Either it is a catchword (`Da` before `da der bleibende`) or the scribe
    finished a broken word at the foot and wrote it whole again overleaf
    (`sti¬ / pulirten` then `stipulirten`). Neither is a sentence stopping.
    """
    a, b = WORD.findall(last), WORD.findall(first)
    if len(a) != 1 or not b:
        return False
    x, y = a[0].lower().replace('ſ', 's'), b[0].lower().replace('ſ', 's')
    return len(x) >= 2 and (y.startswith(x) or (len(x) >= 3 and y.endswith(x)))


def candidates(docs):
    """Every line that might begin a paragraph, with the cue that says so."""
    out = []
    for lid, body in docs.items():
        if _CFG and DOC_TYPE.get(lid) == 'register':
            continue
        pages = [ls for _, ls in split_pages(body)]
        for pi, page in enumerate(pages):
            if len(page) < 3:
                continue
            lens = [len(t.strip()) for _, t in page]
            measure = statistics.median(lens[:-1]) or 1
            # The first line of a page is weighed against the foot of the page
            # before, and only where the unit asks for page ends.
            first = 0 if (PAGE_ENDS and pi > 0) else 1
            for k in range(first, len(page)):
                lineno, text = page[k]
                s = text.strip()
                if not s or (lid, lineno) in CATCHWORDS:
                    continue
                if k == 0:
                    before = pages[pi - 1]
                    if len(before) < 3:
                        continue
                    prev_no, prev = before[-1]
                    if ((lid, prev_no) in CATCHWORDS
                            or _repeats_overleaf(prev, text)):
                        continue
                    prev_measure = statistics.median(
                        len(t.strip()) for _, t in before[:-1]) or 1
                else:
                    prev_no, prev = page[k - 1]
                    prev_measure = measure
                p = prev.strip()
                cues, conf = [], 'review'

                closed = bool(ENDS_SENTENCE.search(p))
                is_rubric = bool(RUBRIC.match(s))
                is_salut = bool(SALUTATION.match(s)) and closed
                # The short-line test looks BACKWARDS: this line begins a
                # paragraph because the one before it stopped early. The last
                # line of a page is never `prev` within the page, because it is
                # short when the page ended rather than the sense.
                prev_short = not RUBRIC.match(p) and _short(prev, prev_measure)

                if is_rubric:
                    cues.append('rubric')
                if is_salut:
                    cues.append('salutation')
                if prev_short:
                    cues.append('page_end' if k == 0 else 'short_line')

                if not cues:
                    continue

                # A short line means two different things and they must not be
                # confused. Where the sentence has closed, it is the end of a
                # paragraph. Where it has not, it is usually just a line that
                # happened to run out - EXCEPT in a column of short lines, which
                # is a list or a block of signatures, and there every line is
                # its own item.
                #
                # Where the unit counts words, a column is trusted only if both
                # lines are within `column_words`: that is a signature block or
                # a dateline (`Beda | Ingrossator`). Wider, it broke "für den
                # regierenden | Fürsten von Hohenlohe" mid-sentence, so it goes
                # to review instead.
                in_column = prev_short and len(s) < SHORT * measure
                column_ok = in_column and (
                    FEW_WORDS is None
                    or (COLUMN_WORDS is not None
                        and len(p.split()) <= COLUMN_WORDS
                        and len(s.split()) <= COLUMN_WORDS))
                if is_rubric or is_salut or (prev_short and closed) or column_ok:
                    conf = 'high'
                if in_column and not (is_rubric or closed):
                    cues.append('column')

                # Conservative default. A paragraph break that should not be
                # there splits a sentence in the reading view; one that is
                # missing only leaves the prose running on. So anything resting
                # on a short line alone, mid-sentence, is left unbroken until a
                # human says otherwise.
                decision = 'break' if conf == 'high' else 'run'

                out.append({
                    'letter': lid, 'line': lineno, 'page_measure': round(prev_measure),
                    'prev_len': len(p), 'ratio': round(len(p) / prev_measure, 2),
                    'cue': '+'.join(cues), 'decision': decision, 'confidence': conf,
                    'prev_line': p[:60], 'context': s[:70],
                })
    return out


def main():
    docs = load_corpus()
    rows = candidates(docs)
    print(f'{UNIT.slug}: {len(docs)} documents, {len(rows)} paragraph candidates')

    kept = 0
    if os.path.isfile(DECISIONS):
        prior = {}
        with open(DECISIONS, encoding='utf-8-sig', newline='') as f:
            for old in csv.DictReader(f):
                prior[(old.get('letter', ''), old.get('context', ''))] = old
        for r in rows:
            old = prior.get((str(r['letter']), r['context']))
            if not old:
                continue
            if old.get('confidence') == 'held' or old.get('decision') != r['decision']:
                r['decision'] = old['decision']
                r['confidence'] = 'held'
                kept += 1
    if kept:
        print(f'kept {kept} hand-adjudicated decision(s) from the previous run')

    cols = ['letter', 'line', 'decision', 'confidence', 'cue', 'ratio',
            'prev_len', 'page_measure', 'prev_line', 'context']
    with open(DECISIONS, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r[c] for c in cols})
    print(f'wrote {DECISIONS} ({len(rows)} rows)')

    cue = Counter(r['cue'] for r in rows)
    conf = Counter(r['confidence'] for r in rows)
    A = []
    A.append(f'# Paragraphs - {UNIT.get("ref", UNIT.slug)}\n')
    A.append('Where the reading text should break into paragraphs. The archival '
             'text is untouched; these decisions drive the generated *reading* view '
             'only.\n')
    A.append(f'- candidates: **{len(rows)}** across {len(docs)} documents')
    for k, v in cue.most_common():
        A.append(f'  - `{k}` {v}')
    A.append('')
    for k, v in conf.most_common():
        A.append(f'- {k}: {v}')
    A.append('\n## For your review\n')
    A.append('Candidates resting on a weak short line alone. The `decision` column in '
             '`paragraph_decisions.csv` is hand-editable - change a cell to `run` and '
             'regenerate.\n')
    A.append('| Doc | Line | Ratio | Line before | Begins |')
    A.append('|---|---|---|---|---|')
    for r in rows:
        if r['confidence'] == 'review':
            A.append(f'| {r["letter"]} | {r["line"]} | {r["ratio"]} | '
                     f'{r["prev_line"]} | {r["context"]} |')
    with open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(A) + '\n')
    print(f'wrote {REPORT}')
    print('cues       :', dict(cue))
    print('confidence :', dict(conf))


if __name__ == '__main__':
    main()
