# -*- coding: utf-8 -*-
"""The working record of the full check of APP 53/17/0/-/Konin Gr.145 against the scans.

    python full_check_note.py checked 0655_a2 0656_a1        # pages read word for word
    python full_check_note.py row < one JSON object            # a finding
    python full_check_note.py status                           # what is done, what is left

The editor asked (2026-10-06) for every page to be read for dropped phrases,
and for each one found to be listed with a word on whether it matters to the
meaning. The findings are kept in full_check.jsonl beside this file, one per
line, so that the work can stop and start again:

    page    the page id
    kind    dropped (words on the scan that the transcription lacks)
            misread (a reading that changes the sense; small slips of spelling are not collected)
    old     the transcription as it stood (enough words to stand once on the page)
    new     the same with the scan's words put in, in the modern spelling of the rest
    scan    the words as the scan has them
    en_old, en_new   the English before and after, where it has to follow
    weight  court (changes what the court found or ordered), fact (adds or changes a place,
            person, measure or date), formula (wording only)
    note    anything else

When the check is finished the rows are applied by corrections_full.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(HERE, 'full_check.jsonl')
DONE = os.path.join(HERE, 'full_check_pages.txt')


def all_pages():
    ids = []
    for n in range(654, 716):
        for half in ('a1', 'a2'):
            pid = '%04d_%s' % (n, half)
            if pid not in ('0654_a1', '0655_a1'):
                ids.append(pid)
    return ids


def done():
    if not os.path.isfile(DONE):
        return []
    return [l.strip() for l in io.open(DONE, encoding='utf-8') if l.strip()]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    cmd = sys.argv[1]
    if cmd == 'checked':
        have = done()
        with io.open(DONE, 'a', encoding='utf-8', newline='\n') as f:
            for p in sys.argv[2:]:
                assert p in all_pages(), p
                if p not in have:
                    f.write(p + '\n')
    elif cmd == 'row':
        r = json.loads(sys.stdin.read())
        assert r['page'] in all_pages() and r['kind'] in ('dropped', 'misread') and r['weight'] in ('court', 'fact', 'formula'), r
        t = io.open(os.path.join(os.path.dirname(HERE), 'transcriptions', r['page'] + '.txt'), encoding='utf-8').read()
        assert t.count(r['old']) == 1, 'old text stands %d time(s) on %s' % (t.count(r['old']), r['page'])
        with io.open(ROWS, 'a', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    have = done()
    left = [p for p in all_pages() if p not in have]
    n = sum(1 for _ in io.open(ROWS, encoding='utf-8')) if os.path.isfile(ROWS) else 0
    print('%d of %d pages read; %d findings; next: %s' % (len(have), len(all_pages()), n, ' '.join(left[:4])))


if __name__ == '__main__':
    main()
