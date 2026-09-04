# -*- coding: utf-8 -*-
"""
Generate the Jekyll site data from the canonical corpus database.

Reads  : letters.json (the database, itself derived from the canonical .txt)
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
UNIT = unitlib.one_unit(unitlib.unit_arg())
SITE = os.path.join(ROOT, 'site')
LETTERS_DIR = os.path.join(SITE, '_letters')
DATA_DIR = os.path.join(SITE, '_data')
ASSETS_DIR = os.path.join(SITE, 'assets')

# ---------------------------------------------------------------- people
# Canonical names from whos_who.md. Each entry: (slug, display, regex).
# The regex matches inflected/adjectival forms (Prusimskische, Hawichs, ...)
# but is anchored at a word start so it can't match inside another word.
PEOPLE = [
    # political / military / court
    ('metternich',     'Metternich',        r'Metternich'),
    ('talleyrand',     'Talleyrand',        r'Talleyrand'),
    ('scharnhorst',    'Scharnhorst',       r'Scharnhorst'),
    ('koeckritz',      'Köckritz',          r'Köckritz'),
    ('staegemann',     'Stägemann',         r'Stägemann'),
    ('kircheisen',     'Kircheisen',        r'Kircheisen'),
    ('voss',           'Voss',              r'Voss'),
    ('winzingerode',   'Winzingerode',      r'Winzingerode'),
    ('massenbach',     'Massenbach',        r'Massenbach'),
    ('hoym',           'Hoym',              r'H[oö]ym'),
    ('sacken',         'Sacken (Sakken)',   r'Sakken'),
    ('zastrow',        'Zastrow',           r'Zastrow'),
    ('humboldt',       'Wilhelm von Humboldt', r'Humboldt'),
    ('nesselrode',     'Nesselrode',        r'Nesselrode'),
    ('napoleon',       'Napoleon',          r'Napoleon'),
    # A surname AND an occupation: L303's register has "der Gärtner Nickel"
    # (the gardener) beside "der Sattler Hennig". The index cannot separate
    # them, so the display name says which one is meant.
    ('gaertner',       'Gärtner (Geh. Rath)', r'Gärtner'),
    # estate / legal / household
    ('hawich',         'Hawich',            r'Hawich'),
    ('honrichs',       'Honrichs',          r'Honrichs'),
    ('hecker',         'Hecker',            r'Hecker'),
    ('glenck',         'Glenck',            r'Glenck'),
    ('cosmar',         'Cosmar',            r'Cosmar'),
    ('stoessel',       'Stössel',           r'Stössel'),
    ('weigel',         'Weigel',            r'Weigel'),
    ('wedel',          'Wedel',             r'Wedel'),
    ('rapacki',        'Rapacki',           r'Rapacki'),
    ('kwilecki',       'Kwilecki',          r'Kwileck'),
    ('niedzewiecki',   'Niedzewiecki',      r'Niedzew'),
    # One woman under four surnames across the correspondence: born Prusimska,
    # married Dąbska (used 1807-1811), then remarried - the letters write that
    # second husband's name as Moscinska/Moszynska, which is the WRITERS' own
    # error for Miączyńska, not a transcription slip. Letter 266 hedges openly
    # ("Dąbska oder Moscinska"), and letter 285 states the chain: "der Tochter
    # des Prussiemski, jezt verehelichte Miączyńska".
    #
    # The pattern requires a feminine -a ending, which keeps two things out:
    # the adjectival `Prusimskische(n)` (the family and its estates, not her -
    # father and daughter are established as different people), and `Moszynski`,
    # the husband.
    ('prusimska',      'Michalina Prusimska (Dąbska / Miączyńska / Moscinska)',
     r'(?:Pru[sz]+ie?msk|D[ąa]m?bsk|Mosci[nń]sk|Moszy[nń]sk|Moscy[nń]sk|'
     r'Mi[ąa]czy[nń]sk)a(?![a-zà-ÿ])'),
    # Her father Antoni and the family estates. Kept separate deliberately.
    ('prusimski',      'Prusimski family (Trąbczyn estates)',
     r'Pru[sz]+ie?msk(?:i|isch\w*)(?![a-zà-ÿ])'),
    ('schlabrendorff', 'Schlabrendorff',    r'Schlabrendorff'),
    ('barbe',          'Barbe',             r'Barbe'),
    ('schenck',        'Schenck',           r'Schenck'),
    ('lahr',           'von der Lahr',      r'L[aä]hr'),
    ('bernhardi',      'Bergrath Bernhardi', r'Bernhardi'),
    ('bernhard',       'Meyer Bernhard',    r'Bernhard(?!i)'),
    ('pochammer',      'Pochammer',         r'Pochamm?er'),
    ('lombardini',     'Lombardini',        r'Lombardin'),
    ('eysenhardt',     'Eysenhardt',        r'Eysenhardt'),
    ('reinhardt',      'Reinhardt',         r'Reinhardt'),
    ('michaelis',      'Michaelis',         r'Michaelis'),
    ('otocki',         'Otocki',            r'Otocki'),
    ('kunckel',        'Kunckel',           r'Kunckel'),
    ('goeschel',       'Göschel',           r'Göschel'),
    ('graevenitz',     'Grävenitz',         r'Grävenitz'),
    ('knobelsdorff',   'Knobelsdorff',      r'Knobelsdorff'),
    ('sobottendorff',  'Sobottendorff',     r'Sobottendorff'),
    ('bornstaedt',     'Bornstädt',         r'Bornstädt'),
    ('goldbeck',       'Goldbeck',          r'Goldbeck'),
    ('falkenhausen',   'Falkenhausen',      r'Falkenhausen'),
    # Corpus spelling is Pourtales (the writer never used the accent); the
    # display name gives the family's proper form. `Portalis` survives once, at
    # line 18917, inside the writer's own note "Pourtales (nicht Portalis)" -
    # matched here so that mention still indexes to the right man.
    ('pourtales',      'Pourtalès (Pourtales)', r'Pourtal|Portalis'),
    ('schulenburg',    'Schulenburg',       r'Schul[ee]mburg|Schulenburg'),
    ('chomanowski',    'Chomanowski',       r'Chomanowski'),
    ('przespolewski',  'Przespolewski',     r'Przespolewski'),
    ('asch',           'Asch',              r'Asch\b'),
    ('hache',          'Hache',             r'Hache'),
    ('zerboni',        'Zerboni',           r'Zerboni'),
    ('broniewski',     'Broniewski',        r'Broniew|Bronisz'),
    # principals
    ('triebenfeld',    'v. Triebenfeld',    r'Triebenfeld'),
    ('hohenlohe',      'Hohenlohe',         r'Hohenlohe'),
]
def _auto_people():
    """Names vetted by name_catalogue.py that the curated list above misses.

    The hand list had 55 entries and matched 54 of the 807 tokens sitting in
    person position - Grotowski (x15), Brzechsta (x29), Hardenberg (x24) and
    many more were absent, so they were never highlighted anywhere. The curated
    entries stay authoritative: they carry display names, merged identities
    (Michalina Prusimska's four surnames) and distinctions the statistics cannot
    see (Hawich vs Honrichs). This only fills the long tail.
    """
    path = os.path.join(ROOT, 'reference', 'name_seeds.json')
    if not os.path.isfile(path):
        return []
    covered = set()
    for _, _, pat in PEOPLE:
        try:
            rx = re.compile(pat, re.UNICODE)
        except re.error:
            continue
        covered.add(rx)
    out = []
    for e in json.load(open(path, encoding='utf-8')):
        if e['kind'] != 'person' or e['count'] < 2:
            continue
        name = e['name']
        if any(rx.search(name) for rx in covered):
            continue
        # slugify() is defined further down the file, so slug locally
        slug = re.sub(r'[^a-z0-9]+', '-',
                      unicodedata.normalize('NFKD', name.lower())
                      .encode('ascii', 'ignore').decode()).strip('-')
        if not slug:
            continue
        # match the name plus German inflection, anchored at a word start
        out.append((slug, name,
                    re.escape(name) + r'(?:s|n|en|es|sche\w*|ische\w*)?'))
    return out


PEOPLE = PEOPLE + _auto_people()

# Colon abbreviations. These writers routinely shorten a familiar name to its
# first syllable and a colon: "Min: v. Hard:", "Gen Lieut v. Koch:", "der Gr.
# Pourt:". Matching only the full spelling silently loses those mentions - nine
# letters discuss Hardenberg and never once write his name out, which left him
# indexed in 31 letters instead of 40.
#
# Only abbreviations verified in context are listed. Deliberately absent:
#   Ant:  is "Antwort", not Anton
#   Kur:  is "Curländische", not a person
#   Ko:   reads as Koschentin, the estate, not Köckritz. L2's "In der Ko:
#         Geschichte" is followed by Pourtalès wanting to buy, which settles it
#   Sch:  could be Schlabrendorff, Schenck or Schimmelpfennig
#   B:    could be Barbe, Beyme or Brzechsta
# A wrong expansion here would invent a mention that is not in the letter,
# which is worse than missing one.
NAME_ABBREV = {
    'hardenberg': r'Hard(?:enb)?:',
    'koeckritz':  r'K[oö]ch:',
    'amelang':    r'Am(?:el)?:',
    'pourtales':  r'Pourt:',
    'graevenitz': r'Grev:',
    'lombardini': r'Lomb:',
    # Both instances are title-anchored ("der Fürstin Sa:", "Die Fürsten Sa:")
    # and Sacken is the only Fürstin S- in the corpus. Requiring the title is
    # what makes this safe; a bare 'Sa:' would not be.
    'sacken':     r'F(?:ü|ue)rst(?:in|en)\s+Sa:',
}

PEOPLE_RE = [(slug, disp,
              re.compile(r'(?<![A-Za-zÀ-ÿ])(?:' + pat
                         + (('|' + NAME_ABBREV[slug]) if slug in NAME_ABBREV else '')
                         + r')', re.UNICODE))
             for slug, disp, pat in PEOPLE]
PEOPLE_DISPLAY = {slug: disp for slug, disp, _ in PEOPLE}

# Place spellings that are the same place.
PLACE_CANON = {
    'posen': 'Posen', 'Posen': 'Posen',
    'Zagorowa': 'Zagorowo', 'Zagorowo': 'Zagorowo',
}

MONTHS = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
          7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

SOURCE_LABEL = {
    'signature': 'read from the letter',
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
    """(letter_id, page) -> image filename, from the reviewed page/scan mapping."""
    path = os.path.join(UNIT.dir, 'page_scan_map.csv')
    out = {}
    if not os.path.isfile(path):
        print('  no page_scan_map.csv - pages will render without scans')
        return out
    with open(path, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            if row['letter'] and row['page'] and row['image']:
                out[(row['letter'], int(row['page']))] = row['image']
    return out


def main():
    with open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8') as f:
        recs = json.load(f)
    print(f'loaded {len(recs)} records')
    scans = load_scan_map()
    have = os.path.isdir(os.path.join(SITE, 'assets', 'scans'))
    print(f'scan mapping: {len(scans)} pages'
          + ('' if have else '  (derivatives not built yet - run make_scan_derivatives.py)'))

    # ---------- ordering ----------
    def archival_key(r):
        m = re.match(r'(\d+)([a-z]*)$', r['letter_id'])
        return (int(m.group(1)), m.group(2))

    def chrono_key(r):
        if not r['date_iso']:
            return (1, '9999', archival_key(r))
        return (0, r['date_iso'], archival_key(r))

    archival = sorted(recs, key=archival_key)
    chrono = sorted(recs, key=chrono_key)
    units_by_slug = {u.slug: u for u in unitlib.load_units()}
    _url_by_id = {r['letter_id']: r['permalink'] for r in recs}
    arch_pos = {r['letter_id']: i for i, r in enumerate(archival)}
    chrono_pos = {r['letter_id']: i for i, r in enumerate(chrono)}

    # ---------- people / places ----------
    people_index = defaultdict(list)
    place_index = defaultdict(list)
    for r in recs:
        found = []
        for slug, disp, rx in PEOPLE_RE:
            if rx.search(r['text']):
                found.append(slug)
                people_index[slug].append(r['letter_id'])
        r['_people'] = found
        p = PLACE_CANON.get(r['place'], r['place'])
        # Letters that name no place of writing are grouped under "Unknown"
        # rather than dropped. Many of these genuinely never say where they were
        # written, and silently omitting them made the places list look complete
        # when a third of the corpus was missing from it.
        r['_place'] = p or 'Unknown'
        place_index[r['_place']].append(r['letter_id'])

    # ---------- write letter pages ----------
    if os.path.isdir(LETTERS_DIR):
        shutil.rmtree(LETTERS_DIR)
    os.makedirs(LETTERS_DIR)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for r in recs:
        lid = r['letter_id']
        is_reg = r['doc_type'] == 'register'
        a, c = arch_pos[lid], chrono_pos[lid]
        fm = []
        fm.append('---')
        fm.append('layout: letter')
        # The URL carries the archival unit and the document number, which
        # together are the citation key: /letters/oe1bu9454/48/. The filename
        # stays flat and padded so the collection sorts.
        fm.append(f'permalink: {yaml_str(r["permalink"])}')
        fm.append(f'title: {yaml_str("Letter " + lid)}')
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
        _dup = r['duplicate_of']
        fm.append('duplicate_of_url: ' + (yaml_str(_url_by_id[_dup])
                                         if _dup and _dup in _url_by_id else 'null'))
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
            img = scans.get((lid, p['page']), '')
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
                body.append('<p>' + html.escape(p['reading']) + '</p>')
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
    url_by_id = {r['letter_id']: r['permalink'] for r in recs}
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
                                % (yaml_str(i), yaml_str(url_by_id[i]))
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
                                % (yaml_str(i), yaml_str(url_by_id[i]))
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
    by_id = {r['letter_id']: r for r in recs}
    checked = mismatch = 0
    total_pages = 0
    for fn in os.listdir(LETTERS_DIR):
        with open(os.path.join(LETTERS_DIR, fn), encoding='utf-8') as f:
            content = f.read()
        lid = re.search(r'^letter_id: "(.+?)"$', content, re.M).group(1)
        recovered = [html.unescape(x) for x in
                     re.findall(r'<li>(.*?)</li>', content, re.S)]
        # The rendered view is the transcription layer, which build_db.py has
        # already proven differs from the archival text only where a recorded
        # decision says so.
        expected = [l for p in by_id[lid]['pages']
                    for l in p.get('transcription', p['diplomatic']).split('\n')
                    if l.strip()]
        total_pages += len(re.findall(r'<section class="ms-page"', content))
        if recovered != expected:
            mismatch += 1
            print(f'  MISMATCH letter {lid}: {len(recovered)} lines vs {len(expected)}')
        checked += 1
    print(f'letter pages checked    : {checked}')
    print(f'manuscript pages        : {total_pages}')
    print(f'archival lines exact    : {mismatch == 0}')
    assert checked == len(recs), f'page count {checked} != record count {len(recs)}'
    assert mismatch == 0, 'archival text was altered - refusing to continue'
    print('VERIFIED: every archival line reproduced character-for-character')


if __name__ == '__main__':
    main()
