# -*- coding: utf-8 -*-
"""Match the gazetteer's 112 places against the three Polish reference works.

    python pipeline/gazetteer/match_sources.py            # build candidates, write the log and the page
    python pipeline/gazetteer/match_sources.py --apply <file>   # merge the editor's decisions

The databases are the converted texts of Igor's repository
(C:\\Users\\Tersnaus\\Downloads\\polish-place-name-sources\\sources\\; its
RIGHTS.md permits reading, searching and citing): Nazwy miejscowe Polski
(sources/nmpol/, alphabetical, stops at Sw), the Kodeks
dyplomatyczny Wielkopolski (sources/kdw/, by charter) and the Slownik
geograficzny (sources/sg/, by page; the entries run inline, each beginning
after a period).

What is written, and where:

- review/place_name_sources/matches.json  the candidates in full, snippets
  included. NOT committed: review/ is the editor's machine, and two of the
  three works are in copyright - the public repository carries no text of
  them (RIGHTS.md).
- review/place_name_sources/match_log.html  the decision page, the matches
  embedded; opened in a browser; a Save button gives match_decisions.json,
  which --apply merges back.
- pipeline/gazetteer/source_matches.yml  the record the edition keeps:
  per place, per source, each candidate's locator, whether its context
  names the area, and the editor's decision. Locators and decisions only,
  no snippet text (the repository is public).

A match is made on name plus administrative context, never the bare name
(docs/known-limits.md of that repository: Rogowo twelve entries,
Dabrowka past eighty). The context qualifiers of our ground: the powiat of
Slupca, the gmina and parish of Trabczyn, the parish of Zagorow, and the
neighbouring places and lords the entries name (Lad, Pyzdry, Konin,
Slupca). A candidate without a qualifying context is shown to the editor
with its context marked unknown; nothing is auto-accepted.

Decisions: yes (this is our place), no (another place of the same name),
unsure (keep open). A candidate already cited by the entry's footnotes is
pre-decided yes ("already cited"); a Kodeks charter already in the edition
but not yet cited is left to the editor.
"""
import bisect
import io
import json
import os
import re
import sys
import unicodedata

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SOURCES = r'C:\Users\Tersnaus\Downloads\polish-place-name-sources\sources'
REVIEW = os.path.join(ROOT, 'review', 'place_name_sources')
LOG = os.path.join(ROOT, 'pipeline', 'gazetteer', 'source_matches.yml')

CONTEXT = ['slupecki', 'gm. trabczyn', 'par. trabczyn', 'par. zagorow',
           'zagorow', 'trabczyn', 'pow. konin', 'kosko', 'rzgow', 'pyzdry',
           'slupca', 'wrabczyn', 'lukom', 'mieliszew', 'ciesle', 'kawnice',
           'petrykowo', 'ostrowit']

MAX_MENTIONS = 15


def fold_map(s):
    """Ascii-fold with a map back to raw positions: returns (folded, idxmap)
    where idxmap[i] is the raw index of folded[i]."""
    out, idx = [], []
    for i, ch in enumerate(s):
        d = unicodedata.normalize('NFD', ch)
        for part in d:
            if unicodedata.combining(part):
                continue
            out.append(part)
            idx.append(i)
    folded = ''.join(out).translate(str.maketrans(
        {'ł': 'l', 'Ł': 'L', 'ø': 'o', 'Ø': 'O', 'ß': 'ss', 'æ': 'ae', 'Æ': 'AE'})).lower()
    # translate changes length for the multi-char maps; rebuild the map by
    # walking the translated string
    return folded, idx


def load_gazetteer():
    """slug -> record, from reference/gazetteer/ (the editor's 112)."""
    out = {}
    d = os.path.join(ROOT, 'reference', 'gazetteer')
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.yml') or fn.startswith('source'):
            continue
        with open(os.path.join(d, fn), encoding='utf-8') as f:
            g = yaml.safe_load(f) or {}
        forms = []
        for form in [g.get('heading')] + [n.get('form') for n in (g.get('names') or [])
                                          if n.get('form')] + list(g.get('aliases') or []):
            if form and form not in forms:
                forms.append(form)
        reg = None
        if g.get('register'):
            with open(os.path.join(ROOT, 'reference', 'places.yml'), encoding='utf-8') as f:
                reg = (yaml.safe_load(f) or {}).get('places', {}).get(g['register'])
        if reg:
            for v in reg.get('variants') or []:
                form = v if isinstance(v, str) else v.get('form')
                if form and form not in forms:
                    forms.append(form)
        out[g['slug']] = {'heading': g.get('heading') or g['slug'],
                          'kind_text': g.get('kind_text') or '',
                          'location': (g.get('location') or {}).get('text', ''),
                          'status': g.get('status') or 'extant',
                          'register': g.get('register'),
                          'text': (g.get('text_en') or '').strip(),
                          'forms': forms}
    return out


