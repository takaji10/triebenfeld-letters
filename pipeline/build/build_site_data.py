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
from entities import load_people, load_places, entities_in, place_authority

PEOPLE_RE = [(slug, disp, rx) for slug, disp, rx in load_people()]
PEOPLE_DISPLAY = {slug: disp for slug, disp, _ in PEOPLE_RE}
PEOPLE = [(slug, disp, None) for slug, disp, _ in PEOPLE_RE]
PLACE_CANON = load_places()
# The places a document NAMES, which for a grant or a mortgage-book report is
# the question worth asking: the dateline gives the chancery, not the estate.
PLACES_RE = place_authority()
PLACE_DISP = {slug: disp for slug, disp, _ in PLACES_RE}
# The place of writing takes the same Polish (German) label as the lists.
PLACE_LABEL = unitlib.load_place_labels()
# The English name of a place of writing where English has its own (Vienna,
# Warsaw): the register's `render`. German pages keep the register's label.
PLACE_RENDER = {unitlib.place_label(e): e['render']
                for e in (unitlib.load_places_authority().get('places') or {}).values()
                if e.get('render')}

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


def _reference(name):
    import yaml as _yaml
    p = os.path.join(ROOT, 'reference', name)
    return (_yaml.safe_load(open(p, encoding='utf-8')) or {}) if os.path.exists(p) else {}


# Short biographies (reference/people_bios.yml, keyed by the person's slug) and
# map coordinates (reference/places_osm.yml, keyed by the name the site prints).
# Both are written by hand and optional: a person or place without an entry
# simply shows without one.
BIOS = _reference('people_bios.yml')
OSM = _reference('places_osm.yml')


def life_de(s):
    """'b. c. 1760 (estimated), d. 1816' -> 'geb. ca. 1760 (geschätzt), gest. 1816'."""
    for en, de in (('documented', 'belegt'), ('(estimated)', '(geschätzt)'),
                   ('d. by ', 'gest. spätestens '), ('b. ', 'geb. '), ('d. ', 'gest. '),
                   ('c. ', 'ca. ')):
        s = s.replace(en, de)
    return s


def osm_lines(name):
    v = OSM.get(name)
    return f'  lat: {v["lat"]}\n  lon: {v["lon"]}\n' if v else ''


def slugify(s):
    s = s.lower()
    for a, b in (('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss'),('ą','a'),('ę','e'),
                 ('ł','l'),('ń','n'),('ó','o'),('ś','s'),('ź','z'),('ż','z'),('è','e')):
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


def date_label(r, lang='en'):
    if not r['date_iso']:
        return 'undatiert' if lang == 'de' else 'undated'
    y, m, d = r['year'], r['month'], r['day']
    if lang == 'de':
        if d:
            return f"{d}. {MONTHS_DE[m]} {y}"
        return f"{MONTHS_DE[m]} {y}" if m else str(y)
    if d:
        return f"{d} {MONTHS[m]} {y}"
    if m:
        return f"{MONTHS[m]} {y}"
    return str(y)


# The German view of a document page. The page is shared between the two
# languages, so it carries both and i18n.js shows the one asked for.
MONTHS_DE = {1:'Januar',2:'Februar',3:'März',4:'April',5:'Mai',6:'Juni',
             7:'Juli',8:'August',9:'September',10:'Oktober',11:'November',12:'Dezember'}
SOURCE_LABEL_DE = {
    'signature': 'aus dem Brief gelesen',
    'dateline':  'aus der Datumszeile des Dokuments gelesen',
    'supplied':  'vom Bearbeiter ergänzt',
    'inferred':  'aus benachbarten Briefen erschlossen',
    'twin':      'aus dem Duplikat übernommen (Brief 48)',
    'none':      'kein Datum in der Quelle',
}
_NOTES_DE = None


