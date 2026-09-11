# -*- coding: utf-8 -*-
"""
Adjudicate the open rows of a transcription-fix sheet, in batches.

    python adjudicate_fixes.py --unit oe1bu14526 --dry-run   # spend nothing
    python adjudicate_fixes.py --unit oe1bu9454 --batch       # half price
    python adjudicate_fixes.py --unit oe1bu9454 --collect
    python adjudicate_fixes.py --unit oe1bu14526 --score      # against hand rulings

triage_fixes.py applies the bars a rule can apply, and on a formulaic holding
that is most of the work. On the correspondence it settles one row in 2,868: the
letters are varied prose, so "the corpus attests the other form" almost never
has an answer, and what is left is 2,840 judgements about German on a page.

Those judgements are the same shape 701 times over, which is what a batch is
for. Each request carries one document's proposals with the corpus lines around
them, and the standing rules as the system prompt - docs/EDITORIAL_RULES.md
itself, so the rules live in one place and drift nowhere.

What comes back is a decision in the sheet's own vocabulary:

    y                     apply the proposal as it stands
    n                     leave the transcription alone
    <a reading>           apply this instead of the proposal
    @<line> old -> new    apply exactly this, where the row could not be anchored
    ?                     the editor must decide - names, figures, real doubt

Nothing is applied here. The decisions go into the sheet, and
apply_transcription_fixes.py records and acts on them as for any other ruling.

--score is the part that earns the trust: it runs the same prompt over rows an
editor has already ruled on and reports the agreement, so the thing can be
measured on known answers before being turned loose on unknown ones.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, time, argparse
from collections import defaultdict, Counter

import anthropic
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL = 'claude-opus-5'
MAX_TOKENS = 8000
CONTEXT = 2          # corpus lines either side of the anchor
PRICES = {'claude-opus-5': (5, 25)}

TOOL = {
    'name': 'submit_rulings',
    'description': 'One ruling per proposal, in the order given.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'rulings': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'key': {'type': 'string',
                                'description': 'The proposal\'s key, copied exactly.'},
                        'decision': {
                            'type': 'string',
                            'description': "'y' to apply as proposed; 'n' to leave "
                                           "the transcription alone; '?' if the "
                                           "editor must decide; a reading to apply "
                                           "instead of the proposal; or "
                                           "'@<line> old -> new' to name the fix "
                                           "exactly where the row is not anchored."},
                        'why': {'type': 'string',
                                'description': 'One clause. The evidence, not the '
                                               'restatement.'},
                    },
                    'required': ['key', 'decision', 'why'],
                },
            },
        },
        'required': ['rulings'],
    },
}


def rules_text():
    p = os.path.join(ROOT, 'docs', 'EDITORIAL_RULES.md')
    return io.open(p, encoding='utf-8').read()


def system_prompt():
    return f"""\
You are adjudicating proposed corrections to a diplomatic transcription of
German archival manuscripts, against the edition's standing rules. The rules are
reproduced in full below and they govern: where they settle a proposal, follow
them; where they do not, say so with '?' rather than guessing.

The proposals come from the translator, which reports what it could not make
sense of. They are often right and often not, and the only thing worse than
missing a correction is inventing one: this transcription is the edition's
record, and a plausible improvement that is not on the page destroys the
evidence that the reading was ever in doubt.

For each proposal you are given the corpus lines around it. Judge on those lines
and on the rules. In particular:

  * a word broken across a line is mended on the half that is wrong, and the
    page's own line division is kept. If the transcription reads `ver-/abgerüdeter`
    and the word is `verabredeter`, the ruling is '@<line of the second half>
    abgerüdeter -> abredeter', not a rewrite of the whole span;
  * where only part of a multi-word proposal is sound, give the reading you would
    apply rather than 'y';
  * '?' is for a genuine editorial question: a personal or place name, a figure, an
    abbreviation the scribe wrote, or a passage the page could honestly read two
    ways. It is NOT for a proposal that is merely untidy. Scored against 231 rows
    an editor had already ruled on, this prompt deferred on 138 of them while its
    own reasons named the answer - "only the Entsagung half is a demonstrable
    one-letter slip" is a ruling, not a question. Where you can name the line and
    the token, name them.
  * A proposal may be part sound and part guess. Rule on the sound part: give the
    '@<line> old -> new' for the half you can demonstrate and leave the rest of
    the span alone. That is a better answer than '?' and a much better one than
    'y'.
  * A proposal quoting two variant spellings of the same word - 'Abten / Ahten' -
    is two fixes, not an ambiguity. Give both, separated by ' ; '.