def alternation(form_to_places):
    """One compiled regex over every folded form; groups name the form."""
    forms = sorted({fold_map(f)[0] for f in form_to_places if len(fold_map(f)[0]) >= 3},
                   key=len, reverse=True)
    pat = re.compile(r'(?<![a-z0-9])(' + '|'.join(re.escape(f) for f in forms) + r')(?![a-z0-9])')
    return pat


def load_forms():
    gaz = load_gazetteer()
    form_to_places = {}
    for slug, g in gaz.items():
        for f in g['forms']:
            ff = fold_map(f)[0]
            if len(ff) >= 3:
                form_to_places.setdefault(ff, set()).add(slug)
    return gaz, form_to_places


# ---------------------------------------------------------------- the Slownik

def sg_pages(text):
    """(positions, pages) for the anchors <!-- p.NNN -->."""
    pos, pages = [], []
    for m in re.finditer(r'<!-- p\.(\d+) -->', text):
        pos.append(m.end())
        pages.append(int(m.group(1)))
    return pos, pages


def sg_scan():
    gaz, form_to_places = load_forms()
    pat = alternation(form_to_places)
    out = {slug: [] for slug in gaz}
    d = os.path.join(SOURCES, 'sg')
    for fn in sorted(os.listdir(d)):
        if not re.match(r'sg\d+\.md$', fn):
            continue
        vol = int(re.match(r'sg(\d+)\.md$', fn).group(1))
        raw = io.open(os.path.join(d, fn), encoding='utf-8').read()
        folded, idx = fold_map(raw)
        apos, apages = sg_pages(raw)
        for m in pat.finditer(folded):
            form = m.group(1)
            rpos = idx[m.start()]
            page = apages[bisect.bisect_right(apos, rpos) - 1] if apos else 0
            before = raw[max(0, rpos - 4):rpos]
            kind = 'entry' if (rpos == 0 or before.rstrip().endswith('.') or before.endswith('\n')
                               or before.rstrip().endswith('>')) else 'mention'
            window = raw[rpos:rpos + 560]
            cut = window.rfind('. ')
            snippet = window[:cut + 1].strip() if cut > 80 else window.strip()
            for slug in form_to_places[form]:
                out[slug].append({'vol': vol, 'page': page, 'kind': kind,
                                  'form': form, 'head': ' '.join(snippet[:110].split()),
                                  'snippet': ' '.join(snippet.split())[:420]})
    out_entries_all = [c for rows in out.values() for c in rows]
    # an entry stands when its context names our ground or its headword is
    # the place's own name; a mention without context is noise (a common
    # word in every second description) and is dropped; a mention with
    # context - the gmina and parish tables - is kept, capped.
    # A form that floods the dictionary (Laski, Maly: the common words and
    # the common village names with hundreds of entries) must show our
    # ground in its context even as an entry, or it is dropped: a place
    # called by a common word is found by its powiat, not by its name.
    per_form_entries = {}
    for c in out_entries_all:
        if c['kind'] == 'entry':
            per_form_entries[c['form']] = per_form_entries.get(c['form'], 0) + 1
    flooded = {f for f, n in per_form_entries.items() if n > 30}
    headings = {slug: fold_map(g['heading'])[0] for slug, g in gaz.items()}
    for slug in out:
        keep = []
        for c in out[slug]:
            if c['kind'] == 'entry':
                if c['form'] in flooded:
                    if context_of(c['snippet'])[0] == 'ok':
                        keep.append(c)
                elif c['form'] == headings[slug] or context_of(c['snippet'])[0] == 'ok':
                    keep.append(c)
        mentions = [c for c in out[slug]
                    if c['kind'] == 'mention' and context_of(c['snippet'])[0] == 'ok']
        keep.extend(mentions[:MAX_MENTIONS])
        keep.sort(key=lambda c: (0 if c['kind'] == 'entry' else 1, c['vol'], c['page']))
        out[slug] = keep
    return out


# ------------------------------------------------------------------ the Kodeks

def load_kdw_index():
    index = {}
    d = os.path.join(SOURCES, 'kdw')
    for fn in sorted(os.listdir(d)):
        if not re.match(r'kdw\d+\.md$', fn):
            continue
        vol = int(re.match(r'kdw(\d+)\.md$', fn).group(1))
        raw = io.open(os.path.join(d, fn), encoding='utf-8').read()
        heads = [(m.start(), int(m.group(1))) for m in
                 re.finditer(r'(?m)^## Dokument Nr (\d+)\s*$', raw)]
        # the longest body per number (the volume's regest index repeats the
        # headings with regests only)
        best = {}
        for i, (start, num) in enumerate(heads):
            end = heads[i + 1][0] if i + 1 < len(heads) else len(raw)
            if num not in best or (end - start) > (best[num][2] - best[num][1]):
                best[num] = (num, start, end)
        index[vol] = {'raw': raw, 'charters': sorted(best.values())}
    return index


