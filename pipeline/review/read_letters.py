# -*- coding: utf-8 -*-
"""Read each letter of a holding whole: propose witnessed corrections and write
a German summary (Kurzregest) of what the letter is for.

    python read_letters.py --unit oe1bu9454 --dry-run            # prompt + token count, free
    python read_letters.py --unit oe1bu9454 --letters 136,215    # live, a pilot
    python read_letters.py --unit oe1bu9454 --batch              # the rest, half price
    python read_letters.py --unit oe1bu9454 --collect
    python read_letters.py --unit oe1bu9454 --check              # local checks, free

The model reads and proposes; nothing it returns reaches the corpus or the site
directly. --check runs the free mechanical filters (a fix needs a witness the
machine can verify; a summary may not contain a figure or a name the letter does
not) and writes review/<slug>/reading_check.md for a human read. Kept fixes go
through apply_transcription_fixes.py like any other; kept summaries go into
units/<slug>/summaries_de.yml.

Written from the GERMAN, because this holding has no translation yet. The
summary rules follow summarise.py's SYSTEM_DE, with the edition's relevance rule
(Trąbczyn and its settlers never left out) and a hard ban on anything not in the
letter itself.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, json, time, argparse, hashlib, collections
import yaml
import anthropic
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL = 'claude-opus-5-5'
PRICES = {'claude-opus-5-5': (5, 25), 'claude-opus-5': (5, 25)}
MAX_TOKENS = 16000
NEIGHBOUR_LINES = 80        # context letters are cut to this many lines each

# Approved recurring patterns and settled title spellings (memory / notes.md).
APPROVED = """\
  Ewr (never Eine/Ein before Durchlaucht), Jezt (not Jagt), Schicken Sie (not
  Schaden Sie), Indes (conjunction; not Jedes), schicken (send; not schulen),
  Summa (not Suma), Königl. Majestät, closing formula "In tiefster Ehrfurcht
  ersterbe", titles: Hoffrath, Krieges Rath, Staats Kanzler, Bürgermeister,
  Prefect, Cabinets Rath. Hawich (the Justiz Bürgermeister of Zagorowo) is often
  misread as Habisch/Habich/Habik/Hawick. Brzechffa, Niedźwiecki, Prusimski/
  Prusimska, Bertrand, Götzen, Bornstädt, Glenck, Schenck, Beguelin."""


def unit_preamble(unit):
    ref = unit.get('ref') or unit.slug
    span = unit.get('date_span') or ''
    title = ' '.join((unit.get('title') or '').split())
    desc = ' '.join((unit.get('description') or '').split())
    return (f'The holding is {ref}' + (f', {span}' if span else '') + '. '
            + (title + '. ' if title else '') + desc)


def authorities():
    ppl = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'people.yml'),
                              encoding='utf-8'))['people']
    pl = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'places.yml'),
                             encoding='utf-8'))['places']
    people = sorted({(e.get('display') or '').strip() for e in ppl.values()} - {''})
    places = sorted({unitlib.place_label(e) for e in pl.values()} - {''})
    return people, places


def build_system(unit):
    people, places = authorities()
    return f"""\
You are reading one document of a scholarly edition of archival letters, so that \
two things can be done with it: a German summary for the edition's letter list, \
and the correction of a few transcription errors that can be PROVEN.

{unit_preamble(unit)}

The edition's focus: the Trąbczyn estate and its settlers (Olęder, called \
Hauländer or Colonisten in these letters), within the business of Prince \
Friedrich Ludwig zu Hohenlohe-Ingelfingen and his agent, the Krieges Rath \
Peter Friedrich August von Triebenfeld.

THE TEXT. The German was read from Kurrent handwriting by machine and then \
corrected by hand for names and layout. It is mostly sound, but garbled words \
remain. [?] marks a doubtful reading, [xyz] letters supplied by the editor, \
[...] a gap, ¬ a word broken at the line end. Spelling is period spelling and \
the writer's own: it is NOT an error (ſ, ß/ss, zz, th, Güther, gerne, seyn, \
Pohlen, Hube, doubled letters). Lines are numbered as the edition shows them.

=== TASK 1: SUMMARY (German, the field summary_de) ===
One paragraph. HARD LIMIT 80 words, aim for 50 to 70; a short letter gets fewer words, never padded. Count them. If you are over, cut the least important point rather than compressing everything.
  * Say what the letter is FOR: what is reported, asked, agreed, conveyed or \
