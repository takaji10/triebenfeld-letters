"""The mechanical part of the voice review (docs/VOICE_REVIEW_PLAN.md, step 3).

Reads the site's own prose in scope - the document summaries, the holdings'
"About" and "How it was prepared", the literature's accounts, briefs and
summaries, the newspapers' accounts and briefs, the hand-made links'
sentences, the people's bios, the genealogy's notes and the glossary's
definitions - in English and German, and counts what can be counted against
docs/EDITORS_VOICE.md ("The brief") and docs/HOUSE_STYLE.md:

  long         a sentence of more than 50 words (the editor averages 29)
  connective   "however", "moreover", "furthermore", "additionally", "notably"
               (de: "jedoch", "außerdem", "darüber hinaus", "zudem")
  reader       "you" / "your", a question mark
  contraction  n't, 're, 've, 'll, 'm, 'd
  dash         an em dash or a hyphen standing for a dash; the rule is the
               spaced en dash ( – ), English and German
  spelling     an American form where the editor writes Canadian
  repo         the repository on a reader's page: NEEDS_CONFIRMATION, a file
               path, a backticked slug, a dated ruling ("the editor, 2026-..."),
               TODO, the changelog, a spot sheet, an era's code name
  meta         the site talking about itself: "this page", "below", "above",
               "the edition", "die Edition", "Ausgabe" (of the site)

Nothing is changed. Writes review/voice/report.md (a section per file, worst
first) and review/voice/counts.csv, and prints the totals. The holdings'
"How it was prepared" is the one place method may be told (HOUSE_STYLE, "No
method talk"), so its repo and meta flags are reported apart.

Usage: python pipeline/review/voice_scan.py
"""
import csv, glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'review', 'voice')


def texts():
    """(kind, where, lang, text) for every piece of prose in scope."""
    os.chdir(ROOT)
    for lang, f in (('en', 'site/_data/summaries.yml'), ('de', 'site/_data/summaries_de.yml')):
        for k, v in (yaml.safe_load(open(f, encoding='utf-8')) or {}).items():
            if isinstance(v, str):
                yield 'summary', k, lang, v
    for f in sorted(glob.glob('units/*/about*.md') + glob.glob('units/*/process*.md')):
        slug = f.split('/')[1] if '/' in f else f.split(os.sep)[1]
        base = os.path.basename(f)
        kind = 'holding-about' if base.startswith('about') else 'holding-process'
        lang = 'de' if base.endswith('_de.md') else 'en'
        t = re.sub(r'<!--.*?-->', '', open(f, encoding='utf-8').read(), flags=re.S)
        yield kind, slug, lang, t
    for f in sorted(glob.glob('literature/*/work.yml')):
        y = yaml.safe_load(open(f, encoding='utf-8')) or {}
        for key in ('account', 'brief', 'summary'):
            for lang in ('en', 'de'):
                if y.get(f'{key}_{lang}'):
                    yield 'literature', f'{y.get("slug")}/{key}', lang, y[f'{key}_{lang}']
    for f in sorted(glob.glob('newspapers/*/item.yml')):
        y = yaml.safe_load(open(f, encoding='utf-8')) or {}
        for key in ('account', 'brief'):
            for lang in ('en', 'de'):
                if y.get(f'{key}_{lang}'):
                    yield 'newspaper', f'{y.get("slug")}/{key}', lang, y[f'{key}_{lang}']
    links = yaml.safe_load(open('literature/links.yml', encoding='utf-8'))
    for ln in (links if isinstance(links, list) else links.get('links', [])):
        for lang in ('en', 'de'):
            if isinstance(ln, dict) and ln.get(lang):
                yield 'link', ln.get('id', '?'), lang, ln[lang]
    for slug, b in (yaml.safe_load(open('reference/people_bios.yml', encoding='utf-8')) or {}).items():
        if isinstance(b, dict):
            for key, lang in (('bio', 'en'), ('bio_de', 'de')):
                if b.get(key):
                    yield 'person', slug, lang, b[key]
    def walk(o, where):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and k in ('bio', 'note', 'notes'):
                    yield 'genealogy', where, 'en', v
                elif isinstance(v, str) and k in ('bio_de', 'notes_de', 'note_de'):
                    yield 'genealogy', where, 'de', v
                else:
                    yield from walk(v, where if not isinstance(k, str) or k in ('marriages', 'children', 'parents') else k)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v, where)
    yield from walk(yaml.safe_load(open('reference/genealogy.yml', encoding='utf-8')), 'genealogy')
    g = yaml.safe_load(open('reference/glossary.yml', encoding='utf-8'))
    for e in (g.get('entries') if isinstance(g, dict) else g) or []:
        if isinstance(e, dict):
            for key, lang in (('short_en', 'en'), ('long_en', 'en'), ('short_de', 'de'), ('long_de', 'de')):
                if e.get(key):
                    yield 'glossary', e.get('slug') or e.get('id') or '?', lang, e[key]


