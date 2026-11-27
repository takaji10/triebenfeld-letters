"""Compare the Gr.1181 led reader (A) with the blind reader (B), item by item.
Writes review/latin_audit/app5320pozgr1181/compare.tsv: ref, page, kind, A certainty, B certainty,
class (agree / transcription / differ / nob), transcribed, A page_shows, B page_shows."""
import json, io, re, glob, os, sys, difflib
sys.stdout.reconfigure(encoding='utf-8')
ROOT = __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))
R = __import__('os').path.join(ROOT, 'review', 'latin_audit', sys.argv[1] if len(sys.argv) > 1 else 'app5320pozgr1181') + '/'
A = {}
for k in (1, 2, 3, 4):
    for i, f in enumerate(json.load(io.open(R + 'reader_a_%d.json' % k, encoding='utf-8'))['findings']):
        A['%d.%d' % (k, i)] = f
B = {}
for p in sorted(glob.glob(R + 'reader_b_*.json')):
    for x in json.load(io.open(p, encoding='utf-8')):
        if 'ref' in x:
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