Answer for every proposal you are given, with its key copied exactly.

--- THE EDITION'S STANDING RULES ---

{rules_text()}"""


def block(rows, lines):
    """One document's proposals, each with the corpus lines around it."""
    out = []
    for r in rows:
        out.append(f"KEY {r['key']}")
        out.append(f"  transcription reads : {r['transcribed']!r}")
        out.append(f"  proposal            : {r['proposed']!r}")
        if r.get('why'):
            out.append(f"  translator's reason : {r['why'][:300]}")
        out.append(f"  this row needs      : {r['needs']}")
        ln = (r.get('line') or '').split()
        if ln and ln[0].isdigit():
            n = int(ln[0])
            out.append(f"  corpus lines (the anchor is line {n}):")
            for j in range(max(1, n - CONTEXT), min(len(lines), n + CONTEXT + 1)):
                mark = '>>' if j == n else '  '
                out.append(f"    {mark}{j}: {lines[j-1]}")
        else:
            out.append('  not anchored: the quoted German is on no single line. '
                       'Rule "?" unless you can name the line and token yourself.')
        out.append('')
    return '\n'.join(out)


def open_rows(sheet, only_ruled=False):
    """The rows to work on: the open ones, or - for scoring - the ruled ones.

    Scoring has to include rows whose ruling has already been applied, or the
    only thing measurable is the refusals, and a validation that cannot see a
    single correct 'y' is no validation at all.
    """
    rows = list(csv.DictReader(io.open(sheet, encoding='utf-8-sig')))
    out = []
    for r in rows:
        ruled = bool((r.get('decision') or '').strip())
        if only_ruled:
            if ruled:
                out.append(r)
            continue
        if not (r.get('needs') or '') or r['needs'] == 'applied':
            continue
        if not ruled:
            out.append(r)
    return rows, out


def requests_for(rows, lines, sys_prompt, model=None):
    by_doc = defaultdict(list)
    for r in rows:
        by_doc[r['pad']].append(r)
    reqs = []
    for pad, rs in sorted(by_doc.items()):
        # keep a request small enough to answer carefully
        for i in range(0, len(rs), 25):
            chunk = rs[i:i + 25]
            reqs.append((f'{pad}_{i//25}', {
                'model': model or MODEL,
                'max_tokens': MAX_TOKENS,
                'system': [{'type': 'text', 'text': sys_prompt,
                            'cache_control': {'type': 'ephemeral'}}],
                'tools': [TOOL],
                'tool_choice': {'type': 'tool', 'name': 'submit_rulings'},
                'messages': [{'role': 'user', 'content':
                              f'Document {pad}. Rule on each proposal.\n\n'
                              + block(chunk, lines)}],
            }))
    return reqs


def out_dir(slug):
    d = os.path.join(ROOT, 'cache', 'adjudication', slug)
    os.makedirs(d, exist_ok=True)
    return d


def client():
    """Prefer .anthropic_key over the environment, as the other scripts do: the
    exported ANTHROPIC_API_KEY here is not valid for direct calls."""
    p = os.path.join(ROOT, '.anthropic_key')
    if os.path.isfile(p):
        key = io.open(p, encoding='utf-8').read().strip()
        if key:
            return anthropic.Anthropic(api_key=key)
    if not os.environ.get('ANTHROPIC_API_KEY'):
        sys.exit('No API key. Put one in .anthropic_key (gitignored) or export '
                 'ANTHROPIC_API_KEY.')
    return anthropic.Anthropic()


