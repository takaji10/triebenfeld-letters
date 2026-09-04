# -*- coding: utf-8 -*-
"""Apply the obvious corrections that the first pass deliberately withheld.

    python repair_translations.py --dry-run     # what would be sent, spend nothing
    python repair_translations.py --batch       # half price
    python repair_translations.py --collect
    python repair_translations.py --limit 5     # live, for a look first

The first pass was told never to fold an emendation into the English, so a
mangled token was carried through verbatim: "the Duchess of Sagen" for Sagan,
"comes ex nexa" for ex nexu, "der Fünſt" for der Fürst. That is right for a
diplomatic edition and wrong for this one, which is a reading copy - anybody
doing close textual work goes back to the manuscript regardless.

So this pass revisits only the pages where a corrupt token actually reached the
English (594 of 864), hands the model back its own translation and its own
recorded emendations, and asks it to apply the ones that are not in reasonable
doubt while keeping a visible mark on the ones that are. It rewrites nothing
else: the other pages, and all the flag metadata, are left exactly as they were.

The original English is preserved as `en_original` on every page it touches, so
the change is reversible and auditable rather than a silent overwrite.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, csv, json, time, argparse

import yaml
import anthropic

_STDOUT = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdout = _STDOUT
_KEEP = []

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translate as T                      # client, prices, pad, glossary loading
import sys
_KEEP.append(sys.stdout)
sys.stdout = _STDOUT

SHEET = os.path.join(ROOT, 'review', 'translation_review.csv')
RAW = os.path.join(ROOT, 'cache', 'translation-raw')
STATE = os.path.join(RAW, '_repair_batches.json')
MAX_TOKENS = 4000                          # one page of English, not a whole letter
ABBREV_RUN = [False]       # set by main() so apply_repair can record the reason


TOOL = {
    'name': 'submit_repair',
    'description': 'Return the corrected English for this one manuscript page.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'en': {'type': 'string',
                   'description': 'The corrected English for this page.'},
            'marker_count': {'type': 'integer',
                             'description': 'How many [illegible]/[uncertain: ]/'
                                            '[text lost] markers the English now carries.'},
            'applied': {
                'type': 'array',
                'description': 'Corrections you folded in silently.',
                'items': {'type': 'object', 'properties': {
                    'de': {'type': 'string'}, 'as': {'type': 'string'}},
                    'required': ['de', 'as']}},
            'still_uncertain': {
                'type': 'array',
                'description': 'Emendations you did NOT apply, left visibly marked '
                               'because the intended word is genuinely in doubt.',
                'items': {'type': 'object', 'properties': {
                    'de': {'type': 'string'}, 'why': {'type': 'string'}},
                    'required': ['de', 'why']}},
        },
        'required': ['en', 'marker_count'],
    },
}


def build_system(g):
    return f"""\
You are correcting one page of an English translation of an early-19th-century \
German letter, transcribed from Kurrent handwriting by machine.

EDITORIAL POLICY
{g['editorial_policy']}

HOUSE STYLE
{g['house_style']}

You will be given the German page, the English currently published for it, and \
the emendations the first translator recorded but deliberately did NOT apply.

Your job is to return the English with the obvious corrections folded in.

  * Apply an emendation when the intended word is not in reasonable doubt, and \
translate it properly into English - if the German should read `Rußland`, the \
English says "Russia", not "Rußland". Never leave a German word standing in the \
English because it was the emended form.
  * Do NOT apply one where you cannot tell what was meant, where two readings \
differ in meaning, or where it would change a figure or which person or place is \
referred to. Leave those visibly marked as `[uncertain: ...]`.
  * Keep every existing `[illegible]`, `[uncertain: ...]` and `[text lost]` mark \
that still applies. Do not smooth over a hole.
  * Change nothing else. This is a correction pass, not a retranslation: leave \
wording you are not fixing exactly as it stands.
  * Reproduce every numeral exactly as in the German, and never invent a name.

