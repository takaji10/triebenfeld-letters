# -*- coding: utf-8 -*-
"""Produce an independent second witness for each manuscript page.

The corpus has one transcription and no way to check it. Letters 48 and 302 are
the same document transcribed twice, and they disagree on 104 of ~630 words --
so a single pass over this hand is not reliable, and every text-internal method
(frequency, edit distance) is blind to the errors that matter most: real words
in the wrong place, and names that look like ordinary names.

This script reads each page again from its scan and stores the result beside
the existing text, never over it. `collate_witnesses.py` then does the
comparison. Nothing here writes to the corpus.

The read is deliberately BLIND: the model is given the page image and the
period/genre conventions, and never the existing transcription or a list of the
names that occur in it. A primed witness agrees with you and proves nothing.

    python retranscribe.py --pilot                 # 8 pages, live, inspect quality
    python retranscribe.py --letters 1,48,302      # named letters
    python retranscribe.py --all --batch           # all 869 pages via Batch API
    python retranscribe.py --collect               # fetch finished batches
    python retranscribe.py                         # how many pages still lack a witness

Resumable: a page that already has a stored witness is skipped, so an
interrupted run costs nothing to restart.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, csv, json, time, base64, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import anthropic
import unitlib
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
SCANS = os.path.join(ROOT, 'pages')
OUT = os.path.join(ROOT, 'retranscription')
MAP = os.path.join(UNIT.dir, 'page_scan_map.csv')

MODEL = 'claude-opus-5'
MAX_TOKENS = 8000

# $ per million tokens (input, output), for the run's own cost readout.
PRICES = {'claude-opus-5': (5, 25), 'claude-fable-5-1': (10, 50),
          'claude-sonnet-5': (2, 10), 'claude-opus-4-8': (5, 25)}

SYSTEM = """\
You are a paleographer transcribing manuscript letters written between 1798 and \
1816 in Kurrentschrift (German cursive). The correspondence is private and \
administrative: estate management, debts, lawsuits, court and ministry business \
in Silesia, South Prussia and the Duchy of Warsaw, and the Congress of Vienna. \
Hands vary; some pages are hasty, blotted, faded or water-damaged.

Transcribe DIPLOMATICALLY -- what is on the page, not what it ought to say.

LANGUAGE
Almost every page is German. A few are French or Polish, and chancery Latin is \
scattered inline through the German. Begin your output with a single line \
declaring the dominant language of the page:

    [lang: de]   (or fr, pl, la)

Then transcribe. Judge the language from the page itself. Beware that this \
German uses heavy French and Latin administrative loan-vocabulary -- words for \
revenue, currency, manufacture, prefecture, dispatches and legal process are \
routinely French or Latin in form inside ordinary German sentences. Loan-words \
do not make a page French: declare fr or pl only if the page is genuinely \
written in that language throughout.

Rules:
1. One manuscript line per output line. Preserve the original lineation exactly.
   Do not join lines, do not reflow, do not paragraph.
2. Preserve the writer's orthography exactly. This is pre-standardised German:
   expect and keep doubled consonants, excrescent -h- and -t-, -th- and -dt-
   spellings, y where modern German has i, ß and ss as written, and abbreviated
   or superscripted honorifics, currencies and measures. Never modernise
   spelling, capitalisation or punctuation, and never regularise a word to match
   another spelling of it elsewhere on the page.
3. Where the hand distinguishes long s, write it as ſ. Where it does not, or
   you cannot tell, write s.
4. A word broken across a line ends with ¬ on the first line.
5. Uncertain reading: [word?]. Illegible: [?]. One [?] per illegible word.
6. Marginal notes, interlineations and later additions: put each on its own
   line prefixed with [margin] or [interlinear]. Do not silently omit them.
7. Deletions that remain legible: [del: word]. Illegible deletions: [del: ?].
8. Reproduce numerals, sums and dates exactly as written, including the form of
   abbreviation. Never normalise, expand or compute a figure.
9. Latin legal and chancery formulae appear inline inside German sentences --
   prepositional tags, case and document labels, procedural phrases. Transcribe
   them as Latin, in the form written. Do not Germanise or translate them.
