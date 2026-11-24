# -*- coding: utf-8 -*-
"""List candidate sentences in the edition's English prose that may break the
house style (docs/HOUSE_STYLE.md). It only lists; it changes nothing and
writes nothing into the repository (CSV to stdout, or to --out).

Rules (heuristics; read each hit):
  R1  physical counts: a sentence (or text) opening on a number word or digit
      followed within 4 words by page(s)/leaf/leaves/sheet(s)/notebook(s)/
      folio(s)/volume(s): "Thirteen pages of the register".
  R2  "the" at first mention: "the" + optional adjective + plural noun, or
      "the" + number word + noun, where that noun has not appeared earlier in
      the same text ("the three townsmen" with no earlier "townsmen").
  R4  the text as subject: "the letter states", "the entry is dated",
      "is dated at", "copied into", "under each entry", "stand the names of",
      "in the order in which", and "signed by" in the last sentence of a text.

Sources (docs/PROSE_SOURCES.md): units/*/about.md and unit.yml titles,
site/_data/summaries.yml, literature/*/work.yml, newspapers/*/item.yml,
reference/eras.yml, places/*/place.yml, reference/people_bios.yml,
reference/genealogy.yml.

Usage: python pipeline/review/prose_lint.py [--category C] [--unit SLUG]
                                            [--rule R1 --rule R2] [--out FILE]
Categories: holdings, summaries, literature, newspapers, eras, places, people.
Counts per rule and category go to stderr.
"""
import argparse, collections, csv, glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATEGORIES = ['holdings', 'summaries', 'literature', 'newspapers', 'eras',
              'places', 'people']

NUMS = ('one two three four five six seven eight nine ten eleven twelve '
        'thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty '
        'thirty forty fifty sixty seventy eighty ninety hundred several both '
        'many few').split()
NUM_RE = r'(?:%s|\d[\d,.]*)' % '|'.join(NUMS)
COUNT_NOUNS = r'(?:pages?|leaf|leaves|sheets?|notebooks?|folios?|volumes?)'
R1 = re.compile(r'^\W*(?:%s)\b(?:\s+[\w’\'.-]+){0,4}?\s+%s\b'
                % (NUM_RE, COUNT_NOUNS), re.I)

R4_PATTERNS = [re.compile(p, re.I) for p in (
    r'\bthe (?:text|letter|entry|document|note|register|copy|petition) '
    r'(?:states|says|records|notes|reads|mentions|reports)\b',
    r'\bthe entry is dated\b', r'\bis dated at\b', r'\bcopied into\b',
    r'\bunder each entry\b', r'\bstand the names of\b',
    r'\bin the order in which\b')]
SIGNED = re.compile(r'\bsigned by\b', re.I)

NUMWORD = re.compile(r'^(?:%s)$' % '|'.join(NUMS[:-4]), re.I)
THE_NUM = re.compile(r"\b[Tt]he\s+(%s)\s+([a-z][a-z-]+)\b(?!\s+(?:of|on|for|in|from|to|that|which|who|above|below|named|mentioned)\b)" % '|'.join(NUMS[:-4]))
THE_PLURAL = re.compile(r"\b[Tt]he\s+(?:([a-z][a-z-]+)\s+)?([a-z][a-z-]{3,})\b(?!\s+(?:of|on|for|in|from|to|that|which|who|whom|above|below|here|named|concerned|mentioned|following)\b)")
# "the" + word that makes the noun definite or is no adjective at all.
MIDDLE_DEFINITE = set('same other following above preceding remaining rest first second third last next former latter several various respective'.split())
IRREGULAR = {'men', 'women', 'children', 'townsmen', 'tradesmen', 'noblemen',
             'gentlemen', 'craftsmen', 'peasantry', 'people'}
