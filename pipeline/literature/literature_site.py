# -*- coding: utf-8 -*-
"""
The literature on the website: a list of the works and a page for each.

Reads  : corpus/literature/index.json and the passage files beside it
         (made by build_literature.py), site/_data/i18n.yml (the labels)
Writes : site/_data/literature.yml         the visible works, for the list page
         site/_literature/<slug>.md        /literature/<slug>/
         site/_literature_de/<slug>.md     /de/literatur/<slug>/

A work with `visible: false` (Seidel, docs/LITERATURE_PLAN.md section 4) is
skipped entirely: nothing of it is written under site/. verify_site.py holds
the built site to that.

Each page gives the work passage by passage, the original and the English side
by side, each passage headed by its printed page so that it can be cited. The
text is the passage file's, rendered as Markdown by Jekyll. Only the rendering
is changed, never the words: footnote markers [^n] become links to their notes
(kramdown's own footnotes would clash between the two columns), headings are
set two levels down under the page's own, and the four-space indent of a
note's second paragraph is taken off so that it is not shown as code, a "|"
outside a table is escaped (kramdown would make the line a table), and a line
break inside a paragraph is kept as a break.
Everything under site/_literature* is generated output.

Usage: python pipeline/literature/literature_site.py
"""
import io, os, re, sys, json
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(ROOT, 'corpus', 'literature')
SITE = os.path.join(ROOT, 'site')
BASES = {'en': ('_literature', '/literature/', '/de/literatur/'),
         'de': ('_literature_de', '/de/literatur/', '/literature/')}

DEF = re.compile(r'^\[\^([^\]\s]+)\]:[ \t]*', re.M)
# a note ([^5]: at the start of a line) or a marker ([^5] anywhere else)
NOTE = re.compile(r'^\[\^(?P<d>[^\]\s]+)\]:[ \t]*|\[\^(?P<r>[^\]\s]+)\]', re.M)
HEADING = re.compile(r'^(#{1,6})(?=\s)', re.M)
IAL = re.compile(r'[ \t]*\{#[^}]*\}[ \t]*$', re.M)


def passage_text(slug, key, lang):
    path = os.path.join(CORPUS, slug, f'{key}.{lang}.txt')
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    # three comment lines and a blank line (build_literature.header)
    assert all(l.startswith('# ') for l in lines[:3]) and lines[3] == '', path
    return '\n'.join(lines[4:]).rstrip('\n')


def footnotes(texts, lang):
    """Turn [^n] into links and [^n]: into anchored notes, across one work.

    A marker links to the first note of its number at or after it, else the
    last one before it: a book may number its notes again in each chapter."""
    defs = []                       # (passage index, offset, id)
    for i, t in enumerate(texts):
        if t:
            defs += [(i, m.start(), m.group(1)) for m in DEF.finditer(t)]
    anchor = {d: f'n-{lang}-{n}' for n, d in enumerate(defs, 1)}

    def target(i, pos, fid):
        same = [d for d in defs if d[2] == fid]
        after = [d for d in same if (d[0], d[1]) >= (i, pos)]
        d = after[0] if after else (same[-1] if same else None)
        return anchor.get(d)

    out, missing = [], 0
    for i, t in enumerate(texts):
        if t is None:
            out.append(None)
            continue
        def one(m):
            nonlocal missing
            if m.group('d'):
                return (f'<span class="lit-note" id="{anchor[(i, m.start(), m.group("d"))]}">'
                        f'{m.group("d")}</span> ')
            a = target(i, m.start(), m.group('r'))
            if not a:
                missing += 1
                return m.group(0)
            return f'<sup class="lit-fn"><a href="#{a}">{m.group("r")}</a></sup>'
        out.append(NOTE.sub(one, t))
    return out, missing


BLOCK = re.compile(r'^\s*(\||#|[-*+] |\d+[.)] )')


def render(t):
    t = IAL.sub('', t)
    t = HEADING.sub(lambda m: '#' * min(6, len(m.group(1)) + 2), t)
    t = re.sub(r'^    (?=\S)', '', t, flags=re.M)
    # a name printed as asterisks ("v. ****d") is not emphasis
    t = re.sub(r'\*{4,}', lambda m: '\\*' * len(m.group(0)), t)
    lines = t.split('\n')
    for i, line in enumerate(lines):
        table = line.lstrip().startswith('|')
        # kramdown takes any line with a "|" for a table row ("16|38.")
        if not table:
            line = line.replace('|', '\\|')
        # a line break inside a paragraph is kept, as the files show it
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if (line.strip() and nxt.strip() and not table and not line.lstrip().startswith('#')
                and not BLOCK.match(nxt) and not line.endswith(('  ', '\\'))):
            line += '  '
        lines[i] = line
    return '\n'.join(lines)


