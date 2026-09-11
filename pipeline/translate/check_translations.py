# -*- coding: utf-8 -*-
"""Mechanical checks on the translations. No API calls, no cost.

    python check_translations.py                # check everything, write sheet + report
    python check_translations.py --letters 48   # just these
    python check_translations.py --tag B        # check a second witness instead

The premise: a translation reads fluently whether or not it is faithful, so
fluency tells you nothing and the only trustworthy checks are the ones that do
not depend on reading the English at all. These are those checks.

What is genuinely catchable, and checked here:
  numbers       every numeral of two digits or more must survive into the English
  names         every catalogued name must survive; names not in the German are inventions
  markers       no mark of doubt may be lost (a smoothed-over hole), and the model's
                own count must match what it actually emitted. Markers the English
                adds where the German has none are NOT a failure - they are reported
                as `unmarked-in-german`, and they are the most valuable rows here,
                because they point at corruption the transcription never flagged
  rare pairs    all 42 corpus occurrences of Anweisung/Abweisung and
                committirt/exmittirt must be flagged - this one blocks publication
  glossary      wherever a termbase pattern fires in the German, the agreed
                English rendering must appear, so 318 letters do not drift apart
  structure     segment count must equal the manuscript page count
  ratio         wildly long or short output, or German left untranslated

What is NOT catchable here, stated plainly rather than faked: the common
function-word confusions (nach/noch, als/da, wie/wir, vor/von) run to about nine
occurrences per page. Nothing mechanical can tell a correct 'nach' from a
misread 'noch' when both make fluent sense. Those depend on the model flagging
them, on the targeted second witness in collate_translations.py, and on a small
sampled spot-check seeded here so a reviewer can calibrate whether the model is
under-flagging.

Rulings you have already given live in translation_rulings.json and are not
raised again, exactly as name_rulings.json works.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import unitlib
import termbase
import io, os, re, sys, csv, json, random, argparse

import yaml
import sys

_STDOUT = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdout = _STDOUT
_KEEP = []          # see known_names(): stops a borrowed wrapper closing our buffer
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = os.path.join(ROOT, 'review', 'translation_review.csv')
REPORT = os.path.join(ROOT, 'review', 'translation_report.md')
NOTES = os.path.join(ROOT, 'review', 'transcription_candidates.csv')
INFO = os.path.join(ROOT, 'review', 'translation_annotations.csv')
RULINGS = os.path.join(ROOT, 'reference', 'translation_rulings.json')

SPOTCHECK_PER_LETTER = 1      # unflagged watch-list samples, as a calibration probe
                              # (per LETTER, not per page - it was firing on every
                              #  page, which put ~1,500 probe rows in a sheet meant
                              #  for actual queries)
RATIO_LO, RATIO_HI = 0.55, 1.9

DIGITS = re.compile(r'\d[\d.,/]*')
DE_MARKER = re.compile(r'\[[^\]]*\?\]|\[\.\.\.\]')
EN_MARKER = re.compile(r'\[illegible\]|\[uncertain:[^\]]*\]|\[text lost\]')
# German function words surviving into the English in a run - the model lapsing
# into copying rather than translating.
DE_RUN = re.compile(r'\b(?:der|die|das|und|nicht|werden|worden|wegen|welche|'
                    r'dieses|solche|daß|dass|sich|nach|noch)\b', re.I)


def known_names():
    """The names worth checking survived the crossing.

    Deliberately NOT name_review_sheet.known_names(): that is a *suppression*
    set - everything already settled, including the `rejected` list of ordinary
    German words like Sachen, Jemanden and Rath that were confirmed as not
    needing attention. Checking those as if they were proper nouns produces
    nothing but noise. The real catalogue of names is name_seeds.json, which
    carries a kind for each entry, so person and place names can be taken and
    ordinary vocabulary left behind.
    """
    p = os.path.join(ROOT, 'reference', 'name_seeds.json')
    if not os.path.isfile(p):
        return set()
    seeds = json.load(open(p, encoding='utf-8'))
    return {e['name'] for e in seeds
            if e.get('kind') in ('person', 'place') and len(e['name']) >= 4}


def _is_exonym_render(word, glossary):
    """"Vienna" is not an invented name just because the German said "Wien".

    Nor is "Trabczyn" an invented name because the page spelled it Trombczin.
    Both sections are renderings the prompt asked for, so both exempt.
    """
    w = word.lower()
    return any(w in (e['render'] or '').lower()
               for sect in ('exonyms', 'canonical_names')
               for e in glossary.get(sect, []))


def _left_in_german(entry, en):
    """Is this term's own German form standing in the English?

    Only meaningful for `policy: translate`. The term's spelling is used, not
    its pattern: a pattern is written wide enough to catch inflections and
    misreadings, and matching those against the English would report a cognate
    as leakage. The bare word the termbase names is the thing that must not be
    there.

    Skipped where the term IS its English - Berlin, Hanover, England - since
    then the German form standing in the English is the correct answer.
    """
    term = (entry.get('term') or '').strip()
    render = (entry.get('render') or '').strip()
    if not term or len(term) < 4 or term.lower() == render.lower():
        return False
    if term.lower() in render.lower():
        return False
    return bool(re.search(r'\b' + re.escape(term) + r'\b', en))


def _renders(glossary):
    """Every English rendering the prompt asked for, lowercased."""
    return [(e.get('render') or '').lower()
            for sect, _ in termbase.SECTIONS
            for e in glossary.get(sect, [])
            if e.get('render')]


def _invented(core, de, glossary):
    """Is this reported English name absent from the German - a real invention?

    The check exists to catch a name the translation supplied and the page does
    not have. It is NOT a check that the English copied the German, and the
    difference became the whole story once the edition ruled that everything
    goes into English: the translation now reports `Prince of
    Hohenlohe-Ingelfingen`, `monastery of Ląd`, `Mr. Leixner` and `Christmas`,
    every one of them correct, and the old test called all four inventions
    because it took the first five characters of the whole phrase and looked
    for them in the German. Thirty-two deeds produced 97 such rows, which
    across the corpus would have buried the five real ones.

    So: a name is invented only when NOTHING in it is on the page. Any content
    word that stem-matches the German acquits the whole phrase - the rest is
    the translated title, particle or honorific that was asked for. A phrase
    that is itself a termbase rendering is acquitted too, inflections included,
    which is what `South Prussian` needed against a render of `South Prussia`.
    """
    core = core.strip()
    if not core or '[' in core or ']' in core:
        return False                      # a mark of doubt, not a name
    low, del_ = core.lower(), de.lower()
    head = low.split()[0] if low.split() else ''
    for r in _renders(glossary):
        if not r:
            continue
        if low in r or r in low:
            return False
        # `Frankfurt a/O.` against a render of `Frankfurt an der Oder`: neither
        # contains the other, but the head word is the place and it agrees.
        if head and len(head) >= 4 and r.split()[:1] == [head]:
            return False
    # Length floor 4, except for a capitalised short word: `Ląd` is three
    # characters and is the entire identity of `monastery of Ląd`.
    words = [w for w in re.findall(r"[^\W\d_]+", core)
             if w.lower() not in _EMPTY
             and (len(w) >= 4 or (len(w) >= 3 and w[:1].isupper()))]
    if not words:
        return False                      # nothing in it identifies anyone
    for w in words:
        stem = re.sub(r'(s|n|en|es)$', '', w)[:5].lower()
        if len(stem) >= 3 and stem in del_:
            return False                  # this much of the name IS on the page
    return True


def load_rulings():
    if os.path.isfile(RULINGS):
        r = json.load(open(RULINGS, encoding='utf-8'))
        return set(r.get('cleared', []))
    return set()


def norm_num(s):
    """23.000 / 23,000 / 23000 all compare equal; ordinals keep their digits."""
    return re.sub(r'[.,/]', '', s)


def page_source(rec, page_no):
    for p in rec['pages']:
        if p['page'] == page_no:
            return p.get('reading') or p.get('diplomatic') or ''
    return ''


# Words that carry none of a rendering's identity. "Your Most Serene Highness"
# and "His Most Serene Highness" are the same term of art; the deeds refer to
# the Fürst in the third person where the letters address him in the second,
# and a check keyed on the pronoun raised 26 rows saying so.
_EMPTY = {'your', 'his', 'her', 'their', 'our', 'the', 'a', 'an', 'of', 'and',
          'in', 'on', 'to', 'for', 'most', 'by'}


def rendering_present(want, en):
    """Is the agreed English rendering there, allowing for inflection?

    The old test looked for the rendering's first characters verbatim, so
    `dismemberment` was reported missing from a page reading "dismembered",
    `propination rights` from one reading "propination lessee", and every
    third-person honorific from every deed in the volume. Those are not drift.

    A rendering counts as present when each of its content words appears in
    some inflected form - matched on a stem, so `lease` finds `leased` but not
    `least`. Drift that matters - a term rendered by a different English word
    altogether - still raises its row.
    """
    words = [w for w in re.findall(r"[^\W\d_]+", want) if w.lower() not in _EMPTY]
    if not words:                       # a rendering of nothing but stopwords
        words = re.findall(r"[^\W\d_]+", want)
    for w in words:
        stem = w[:max(4, len(w) - 3)]
        if not re.search(r'\b' + re.escape(stem), en, re.I):
            return False
    return True


def check_letter(rec, out, glossary, canon, rng):
    """Return (rows, stats) for one translated letter."""
    rows = []
    lid = str(rec['letter_id'])
    segs = {p.get('page'): p for p in out.get('pages', [])}

    # -- structure: fail closed, nothing downstream is trustworthy without it --
    if len(out.get('pages', [])) != len(rec['pages']):
        rows.append(dict(kind='structure', page='', german='', english='',
                         note=f"{len(out.get('pages', []))} segment(s) for "
                              f"{len(rec['pages'])} manuscript page(s)"))
        return rows, {'structure': 1}

    # Terms whose English is deliberately not the German word. Built from
    # BOTH sections that do that: exonyms (Wien -> Vienna) and the generated
    # canonical names (Trombczin -> Trabczyn). Without the second, every
    # canonicalisation the prompt asked for came back as a lost name.
    exonyms = set()
    exo_rx = []
    for sect in ('exonyms', 'canonical_names'):
        for e in glossary.get(sect, []):
            exonyms.update(re.findall(r'[^\W\d_]{4,}', e['term']))
            # The term's own spelling is not the only one it covers. `Sachsen`
            # is the term; the page says `Sachßen`, which the entry's PATTERN
            # matches and its spelling does not - so the token was checked as a
            # name, found absent from an English reading `Saxony`, and reported
            # lost. Ten times, for one entry. Test the pattern, which is what
            # the entry actually asserts.
            try:
                exo_rx.append(re.compile(e['pattern'], re.I))
            except re.error:
                pass

    stats = {}
    letter_probe = []
    for p in rec['pages']:
        n = p['page']
        seg = segs.get(n)
        de = p.get('reading') or p.get('diplomatic') or ''
        if seg is None:
            rows.append(dict(kind='structure', page=n, german='', english='',
                             note='no segment returned for this page'))
            continue
        en = seg.get('en') or ''

        # -- numbers -------------------------------------------------------
        # Two digits or more. Bare single digits are list numbering ("ad 2.",
        # "3.") far more often than money, and checking them buries the real
        # figures - which are the whole point - under enumeration noise.
        en_nums = {norm_num(x) for x in DIGITS.findall(en)}
        for raw in DIGITS.findall(de):
            v = norm_num(raw)
            if len(v) >= 2 and v not in en_nums:
                rows.append(dict(kind='number-check', page=n, german=raw, english='',
                                 note='numeral in the German does not appear in the English'))
                stats['number'] = stats.get('number', 0) + 1

        # -- names ---------------------------------------------------------
        for tok in set(re.findall(r'[^\W\d_]{4,}', de)):
            if tok in exonyms or any(rx.fullmatch(tok) for rx in exo_rx):
                continue      # correctly rendered into English; checked as glossary
            if tok in canon and tok not in en:
                # a stem match satisfies it: German inflects, English possesses
                if not re.search(re.escape(tok[:max(4, len(tok) - 2)]), en, re.I):
                    rows.append(dict(kind='name-check', page=n, german=tok, english='',
                                     note='name in the German is absent from the English'))
                    stats['name'] = stats.get('name', 0) + 1
        for nm in seg.get('names') or []:
            # The tool returns pairs now - {de: what the page says, en: what
            # the English used}. Old cache files hold bare strings, and both
            # shapes have to survive a sheet built over a part-migrated cache.
            if isinstance(nm, dict):
                nm = (nm.get('en') or nm.get('de') or '').strip()
            if not isinstance(nm, str) or not nm.strip():
                continue
            core = re.sub(r'^(v\.?|von|de)\s+', '', nm).strip()
            if _invented(core, de, glossary):
                rows.append(dict(kind='name-check', page=n, german='', english=nm,
                                 note='name reported in the English is not in the German'))
                stats['name'] = stats.get('name', 0) + 1

        # -- markers -------------------------------------------------------
        # Two different questions, and conflating them was wrong. First: did a
        # hole get smoothed over? That is en < de, and it is a failure. Second:
        # did the model mark something the German does NOT mark? That is en > de
        # - not a failure at all but the most interesting output this pipeline
        # produces, because it points at corruption the transcription never
        # flagged. It gets its own kind so it can be read as a finding.
        de_m, en_m = len(DE_MARKER.findall(de)), len(EN_MARKER.findall(en))
        said = seg.get('marker_count')
        if en_m < de_m:
            rows.append(dict(kind='marker-check', page=n, german=f'{de_m} in German',
                             english=f'{en_m} in English',
                             note='a mark of doubt in the German is missing from the '
                                  'English - a hole may have been smoothed over'))
            stats['marker'] = stats.get('marker', 0) + 1
        elif en_m > de_m:
            rows.append(dict(kind='unmarked-in-german', page=n,
                             german=f'{de_m} marked', english=f'{en_m} marked',
                             note='the translator marked doubt where the German marks '
                                  'none - candidate silent transcription corruption'))
        if said is not None and said != en_m:
            rows.append(dict(kind='marker-check', page=n, german='', english=f'{en_m} present',
                             note=f'model reported {said} markers but emitted {en_m}'))
            stats['marker'] = stats.get('marker', 0) + 1

        # -- rare pairs: exhaustive, and blocking --------------------------
        flagged_de = ' '.join((f.get('de') or '') for f in (seg.get('flagged') or []))
        for e in glossary['rare_pairs']:
            for m in re.finditer(e['pattern'], de, re.I):
                word = m.group(0)
                if word.lower() not in flagged_de.lower():
                    rows.append(dict(kind='rare-pair', page=n, german=word, english='',
                                     note=f"{e['pair'][0]}/{e['pair'][1]} occurrence not "
                                          f"flagged by the model - blocks publication"))
                    stats['rare'] = stats.get('rare', 0) + 1

        # -- renderings that must never appear -----------------------------
        # Everything else here asks whether the right English arrived. This
        # asks whether the wrong English did. It is the only check that can
        # stop a correction the edition already made being made again by the
        # next translation pass: hypocaustum came back as a chestnut table
        # once, and nothing in this file could have caught it a second time.
        for rx, when, render, why in termbase.forbidden(glossary):
            if rx.search(en) and (when is None or when.search(de)):
                rows.append(dict(kind='forbidden-render', page=n, german='',
                                 english=render,
                                 note=why or 'a rendering this edition has ruled against'))
                stats['forbidden'] = stats.get('forbidden', 0) + 1

        # -- glossary consistency ------------------------------------------
        # The same tuple the prompt is built from, so a section cannot be
        # enforced without being taught. `exonyms` was enforced and never
        # taught for the whole of the first published pass.
        for sect, _ in termbase.SECTIONS:
            for e in glossary[sect]:
                if re.search(e['pattern'], de, re.I):
                    want = e['render']
                    # `also` is for a German word with more than one correct
                    # English depending on sense. Pohlen is Poland and the
                    # Poles; demanding the first reported every page using the
                    # second as drift, 38 times over.
                    if not any(rendering_present(w, en)
                               for w in [want] + list(e.get('also') or [])):
                        rows.append(dict(kind='glossary-mismatch', page=n,
                                         german=e['term'], english=want,
                                         note='termbase rendering not found in the English'))
                        stats['glossary'] = stats.get('glossary', 0) + 1
                    elif e['policy'] == 'translate' and _left_in_german(e, en):
                        # The rendering test is a stem match, so it cannot tell
                        # `Michaelmas` from `Michaelis` - the German word shares
                        # the stem and satisfies the check while standing
                        # untranslated in an English sentence. That is the exact
                        # failure the house rule forbids, and it passed silently
                        # 28 times. Asking the opposite question catches it:
                        # for a term the edition says to TRANSLATE, the German
                        # word appearing verbatim in the English is leakage.
                        rows.append(dict(kind='untranslated-term', page=n,
                                         german=e['term'], english=want,
                                         note='the German term stands untranslated in '
                                              'the English, though the rendering is '
                                              'also present'))
                        stats['untranslated_term'] = stats.get('untranslated_term', 0) + 1

        # -- gaps: the reliable damage signal is the marker, not a line range --
        if '[...]' in de:
            rows.append(dict(kind='damage-page', page=n, german='[...]', english='',
                             note='page carries a gap or damaged edge; confirm the '
                                  'English shows the hole rather than bridging it'))

        # -- shape ----------------------------------------------------------
        dw, ew = len(de.split()), len(en.split())
        if dw > 40:
            ratio = ew / dw
            if not (RATIO_LO <= ratio <= RATIO_HI):
                rows.append(dict(kind='ratio', page=n, german=f'{dw} words',
                                 english=f'{ew} words',
                                 note=f'English/German ratio {ratio:.2f} - possible '
                                      f'truncation or padding'))
                stats['ratio'] = stats.get('ratio', 0) + 1
        if ew > 30 and len(DE_RUN.findall(en)) >= 4:
            rows.append(dict(kind='untranslated', page=n, german='', english=en[:60],
                             note='German function words survive in the English'))
            stats['untranslated'] = stats.get('untranslated', 0) + 1

        # -- model's own reports, passed through for your eyes -------------
        for u in seg.get('unparseable') or []:
            rows.append(dict(kind='unparseable', page=n, german=(u.get('de') or '')[:80],
                             english='', note=(u.get('why') or '')[:120]))
        for f in seg.get('flagged') or []:
            rows.append(dict(kind='flagged', page=n, german=(f.get('de') or '')[:80],
                             english=(f.get('rendered_as') or '')[:80],
                             note=('alt: ' + (f.get('alt') or '')[:60] + ' | '
                                   + (f.get('why') or ''))[:160]))
        # Emendations split into two quite different things, and lumping them
        # together was what made this sheet unreadable. If the corrupt token
        # never reached the English, the translation is already sound and the
        # note is a finding about the TRANSCRIPTION - it belongs in the corpus
        # correction queue, not in a translation review. Only where the mangled
        # token rode into the English is the reading copy actually damaged.
        for s in seg.get('emendation_suggestions') or []:
            de_s, prop = (s.get('de') or ''), (s.get('proposed') or '')
            toks = re.findall(r'[^\W\d_]{4,}', de_s)
            rode_in = any(t in en for t in toks)
            hedged = any(c in prop for c in '?/') or ' or ' in prop.lower()
            row = dict(page=n, german=de_s[:80], english=prop[:80],
                       note=(s.get('why') or '')[:160])
            if not rode_in:
                row['kind'] = 'transcription-note'      # English already reads correctly
            elif hedged:
                row['kind'] = 'emendation-uncertain'    # keep visible to the reader
            else:
                row['kind'] = 'emendation-degrades'     # reading copy damaged here
                stats['degrades'] = stats.get('degrades', 0) + 1
            rows.append(row)

        # -- watch-list calibration probe ----------------------------------
        cands = []
        for e in glossary['watchlist']:
            for w in e['pair']:
                for m in re.finditer(rf'\b{w}\b', de, re.I):
                    ctx = de[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ')
                    if w.lower() not in flagged_de.lower():
                        cands.append((w, ctx))
        letter_probe.extend((n, w, ctx) for w, ctx in cands)

    for n, w, ctx in rng.sample(letter_probe, min(SPOTCHECK_PER_LETTER, len(letter_probe))):
        rows.append(dict(kind='watchlist-spotcheck', page=n, german=ctx[:80],
                         english='', note=f'random sample on "{w}" - not a suspected '
                                          f'error, a probe on under-flagging'))
    return rows, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--letters', default='')
    ap.add_argument('--tag', default=None)
    a = ap.parse_args()
    a.unit = unitlib.resolve_unit(a.unit)
    # review sheets belong to their unit, not to the project
    globals()['SHEET'] = os.path.join(unitlib.review_dir(a.unit), 'translation_review.csv')
    globals()['REPORT'] = os.path.join(unitlib.review_dir(a.unit), 'translation_report.md')
    globals()['NOTES'] = os.path.join(unitlib.review_dir(a.unit), 'transcription_candidates.csv')
    globals()['INFO'] = os.path.join(unitlib.review_dir(a.unit), 'translation_annotations.csv')

    src = os.path.join(ROOT, 'cache', 'translation-raw' + (f'-{a.tag}' if a.tag else ''))
    if not os.path.isdir(src):
        sys.exit(f'no translations at {src} - run translate.py first')

    # Keyed by pad, not by letter_id: the archive's own number is unique only
    # inside its holding, and both units have a document 2.
    recs = unitlib.records_by_pad(ROOT)
    # Through termbase.load(), so the CANONICAL NAMES the prompt was given
    # and the CANONICAL NAMES enforced here are the same list by construction.
    glossary = termbase.load()
    canon = known_names()
    cleared = load_rulings()
    want = {x.strip() for x in a.letters.split(',') if x.strip()}

    all_rows, per_letter, blocked = [], {}, set()
    for fn in unitlib.scope_to_unit(sorted(os.listdir(src)), a.unit):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        out = json.load(open(os.path.join(src, fn), encoding='utf-8'))
        lid = str(out.get('letter'))
        # the filename is the pad, and is the only identifier in a cache file
        # that carries its unit
        pad = os.path.splitext(fn)[0]
        if want and lid not in want:
            continue
        rec = recs.get(pad)
        if rec is None:
            continue
        rng = random.Random(f'spotcheck-{pad}')       # seeded: reproducible probes
        rows, stats = check_letter(rec, out, glossary, canon, rng)
        rows = [r for r in rows
                if f"{pad}|{r['page']}|{r['kind']}|{r['german']}" not in cleared]
        for r in rows:
            r['pad'] = pad
            r['letter'] = lid
            r['ruling'] = ''
        # forbidden-render joins the two blocking kinds: it means a reading
        # the edition has already corrected has come back, and publishing it
        # would put the error in print a second time.
        if any(r['kind'] in ('rare-pair', 'structure', 'forbidden-render')
               for r in rows):
            blocked.add(lid)
        all_rows.extend(rows)
        per_letter[pad] = stats

    # Fold in the second witness's meaning-level disagreements, if one has been
    # run. They belong in the same sheet: one place to look, not two.
    div = os.path.join(ROOT, 'review', 'translation_divergence.json')
    if os.path.isfile(div):
        for r in json.load(open(div, encoding='utf-8')):
            if want and str(r['letter']) not in want:
                continue
            if f"{r['letter']}|{r['page']}|divergence|{r['german']}" in cleared:
                continue
            r.setdefault('ruling', '')
            all_rows.append(r)

    # Two audiences, two sheets. A note about the transcription is not a query
    # about the translation, and mixing them made the review sheet four times
    # longer than the work it actually represents.
    # Three audiences, three files. The review sheet should hold only what
    # needs a decision from a person. `flagged` and `unparseable` are the
    # translator showing its working - they never reach the reader, who sees
    # only the [illegible]/[uncertain: ] marks in the text itself - so they are
    # reference material, not queries.
    INFO_KINDS = {'flagged', 'unparseable', 'watchlist-spotcheck'}
    notes = [r for r in all_rows if r['kind'] == 'transcription-note']
    info = [r for r in all_rows if r['kind'] in INFO_KINDS]
    all_rows = [r for r in all_rows
                if r['kind'] != 'transcription-note' and r['kind'] not in INFO_KINDS]

    cols = ['letter', 'pad', 'page', 'kind', 'german', 'english', 'note', 'ruling']
    with open(SHEET, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        w.writerows(all_rows)
    for path, data in ((NOTES, notes), (INFO, info)):
        with open(path, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, cols)
            w.writeheader()
            w.writerows(data)

    by_kind = {}
    for r in all_rows:
        by_kind[r['kind']] = by_kind.get(r['kind'], 0) + 1

    lines = ['# Translation check report', '',
             f'{len(per_letter)} letter(s) checked, {len(all_rows)} row(s) raised.', '']
    if blocked:
        lines += ['## Blocked from publication', '',
                  'A rare-pair occurrence went unflagged, or the segment count did not '
                  'match the page count. Both mean something is wrong that a reader '
                  'could not see.', '',
                  '  ' + ', '.join(f'L{x}' for x in sorted(blocked)), '']
    lines += ['## Rows by kind', '', '| kind | count |', '|---|---|']
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        lines.append(f'| {k} | {v} |')
    lines += ['', '## Not checkable here', '',
              'The common function-word confusions (nach/noch, als/da, wie/wir, '
              'vor/von) run to roughly nine occurrences per manuscript page. No '
              'mechanical test distinguishes a correct one from a misread one when '
              'both are fluent. They rely on the model flagging them, on the second '
              'witness in collate_translations.py, and on the seeded '
              '`watchlist-spotcheck` rows above.', '']
    open(REPORT, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

    print(f'{len(per_letter)} letter(s) checked, {len(all_rows)} row(s) raised')
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f'  {v:>5}  {k}')
    if blocked:
        print('\nblocked from publication: ' + ', '.join(f'L{x}' for x in sorted(blocked)))
    print(f'\nwrote {SHEET}\nwrote {REPORT}')


if __name__ == '__main__':
    main()