def sentences(t):
    t = re.sub(r'\[\^?[\w-]+\]|\[\[[^\]]*\]\]|\(\{\{[^)]*\}\}\)|`[^`]*`(?=\))', '', t)  # footnote marks, links
    t = re.sub(r'^#+ .*$|^\s*[-*] ', ' ', t, flags=re.M)
    t = re.sub(r'\s+', ' ', t).strip()
    return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜŁŚŻ„"(])', t) if s.strip()]


AMERICAN = r'\b(color(s|ed|ing|ful)?|honor(s|ed|able)?|favor(s|ed|ite|able)?|center(s|ed)?|theater|labor(s|ed|er|ers)?|neighbor(s|ing|hood)?|traveled|traveling|defense|offense|catalog(s)?|gray)\b'
CHECKS = {
    'en': {
        'connective': r'\b(however|moreover|furthermore|additionally|notably)\b',
        'reader': r'\byou(r|rs)?\b|\?',
        'contraction': r"\b\w+(n't|'re|'ve|'ll|'m|'d)\b",
        'spelling': AMERICAN,
        'meta': r'\b(this page|on this site|see below|see above|as above|the edition|this edition)\b',
    },
    'de': {
        'connective': r'\b(jedoch|außerdem|darüber hinaus|zudem)\b',
        # "Sie" is as often "she" or "they" as the reader; only the dative counts
        'reader': r'\bIhnen\b|\?',
        'contraction': r'(?!)',
        'spelling': r'(?!)',
        'meta': r'\b(diese Seite|siehe unten|siehe oben|der Edition|die Edition|dieser Edition|der Ausgabe(?! der Datenbank)|diese Ausgabe)\b',
    },
}
QUOTE = re.compile(r'"[^"]*"|“[^”]*”|„[^“”]*[“”]|«[^»]*»|‘[^’]*’(?!s)')
DASH = r'\S—\S|\s—\s|\s-\s'
REPO = (r'NEEDS_CONFIRMATION|\b[\w./-]+\.(yml|yaml|md|py|json|csv)\b|`[^`]+`|\((the )?editor,? \d{4}-\d\d|'
        r'\b20\d\d-\d\d-\d\d\b|\bTODO\b|changelog|spot sheet|Spot-Bogen|\b(wlodzimierz|prusimski-boundary|twentieth-century|hohenlohe|restitution|medieval)-era\b')


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    totals = {}
    for kind, where, lang, t in texts():
        ss = sentences(t)
        if not ss:
            continue
        lens = [len(re.findall(r"[\w'’-]+", s)) for s in ss]
        flags = []
        for s, n in zip(ss, lens):
            if n > 50:
                flags.append(('long', f'{n} words', s))
            bare = QUOTE.sub(' ', s)
            for name, rx in CHECKS[lang].items():
                for m in re.finditer(rx, bare, flags=re.I if name != 'reader' or lang == 'en' else 0):
                    flags.append((name, m.group(0), s))
            for m in re.finditer(DASH, s):
                flags.append(('dash', repr(m.group(0)), s))
            for m in re.finditer(REPO, s):
                flags.append(('repo', m.group(0), s))
        if kind == 'holding-process':
            flags = [(('method-' + n) if n in ('repo', 'meta') else n, a, b) for n, a, b in flags]
        avg = sum(lens) / len(lens)
        rows.append({'kind': kind, 'where': where, 'lang': lang, 'sentences': len(ss),
                     'avg_words': round(avg, 1), 'flags': flags})
        for n, _, _ in flags:
            totals[(kind, n)] = totals.get((kind, n), 0) + 1
    rows.sort(key=lambda r: (-len(r['flags']), r['kind'], r['where'], r['lang']))
    with open(os.path.join(OUT, 'counts.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        names = ['long', 'connective', 'reader', 'contraction', 'dash', 'spelling', 'repo', 'meta', 'method-repo', 'method-meta']
        w.writerow(['kind', 'where', 'lang', 'sentences', 'avg_words'] + names)
        for r in rows:
            w.writerow([r['kind'], r['where'], r['lang'], r['sentences'], r['avg_words']]
                       + [sum(1 for n, _, _ in r['flags'] if n == x) for x in names])
    with open(os.path.join(OUT, 'report.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Voice scan\n\nGenerated by pipeline/review/voice_scan.py; nothing was changed.\n\n')
        for r in rows:
            if not r['flags']:
                continue
            f.write(f"## {r['kind']} {r['where']} ({r['lang']}): {len(r['flags'])} flags, "
                    f"{r['sentences']} sentences, {r['avg_words']} words on average\n\n")
            for n, a, s in r['flags']:
                f.write(f'- **{n}** `{a}`: {s[:300]}\n')
            f.write('\n')
    sys.stdout.reconfigure(encoding='utf-8')
    kinds = sorted({k for k, _ in totals})
    for k in kinds:
        n_items = sum(1 for r in rows if r['kind'] == k)
        avg = [r['avg_words'] for r in rows if r['kind'] == k and r['lang'] == 'en']
        print(f'{k:16} {n_items:4} texts; EN avg sentence {sum(avg)/len(avg) if avg else 0:4.1f} words; '
              + ', '.join(f'{n} {c}' for (kk, n), c in sorted(totals.items()) if kk == k))
    print('report: review/voice/report.md')


if __name__ == '__main__':
    main()
