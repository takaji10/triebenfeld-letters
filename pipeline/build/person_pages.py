# -*- coding: utf-8 -*-
"""
The pages of the people who have their own page on the site.

Reads  : reference/genealogy.yml          the authored genealogy, one block
                                        per person (docs/LITERATURE_PLAN.md,
                                        section 22)
         site/_data/people.yml            the generated people (the build's)
         site/_data/literature_mentions.yml  the generated "In the literature"
Writes : site/_data/genealogy.yml         the genealogy as the site reads it
         site/_people/<slug>.md           the page, English
         site/_people_de/<slug>.md        the page, German

A block whose slug is a shown person makes that person a page: who they are
(the people.yml bio), their life dates, their family with the source of
every fact, the documents that name them, and the works of the literature
that name them. A block for a person of no document of the edition
(`standalone: true`) makes the page alone: the block carries its own heading
and biography, the page has no list of documents, and the literature it
belongs to is named by hand (`literature_passages:`).
The database's estimated dates are never carried
(reference/genealogy.yml, header; the editor, 2026-10-22).

Every `source` is validated and resolved here into what the page shows: a
"work/passage" becomes the work's citation and the passage's name, linked to
the passage on the work's page; a document uid becomes the holding's
reference and the document's number, linked to the document; "editor" becomes
the edition. A slip fails the build loudly:
  - every slug is a shown person of the edition;
  - every `link:` names a person of the edition;
  - every "work/passage" names a passage of a work shown on the site;
  - every uid names a document of the edition.

Run as a step of pipeline/regenerate.py, after literature_index.py, because the page
carries the "In the literature" list the index writes.

Usage: python pipeline/build/person_pages.py [--quiet]
"""
import io
import json
import os
import re
import sys
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'site')
DATA_DIR = os.path.join(SITE, '_data')


def yaml_str(s):
    """A double-quoted YAML scalar, on one line."""
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


