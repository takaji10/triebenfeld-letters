# -*- coding: utf-8 -*-
"""
Generate the Jekyll site data from the canonical corpus database.

Reads  : corpus/documents/ via unitlib.load_documents() (themselves derived
         from the canonical .txt)
Writes : site/_letters/*.html          one page per record
         site/_data/*.yml              people, places, stats
         site/assets/search-index.json client-side search + filter index

The canonical corpus is never modified. This script is rerunnable at any time;
everything under site/_letters and site/assets/search-index.json is generated
output and should not be hand-edited. Translations live in site/_data/translations/
and are NOT touched here.

Fidelity: the diplomatic view is the corpus text with HTML-escaping as the only
transformation. verify() re-extracts it from the generated files and asserts a
character-exact round trip.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, json, re, csv, html, shutil, unicodedata
from collections import Counter, defaultdict
import unitlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNITS = unitlib.load_units()
SITE = os.path.join(ROOT, 'site')
LETTERS_DIR = os.path.join(SITE, '_letters')
DATA_DIR = os.path.join(SITE, '_data')
ASSETS_DIR = os.path.join(SITE, 'assets')

# ---------------------------------------------------------------- people
# The authorities and the matching both live in entities.py now, so this script
# and the dataset builder cannot drift apart on who a document names.
from entities import load_people, load_places, entities_in

PEOPLE_RE = [(slug, disp, rx) for slug, disp, rx in load_people()]
PEOPLE_DISPLAY = {slug: disp for slug, disp, _ in PEOPLE_RE}
PEOPLE = [(slug, disp, None) for slug, disp, _ in PEOPLE_RE]
PLACE_CANON = load_places()

MONTHS = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
          7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

SOURCE_LABEL = {
    'signature': 'read from the letter',
    'dateline':  "read from the document's own dateline",
    'supplied':  'supplied by the researcher',
    'inferred':  'inferred from neighbouring letters',
    'twin':      'taken from its duplicate (letter 48)',
    'none':      'no date in the source',
}


def slugify(s):
    s = s.lower()
    for a, b in (('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss'),('ą','a'),('ę','e'),
                 ('ł','l'),('ń','n'),('ó','o'),('ś','s'),('ź','z'),('ż','z'),('è','e')):
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


def date_label(r):
    if not r['date_iso']:
        return 'undated'
    y, m, d = r['year'], r['month'], r['day']
    if d:
        return f"{d} {MONTHS[m]} {y}"
    if m:
        return f"{MONTHS[m]} {y}"
    return str(y)


def reading_html(text, is_register):
    """
    Reading view: line-wrap hyphens resolved, lines flowed into paragraphs.
    Blank lines in the corpus are page breaks, so they delimit blocks.
    Presentational only - the diplomatic view remains canonical.
    """
    blocks = re.split(r'\n\s*\n', text)
    out = []
    for block in blocks:
        lines = [l for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        if is_register:
            # tabular: one entry per line, keep the line structure
            body = '<br>\n'.join(html.escape(l.strip()) for l in lines)
            out.append(f'<p>{body}</p>')
            continue
        buf = ''
        for line in lines:
            s = line.strip()
            if not buf:
                buf = s
            elif buf.endswith('¬'):
                # ¬ is unambiguously a word-continuation mark: join, drop it.
                buf = buf[:-1] + s
            elif re.search(r'\w-$', buf) and s[:1].islower():
                # A hyphen attached to a word with a lowercase continuation is a
                # line-wrap ("Ver-" + "mögen"): join and drop the hyphen.
                # Deliberately NOT applied when the next line starts uppercase -
                # those are ambiguous in this corpus between real compounds
                # ("Haupt-" + "Ersaz") and the writer's habitual dash, so they
                # are left exactly as written.
                buf = buf[:-1] + s
            else:
                buf += ' ' + s
        out.append('<p>' + html.escape(buf) + '</p>')
    return '\n'.join(out)


def diplomatic_html(text):
    """Exactly the corpus text, HTML-escaped. No other transformation."""
    return html.escape(text)


_DOC_LABELS = None


def doc_type_label(doc_type):
    """'certified_copy' -> 'Certified copy'.

    Read out of site/_data/i18n.yml so the label has one home: the site renders
    the German from the same file, and a kind added there needs no change here.
    Anything unlabelled falls back to the generic word rather than to 'Letter'.
    """
    global _DOC_LABELS
    if _DOC_LABELS is None:
        _DOC_LABELS = {}
        path = os.path.join(ROOT, 'site', '_data', 'i18n.yml')
        try:
            import yaml
            with open(path, encoding='utf-8') as f:
                _DOC_LABELS = yaml.safe_load(f).get('en', {}) or {}
        except Exception:
            _DOC_LABELS = {}
    label = _DOC_LABELS.get((doc_type or '').strip())
    if isinstance(label, str) and label:
        return label
    return _DOC_LABELS.get('document', 'Document')


def yaml_str(s):
    """Quote a scalar safely for YAML."""
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


def yaml_opt(s):
    """
    Optional scalar: empty becomes a real YAML null.

    This matters. Liquid treats the empty string as TRUTHY, so emitting "" for an
    absent value makes `{% if page.duplicate_of %}` fire on every page. Nulls are
    falsy, so absent fields behave the way the templates assume.
    """
    if s is None or str(s).strip() == '':
        return 'null'
    return yaml_str(s)


def load_scan_map():
    """(unit, letter_id, page) -> image filename, across every unit.

    The unit is part of the key because document numbers repeat between units:
    two holdings can both have a letter 48.
    """
    out = {}
    for u in UNITS:
        path = os.path.join(u.dir, 'page_scan_map.csv')
        if not os.path.isfile(path):
            print(f'  {u.slug}: no page_scan_map.csv - pages render without scans')
            continue
        with open(path, encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                if row['letter'] and row['page'] and row['image']:
                    out[(u.slug, row['letter'], int(row['page']))] = row['image']
    return out


def main():
    # The per-document files are the primary form; the merged array is derived
    # from them and kept only for readers outside this project.
    recs = unitlib.load_documents(ROOT)
    print(f'loaded {len(recs)} records')
    scans = load_scan_map()
    have = os.path.isdir(os.path.join(SITE, 'assets', 'scans'))
    print(f'scan mapping: {len(scans)} pages'
          + ('' if have else '  (derivatives not built yet - run make_scan_derivatives.py)'))

    # ---------- ordering ----------
    def archival_key(r):
        # An archival number only orders documents within its own holding, so
        # the unit comes first: unit A's 303 precedes unit B's 1.
        m = re.match(r'(\d+)([a-z]*)$', r['letter_id'])
        return (r['unit'], int(m.group(1)), m.group(2))

    def chrono_key(r):
        if not r['date_iso']:
            return (1, '9999', archival_key(r))
        return (0, r['date_iso'], archival_key(r))

    archival = sorted(recs, key=archival_key)
    chrono = sorted(recs, key=chrono_key)
    units_by_slug = {u.slug: u for u in UNITS}
    # duplicate_of is recorded in the unit's own rulings.yml, so it names an
    # archival number in the same holding - resolve it inside that unit.
    _url_by_uid = {r['uid']: r['permalink'] for r in recs}
    # parent_letter names a document number inside the same holding, so the
    # lookup has to be scoped by unit: two units both have a document 7.
    _by_unit_lid = {(r['unit'], r['letter_id']): r for r in recs}
    # Keyed by uid, not letter_id: document numbers repeat between units.
    arch_pos = {r['uid']: i for i, r in enumerate(archival)}
    chrono_pos = {r['uid']: i for i, r in enumerate(chrono)}

    # ---------- people / places ----------
    people_index = defaultdict(list)
    place_index = defaultdict(list)
    for r in recs:
        found = []
        for slug, disp, rx in PEOPLE_RE:
            if rx.search(r['text']):
                found.append(slug)
                people_index[slug].append(r['uid'])
        r['_people'] = found
        p = PLACE_CANON.get(r['place'], r['place'])
        # Letters that name no place of writing are grouped under "Unknown"
        # rather than dropped. Many of these genuinely never say where they were
        # written, and silently omitting them made the places list look complete
        # when a third of the corpus was missing from it.
        r['_place'] = p or 'Unknown'
        place_index[r['_place']].append(r['uid'])

    # ---------- write letter pages ----------
    if os.path.isdir(LETTERS_DIR):
        shutil.rmtree(LETTERS_DIR)
    os.makedirs(LETTERS_DIR)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for r in recs:
        lid = r['letter_id']
        is_reg = r['doc_type'] == 'register'
        a, c = arch_pos[r['uid']], chrono_pos[r['uid']]
        fm = []
        fm.append('---')
        fm.append('layout: letter')
        # The URL carries the archival unit and the document number, which
        # together are the citation key: /letters/oe1bu9454/48/. The filename
        # stays flat and padded so the collection sorts.
        fm.append(f'permalink: {yaml_str(r["permalink"])}')
        # The page names itself for what it is. Calling a purchase deed
        # "Letter 7" was harmless while the edition held only correspondence.
        fm.append(f'title: {yaml_str(doc_type_label(r["doc_type"]) + " " + lid)}')
        fm.append(f'letter_id: {yaml_str(lid)}')
        fm.append(f'unit: {yaml_str(r["unit"])}')
        fm.append(f'uid: {yaml_str(r["uid"])}')
        fm.append(f'pad: {yaml_str(r["pad"])}')
        fm.append(f'doc_type: {yaml_str(r["doc_type"])}')
        fm.append(f'seq_archival: {r["seq_archival"]}')
        fm.append(f'date_iso: {yaml_opt(r["date_iso"])}')
        fm.append(f'date_label: {yaml_str(date_label(r))}')
        fm.append(f'date_precision: {yaml_str(r["date_precision"])}')
        fm.append(f'date_source: {yaml_str(r["date_source"])}')
        fm.append(f'date_source_label: {yaml_opt(SOURCE_LABEL.get(r["date_source"], ""))}')
        # Only carry the basis when it says more than the source label already does.
        basis = r['date_inferred_from'] if r['date_source'] in ('inferred', 'none') else ''
        fm.append(f'date_basis: {yaml_opt(basis)}')
        fm.append(f'year: {r["year"] if r["year"] else "null"}')
        fm.append(f'place: {yaml_opt(r["_place"])}')
        fm.append(f'sender: {yaml_opt(r.get("sender", ""))}')
        fm.append(f'recipient: {yaml_opt(r.get("recipient", ""))}')
        fm.append(f'parent_letter: {yaml_opt(r["parent_letter"])}')
        # The parent's own kind, so an enclosure reads "part of contract 18"
        # rather than "part of letter 18" over a deed.
        _par = _by_unit_lid.get((r['unit'], r['parent_letter'])) if r['parent_letter'] else None
        fm.append(f'parent_doc_type: {yaml_opt(_par["doc_type"] if _par else "")}')
        fm.append(f'duplicate_of: {yaml_opt(r["duplicate_of"])}')
        fm.append(f'uncertainty_count: {r["uncertainty_count"]}')
        fm.append(f'has_damage: {"true" if r["has_damage"] else "false"}')
        fm.append(f'is_missing: {"true" if r["is_missing"] else "false"}')
        fm.append(f'n_lines: {r["n_lines"]}')
        fm.append(f'n_pages: {len(r.get("pages") or [])}')
        fm.append('people: [' + ', '.join(yaml_str(p) for p in r['_people']) + ']')
        fm.append('themes: []')
        fm.append(f'prev_archival: {yaml_opt(archival[a-1]["letter_id"]) if a > 0 else "null"}')
        fm.append(f'next_archival: {yaml_opt(archival[a+1]["letter_id"]) if a < len(archival)-1 else "null"}')
        fm.append(f'prev_chrono: {yaml_opt(chrono[c-1]["letter_id"]) if c > 0 else "null"}')
        fm.append(f'next_chrono: {yaml_opt(chrono[c+1]["letter_id"]) if c < len(chrono)-1 else "null"}')
        # A neighbour may sit in another unit once the corpus grows, so the
        # template is handed the URL rather than building one from the id.
        fm.append(f'prev_archival_url: {yaml_opt(archival[a-1]["permalink"]) if a > 0 else "null"}')
        fm.append(f'next_archival_url: {yaml_opt(archival[a+1]["permalink"]) if a < len(archival)-1 else "null"}')
        fm.append(f'prev_chrono_url: {yaml_opt(chrono[c-1]["permalink"]) if c > 0 else "null"}')
        fm.append(f'next_chrono_url: {yaml_opt(chrono[c+1]["permalink"]) if c < len(chrono)-1 else "null"}')
        # Typed links to other documents in the same holding. Rendered as
        # links, so a confirmation reaches the contract it confirms.
        _rels = [(_rel, _by_unit_lid.get((r['unit'], str(_rel.get('target', '')))))
                 for _rel in (r.get('relations') or [])]
        _rels = [(a, b) for a, b in _rels if b]
        if _rels:
            fm.append('relations:')
            for _rel, _t in _rels:
                fm.append(f'  - kind: {yaml_str(_rel.get("kind", ""))}')
                fm.append(f'    target: {yaml_str(_t["letter_id"])}')
                fm.append(f'    target_url: {yaml_str(_t["permalink"])}')
                fm.append(f'    target_title: {yaml_str(doc_type_label(_t["doc_type"]) + " " + _t["letter_id"])}')
                fm.append(f'    note: {yaml_str(_rel.get("note", ""))}')
        _dup = f"{r['unit']}-{r['duplicate_of']}" if r['duplicate_of'] else ''
        fm.append('duplicate_of_url: ' + (yaml_str(_url_by_uid[_dup])
                                         if _dup and _dup in _url_by_uid else 'null'))
        fm.append('---')

        # One block per manuscript page, so page breaks stay visible and each
        # page has somewhere for its scan to sit later.
        body = []
        pages = r.get('pages') or []
        for p in pages:
            body.append(f'<section class="ms-page" id="p{p["page"]}" '
                        f'data-page="{p["page"]}" '
                        f'data-lines="{p["line_start"]}-{p["line_end"]}">')
            if len(pages) > 1:
                body.append(
                    f'<div class="page-rule"><span class="page-no">Page {p["page"]}</span>'
                    f'<span class="page-lines">archival lines '
                    f'{p["line_start"]}-{p["line_end"]}</span></div>')
            # Two panes: the manuscript image on the left, its own text on the
            # right, so a page and its scan always sit together.
            img = scans.get((r['unit'], lid, p['page']), '')
            body.append('<div class="pane-pair">')
            body.append('<div class="pane-scan">')
            if img:
                body.append(
                    f'<a class="scan-link" href="{{{{ \'/assets/scans/{img}\' | relative_url }}}}" '
                    f'target="_blank" rel="noopener">'
                    f'<img class="scan" loading="lazy" '
                    f'src="{{{{ \'/assets/scans/{img}\' | relative_url }}}}" '
                    f'alt="Manuscript page {p["page"]} of letter {lid}">'
                    f'<span class="scan-cap">{html.escape(img)} '
                    f', open full size</span></a>')
            else:
                body.append('<p class="muted noscan">No scan matched to this page.</p>')
            body.append('</div>')

            body.append('<div class="pane-text">')
            # view 1 - the transcription: manuscript line breaks kept, line-end
            # marks resolved per the recorded decisions. Numbered to the
            # archival line so it can still be cited line by line.
            body.append('<div class="text-view" data-view="diplomatic">')
            body.append('<ol class="dip" start="' + str(p['line_start']) + '">')
            for ln in p.get('transcription', p['diplomatic']).split('\n'):
                body.append('<li>' + html.escape(ln) + '</li>')
            body.append('</ol></div>')
            # view 2 - reading
            body.append('<div class="text-view" data-view="reading" hidden>')
            if is_reg:
                body.append('<p>' + '<br>\n'.join(
                    html.escape(x.strip()) for x in p['reading'].split('\n') if x.strip()) + '</p>')
            else:
                # One <p> per paragraph. The first carries `runs-on` where the
                # paragraph began on the previous page: the text never crosses a
                # page break, so it would otherwise look like a fresh paragraph
                # every time a page turns. The style drops the indent there.
                paras = p.get('paragraphs') or [p['reading']]
                for _i, _para in enumerate(paras):
                    if not _para.strip():
                        continue
                    _cls = ' class="runs-on"' if (_i == 0
                                                  and p.get('continues_previous')) else ''
                    body.append(f'<p{_cls}>' + html.escape(_para) + '</p>')
            body.append('</div>')
            # view 3 - translation, filled in from _data/translations later
            body.append(f'<div class="text-view" data-view="translation" hidden '
                        f'data-seg="{p["page"]}"></div>')
            body.append('</div>')     # .pane-text
            body.append('</div>')     # .pane-pair
            body.append('</section>')
        with open(os.path.join(LETTERS_DIR, r['pad'] + '.html'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    print(f'wrote {len(recs)} pages to site/_letters/')

    # Documents published before the URLs carried their archival unit keep
    # working: a unit flagged legacy_flat_urls gets a stub at the old address
    # that forwards to the new one. Only the first unit needs this, and only
    # while those links are still in circulation.
    redir_dir = os.path.join(SITE, 'redirects')
    for fn in os.listdir(redir_dir) if os.path.isdir(redir_dir) else []:
        os.remove(os.path.join(redir_dir, fn))
    stubs = [r for r in recs
             if units_by_slug.get(r['unit'], {}).get('legacy_flat_urls')
             and r['permalink'] != '/letters/' + r['letter_id'] + '/']
    if stubs:
        os.makedirs(redir_dir, exist_ok=True)
        for r in stubs:
            old_url = '/letters/' + r['letter_id'] + '/'
            with open(os.path.join(redir_dir, r['pad'] + '.html'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('---\n')
                f.write('permalink: ' + yaml_str(old_url) + '\n')
                f.write('sitemap: false\n')
                f.write('---\n')
                f.write('<link rel="canonical" href="{{ ' + repr(r['permalink'])
                        + " | relative_url }}\">\n")
                f.write('<meta http-equiv="refresh" content="0; url={{ '
                        + repr(r['permalink']) + ' | relative_url }}">\n')
                f.write('<p>This document has moved to '
                        '<a href="{{ ' + repr(r['permalink']) + ' | relative_url }}">'
                        + r['permalink'] + '</a>.</p>\n')
    print(f'wrote {len(stubs)} redirect stubs for pre-namespace URLs')

    # ---------- data files ----------
    # One row per archival unit, so the reader can see where a document came
    # from and the browse page can filter by holding.
    with open(os.path.join(DATA_DIR, 'units.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        for u in UNITS:
            n = sum(1 for r in recs if r['unit'] == u.slug)
            if not n:
                continue
            pages = sum(r['n_pages'] for r in recs if r['unit'] == u.slug)
            dated = [r['date_iso'] for r in recs if r['unit'] == u.slug and r['date_iso']]
            f.write(f'- slug: {yaml_str(u.slug)}\n')
            f.write(f'  ref: {yaml_str(u["ref"])}\n')
            f.write(f'  archive: {yaml_str(u.get("archive", ""))}\n')
            f.write(f'  title: {yaml_str((u.get("title") or "").strip())}\n')
            f.write(f'  description: {yaml_str((u.get("description") or "").strip())}\n')
            f.write(f'  count: {n}\n')
            f.write(f'  pages: {pages}\n')
            f.write(f'  first: {yaml_str(min(dated) if dated else "")}\n')
            f.write(f'  last: {yaml_str(max(dated) if dated else "")}\n')

    # Keyed by uid: the indexes above collect uids, because an archival number
    # is only unique inside its own holding.
    url_by_uid = {r['uid']: r['permalink'] for r in recs}
    label_by_uid = {r['uid']: r['letter_id'] for r in recs}
    with open(os.path.join(DATA_DIR, 'people.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        for slug, disp, _ in PEOPLE:
            ids = people_index.get(slug, [])
            if not ids:
                continue
            f.write(f'- slug: {yaml_str(slug)}\n')
            f.write(f'  name: {yaml_str(disp)}\n')
            f.write(f'  count: {len(ids)}\n')
            f.write('  letters: ['
                    + ', '.join('{id: %s, url: %s}'
                                % (yaml_str(label_by_uid[i]), yaml_str(url_by_uid[i]))
                                for i in ids) + ']\n')

    with open(os.path.join(DATA_DIR, 'places.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        # "Unknown" sorts last rather than alphabetically among the real places.
        for place in sorted(place_index, key=lambda p: (p == 'Unknown', p)):
            ids = place_index[place]
            f.write(f'- name: {yaml_str(place)}\n')
            f.write(f'  slug: {yaml_str(slugify(place))}\n')
            f.write(f'  count: {len(ids)}\n')
            f.write('  letters: ['
                    + ', '.join('{id: %s, url: %s}'
                                % (yaml_str(label_by_uid[i]), yaml_str(url_by_uid[i]))
                                for i in ids) + ']\n')

    years = Counter(r['date_iso'][:4] for r in recs if r['date_iso'])
    with open(os.path.join(DATA_DIR, 'stats.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        f.write(f'total: {len(recs)}\n')
        f.write(f'letters: {sum(1 for r in recs if r["doc_type"] == "letter")}\n')
        f.write(f'undated: {sum(1 for r in recs if not r["date_iso"])}\n')
        f.write(f'people: {len([s for s in people_index if people_index[s]])}\n')
        f.write(f'places: {len(place_index)}\n')
        f.write('years:\n')
        for y in sorted(years):
            f.write(f'  - year: {y}\n    count: {years[y]}\n')

    # ---------- search / filter index ----------
    # Summaries are a finding aid written from the English translations by
    # summarise.py. They live in site/_data/summaries.yml, are not generated
    # here, and are simply carried into the index so the browse list can show
    # them without a second fetch. Absent file, absent key: the list falls back
    # to a text snippet exactly as before.
    summaries, summaries_de = {}, {}
    import yaml as _yaml
    for fn, into in (('summaries.yml', 'en'), ('summaries_de.yml', 'de')):
        sp = os.path.join(DATA_DIR, fn)
        if os.path.isfile(sp):
            loaded = _yaml.safe_load(open(sp, encoding='utf-8')) or {}
            if into == 'en':
                summaries = loaded
            else:
                summaries_de = loaded

    index = []
    for r in recs:
        index.append({
            'id': r['letter_id'],
            'uid': r['uid'],
            'unit': r['unit'],
            'url': r['permalink'],
            'pad': r['pad'],
            'date': r['date_iso'],
            'label': date_label(r),
            'year': r['date_iso'][:4] if r['date_iso'] else '',
            'place': r['_place'],
            'people': r['_people'],
            'themes': [],
            'precision': r['date_precision'],
            'source': r['date_source'],
            'damage': bool(r['has_damage']),
            'unc': r['uncertainty_count'],
            'dup': r['duplicate_of'],
            'parent': r['parent_letter'],
            'type': r['doc_type'],
            'n': r['n_lines'],
            'from': r.get('sender', ''),
            'to': r.get('recipient', ''),
            'summary': summaries.get(r['pad'], ''),
            'summary_de': summaries_de.get(r['pad'], ''),
            # normalised text for search: hyphens resolved so wrapped words are findable
            'text': re.sub(r'\s+', ' ', r['text'].replace('¬\n', '').replace('¬', '')),
        })
    with open(os.path.join(ASSETS_DIR, 'search-index.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))
    size = os.path.getsize(os.path.join(ASSETS_DIR, 'search-index.json'))
    print(f'wrote search index ({size/1024:.0f} KB)')

    verify(recs)


def verify(recs):
    """
    Round-trip every archival line out of the generated pages.

    The diplomatic view is rendered as one <li> per manuscript line, so pulling
    those back out must reproduce the corpus's non-blank lines exactly, in order.
    """
    print('\n--- verification ---')
    # Keyed by uid, not letter_id: an archival number is unique only inside its
    # own holding, so two units both having a document 7 would collide here and
    # this check would silently compare one against the other's text.
    by_uid = {r['uid']: r for r in recs}
    checked = mismatch = 0
    total_pages = 0
    for fn in os.listdir(LETTERS_DIR):
        with open(os.path.join(LETTERS_DIR, fn), encoding='utf-8') as f:
            content = f.read()
        uid = re.search(r'^uid: "(.+?)"$', content, re.M).group(1)
        # The diplomatic view is one <li> per manuscript line, inside
        # <ol class="dip">. Scope the extraction to those lists: the page also
        # carries other <li> - the typed relations to other documents - and a
        # bare <li> match would read them back as if they were transcription.
        recovered = [html.unescape(x)
                     for blk in re.findall(r'<ol class="dip"[^>]*>(.*?)</ol>', content, re.S)
                     for x in re.findall(r'<li>(.*?)</li>', blk, re.S)]
        # The rendered view is the transcription layer, which build_db.py has
        # already proven differs from the archival text only where a recorded
        # decision says so.
        expected = [l for p in by_uid[uid]['pages']
                    for l in p.get('transcription', p['diplomatic']).split('\n')
                    if l.strip()]
        total_pages += len(re.findall(r'<section class="ms-page"', content))
        if recovered != expected:
            mismatch += 1
            print(f'  MISMATCH {uid}: {len(recovered)} lines vs {len(expected)}')
        checked += 1
    print(f'letter pages checked    : {checked}')
    print(f'manuscript pages        : {total_pages}')
    print(f'archival lines exact    : {mismatch == 0}')
    assert checked == len(recs), f'page count {checked} != record count {len(recs)}'
    assert mismatch == 0, 'archival text was altered - refusing to continue'
    print('VERIFIED: every archival line reproduced character-for-character')


if __name__ == '__main__':
    main()
