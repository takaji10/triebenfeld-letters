# -*- coding: utf-8 -*-
"""
Cut the literature into passages and pair the two languages.

Reads  : literature/<slug>/work.yml, original.md, english.md
Writes : corpus/literature/index.json            every work and its passages
         corpus/literature/<slug>/<key>.<lang>.txt  one passage, one language
         (lang is the work's language, "la", "de", "fr" or "pl", or "en")

A work printed in English (`language: en`, Mączak 1968) has no english.md:
its original is cut alone, and its passages have the one language.

The literature is not part of the edition's documents (docs/LITERATURE_PLAN.md):
it is context, kept whole, for questions put to the edition. This script never
changes a text. A passage is the run of lines between two page marks, the marks
themselves left out; check() puts every work back together from its passages and
asserts that nothing was lost or changed but the marks and the blank lines at a
passage's ends.

How a work is cut (its work.yml, "pages"):
  mark     a page mark, a regex with a group "page" ("[p. 12]", "— 12 —").
           What stands before the first mark is the "front". Unnumbered pages
           before the first numbered page of a part belong to its front; an
           unnumbered page after a numbered one is keyed "<page>-u<k>".
  parts    true where page numbers begin again in each part (the Neue
           Feuerbrände): a drop in the numbers begins a new part, and the
           unnumbered and roman pages just before the drop open it. Keys are
           then "<part>-<page>". Without it a drop is reported as an error.
  chapter  a heading regex, for a work without page marks (Guradze until the
           editor adds them): one passage per chapter, keyed c01, c02, ...
  notes    (top level) a heading per language after which everything is one
           passage "notes" (the Materialien's gathered notes).

Keys found in one language only are reported: they are where the two files
differ and are to be looked at, not corrected here.

Usage: python pipeline/literature/build_literature.py [--quiet]
"""
import io, os, re, sys, json, shutil
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIT = os.path.join(ROOT, 'literature')
OUT = os.path.join(ROOT, 'corpus', 'literature')
LANGS = (('original', None), ('english', 'en'))


