# -*- coding: utf-8 -*-
"""The reader's glossary: where each entry falls in each document.

Called from build_site_data.py. Reads reference/glossary.yml (hand-written)
and writes, all generated:

  site/_data/glossary.yml        the entries, with the documents each is found
                                 in, for the glossary page
  site/_data/glossary_hits.json  per document: which word to mark, in which
                                 view, on which manuscript page
  site/assets/glossary.json      the definitions, fetched once by the document
                                 pages' script and cached
  review/glossary_matches.csv    every marked word with its line, to read for
                                 false hits before publishing

The German in the built pages is not touched: the page's script wraps the words
when it opens, so verify_site.py's character-exact check is unaffected.

Rules (docs/GLOSSARY_PLAN.md): the first hit of an entry on a manuscript page
is marked, once per view; not a word split across lines, nor one under a [?]
doubt mark. Views: `dip` (transcription, line by line), `rd` (reading text),
`en` (the English, per page), and the summaries `sen` and `sde`.
"""
import os, re, csv, json, html
import yaml

FIELDS = ('kind', 'lang', 'head_en', 'head_de', 'orig', 'short_en', 'short_de')


def _patterns(v):
    if not v:
        return []
    return [re.compile(x) for x in ([v] if isinstance(v, str) else v)]


def load(root):
    with open(os.path.join(root, 'reference', 'glossary.yml'), encoding='utf-8') as f:
        g = yaml.safe_load(f) or {}
    entries = g.get('entries') or []
    for e in entries:
        e['_de'] = _patterns(e.get('match_de'))
        e['_en'] = _patterns(e.get('match_en'))
    return entries


def _first(pats, text):
    """The earliest acceptable hit of any pattern: (start, end) or None."""
    best = None
    for rx in pats:
        for m in rx.finditer(text):
            s, t = (m.span('w') if 'w' in rx.groupindex and m.group('w') else m.span())
            after = text[t:t + 4]
            # a doubtful reading, or a word broken at the line end, is not marked
            if (after.startswith('[?]') or after.startswith('¬') or after.startswith('-')
                    or text[s:t].strip() != text[s:t]):
                continue
            if best is None or s < best[0]:
                best = (s, t)
            break
    return best


def _line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def compute(entries, recs, site_dir):
    """Hits per document, keyed by pad: [[view, page, surface, id], ...]."""
    data_dir = os.path.join(site_dir, '_data')
    summ = {}
    for fn, key in (('summaries.yml', 'sen'), ('summaries_de.yml', 'sde')):
        p = os.path.join(data_dir, fn)
        summ[key] = (yaml.safe_load(open(p, encoding='utf-8')) or {}) if os.path.exists(p) else {}

    hits, review = {}, []
    for r in recs:
        pad = r['pad']
        tr = {}
        tp = os.path.join(data_dir, 'translations', pad + '.yml')
        if os.path.exists(tp):
            t = yaml.safe_load(open(tp, encoding='utf-8')) or {}
            tr = {str(s.get('page')): s.get('en') or '' for s in t.get('segments') or []}
        out = []

        def mark(view, page, text, pats, e, where):
            if not pats or not text:
                return
            if e.get('per') == 'document' and any(h[0] == view and h[3] == e['id'] for h in out):
                return
            if view == 'dip':
                # line by line: a hit may not cross a manuscript line
                for i, line in enumerate(text.split('\n')):
                    b = _first(pats, line)
                    if b:
                        out.append([view, page, line[b[0]:b[1]], e['id']])
                        review.append([r['uid'], view, page, f'line {where + i}', e['id'], line[b[0]:b[1]], line.strip()[:160]])
                        return
                return
            b = _first(pats, text)
            if b:
                s = text[b[0]:b[1]]
                out.append([view, page, s, e['id']])
                ctx = text[max(0, b[0] - 60):b[1] + 60].replace('\n', ' ')
                review.append([r['uid'], view, page, f'line {_line_of(text, b[0])}', e['id'], s, ctx])

        for e in entries:
            for p in r.get('pages') or []:
                n = p['page']
                if e.get('per') == 'document':
                    # once in the document per view: skip a view already marked
                    done = {h[0] for h in out if h[3] == e['id']}
                    if {'dip', 'rd', 'en'} <= done:
                        break
                mark('dip', n, p.get('transcription') or p.get('diplomatic') or '', e['_de'], e, p.get('doc_line_start') or 1)
                mark('rd', n, p.get('reading') or '', e['_de'], e, 0)
                mark('en', n, tr.get(str(n), ''), e['_en'], e, 0)
            mark('sen', 0, summ['sen'].get(pad, ''), e['_en'], e, 0)
            mark('sde', 0, summ['sde'].get(pad, ''), e['_de'], e, 0)
        if out:
            hits[pad] = out
        r['_gl'] = sorted({h[3] for h in out})
    return hits, review


