# -*- coding: utf-8 -*-
"""
A page for each holding, in both languages.

Reads  : units/<slug>/about.md      the description of the holding
         units/<slug>/process.md    how the holding was prepared
         (and about_de.md / process_de.md where they exist)
Writes : site/_holdings/<slug>.md      /sources/<slug>/
         site/_holdings_de/<slug>.md   /de/quellen/<slug>/

The two texts are written by hand and kept with the holding. A document is
cited in them as [[41]] or [[41, 44]]; the citation becomes a link to that
document of the same holding, and check_unit_text.py holds each sentence to the
documents it cites. Everything under site/_holdings* is generated output.
"""
import os, re

CITE = re.compile(r'\[\[\s*([0-9]+[a-z]?(?:\s*,\s*[0-9]+[a-z]?)*)\s*\]\]')
# Another holding, named by its reference and linked to its page.
HOLDING = re.compile(r'\[\[unit:([a-z0-9]+)\]\]')
# A paragraph that states no fact from a document (where the file is kept, how
# it is arranged) says so with this mark, and is not asked for a citation.
CONTEXT = '<!-- context -->'
# Divides the two texts in the generated page; the layout splits on it.
SPLIT = '<!--prepared-->'


def cited(text):
    """Every document id a text cites, in order, with repeats."""
    return [i.strip() for m in CITE.finditer(text) for i in m.group(1).split(',')]


def read_text(unit_dir, name, lang):
    """(text, language it is in) for about/process; German falls back to English."""
    for suffix, got in ((('_de', 'de'),) if lang == 'de' else ()) + (('', 'en'),):
        p = os.path.join(unit_dir, name + suffix + '.md')
        if os.path.exists(p):
            s = open(p, encoding='utf-8').read().strip()
            if s:
                return s, got
    return '', lang


def link_holdings(text, units, base):
    """[[unit:<slug>]] becomes that holding's reference, linked to its page."""
    refs = {u.slug: u['ref'] for u in units}

    def one(m):
        slug = m.group(1)
        if slug not in refs:
            return m.group(0)
        return '<a href="{{ %r | relative_url }}">%s</a>' % (base + slug + '/', refs[slug])
    return HOLDING.sub(one, text)


def link_citations(text, url_by_id):
    def one(m):
        links = []
        for i in (x.strip() for x in m.group(1).split(',')):
            url = url_by_id.get(i)
            # An id that names no document is left as plain text here; the
            # checker reports it, and a build is not the place to stop for it.
            links.append('<a href="{{ %r | relative_url }}">%s</a>' % (url, i)
                         if url else i)
        return '<span class="cite">[' + ', '.join(links) + ']</span>'
    return CITE.sub(one, text)


def write(units, recs, site_dir, root, yaml_str):
    by_unit = {}
    for r in recs:
        by_unit.setdefault(r['unit'], {})[r['letter_id']] = r['permalink']
    n = 0
    for lang, folder, base, other in (('en', '_holdings', '/sources/', '/de/quellen/'),
                                      ('de', '_holdings_de', '/de/quellen/', '/sources/')):
        out_dir = os.path.join(site_dir, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))
        for u in units:
            if u.slug not in by_unit:
                continue
            unit_dir = os.path.join(root, 'units', u.slug)
            about, about_lang = read_text(unit_dir, 'about', lang)
            process, process_lang = read_text(unit_dir, 'process', lang)
            about = link_holdings(about, units, base)
            process = link_holdings(process, units, base)
            urls = by_unit[u.slug]
            fm = ['---',
                  f'unit: {yaml_str(u.slug)}',
                  f'title: {yaml_str(u["ref"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + u.slug + "/")}',
                  f'alt_url: {yaml_str(other + u.slug + "/")}',
                  f'has_about: {"true" if about else "false"}',
                  f'has_process: {"true" if process else "false"}',
                  f'about_lang: {about_lang}',
                  f'process_lang: {process_lang}',
                  '---']
            body = (link_citations(about, urls) + '\n\n' + SPLIT + '\n\n'
                    + link_citations(process, urls) + '\n')
            with open(os.path.join(out_dir, u.slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + body)
            n += 1
    print(f'wrote {n} holding pages to site/_holdings/ and site/_holdings_de/')
