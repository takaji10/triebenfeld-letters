# -*- coding: utf-8 -*-
"""
The places that have their own page on the website (docs/PLACES_PLAN.md).

Reads  : places/<slug>/place.yml              the authored page of the place
        places/<slug>/<source>/source.yml     one source of the place
        places/<slug>/<source>/original.md    the source as printed
        places/<slug>/<source>/english.md     Claude's English of it
        site/_data/estates.yml                the estates in focus (the build's)
Writes : site/_data/places_pages.yml          the places and their sources
        site/_places/<slug>.md                /places/<slug>/
        site/_places_de/<slug>.md             /de/orte/<slug>/

The place pages are the editor's ruling of 2026-10-22 ("a new source to a
place: Zagórów ... added under the place name, on a separate page for the
place"): a page per place, hung on the place's card on the Places page and
linked from it, bilingual like the person pages, carrying the sources
brought in for the place — each shown whole (the original as printed,
nothing tidied, with Claude's English beside it, the English first by the
literature's buttons, assets/literature.js) with its own facts, account and
caveat, as a newspapers item's page is. The first place is Zagórów
(slug zagorowo), whose first source is the town's own presentation on
zagorow.pl, captured by the Wayback Machine on 14 June 2022.

A source kept off the site (`visible: false`, the rule of the literature,
LITERATURE_PLAN section 4) is listed with summary_only: true and its page
holds only the summary of its contents — summary_en and summary_de are
required, or the build stops.

The slug of a place's page is the place's slug in reference/places.yml, the
same slug its card on the Places page carries; the build fails loudly if it
is no estate of the edition, so a misspelt slug cannot make an orphan page.

Run as a step of regenerate.py, after build_site_data.py (the estates) and
beside person_pages.py.

Usage: python pipeline/places/place_pages.py [--quiet]
"""
import io, os, re, sys, json
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLACES = os.path.join(ROOT, 'places')
SITE = os.path.join(ROOT, 'site')
BASES = {'en': ('_places', '/places/', '/de/orte/'),
         'de': ('_places_de', '/de/orte/', '/places/')}

HEADING = re.compile(r'^(#{1,6})(?=\s)', re.M)

# The fields of source.yml the site reads.
SOURCE_FIELDS = ('slug', 'ref', 'title', 'title_en', 'cite', 'site',
                 'original_url', 'captured', 'published', 'year',
                 'date_span', 'language', 'kind', 'era', 'english_by',
                 'source', 'account_en', 'account_de')


def body_of(path):
    """The file's text: leading comment lines and the blank line after them
    are the file's own header, as in corpus/literature/."""
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    i = 0
    while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
        if lines[i].strip() == '':
            i += 1
            break
        i += 1
    text = '\n'.join(lines[i:]).strip('\n')
    assert text, path
    return text