# Words ending in s that are not plural nouns, and common function words.
NOT_PLURAL = set('''this his its was has does always perhaps thus whereas
across besides towards afterwards less unless various previous famous
numerous ridiculous serious obvious previous nervous gracious business
witness address process access success progress press mass class glass
dress loss cross boss chaos focus bonus status census consensus campus
virus bias atlas canvas series species lens news analysis basis crisis
emphasis hypothesis synthesis thesis diagnosis oasis axis tennis pass
paris francois nicolas jacques charles louis james thomas lucas andreas
carolus heinrichs honrichs hohenlohes following remaining existing
missing outstanding surviving incoming outgoing during evening morning
spring king ring thing wing string ceiling building wedding meeting
clothing painting mining feeling being nothing something everything'''.split())
MIDDLE_SKIP = set('''of in to for and or on at by from with as that which who
was were is are be been had has have not no all any each every both only
also then there here same other such own very more most less'''.split())


def stem(w):
    w = w.lower()
    for suf in ('ies', 'es', 's'):
        if len(w) > 4 and w.endswith(suf):
            return w[:-len(suf)] if suf != 'ies' else w[:-3] + 'y'
    return w


def is_plural_noun(w):
    if w in IRREGULAR:
        return True
    if w in NOT_PLURAL or len(w) < 5:
        return False
    if re.search(r'(ss|us|is|ous|ics|ing)$', w):
        return False
    return w.endswith('s')