10. If a page carries a page number, dateline, docket or file annotation,
   transcribe it in place.

Proper names -- of people, estates, villages, offices -- are the hardest part of
this hand and the most important to get right. Transcribe the letterforms you
actually see. Do not substitute a more familiar or more plausible name, and do
not regularise a name toward a commoner spelling.

Do not translate. Do not summarise. Do not correct the writer's grammar,
spelling or arithmetic. Do not comment.

After the [lang:] line, output the transcription and nothing else. No preamble,
no code fence."""

USER = ("Transcribe this manuscript page in full, following the rules exactly. "
        "Begin with the first mark on the page and continue to the last.")

# The three pages known not to be German. This is a hint, not an override: the
# model still declares what it sees, so a wrong hint shows up as a disagreement
# rather than silently forcing a reading. Kept per-page deliberately -- telling
# every page that it "might be French" would invite the loan-vocabulary trap
# rule 2 warns about, across all 869.
LANG_HINT = {
    ('283', '1'): 'French',
    ('283', '2'): 'French',
    ('72e', '1'): 'Polish',
}


def make_client():
    """Prefer a key in .anthropic_key over the environment.

    Claude Code exports an ANTHROPIC_API_KEY that is not always valid for
    direct API calls, and shell exports do not survive between tool calls, so a
    gitignored file next to the script is the reliable place to put one.
    """
    keyfile = os.path.join(ROOT, '.anthropic_key')
    if os.path.isfile(keyfile):
        key = open(keyfile, encoding='utf-8').read().strip()
        if key:
            return anthropic.Anthropic(api_key=key)
    if not os.environ.get('ANTHROPIC_API_KEY'):
        sys.exit('No API key. Put one in .anthropic_key (gitignored) or export '
                 'ANTHROPIC_API_KEY.')
    return anthropic.Anthropic()


def load_pages():
    rows = []
    with open(MAP, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            if r.get('image'):
                rows.append(r)
    return rows


def out_path(letter, page):
    return os.path.join(OUT, f'L{letter}_p{page}.json')


def already(letter, page):
    p = out_path(letter, page)
    if not os.path.isfile(p):
        return False
    try:
        return bool(json.load(open(p, encoding='utf-8')).get('text'))
    except Exception:
        return False


def image_block(image):
    path = os.path.join(SCANS, image)
    with open(path, 'rb') as f:
        data = base64.standard_b64encode(f.read()).decode()
    return {'type': 'image',
            'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': data}}


def request_params(row, model=None, effort=None):
    user = USER
    hint = LANG_HINT.get((str(row['letter']), str(row['page'])))
    if hint:
        user += (f' This page is known to be in {hint}, not German; transcribe it '
                 f'in the language on the page.')
    p = dict(
        model=model or MODEL,
        max_tokens=MAX_TOKENS,
        system=[{'type': 'text', 'text': SYSTEM,
                 'cache_control': {'type': 'ephemeral'}}],
        messages=[{'role': 'user',
                   'content': [image_block(row['image']),
                               {'type': 'text', 'text': user}]}],
    )
    # Thinking is deliberately not set: Opus 5 and Fable 5.1 both run adaptive
    # thinking by default, and Fable 5.1 rejects any explicit configuration.
    if effort:
        p['output_config'] = {'effort': effort}
    return p


def save(row, text, usage, extra=None):
    rec = {'letter': row['letter'], 'page': row['page'], 'image': row['image'],
           'model': (extra or {}).pop('model', MODEL),
           'text': text, 'usage': usage}
    if extra:
        rec.update(extra)
    os.makedirs(OUT, exist_ok=True)
    with open(out_path(row['letter'], row['page']), 'w',
              encoding='utf-8', newline='\n') as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)


def run_live(rows, client, model=None, effort=None):
    done = cost_in = cost_out = 0
    t0 = time.time()
    for i, row in enumerate(rows, 1):
        tag = f"L{row['letter']} p{row['page']}"
        if already(row['letter'], row['page']):
            print(f'  [{i}/{len(rows)}] {tag} - already done, skipping')
            continue
        try:
            with client.messages.stream(**request_params(row, model, effort)) as s:
                msg = s.get_final_message()
        except anthropic.APIStatusError as e:
            print(f'  [{i}/{len(rows)}] {tag} - API error {e.status_code}: {e.message}')
            continue
        except anthropic.APIConnectionError as e:
            print(f'  [{i}/{len(rows)}] {tag} - connection error: {e}')
            continue
        text = '\n'.join(b.text for b in msg.content if b.type == 'text').strip()
        u = msg.usage
        usage = {'input': u.input_tokens, 'output': u.output_tokens,
                 'cache_read': getattr(u, 'cache_read_input_tokens', 0) or 0,
                 'cache_write': getattr(u, 'cache_creation_input_tokens', 0) or 0}
        save(row, text, usage, {'model': model or MODEL})
        cost_in += usage['input'] + usage['cache_read'] + usage['cache_write']
        cost_out += usage['output']
        done += 1
        print(f"  [{i}/{len(rows)}] {tag} - {len(text.splitlines())} lines, "
              f"{usage['output']} out tok")
    dt = time.time() - t0
    # Cache reads/writes are cheaper than the headline input rate; costing them
    # at it over-counts slightly, so this is a safe ceiling rather than a guess.
    pi, po = PRICES.get(model or MODEL, (5, 25))
    est = cost_in / 1e6 * pi + cost_out / 1e6 * po
    print(f'\n{done} page(s) in {dt:.0f}s  |  {cost_in:,} in / {cost_out:,} out tok'
          f'  |  <= ${est:.2f} at live rates (Batch API halves it)')
    if done:
        print(f'per page: {cost_in//done:,} in / {cost_out//done:,} out'
              f'  |  <= ${est/done:.3f}')


def run_batch(rows, client, model=None, effort=None):
    todo = [r for r in rows if not already(r['letter'], r['page'])]
    if not todo:
        print('nothing to do - every page already has a second witness')
        return
    print(f'submitting {len(todo)} page(s) to the Batch API (50% of live rates)')
    reqs = [{'custom_id': f"L{r['letter']}_p{r['page']}",
             'params': request_params(r, model, effort)} for r in todo]
    index = {q['custom_id']: r for q, r in zip(reqs, todo)}
    batches = []
    for i in range(0, len(reqs), 100):          # keep each request payload sane
        chunk = reqs[i:i + 100]
        b = client.messages.batches.create(requests=chunk)
        batches.append(b.id)
        print(f'  batch {b.id}  ({len(chunk)} pages)')
    state = os.path.join(OUT, '_batches.json')
    os.makedirs(OUT, exist_ok=True)
    json.dump({'batches': batches, 'model': model or MODEL,
               'index': {k: v for k, v in index.items()}},
              open(state, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\nwrote {state}\nrun  python retranscribe.py --collect  once they finish')


def run_collect(client):
    state = os.path.join(OUT, '_batches.json')
    if not os.path.isfile(state):
        print('no batches in flight'); return
    st = json.load(open(state, encoding='utf-8'))
    index = st['index']
    pending = []
    got = 0
    for bid in st['batches']:
        b = client.messages.batches.retrieve(bid)
        if b.processing_status != 'ended':
            print(f'  {bid}: {b.processing_status} - not ready')
            pending.append(bid); continue
        for res in client.messages.batches.results(bid):
            row = index.get(res.custom_id)
            if row is None:
                continue
            if res.result.type != 'succeeded':
                print(f'  {res.custom_id}: {res.result.type}')
                continue
            msg = res.result.message
            text = '\n'.join(bl.text for bl in msg.content if bl.type == 'text').strip()
            u = msg.usage
            save(row, text, {'input': u.input_tokens, 'output': u.output_tokens,
                             'cache_read': getattr(u, 'cache_read_input_tokens', 0) or 0,
                             'cache_write': getattr(u, 'cache_creation_input_tokens', 0) or 0},
                 {'model': st.get('model', MODEL), 'batch_id': bid})
            got += 1
        print(f'  {bid}: collected')
    print(f'\ncollected {got} page(s)')
    if pending:
        st['batches'] = pending
        json.dump(st, open(state, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{len(pending)} batch(es) still running')
    else:
        os.remove(state)


# Chosen so the comparison can be scored, not just eyeballed:
#   1/1     three errors I read off the scan myself (Rußland / Congreß / schleunig)
#   48/1    + 302/1  the twin - two existing witnesses and several confirmed readings
#   31/2    the Henrichs / Hainrich name split
#   63/1    Schreibn;  87/2  figures + a page-break fragment
#   136/10  a badly garbled passage;  291/2  konzler / Geheimte / gezahlet
PILOT = [('1', '1'), ('48', '1'), ('302', '1'), ('31', '2'),
         ('63', '1'), ('87', '2'), ('136', '10'), ('291', '2')]

# Models the sweep compares. Tag is the witness-directory suffix.
SWEEP = [('claude-opus-5', 'opus'), ('claude-sonnet-5', 'sonnet')]


def run_check(client, model):
    """One minimal call, to prove the key works before spending anything."""
    try:
        r = client.messages.create(model=model, max_tokens=4,
                                   messages=[{'role': 'user', 'content': 'hi'}])
        print(f'OK - key works, {model} reachable '
              f'({r.usage.input_tokens} in / {r.usage.output_tokens} out tokens)')
        return True
    except anthropic.AuthenticationError as e:
        print(f'FAILED - the key was rejected: {e.message}')
    except anthropic.PermissionDeniedError as e:
        print(f'FAILED - key lacks permission for {model}: {e.message}')
    except anthropic.NotFoundError:
        print(f'FAILED - model {model} not available on this account')
    except anthropic.APIStatusError as e:
        print(f'FAILED - {e.status_code}: {e.message}')
        if e.status_code == 400 and 'credit' in (e.message or '').lower():
            print('        (looks like the account needs credit topping up)')
    except anthropic.APIConnectionError as e:
        print(f'FAILED - could not reach the API: {e}')
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pilot', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--letters', help='comma-separated letter ids')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--model', default=MODEL, help=f'default {MODEL}')
    ap.add_argument('--effort', choices=['low', 'medium', 'high', 'xhigh', 'max'],
                    help='output_config.effort; omit for the model default')
    ap.add_argument('--tag', help='write to retranscription-<tag>/ instead, so a '
                                  'second model does not overwrite the first')
    ap.add_argument('--sweep', action='store_true',
                    help='run the pilot pages on every model in SWEEP, each to '
                         'its own witness directory, for a like-for-like compare')
    ap.add_argument('--check', action='store_true',
                    help='verify the API key with one tiny call (costs ~$0.0001)')
    ap.add_argument('--batch', action='store_true', help='use the Batch API')
    ap.add_argument('--collect', action='store_true', help='fetch finished batches')
    a = ap.parse_args()

    global OUT
    if getattr(a, 'tag', None):
        OUT = os.path.join(ROOT, f'retranscription-{a.tag}')

    client = make_client()
    if a.check:
        ok = all(run_check(client, m) for m, _ in SWEEP)
        sys.exit(0 if ok else 1)
    if a.collect:
        run_collect(client); return

    rows = load_pages()
    if a.pilot:
        want = set(PILOT)
        rows = [r for r in rows if (r['letter'], r['page']) in want]
    elif a.letters:
        want = {s.strip() for s in a.letters.split(',')}
        rows = [r for r in rows if r['letter'] in want]
    elif not a.all:
        n = sum(1 for r in rows if already(r['letter'], r['page']))
        print(f'{len(rows)} pages with scans; {n} already have a second witness')
        print('pass --pilot, --letters, or --all'); return
    if a.limit:
        rows = rows[:a.limit]

    if a.sweep:
        base = OUT
        for model, tag in SWEEP:
            OUT = os.path.join(ROOT, f'retranscription-{tag}')
            print(f'=== {model} -> {os.path.basename(OUT)}/ ===')
            run_live(rows, client, model, a.effort)
            print()
        OUT = base
        print('now run:  python compare_pilot.py')
        return

    print(f'{len(rows)} page(s) selected, model {MODEL}\n')
    (run_batch if a.batch else run_live)(rows, client)


if __name__ == '__main__':
    main()