def load(path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def main():
    quiet = '--quiet' in sys.argv
    genealogy = load(os.path.join(ROOT, 'reference', 'genealogy.yml')).get('people') or {}
    people = {p['slug']: p for p in load(os.path.join(DATA_DIR, 'people.yml'))}
    i18n = load(os.path.join(SITE, '_data', 'i18n.yml'))
    with open(os.path.join(ROOT, 'dataset', 'letters.json'), encoding='utf-8') as f:
        letters = {r['uid']: r for r in json.load(f)}
    with open(os.path.join(ROOT, 'dataset', 'literature', 'index.json'), encoding='utf-8') as f:
        lit = {w['slug']: w for w in json.load(f) if w.get('visible')}
    refs = {}

    def unit_ref(unit):
        if unit not in refs:
            with open(os.path.join(ROOT, 'units', unit, 'unit.yml'), encoding='utf-8') as f:
                refs[unit] = yaml.safe_load(f)['ref']
        return refs[unit]

    def resolve(src, lang, where):
        """A source string into [{text, url}] for the page to show."""
        s = i18n[lang]
        out = []
        for part in [x.strip() for x in str(src).split(';') if x.strip()]:
            if part == 'editor':
                out.append({'text': 'the edition' if lang == 'en' else 'die Edition'})
                continue
            if '/' in part:
                work, _, key = part.partition('/')
                w = lit.get(work)
                if w is None or not w.get('visible'):
                    raise ValueError(f'{where}: source {part!r}: no such visible work')
                p = next((p for p in w['passages'] if p['key'] == key), None)
                if p is None:
                    raise ValueError(f'{where}: source {part!r}: no passage of {work}')
                if p.get('title'):
                    label = p['title']
                elif key == 'front':
                    label = s['lit_front']
                else:
                    label = s['lit_page'].replace('%s', str(key))
                out.append({'text': f"{w['cite']}, {label}",
                            'url': f"/literature/{work}/#p-{key}" if lang == 'en'
                            else f"/de/literatur/{work}/#p-{key}"})
            elif part in lit:
                # a work named without a passage: the work's own page
                w = lit[part]
                out.append({'text': w['cite'],
                            'url': f"/literature/{part}/" if lang == 'en'
                            else f"/de/literatur/{part}/"})
            else:
                r = letters.get(part)
                if r is None:
                    raise ValueError(f'{where}: source {part!r}: no such document')
                ref = unit_ref(r['unit'])
                text = (f'{ref}, document {r["letter_id"]}' if lang == 'en'
                        else f'{ref}, Dokument {r["letter_id"]}')
                out.append({'text': text, 'url': r['permalink']})
        return out

    def resolve_entry(e, where):
        for lang in ('en', 'de'):
            if e.get('source'):
                e[f'sources_{lang}'] = resolve(e['source'], lang, where)
            if e.get('note_source'):
                e[f'note_sources_{lang}'] = resolve(e['note_source'], lang, where)

    def resolve_list(entries, where):
        for e in entries:
            resolve_entry(e, where)
            # a nested list with its own group source
            kids = e.get('children')
            if isinstance(kids, dict):
                e['children'] = kids.get('entries') or []
                if kids.get('source'):
                    e['children_source'] = kids['source']
                    e['children_sources_en'] = resolve(kids['source'], 'en', where)
                    e['children_sources_de'] = resolve(kids['source'], 'de', where)
            for k in (e.get('children') or []):
                resolve_entry(k, where)

    for slug, block in genealogy.items():
        where = f'genealogy.yml: {slug}'
        standalone = slug not in people
        if standalone:
            # A person of no document of the edition: the block carries its
            # own heading and biography, and the page has no list of
            # documents. The literature is named by hand.
            if not block.get('standalone'):
                raise ValueError(f'{where}: no person of the edition, and no '
                                 f"'standalone: true' - the block needs its own "
                                 f'heading and bio, or the slug is misspelt')
            for field in ('heading', 'heading_de', 'bio', 'bio_de'):
                if not block.get(field):
                    raise ValueError(f'{where}: a standalone block needs a {field}')
        if block.get('born'):
            if not block.get('born_source'):
                raise ValueError(f'{where}: born without a born_source')
            block['born_sources_en'] = resolve(block['born_source'], 'en', where)
            block['born_sources_de'] = resolve(block['born_source'], 'de', where)
        if block.get('died'):
            if not block.get('died_source'):
                raise ValueError(f'{where}: died without a died_source')
            block['died_sources_en'] = resolve(block['died_source'], 'en', where)
            block['died_sources_de'] = resolve(block['died_source'], 'de', where)
        resolve_list(block.get('parents') or [], f'{where}.parents')
        resolve_list(block.get('marriages') or [], f'{where}.marriages')
        resolve_list(block.get('children') or [], f'{where}.children')
        if block.get('literature_passages'):
            for lang in ('en', 'de'):
                block[f'literature_{lang}'] = [
                    r for e in block['literature_passages']
                    for r in resolve(e, lang, f'{where}.literature_passages')]

    # The site's copy of the genealogy.
    with open(os.path.join(DATA_DIR, 'genealogy.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/build/person_pages.py from '
                'reference/genealogy.yml - do not hand-edit.\n')
        yaml.safe_dump({'people': genealogy}, f, allow_unicode=True,
                       default_flow_style=False, sort_keys=False, width=100)

    # One page per person, in each language.
    bases = (('en', '_people', '/people/', '/de/personen/'),
             ('de', '_people_de', '/de/personen/', '/people/'))
    for lang, folder, url, other in bases:
        d = os.path.join(SITE, folder)
        if os.path.isdir(d):
            for fn in os.listdir(d):
                if fn.endswith('.md'):
                    os.remove(os.path.join(d, fn))
        os.makedirs(d, exist_ok=True)
        for slug in genealogy:
            if slug in people:
                p = people[slug]
                heading = p['heading_de'] if lang == 'de' else p['heading']
            else:
                g = genealogy[slug]
                heading = g['heading_de'] if lang == 'de' else g['heading']
            fm = ['---',
                  'layout: person',
                  f'person: {yaml_str(slug)}',
                  f'title: {yaml_str(heading)}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(url + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  'excerpt_separator: ""',
                  '---', '']
            with open(os.path.join(d, slug + '.md'), 'w', encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm))
        if not quiet:
            print(f'person pages ({lang}): {len(genealogy)}')


if __name__ == '__main__':
    main()
