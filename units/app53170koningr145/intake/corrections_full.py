# -*- coding: utf-8 -*-
"""The full check of APP 53/17/0/-/Konin Gr.145 applied to the text, 2026-10-06.

    python units/app53170koningr145/intake/corrections_full.py            # check only
    python units/app53170koningr145/intake/corrections_full.py --write    # once

A record: run once, after corrections.py. Do not run it again, and do not run
build_pages.py --write or corrections.py --write after it.

The editor asked for every page to be read against its scan for dropped
phrases. All 122 pages were read (full_check_pages.txt). What was found is in
full_check_rows.py: words on the scan that the transcription lacked, and
readings that change the sense. Each row's `old` must stand exactly once on
its page; rows are applied in the order they were recorded. Applied to
transcriptions/ and corpus.txt, and logged in transcription_decisions.csv
with the kind and weight of each.

What was not collected: slips of spelling that change nothing (a missing
accent, i for y), since the text is in modern spelling by the editor's choice.
"""
import csv
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'app53170koningr145'
sys.path.insert(0, HERE)
import full_check_rows as F  # noqa: E402


def page_ids():
    ids = []
    for n in range(654, 716):
        for half in ('a1', 'a2'):
            pid = '%04d_%s' % (n, half)
            if pid not in ('0654_a1', '0655_a1'):
                ids.append(pid)
    return ids


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write = '--write' in sys.argv
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    ids = page_ids()
    text = {p: io.open(os.path.join(tdir, p + '.txt'), encoding='utf-8').read().rstrip('\n').split('\n') for p in ids}
    log, bad = [], []
    for r in F.ROWS:
        pid, old, new = r['page'], r['old'], r['new']
        hits = [i for i, l in enumerate(text[pid]) if old in l]
        n = sum(text[pid][i].count(old) for i in hits)
        if n != 1:
            bad.append('%s: found %d time(s): %r' % (pid, n, old[:70]))
            continue
        i = hits[0]
        text[pid][i] = text[pid][i].replace(old, new)
        key = hashlib.md5(('full|%s|%s|%s' % (pid, old, new)).encode()).hexdigest()[:8]
        log.append([key, SLUG + '-001', ids.index(pid) + 1, old, new, '%s: %s -> %s' % (pid, old[:60], new[:60]),
                    'full check against the scan, %s, %s: %s' % (r['kind'], r['weight'], r['note'] or r['scan'])])
    print(len(F.ROWS), 'rows;', len(bad), 'do not apply')
    for b in bad:
        print('  ', b)
    if bad or not write:
        return
    for pid in ids:
        io.open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(text[pid]) + '\n')
    out = ['[DOC 1]']
    for pid in ids:
        out.append('[PAGE %s]' % pid)
        out.extend(text[pid])
    io.open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    with io.open(os.path.join(UNIT_DIR, 'transcription_decisions.csv'), 'a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(log)
    print('written and logged')


if __name__ == '__main__':
    main()