TERMBASE - unchanged, use these renderings:
{T.glossary_table(g)}"""


def abbrev_targets():
    """(letter, page) pairs whose English still carries a colon abbreviation.

    The first pass was told to reproduce proper nouns exactly as spelled, which
    fought against ordinary comprehension and left the model deciding case by
    case: "Min: v. Hard:" came out as "Minister Hardenberg" in one letter and as
    "the Prince Hard:" in the next. Expanding an abbreviation is not correcting
    a name, so the glossary now says so and these pages are brought into line.
    """
    g = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'translation_glossary.yml'),
                            encoding='utf-8'))
    table = {a['short']: a['expand'] for a in g.get('abbreviations', [])}
    rx = re.compile(r'(?<![A-Za-zÀ-ÿ])(' + '|'.join(
        re.escape(k) for k in sorted(table, key=len, reverse=True)) + ')')
    out = {}
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        d = json.load(open(os.path.join(RAW, fn), encoding='utf-8'))
        for pg in d.get('pages', []):
            hits = sorted(set(rx.findall(pg.get('en') or '')))
            if hits:
                out[(str(d['letter']), pg['page'])] = [
                    {'de': h, 'proposed': table[h],
                     'why': 'colon abbreviation; expand it in the English'}
                    for h in hits]
    return out


def targets():
    """(letter, page) pairs where a corrupt token reached the English."""
    out = {}
    with open(SHEET, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            if r['kind'] != 'emendation-degrades':
                continue
            if (r.get('ruling') or '').strip().upper() == 'OK':
                continue          # you have already said this one is fine as-is
            out.setdefault((r['letter'], int(r['page'])), []).append(
                {'de': r['german'], 'proposed': r['english'], 'why': r['note']})
    return out


def user_block(rec, page_no, en, emends):
    de = ''
    for p in rec['pages']:
        if p['page'] == page_no:
            de = p.get('reading') or p.get('diplomatic') or ''
    lines = [f"Letter {rec['letter_id']}, manuscript page {page_no}.", '',
             'GERMAN AS TRANSCRIBED:', de, '', 'ENGLISH AS PUBLISHED:', en, '',
             'EMENDATIONS RECORDED BUT NOT APPLIED:']
    for e in emends:
        lines.append(f"  - {e['de']!r} probably reads {e['proposed']!r}"
                     + (f"   ({e['why']})" if e.get('why') else ''))
    lines += ['', 'Return the corrected English for this page via submit_repair.']
    return '\n'.join(lines)


def params(rec, page_no, en, emends, system, model=None):
    return dict(model=model or T.MODEL, max_tokens=MAX_TOKENS,
                system=[{'type': 'text', 'text': system,
                         'cache_control': {'type': 'ephemeral'}}],
                tools=[TOOL], tool_choice={'type': 'tool', 'name': 'submit_repair'},
                messages=[{'role': 'user',
                           'content': user_block(rec, page_no, en, emends)}])


def apply_repair(lid, page_no, payload):
    """Write the corrected English back, keeping the original alongside it."""
    path = os.path.join(RAW, T.pad(lid) + '.json')
    d = json.load(open(path, encoding='utf-8'))
    for p in d['pages']:
        if p.get('page') != page_no:
            continue
        if 'en_original' not in p:
            p['en_original'] = p.get('en', '')
        p['en'] = payload.get('en', p.get('en', ''))
        if payload.get('marker_count') is not None:
            p['marker_count'] = payload['marker_count']
        prev = p.get('repair') or {}
        p['repair'] = {'applied': (prev.get('applied') or [])
                                  + (payload.get('applied') or []),
                       'still_uncertain': payload.get('still_uncertain') or [],
                       'abbrev': prev.get('abbrev') or ABBREV_RUN[0]}
        json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', action='store_true')
    ap.add_argument('--collect', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--model', default=None)
    ap.add_argument('--abbrev', action='store_true',
                    help='target pages whose English still has a colon abbreviation')
    a = ap.parse_args()

    ABBREV_RUN[0] = a.abbrev
    recs = {str(r['letter_id']): r for r in T.load_letters()}
    g = T.load_glossary()
    system = build_system(g)

    if a.collect:
        client = T.make_client()
        st = json.load(open(STATE, encoding='utf-8'))
        pending, got = [], 0
        cin = cout = 0
        for bid in st['batches']:
            b = client.messages.batches.retrieve(bid)
            if b.processing_status != 'ended':
                print(f'  {bid}: {b.processing_status} - not ready')
                pending.append(bid)
                continue
            for res in client.messages.batches.results(bid):
                if res.result.type != 'succeeded':
                    print(f'  {res.custom_id}: {res.result.type}')
                    continue
                lid, pg = res.custom_id[1:].split('_p')
                payload = None
                for blk in res.result.message.content:
                    if blk.type == 'tool_use':
                        payload = blk.input
                if payload and apply_repair(lid, int(pg), payload):
                    got += 1
                u = res.result.message.usage
                cin += u.input_tokens + (getattr(u, 'cache_read_input_tokens', 0) or 0)
                cout += u.output_tokens
            print(f'  {bid}: collected')
        T.report_cost(got, cin, cout, st.get('model'), 0.0, unit='page')
        if pending:
            st['batches'] = pending
            json.dump(st, open(STATE, 'w', encoding='utf-8'), indent=1)
        elif os.path.isfile(STATE):
            os.remove(STATE)
        print(f'\nrepaired {got} page(s)')
        return

    todo = []
    chosen = abbrev_targets() if a.abbrev else targets()
    for (lid, pg), emends in sorted(chosen.items()):
        rec = recs.get(lid)
        if not rec:
            continue
        d = json.load(open(os.path.join(RAW, T.pad(lid) + '.json'), encoding='utf-8'))
        page = next((p for p in d['pages'] if p.get('page') == pg), None)
        if not page or not page.get('en'):
            continue
        if page.get('repair') and not a.abbrev:
            continue          # already repaired; re-sending would only re-bill it
        if a.abbrev and (page.get('repair') or {}).get('abbrev'):
            continue
        en = page['en']
        todo.append((lid, pg, en, emends, rec))
    if a.limit:
        todo = todo[:a.limit]

    print(f'{len(todo)} page(s) to repair, '
          f'{len({t[0] for t in todo})} letter(s) affected')
    if a.dry_run:
        print(f'system prompt: {len(system):,} chars (cached after the first call)')
        if todo:
            lid, pg, en, em, rec = todo[0]
            print('\n--- first request ---')
            print(user_block(rec, pg, en, em)[:1400])
        return

    client = T.make_client()
    if a.batch:
        reqs = [{'custom_id': f'L{lid}_p{pg}',
                 'params': params(rec, pg, en, em, system, a.model)}
                for lid, pg, en, em, rec in todo]
        batches = []
        for i in range(0, len(reqs), 100):
            b = client.messages.batches.create(requests=reqs[i:i + 100])
            batches.append(b.id)
            print(f'  batch {b.id}  ({len(reqs[i:i + 100])} pages)')
        json.dump({'batches': batches, 'model': a.model or T.MODEL},
                  open(STATE, 'w', encoding='utf-8'), indent=1)
        print(f'\nwrote {STATE}\nrun  python repair_translations.py --collect')
        return

    done = cin = cout = 0
    t0 = time.time()
    for i, (lid, pg, en, em, rec) in enumerate(todo, 1):
        try:
            with client.messages.stream(**params(rec, pg, en, em, system, a.model)) as s:
                msg = s.get_final_message()
        except anthropic.APIStatusError as e:
            print(f'  [{i}/{len(todo)}] L{lid} p{pg} - API error {e.status_code}')
            continue
        payload = next((b.input for b in msg.content if b.type == 'tool_use'), None)
        if not payload:
            continue
        apply_repair(lid, pg, payload)
        u = msg.usage
        cin += u.input_tokens + (getattr(u, 'cache_read_input_tokens', 0) or 0)
        cout += u.output_tokens
        done += 1
        n_app = len(payload.get('applied') or [])
        print(f'  [{i}/{len(todo)}] L{lid} p{pg} - {n_app} correction(s) applied')
    T.report_cost(done, cin, cout, a.model, time.time() - t0, unit='page')


if __name__ == '__main__':
    main()