def sentences(text):
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])["”)\]]?\s+(?=["“(\[]?[A-Z0-9])', text)
    out, buf = [], ''
    abbr = re.compile(r'(?:\b(?:St|Dr|Mr|Mrs|No|Nr|fol|ff|cf|p|pp|vol|ca|c|Rep|Bü|Gr|Tab|Rthl|Ms|Co|Jr|Sr)|\b[A-Z])\.$')
    for p in parts:
        buf = (buf + ' ' + p).strip() if buf else p
        if abbr.search(buf):
            continue
        out.append(buf)
        buf = ''
    if buf:
        out.append(buf)
    return out


def strip_md(s):
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\{%.*?%\}|\{\{.*?\}\}', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('*', '').replace('_', ' ')
    return s


def about_paragraphs(path):
    raw = open(path, encoding='utf-8').read()
    paras = []
    for blk in re.split(r'\n\s*\n', strip_md(raw)):
        blk = blk.strip()
        if not blk or blk.startswith(('#', '|', '---')):
            continue
        paras.append(re.sub(r'^\s*[-+] ', '', blk, flags=re.M))
    return paras


def load_yaml(path):
    try:
        return yaml.safe_load(open(path, encoding='utf-8')) or {}
    except Exception as e:  # unreadable file: say so, go on
        print(f'prose_lint: cannot read {path}: {e}', file=sys.stderr)
        return {}


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


def records(cats, unit):
    """Yield (category, source_file, key, text); one text = one unit of prose
    (R2's 'earlier in the same text' is within it)."""
    def want(c):
        return not cats or c in cats

    if want('holdings'):
        for d in sorted(glob.glob(os.path.join(ROOT, 'units', '*'))):
            slug = os.path.basename(d)
            if unit and slug != unit:
                continue
            p = os.path.join(d, 'about.md')
            if os.path.isfile(p):
                for i, para in enumerate(about_paragraphs(p), 1):
                    yield 'holdings', rel(p), f'{slug}:about#{i}', para
            y = os.path.join(d, 'unit.yml')
            if os.path.isfile(y):
                u = load_yaml(y)
                for f in ('title', 'card_title', 'full_title', 'short_title'):
                    if isinstance(u.get(f), str) and not u[f].upper().startswith('TODO'):
                        yield 'holdings', rel(y), f'{slug}:{f}', u[f]
    if want('summaries'):
        p = os.path.join(ROOT, 'site', '_data', 'summaries.yml')
        for pad, text in load_yaml(p).items():
            if unit and not str(pad).startswith(unit + '-'):
                continue
            if isinstance(text, str):
                yield 'summaries', rel(p), str(pad), text
    for cat, pat, fields in (
            ('literature', 'literature/*/work.yml',
             ('account_en', 'brief_en', 'summary_en', 'note_en')),
            ('newspapers', 'newspapers/*/item.yml',
             ('account_en', 'brief_en', 'summary_en'))):
        if not want(cat):
            continue
        for p in sorted(glob.glob(os.path.join(ROOT, pat))):
            slug = os.path.basename(os.path.dirname(p))
            if unit and slug != unit:
                continue
            w = load_yaml(p)
            for f in fields:
                if isinstance(w.get(f), str):
                    yield cat, rel(p), f'{slug}:{f}', w[f]
    if want('eras') and not unit:
        p = os.path.join(ROOT, 'reference', 'eras.yml')
        for slug, e in (load_yaml(p).get('eras') or {}).items():
            for f in ('intro_en', 'blurb_en', 'ownership_en'):
                if isinstance(e.get(f), str):
                    yield 'eras', rel(p), f'{slug}:{f}', e[f]
    if want('places') and not unit:
        for p in sorted(glob.glob(os.path.join(ROOT, 'places', '*', 'place.yml'))):
            slug = os.path.basename(os.path.dirname(p))
            w = load_yaml(p)
            for f in ('standfirst_en', 'intro_en'):
                if isinstance(w.get(f), str):
                    yield 'places', rel(p), f'{slug}:{f}', w[f]
    if want('people') and not unit:
        p = os.path.join(ROOT, 'reference', 'people_bios.yml')
        for slug, b in load_yaml(p).items():
            if isinstance(b, dict) and isinstance(b.get('bio'), str):
                yield 'people', rel(p), f'{slug}:bio', b['bio']
        p = os.path.join(ROOT, 'reference', 'genealogy.yml')
        for slug, b in (load_yaml(p).get('people') or {}).items():
            for f in ('bio', 'heading'):
                if isinstance(b, dict) and isinstance(b.get(f), str):
                    yield 'people', rel(p), f'{slug}:{f}', b[f]


def lint_text(text):
    """[(rule, sentence)] for one text."""
    hits = []
    sents = sentences(text)
    seen_before = ''          # the text up to the start of the current sentence
    offset = 0
    flat = re.sub(r'\s+', ' ', text).strip()
    for n, s in enumerate(sents):
        pos = flat.find(s[:40], offset)
        pos = offset if pos < 0 else pos
        before = flat[:pos].lower()
        offset = pos
        if R1.search(s):
            hits.append(('R1', s))
        if any(p.search(s) for p in R4_PATTERNS) or \
                (n == len(sents) - 1 and SIGNED.search(s)):
            hits.append(('R4', s))
        flagged = False
        for m in THE_NUM.finditer(s):
            noun = m.group(2)
            if stem(noun) not in re.sub(r'[^a-z ]', ' ', before + ' ' + s[:m.start()].lower()):
                flagged = True
        if not flagged:
            for m in THE_PLURAL.finditer(s):
                adj, noun = m.group(1), m.group(2)
                if adj and (adj in MIDDLE_SKIP or adj in MIDDLE_DEFINITE):
                    continue
                if adj and NUMWORD.match(adj):
                    continue                      # handled by THE_NUM
                if not is_plural_noun(noun):
                    continue
                if adj and adj.endswith('s'):     # "the Prince's"-style stems, "the rights"
                    continue
                earlier = re.sub(r'[^a-z ]', ' ', before + ' ' + s[:m.start()].lower())
                if stem(noun) in earlier:
                    continue
                flagged = True
                break
        if flagged and not any(h[0] == 'R2' for h in hits):
            hits.append(('R2', s))      # the first mention only: one per text
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--category', choices=CATEGORIES, action='append')
    ap.add_argument('--unit', help='a holding slug (or work/item slug)')
    ap.add_argument('--rule', choices=['R1', 'R2', 'R4'], action='append')
    ap.add_argument('--out', help='write the CSV here instead of stdout')
    a = ap.parse_args()

    rows = []
    for cat, src, key, text in records(a.category, a.unit):
        for rule, s in lint_text(text):
            if a.rule and rule not in a.rule:
                continue
            rows.append((rule, cat, src, key, s))
    f = open(a.out, 'w', encoding='utf-8', newline='') if a.out else \
        open(sys.stdout.fileno(), 'w', encoding='utf-8', newline='', closefd=False)
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['rule', 'category', 'source_file', 'key', 'sentence'])
    w.writerows(rows)
    f.flush()
    if a.out:
        f.close()
    c = collections.Counter((r[0], r[1]) for r in rows)
    print('hits: ' + str(len(rows)), file=sys.stderr)
    for (rule, cat), n in sorted(c.items()):
        print(f'  {rule} {cat}: {n}', file=sys.stderr)


if __name__ == '__main__':
    main()