complained of. Do not walk through it in order. Lead with the substance, not \
with "Dieser Brief" or "In diesem Schreiben".
  * Name the people, places and sums that matter. Concrete detail is the whole \
value: "drängt auf Aufhebung der Sequestration von Zagórów" is useful, \
"bespricht Gutsangelegenheiten" is not.
  * RELEVANCE: anything about Trąbczyn, its villages (Szetlewek, Łaziny/Laske, \
Osiny, Nowa Wieś), its settlers, or the Prusimska claim is ALWAYS included, \
even if it is one sentence of a long letter. A letter that has nothing to do \
with Trąbczyn is summarised on its own terms (politics in Vienna, a debt, iron \
from Koszęcin); never stretch it towards Trąbczyn.
  * Leave out: courtesies, closing formulas, fees and stamp duty, witnesses, \
the copying clerk, whether a signature is legible.
  * NOTHING FROM OUTSIDE THE LETTER. No background history, no motives, no \
judgement of the writer, no identification of a person the letter does not \
name (an unnamed "Freund" stays "ein Freund"), no date or sum that is not \
written in it. Sender and recipient are given to you below; use them, do not \
guess others. Do not repeat the date or the place of writing.
  * The writer and the addressee: if the sender or recipient is given below as "not identified", do NOT name one, even if you are fairly sure who it is; write "der Schreiber" or describe the document. Name people only as the letter names them.
  * Every figure must stay attached to exactly what the letter attaches it to on that line. Do not carry a sum from one item to a neighbouring one. If you are not certain what a figure belongs to, leave it out.
  * Keep the letter's own mood: a plan is a plan, a rumour a rumour, a request a request ("will", "soll", "hofft", "berichtet, dass"). Do not turn intentions or hearsay into facts.
  * Never build a statement on a garbled or doubtful word ([?], or a word that is not German), even when the intended word seems obvious. Leave that point out.
  * If the text is garbled, summarise only what can be read and say so \
("großenteils unleserlich; erkennbar ist ..."). Never fill a gap with what \
would make sense.
  * Forms: people as the edition names them (list below); places by their \
Polish name as the edition displays it, i.e. the part before the brackets in \
the list below (Zagórów, Kamionna, Trąbczyn, Wrocław); money as Rthl (also for \
rt, rthl, Rthlr); figures exactly as written. Plain modern German. No em \
dashes and no en dashes, except a dash between two figures for a range.

For every statement in the summary give the letter line number(s) it rests on \
(field claims). If you cannot point to a line, the statement does not belong in \
the summary.

=== TASK 2: CORRECTIONS (field fixes) ===
Propose a correction ONLY when it can be proven by one of these witnesses:
  same_letter    the correct form is written elsewhere in this same letter \
(give that line in witness)
  attested       the correct form is the usual form in this correspondence \
and the transcribed form is a misreading of it (e.g. a name or title spelled \
correctly many times elsewhere)
  standard_form  a name or title in the edition's settled form (lists below)
  formula        a fixed formula (forms of address, closing formulas) whose \
wording is certain
  grammar        the sentence admits exactly one reading and the transcribed \
word makes it ungrammatical; give the one reading in witness
NEVER propose: a change made because another word would make better sense \
(this is the error to avoid above all); a change to a figure, a date, or \
anything in square brackets; adding [?]; modernising or normalising spelling; \
anything in a passage too garbled to read with confidence. When in doubt, do \
not propose it: put it in suspicions instead. Zero fixes is a normal result.
Each fix: line (letter line number), old (the exact transcribed token, which \
must occur once on that line), new, category, witness.

=== TASK 3: SUSPICIONS ===
Words you believe are misread but cannot prove. They are logged, not applied.

=== EDITION FORMS ===
Approved patterns and settled spellings:
{APPROVED}

People (edition display names):
{', '.join(people)}

Places (Polish name (German name as the letters write it)):
{', '.join(places)}