def render(t):
    """Only the rendering is changed, never the words: headings sit two
    levels down under the page's own, a line break inside a paragraph is
    kept (a printed line stays a printed line), a "|" is escaped so kramdown
    does not make a table of the line. As the newspapers' site builder
    renders its items."""
    t = HEADING.sub(lambda m: '#' * min(6, len(m.group(1)) + 2), t)
    lines = t.split('\n')
    for i, line in enumerate(lines):
        if not line.lstrip().startswith('|'):
            line = line.replace('|', '\\|')
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if (line.strip() and nxt.strip() and not line.lstrip().startswith('#')
                and not line.endswith(('  ', '\\'))):
            line += '  '
        lines[i] = line
    return '\n'.join(lines)


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def main():
    quiet = '--quiet' in sys.argv
    estates = {e['slug'] for e in (
        yaml.safe_load(io.open(os.path.join(SITE, '_data', 'estates.yml'),
                               encoding='utf-8')) or [])}

    places = []
    for slug in sorted(os.listdir(PLACES)):
        d = os.path.join(PLACES, slug)
        if not os.path.isdir(d):
            continue
        where = f'places/{slug}/place.yml'
        with open(os.path.join(d, 'place.yml'), encoding='utf-8') as f:
            pl = yaml.safe_load(f)
        if pl.get('slug') != slug:
            raise SystemExit(f'{where}: slug {pl.get("slug")!r} does not '
                             f'match the folder {slug!r}')
        if slug not in estates:
            raise SystemExit(f'{where}: {slug} is not an estate of the '
                             'edition - the page hangs on a card of the '
                             'Places page (reference/places.yml, '
                             'site/_data/estates.yml)')
        for field in ('heading', 'heading_de', 'standfirst_en',
                      'standfirst_de', 'intro_en', 'intro_de'):
            if not pl.get(field):
                raise SystemExit(f'{where}: a place page needs a {field}')

        sources = []
        for src in sorted(os.listdir(d)):
            sd = os.path.join(d, src)
            if not os.path.isdir(sd):
                continue
            swhere = f'places/{slug}/{src}/source.yml'
            with open(os.path.join(sd, 'source.yml'), encoding='utf-8') as f:
                sy = yaml.safe_load(f)
            visible = sy.get('visible', True)
            keep = {k: sy.get(k, '') for k in SOURCE_FIELDS}
            keep['visible'] = visible
            if visible:
                for fn in ('original.md', 'english.md'):
                    if not os.path.isfile(os.path.join(sd, fn)):
                        raise SystemExit(f'{swhere}: a shown source needs {fn}')
            else:
                # Kept off the site: the detailed summary of the contents,
                # in both languages, or the build stops (the literature's
                # rule, LITERATURE_PLAN section 4).
                if not (sy.get('summary_en') and sy.get('summary_de')):
                    raise SystemExit(
                        f'{swhere}: kept off the site but has no summary_en '
                        'and summary_de')
            sources.append(keep | {
                'dir': src,
                'summary_only': not visible,
                'summary_en': sy.get('summary_en', ''),
                'summary_de': sy.get('summary_de', ''),
            })
        if not sources:
            raise SystemExit(f'{where}: a place page needs at least one '
                             'source under its folder')
        places.append(pl | {'sources': sources})

    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))

    for pl in places:
        slug = pl['slug']
        for lang, (folder, base, other) in BASES.items():
            body = ['{%- comment -%} Generated by '
                    'pipeline/places/place_pages.py - do not hand-edit. '
                    'The urls.html include sets lang and t for the facts '
                    'below: the content is rendered before the layout, so '
                    'the layout\'s assignments are not in scope here. '
                    '{%- endcomment -%}',
                    '{% include urls.html %}']
            for s in pl['sources']:
                sd = os.path.join(PLACES, slug, s['dir'])
                lang_key = 'lit_lang_' + str(s['language'])
                published = s.get('published') or s['date_span']
                # The facts, the account and the caveat stand outside the
                # raw block: the page's labels are the site's i18n (the
                # newspapers' layout carries theirs; here the source is a
                # section of the place's page, and its facts stand with it).
                body += [f'<section class="place-source" id="s-{s["slug"]}">',
                         '',
                         f'<h2>{s["title"]}</h2>',
                         '',
                         '<dl class="source-facts">',
                         f'  <div><dt>{{{{ t.lit_published }}}}</dt>'
                         f'<dd>{published}</dd></div>',
                         f'  <div><dt>{{{{ t.lit_language }}}}</dt>'
                         f'<dd>{{{{ t["{lang_key}"] }}}}</dd></div>',
                         '</dl>',
                         '',
                         '<div class="prose">',
                         f'<p>{s["account_en"] if lang == "en" else s["account_de"]}</p>',
                         '<p class="lit-caveat">{{ t.np_caveat }}</p>',
                         (f'<p><a href="{s["source"]}" rel="noopener">'
                          f'{{{{ t.place_source_link }}}}</a></p>'
                          if s['source'] else '<!-- no source link -->'),
                         '</div>',
                         '',
                         '{% raw %}']
                if s['summary_only']:
                    body += ['<div class="np-summary" markdown="1">', '',
                             s['summary_' + lang].strip(), '', '</div>']
                else:
                    texts = {'en': body_of(os.path.join(sd, 'english.md')),
                             s['language']: body_of(os.path.join(sd, 'original.md'))}
                    for lg, cls in (('en', 'lit-en'), (s['language'], 'lit-orig')):
                        body += [f'<div class="{cls}" lang="{lg}" markdown="1">', '',
                                 render(texts[lg]), '', '</div>']
                body += ['{% endraw %}', '', '</section>', '']
            fm = ['---',
                  'layout: place',
                  f'place: {yaml_str(slug)}',
                  f'title: {yaml_str(pl["heading_de"] if lang == "de" else pl["heading"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  'excerpt_separator: ""',
                  '---', '']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    # The site's copy: the places and their sources, for the layout and the
    # link from the card on the Places page.
    out = {pl['slug']: {k: pl[k] for k in (
        'heading', 'heading_de', 'standfirst_en', 'standfirst_de',
        'intro_en', 'intro_de')} | {'sources': [
            {k: v for k, v in s.items() if k != 'dir'} for s in pl['sources']]}
           for pl in places}
    with open(os.path.join(SITE, '_data', 'places_pages.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/places/place_pages.py from '
                'places/<slug>/place.yml\n'
                '# and the source folders under them - do not hand-edit.\n'
                '# A source with summary_only: true is kept off the site; '
                'its page holds\n'
                '# only the summary of its contents.\n')
        yaml.safe_dump(out, f, allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=100)
    if not quiet:
        print(f'wrote {len(places)} place pages to site/_places/ '
              'and site/_places_de/')


if __name__ == '__main__':
    main()
