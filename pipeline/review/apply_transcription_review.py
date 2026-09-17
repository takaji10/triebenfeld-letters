# -*- coding: utf-8 -*-
"""
Apply a ruled transcription_review.csv to the unit's corpus.txt.

    python pipeline/review/apply_transcription_review.py --unit <slug>            # report only
    python pipeline/review/apply_transcription_review.py --unit <slug> --apply    # write

The sheet gives each change as whole lines, before and after, so it can do what
apply_transcription_fixes.py deliberately cannot: put lines back in the order
they stand on the page, and remove a line that is not on the page at all. A row
spanning several lines names them 'start-end' and joins them with ' / '.

`your_ruling` is read as: `y` apply as proposed, `n` or blank skip, anything
else is your own reading of the line(s), written in the same ' / ' form.

Nothing is guessed:

  * a row whose lines no longer read as the sheet recorded them is refused
  * a row that would touch a [DOC ...] or [PAGE ...] marker is refused, because
    those carry the document boundaries and the pairing with the scans
  * overlapping rows stop the run before anything is written

Rows are applied from the bottom of the corpus up, so a row that removes a line
cannot shift the lines a later row names. Every change is appended to
review/<slug>/<sheet>_applied.md, and the totals of [?] and [...]
are reported before and after, because a mark of doubt is evidence.
"""
import argparse
import csv
import datetime
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

YES = {'y', 'yes', 'ok', 'apply', 'a'}
NO = {'', 'n', 'no', 'x', '-', 'reject', 'skip'}
SEP = ' / '
MARKER = re.compile(r'^\[(DOC|PAGE) ')
DOUBT = re.compile(r'\[[^\]]*\?\]')


def span(s):
    """'602-603' -> (602, 603); '17' -> (17, 17)."""
    a, _, b = s.strip().partition('-')
    return int(a), int(b or a)


def marks(lines):
    text = '\n'.join(lines)
    return len(DOUBT.findall(text)), text.count('[...]')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--apply', action='store_true', help='write corpus.txt; otherwise report only')
    ap.add_argument('--sheet', default='transcription_review.csv',
                    help='the sheet in review/<slug>/ (default transcription_review.csv)')
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    sheet = os.path.join(ROOT, 'review', unit.slug, a.sheet)
    with open(sheet, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    lines = unit.read_corpus()

    plan, refused, skipped = [], [], 0
    for r in rows:
        ruling = (r.get('your_ruling') or '').strip()
        if ruling.lower() in NO:
            skipped += 1
            continue
        after = r['proposed'] if ruling.lower() in YES else ruling
        start, end = span(r['line'])
        old = lines[start - 1:end]
        new = after.split(SEP)
        if SEP.join(old) != r['transcribed']:
            refused.append((r, 'the line no longer reads as the sheet recorded it'))
        elif any(MARKER.match(l) for l in old + new):
            refused.append((r, 'it would touch a [DOC] or [PAGE] marker'))
        else:
            plan.append((start, end, old, new, r))

    plan.sort(key=lambda p: p[0])
    for (s1, e1, *_), (s2, *_rest) in zip(plan, plan[1:]):
        if s2 <= e1:
            raise SystemExit(f'rows overlap at corpus lines {s1}-{e1} and {s2}; nothing written')

    before_marks = marks(lines)
    n_before = len(lines)
    for start, end, old, new, r in reversed(plan):
        lines[start - 1:end] = new
    after_marks = marks(lines)

    print(f'{unit.slug}: {len(rows)} row(s) in the sheet')
    print(f'  to apply : {len(plan)}')
    print(f'  skipped  : {skipped} (ruled no, or not ruled)')
    print(f'  refused  : {len(refused)}')
    for r, why in refused:
        print(f"    row {r['id']} (line {r['line']}): {why}")
    print(f'  lines    : {n_before} -> {len(lines)}')
    print(f'  [?] marks: {before_marks[0]} -> {after_marks[0]}')
    print(f'  [...]    : {before_marks[1]} -> {after_marks[1]}')

    if not a.apply:
        print('\nreport only - pass --apply to write')
        return

    with open(unit.corpus_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))

    log = os.path.join(ROOT, 'review', unit.slug, os.path.splitext(a.sheet)[0] + '_applied.md')
    fresh = not os.path.isfile(log)
    with open(log, 'a', encoding='utf-8', newline='\n') as f:
        if fresh:
            f.write(f'# {os.path.splitext(a.sheet)[0]} applied - {unit.slug}\n\n'
                    'Each change gives the corpus line(s) before and after. Line numbers are\n'
                    'those of corpus.txt before the pass in which the change was made.\n')
        f.write(f'\n## Pass of {datetime.date.today().isoformat()}: {len(plan)} change(s)\n')
        for start, end, old, new, r in plan:
            where = f'line {start}' if start == end else f'lines {start}-{end}'
            f.write(f"\n### {where} - document {r['doc']}, page {r['page']}\n\n"
                    f"- was: `{SEP.join(old)}`\n- now: `{SEP.join(new)}`\n- why: {r['why']}\n")
    print(f'\nwrote {unit.corpus_path}')
    print(f'logged {log}')
    print(f'next: python regenerate.py --unit {unit.slug}')


if __name__ == '__main__':
    main()