def _sort_key(head):
    """Sort and file a headword by its first letter, ignoring quotation marks
    and accents: Łukom under L, "I remain until death" under I."""
    import unicodedata
    h = head.strip().lstrip('"\'„“‘').replace('Ł', 'L').replace('ł', 'l')
    h = ''.join(c for c in unicodedata.normalize('NFD', h) if not unicodedata.combining(c))
    return h.lower(), (h[:1].upper() if h[:1].isalpha() else '#')


def source_html(source):
    """The `source:` line for the glossary page. A path into reference/ is
    dropped; "s.v. Entry (https://...)" becomes a link on the entry name."""
    s = re.sub(r' \(reference/[^)]*\)', '', (source or '').strip())
    out, last = [], 0
    for m in re.finditer(r'(s\.v\. )([^();]+?) \((https?://[^)\s]+)\)', s):
        out.append(html.escape(s[last:m.start()]) + html.escape(m.group(1))
                   + f'<a href="{html.escape(m.group(3))}">{html.escape(m.group(2))}</a>')
        last = m.end()
    return ''.join(out) + html.escape(s[last:])


def write(entries, recs, root, site_dir, assets_dir, yaml_str):
    hits, review = compute(entries, recs, site_dir)

    with open(os.path.join(site_dir, '_data', 'glossary_hits.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(hits, f, ensure_ascii=False, separators=(',', ':'))

    defs = {e['id']: {k: (e.get(k) or '').strip() for k in FIELDS} for e in entries}
    with open(os.path.join(assets_dir, 'glossary.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(defs, f, ensure_ascii=False, separators=(',', ':'))

    docs = {}
    for r in recs:
        for i in r.get('_gl') or []:
            docs.setdefault(i, []).append(r['uid'])
    with open(os.path.join(site_dir, '_data', 'glossary.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py from reference/glossary.yml - do not hand-edit.\n')
        for e in entries:
            f.write(f'- id: {yaml_str(e["id"])}\n')
            for k in FIELDS + ('long_en', 'long_de', 'source', 'check_against'):
                f.write(f'  {k}: {yaml_str((e.get(k) or "").strip())}\n')
            f.write(f'  source_html: {yaml_str(source_html(e.get("source")))}\n')
            f.write(f'  checked: {"true" if e.get("checked") else "false"}\n')
            for L in ('en', 'de'):
                key, initial = _sort_key(e.get('head_' + L) or e['id'])
                f.write(f'  sort_{L}: {yaml_str(key)}\n  initial_{L}: {yaml_str(initial)}\n')
            f.write(f'  docs: {len(docs.get(e["id"], []))}\n')

    rdir = os.path.join(root, 'review')
    os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, 'glossary_matches.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['uid', 'view', 'page', 'where', 'entry', 'marked', 'context'])
        w.writerows(review)

    print(f'glossary: {len(entries)} entries, {sum(len(v) for v in hits.values())} marks '
          f'in {len(hits)} documents; {sum(1 for e in entries if not docs.get(e["id"]))} entries found nowhere')
