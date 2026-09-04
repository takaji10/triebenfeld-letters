# -*- coding: utf-8 -*-
"""One-paragraph summary of each letter, written from the English translation.

    python summarise.py --dry-run        # what would be sent, spend nothing
    python summarise.py --limit 5        # a look first, live
    python summarise.py --batch          # everything outstanding, half price
    python summarise.py --collect
    python summarise.py --build          # assemble site/_data/summaries.yml

Written from the English rather than the German on purpose: the translation has
already resolved the line-wraps, the abbreviations and the obvious corruptions,
so summarising it is a far more reliable operation than summarising raw
transcription would be, and it costs a fraction as much.

Summaries are a finding aid, not part of the edition's text. They live in
site/_data/summaries.yml, which nothing else generates, and they never touch
the corpus, letters.json, or anything regenerate.py rebuilds.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, json, time, argparse

import yaml
import anthropic

_STDOUT = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdout = _STDOUT
_KEEP = []

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translate as T
import sys
_KEEP.append(sys.stdout)
sys.stdout = _STDOUT

RAW = os.path.join(ROOT, 'cache', 'translation-raw')
MAX_TOKENS = 600

# --lang de writes a parallel set. The German summary is written from the same
# English translation, not translated from the English summary: going through a
# summary twice compounds whatever the first pass got wrong, and the source is
# equally available either way.
LANGS = {
    'en': {'out': os.path.join('cache', 'summaries-raw'), 'dest': 'summaries.yml'},
    'de': {'out': os.path.join('cache', 'summaries-raw-de'), 'dest': 'summaries_de.yml'},
}
LANG = 'en'
OUT = os.path.join(ROOT, LANGS['en']['out'])
STATE = os.path.join(OUT, '_batches.json')
DEST = os.path.join(ROOT, 'site', '_data', LANGS['en']['dest'])


def set_lang(lang):
    global LANG, OUT, STATE, DEST
    LANG = lang
    OUT = os.path.join(ROOT, LANGS[lang]['out'])
    STATE = os.path.join(OUT, '_batches.json')
    DEST = os.path.join(ROOT, 'site', '_data', LANGS[lang]['dest'])

SYSTEM = """\
You are writing finding-aid summaries for a scholarly edition of letters written \
between 1798 and 1816, mostly by a Prussian estate agent, the Kriegs- und \
Forstrath von Triebenfeld, to his employer Friedrich Ludwig, Fürst zu \
Hohenlohe-Ingelfingen. They concern estates in South Prussia and the Duchy of \
Warsaw, debts, lawsuits, the Napoleonic wars and the Congress of Vienna.

You will be given the English translation of one letter. Write ONE paragraph \
summarising what it actually contains.

  * 40 to 80 words. One paragraph, no headings, no bullet points.
  * Lead with the substance, not with "This letter". Say what is reported, asked \
for, or complained of.
  * Name the people, places and sums that matter. These summaries are what a \
reader scans a list of 313 documents by, so concrete detail is the whole value: \
"presses for the sequestration of Zagorowo to be lifted" is useful, "discusses \
estate business" is not.
  * Use the names exactly as the translation spells them.
  * Where the letter is largely a financial schedule or a legal instrument, say \
so and give its subject and totals.
  * If the text is too damaged or fragmentary to summarise, say briefly what \
survives rather than inventing continuity.
  * Neutral register. Do not editorialise, and do not repeat the date or the \
place of writing - the page already displays those."""

SYSTEM_DE = """Sie schreiben Kurzregesten für eine wissenschaftliche Edition von Briefen aus den Jahren 1798 bis 1816, verfasst überwiegend von dem preußischen Guts- und Geschäftsträger, dem Kriegs- und Forstrath von Triebenfeld, an seinen Dienstherrn Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen. Es geht um Güter in Südpreußen und im Herzogtum Warschau, um Schulden, Prozesse, die napoleonischen Kriege und den Wiener Kongress.