def kdw_scan(index):
    gaz, form_to_places = load_forms()
    pat = alternation(form_to_places)
    out = {slug: {} for slug in gaz}
    for vol, data in sorted(index.items()):
        raw = data['raw']
        folded, idx = fold_map(raw)
        bounds = [(s, e, n) for n, s, e in data['charters']]
        starts = [b[0] for b in bounds]
        for m in pat.finditer(folded):
            form = m.group(1)
            rpos = idx[m.start()]
            i = bisect.bisect_right(starts, rpos) - 1
            if i < 0:
                continue
            s, e, num = bounds[i]
            window = raw[max(s, rpos - 100):rpos + 160]
            for slug in form_to_places[form]:
                rec = out[slug].setdefault(num, {'vol': vol, 'num': num,
                                                 'hits': 0, 'forms': set(),
                                                 'snippet': ''})
                rec['hits'] += 1
                rec['forms'].add(form)
                if len(rec['snippet']) < 200:
                    rec['snippet'] = ' '.join(window.split())[:260]
    result = {}
    for slug, by_num in out.items():
        rows = []
        for num in sorted(by_num):
            r = by_num[num]
            # the date from the charter's heading line
            head = ''
            for n, s, e in index[r['vol']]['charters']:
                if n == num:
                    body = index[r['vol']]['raw'][s:e]
                    lines = body.split('\n')
                    head = lines[1] if len(lines) > 1 else ''
                    break
            ym = re.search(r'\b(1[0-9]{3}|[89][0-9]{2})\b', head)
            rows.append({'vol': r['vol'], 'num': num, 'year': int(ym.group(1)) if ym else None,
                         'hits': r['hits'], 'head': ' '.join(head.split())[:160],
                         'snippet': r['snippet']})
        result[slug] = rows
    return result


# ------------------------------------------------------- Nazwy miejscowe Polski

def nmpol_block_starts(raw):
    """raw offsets of each paragraph's first character (headwords begin
    paragraphs; anchors sit on their own line before the block)."""
    starts = set()
    pos = 0
    for line in raw.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('<!--'):
            pos += len(line) + 1
            continue
        if not starts or True:
            pass
        pos += len(line) + 1
    # simpler: mark the first non-anchor character after each blank line
    starts = set()
    for m in re.finditer(r'(?:^|\n\s*\n)(?:<!--.*?-->\s*)*(\S)', raw, re.S):
        starts.add(m.start(1))
    return starts


def nmpol_scan():
    gaz, form_to_places = load_forms()
    pat = alternation(form_to_places)
    out = {slug: [] for slug in gaz}
    d = os.path.join(SOURCES, 'nmpol')
    for fn in sorted(os.listdir(d)):
        if not re.match(r't\d+\.md$', fn):
            continue
        tome = int(re.match(r't(\d+)\.md$', fn).group(1))
        raw = io.open(os.path.join(d, fn), encoding='utf-8').read()
        folded, idx = fold_map(raw)
        starts = nmpol_block_starts(raw)
        apos = [m.end() for m in re.finditer(r'<!-- p\.(\d+) -->', raw)]
        apages = [int(m.group(1)) for m in re.finditer(r'<!-- p\.(\d+) -->', raw)]
        for m in pat.finditer(folded):
            form = m.group(1)
            rpos = idx[m.start()]
            page = apages[bisect.bisect_right(apos, rpos) - 1] if apos else 0
            kind = 'entry' if rpos in starts else 'mention'
            window = raw[rpos:rpos + 560]
            cut = window.rfind('. ')
            snippet = window[:cut + 1].strip() if cut > 80 else window.strip()
            for slug in form_to_places[form]:
                out[slug].append({'tome': tome, 'page': page, 'kind': kind,
                                  'head': ' '.join(snippet[:110].split()),
                                  'snippet': ' '.join(snippet.split())[:420]})
    for slug in out:
        entries = [c for c in out[slug] if c['kind'] == 'entry']
        mentions = [c for c in out[slug]
                    if c['kind'] == 'mention' and context_of(c['snippet'])[0] == 'ok']
        mentions = mentions[:MAX_MENTIONS]
        entries.sort(key=lambda c: (c['tome'], c['page']))
        out[slug] = entries + mentions
    return out


# ------------------------------------------------------------- decisions

def kdw_docs_in_edition():
    with open(os.path.join(ROOT, 'units', 'kdw', 'rulings.yml'), encoding='utf-8') as f:
        r = yaml.safe_load(f) or {}
    cit = (r.get('documents') or {}).get('citation') or {}
    return {(int(c['volume']), int(c['number'])): int(doc) for doc, c in cit.items()}


