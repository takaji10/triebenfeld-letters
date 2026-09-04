# -*- coding: utf-8 -*-
"""English translation of the letters, one letter per request, page by page out.

    python translate.py --check                 # validate key/model, ~4 tokens
    python translate.py --pilot                 # the 12-letter convention sample, live
    python translate.py --letters 48,302,136    # named letters, live
    python translate.py --all --batch           # everything outstanding, at half price
    python translate.py --collect               # merge finished batches
    python translate.py --rerun-flagged --tag B # second witness, flagged pages only

Why the unit of work is a LETTER and not a page, unlike retranscribe.py: there
each page was an independent image and context would have been contamination.
Here sentences run across page breaks, pronouns point back several pages, and
half the business of a letter is only intelligible from its opening. So the
whole letter goes in and per-page segments come back, keyed (letter_id, page) -
the one join key that survives a corpus edit, since line numbers do not.

The standing instruction, and the reason this script exists in this shape:
translation is a fluency machine. Handed a corrupt German sentence a model will
produce a smooth English one, silently turning a transcription error into a
fluent falsehood no reader can catch. So the model is required to report what it
could not parse instead of inventing sense, and its guesses at what the German
*should* say are kept in a separate field where they cannot leak into the text
the site displays. check_translations.py then verifies mechanically that every
numeral, every settled name and every mark of doubt survived the crossing.

Nothing here writes to the corpus, letters.json, or anything regenerate.py
rebuilds. Output goes to translation-raw/, and only publish_translations.py
moves it into site/_data/translations/.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, csv, json, time, argparse

import yaml
import anthropic
import unitlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
LETTERS = os.path.join(ROOT, 'corpus', 'letters.json')
GLOSSARY = os.path.join(ROOT, 'reference', 'translation_glossary.yml')
CORRESPONDENTS = os.path.join(UNIT.dir, 'correspondents.json')

MODEL = 'claude-opus-5'
MAX_TOKENS = 16000

# $ per million tokens (input, output), for the run's own cost readout.
PRICES = {'claude-opus-5': (5, 25), 'claude-fable-5-1': (10, 50),
          'claude-sonnet-5': (2, 10), 'claude-opus-4-8': (5, 25)}

# Documents not in German. 72e is the Polish duplicate of the German 72d;
# 283 is a French letter from a Congress correspondent.
LANG = {'72e': 'Polish', '283': 'French'}

# The convention-setting sample: deliberately spans the range rather than
# picking easy letters. Clean late letters, known-bad ones, both non-German
# documents, and the 48/302 twin - the only document with two witnesses.
PILOT = ['48', '302', '136', '291', '17', '72e', '283', '290', '297', '3', '215', '247']


# ----------------------------------------------------------------- prompt --

def load_glossary():
    return yaml.safe_load(open(GLOSSARY, encoding='utf-8'))


def glossary_table(g):
    """The termbase, flattened into the form the model actually needs."""
    out = []
    for sect, head in (('currency', 'CURRENCY'), ('honorifics', 'FORMS OF ADDRESS'),
                       ('formulas', 'CLOSING FORMULAS'), ('terms', 'TERMS OF ART')):
        out.append(f'\n{head}')
        for e in g[sect]:
            if e['policy'] == 'keep':
                rule = f"keep as `{e['render']}`"
            else:
                rule = f"render as `{e['render']}`"
            line = f"  {e['term']} -> {rule}"
            if e.get('gloss'):
                line += f"   ({e['gloss']})"
            out.append(line)
    out.append('\nRARE CONFUSION PAIRS - flag EVERY occurrence, without exception:')
    for e in g['rare_pairs']:
        out.append(f"  {e['pair'][0]} / {e['pair'][1]}: {e['note']}")
    out.append('\nWATCH-LIST - common, so flag only where genuinely ambiguous in context:')
    for e in g['watchlist']:
        out.append(f"  {e['pair'][0]} / {e['pair'][1]}: {e['note']}")
    return '\n'.join(out)


def build_system(g):
    return f"""\