Use the tool submit_reading. Fill reading_notes first (at most 120 words, for \
your own orientation: who writes to whom about what), then the rest."""


TOOL = {
    'name': 'submit_reading',
    'description': 'Return the reading of this letter.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'reading_notes': {'type': 'string'},
            'legibility': {'type': 'string',
                           'enum': ['sound', 'partly garbled', 'largely garbled']},
            'summary_de': {'type': 'string'},
            'claims': {'type': 'array', 'items': {
                'type': 'object',
                'properties': {'statement': {'type': 'string'},
                               'lines': {'type': 'array', 'items': {'type': 'integer'}}},
                'required': ['statement', 'lines']}},
            'fixes': {'type': 'array', 'items': {
                'type': 'object',
                'properties': {'line': {'type': 'integer'}, 'old': {'type': 'string'},
                               'new': {'type': 'string'},
                               'category': {'type': 'string', 'enum': [
                                   'same_letter', 'attested', 'standard_form',
                                   'formula', 'grammar']},
                               'witness': {'type': 'string'}},
                'required': ['line', 'old', 'new', 'category', 'witness']}},
            'suspicions': {'type': 'array', 'items': {
                'type': 'object',
                'properties': {'line': {'type': 'integer'}, 'word': {'type': 'string'},
                               'note': {'type': 'string'}},
                'required': ['line', 'word', 'note']}},
        },
        'required': ['reading_notes', 'legibility', 'summary_de', 'claims',
                     'fixes', 'suspicions'],
    },
}


# ------------------------------------------------------------------ data --

class Corpus:
    def __init__(self, unit):
        self.unit = unit
        self.path = os.path.join(unit.dir, 'corpus.txt')
        self.lines = open(self.path, encoding='utf-8').read().split('\n')
        # letter id -> [(corpus_line, letter_line or None, text)]
        self.docs = collections.OrderedDict()
        cur = None; n = 0
        for i, l in enumerate(self.lines, 1):
            m = re.match(r'\[DOC (\S+)\]', l)
            if m:
                cur = m.group(1); n = 0; self.docs[cur] = []
                continue
            if cur is None:
                continue
            s = l.strip()
            if s and not s.startswith('[PAGE '):
                n += 1; self.docs[cur].append((i, n, l))
            else:
                self.docs[cur].append((i, None, l))

    def numbered(self, lid, limit=None):
        out = []
        for _ci, ln, t in self.docs.get(lid, []):
            if ln is None:
                if t.strip():
                    out.append(f'     {t}')
                continue
            if limit and ln > limit:
                out.append('     [... context cut ...]'); break
            out.append(f'{ln:>4} {t}')
        return '\n'.join(out)

    def letter_lines(self, lid):
        return {ln: t for _ci, ln, t in self.docs.get(lid, []) if ln}

    def corpus_line(self, lid, ln):
        for ci, n, _t in self.docs.get(lid, []):
            if n == ln:
                return ci
        return None


def load_meta(unit):
    rows = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8'))
    # pipeline-check: scoped to one unit; the corpus.txt [DOC n] number is the key
    return {str(r['letter_id']): r for r in rows if r.get('unit') == unit.slug}


def reading_order(meta):
    live = [r for r in meta.values() if not r.get('is_missing')]
    live.sort(key=lambda r: (r.get('date_iso') or '9999', r.get('seq_archival') or 0))
    return [str(r['letter_id']) for r in live]


def user_block(lid, corpus, meta, order, rulings):
    r = meta[lid]
    i = order.index(lid)
    head = [f"DOCUMENT {lid}",
            f"Date: {r.get('date_display') or r.get('date_iso') or 'undated'}"
            + (f" ({r.get('date_iso')})" if r.get('date_iso') else ''),
            f"Sender: {r.get('sender') or 'not identified'}",
            f"Recipient: {r.get('recipient') or 'not identified'}",
            f"Place of writing: {r.get('place') or 'not stated'}",
            f"Language: {r.get('language') or 'de'}"]
    if r.get('rough_transcription'):
        head.append('This letter is marked ROUGH TRANSCRIPTION: much of it is '
                    'garbled. Only same_letter and standard_form fixes.')
    parts = ['\n'.join(head), '=== THE LETTER ===\n' + corpus.numbered(lid)]
    twin = rulings['DUP_OF'].get(lid) or next(
        (k for k, v in rulings['DUP_OF'].items() if v == lid), None)
    if twin and twin in corpus.docs:
        parts.append(f'=== ANOTHER COPY OF THE SAME TEXT (document {twin}); a '
                     f'witness for corrections, not to be summarised ===\n'
                     + corpus.numbered(twin))
    for tag, j in (('PREVIOUS', i - 1), ('NEXT', i + 1)):
        if 0 <= j < len(order):
            o = order[j]; m = meta[o]
            parts.append(f'=== CONTEXT ONLY: the {tag} letter in date order '
                         f'(document {o}, {m.get("date_iso") or "undated"}, '
                         f'{m.get("sender") or "?"} to {m.get("recipient") or "?"}). '
                         f'Do not summarise it or correct it. ===\n'
                         + corpus.numbered(o, NEIGHBOUR_LINES))
    parts.append(f'Now read DOCUMENT {lid} and submit the reading.')
    return '\n\n'.join(parts)


def source_hash(corpus, lid):
    return hashlib.sha256(corpus.numbered(lid).encode('utf-8')).hexdigest()[:16]


# ------------------------------------------------------------------ runs --

def out_dir(unit):
    return os.path.join(ROOT, 'cache', f'reading-{unit.slug}')


def out_path(unit, lid):
    return os.path.join(out_dir(unit), f'{unit.pad(lid)}.json')


def done(unit, lid):
    p = out_path(unit, lid)
    return os.path.isfile(p) and bool(json.load(open(p, encoding='utf-8')).get('reading'))


def params(system, user):
    return dict(model=MODEL, max_tokens=MAX_TOKENS,
                system=[{'type': 'text', 'text': system,
                         'cache_control': {'type': 'ephemeral'}}],
                tools=[TOOL], tool_choice={'type': 'auto'},
                messages=[{'role': 'user', 'content': user}])


def extract(msg):
    for b in msg.content:
        if b.type == 'tool_use' and b.name == 'submit_reading':
            p = b.input
            for k in ('claims', 'fixes', 'suspicions'):
                if isinstance(p.get(k), str):
                    try:
                        p[k] = json.loads(p[k])
                    except Exception:
                        pass
            return p
    return None


def usage_of(msg):
    u = msg.usage
    return {'input': u.input_tokens, 'output': u.output_tokens,
            'cache_read': getattr(u, 'cache_read_input_tokens', 0) or 0,
            'cache_write': getattr(u, 'cache_creation_input_tokens', 0) or 0}


def cost(usages, batch=False):
    pi, po = PRICES[MODEL]
    c = sum(u['input'] * pi + u['cache_write'] * pi * 1.25 + u['cache_read'] * pi * 0.1
            + u['output'] * po for u in usages) / 1e6
    return c / 2 if batch else c


def save(unit, corpus, lid, reading, usage, extra=None):
    os.makedirs(out_dir(unit), exist_ok=True)
    out = {'letter': lid, 'pad': unit.pad(lid), 'model': MODEL,
           'source_hash': source_hash(corpus, lid), 'reading': reading, 'usage': usage}
    out.update(extra or {})
    json.dump(out, open(out_path(unit, lid), 'w', encoding='utf-8', newline='\n'),
              ensure_ascii=False, indent=1)


def make_client():
    keyfile = os.path.join(ROOT, '.anthropic_key')
    if os.path.isfile(keyfile):
        key = open(keyfile, encoding='utf-8').read().strip()
        if key:
            return anthropic.Anthropic(api_key=key)
    if not os.environ.get('ANTHROPIC_API_KEY'):
        sys.exit('No API key. Put one in .anthropic_key (gitignored) or export ANTHROPIC_API_KEY.')
    return anthropic.Anthropic()


def run_live(unit, corpus, meta, order, rulings, lids):
    client = make_client(); system = build_system(unit); usages = []
    for k, lid in enumerate(lids, 1):
        if done(unit, lid):
            print(f'  [{k}/{len(lids)}] L{lid} already read'); continue
        for attempt in range(3):
            with client.messages.stream(**params(system, user_block(
                    lid, corpus, meta, order, rulings))) as s:
                msg = s.get_final_message()
            u = usage_of(msg); usages.append(u)
            rd = extract(msg)
            if rd and rd.get('summary_de') and msg.stop_reason != 'max_tokens':
                save(unit, corpus, lid, rd, u)
                print(f"  [{k}/{len(lids)}] L{lid} {rd.get('legibility')}, "
                      f"{len(rd.get('fixes') or [])} fix(es), {u['output']} out tok")
                break
            print(f'  [{k}/{len(lids)}] L{lid} unusable result, retrying')
    print(f'{len(usages)} call(s), ${cost(usages):.2f} at live rates')


def run_batch(unit, corpus, meta, order, rulings, lids):
    client = make_client(); system = build_system(unit)
    todo = [l for l in lids if not done(unit, l)]
    reqs = [{'custom_id': 'L' + re.sub(r'[^A-Za-z0-9_-]', '_', l),
             'params': params(system, user_block(l, corpus, meta, order, rulings))}
            for l in todo]
    ids = {r['custom_id']: l for r, l in zip(reqs, todo)}
    os.makedirs(out_dir(unit), exist_ok=True)
    state = os.path.join(out_dir(unit), '_batches.json')
    st = json.load(open(state, encoding='utf-8')) if os.path.isfile(state) else {'batches': [], 'ids': {}}
    for i in range(0, len(reqs), 100):
        b = client.messages.batches.create(requests=reqs[i:i + 100])
        st['batches'].append(b.id); print(f'  batch {b.id} ({len(reqs[i:i+100])} letters)')
    st['ids'].update(ids)
    json.dump(st, open(state, 'w', encoding='utf-8'), indent=1)
    print(f'{len(todo)} letter(s) submitted; run --collect when they end')


def run_collect(unit, corpus):
    client = make_client()
    state = os.path.join(out_dir(unit), '_batches.json')
    if not os.path.isfile(state):
        return print('no batches in flight')
    st = json.load(open(state, encoding='utf-8')); pending = []; usages = []; bad = []
    for bid in st['batches']:
        b = client.messages.batches.retrieve(bid)
        if b.processing_status != 'ended':
            print(f'  {bid}: {b.processing_status}'); pending.append(bid); continue
        for res in client.messages.batches.results(bid):
            lid = st['ids'].get(res.custom_id)
            if lid is None or res.result.type != 'succeeded':
                bad.append(res.custom_id); continue
            msg = res.result.message
            if res.custom_id.startswith('V'):
                v = vextract(msg)
                if not v or not v.get('summary_checked'):
                    bad.append(res.custom_id); continue
                u = usage_of(msg); usages.append(u)
                attach_verify(unit, lid, v, u, {'verify_batch_id': bid}); continue
            rd = extract(msg)
            if not rd or not rd.get('summary_de') or msg.stop_reason == 'max_tokens':
                bad.append(res.custom_id); continue
            u = usage_of(msg); usages.append(u)
            save(unit, corpus, lid, rd, u, {'batch_id': bid})
        print(f'  {bid}: collected')
    st['batches'] = pending
    json.dump(st, open(state, 'w', encoding='utf-8'), indent=1)
    print(f'{len(usages)} collected, ${cost(usages, batch=True):.2f} at batch rates'
          + (f'; not usable, re-run: {", ".join(bad)}' if bad else ''))


def run_dry(unit, corpus, meta, order, rulings, lids):
    system = build_system(unit)
    lid = lids[0]
    user = user_block(lid, corpus, meta, order, rulings)
    print(system[:3000], '\n...\n'); print(user[:4000], '\n...')
    try:
        client = make_client()
        ns = client.messages.count_tokens(model=MODEL, system=system, tools=[TOOL],
                                          messages=[{'role': 'user', 'content': 'x'}]).input_tokens
        tot = 0
        for l in lids:
            tot += client.messages.count_tokens(model=MODEL, messages=[{'role': 'user', 'content':
                    user_block(l, corpus, meta, order, rulings)}]).input_tokens
        print(f'\nsystem+tool: {ns:,} tokens (cached after the first call)')
        print(f'letters: {len(lids)}, user blocks {tot:,} tokens, avg {tot // max(1, len(lids)):,}')
        est_out = 1500 * len(lids)
        pi, po = PRICES[MODEL]
        c = (tot * pi + ns * pi * 0.1 * len(lids) + est_out * po) / 1e6
        print(f'estimate: ~${c:.2f} live, ~${c / 2:.2f} batch (output assumed 1,500 tok/letter)')
    except Exception as e:
        print('token count unavailable:', e)


# ---------------------------------------------------------------- verify --

VERIFY_SYSTEM = """\
You check a German summary of an archival letter against the letter itself. You \
are the safeguard against invention: a summary may only say what the letter \
says. The letter is a machine transcription of Kurrent handwriting and has \
garbled words; period spelling is normal.