def read_lines(path):
    with open(path, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n').split('\n')


def is_arabic(label):
    return label.isdigit()


def raw_pages(lines, mark):
    """[(label or None for the front, start line, [lines])], marks left out."""
    pages = [[None, 1, []]]
    rx = re.compile(mark)
    for i, line in enumerate(lines, 1):
        m = rx.match(line)
        if m:
            pages.append([m.group('page'), i, []])
        else:
            pages[-1][2].append(line)
    return pages


def key_pages(pages, parts, errors, where):
    """Give each page its part and key; merge each part's front."""
    # assign parts: a drop in arabic numbers opens a new part, taking with it
    # the run of non-arabic pages since the last arabic one
    part, last = 1, None
    assigned = []          # [part, label, start, lines]
    pending = []
    for label, start, body in pages:
        if label is not None and is_arabic(label):
            n = int(label)
            if last is not None and n <= last:
                if not parts:
                    errors.append(f'{where}: page {label} (line {start}) after page {last}')
                else:
                    part += 1
                    for p in pending:
                        p[0] = part
            last = n
            pending = []
            assigned.append([part, label, start, body])
        else:
            row = [part, label, start, body]
            assigned.append(row)
            if label is not None:
                pending.append(row)
    # keys
    out = []
    seen_numbered = {}
    prev, ucount = {}, {}
    for part, label, start, body in assigned:
        pre = f'{part}-' if parts else ''
        if label is None or (label == 'unnumbered' and not seen_numbered.get(part)):
            key, page = pre + 'front', None
        elif label == 'unnumbered':
            ucount[(part, prev[part])] = ucount.get((part, prev[part]), 0) + 1
            key, page = f'{pre}{prev[part]}-u{ucount[(part, prev[part])]}', None
        else:
            seen_numbered[part] = True
            prev[part] = label
            key, page = pre + label, label
        if out and out[-1]['key'] == key:
            out[-1]['lines'].extend(body)
        else:
            out.append({'key': key, 'part': part if parts else None,
                        'page': page, 'start': start, 'lines': list(body)})
    return out


def chapters(lines, rx):
    out = [{'key': 'front', 'part': None, 'page': None, 'start': 1, 'lines': []}]
    n = 0
    rx = re.compile(rx)
    for i, line in enumerate(lines, 1):
        if rx.match(line):
            n += 1
            title = re.sub(r'\{#[^}]*\}', '', line.lstrip('#')).replace('*', '').strip()
            out.append({'key': f'c{n:02d}', 'part': None, 'page': None,
                        'title': title, 'start': i, 'lines': []})
        out[-1]['lines'].append(line)
    return out


def split_notes(passages, rx):
    """Everything from the notes heading on becomes the passage "notes"."""
    rx = re.compile(rx)
    for i, p in enumerate(passages):
        for j, line in enumerate(p['lines']):
            if rx.match(line):
                rest = p['lines'][j:]
                for q in passages[i + 1:]:
                    rest.extend(q['lines'])     # marks after the notes are dropped
                p['lines'] = p['lines'][:j]
                notes = {'key': 'notes', 'part': None, 'page': None,
                         'start': p['start'] + j, 'lines': rest}
                return passages[:i + 1] + [notes], len(passages) - i - 1
    return passages, 0


def trim(lines):
    a, b = 0, len(lines)
    while a < b and not lines[a].strip():
        a += 1
    while b > a and not lines[b - 1].strip():
        b -= 1
    return lines[a:b]


def cut(work, which, errors):
    lines = read_lines(os.path.join(LIT, work['slug'], which + '.md'))
    pages = work.get('pages') or {}
    where = f"{work['slug']}/{which}"
    if pages.get('mark'):
        passages = key_pages(raw_pages(lines, pages['mark']), pages.get('parts'),
                             errors, where)
    else:
        passages = chapters(lines, pages['chapter'])
    dropped = 0
    notes = (work.get('notes') or {}).get(which)
    if notes:
        passages, dropped = split_notes(passages, notes)
        if dropped:
            errors.append(f'{where}: {dropped} page marks after the notes heading')
    check(lines, passages, pages.get('mark'), where, errors)
    for p in passages:
        p['text'] = '\n'.join(trim(p['lines']))
    return [p for p in passages if p['text'] or p['page']]


def check(lines, passages, mark, where, errors):
    """The passages, put back together, are the file without its marks."""
    rx = re.compile(mark) if mark else None
    want = [l for l in lines if not (rx and rx.match(l))]
    got = [l for p in passages for l in p['lines']]
    if want != got:
        errors.append(f'{where}: the passages do not put the file back together')


def header(work, p, lang):
    loc = 'notes' if p['key'] == 'notes' else (
        f"part {p['part']}, " if p['part'] else '') + (
        f"p. {p['page']}" if p['page'] else p.get('title') or p['key'])
    return (f"# {work['slug']}  {p['key']}  {lang}\n"
            f"# {work['cite']}, {loc}\n"
            f"# {'translation by ' + work['english_by'] if lang == 'en' else 'original'}\n\n")


def main():
    quiet = '--quiet' in sys.argv
    errors, works = [], []
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for slug in sorted(os.listdir(LIT)):
        wy = os.path.join(LIT, slug, 'work.yml')
        if not os.path.isfile(wy):
            continue
        with open(wy, encoding='utf-8') as f:
            work = yaml.safe_load(f)
        assert work['slug'] == slug, wy
        langs = LANGS[:1] if work['language'] == 'en' else LANGS
        cuts = {which: cut(work, which, errors) for which, _ in langs}
        cuts.setdefault('english', [])
        by = {which: {p['key']: p for p in ps} for which, ps in cuts.items()}
        order = [p['key'] for p in cuts['original']]
        order += [k for k in by['english'] if k not in by['original']]
        only = {which: [k for k in order if k not in by[which]] for which, _ in langs}
        os.makedirs(os.path.join(OUT, slug))
        passages = []
        for k in order:
            o, e = by['original'].get(k), by['english'].get(k)
            p = o or e
            row = {'key': k, 'part': p['part'], 'page': p['page']}
            if p.get('title'):
                row['title'] = p['title']
            for which, lang in LANGS:
                q = by[which].get(k)
                lang = lang or work['language']
                if q is None:
                    continue
                row[lang] = {'line': q['start'], 'chars': len(q['text'])}
                with open(os.path.join(OUT, slug, f'{k}.{lang}.txt'), 'w',
                          encoding='utf-8', newline='\n') as f:
                    f.write(header(work, q, lang) + q['text'] + '\n')
            passages.append(row)
        works.append({k: work.get(k) for k in (
            'slug', 'visible', 'kind', 'title', 'title_en', 'cite', 'author',
            'author_sort', 'published', 'year', 'language', 'english_by', 'scan',
            'figures', 'account_en', 'account_de', 'summary_en', 'summary_de')
            if work.get(k) is not None}
            | {'passages': passages})
        n = len(passages)
        print(f"{slug}: {n} passages"
              + ''.join(f"; missing from the {w}: {', '.join(ks)}" for w, ks in only.items() if ks))
        if not quiet:
            short = [r['key'] for r in passages
                     if work['language'] in r and 'en' in r and r[work['language']]['chars']
                     and not 0.6 < r['en']['chars'] / r[work['language']]['chars'] < 1.8]
            if short:
                print(f"  lengths differ much: {', '.join(short)}")
    with open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(works, f, ensure_ascii=False, indent=1)
    for e in errors:
        print('ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
