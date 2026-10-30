# -*- coding: utf-8 -*-
"""One-off (2026-10-30): give each newspaper item a real title. The editor:
some of the titles were far longer than the newspaper's own title. `title` is
now the headline as printed (empty where the item has none), `title_en` and
`title_de` the title in each language of the site, `issue_en` / `issue_de`
the line of volume, number, date and page. The old long title is kept as
`long_title` (nothing displays it). Run once; the record is the commit.
Usage: python pipeline/review/set_np_titles.py [--apply]
"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# slug: (title as printed, title_en, title_de, issue_en, issue_de)
T = {
 'dziennikpoznanski18791220': ('', 'Death notice of Count Włodzimierz Miączyński',
    'Todesanzeige des Grafen Włodzimierz Miączyński',
    'R. 21, nr 292 · 20 December 1879 · p. 4', 'Jg. 21, Nr. 292 · 20. Dezember 1879 · S. 4'),
 'dziennikpoznanski19370807': ('Z Zagórowa', 'From Zagórów', 'Aus Zagórów',
    'R. 79, nr 180 · 7 August 1937', 'Jg. 79, Nr. 180 · 7. August 1937'),
 'echotureckie1931018': ('Zajście w Zagórowie', 'A disturbance in Zagórów', 'Ein Vorfall in Zagórów',
    'R. 8, nr 18 (nr 379) · 6 May 1931', 'Jg. 8, Nr. 18 (Nr. 379) · 6. Mai 1931'),
 'jutrzenka1913z8': ('Jak się ubiera nasz lud.', 'How our people dress', 'Wie sich unser Volk kleidet',
    'R. 3, nr 8 · 24 April 1913 · pp. 7-10', 'Jg. 3, Nr. 8 · 24. April 1913 · S. 7-10'),
 'kurjerpoznanski19330712': ('(Zhitleryzowani koloniści)', 'Hitlerized colonists', 'Hitlerisierte Kolonisten',
    '12 July 1933', '12. Juli 1933'),
 'kuryerpolski1754075': ('', 'Report on the funeral of Paweł Prusimski', 'Bericht über das Begräbnis des Paweł Prusimski',
    'nr 75 · 25 December 1754', 'Nr. 75 · 25. Dezember 1754'),
 'luteraniezagorow': ('Zagórów filiał Parafii Ewangelicko - Augsburskiej w Koninie',
    'Zagórów, the filial of the Evangelical-Augsburg Parish in Konin',
    'Zagórów, Filial der Evangelisch-Augsburgischen Pfarrei in Konin',
    'luteranie.konin.pl · undated', 'luteranie.konin.pl · ohne Datum'),
 'ostdeutscherbeobachter19420197': ('225 Jahre alte deutsche Siedlung im Wartheland',
    'A 225-year-old German settlement in the Wartheland', '225 Jahre alte deutsche Siedlung im Wartheland',
    'Jg. 4, Nr. 197 · 19 July 1942', 'Jg. 4, Nr. 197 · 19. Juli 1942'),
 'slowo18920104': ('Sprzedaże dóbr', 'Sales of estates', 'Güterverkäufe',
    'R. XI, nr 2 · 4 January 1892 · p. 3', 'Jg. XI, Nr. 2 · 4. Januar 1892 · S. 3'),
 'twojaslupca20150706': ('Trąbczyn świętował 775 lat', 'Trąbczyn celebrated 775 years', 'Trąbczyn feierte 775 Jahre',
    'twojaslupca.pl · 6 July 2015', 'twojaslupca.pl · 6. Juli 2015'),
 'zdrowie1912z10': ('W sprawie odżywiania się ludu', 'On the nutrition of the people', 'Zur Ernährung des Volkes',
    'R. XXVIII, z. 10 · 1912 · pp. 720-725', 'Jg. XXVIII, H. 10 · 1912 · S. 720-725'),
 'zdrowie1914z6': ('Jak mieszka lud nasz?', 'How does our people live?', 'Wie wohnt unser Volk?',
    'R. XXX, z. 6 · 1914 · pp. 432-440', 'Jg. XXX, H. 6 · 1914 · S. 432-440'),
}


def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def block(text, key):
    """(start, end) of a top-level `key:` entry with its indented lines."""
    m = re.search(r'^%s:.*\n' % key, text, re.M)
    if not m:
        return None
    end = m.end()
    for line in text[m.end():].splitlines(keepends=True):
        if line.startswith((' ', '\t')) or not line.strip():
            end += len(line)
        else:
            break
    return m.start(), end


def main():
    apply = '--apply' in sys.argv
    base = os.path.join(ROOT, 'newspapers')
    slugs = sorted(d for d in os.listdir(base) if os.path.exists(os.path.join(base, d, 'item.yml')))
    assert set(slugs) == set(T), set(slugs) ^ set(T)
    for slug in slugs:
        p = os.path.join(base, slug, 'item.yml')
        text = open(p, encoding='utf-8').read()
        assert 'long_title:' not in text, slug
        printed, en, de, ien, ide = T[slug]
        tb = block(text, 'title')
        old_title = text[tb[0]:tb[1]]
        # drop the old title_en (its replacement is below)
        text = text[:tb[0]] + 'LONGTITLE_AND_NEW\n' + text[tb[1]:]
        eb = block(text, 'title_en')
        if eb:
            text = text[:eb[0]] + text[eb[1]:]
        new = ('# The title of the item (editor, 2026-10-30): the headline as the paper prints it\n'
               '# (empty where it has none), then the title in each language of the site. The\n'
               '# long description that stood here is kept as long_title and shown nowhere.\n'
               f'title: {q(printed)}\n'
               f'title_en: {q(en)}\n'
               f'title_de: {q(de)}\n'
               f'issue_en: {q(ien)}\n'
               f'issue_de: {q(ide)}\n'
               + old_title.replace('title:', 'long_title:', 1))
        text = text.replace('LONGTITLE_AND_NEW\n', new, 1)
        print(slug, '->', en)
        if apply:
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(text)


main()