Sie erhalten die englische Übersetzung eines Briefes. Schreiben Sie EINEN Absatz auf Deutsch, der wiedergibt, was der Brief tatsächlich enthält.

  * 40 bis 80 Wörter. Ein Absatz, keine Überschriften, keine Aufzählungen.
  * Beginnen Sie mit der Sache selbst, nicht mit "Dieser Brief". Sagen Sie, was berichtet, erbeten oder beklagt wird.
  * Nennen Sie die Personen, Orte und Summen, auf die es ankommt. Diese Regesten sind das, wonach ein Leser eine Liste von 313 Dokumenten überfliegt; das Konkrete ist ihr ganzer Wert.
  * Verwenden Sie die Namen genau in der Schreibweise der Edition, und die zeitgenössischen Formen: Rthl, Ducaten, Sequestration, Erbpacht, Vollmacht.
  * Handelt es sich im Wesentlichen um eine Rechnung oder eine Rechtsurkunde, so sagen Sie das und nennen Gegenstand und Summen.
  * Ist der Text zu beschädigt oder zu bruchstückhaft, sagen Sie knapp, was erhalten ist, statt Zusammenhang zu erfinden.
  * Sachlicher Ton. Nicht kommentieren, und Datum und Ausstellungsort nicht wiederholen - die Seite zeigt beides bereits an."""

TOOL = {
    'name': 'submit_summary',
    'description': 'Return the one-paragraph summary of this letter.',
    'input_schema': {
        'type': 'object',
        'properties': {'summary': {'type': 'string',
                                   'description': 'One paragraph, 40-80 words.'}},
        'required': ['summary'],
    },
}


def english_of(d):
    return '\n\n'.join((p.get('en') or '').strip() for p in d.get('pages', [])
                       if (p.get('en') or '').strip())


def load_done():
    if not os.path.isdir(OUT):
        return {}
    out = {}
    for fn in os.listdir(OUT):
        if fn.endswith('.json') and not fn.startswith('_'):
            d = json.load(open(os.path.join(OUT, fn), encoding='utf-8'))
            if d.get('summary'):
                out[str(d['letter'])] = d
    return out


def user_block(rec, en):
    meta = [f"Letter {rec['letter_id']}"]
    if rec.get('sender'):
        meta.append(f"From: {rec['sender']}")
    if rec.get('recipient'):
        meta.append(f"To: {rec['recipient']}")
    if rec.get('doc_type') == 'register':
        meta.append('This document is a register, not a letter.')
    return '\n'.join(meta) + '\n\nENGLISH TRANSLATION:\n' + en


def params(rec, en, model=None):
    return dict(model=model or T.MODEL, max_tokens=MAX_TOKENS,
                system=[{'type': 'text', 'text': (SYSTEM_DE if LANG == 'de' else SYSTEM),
                         'cache_control': {'type': 'ephemeral'}}],
                tools=[TOOL], tool_choice={'type': 'tool', 'name': 'submit_summary'},
                messages=[{'role': 'user', 'content': user_block(rec, en)}])


def save(lid, summary, usage, model):
    os.makedirs(OUT, exist_ok=True)
    json.dump({'letter': lid, 'pad': T.pad(lid), 'summary': summary,
               'model': model, 'usage': usage},
              open(os.path.join(OUT, T.pad(lid) + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


def build():
    """Assemble the per-letter files into the one data file the site reads."""
    done = load_done()
    if not done:
        sys.exit('nothing to build - run the summariser first')
    # Key by the unit's pad, recomputed from the letter id: the 'pad' stored
    # in an older cache file predates unit namespacing.
    out = {T.pad(d['letter']): d['summary'].strip() for d in done.values()}
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by summarise.py from the English translations.\n'
                '# A finding aid, not part of the edition text. Safe to regenerate.\n')
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=True, width=1000,
                       default_flow_style=False)
    print(f'wrote {DEST}  ({len(out)} summaries)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--batch', action='store_true')
    ap.add_argument('--collect', action='store_true')
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--model', default=None)
    ap.add_argument('--lang', default='en', choices=sorted(LANGS))
    a = ap.parse_args()
    set_lang(a.lang)

    if a.build:
        build()
        return

    recs = {str(r['letter_id']): r for r in T.load_letters()}

    if a.collect:
        client = T.make_client()
        st = json.load(open(STATE, encoding='utf-8'))
        pending, got, cin, cout = [], 0, 0, 0
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
                lid = res.custom_id[1:]
                payload = next((bl.input for bl in res.result.message.content
                                if bl.type == 'tool_use'), None)
                if not payload or not payload.get('summary'):
                    continue
                u = res.result.message.usage
                save(lid, payload['summary'],
                     {'input': u.input_tokens, 'output': u.output_tokens,
                      'cache_read': getattr(u, 'cache_read_input_tokens', 0) or 0},
                     st.get('model', T.MODEL))
                cin += u.input_tokens + (getattr(u, 'cache_read_input_tokens', 0) or 0)
                cout += u.output_tokens
                got += 1
            print(f'  {bid}: collected')
        T.report_cost(got, cin, cout, st.get('model'), 0.0, unit='summary')
        if pending:
            st['batches'] = pending
            json.dump(st, open(STATE, 'w', encoding='utf-8'), indent=1)
        elif os.path.isfile(STATE):
            os.remove(STATE)
        if got:
            build()
        return

    done = load_done()
    todo = []
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        d = json.load(open(os.path.join(RAW, fn), encoding='utf-8'))
        lid = str(d['letter'])
        if lid in done:
            continue
        en = english_of(d)
        rec = recs.get(lid)
        if not en or not rec:
            continue
        todo.append((lid, rec, en))
    if a.limit:
        todo = todo[:a.limit]

    print(f'{len(todo)} letter(s) to summarise')
    if a.dry_run:
        if todo:
            lid, rec, en = todo[0]
            print(f'system: {len(SYSTEM_DE if LANG == "de" else SYSTEM):,} chars (cached)')
            print('\n--- first request ---')
            print(user_block(rec, en)[:900])
        return
    if not todo:
        build()
        return

    client = T.make_client()
    if a.batch:
        reqs = [{'custom_id': f'L{lid}', 'params': params(rec, en, a.model)}
                for lid, rec, en in todo]
        batches = []
        for i in range(0, len(reqs), 100):
            b = client.messages.batches.create(requests=reqs[i:i + 100])
            batches.append(b.id)
            print(f'  batch {b.id}  ({len(reqs[i:i + 100])} letters)')
        os.makedirs(OUT, exist_ok=True)
        json.dump({'batches': batches, 'model': a.model or T.MODEL},
                  open(STATE, 'w', encoding='utf-8'), indent=1)
        print(f'\nwrote {STATE}\nrun  python summarise.py --collect  once they finish')
        return

    n = cin = cout = 0
    t0 = time.time()
    for i, (lid, rec, en) in enumerate(todo, 1):
        try:
            with client.messages.stream(**params(rec, en, a.model)) as s:
                msg = s.get_final_message()
        except anthropic.APIStatusError as e:
            print(f'  [{i}/{len(todo)}] L{lid} - API error {e.status_code}')
            continue
        payload = next((b.input for b in msg.content if b.type == 'tool_use'), None)
        if not payload or not payload.get('summary'):
            continue
        u = msg.usage
        save(lid, payload['summary'],
             {'input': u.input_tokens, 'output': u.output_tokens,
              'cache_read': getattr(u, 'cache_read_input_tokens', 0) or 0},
             a.model or T.MODEL)
        cin += u.input_tokens + (getattr(u, 'cache_read_input_tokens', 0) or 0)
        cout += u.output_tokens
        n += 1
        print(f'  [{i}/{len(todo)}] L{lid} - {len(payload["summary"].split())} words')
    T.report_cost(n, cin, cout, a.model, time.time() - t0, unit='summary')
    if n:
        build()


if __name__ == '__main__':
    main()