def label(p, s):
    t = _label(p, s)
    return t[:1].upper() + t[1:] if p['key'].endswith('front') else t


def _label(p, s):
    if p['key'] == 'notes':
        return s['lit_notes']
    if p.get('title'):
        return p['title']
    part = s['lit_part'].replace('%d', str(p['part'])) + ', ' if p['part'] else ''
    if p['key'].endswith('front'):
        return part + s['lit_front']
    m = re.search(r'(\w+)-u(\d+)$', p['key'])
    if m:
        return part + s['lit_unnumbered'].replace('%s', m.group(1))
    return part + s['lit_page'].replace('%s', str(p['page']))


def short(p, s):
    """The label in the list of pages at the head of a work."""
    if p['key'] == 'notes':
        return s['lit_notes']
    if p.get('title'):
        return p['title']
    if p['key'].endswith('front'):
        return (f"{p['part']}: " if p['part'] else '') + s['lit_front_short']
    if re.search(r'-u\d+$', p['key']):
        return None
    return (f"{p['part']}: " if p['part'] and p['page'] in ('1',) else '') + str(p['page'])


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def main():
    with open(os.path.join(CORPUS, 'index.json'), encoding='utf-8') as f:
        works = json.load(f)
    with open(os.path.join(SITE, '_data', 'i18n.yml'), encoding='utf-8') as f:
        strings = yaml.safe_load(f)
    shown = [w for w in works if w.get('visible')]
    hidden = [w['slug'] for w in works if not w.get('visible')]

    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))

    listing = []
    for w in sorted(shown, key=lambda w: w['year']):
        slug, orig = w['slug'], w['language']
        ps = w['passages']
        texts = {}
        for lg in (orig, 'en'):
            texts[lg], missing = footnotes([passage_text(slug, p['key'], lg) for p in ps], lg)
            if missing:
                print(f'{slug} ({lg}): {missing} note markers with no note, left as they stand')
        listing.append({k: w.get(k, '') for k in (
            'slug', 'kind', 'title', 'title_en', 'cite', 'author', 'published',
            'year', 'language', 'english_by', 'scan', 'account_en', 'account_de')}
            | {'pages': sum(1 for p in ps if p['page'])})
        for lang, (folder, base, other) in BASES.items():
            s = strings[lang]
            body = ['{% raw %}', '<nav class="lit-jump" aria-label="' + s['lit_pages'] + '">']
            jumps = [(p['key'], short(p, s)) for p in ps]
            body.append(' '.join(f'<a href="#p-{k}">{v}</a>' for k, v in jumps if v))
            body.append('</nav>')
            for i, p in enumerate(ps):
                body += ['', f'<section class="lit-passage" id="p-{p["key"]}">',
                         f'<h2 class="lit-loc"><a href="#p-{p["key"]}">{label(p, s)}</a></h2>']
                for lg, cls in ((orig, 'lit-orig'), ('en', 'lit-en')):
                    t = texts[lg][i]
                    if t is None:
                        which = s['lit_english'] if lg == 'en' else s['lit_original']
                        body += [f'<div class="{cls} lit-none" lang="{lg}">',
                                 '<p>' + s['lit_missing'].replace('%s', which) + '</p>', '</div>']
                    else:
                        body += [f'<div class="{cls}" lang="{lg}" markdown="1">', '',
                                 render(t), '', '</div>']
                body.append('</section>')
            body.append('{% endraw %}')
            fm = ['---',
                  f'work: {yaml_str(slug)}',
                  f'title: {yaml_str(w["cite"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  # no excerpt: Jekyll would cut one inside the {% raw %} block
                  'excerpt_separator: ""',
                  '---']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    with open(os.path.join(SITE, '_data', 'literature.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/literature/literature_site.py from\n'
                '# literature/<slug>/work.yml. The works shown on the site only.\n')
        yaml.safe_dump(listing, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f'wrote {len(shown)} works to site/_literature/ and site/_literature_de/'
          + (f"; not shown: {', '.join(hidden)}" if hidden else ''))


if __name__ == '__main__':
    main()