For each claim of the summary, decide:
  supported    the cited lines (or other lines of the letter) say this
  overstated   the letter says something weaker or different: a plan stated as \
a fact, hearsay as fact, a figure attached to the wrong item, a person named \
whom the letter does not name, a garbled word interpreted
  unsupported  the letter does not say this

Then give summary_checked: the summary with every overstated claim weakened to \
what the letter says and every unsupported claim removed. You may ONLY delete \
or weaken. Never add information, never add a name, a figure or a place, never \
rephrase what is supported. If everything is supported, return the summary \
unchanged. Keep it German, no em dashes.

The edition names places by their Polish name even where the letter writes the German one (Kaemen = Kamionna, Zagorowo = Zagórów, Breslau = Wrocław, Brieg = Brzeg, Schlawenschitz = Sławięcice); money is given as Rthl for rt. That is correct and supported, not an interpretation. Places, as Polish (German):
{places}"""

VERIFY_TOOL = {
    'name': 'submit_check',
    'description': 'Return the verdict on each claim and the checked summary.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'claims': {'type': 'array', 'items': {
                'type': 'object',
                'properties': {'statement': {'type': 'string'},
                               'verdict': {'type': 'string', 'enum': [
                                   'supported', 'overstated', 'unsupported']},
                               'reason': {'type': 'string'}},
                'required': ['statement', 'verdict', 'reason']}},
            'summary_checked': {'type': 'string'},
        },
        'required': ['claims', 'summary_checked'],
    },
}


def verify_user(lid, corpus, meta, rd):
    m = meta[lid]
    claims = '\n'.join(f'- {c.get("statement")} (lines {c.get("lines")})'
                       for c in rd.get('claims') or [])
    return (f"DOCUMENT {lid}. Sender: {m.get('sender') or 'not identified'}. "
            f"Recipient: {m.get('recipient') or 'not identified'}.\n\n"
            f"=== THE LETTER ===\n{corpus.numbered(lid)}\n\n"
            f"=== THE SUMMARY ===\n{rd.get('summary_de')}\n\n"
            f"=== ITS CLAIMS ===\n{claims}\n\nCheck it and use the tool submit_check.")


def vparams(user):
    return dict(model=MODEL, max_tokens=4000,
                system=[{'type': 'text', 'text': VERIFY_SYSTEM.format(places=', '.join(authorities()[1])),
                         'cache_control': {'type': 'ephemeral'}}],
                tools=[VERIFY_TOOL], tool_choice={'type': 'auto'},
                messages=[{'role': 'user', 'content': user}])


def vextract(msg):
    for b in msg.content:
        if b.type == 'tool_use' and b.name == 'submit_check':
            p = b.input
            if isinstance(p.get('claims'), str):
                try:
                    p['claims'] = json.loads(p['claims'])
                except Exception:
                    pass
            return p
    return None


def verified(unit, lid):
    p = out_path(unit, lid)
    return os.path.isfile(p) and bool(json.load(open(p, encoding='utf-8')).get('verify'))


def attach_verify(unit, lid, v, u, extra=None):
    p = out_path(unit, lid)
    rec = json.load(open(p, encoding='utf-8'))
    rec['verify'] = v
    rec['verify_usage'] = u
    rec.update(extra or {})
    json.dump(rec, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)


def run_verify(unit, corpus, meta, lids, batch=False):
    client = make_client()
    todo = [l for l in lids if done(unit, l) and not verified(unit, l)]
    reads = {l: json.load(open(out_path(unit, l), encoding='utf-8'))['reading'] for l in todo}
    if batch:
        reqs = [{'custom_id': 'V' + re.sub(r'[^A-Za-z0-9_-]', '_', l),
                 'params': vparams(verify_user(l, corpus, meta, reads[l]))} for l in todo]
        state = os.path.join(out_dir(unit), '_batches.json')
        st = json.load(open(state, encoding='utf-8')) if os.path.isfile(state) else {'batches': [], 'ids': {}}
        for i in range(0, len(reqs), 100):
            b = client.messages.batches.create(requests=reqs[i:i + 100])
            st['batches'].append(b.id)
            print(f'  batch {b.id} ({len(reqs[i:i + 100])} checks)')
        st['ids'].update({r['custom_id']: l for r, l in zip(reqs, todo)})
        json.dump(st, open(state, 'w', encoding='utf-8'), indent=1)
        return print(f'{len(todo)} check(s) submitted; run --collect when they end')
    usages = []
    for k, l in enumerate(todo, 1):
        with client.messages.stream(**vparams(verify_user(l, corpus, meta, reads[l]))) as s:
            msg = s.get_final_message()
        u = usage_of(msg)
        usages.append(u)
        v = vextract(msg)
        if v and v.get('summary_checked'):
            attach_verify(unit, l, v, u)
            bad = [c for c in v.get('claims') or [] if c.get('verdict') != 'supported']
            print(f'  [{k}/{len(todo)}] L{l}: {len(bad)} claim(s) not supported')
        else:
            print(f'  [{k}/{len(todo)}] L{l}: no usable check')
    print(f'{len(usages)} check(s), ${cost(usages):.2f} at live rates')

# ---------------------------------------------------------------- checks --

WORD = r"[A-Za-zÄÖÜäöüßſąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+"


def vocabulary():
    c = collections.Counter()
    for d in os.listdir(os.path.join(ROOT, 'units')):
        p = os.path.join(ROOT, 'units', d, 'corpus.txt')
        if os.path.isfile(p):
            c.update(re.findall(WORD, open(p, encoding='utf-8').read()))
    return c


def authority_forms():
    ppl = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'people.yml'), encoding='utf-8'))['people']
    pl = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'places.yml'), encoding='utf-8'))['places']
    forms = set()
    for e in list(ppl.values()) + list(pl.values()):
        for k in ('display', 'german'):
            forms.update(re.findall(WORD, e.get(k) or ''))
        for v in e.get('variants') or []:
            forms.update(re.findall(WORD, v if isinstance(v, str) else (v.get('form') or '')))
    forms.update(re.findall(WORD, APPROVED))
    return forms


def norm_num(s):
    return re.sub(r'[.,\s]', '', s)


def check_fix(f, lid, letter, vocab, forms, rough):
    """(keep, reason) for one proposed fix: the machine-verifiable bar only."""
    ln, old, new, cat = f.get('line'), f.get('old') or '', f.get('new') or '', f.get('category')
    line = letter.get(ln)
    if line is None:
        return False, 'line out of range'
    if old == new:
        return False, 'no change'
    if re.search(r'[\d\[\]]', old + new):
        return False, 'touches a figure or brackets'
    pat = r'(?<![^\W\d_])' + re.escape(old) + r'(?![^\W\d_])'
    if len(re.findall(pat, line)) != 1:
        return False, f'"{old}" not exactly once on the line'
    if rough and cat not in ('same_letter', 'standard_form'):
        return False, 'rough letter: only same_letter / standard_form'
    others = '\n'.join(t for n, t in letter.items() if n != ln)
    nw = re.findall(WORD, new)
    if cat == 'same_letter' and new[:1].isupper() and not all(w in forms for w in nw):
        # A name spelled two ways in one letter may be the writer's own
        # variation, not a misreading: the editor kept Kiełszewski in letter
        # 215 although line 176 has Kiełczewski (2026-09-29). Names change
        # only to a settled edition form.
        return None, 'capitalised: a name stays unless an edition form exists; a noun may be fixed'
    if cat == 'same_letter':
        ok = re.search(r'(?<![^\W\d_])' + re.escape(new) + r'(?![^\W\d_])', others)
        return (True, 'same letter') if ok else (False, 'new form not elsewhere in the letter')
    if cat == 'standard_form':
        return (True, 'standard form') if nw and all(w in forms for w in nw) else (False, 'not an edition form')
    if cat in ('attested', 'formula'):
        o = sum(vocab[w] for w in re.findall(WORD, old)) if re.findall(WORD, old) else 0
        n = min((vocab[w] for w in nw), default=0)
        if n >= 3 and o <= 2:
            return True, f'attested ({n}x; old {o}x)'
        return False, f'not attested enough (new {n}x, old {o}x)'
    return None, 'grammar: needs a human read'


def check_summary(rd, letter, text, known):
    flags = []
    s = rd.get('summary_de') or ''
    words = len(s.split())
    if words > 80:
        flags.append(f'{words} words')
    if '—' in s or re.search(r'(?<!\d)–|–(?!\d)', s):
        flags.append('dash')
    nums_letter = {norm_num(x) for x in re.findall(r'\d[\d.,/]*', text)}
    for x in re.findall(r'\d[\d.,/]*', s):
        if norm_num(x).rstrip('.') not in nums_letter and norm_num(x) not in nums_letter:
            flags.append(f'figure {x} not in letter')
    low = text.lower().replace('ſ', 's')
    for w in set(re.findall(r'(?<=\s)[A-ZÄÖÜŁŚŻ]' + WORD[1:], ' ' + s)):
        stem = w.lower()[:5]
        if stem not in low and w not in known:
            flags.append(f'name? {w}')
    for c in rd.get('claims') or []:
        for n in c.get('lines') or []:
            if n not in letter:
                flags.append(f'cited line {n} out of range')
    return words, flags


def run_check(unit, corpus, meta):
    vocab = vocabulary(); forms = authority_forms()
    rough = unitlib.load_rulings(unit)['ROUGH_LETTERS']
    docs = os.path.join(ROOT, 'corpus', 'documents')
    rep = ['# Reading check', '']
    kept, dropped, manual = [], [], []
    summaries = {}
    for lid in reading_order(meta):
        if not done(unit, lid):
            continue
        rec = json.load(open(out_path(unit, lid), encoding='utf-8'))
        rd = rec['reading']
        stale = rec.get('source_hash') != source_hash(corpus, lid)
        letter = corpus.letter_lines(lid)
        text = '\n'.join(letter.values())
        known = set()
        dp = os.path.join(docs, f'{meta[lid]["uid"]}.json')
        if os.path.isfile(dp):
            d = json.load(open(dp, encoding='utf-8'))
            for m in (d.get('mentions') or []) + (d.get('place_mentions') or []):
                known.update(re.findall(WORD, m.get('display') or ''))
            known.update(re.findall(WORD, d.get('sender') or ''))
            known.update(re.findall(WORD, d.get('recipient') or ''))
        v = rec.get('verify') or {}
        final = (v.get('summary_checked') or rd.get('summary_de') or '').strip()
        words, flags = check_summary(dict(rd, summary_de=final), letter, text, known)
        m = meta[lid]
        changed = bool(v) and final != (rd.get('summary_de') or '').strip()
        rep += [f'## {lid}  ({m.get("date_iso") or "undated"}; {m.get("sender") or "?"} → '
                f'{m.get("recipient") or "?"}; {rd.get("legibility")})' + ('  **STALE**' if stale else '')
                + ('' if v else '  (not verified)'), '', final, '',
                f'{words} words' + ('; FLAGS: ' + '; '.join(flags) if flags else '')]
        if changed:
            rep += ['', '*Before the check:* ' + (rd.get('summary_de') or '')]
        for c in rd.get('claims') or []:
            rep.append(f'- claim {c.get("lines")}: {c.get("statement")}')
        for c in v.get('claims') or []:
            if c.get('verdict') != 'supported':
                rep.append(f'- CHECK {c.get("verdict").upper()}: {c.get("statement")} — {c.get("reason")}')
        summaries[lid] = dict(summary=final, words=words, flags=flags, verified=bool(v),
                              changed=changed, stale=stale)
        for f in rd.get('fixes') or []:
            ok, why = check_fix(f, lid, letter, vocab, forms, lid in rough)
            row = dict(f, letter=lid, verdict=why,
                       corpus_line=corpus.corpus_line(lid, f.get('line')))
            (kept if ok else manual if ok is None else dropped).append(row)
            rep.append(f'- FIX {"KEEP" if ok else "READ" if ok is None else "drop"} '
                       f'l.{f.get("line")} {f.get("old")} → {f.get("new")} '
                       f'[{f.get("category")}: {f.get("witness")}] — {why}')
        for sp in rd.get('suspicions') or []:
            rep.append(f'- suspicion l.{sp.get("line")} {sp.get("word")}: {sp.get("note")}')
        rep.append('')
    out = os.path.join(ROOT, 'review', unit.slug)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'reading_check.md'), 'w', encoding='utf-8').write('\n'.join(rep))
    json.dump(summaries, open(os.path.join(out, 'reading_summaries.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    json.dump({'kept': kept, 'manual': manual, 'dropped': dropped},
              open(os.path.join(out, 'reading_fixes.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'fixes: {len(kept)} pass the machine bar, {len(manual)} need a read, '
          f'{len(dropped)} dropped -> review/{unit.slug}/reading_check.md')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', required=True)
    ap.add_argument('--letters', default='')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--batch', action='store_true')
    ap.add_argument('--collect', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--verify', action='store_true')
    a = ap.parse_args()
    unit = unitlib.one_unit(a.unit)
    corpus = Corpus(unit); meta = load_meta(unit); order = reading_order(meta)
    rulings = unitlib.load_rulings(unit)
    lids = [x.strip() for x in a.letters.split(',') if x.strip()] or order
    missing = [l for l in lids if l not in meta or l not in corpus.docs]
    if missing:
        sys.exit(f'unknown letters: {missing}')
    if a.check:
        return run_check(unit, corpus, meta)
    if a.verify:
        return run_verify(unit, corpus, meta, lids, batch=a.batch)
    if a.collect:
        return run_collect(unit, corpus)
    if a.dry_run:
        return run_dry(unit, corpus, meta, order, rulings, lids)
    if a.batch:
        return run_batch(unit, corpus, meta, order, rulings, lids)
    run_live(unit, corpus, meta, order, rulings, lids)


if __name__ == '__main__':
    main()
