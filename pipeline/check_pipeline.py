# -*- coding: utf-8 -*-
"""
Standing checks on the pipeline itself, not on the edition it builds.

    python check_pipeline.py

Two mistakes were made repeatedly while this project grew from one holding to
two, and both are invisible until output looks wrong:

  1. ONE HOLDING'S FACTS WRITTEN INTO CODE. The translator's prompt described
     "letters written between 1798 and 1816 by von Triebenfeld" whatever it was
     pointed at; the summariser said the same; the document languages, the pilot
     sample, the twin basis and the register prose all named 9454's documents.
     Each was found by noticing bad output. A holding's facts belong in
     units/<slug>/unit.yml and rulings.yml, where the next holding can state its
     own.

  2. THE ARCHIVE'S DOCUMENT NUMBER USED AS AN ADDRESS. `letter_id` is unique
     only inside its holding, and both units have a document 2. Keying on it
     made one script check every deed against the letter of the same number and
     another pair one holding's English with another's record - the same bug,
     written twice, because each script built its own dictionary. `pad` and
     `uid` carry the unit; `unitlib.records_by_pad()` is the one dictionary.

Neither check is clever. Both are cheap, and both would have caught what took a
day to find by hand.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Facts about one holding. Harmless in a comment or a docstring - that is where
# the reasons for past decisions are recorded - and wrong in running code.
UNIT_FACTS = re.compile(
    r'\b(Triebenfeld|Hohenlohe|Trąbczyn|Zagorowo|Betsche|Kalisch|'
    r'1798|1816|1766|1808|oe1bu9454|oe1bu14526)\b')

# Building a record dictionary on the archive's own number.
BY_LETTER_ID = re.compile(r"\{\s*str\(\s*\w+\[['\"]letter_id['\"]\]\s*\)\s*:")

SKIP_DIRS = {'__pycache__', '.git', 'node_modules'}
# These may name a holding: they are about a specific holding by design.
ALLOW = {os.path.join('pipeline', 'intake', 'stage_pages.py'),
         os.path.join('pipeline', 'intake', 'import_pages.py'),
         os.path.join('pipeline', 'check_pipeline.py')}   # its own pattern list

# An inline waiver, which must carry its reason. It covers the line it sits on
# and the few that follow, so one waiver serves one statement:
#     recs = {str(r['letter_id']): r ...}   # pipeline-check: scoped to one unit
# Silence with a reason attached is a decision; silence without one is a bug
# waiting to be rediscovered.
WAIVER = re.compile(r'#\s*pipeline-check:\s*(\S.*)$')
# A whole file may be waived where the debt is the file's, not a line's:
#     # pipeline-check-file: <reason>
FILE_WAIVER = re.compile(r'#\s*pipeline-check-file:\s*(\S.*)')


def code_lines(path):
    """Lines that run, with comments and docstrings dropped.

    Crude but sufficient: a triple-quoted block is skipped wholesale and
    anything after a # is cut. It over-reports a string containing a #, which
    is a false positive worth having.
    """
    out, in_doc, mark = [], False, ''
    for n, raw in enumerate(io.open(path, encoding='utf-8'), 1):
        line = raw
        if in_doc:
            if mark in line:
                in_doc = False
                line = line.split(mark, 1)[1]
            else:
                continue
        while True:
            m = re.search(r'"""|\'\'\'', line)
            if not m:
                break
            mark = m.group(0)
            rest = line[m.end():]
            if mark in rest:
                line = line[:m.start()] + rest.split(mark, 1)[1]
                continue
            line, in_doc = line[:m.start()], True
            break
        line = line.split('#', 1)[0]
        if line.strip():
            out.append((n, line))
    return out


def main():
    problems, waived = [], []
    for base, dirs, files in os.walk(os.path.join(ROOT, 'pipeline')):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(base, fn)
            rel = os.path.relpath(path, ROOT)
            if rel.replace('/', os.sep) in ALLOW:
                continue
            raw_lines = io.open(path, encoding='utf-8').read().splitlines()
            fw = next((FILE_WAIVER.search(l) for l in raw_lines[:40]
                       if FILE_WAIVER.search(l)), None)
            if fw:
                waived.append((rel, fw.group(1).strip()))
                continue
            for n, line in code_lines(path):
                whole = raw_lines[n - 1] if n <= len(raw_lines) else ''
                # a waiver stands for the statement it introduces, not only for
                # the line it sits on: a regex spread over five lines is one
                # decision, and should not need five waivers
                back = raw_lines[max(0, n - 7):n]
                if any(WAIVER.search(l) for l in back):
                    continue
                if 'help=' in whole:
                    continue        # a slug in --help text is documentation
                m = UNIT_FACTS.search(line)
                if m:
                    problems.append((rel, n, f'names one holding: {m.group(0)!r}',
                                     line.strip()[:90]))
                if BY_LETTER_ID.search(line):
                    problems.append((rel, n, 'keys records on letter_id - use '
                                             'unitlib.records_by_pad()',
                                     line.strip()[:90]))

    for rel, n, why, line in problems:
        print(f'{rel}:{n}: {why}\n    {line}')
    for rel, why in waived:
        print(f'{rel}: waived - {why}')
    print(f'\n{len(problems)} problem(s), {len(waived)} file(s) waived')
    if problems:
        print('\nA holding\'s facts belong in units/<slug>/unit.yml and '
              'rulings.yml.\nRecords are keyed by pad, never by the archive\'s '
              'own document number.')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
