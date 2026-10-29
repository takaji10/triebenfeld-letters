# -*- coding: utf-8 -*-
"""
The newspapers on the website: the press section, one page per item.

Reads  : newspapers/<slug>/item.yml, original.md, english.md,
         site/_data/i18n.yml (the labels)
Writes : site/_data/newspapers.yml      the visible items, for the list page
         site/_newspapers/<slug>.md     /newspapers/<slug>/
         site/_newspapers_de/<slug>.md  /de/zeitungen/<slug>/

The press section is the editor's ruling of 2026-10-22 ("Let's make a new
section for newspaper articles, since it doesn't really fall under archival
sources or literature"): newspaper items are neither holdings (the Sources
page is for primary sources from archives) nor literature (works about the
history). The first item is the "Z Zagórowa" column of Dziennik Poznański,
R. 79, nr 180 (7 August 1937).

An item's page is like a work of the literature's (one text at a time, the
English first, by the buttons of _layouts/newspaper.html), but it has no
passages: the item is one clipping, shown whole, the original line by line
as printed (the ¬ of a word broken at the line's end is kept as printed).

Everything under site/_newspapers* is generated output.

Usage: python pipeline/newspapers/newspapers_site.py
"""
import io, os, re, sys, json
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NEWS = os.path.join(ROOT, 'newspapers')
SITE = os.path.join(ROOT, 'site')
BASES = {'en': ('_newspapers', '/newspapers/', '/de/zeitungen/'),
         'de': ('_newspapers_de', '/de/zeitungen/', '/newspapers/')}

HEADING = re.compile(r'^(#{1,6})(?=\s)', re.M)


def body_of(path):
    """The file's text: leading comment lines and the blank line after them
    are the file's own header, as in dataset/literature/."""
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
    does not make a table of the line."""
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
    items = []
    for slug in sorted(os.listdir(NEWS)):
        d = os.path.join(NEWS, slug)
        if not os.path.isdir(d):
            continue
        with open(os.path.join(d, 'item.yml'), encoding='utf-8') as f:
            it = yaml.safe_load(f)
        it['slug'] = slug
        items.append(it)

    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))

    listing = []
    for it in sorted(items, key=lambda x: (x['year'], x['slug'])):
        # The thumb is written only when the file is here (make_thumbs.py),
        # so a card shows no image the site does not carry; the briefs are
        # the card's own short rendering of the account (the long account
        # stays on the item's page).
        thumb = None
        if os.path.isfile(os.path.join(SITE, 'assets', 'thumbs', f'np-{it["slug"]}.jpg')):
            thumb = f'/assets/thumbs/np-{it["slug"]}.jpg'
        row = {k: it.get(k, '') for k in (
            'slug', 'newspaper', 'title', 'title_en', 'cite', 'ref',
            'published', 'year', 'language', 'english_by', 'source',
            'image', 'translation', 'account_en', 'account_de')}
        row |= {'brief_en': it.get('brief_en') or None,
                'brief_de': it.get('brief_de') or None,
                'thumb': thumb}
        listing.append(row | {'summary_only': not it.get('visible', True)})
        if it.get('visible', True):
            texts = {'en': body_of(os.path.join(NEWS, it['slug'], 'english.md')),
                     it['language']: body_of(os.path.join(NEWS, it['slug'], 'original.md'))}
        else:
            # Kept off the site (under copyright, the rule of the literature,
            # LITERATURE_PLAN section 4): no text, only the detailed summary
            # of the contents, in both languages, or the build stops.
            if not (it.get('summary_en') and it.get('summary_de')):
                raise SystemExit(
                    f"{it['slug']}: kept off the site but has no summary_en and "
                    'summary_de in its item.yml')
        for lang, (folder, base, other) in BASES.items():
            body = ['{% raw %}']
            if it.get('visible', True):
                for lg, cls in ((it['language'], 'lit-orig'), ('en', 'lit-en')):
                    body += [f'<div class="{cls}" lang="{lg}" markdown="1">', '',
                             render(texts[lg]), '', '</div>']
            else:
                body += ['<div class="np-summary" markdown="1">', '',
                         it['summary_' + lang].strip(), '', '</div>']
            body.append('{% endraw %}')
            fm = ['---',
                  f'item: {yaml_str(it["slug"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + it["slug"] + "/")}',
                  f'alt_url: {yaml_str(other + it["slug"] + "/")}',
                  'excerpt_separator: ""',
                  '---']
            with open(os.path.join(SITE, folder, it['slug'] + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    with open(os.path.join(SITE, '_data', 'newspapers.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/newspapers/newspapers_site.py from\n'
                '# newspapers/<slug>/item.yml. An item kept off the site is\n'
                '# listed with summary_only: true and holds only its summary.\n')
        yaml.safe_dump(listing, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f'wrote {len(items)} newspaper items to site/_newspapers/ '
          'and site/_newspapers_de/')


if __name__ == '__main__':
    main()