You are translating a scholarly edition of letters written between 1798 and 1816, \
mostly by a Prussian estate agent, the Kriegs- und Forstrath von Triebenfeld, to \
his employer Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen. They concern \
estates in South Prussia and the Duchy of Warsaw, debts, lawsuits, the Napoleonic \
wars and the Congress of Vienna.

The German you are given was transcribed from Kurrent handwriting by machine and \
then corrected by hand over many passes. It is largely sound but it is not \
perfect, and the imperfections that remain are exactly the kind that survive \
translation invisibly: corrupted proper nouns that look like ordinary names, \
unreliable figures, and single-letter confusions that reverse a sentence's sense \
while leaving it fluent.

So the governing rule of this work is:

  TRANSLATE WHAT THE GERMAN ACTUALLY SAYS, NOT WHAT IT OUGHT TO SAY.

If a passage does not parse, do not quietly repair it into good English. Record \
it in `unparseable` and translate as much as you honestly can. If a passage \
parses two ways that differ in meaning, do not silently pick the smoother one: \
put it in `flagged` with both readings. A visibly doubtful English sentence is a \
better outcome than a confident wrong one. This edition's stated principle is \
that readings which could not be settled from evidence are left alone rather than \
guessed at, and your output is held to the same standard.

HOUSE STYLE
{g['house_style']}

NUMBERS AND NAMES - carried across, never re-derived:
  * Reproduce every numeral exactly as written. Do not convert, recompute, \
correct, modernise or tidy a figure, even when it is obviously wrong. A sum that \
reads 23000 in the German reads 23000 in the English.
  * Reproduce every proper noun exactly as spelled in the German. Never \
translate, normalise or "correct" a name, and never supply a name the German \
does not have. Personal and place names are the least reliable part of this \
transcription; silently improving one destroys the evidence that it was wrong.
  * List what you carried across in the `names` and `numbers` fields so it can \
be checked mechanically.

MARKS OF DOUBT - the German's holes stay holes in the English:
  * `[?]`      (illegible in the manuscript)   -> render as `[illegible]`
  * `[word?]`  (an uncertain reading)          -> render as `[uncertain: word]`
  * `[...]`    (a gap, or damaged page edge)   -> render as `[text lost]`
  Put each marker at the point in the English sentence where it belongs. Never \
bridge a gap with invented connective sense. Report the number of markers you \
emitted for each page in `marker_count`; it is checked against the German.

EMENDATIONS - kept out of the translation:
  If you think you can see what the manuscript really said - that `Heinrich` is \
a misreading of `Hawich`, say - do NOT put your guess in the English. Put it in \
`emendation_suggestions`, with your reason. The translation carries the text as \
transcribed; proposed fixes to the transcription are a separate editorial matter \
and are reviewed against the manuscript by a human.

TERMBASE - use these renderings consistently, in every letter:
{glossary_table(g)}