def kdw_already_cited():
    out = {}
    d = os.path.join(ROOT, 'reference', 'gazetteer')
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.yml') or fn.startswith('source'):
            continue
        with open(os.path.join(d, fn), encoding='utf-8') as f:
            g = yaml.safe_load(f) or {}
        for fnote in g.get('footnotes') or []:
            for r in fnote.get('refs') or []:
                if r.get('source') != 'kdw':
                    continue
                m = re.match(r'vol\. (\d+), no\. (\d+)', r.get('locator') or '')
                if m:
                    out.setdefault((int(m.group(1)), int(m.group(2))), []).append(g['slug'])
    return out


def sg_already_cited():
    """slug -> set of pages the entry's own footnotes cite in the Slownik."""
    out = {}
    d = os.path.join(ROOT, 'reference', 'gazetteer')
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.yml') or fn.startswith('source'):
            continue
        with open(os.path.join(d, fn), encoding='utf-8') as f:
            g = yaml.safe_load(f) or {}
        pages = set()
        for fnote in g.get('footnotes') or []:
            for r in fnote.get('refs') or []:
                if r.get('source') != 'slownik':
                    continue
                for m in re.finditer(r'(\d+)(?:-(\d+))?', r.get('locator') or ''):
                    a = int(m.group(1))
                    b = int(m.group(2)) if m.group(2) else a
                    pages.update(range(a, b + 1))
        if pages:
            out[g['slug']] = pages
    return out


def context_of(snippet):
    fb = fold_map(snippet)[0]
    hit = [c for c in CONTEXT if c in fb]
    if hit:
        return 'ok', hit
    return ('unknown' if any(q in fb for q in ('pow.', 'gm.', 'par.')) else 'none'), hit


# The English of the snippets: translated in session by Claude (the editor's
# word, 2026-10-25: "Don't use a paid path; let's do it in-line here"), keyed
# by the SHA-1 of the exact text, and never committed - the two dictionaries
# are in copyright (their RIGHTS.md), so their text and its translation stay
# in review/ beside the snippets they translate.
TRANS_CACHE = os.path.join(REVIEW, 'translations.json')


def _load_translations():
    if os.path.exists(TRANS_CACHE):
        with open(TRANS_CACHE, encoding='utf-8') as f:
            return json.load(f)
    return {}


def _attach_en(rows, cache):
    import hashlib
    for row in rows:
        head = row.get('head')
        snip = row.get('snippet')
        if head and len(head) >= 12:
            h = hashlib.sha1(head.encode('utf-8')).hexdigest()[:12]
            if h in cache:
                row['en_head'] = cache[h]
        if snip and len(snip) >= 12:
            h = hashlib.sha1(snip.encode('utf-8')).hexdigest()[:12]
            if h in cache:
                row['en_snip'] = cache[h]
    return rows


def build():
    gaz = load_gazetteer()
    kidx = load_kdw_index()
    in_edition = kdw_docs_in_edition()
    cited = kdw_already_cited()
    sg_cited = sg_already_cited()

    previous = {}
    if os.path.exists(LOG):
        try:
            with open(LOG, encoding='utf-8') as f:
                previous = (yaml.safe_load(f) or {}).get('places') or {}
        except Exception:
            previous = {}
        if not isinstance(previous, dict):
            previous = {}

    sg_hits = sg_scan()
    kdw_hits = kdw_scan(kidx)
    nm_hits = nmpol_scan()

    out = {}
    for slug, g in gaz.items():
        rec = {'heading': g['heading'], 'kind_text': g['kind_text'],
               'location': g['location'], 'status': g['status'],
               'register': g['register'], 'forms': g['forms'],
               'sources': {}}

        rows = []
        for c in kdw_hits.get(slug, []):
            key = (c['vol'], c['num'])
            doc = in_edition.get(key)
            cited_by = cited.get(key) or []
            rows.append({'locator': 'vol. %d, no. %d' % key,
                         'year': c['year'], 'hits': c['hits'],
                         'head': c['head'], 'snippet': c['snippet'],
                         'doc': doc, 'cited_by': cited_by,
                         'decision': 'yes' if cited_by else None,
                         'note': 'already cited by the entry' if cited_by else None})
        rec['sources']['kdw'] = {'candidates': rows}

        rows = []
        for c in sg_hits.get(slug, []):
            ctx, hit = context_of(c['snippet'])
            row = {'locator': 't. %s, p. %d' % (_roman(c['vol']), c['page']),
                   'kind': c['kind'], 'head': c['head'], 'snippet': c['snippet'],
                   'context': ctx, 'context_hits': hit[:3]}
            if c['page'] in (sg_cited.get(slug) or set()) and c['kind'] == 'entry':
                row['decision'] = 'yes'
                row['note'] = 'already cited by the entry'
            rows.append(row)
        rec['sources']['sgkp'] = {'candidates': rows}

        rows = []
        for c in nm_hits.get(slug, []):
            ctx, hit = context_of(c['snippet'])
            rows.append({'locator': 't. %d, p. %d' % (c['tome'], c['page']),
                         'kind': c['kind'], 'head': c['head'], 'snippet': c['snippet'],
                         'context': ctx, 'context_hits': hit[:3]})
        rec['sources']['nmpol'] = {'candidates': rows}

        prev = previous.get(slug) or {}
        if not isinstance(prev, dict):
            prev = {}
        for src, pdata in rec['sources'].items():
            pprev = prev.get(src) or {}
            if not isinstance(pprev, dict):
                pprev = {}
            pprev = pprev.get('candidates') or []
            by_loc = {c.get('locator'): c for c in pprev if isinstance(c, dict)}
            for row in pdata['candidates']:
                old = by_loc.get(row['locator'])
                if not isinstance(old, dict):
                    continue
                oldd = old.get('decision')
                # a bare yes/no in an older log round-trips as True/False
                if oldd in (True, False):
                    oldd = 'yes' if oldd else 'no'
                if oldd and oldd != 'pending' and not row.get('cited_by') \
                        and row.get('note') != 'already cited by the entry':
                    row['decision'] = oldd
                    row['note'] = old.get('note')
        out[slug] = rec
    cache = _load_translations()
    for slug, rec in out.items():
        for src in rec['sources']:
            _attach_en(rec['sources'][src]['candidates'], cache)
    return out


_ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII',
          9: 'IX', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII', 14: 'XIV', 15: 'XV',
          16: 'XVI'}


def _roman(v):
    return _ROMAN.get(v, str(v))


_LOG_KEYS = ('locator', 'decision', 'kind', 'context', 'doc', 'cited_by', 'note')


def _log_row(row):
    parts = []
    for k in _LOG_KEYS:
        v = row.get(k)
        if v is None or v == '':
            continue
        if k == 'locator':
            parts.append('locator: "%s"' % v)
        elif k in ('decision', 'kind', 'context'):
            # quoted: YAML 1.1 reads a bare no as False and a bare yes as True
            parts.append('%s: "%s"' % (k, v))
        elif k == 'note':
            parts.append('note: "%s"' % str(v).replace('"', "'"))
        elif k == 'cited_by':
            parts.append('cited_by: [%s]' % ', '.join(v))
        elif k == 'doc':
            parts.append('doc: %s' % (v if isinstance(v, str) else 'kdw-%d' % v))
        else:
            parts.append('%s: %s' % (k, v))
    return '      - { %s }' % ', '.join(parts)


def write_log(places):
    """The committed record: locators, context, decisions; no snippet text.
    `places` is the yaml-shaped dict (slug -> source -> candidates)."""
    lines = ['# The match log of the gazetteer against the three Polish reference',
             '# works (docs/PLACE_NAME_DATABASES_PLAN.md, section 3). Made by',
             '# pipeline/gazetteer/match_sources.py; the decisions are the editor\'s,',
             '# recorded on the review page (review/place_name_sources/match_log.html,',
             '# not committed) and applied with --apply. Locators and decisions only:',
             '# the works\' texts, two of them in copyright, stay in Igor\'s',
             '# repository and in review/.',
             'places:']
    for slug in places:
        lines.append('  %s:' % slug)
        for src in ('kdw', 'sgkp', 'nmpol'):
            cands = ((places[slug].get(src) or {}).get('candidates')) or []
            lines.append('    %s:' % src)
            if not cands:
                lines.append('      candidates: []')
            else:
                lines.append('      candidates:')
                for row in cands:
                    lines.append(_log_row(row))
    with open(LOG, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('wrote', os.path.relpath(LOG, ROOT))


def to_log_shape(matches):
    places = {}
    for slug, rec in matches.items():
        srcs = {}
        for src in ('kdw', 'sgkp', 'nmpol'):
            srcs[src] = {'candidates': [
                {k: row[k] for k in _LOG_KEYS if row.get(k) is not None}
                for row in rec['sources'][src]['candidates']]}
        places[slug] = srcs
    return places


PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Match log — the gazetteer against the place-name databases</title>
<style>
:root { --ink:#1a1a1a; --mut:#6b6b6b; --line:#ddd; --bg:#fafaf8; --ok:#1a7f37; --no:#b42318; --un:#b58105; }
* { box-sizing:border-box }
body { margin:0; font:14px/1.45 Georgia,serif; color:var(--ink); background:var(--bg) }
header { position:sticky; top:0; z-index:5; background:#fff; border-bottom:1px solid var(--line); padding:10px 16px; display:flex; gap:14px; align-items:center; flex-wrap:wrap }
header h1 { font-size:16px; margin:0; margin-right:auto }
header input[type=search] { padding:5px 8px; width:220px; font:inherit }
button { font:inherit; padding:5px 12px; cursor:pointer; border:1px solid var(--line); background:#fff; border-radius:4px }
button.primary { background:#1a1a1a; color:#fff; border-color:#1a1a1a }
#counts { color:var(--mut) }
main { display:flex; align-items:flex-start }
nav { width:230px; flex:0 0 230px; position:sticky; top:56px; max-height:calc(100vh - 60px); overflow-y:auto; border-right:1px solid var(--line); background:#fff; padding:8px 0 }
nav a { display:flex; justify-content:space-between; padding:3px 12px; color:var(--ink); text-decoration:none; font-size:13px }
nav a:hover { background:#f0f0ec }
nav a.cur { background:#e8e8e2; font-weight:bold }
.dot { width:9px; height:9px; border-radius:50%; flex:0 0 9px; margin-top:4px }
.dot.done { background:var(--ok) } .dot.part { background:var(--un) } .dot.open { background:#ccc } .dot.zero { background:#fff; border:1px solid #ccc }
#pane { flex:1; padding:16px 22px; max-width:920px }
.card { background:#fff; border:1px solid var(--line); border-radius:6px; padding:14px 18px; margin-bottom:18px }
.card h2 { margin:0 0 2px; font-size:19px }
.meta { color:var(--mut); font-size:13px; margin:0 0 8px }
.src { margin-top:12px }
.src h3 { font-size:13px; margin:10px 0 6px; text-transform:uppercase; letter-spacing:.05em; color:var(--mut) }
.cand { border-top:1px solid var(--line); padding:8px 0 }
.cand .loc { font-weight:bold }
.loc a { color:#0b5394 }
.chip { display:inline-block; font:11px/1 sans-serif; padding:2px 6px; border-radius:8px; margin-left:6px; vertical-align:1px }
.chip.ok { background:#e3f2e1; color:var(--ok) } .chip.unknown { background:#fdf3d8; color:var(--un) } .chip.none { background:#eee; color:var(--mut) }
.chip.cited { background:#e3ecf7; color:#0b5394 } .chip.doc { background:#e8eaf6; color:#3949ab }
.snip { color:#333; font-size:13px; margin:4px 0 }
.snip.missing { color:var(--mut); font-style:italic }
details.orig { margin:2px 0 0 }
details.orig summary { cursor:pointer; color:var(--mut); font-size:12px; user-select:none }
details.orig .snip { color:var(--mut); font-size:12px }
.decide { display:flex; gap:10px; align-items:center; margin-top:4px; font-size:13px }
.decide label { cursor:pointer }
.decide input { accent-color:#1a1a1a }
.decide input[type=text] { flex:1; font:inherit; padding:3px 6px; border:1px solid var(--line); border-radius:4px }
.empty { color:var(--mut); font-style:italic }
#saved { color:var(--ok); display:none }
</style>
</head>
<body>
<header>
  <h1>Match log — the gazetteer against the three databases</h1>
  <input type="search" id="q" placeholder="find a place…">
  <label><input type="checkbox" id="openonly"> undecided first</label>
  <span id="counts"></span>
  <button class="primary" id="save">Save → match_decisions.json</button>
  <span id="saved">saved.</span>
</header>
<main>
<nav id="list"></nav>
<div id="pane"></div>
</main>
<script>
const DATA = __DATA__;
const ORDER = __ORDER__;
const state = JSON.parse(localStorage.getItem('matchlog') || '{}');
function get(p, s, i) { return ((state[p]||{})[s]||{})[i] || {} }
function set(p, s, i, k, v) {
  state[p] = state[p] || {}; state[p][s] = state[p][s] || {}; state[p][s][i] = state[p][s][i] || {};
  if (v === null) delete state[p][s][i][k]; else state[p][s][i][k] = v;
  localStorage.setItem('matchlog', JSON.stringify(state));
  counts(); renderList(); renderPane();
}
function dec(p, src, i, c) { return (c && c.decision) || get(p, src, i).decision }
function counts() {
  let total = 0, done = 0;
  for (const p of ORDER) {
    const rec = DATA[p];
    for (const src of ['kdw','sgkp','nmpol']) {
      (rec.sources[src].candidates||[]).forEach((c, i) => {
        total++;
        const d = dec(p, src, i, c);
        if (d === 'yes' || d === 'no') done++;
      });
    }
  }
  document.getElementById('counts').textContent = done + ' / ' + total + ' decided';
}
function dot(p) {
  const rec = DATA[p]; let open = 0, total = 0;
  for (const src of ['kdw','sgkp','nmpol']) {
    (rec.sources[src].candidates||[]).forEach((c, i) => {
      total++;
      const d = dec(p, src, i, c);
      if (d !== 'yes' && d !== 'no') open++;
    });
  }
  if (total === 0) return 'zero';
  return open === 0 ? 'done' : (open < total ? 'part' : 'open');
}
let cur = null;
function renderList() {
  const q = document.getElementById('q').value.toLowerCase();
  const openOnly = document.getElementById('openonly').checked;
  const nav = document.getElementById('list'); nav.innerHTML = '';
  for (const p of ORDER) {
    const rec = DATA[p];
    if (q && !p.includes(q) && !rec.heading.toLowerCase().includes(q)) continue;
    const d = dot(p);
    if (openOnly && (d === 'done' || d === 'zero')) continue;
    const a = document.createElement('a');
    a.href = '#' + p; a.dataset.slug = p;
    a.innerHTML = '<span>' + rec.heading + '</span><span class="dot ' + d + '"></span>';
    if (p === cur) a.classList.add('cur');
    a.onclick = (e) => { e.preventDefault(); cur = p; renderList(); renderPane(); };
    nav.appendChild(a);
  }
}
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;') }
function row(p, src, c, i) {
  const d = dec(p, src, i, c);
  const n = get(p, src, i).note || c.note || '';
  let chip = '', link = '';
  if (src === 'kdw') {
    chip = c.cited_by ? '<span class="chip cited">already cited: ' + esc(c.cited_by.join(', ')) + '</span>'
         : (c.doc ? '<span class="chip doc">in the edition: /documents/kdw/' + c.doc + '/</span>'
                  : '<span class="chip none">not in the edition</span>');
    link = c.doc ? ' <a href="/documents/kdw/' + c.doc + '/" target="_blank">open in the edition</a>' : '';
  } else {
    chip = c.context === 'ok' ? '<span class="chip ok">our ground: ' + esc((c.context_hits||[]).join(', ')) + '</span>'
         : c.context === 'unknown' ? '<span class="chip unknown">context unclear</span>'
         : '<span class="chip none">no area context</span>';
  }
  const orig = (c.head || '') + (c.snippet ? ' — ' + c.snippet : '');
  const enHead = c.en_head || '';
  const enSnip = c.en_snip || '';
  let snipHtml;
  if (enSnip) {
    snipHtml = '<div class="snip">' + esc(enSnip) + '</div>';
  } else if (enHead) {
    snipHtml = '<div class="snip">' + esc(enHead) + '</div>';
  } else {
    snipHtml = '<div class="snip missing">' + esc(c.head || '') + ' — [not yet translated]</div>';
  }
  return '<div class="cand">'
    + '<span class="loc">' + esc(c.locator) + '</span>'
    + (c.year ? ' <span style="color:var(--mut)">' + c.year + '</span>' : '')
    + (c.kind === 'mention' ? ' <span class="chip none">a mention, not the entry</span>' : '')
    + chip + link
    + snipHtml
    + (orig.trim() ? '<details class="orig"><summary>original</summary><div class="snip">' + esc(orig) + '</div></details>' : '')
    + '<div class="decide">'
    + '<label><input type="radio" data-k="decision" data-v="yes" ' + (d==='yes'?'checked':'') + '> yes</label>'
    + '<label><input type="radio" data-k="decision" data-v="no" ' + (d==='no'?'checked':'') + '> no</label>'
    + '<label><input type="radio" data-k="decision" data-v="unsure" ' + (d==='unsure'?'checked':'') + '> unsure</label>'
    + '<input type="text" value="' + esc(n) + '" placeholder="note…" data-k="note">'
    + '</div></div>';
}
function renderPane() {
  const pane = document.getElementById('pane');
  if (!cur || !DATA[cur]) { pane.innerHTML = '<div class="card"><p class="empty">Choose a place from the list.</p></div>'; return }
  const rec = DATA[cur];
  let h = '<div class="card"><h2>' + esc(rec.heading) + '</h2>'
    + '<p class="meta">' + esc(rec.kind_text) + (rec.location ? ' — ' + esc(rec.location) : '') + ' · '
    + (rec.status === 'historical' ? 'no longer exists' : 'exists') + '</p>'
    + '<p class="meta">Name forms searched: ' + esc((rec.forms||[]).join(' ; ')) + '</p>';
  for (const src of ['kdw','sgkp','nmpol']) {
    const cands = rec.sources[src].candidates || [];
    const label = src === 'kdw' ? 'Kodeks dyplomatyczny Wielkopolski' : src === 'sgkp' ? 'Słownik geograficzny Królestwa Polskiego' : 'Nazwy miejscowe Polski';
    h += '<div class="src"><h3>' + label + ' (' + cands.length + ')</h3>';
    if (!cands.length) h += '<p class="empty">No entry found for any form of the name.</p>';
    cands.forEach((c, i) => { h += row(cur, src, c, i); });
    h += '</div>';
  }
  h += '</div>';
  pane.innerHTML = h;
  pane.querySelectorAll('.decide input[type=radio]').forEach(inp => {
    inp.onchange = () => set(cur, inp.closest('.cand').dataset.src, +inp.closest('.cand').dataset.i, 'decision', inp.dataset.v);
  });
  pane.querySelectorAll('.decide input[type=text]').forEach(inp => {
    inp.onchange = () => set(cur, inp.closest('.cand').dataset.src, +inp.closest('.cand').dataset.i, 'note', inp.value || null);
  });
}
// tag each candidate row with its coordinates for the handlers
const _row = row;
row = function(p, src, c, i) { return _row(p, src, c, i).replace('<div class="cand">', '<div class="cand" data-src="' + src + '" data-i="' + i + '">') };
document.getElementById('save').onclick = () => {
  // keyed by locator, not index: a later rebuild must not misplace a decision
  const out = { saved: new Date().toISOString(), decisions: {} };
  for (const p of ORDER) {
    const rec = DATA[p];
    for (const src of ['kdw','sgkp','nmpol']) {
      (rec.sources[src].candidates||[]).forEach((c, i) => {
        if (c.truncated) return;
        const st = get(p, src, i);
        const d = c.decision || st.decision;
        const note = st.note || null;
        if (!d && !note) return;
        out.decisions[p] = out.decisions[p] || {};
        out.decisions[p][src] = out.decisions[p][src] || {};
        out.decisions[p][src][c.locator] = { decision: d || null, note: note };
      });
    }
  }
  const blob = new Blob([JSON.stringify(out, null, 1)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = 'match_decisions.json'; a.click();
  document.getElementById('saved').style.display = 'inline';
  setTimeout(() => document.getElementById('saved').style.display = 'none', 2000);
};
document.getElementById('q').oninput = renderList;
document.getElementById('openonly').onchange = renderList;
window.onkeydown = (e) => {
  if (e.target.tagName === 'INPUT') return;
  if (!cur) return;
  const i = ORDER.indexOf(cur);
  if (e.key === 'ArrowDown' && i < ORDER.length - 1) { cur = ORDER[i+1]; renderList(); renderPane(); e.preventDefault(); }
  if (e.key === 'ArrowUp' && i > 0) { cur = ORDER[i-1]; renderList(); renderPane(); e.preventDefault(); }
};
counts(); renderList(); renderPane();
</script>
</body>
</html>
"""


def write_page(matches):
    compact = {slug: {'heading': rec['heading'], 'kind_text': rec['kind_text'],
                      'location': rec['location'], 'status': rec['status'],
                      'forms': rec['forms'], 'sources': rec['sources']}
               for slug, rec in matches.items()}
    os.makedirs(REVIEW, exist_ok=True)
    data = json.dumps(compact, ensure_ascii=False)
    order = json.dumps(list(compact), ensure_ascii=False)
    html = PAGE_HEAD.replace('__DATA__', data).replace('__ORDER__', order)
    with open(os.path.join(REVIEW, 'match_log.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    with open(os.path.join(REVIEW, 'matches.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(compact, f, ensure_ascii=False, indent=1)
    print('wrote', os.path.relpath(os.path.join(REVIEW, 'match_log.html'), ROOT),
          'and matches.json')


def apply(path):
    """Merge the editor's downloaded decisions into source_matches.yml.
    The decisions are keyed by locator, so a later rebuild cannot misplace
    them."""
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    state = data.get('decisions') or {}
    with open(LOG, encoding='utf-8') as f:
        log = yaml.safe_load(f) or {}
    places = log.get('places') or {}
    n = 0
    for slug, srcs in state.items():
        for src, rows in (srcs or {}).items():
            cands = ((places.get(slug) or {}).get(src) or {}).get('candidates') or []
            by_loc = {c.get('locator'): c for c in cands}
            for loc, row in (rows or {}).items():
                cand = by_loc.get(loc)
                if cand is None:
                    print('  unmatched: %s / %s / %s' % (slug, src, loc))
                    continue
                changed = False
                if row.get('decision') and cand.get('decision') != row['decision']:
                    cand['decision'] = row['decision']
                    changed = True
                if row.get('note') and cand.get('note') != row['note']:
                    cand['note'] = row['note']
                    changed = True
                n += changed
    write_log(places)
    print('%d decision(s) applied.' % n)


def main():
    if '--apply' in sys.argv:
        apply(sys.argv[sys.argv.index('--apply') + 1])
        return
    matches = build()
    write_log(to_log_shape(matches))
    write_page(matches)
    n_k = sum(len(r['sources']['kdw']['candidates']) for r in matches.values())
    n_s = sum(len(r['sources']['sgkp']['candidates']) for r in matches.values())
    n_n = sum(len(r['sources']['nmpol']['candidates']) for r in matches.values())
    s_ok = sum(1 for r in matches.values() for c in r['sources']['sgkp']['candidates'] if c.get('context') == 'ok')
    n_ok = sum(1 for r in matches.values() for c in r['sources']['nmpol']['candidates'] if c.get('context') == 'ok')
    pre = sum(1 for r in matches.values() for c in r['sources']['kdw']['candidates'] if c.get('cited_by'))
    print('places: %d; candidates: kdw %d (%d already cited), sgkp %d (context ok %d), nmpol %d (context ok %d)'
          % (len(matches), n_k, pre, n_s, s_ok, n_n, n_ok))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
