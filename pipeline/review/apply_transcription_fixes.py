# -*- coding: utf-8 -*-
"""
Apply the rulings in transcription_fixes.csv to the unit's corpus.txt.

    python apply_transcription_fixes.py --unit oe1bu14526            # report only
    python apply_transcription_fixes.py --unit oe1bu14526 --apply    # write

corpus.txt is the canonical transcription and the one file in the project that
no build ever rewrites, so this is deliberately timid:

  * it changes single words, never spans. A proposal is reduced to the words it
    actually alters, and each of those must sit whole inside one corpus line
  * the word it is replacing must appear exactly once in the anchored line
  * a row whose line no longer reads as the sheet recorded it is refused, not
    guessed at - the sheet is stale and should be rebuilt
  * a row that changes a word the edition recognises as a person or a place is
    applied only with --names, because a name silently improved destroys the
    evidence that the reading was wrong

`decision` is read as: `y` apply as proposed, `n` or blank reject, anything else
is the reading you want in place of the proposal.

A row the sheet could not anchor - the model quoted the reading text, in which
the line breaks and abbreviations are already resolved, so its words are not on
any single line of corpus.txt - can still be ruled on by writing the fix out:

    @1179 Zeu -> Zei ; @3013 me -> nie

Each clause names a corpus line, the exact token on it, and what to put there.
Nothing is applied unless the token is on that line exactly once.

Every applied change is written to review/<slug>/transcription_fixes_applied.md,
with the line before and after, so the pass can be read back and reversed.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, difflib, argparse

import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NO = {'', 'n', 'no', 'x', '-', 'reject', 'skip'}
YES = {'y', 'yes', 'ok', 'apply', 'a'}
WORD = re.compile(r'[^\W\d_]+', re.UNICODE)
# '@1179 Zeu -> Zei' - an editor's fix for a row the sheet could not anchor
EXPLICIT = re.compile(r'^\s*@(\d+)\s+(.+?)\s*->\s*(.+)$')


def occurrences(line, token):
    """How many times `token` stands in `line` as its own run of characters.

    Plain substring counting applied a fix twice: `ehörig` -> `gehörig` matched
    again inside the `gehörig` the first pass had already written, and left
    `ggehörig`. A replacement must see the token whole, with a non-word
    character (or the line edge) on each side.
    """
    return len(re.findall(r'(?<![^\W\d_])' + re.escape(token) + r'(?![^\W\d_])',
                          line))


def replace_once(line, token, reading):
    return re.sub(r'(?<![^\W\d_])' + re.escape(token) + r'(?![^\W\d_])',
                  lambda _m: reading, line, count=1)


def word_changes(before, after):
    """The individual word substitutions a proposal amounts to.

    `Erbkünster muß sich auf eigene Kosten gekommen` ->
    `Erbpächter muß sich auf eigene Kosten erbauen` is two word changes, not one
    span of eight. Reducing it lets each half be applied on the line it actually
    sits on, and lets a restructuring - a different number of words - be refused
    rather than half-applied.
    """
    a, b = before.split(), after.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if tag == 'equal':
            continue
        if tag != 'replace' or (i2 - i1) != (j2 - j1):
            return None                      # words added or dropped: not ours
        out.extend(zip(a[i1:i2], b[j1:j2]))
    return out


def name_authority():
    """Every surface form the edition recognises as a person or a place.

    Capitalisation cannot be the test - German capitalises every noun, and it
    refused `Weyernster` -> `Weihnachten`, which is Christmas. What actually
    needs the extra flag is a change to a word the edition has identified as
    somebody or somewhere, because that is where a silent improvement destroys
    the evidence that the reading was wrong.
    """
    _sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))
    from entities import load_people, load_places
    out = set()
    for slug, display, _ in load_people():
        out.update(w.lower() for w in WORD.findall(display))
    for variant, canon in load_places().items():
        out.update(w.lower() for w in WORD.findall(variant))
        out.update(w.lower() for w in WORD.findall(canon))
    return {w for w in out if len(w) > 3}


def is_name(w, authority):
    core = w.strip('.,;:()[]"\'').lower()
    return core in authority


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds '
                                   'more than one')
    ap.add_argument('--apply', action='store_true', help='write corpus.txt')
    ap.add_argument('--names', action='store_true',
                    help='also apply changes that touch a name in the authority')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    unit = unitlib.one_unit(slug)
    rev = unitlib.review_dir(slug)
    sheet = os.path.join(rev, 'transcription_fixes.csv')
    if not os.path.isfile(sheet):
        sys.exit(f'no sheet at {sheet} - run transcription_fixes.py first')

    corpus_path = os.path.join(unit.dir, unit.get('corpus') or 'corpus.txt')
    text = io.open(corpus_path, encoding='utf-8').read()
    lines = text.split('\n')

    authority = name_authority()
    applied, refused, skipped, done_already = [], [], 0, 0
    for r in csv.DictReader(io.open(sheet, encoding='utf-8-sig')):
        d = (r.get('decision') or '').strip()
        if d.lower() in NO:
            skipped += 1
            continue
        if (r.get('needs') or '') == 'applied':
            # the sheet's own receipt: this ruling is already in the corpus,
            # which is why the row no longer locates. Not an unfinished job.
            done_already += 1
            continue
        want = r['proposed'] if d.lower() in YES else d

        # an explicit fix: '@<line> <token> -> <reading>', several allowed
        if EXPLICIT.match(d):
            # checked in full before anything is written: half a ruling applied
            # is worse than none, and harder to see afterwards
            plan, trouble = [], None
            for clause in d.split(';'):
                m = EXPLICIT.match(clause.strip())
                if not m:
                    trouble = f'{clause.strip()!r} is not @line old -> new'
                    break
                n, old, new = int(m.group(1)), m.group(2), m.group(3).strip()
                if not 1 <= n <= len(lines):
                    trouble = f'line {n} is outside the corpus'
                    break
                if occurrences(lines[n - 1], old) != 1:
                    trouble = (f'{old!r} appears {occurrences(lines[n - 1], old)} '
                               f'time(s) on line {n}')
                    break
                plan.append((n, old, new))
            if trouble:
                refused.append((r, trouble))
                continue
            for n, old, new in plan:
                before = lines[n - 1]
                lines[n - 1] = replace_once(before, old, new)
                applied.append((r, n, before, lines[n - 1]))
            continue

        why_no = None
        if r['confidence'] == 'unlocated' or not r['line'].strip():
            why_no = 'not located in the corpus'
        elif len(r['line'].split()) > 1:
            why_no = 'occurs more than once on the page - apply this one by hand'
        if why_no:
            refused.append((r, why_no))
            continue

        pairs = word_changes(r['transcribed'], want)
        if not pairs:
            refused.append((r, 'not a word-for-word change - apply by hand'))
            continue

        n0 = int(r['line'])
        # the anchor line, and the few after it a broken word may run into
        span = range(n0 - 1, min(len(lines), n0 - 1 + 4))
        done, trouble = [], None
        for old, new in pairs:
            if (is_name(old, authority) or is_name(new, authority)) and not a.names:
                trouble = (f'{old!r} -> {new!r} touches a name in the authority '
                           f'- re-run with --names to apply it')
                break
            hits = [i for i in span if occurrences(lines[i], old) == 1]
            if not hits:
                trouble = f'{old!r} not found once on line {n0} or the 3 after it'
                break
            if len({i for i in span if occurrences(lines[i], old)}) > 1:
                trouble = f'{old!r} appears on more than one line here'
                break
            done.append((hits[0], old, new))
        if trouble:
            refused.append((r, trouble))
            continue

        for i, old, new in done:
            before = lines[i]
            lines[i] = replace_once(before, old, new)
            applied.append((r, i + 1, before, lines[i]))

    print(f'{len(applied)} change(s) on {len({x[1] for x in applied})} line(s)')
    print(f'{len(refused)} refused, {skipped} rejected, '
          f'{done_already} already in the corpus')
    for r, why in refused[:12]:
        print(f'  L{r["letter"]} p{r["page"]} {r["transcribed"]!r}: {why}')
    if len(refused) > 12:
        print(f'  ... and {len(refused) - 12} more')

    if not a.apply:
        print('\n(report only - re-run with --apply to write corpus.txt)')
        return
    if not applied:
        return

    out = '\n'.join(lines)
    assert len(out.split('\n')) == len(text.split('\n')), 'line count changed'
    with io.open(corpus_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    log = os.path.join(rev, 'transcription_fixes_applied.md')
    with io.open(log, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# Transcription fixes applied - {slug}\n\n'
                f'{len(applied)} change(s). Each row gives the corpus line '
                f'before and after.\n\n')
        for r, n, before, after in applied:
            f.write(f'## line {n} - document {r["letter"]}, page {r["page"]}'
                    f' ({r["page_id"]})\n\n'
                    f'- was: `{before}`\n- now: `{after}`\n'
                    f'- why: {r["why"]}\n\n')
    print(f'\nwrote {corpus_path}\nwrote {log}')
    print('now re-run regenerate.py: line numbers have not moved, but the pages, '
          'the reading copy and the site all derive from this file')


if __name__ == '__main__':
    main()