Return one segment per manuscript page, in order, using the submit_translation \
tool. The page count of your answer must equal the page count you were given."""


TOOL = {
    'name': 'submit_translation',
    'description': 'Return the English translation, one segment per manuscript '
                   'page, with everything unsettled recorded rather than smoothed.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'pages': {
                'type': 'array',
                'description': 'One entry per manuscript page, in order.',
                'items': {
                    'type': 'object',
                    'properties': {
                        'page': {'type': 'integer',
                                 'description': 'Manuscript page number as given.'},
                        'en': {'type': 'string',
                               'description': 'The English translation of this page.'},
                        'confidence': {'type': 'string',
                                       'enum': ['high', 'medium', 'low'],
                                       'description': 'How sound the German was here.'},
                        'marker_count': {
                            'type': 'integer',
                            'description': 'How many [illegible]/[uncertain: ]/[text '
                                           'lost] markers you emitted on this page.'},
                        'unparseable': {
                            'type': 'array',
                            'description': 'Spans that do not parse. Do not repair them.',
                            'items': {'type': 'object', 'properties': {
                                'de': {'type': 'string'}, 'why': {'type': 'string'}},
                                'required': ['de', 'why']}},
                        'flagged': {
                            'type': 'array',
                            'description': 'Spans that parse two ways with different '
                                           'meanings, including every rare-pair occurrence.',
                            'items': {'type': 'object', 'properties': {
                                'de': {'type': 'string'},
                                'risk': {'type': 'string'},
                                'rendered_as': {'type': 'string'},
                                'alt': {'type': 'string'},
                                'why': {'type': 'string'}},
                                'required': ['de', 'rendered_as', 'alt']}},
                        'emendation_suggestions': {
                            'type': 'array',
                            'description': 'Guesses at what the manuscript really said. '
                                           'Never folded into the translation.',
                            'items': {'type': 'object', 'properties': {
                                'de': {'type': 'string'},
                                'proposed': {'type': 'string'},
                                'why': {'type': 'string'}},
                                'required': ['de', 'proposed']}},
                        'names': {'type': 'array', 'items': {'type': 'string'},
                                  'description': 'Proper nouns carried across.'},
                        'numbers': {'type': 'array', 'items': {'type': 'string'},
                                    'description': 'Numerals carried across.'},
                    },
                    'required': ['page', 'en', 'confidence', 'marker_count'],
                },
            },
        },
        'required': ['pages'],
    },
}


# ------------------------------------------------------------------- data --

def load_letters():
    """This unit's documents only.

    The corpus file is merged across units, so without the filter a run would
    translate every holding in the project and pay for all of it.
    """
    recs = json.load(open(LETTERS, encoding='utf-8'))
    return [r for r in recs if r.get('unit') == UNIT.slug]


def load_correspondents():
    if os.path.isfile(CORRESPONDENTS):
        return json.load(open(CORRESPONDENTS, encoding='utf-8'))
    return {}


def pad(letter_id):
    """oe1bu9454-048 - the same key the site and the cache use."""
    return UNIT.pad(letter_id)


def out_dir(tag=None):
    return os.path.join(ROOT, 'cache', 'translation-raw' + (f'-{tag}' if tag else ''))


def out_path(letter_id, tag=None):
    return os.path.join(out_dir(tag), pad(letter_id) + '.json')


def already(letter_id, tag=None):
    """Done means a usable result, not merely a file on disk.

    A batch can return a tool input whose `pages` is a partial JSON string
    rather than an array. That file is non-empty but worthless, and treating it
    as done would silently leave the letter untranslated for good, so the shape
    is checked rather than the truthiness."""
    p = out_path(letter_id, tag)
    if not os.path.isfile(p):
        return False
    try:
        pages = json.load(open(p, encoding='utf-8')).get('pages')
    except Exception:
        return False
    return bool(pages) and all(isinstance(x, dict) and x.get('en') for x in pages)


def german_for(rec):
    """The letter as the model sees it: reading text, page-delimited.

    `reading` is the flowed view - wrap marks resolved, catchwords dropped - and
    it still carries the [?] / [word?] / [...] marks of doubt, which is exactly
    what we want the translation to mirror. Pages are delimited explicitly
    rather than by a blank line: an ambiguous separator is precisely the kind of
    silent slippage this whole pipeline exists to prevent.
    """
    parts = []
    for p in rec['pages']:
        body = (p.get('reading') or p.get('diplomatic') or '').strip()
        parts.append(f"=== PAGE {p['page']} ===\n{body}")
    return '\n\n'.join(parts)


def user_block(rec, corr):
    lid = str(rec['letter_id'])
    c = corr.get(lid, {})
    meta = [f"Letter {lid}", f"Date: {rec.get('date_display') or 'undated'}"]
    if rec.get('place'):
        meta.append(f"Written at: {rec['place']}")
    if c.get('sender'):
        meta.append(f"Sender: {c['sender']}")
    if c.get('recipient'):
        meta.append(f"Recipient: {c['recipient']}")
    if not c.get('sender') or not c.get('recipient'):
        meta.append("(Correspondents not fully established - judge register from the "
                    "salutation and signature as they stand.)")
    meta.append(f"Manuscript pages: {len(rec['pages'])}")
    lang = LANG.get(lid)
    if lang:
        meta.append(f"NOTE: this document is in {lang}, not German. Translate from "
                    f"{lang}; the same rules apply.")
    return (f"{chr(10).join(meta)}\n\n"
            f"Translate the following, returning exactly {len(rec['pages'])} page "
            f"segment(s) via the submit_translation tool.\n\n{german_for(rec)}")


def request_params(rec, corr, system, model=None):
    return dict(
        model=model or MODEL,
        max_tokens=MAX_TOKENS,
        system=[{'type': 'text', 'text': system,
                 'cache_control': {'type': 'ephemeral'}}],
        tools=[TOOL],
        tool_choice={'type': 'tool', 'name': 'submit_translation'},
        messages=[{'role': 'user', 'content': user_block(rec, corr)}],
    )


def extract(msg):
    for b in msg.content:
        if b.type == 'tool_use' and b.name == 'submit_translation':
            return normalise(b.input)
    return None


def normalise(payload):
    """Tool input occasionally arrives with `pages` as a JSON *string* rather
    than an array - roughly 3% of a 301-letter batch. The content is intact and
    well-formed, it has simply been serialised one level too far, so parse it
    rather than throwing away a letter that cost real money to produce."""
    if not isinstance(payload, dict):
        return payload
    pages = payload.get('pages')
    if isinstance(pages, str):
        try:
            payload = dict(payload, pages=json.loads(pages))
        except json.JSONDecodeError:
            return payload
    pages = payload.get('pages')
    if isinstance(pages, list):
        fixed = []
        for p in pages:
            if isinstance(p, str):
                try:
                    p = json.loads(p)
                except json.JSONDecodeError:
                    continue
            if isinstance(p, dict):
                fixed.append(p)
        payload = dict(payload, pages=fixed)
    return payload


def save(rec, payload, usage, tag=None, extra=None):
    out = {'letter': str(rec['letter_id']), 'pad': pad(rec['letter_id']),
           'n_pages': len(rec['pages']),
           'model': (extra or {}).get('model', MODEL),
           'pages': (payload or {}).get('pages', []), 'usage': usage}
    if extra:
        out.update({k: v for k, v in extra.items() if k != 'model'})
    os.makedirs(out_dir(tag), exist_ok=True)
    with open(out_path(rec['letter_id'], tag), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


def usage_of(msg):
    u = msg.usage
    return {'input': u.input_tokens, 'output': u.output_tokens,
            'cache_read': getattr(u, 'cache_read_input_tokens', 0) or 0,
            'cache_write': getattr(u, 'cache_creation_input_tokens', 0) or 0}


def report_cost(done, cost_in, cost_out, model, dt, unit='letter'):
    pi, po = PRICES.get(model or MODEL, (5, 25))
    est = cost_in / 1e6 * pi + cost_out / 1e6 * po
    print(f'\n{done} {unit}(s) in {dt:.0f}s  |  {cost_in:,} in / {cost_out:,} out tok'
          f'  |  <= ${est:.2f} at live rates (Batch API halves it)')
    if done:
        print(f'per {unit}: {cost_in // done:,} in / {cost_out // done:,} out'
              f'  |  <= ${est / done:.3f}')


# ------------------------------------------------------------------- runs --

def make_client():
    """Prefer a key in .anthropic_key over the environment - same reasoning as
    retranscribe.py: the exported ANTHROPIC_API_KEY is not always valid for
    direct calls and shell exports do not survive between tool calls."""
    keyfile = os.path.join(ROOT, '.anthropic_key')
    if os.path.isfile(keyfile):
        key = open(keyfile, encoding='utf-8').read().strip()
        if key:
            return anthropic.Anthropic(api_key=key)
    if not os.environ.get('ANTHROPIC_API_KEY'):
        sys.exit('No API key. Put one in .anthropic_key (gitignored) or export '
                 'ANTHROPIC_API_KEY.')
    return anthropic.Anthropic()


def run_live(recs, client, system, corr, model=None, tag=None):
    done = cost_in = cost_out = 0
    t0 = time.time()
    for i, rec in enumerate(recs, 1):
        lid = str(rec['letter_id'])
        if already(lid, tag):
            print(f'  [{i}/{len(recs)}] L{lid} - already done, skipping')
            continue
        try:
            with client.messages.stream(**request_params(rec, corr, system, model)) as s:
                msg = s.get_final_message()
        except anthropic.APIStatusError as e:
            print(f'  [{i}/{len(recs)}] L{lid} - API error {e.status_code}: {e.message}')
            continue
        except anthropic.APIConnectionError as e:
            print(f'  [{i}/{len(recs)}] L{lid} - connection error: {e}')
            continue
        payload = extract(msg)
        if payload is None:
            print(f'  [{i}/{len(recs)}] L{lid} - no tool call returned, skipped')
            continue
        usage = usage_of(msg)
        save(rec, payload, usage, tag, {'model': model or MODEL})
        got = len(payload.get('pages', []))
        warn = '' if got == len(rec['pages']) else f'  !! {got} segs for {len(rec["pages"])} pages'
        cost_in += usage['input'] + usage['cache_read'] + usage['cache_write']
        cost_out += usage['output']
        done += 1
        print(f"  [{i}/{len(recs)}] L{lid} - {got} page(s), {usage['output']} out tok{warn}")
    report_cost(done, cost_in, cost_out, model, time.time() - t0)


def run_batch(recs, client, system, corr, model=None, tag=None):
    todo = [r for r in recs if not already(r['letter_id'], tag)]
    if not todo:
        print('nothing to do - every letter already translated')
        return
    print(f'submitting {len(todo)} letter(s) to the Batch API (50% of live rates)')
    reqs = [{'custom_id': f"L{r['letter_id']}",
             'params': request_params(r, corr, system, model)} for r in todo]
    batches = []
    for i in range(0, len(reqs), 100):
        chunk = reqs[i:i + 100]
        b = client.messages.batches.create(requests=chunk)
        batches.append(b.id)
        print(f'  batch {b.id}  ({len(chunk)} letters)')
    os.makedirs(out_dir(tag), exist_ok=True)
    state = os.path.join(out_dir(tag), '_batches.json')
    json.dump({'batches': batches, 'model': model or MODEL,
               'letters': [str(r['letter_id']) for r in todo]},
              open(state, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\nwrote {state}\nrun  python translate.py --collect'
          + (f' --tag {tag}' if tag else '') + '  once they finish')


def run_collect(client, recs_by_id, tag=None):
    state = os.path.join(out_dir(tag), '_batches.json')
    if not os.path.isfile(state):
        print('no batches in flight')
        return
    st = json.load(open(state, encoding='utf-8'))
    pending, got = [], 0
    cost_in = cost_out = 0
    for bid in st['batches']:
        b = client.messages.batches.retrieve(bid)
        if b.processing_status != 'ended':
            print(f'  {bid}: {b.processing_status} - not ready')
            pending.append(bid)
            continue
        for res in client.messages.batches.results(bid):
            lid = res.custom_id[1:]
            rec = recs_by_id.get(lid)
            if rec is None:
                continue
            if res.result.type != 'succeeded':
                print(f'  {res.custom_id}: {res.result.type}')
                continue
            msg = res.result.message
            payload = extract(msg)
            if payload is None:
                print(f'  {res.custom_id}: no tool call returned')
                continue
            usage = usage_of(msg)
            save(rec, payload, usage, tag,
                 {'model': st.get('model', MODEL), 'batch_id': bid})
            cost_in += usage['input'] + usage['cache_read'] + usage['cache_write']
            cost_out += usage['output']
            got += 1
        print(f'  {bid}: collected')
    report_cost(got, cost_in, cost_out, st.get('model'), 0.0)
    if pending:
        st['batches'] = pending
        json.dump(st, open(state, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{len(pending)} batch(es) still running')
    elif os.path.isfile(state):
        os.remove(state)


def run_check(client, model=None):
    """Four tokens, to prove the key and model work before spending anything."""
    try:
        msg = client.messages.create(
            model=model or MODEL, max_tokens=4,
            messages=[{'role': 'user', 'content': 'Reply with the single word: ready'}])
        print('key and model OK -',
              ''.join(b.text for b in msg.content if b.type == 'text').strip())
    except anthropic.APIStatusError as e:
        sys.exit(f'API error {e.status_code}: {e.message}')


def flagged_letters(tag=None):
    """The subset genuinely worth a second witness: letters containing one of
    the rare confusion pairs.

    The first cut of this selected any letter carrying a flag or an unparseable
    span, on the assumption that would be a small minority. Measured against the
    finished first pass it is 859 of 864 pages - practically the whole corpus,
    because a careful translator finds something worth remarking on nearly
    everywhere. Re-running all of it would cost as much as the original pass and
    almost all of it would be thrown away, because collate_translations.py can
    only adjudicate a disagreement where the glossary defines two semantic poles
    to sort the readings into. That is the rare pairs, and nothing else.

    So the selection is made from the German source rather than from the
    model's flags: 35 pages across 26 letters, which is what a targeted second
    witness actually means here.
    """
    recs = load_letters()
    pairs = load_glossary()['rare_pairs']
    out = []
    for r in recs:
        for p in r['pages']:
            de = p.get('reading') or p.get('diplomatic') or ''
            if any(re.search(e['pattern'], de, re.I) for e in pairs):
                out.append(str(r['letter_id']))
                break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--pilot', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--letters', default='')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--batch', action='store_true')
    ap.add_argument('--collect', action='store_true')
    ap.add_argument('--rerun-flagged', action='store_true')
    ap.add_argument('--tag', default=None)
    ap.add_argument('--model', default=None)
    ap.add_argument('--dry-run', action='store_true',
                    help='show what would be sent, spend nothing')
    a = ap.parse_args()

    recs = load_letters()
    by_id = {str(r['letter_id']): r for r in recs}
    corr = load_correspondents()
    system = build_system(load_glossary())

    if a.check:
        run_check(make_client(), a.model)
        return

    if a.collect:
        run_collect(make_client(), by_id, a.tag)
        return

    if a.rerun_flagged:
        ids = flagged_letters()          # read the first witness, write the second
        if not ids:
            print('no flagged letters yet - run a first pass first')
            return
        print(f'{len(ids)} letter(s) contain a rare confusion pair - the only spans '
              f'a second witness can actually adjudicate')
    elif a.pilot:
        ids = PILOT
    elif a.letters:
        ids = [x.strip() for x in a.letters.split(',') if x.strip()]
    elif a.all:
        ids = [str(r['letter_id']) for r in recs]
    else:
        ap.error('pick one of --check / --pilot / --letters / --all / '
                 '--collect / --rerun-flagged')

    chosen = []
    for lid in ids:
        r = by_id.get(lid)
        if r is None:
            print(f'  L{lid}: no such letter, skipped')
            continue
        if r.get('is_missing') or not (r.get('text') or '').strip():
            print(f'  L{lid}: no surviving text, skipped')
            continue
        chosen.append(r)
    if a.limit:
        chosen = chosen[:a.limit]

    if a.dry_run:
        pages = sum(len(r['pages']) for r in chosen)
        words = sum(len((r.get('text') or '').split()) for r in chosen)
        print(f'{len(chosen)} letter(s), {pages} page(s), {words:,} German words')
        print(f'system prompt: {len(system):,} chars (cached after the first call)')
        if chosen:
            print('\n--- first user block ---')
            print(user_block(chosen[0], corr)[:1200])
        return

    client = make_client()
    print(f'{len(chosen)} letter(s) to translate, model {a.model or MODEL}'
          + (f', tag {a.tag}' if a.tag else ''))
    if a.batch:
        run_batch(chosen, client, system, corr, a.model, a.tag)
    else:
        run_live(chosen, client, system, corr, a.model, a.tag)


if __name__ == '__main__':
    main()
