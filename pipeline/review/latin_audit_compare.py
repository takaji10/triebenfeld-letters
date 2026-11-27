# -*- coding: utf-8 -*-
"""Compare the led readers (A) with the blind readers (B) of the Latin audit, item by item.

    python pipeline/review/latin_audit_compare.py <slug> <A file> [<A file> ...]

A files are review/latin_audit/<slug>/<name>.json; a finding is "<file stem>.<index>" (as
latin_audit_items.py names them). B files are every reader_b*.json in the same folder.
Writes review/latin_audit/<slug>/compare.tsv: ref, page, kind, A certainty, B certainty, class
(agree / transcription / differ / nob = the blind reader unsure or silent), transcribed, A, B.
A class "agree" is a candidate, not a settlement: Claude reads each before it becomes a row.
"""
import json, io, re, glob, os, sys, difflib
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = os.path.join(ROOT, 'review', 'latin_audit', sys.argv[1]) + '/'
A = {}
for fn in sys.argv[2:]:
    stem = os.path.splitext(os.path.basename(fn))[0]
    for i, f in enumerate(json.load(io.open(R + os.path.basename(fn), encoding='utf-8'))['findings']):
        A['%s.%d' % (stem, i)] = f
B = {}
for p in sorted(glob.glob(R + 'reader_b*.json')):
    for x in json.load(io.open(p, encoding='utf-8')):
        if isinstance(x, dict) and 'ref' in x:
            B[x['ref']] = x


def toks(s):
    s = s.lower().replace('ſ', 's')
    s = re.sub(r'\([^)]*\)', ' ', s)                 # readers' glosses in brackets
    s = re.sub(r'[~^\[\]?…\.,;:"\'/|\-]', ' ', s)
    return [t for t in s.split() if len(t) > 2]


def has(tok, pool):
    return any(difflib.SequenceMatcher(None, tok, p).ratio() >= 0.8 for p in pool)


out = ['ref\tpage\tkind\tAcert\tBcert\tclass\ttranscribed\tA\tB']
counts = {}
for ref, f in A.items():
    b = B.get(ref)
    if not b:
        continue
    tr, a, bt = toks(f['transcribed']), toks(f['page_shows']), toks(b.get('page_shows', ''))
    new = [t for t in a if not has(t, tr)]           # what A reads that the transcription lacks
    old = [t for t in tr if not has(t, a)]           # what the transcription has that A rejects
    if not bt or b.get('certainty') == 'unsure':
        cls = 'nob'
    elif new and all(has(t, bt) for t in new) and not any(has(t, bt) for t in old):
        cls = 'agree'
    elif old and all(has(t, bt) for t in old):
        cls = 'transcription'
    elif not new and not old:
        cls = 'agree' if f['kind'] == 'doubt_settled' and all(has(t, bt) for t in a) else 'differ'
    else:
        cls = 'differ'
    counts[cls] = counts.get(cls, 0) + 1
    out.append('\t'.join([ref, f['page_id'], f['kind'], f['certainty'], b.get('certainty', ''), cls,
                          f['transcribed'][:120], f['page_shows'][:140], b.get('page_shows', '')[:160]]))
io.open(R + 'compare.tsv', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print(counts)