def harvest(msg):
    for b in msg.content:
        if b.type == 'tool_use' and b.name == 'submit_rulings':
            return (b.input or {}).get('rulings') or []
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit')
    ap.add_argument('--batch', action='store_true')
    ap.add_argument('--collect', action='store_true')
    ap.add_argument('--score', action='store_true',
                    help='rule on rows already ruled by hand, and compare')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--model', default=None)
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    unit = unitlib.one_unit(slug)
    sheet = os.path.join(unitlib.review_dir(slug), 'transcription_fixes.csv')
    lines = io.open(os.path.join(unit.dir, unit.get('corpus') or 'corpus.txt'),
                    encoding='utf-8').read().split('\n')
    state = os.path.join(out_dir(slug), '_batches.json')
    sp = system_prompt()

    if a.collect:
        st = json.load(io.open(state, encoding='utf-8'))
        cl = client()
        got, pend, cin, cout = [], [], 0, 0
        for bid in st['batches']:
            b = cl.messages.batches.retrieve(bid)
            if b.processing_status != 'ended':
                print(f'  {bid}: {b.processing_status} - not ready')
                pend.append(bid)
                continue
            for res in cl.messages.batches.results(bid):
                if res.result.type != 'succeeded':
                    print(f'  {res.custom_id}: {res.result.type}')
                    continue
                m = res.result.message
                got.extend(harvest(m))
                u = m.usage
                cin += u.input_tokens + (getattr(u, 'cache_read_input_tokens', 0) or 0)
                cout += u.output_tokens
            print(f'  {bid}: collected')
        dest = os.path.join(out_dir(slug), 'rulings.json')
        prior = json.load(io.open(dest, encoding='utf-8')) if os.path.isfile(dest) else []
        by_key = {r['key']: r for r in prior}
        by_key.update({r['key']: r for r in got if r.get('key')})
        json.dump(list(by_key.values()), io.open(dest, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        cost = cin / 1e6 * PRICES[MODEL][0] + cout / 1e6 * PRICES[MODEL][1]
        print(f'\n{len(got)} ruling(s) collected, {len(by_key)} held in {dest}')
        print(f'{cin:,} in / {cout:,} out tok  |  <= ${cost:.2f} at live rates '
              f'(the Batch API halves it)')
        if pend:
            st['batches'] = pend
            json.dump(st, io.open(state, 'w', encoding='utf-8'), indent=1)
        elif os.path.isfile(state):
            os.remove(state)
        return

    rows, todo = open_rows(sheet, only_ruled=a.score)
    if a.limit:
        todo = todo[:a.limit]
    reqs = requests_for(todo, lines, sp, a.model)
    print(f'{len(todo)} row(s) to rule on, in {len(reqs)} request(s)')
    print(f'system prompt: {len(sp):,} chars (cached)')
    if a.dry_run:
        if reqs:
            print('\n--- first request ---')
            print(reqs[0][1]['messages'][0]['content'][:2000])
        return
    if not reqs:
        return

    cl = client()
    if a.batch:
        ids = []
        for i in range(0, len(reqs), 100):
            chunk = [{'custom_id': cid, 'params': p} for cid, p in reqs[i:i + 100]]
            b = cl.messages.batches.create(requests=chunk)
            ids.append(b.id)
            print(f'  batch {b.id}  ({len(chunk)} request(s))')
        json.dump({'batches': ids, 'model': a.model or MODEL, 'score': a.score},
                  io.open(state, 'w', encoding='utf-8'), indent=1)
        print(f'\nwrote {state}\nrun with --collect once they finish')
        return

    got, cin, cout = [], 0, 0
    t0 = time.time()
    for i, (cid, params) in enumerate(reqs, 1):
        with cl.messages.stream(**params) as s:
            m = s.get_final_message()
        got.extend(harvest(m))
        u = m.usage
        cin += u.input_tokens + (getattr(u, 'cache_read_input_tokens', 0) or 0)
        cout += u.output_tokens
        print(f'  [{i}/{len(reqs)}] {cid}: {len(harvest(m))} ruling(s)')
    dest = os.path.join(out_dir(slug), 'rulings.json')
    json.dump(got, io.open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cost = cin / 1e6 * PRICES[MODEL][0] + cout / 1e6 * PRICES[MODEL][1]
    print(f'\n{len(got)} ruling(s) in {time.time()-t0:.0f}s  |  <= ${cost:.2f}')
    print(f'wrote {dest}')


if __name__ == '__main__':
    main()