def note_de(s):
    """German for a short English note, from reference/site_notes_de.yml; '' if none."""
    global _NOTES_DE
    if _NOTES_DE is None:
        import yaml as _yaml
        p = os.path.join(ROOT, 'reference', 'site_notes_de.yml')
        _NOTES_DE = (_yaml.safe_load(open(p, encoding='utf-8')) or {}) if os.path.exists(p) else {}
    return _NOTES_DE.get((s or '').strip(), '')


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


# Shared with publish_translations.py, which renders the English table.
render_table = unitlib.render_table

# How a block the page sets apart opens, by kind (corpus_pages.SET_APART). The
# label is English here and swapped by the language switch through data-i18n.
SET_APART_OPEN = {
    'sideways': '<div class="sideways"><div class="sideways-note" data-i18n="sideways">'
                'Written sideways on the page</div>',
    'office': '<div class="sideways office-note"><div class="sideways-note" '
              'data-i18n="office_note">Written by the receiving office</div>',
}


def yaml_str(s):
    """Quote a scalar safely for YAML."""
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


_CORR = None
_CORR_MISSING = set()


def correspondent(raw, lang='en', full=True):
    """How a recorded sender or recipient is shown (reference/correspondents.yml).

    full: "name, title", for the document header; otherwise the name alone, for
    the lists. A form with no entry is shown as it stands, and reported once.
    """
    global _CORR
    if not raw:
        return ''
    if _CORR is None:
        import yaml as _yaml
        p = os.path.join(ROOT, 'reference', 'correspondents.yml')
        _CORR = (_yaml.safe_load(open(p, encoding='utf-8')) or {}) if os.path.exists(p) else {}
    e = _CORR.get(raw)
    if not e:
        if raw not in _CORR_MISSING:
            _CORR_MISSING.add(raw)
            print(f'  correspondent not in reference/correspondents.yml: {raw!r}')
        return raw
    name = e.get('name_' + lang) or e.get('name_en') or raw
    title = e.get('title_' + lang) or ''
    return f'{name}, {title}' if full and title else name


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

    Reads it out of the records rather than out of page_scan_map.csv, because
    build_db now resolves the pairing when it builds the page. This used to be
    a second, independent read of the same file, which is how the site could
    show a scan the dataset knew nothing about.
    """
    out = {}
    for r in unitlib.load_documents(ROOT):
        for p in r.get('pages') or []:
            if p.get('scan'):
                out[(r['unit'], r['letter_id'], p['page'])] = p['scan']
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
    # Documents the editor has laid out as tables, keyed (unit, letter_id).
    tables = {(u.slug, lid): t for u in UNITS for lid, t in unitlib.load_tables(u).items()}
    # duplicate_of is recorded in the unit's own rulings.yml, so it names an
    # archival number in the same holding - resolve it inside that unit.
    _url_by_uid = {r['uid']: r['permalink'] for r in recs}
    # parent_letter names a document number inside the same holding, so the
    # lookup has to be scoped by unit: two units both have a document 7.
    _by_unit_lid = {(r['unit'], r['letter_id']): r for r in recs}
    # A document's previous and next stay inside its own holding (editor,
    # 2026-10-03): a reader browsing one holding expects to stay in it, so each
    # order is kept per unit. Keyed by uid: document numbers repeat between units.
    arch_unit, chrono_unit = defaultdict(list), defaultdict(list)
    for r in archival:
        arch_unit[r['unit']].append(r)
    for r in chrono:
        chrono_unit[r['unit']].append(r)
    arch_pos = {r['uid']: i for lst in arch_unit.values() for i, r in enumerate(lst)}
    chrono_pos = {r['uid']: i for lst in chrono_unit.values() for i, r in enumerate(lst)}

    # ---------- people / places ----------
    people_index = defaultdict(list)
    place_index = defaultdict(list)
    named_index = defaultdict(list)
    estate_index = defaultdict(list)
    for r in recs:
        # The shared matcher, so a pattern limited to some documents (a king
        # named only as "Wir Friedrich Wilhelm") is limited here too.
        found = entities_in(r, PEOPLE_RE)
        for slug in found:
            people_index[slug].append(r['uid'])
        r['_people'] = found
        p = PLACE_CANON.get(r['place'], r['place'])
        _lab = PLACE_LABEL.get((p or '').strip().lower())
        if not _lab and p:
            # a dateline form the authority does not list verbatim
            # (Frankfurth a.d. Oder): the place whose pattern it opens with
            _lab = next((disp for _s, disp, rx in PLACES_RE if rx.match(p)), None)
        p = _lab or p
        # Letters that name no place of writing are grouped under "Unknown"
        # rather than dropped. Many of these genuinely never say where they were
        # written, and silently omitting them made the places list look complete
        # when a third of the corpus was missing from it.
        r['_place'] = p or 'Unknown'
        place_index[r['_place']].append(r['uid'])
        named = []
        for slug, disp, rx in PLACES_RE:
            if rx.search(r['text']):
                named.append(slug)
                named_index[slug].append(r['uid'])
        r['_places_named'] = named
        r['_estates'] = r.get('estates') or []
        for slug in r['_estates']:
            estate_index[slug].append(r['uid'])

    # ---------- write letter pages ----------
    if os.path.isdir(LETTERS_DIR):
        shutil.rmtree(LETTERS_DIR)
    os.makedirs(LETTERS_DIR)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for r in recs:
        lid = r['letter_id']
        is_reg = r['doc_type'] == 'register'
        tbl = tables.get((r['unit'], lid))
        a, c = arch_pos[r['uid']], chrono_pos[r['uid']]
        arch_l, chrono_l = arch_unit[r['unit']], chrono_unit[r['unit']]
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
        fm.append(f'date_label_de: {yaml_str(date_label(r, "de"))}')
        fm.append(f'date_precision: {yaml_str(r["date_precision"])}')
        fm.append(f'date_source: {yaml_str(r["date_source"])}')
        fm.append(f'date_source_label: {yaml_opt(SOURCE_LABEL.get(r["date_source"], ""))}')
        # Only carry the basis when it says more than the source label already does.
        basis = r['date_inferred_from'] if r['date_source'] in ('inferred', 'none') else ''
        fm.append(f'date_basis: {yaml_opt(basis)}')
        fm.append(f'date_source_label_de: {yaml_opt(SOURCE_LABEL_DE.get(r["date_source"], ""))}')
        fm.append(f'date_basis_de: {yaml_opt(note_de(basis))}')
        fm.append(f'year: {r["year"] if r["year"] else "null"}')
        fm.append(f'place: {yaml_opt(PLACE_RENDER.get(r["_place"], r["_place"]))}')
        fm.append(f'place_de: {yaml_opt("Unbekannt" if r["_place"] == "Unknown" else r["_place"])}')
        fm.append(f'sender: {yaml_opt(correspondent(r.get("sender", "")))}')
        fm.append(f'sender_de: {yaml_opt(correspondent(r.get("sender", ""), "de"))}')
        fm.append(f'recipient: {yaml_opt(correspondent(r.get("recipient", "")))}')
        fm.append(f'recipient_de: {yaml_opt(correspondent(r.get("recipient", ""), "de"))}')
        fm.append(f'parent_letter: {yaml_opt(r["parent_letter"])}')
        # The parent's own kind, so an enclosure reads "part of contract 18"
        # rather than "part of letter 18" over a deed.
        _par = _by_unit_lid.get((r['unit'], r['parent_letter'])) if r['parent_letter'] else None
        fm.append(f'parent_doc_type: {yaml_opt(_par["doc_type"] if _par else "")}')
        fm.append(f'duplicate_of: {yaml_opt(r["duplicate_of"])}')
        fm.append(f'uncertainty_count: {r["uncertainty_count"]}')
        fm.append(f'has_damage: {"true" if r["has_damage"] else "false"}')
        fm.append(f'rough_transcription: {"true" if r.get("rough_transcription") else "false"}')
        fm.append(f'is_missing: {"true" if r["is_missing"] else "false"}')
        fm.append(f'n_lines: {r["n_lines"]}')
        # The document's own line range, numbered from 1. The layout asked
        # for page.line_start and the front matter never carried it, so every
        # document read "archival lines 1-" with nothing after the dash:
        # Liquid's nil | plus: 1 is 1, and nil renders as empty.
        pgs = r.get('pages') or []
        if pgs:
            fm.append(f'line_first: {pgs[0]["doc_line_start"]}')
            fm.append(f'line_last: {pgs[-1]["doc_line_end"]}')
        fm.append(f'n_pages: {len(r.get("pages") or [])}')
        fm.append('people: [' + ', '.join(yaml_str(p) for p in r['_people']) + ']')
        fm.append('places_named: ['
                  + ', '.join(yaml_str(p) for p in r['_places_named']) + ']')
        fm.append('estates: ['
                  + ', '.join(yaml_str(p) for p in r['_estates']) + ']')
        fm.append('themes: [' + ', '.join(yaml_str(t) for t in (r.get('themes') or [])) + ']')
        fm.append(f'era: {yaml_str(r.get("era") or "")}')
        fm.append(f'prev_archival: {yaml_opt(arch_l[a-1]["letter_id"]) if a > 0 else "null"}')
        fm.append(f'next_archival: {yaml_opt(arch_l[a+1]["letter_id"]) if a < len(arch_l)-1 else "null"}')
        fm.append(f'prev_chrono: {yaml_opt(chrono_l[c-1]["letter_id"]) if c > 0 else "null"}')
        fm.append(f'next_chrono: {yaml_opt(chrono_l[c+1]["letter_id"]) if c < len(chrono_l)-1 else "null"}')
        # The template is handed the URL rather than building one from the id.
        fm.append(f'prev_archival_url: {yaml_opt(arch_l[a-1]["permalink"]) if a > 0 else "null"}')
        fm.append(f'next_archival_url: {yaml_opt(arch_l[a+1]["permalink"]) if a < len(arch_l)-1 else "null"}')
        fm.append(f'prev_chrono_url: {yaml_opt(chrono_l[c-1]["permalink"]) if c > 0 else "null"}')
        fm.append(f'next_chrono_url: {yaml_opt(chrono_l[c+1]["permalink"]) if c < len(chrono_l)-1 else "null"}')
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
                fm.append(f'    target_type: {yaml_str(_t["doc_type"])}')
                fm.append(f'    note_de: {yaml_str(note_de(_rel.get("note", "")))}')
        _dup = f"{r['unit']}-{r['duplicate_of']}" if r['duplicate_of'] else ''
        fm.append('duplicate_of_url: ' + (yaml_str(_url_by_uid[_dup])
                                         if _dup and _dup in _url_by_uid else 'null'))
        fm.append('---')

        # One block per manuscript page, so page breaks stay visible and each
        # page has somewhere for its scan to sit later.
        body = []
        pages = r.get('pages') or []
        for p in pages:
            # A tabulated document's transcription is its table: each page shows
            # the table's rows for that page, in every text view, and is cited
            # by entry number rather than by the lines of a text export.
            _table = render_table(tbl, p['page']) if tbl else ''
            _entries = [row[0].strip() for row in tbl['pages'].get(p['page'], [])] if _table else []
            body.append(f'<section class="ms-page" id="p{p["page"]}" '
                        f'data-page="{p["page"]}" '
                        f'data-lines="{p["doc_line_start"]}-{p["doc_line_end"]}">')
            if len(pages) > 1:
                _where = (f'entries {_entries[0]}-{_entries[-1]}' if _entries else
                          f'lines {p["doc_line_start"]}-{p["doc_line_end"]}')
                body.append(
                    f'<div class="page-rule"><span class="page-no">Page {p["page"]}</span>'
                    f'<span class="page-lines">{_where}</span></div>')
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
            if _table:
                body.append(_table)
            else:
                # Numbered from 1 in each document, contiguously. The unit-absolute
                # line is internal and is not published; corpus/index/ carries the
                # mapping for anyone who needs to resolve a citation.
                # Text written sideways on the page gets a list of its own under
                # a label, so it does not read as if it ran on in order. The
                # numbering carries straight through; the lists stay
                # <ol class="dip"> so verify_site reads every line back.
                # Text the receiving office wrote on the letter is set apart
                # the same way, under its own label.
                side = set(p.get('sideways_lines') or [])
                office = set(p.get('office_lines') or [])
                if p.get('by_paragraph'):
                    body.append('<div class="sideways-note" data-i18n="by_paragraph">'
                                'Transcribed by paragraph, not line by line: each '
                                'numbered entry is a paragraph of the manuscript.</div>')
                _lines = p.get('transcription', p['diplomatic']).split('\n')
                _run = None
                for k, ln in enumerate(_lines):
                    _kind = 'sideways' if k in side else 'office' if k in office else False
                    if _kind != _run:
                        if _run is not None:
                            body.append('</ol>' + ('</div>' if _run else ''))
                        _run = _kind
                        if _run:
                            body.append(SET_APART_OPEN[_run])
                        body.append('<ol class="dip" start="' + str(p['doc_line_start'] + k) + '">')
                    body.append('<li>' + html.escape(ln) + '</li>')
                body.append('</ol>' + ('</div>' if _run else ''))
            body.append('</div>')
            # view 2 - reading
            body.append('<div class="text-view" data-view="reading" hidden>')
            if _table:
                body.append(_table)
            elif is_reg:
                body.append('<p>' + '<br>\n'.join(
                    html.escape(x.strip()) for x in p['reading'].split('\n') if x.strip()) + '</p>')
            else:
                # One <p> per paragraph. The first carries `runs-on` where the
                # paragraph began on the previous page: the text never crosses a
                # page break, so it would otherwise look like a fresh paragraph
                # every time a page turns. The style drops the indent there.
                paras = p.get('paragraphs') or [p['reading']]
                side = set(p.get('sideways_paragraphs') or [])
                office = set(p.get('office_paragraphs') or [])
                for _i, _para in enumerate(paras):
                    if not _para.strip():
                        continue
                    _cls = ' class="runs-on"' if (_i == 0
                                                  and p.get('continues_previous')) else ''
                    if _i in side or _i in office:
                        body.append(SET_APART_OPEN['sideways' if _i in side else 'office']
                                    + '<p>' + html.escape(_para) + '</p></div>')
                    else:
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

    # Every address a document has ever had keeps working.
    #
    # There are two legacy shapes now, not one. `/letters/<n>/` predates the
    # archival namespace and only the first unit ever had those. `/letters/
    # <unit>/<n>/` is what every document was published at until the move to
    # /documents/, so every unit needs that one.
    #
    # The stub FILENAMES carry the shape. They were keyed on the pad alone,
    # which is fine for one shape and silently destroys half the redirects the
    # moment there are two - same filename, second write wins, and the build
    # reports a healthy count either way.
    redir_dir = os.path.join(SITE, 'redirects')
    for fn in os.listdir(redir_dir) if os.path.isdir(redir_dir) else []:
        os.remove(os.path.join(redir_dir, fn))

    def legacy_urls(r):
        """Addresses this document used to live at, newest first."""
        out = [('ns', '/letters/' + r['unit'] + '/' + r['letter_id'] + '/')]
        if units_by_slug.get(r['unit'], {}).get('legacy_flat_urls'):
            out.append(('flat', '/letters/' + r['letter_id'] + '/'))
        return [(tag, u) for tag, u in out if u != r['permalink']]

    stubs = [(r, tag, old) for r in recs for tag, old in legacy_urls(r)]
    if stubs:
        os.makedirs(redir_dir, exist_ok=True)
        for r, tag, old_url in stubs:
            name = r['pad'] + '-' + tag + '.html'
            with open(os.path.join(redir_dir, name), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('---\n')
                f.write('permalink: ' + yaml_str(old_url) + '\n')
                f.write('sitemap: false\n')
                f.write('---\n')
                f.write('<link rel="canonical" href="{{ ' + repr(r['permalink'])
                        + ' | relative_url }}">\n')
                f.write('<meta http-equiv="refresh" content="0; url={{ '
                        + repr(r['permalink']) + ' | relative_url }}">\n')
                f.write('<p>This document has moved to '
                        '<a href="{{ ' + repr(r['permalink']) + ' | relative_url }}">'
                        + r['permalink'] + '</a>.</p>\n')
    n_ns = sum(1 for _, t, _ in stubs if t == 'ns')
    print(f'wrote {len(stubs)} redirect stubs '
          f'({n_ns} namespaced, {len(stubs) - n_ns} pre-namespace)')

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
            # German where a holding has it, empty where it does not. The
            # sources page printed the English description on /de/quellen/ with
            # nothing to mark it, which reads as a translation that happens to
            # be in the wrong language rather than one not yet made.
            f.write(f'  title_de: {yaml_str((u.get("title_de") or "").strip())}\n')
            f.write(f'  description_de: {yaml_str((u.get("description_de") or "").strip())}\n')
            f.write(f'  repository: {yaml_str(u.get("repository") or "")}\n')
            f.write(f'  era: {yaml_str(u.get("era") or "")}\n')
            f.write(f'  count: {n}\n')
            f.write(f'  pages: {pages}\n')
            f.write(f'  first: {yaml_str(min(dated) if dated else "")}\n')
            f.write(f'  last: {yaml_str(max(dated) if dated else "")}\n')
            # The span the Sources page shows is the holding's own, from
            # unit.yml: the documents' datelines fall short of it wherever a
            # file is not yet divided (I. HA GR, Rep. 7 C, Nr. 3709 is one
            # placeholder document of 1800 in a file kept to 1802) or its later
            # pieces are not documents of the edition. The datelines are the
            # fallback for a holding that gives none.
            span = str(u.get('date_span') or '').strip()
            if not span or span.upper() == 'TODO':
                yrs = sorted({d[:4] for d in dated})
                span = '-'.join(dict.fromkeys([yrs[0], yrs[-1]])) if yrs else ''
            span = span.replace('-', '\u2013')
            f.write(f'  span: {yaml_str(span)}\n')

    # A page for each holding: its description, its documents, how it was
    # prepared. The texts are hand-written and live with the holding.
    import unit_pages
    unit_pages.write(UNITS, recs, SITE, ROOT, yaml_str)

    # The reader's glossary: which words to mark in each document, and the
    # entries for the glossary page. Sets r['_gl'] for the search index below.
    import glossary_build
    glossary_build.write(glossary_build.load(ROOT), recs, ROOT, SITE, ASSETS_DIR, yaml_str)

    # Keyed by uid: the indexes above collect uids, because an archival number
    # is only unique inside its own holding.
    url_by_uid ={r['uid']: r['permalink'] for r in recs}
    label_by_uid = {r['uid']: r['letter_id'] for r in recs}
    _date_by_uid = {r['uid']: r['date_iso'] for r in recs}
    with open(os.path.join(DATA_DIR, 'people.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        for slug, disp, _ in PEOPLE:
            ids = people_index.get(slug, [])
            if not ids:
                continue
            f.write(f'- slug: {yaml_str(slug)}\n')
            f.write(f'  name: {yaml_str(disp)}\n')
            f.write(f'  count: {len(ids)}\n')
            # Who this is, in two or three sentences, and when they lived.
            _b = dict(BIOS.get(slug) or {})
            # No dates known: say in which years the documents name them.
            _yrs = sorted(_date_by_uid[i][:4] for i in ids if _date_by_uid.get(i))
            if not _b.get('life') and _yrs:
                _span = _yrs[0] if _yrs[0] == _yrs[-1] else _yrs[0] + '-' + _yrs[-1]
                _b['life'] = 'documented ' + _span
            if _b.get('life') and not _b.get('life_de'):
                _b['life_de'] = life_de(_b['life'])
            for _k in ('life', 'life_de', 'bio', 'bio_de'):
                if _b.get(_k):
                    f.write(f'  {_k}: {yaml_str(" ".join(str(_b[_k]).split()))}\n')
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
            f.write(osm_lines(place))
            f.write('  letters: ['
                    + ', '.join('{id: %s, url: %s}'
                                % (yaml_str(label_by_uid[i]), yaml_str(url_by_uid[i]))
                                for i in ids) + ']\n')

    # Kept in its own file rather than folded into places.yml: that one answers
    # "written here", this one "named here", and a place can score high on one
    # and not appear in the other at all. Summing them would state a number
    # that is true of neither question.
    with open(os.path.join(DATA_DIR, 'places_named.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        for slug in sorted(named_index,
                           key=lambda s: (-len(named_index[s]),
                                          PLACE_DISP.get(s, s))):
            ids = named_index[slug]
            f.write(f'- slug: {yaml_str(slug)}\n')
            f.write(f'  name: {yaml_str(PLACE_DISP.get(slug, slug))}\n')
            f.write(f'  count: {len(ids)}\n')
            f.write(osm_lines(PLACE_DISP.get(slug, slug)))
            f.write('  letters: ['
                    + ', '.join('{id: %s, url: %s}'
                                % (yaml_str(label_by_uid[i]), yaml_str(url_by_uid[i]))
                                for i in ids) + ']\n')

    with open(os.path.join(DATA_DIR, 'estates.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        for slug in sorted(estate_index,
                           key=lambda s: (-len(estate_index[s]),
                                          PLACE_DISP.get(s, s))):
            ids = estate_index[slug]
            f.write(f'- slug: {yaml_str(slug)}\n')
            f.write(f'  name: {yaml_str(PLACE_DISP.get(slug, slug))}\n')
            f.write(f'  count: {len(ids)}\n')
            f.write(osm_lines(PLACE_DISP.get(slug, slug)))
            f.write('  letters: ['
                    + ', '.join('{id: %s, url: %s}'
                                % (yaml_str(label_by_uid[i]), yaml_str(url_by_uid[i]))
                                for i in ids) + ']\n')

    # ---------- eras and themes ----------
    # The vocabularies are authored in reference/; the COUNTS AND SPANS are
    # computed here, every time, from the documents actually assigned. That is
    # the whole point: an era's dates are a fact about its contents, so adding a
    # holding corrects them instead of leaving a hand-typed range to rot.
    # reference/eras.yml states no date at all.
    for fname, key, vocab in (('eras.yml', 'era', unitlib.load_eras()),
                              ('themes.yml', 'themes', unitlib.load_themes())):
        rows = []
        for slug, e in sorted(vocab.items(), key=lambda kv: kv[1].get('order', 99)):
            if key == 'era':
                mine = [r for r in recs if (r.get('era') or '') == slug]
            else:
                mine = [r for r in recs if slug in (r.get('themes') or [])]
            yrs = sorted(r['date_iso'][:4] for r in mine if r.get('date_iso'))
            rows.append((slug, e, mine, yrs))
        with open(os.path.join(DATA_DIR, fname), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# Generated by build_site_data.py - do not hand-edit.\n')
            f.write('# Labels and blurbs come from reference/%s; counts and spans\n' % fname)
            f.write('# are computed from the documents assigned to each.\n')
            for slug, e, mine, yrs in rows:
                f.write('- slug: %s\n' % yaml_str(slug))
                f.write('  order: %d\n' % e.get('order', 99))
                f.write('  status: %s\n' % yaml_str(e.get('status') or 'draft'))
                f.write('  count: %d\n' % len(mine))
                f.write('  first: %s\n' % yaml_str(yrs[0] if yrs else ''))
                f.write('  last: %s\n' % yaml_str(yrs[-1] if yrs else ''))
                for k in ('label_en', 'label_de', 'blurb_en', 'blurb_de',
                          'ownership_en', 'ownership_de'):
                    if e.get(k):
                        f.write('  %s: %s\n' % (k, yaml_str(' '.join(str(e[k]).split()))))

    years = Counter(r['date_iso'][:4] for r in recs if r['date_iso'])
    with open(os.path.join(DATA_DIR, 'stats.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by build_site_data.py - do not hand-edit.\n')
        f.write(f'total: {len(recs)}\n')
        f.write(f'letters: {sum(1 for r in recs if r["doc_type"] == "letter")}\n')
        f.write(f'undated: {sum(1 for r in recs if not r["date_iso"])}\n')
        f.write(f'people: {len([s for s in people_index if people_index[s]])}\n')
        f.write(f'places: {len(place_index)}\n')
        f.write(f'places_named: {len(named_index)}\n')
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
            'label_de': date_label(r, 'de'),
            'year': r['date_iso'][:4] if r['date_iso'] else '',
            'place': r['_place'],
            'people': r['_people'],
            'themes': r.get('themes') or [],
            'era': r.get('era') or '',
            'precision': r['date_precision'],
            'source': r['date_source'],
            'damage': bool(r['has_damage']),
            'unc': r['uncertainty_count'],
            'dup': r['duplicate_of'],
            'parent': r['parent_letter'],
            'type': r['doc_type'],
            'n': r['n_lines'],
            'from': correspondent(r.get('sender', ''), 'en', False),
            'to': correspondent(r.get('recipient', ''), 'en', False),
            'from_de': correspondent(r.get('sender', ''), 'de', False),
            'to_de': correspondent(r.get('recipient', ''), 'de', False),
            'summary': summaries.get(r['pad'], ''),
            'summary_de': summaries_de.get(r['pad'], ''),
            # glossary entries found in the document: /documents/?term=<id>
            'gl': r.get('_gl') or [],
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
    A document transcribed as a table is checked cell by cell instead.
    """
    print('\n--- verification ---')
    _tables = {(u.slug, lid): t for u in UNITS for lid, t in unitlib.load_tables(u).items()}
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
        total_pages += len(re.findall(r'<section class="ms-page"', content))
        checked += 1
        # A tabulated document's transcription is its table: check it against
        # the corpus cell by cell, since each of its lines is a table row.
        _rec = by_uid[uid]
        _tbl = _tables.get((_rec['unit'], _rec['letter_id']))
        if _tbl:
            if unitlib.table_rows_in_page(content) != unitlib.table_expected_rows(_tbl):
                mismatch += 1
                print(f'  MISMATCH {uid}: table differs from the corpus')
            continue
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
        if recovered != expected:
            mismatch += 1
            print(f'  MISMATCH {uid}: {len(recovered)} lines vs {len(expected)}')
    print(f'letter pages checked    : {checked}')
    print(f'manuscript pages        : {total_pages}')
    print(f'archival lines exact    : {mismatch == 0}')
    assert checked == len(recs), f'page count {checked} != record count {len(recs)}'
    assert mismatch == 0, 'archival text was altered - refusing to continue'
    print('VERIFIED: every archival line reproduced character-for-character')


if __name__ == '__main__':
    main()
