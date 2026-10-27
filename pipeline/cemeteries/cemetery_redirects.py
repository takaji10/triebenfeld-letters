# -*- coding: utf-8 -*-
"""
The redirect stubs for the cemeteries' move under Places (2026-10-27):
every address a cemetery page or the cemeteries' list page has ever had
keeps working, as the documents' redirects do. The stubs live in
site/redirects-static/ - site/redirects/ is wiped and rewritten by
build_site_data.py at every build, so anything static must not go there.

Writes : site/redirects-static/cemetery-<slug>.html   /cemeteries/<slug>/
         site/redirects-static/cemetery-de-<slug>.html /de/friedhoefe/<slug>/
         site/redirects-static/cemeteries.html         /cemeteries/
         site/redirects-static/friedhoefe.html         /de/friedhoefe/

The new addresses: /places/cemeteries/<slug>/ and /de/orte/friedhoefe/
<slug>/; the list pages redirect to the Places page's cemeteries section.

Usage: python pipeline/cemeteries/cemetery_redirects.py
"""
import io, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, 'site', '_data', 'cemeteries_list.yml')
OUT = os.path.join(ROOT, 'site', 'redirects-static')

NEW = {'en': '/places/cemeteries/', 'de': '/de/orte/friedhoefe/'}
OLD = {'en': '/cemeteries/', 'de': '/de/friedhoefe/'}
LIST_TO = {'en': '/places/#cemeteries', 'de': '/de/orte/#friedhoefe'}


def stub(path, permalink, target, text_en, text_de):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('---\n')
        f.write('permalink: "%s"\n' % permalink)
        f.write('sitemap: false\n')
        f.write('---\n')
        f.write('<link rel="canonical" href="{{ \'%s\' | relative_url }}">\n' % target)
        f.write('<meta http-equiv="refresh" content="0; url={{ \'%s\' | relative_url }}">\n' % target)
        f.write('<p>%s <a href="{{ \'%s\' | relative_url }}">%s</a>.</p>\n'
                % (text_en, target, target))


def main():
    with io.open(DATA, encoding='utf-8') as f:
        cems = yaml.safe_load(f) or []
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for lang, word in (('en', 'This page has moved to'),
                       ('de', 'Diese Seite ist umgezogen nach')):
        stub(os.path.join(OUT,
             'cemeteries.html' if lang == 'en' else 'friedhoefe.html'),
             OLD[lang], LIST_TO[lang], word, word)
        n += 1
        for c in cems:
            slug = c['slug']
            stub(os.path.join(OUT,
                 ('cemetery-%s.html' if lang == 'en' else 'cemetery-de-%s.html') % slug),
                 OLD[lang] + slug + '/', NEW[lang] + slug + '/', word, word)
            n += 1
    print(f'wrote {n} cemetery redirect stubs to site/redirects-static/')


if __name__ == '__main__':
    main()
