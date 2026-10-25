#!/usr/bin/env python3
# pipeline-check-file: a static mapping of the editor's place index to slugs; the
# place names it names are its data, read from reference/gazetteer/, not one
# holding's facts. See docs/GAZETTEER_PLAN.md.
"""Import the editor's place index into one YAML file per place.

Reads   reference/gazetteer/source/place_names_2026-10-23.md, a copy of the
        editor's "Place Names.md" (112 entries and 21 cross-references, with
        footnotes), and, to resolve the footnotes, reference/gazetteer_sources.yml,
        reference/maps.yml, units/kdw/intake/holding.py (which Kodeks number is
        which document), corpus/letters.json (document addresses and pages) and
        corpus/literature/ (which pages of a work exist).
Writes  reference/gazetteer/<slug>.yml for each of the 112 entries: the editor's
        text kept as written (only the export's escapes undone), and a first
        pass at the kind, location, names, map appearances and footnotes. Every
        point the importer could not settle is a string under `review:`.

Run once on 2026-10-23: this script is a record. After the import the YAML
files are edited by hand and are the authority. It refuses to overwrite an
existing <slug>.yml unless run with --force (which discards hand edits).

    python pipeline/gazetteer/import_place_names.py [--force]
"""
import glob
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'reference', 'gazetteer', 'source', 'place_names_2026-10-23.md')
OUT = os.path.join(ROOT, 'reference', 'gazetteer')

# heading -> (slug, register slug or None)
HEADINGS = {
    'Adamierz': ('adamierz', 'adamierz'), 'Anielewo': ('anielewo', None),
    'Augustynów': ('augustinow', 'augustinow'), 'Bartosz': ('bartosz', None),
    'Beźsług': ('bezslug', None), 'Bieganszczyzna, Osada': ('bieganszczyzna', None),
    'Biskupice': ('biskupice-karczma', None), 'Budy': ('budy', None),
    'Bukowe': ('bukowe', None), 'Chruściki': ('chrusciki', None),
    'Cygany': ('cygany', None), 'Czarna Struga': ('czarna-struga', None),
    'Czarnybród': ('czarnybrod', None), 'Czerwonka': ('czerwonka', None),
    'Długa Górka': ('dluga-gorka', None), 'Drzewce': ('drzewce', 'drzewce'),
    'Drzęzgi': ('drzezgi', None), 'Dziadolina': ('dziadolina', None),
    'Garbin': ('garbin', None), 'Glinianki': ('glinianki', None),
    'Grabina': ('grabina', None), 'Grądzeń': ('gradzyn', 'gradzyn'),
    'Grądzeń-Las': ('gradzen-las', None), 'Hagrowo': ('hagrowo', None),
    'Huta Trąbczyńska': ('huta-trabczynska', None), 'Huta Łukomska': ('huta-lukomska', None),
    'Imielanka': ('imielanka', None), 'Imielno': ('imielno', 'imielno'),
    'Jeziorko': ('jeziorko', None), 'Kirchol': ('kirchol', None),
    'Koczogowa': ('koczogowa', None), 'Kopojno': ('kopojno', 'kopojno'),
    'Kopojno-Parcele': ('kopojno-parcele', None), 'Kościołków': ('kosciolkow', None),
    'Koszelewska Łąka': ('koszelewska-laka', None), 'Kowaliska': ('kowaliska', None),
    'Królestwo': ('krolestwo', None), 'Kuzoi': ('kuzoi', None), 'Laski': ('laski', None),
    'Łazińskie Olędry': ('lazinskie-oledry', None), 'Łazy': ('lazy-trabczyn', 'lazy-trabczyn'),
    'Łomów': ('lomow', None), 'Łukom': ('lukom', 'lukom'),
    'Łukomskie Olędry': ('lukomskie-oledry', 'lukomskie-oledry'),
    'Lusnie Olędry': ('lusnie-oledry', None), 'Łutow': ('lutow', None), 'Maly': ('maly', None),
    'Małgorzatów': ('malgorzatow', None), 'Mały Las': ('ludwigslust', 'ludwigslust'),
    'Maradz': ('maradz', None), 'Maradz Olędry': ('maradz-oledry', None),
    'Mariantów': ('mariantow', 'mariantow'), 'Miąsykąt': ('miasykat', None),
    'Michalinów Oleśnicki': ('michalinow-olesnicki', 'michalinow-olesnicki'),
    'Michalinów Trąbczyński': ('michalinow-oledry', 'michalinow-oledry'),
    'Myszaków': ('myszakow', None), 'Myszakówek': ('myszakowek', None), 'Noga': ('noga', None),
    'Nowa Wieś': ('nowawies-trabczyn', 'nowawies-trabczyn'), 'Olchowo': ('olchowo', None),
    'Oleśnica': ('olesnica', 'olesnica'), 'Oleśnica-Folwark': ('olesnica-folwark', None),
    'Osiny': ('osiny', 'osiny'), 'Ostrowiec': ('ostrowiec', None), 'Podbiel': ('podbiel', None),
    'Porąbki': ('porabki', None), 'Posada': ('posada', None), 'Potaszniki': ('potaszniki', None),
    'Przybysław': ('przybyslaw', 'przybyslaw'), 'Przycierz': ('przycierz', None),
    'Pyzdry': ('pyzdry', 'pyzdry'), 'Rosciszewo': ('rosciszewo', None),
    'Rydlowa Góra': ('rydlowa-gora', None), 'Ryjew': ('ryjew', None),
    'Sadornicz': ('sadornicz', None), 'Sklanna Huta': ('sklanna-huta', None),
    'Skokum': ('skokum', 'skokum'), 'Skokamskie Olędry': ('skokamskie-oledry', None),
    'Smoleniec': ('smoleniec', None), 'Stanisławów': ('stanislawow', None),
    'Stawisko': ('stawisko', None), 'Studzianka': ('studzianka', None),
    'Szetlew': ('szetlew', 'szetlew'), 'Szetlewek': ('szetlewek', 'szetlewek'),
    'Tarczewo': ('tarczewo', None), 'Tarszewo': ('tarszewo', None),
    'Tarszew': ('tarszew-mlyn', None), 'Trąbczyn': ('trabczyn', 'trabczyn'),
    'Trąbczyn B': ('trabczyn-b', None), 'Trąbczyn C': ('trabczyn-c', None),
    'Trąbczyn D': ('trabczyn-d', None), 'Trąbczyn F': ('trabczyn-f', None),
    'Trąbczyn G': ('trabczyn-g', None), 'Trąbczyn Dworski': ('trabczyn-dworski', None),
    'Trąbczyńskie Nowe Olędry': ('trabczynskie-nowe-oledry', 'trabczynskie-nowe-oledry'),
    'Trąbczyńskie Stare Olędry': ('trabczynskie-stare-oledry', 'trabczynskie-stare-oledry'),
    'Trzcianne': ('trzcianne', None), 'Warta River': ('warta', None),
    'Wielki-Bór Obręb': ('wielki-bor-obreb', None), 'Wincentowo': ('wincentowo', None),
    'Włodzimirów': ('wlodzimirow', None), 'Włodzimirow Obręb': ('wlodzimirow-obreb', None),
    'Wrąbczyn': ('wrabczyn', 'wrabczyn'), 'Wrąbczyn Górski': ('wrabczyn-gorski', None),
    'Wrąbczynek': ('wrabczynek', 'wrabczynek'),
    'Wrąbczynkowskie Holendry': ('wrabczynkowskie-holendry', None),
    'Wygoda': ('wygoda', None), 'Wymysłów': ('wymyslow', None),
    'Zagórów': ('zagorowo', 'zagorowo'), 'Zagórowskie Olędry': ('zagorowskie-oledry', None),
    'Zalesie': ('zalesie', None), 'Zwierzyniec': ('zwierzyniec', None),
}

KINDS = [  # longest first
    ('Possibly a site of windmills', 'windmills'), ('Historical forest precinct', 'forest-precinct'),
    ('Olęder settlement', 'oleder-settlement'), ('Isolated dwellings', 'isolated-dwellings'),
    ('Stream or canal', 'stream'), ('Earthen mound', 'mound'), ('Eight mounds', 'mounds'),
    ('Unknown place', 'unknown'), ('Water mill', 'water-mill'), ('Settlement', 'settlement'),
    ('Village', 'village'), ('Hamlet', 'hamlet'), ('Town', 'town'), ('River', 'river'),
    ('Tavern', 'tavern'), ('Folwark', 'folwark'), ('Forest', 'forest'), ('Field', 'field'),
    ('Locale', 'locale'),
]
DIRS = 'northeast|northwest|southeast|southwest|north|south|east|west'
ABBR = {'Hol', 'Ger', 'Pl', 'pl', 'Kol', 'Dw', 'Ml', 'Fig', 'Tab', 'vol', 'No', 'Nos', 'ca', 'Kr'}

SENT = re.compile(r'\.(?:\[\^\d+\])*\s+(?=\S)')


def clean(s):
    s = re.sub(r'\\([\[\]\.#\-:()*_])', r'\1', s)
    s = re.sub(r'\bkm2\b', 'km²', s)
    return re.sub(r' {2,}', ' ', s).strip()


def norm(t):
    s = t.replace('*', '')
    for a, b in {'“': '"', '”': '"', '’': "'", '‘': "'", 'ﬁ': 'fi', 'ﬂ': 'fl'}.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def boundaries(text):
    """End offsets of sentences (a full stop not after an abbreviation)."""
    out = []
    for m in SENT.finditer(text):
        w = re.search(r'(\w+)$', text[:m.start()])
        word = w.group(1) if w else ''
        if word in ABBR or (len(word) == 1 and word.isupper()):
            continue
        nxt = text[m.end()]
        if nxt.islower():
            continue
        out.append(m.end())
    return out


def sentence_span(text, pos):
    b = [0] + boundaries(text) + [len(text)]
    for i in range(len(b) - 1):
        if b[i] <= pos < b[i + 1]:
            return b[i], b[i + 1]
    return 0, len(text)


def load_data():
    with open(os.path.join(ROOT, 'reference', 'gazetteer_sources.yml'), encoding='utf-8') as f:
        sources = yaml.safe_load(f)['sources']
    with open(os.path.join(ROOT, 'reference', 'maps.yml'), encoding='utf-8') as f:
        maps = yaml.safe_load(f)['maps']
    with open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8') as f:
        letters = json.load(f)
    docs = {d['uid']: (d['permalink'], [p['page_id'] for p in d['pages']]) for d in letters}
    kdw = {}
    with open(os.path.join(ROOT, 'units', 'kdw', 'intake', 'holding.py'), encoding='utf-8') as f:
        for line in f:
            m = re.match(r'\s*\((\d+), (\d+), (\d+), \[', line)
            if m:
                kdw[(int(m.group(2)), int(m.group(3)))] = int(m.group(1))
    return sources, maps, docs, kdw


class Resolver:
    def __init__(self, sources, docs, kdw):
        self.sources, self.docs, self.kdw = sources, docs, kdw

    def lit_link(self, work, page):
        if glob.glob(os.path.join(ROOT, 'corpus', 'literature', work, '%s.*.txt' % page)):
            return '/literature/%s/#p-%s' % (work, page)
        return None

    def doc_link(self, uid, page=None):
        if uid not in self.docs:
            return None
        link = self.docs[uid][0]
        return link + ('#p%s' % page if page else '')

    def make_ref(self, key, loc, vol=None, review=None):
        """One ref for source key and raw locator; returns the ref dict."""
        src = self.sources[key]
        rt = src['resolve']
        link, locator = None, loc
        if rt == 'kdw':
            n = int(loc)
            locator = 'vol. %s, no. %s' % (vol, n)
            doc = self.kdw.get((int(vol), n))
            if doc is not None:
                link = self.doc_link('kdw-%d' % doc)
            else:
                ow = src.get('other_witnesses', {}).get('%s/%s' % (vol, n))
                if ow:
                    link = self.doc_link(ow['document'], ow['page'])
        elif rt == 'leaves':
            first = loc.split('-')[0]
            m = re.match(r'(\d+)(v?)$', first)
            if m:
                num = int(m.group(1)) + (1 if m.group(2) else 0)
                pid = '%04d_%s' % (num, 'a1' if m.group(2) else 'a2')
                uid = src['document']
                if uid in self.docs and pid in self.docs[uid][1]:
                    link = self.docs[uid][0] + '#p%d' % (self.docs[uid][1].index(pid) + 1)
            if link is None and review is not None:
                review.append('link: leaf %s of %s not found among the document\'s pages' % (loc, key))
        elif rt == 'table':
            t = src['table'].get(loc)
            if t:
                link = self.doc_link(t['document'], t.get('page'))
            elif review is not None:
                review.append('link: locator %s is not in the table of %s' % (loc, key))
        elif rt == 'document':
            link = self.doc_link(src['document'])
            if loc:
                locator = loc
        elif rt == 'literature':
            locator = 'p. %s' % loc
            link = self.lit_link(src['work'], loc)
            if link is None and review is not None:
                review.append('link: page %s of %s is not in corpus/literature' % (loc, src['work']))
        elif rt == 'work':
            link = '/literature/%s/' % src['work']
            locator = ('p. %s' % loc) if loc else None
        elif rt == 'glossary':
            link = '/glossary/#%s' % src['glossary']
            locator = ('p. %s' % loc) if loc else None
        elif rt == 'url':
            link = src['url']
            locator = None
        return {'source': key, 'locator': locator, 'link': link,
                'status': 'linked' if link else 'missing'}


KDW_RE = re.compile(r'^(Zakrzewski|Piekosiński|Gąsiorowski and [A-ZŁ]\w+),?\s*(?:vol\.\s*(\d+),?\s*)?(No.*)$')
KDW_NUM = re.compile(r'No[s]?[.,]?\s*(\d+(?:\s*(?:,|&)\s*\d+)*)\.?\s*(.*)$')
PARAFJA = [
    ('Parafja Trąbczyn (Słupca): Akta Małżeństw 1776-1793 -- Akta Urodzeń 1784-1797', 'trabczyn-marriages-births-1776-1797'),
    ('Parafja Trąbczyn (Słupca): Akta Urodzeń 1691-1762; 1764-1784; 1762-1764', 'trabczyn-births-1691-1784'),
    ('Parafja Trąbczyn (Słupca): Akta Urodzeń, Małżeństw, Zgonów 1826', 'trabczyn-1826'),
    ('Parafja Trąbczyn (Słupca): Akta Małżeństw 1597-1775', 'trabczyn-marriages-1597-1775'),
    ('Parafja Trąbczyn (Słupca): Akta Urodzeń 1808-1825', 'trabczyn-births-1808-1825'),
    ('Parafja Zagórów (Słupca): Akta Urodzeń 1915-1921', 'zagorow-lutheran-births-1915-1921'),
]
REL_RE = re.compile(r'Relationes-oblatae \[protocollon\][,"\s]*1776,\s*(\d+v?(?:-\d+v?)?)')


def parse_footnote(n, t, prev, R):
    """-> dict(refs, note, review, state). `prev` is the previous footnote's
    state (source key, volume) or None."""
    s = norm(t)
    review = []
    note = None
    refs = []
    vol = None
    src = None

    def kdw_refs(key, volume, tail_t):
        m = KDW_NUM.match(tail_t)
        if not m:
            return None
        nums = re.findall(r'\d+', m.group(1))
        return [R.make_ref(key, x, volume, review) for x in nums], (m.group(2) or None)

    if s.startswith('Ibid'):
        rest = t[4:].strip()
        if prev is None:
            review.append('footnote: n=%d is "Ibid" with nothing before it' % n)
            return dict(refs=[], note=None, review=review, state=None)
        key, vol = prev['source'], prev['vol']
        if not rest:
            refs = [dict(r) for r in prev['refs']]
        elif R.sources[key]['resolve'] == 'kdw':
            got = kdw_refs(key, vol, rest)
            if got is None:
                review.append('footnote: n=%d "%s" not understood' % (n, t))
            else:
                refs, note = got
        else:
            loc = rest.rstrip('.').strip()
            refs = [R.make_ref(key, loc, None, review)]
        src = key
    else:
        m = KDW_RE.match(t)
        mrel = REL_RE.search(s)
        if m:
            key = 'kdw'
            vol = 5 if m.group(1) == 'Piekosiński' else m.group(2)
            if vol is None:
                review.append('footnote: n=%d has no volume' % n)
            else:
                got = kdw_refs(key, vol, m.group(3))
                if got:
                    refs, note = got
                    src = key
        elif (m2 := re.match(r'^Klasztor cystersów w Lądzie (\S+)$', s)):
            src = 'lad-copybook'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif mrel:
            src = 'konin-gr145'
            refs = [R.make_ref(src, mrel.group(1), None, review)]
            mq = re.match(r'^(“[^”]+”)', t)
            if mq:
                note = mq.group(1)
        elif (m2 := re.match(r'^"?Relationes \[protocollon\][,"\s]*1786,\s*(.+)$', s)):
            src = 'konin-gr120'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif (m2 := re.match(r'^"?Relationes, citationes \[protocollon\] 1726-1727[,"\s]*1727,\s*(.+)$', s)):
            src = 'kalisz-1727'
            refs = [R.make_ref(src, 'p. ' + m2.group(1), None, review)]
        elif (m2 := re.match(r'^Inscriptiones, relationes, decreta \[inducta\] 1589 \(53/6/0/-/17\),\s*(.+)$', s)):
            src = 'courtbook-1589'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif s.lstrip('"').startswith('[Odpis dokumentów'):
            src = 'app539680801'
            m2 = re.search(r'",\s*([\d-]+)$', s)
            refs = [R.make_ref(src, m2.group(1) if m2 else None, None, review)]
        elif s.startswith('Breyer, "Grodziec'):
            src = 'breyer-grodziec'
            refs = [R.make_ref(src, None, None, review)]
        elif (m2 := re.match(r'^Breyer, "Deutsche Gaue in Mittelpolen," (\d+)$', s)):
            src = 'breyer1935gaue'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif (m2 := re.match(r'^Chodyła (\d+)\.?\s*(.*)$', s)):
            src = 'chodyla2015'
            refs = [R.make_ref(src, m2.group(1), None, review)]
            if m2.group(2).startswith('Also see Poznań State Archives unit 53/67/0/-/1'):
                refs.append(R.make_ref('app536701', 'unit 53/67/0/-/1', None, review))
            elif m2.group(2):
                note = m2.group(2)
        elif (m2 := re.match(r'^Szwiec (\d+)$', s)):
            src = 'szwiec2009'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif (m2 := re.match(r'^Słowiński and Połom (\d+)$', s)):
            src = 'slowinskipolom2024'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif s.startswith('Minakowska, "Helena Zielonacka"'):
            src = 'minakowska-zielonacka'
            refs = [R.make_ref(src, None, None, review)]
        elif (m2 := re.match(r'^Arct, "Stawisko," (\d+)$', s)):
            src = 'arct'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif s == 'Jehke':
            src = 'jehke'
            refs = [R.make_ref(src, None, None, review)]
        elif s.startswith('Wikimapia,'):
            src = 'wikimapia-szetlewek'
            refs = [R.make_ref(src, None, None, review)]
        elif (m2 := re.match(r'^Archiwum Arcybiskupów Gnieźnieńskich (\S+)$', s)):
            src = 'visitation-1791'
            refs = [R.make_ref(src, m2.group(1), None, review)]
            review.append('footnote: n=%d archive name differs from the edition (ADWł 85)' % n)
        elif (m2 := re.match(r'^"Die neuesten topografischen Nachrichten von Südpreussen," (\d+)$', s)):
            src = 'agad1745'
            refs = [R.make_ref(src, m2.group(1), None, review)]
        elif (m2 := re.match(r'^Perthées, "Geograficzno statystyczne opisanie parafiów Królestwa Polskiego w roku 1796," (\d+) \(Image (\d+)\)$', s)):
            src = 'perthees1796'
            refs = [R.make_ref(src, 'p. %s (image %s)' % (m2.group(1), m2.group(2)), None, review)]
        elif (m2 := re.match(r'^"([^"]+)" ([\d-]+)$', s)) and m2.group(1) in (
                'Trąbczyn', 'Łukom', 'Dziadolina', 'Garbin', 'Noga', 'Siergiejewo', 'Pietrzyków'):
            src = 'slownik'
            pg = m2.group(2)
            refs = [R.make_ref(src, '"%s", %s %s' % (m2.group(1), 'pp.' if '-' in pg else 'p.', pg), None, review)]
        else:
            for title, key in PARAFJA:
                if s.startswith(title):
                    rest = s[len(title):].strip()
                    rest = re.sub(r'^,\s*\d{4},\s*', '', rest)
                    src = key
                    refs = [R.make_ref(key, rest, None, review)]
                    break
    if not refs:
        review.append('footnote: n=%d could not be mapped to a source: %s' % (n, t))
        refs = [{'source': None, 'locator': None, 'link': None, 'status': 'missing'}]
        return dict(refs=refs, note=note, review=review, state=None)
    return dict(refs=refs, note=note, review=review, state={'source': refs[0]['source'], 'vol': vol, 'refs': refs})


def main():
    force = '--force' in sys.argv
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sources, maps, docs, kdw = load_data()
    R = Resolver(sources, docs, kdw)
    with open(SRC, encoding='utf-8', newline='') as f:
        lines = f.read().replace('\r\n', '\n').split('\n')

    defs, entries, xrefs = {}, [], []
    for line in lines:
        if not line.strip():
            continue
        m = re.match(r'^\[\^(\d+)\]:\s+(.*)$', line)
        if m:
            defs[int(m.group(1))] = clean(m.group(2))
            continue
        if '—' not in line or not line.startswith('*'):
            print('UNPARSED LINE:', line[:80])
            continue
        head_raw, text = line.split('—', 1)
        if head_raw.count('*') % 2 == 1 and text.startswith('*'):
            text = text[1:]
        head = clean(head_raw.replace('*', ''))
        text = clean(text)
        status = 'extant' if head_raw.startswith('**') else 'historical'
        if text.startswith('See '):
            target = text[4:].replace('*', '').strip().rstrip('.').strip()
            xrefs.append((head, target))
        else:
            entries.append((head, status, text))
    print('entries %d, cross-references %d, footnote definitions %d' % (len(entries), len(xrefs), len(defs)))
    if len(entries) != 112 or len(xrefs) != 21:
        print('COUNT MISMATCH')
        return 2
    unmapped = [h for h, _, _ in entries if h not in HEADINGS]
    if unmapped:
        print('headings without a slug:', unmapped)
        return 2

    # heading lookup for locations: entries + cross-reference headings
    lookup = {h.casefold(): HEADINGS[h][0] for h, _, _ in entries}
    aliases_of = {}      # slug -> [alias headings]
    stray = []
    for h, target in xrefs:
        if target in HEADINGS:
            slug = HEADINGS[target][0]
            aliases_of.setdefault(slug, []).append(h)
            lookup.setdefault(h.casefold(), slug)
        else:
            stray.append((h, target))
            print('CROSS-REFERENCE WITH NO TARGET ENTRY: "%s" -> "%s"' % (h, target))

    def resolve(phrase):
        p = phrase.strip()
        p = re.sub(r'^the ', '', p)
        p = re.split(r',|\s+in\s+', p)[0]
        p = re.sub(r'\s*\([^)]*\)', '', p).strip()
        p = re.sub(r' estate$', '', p)
        return lookup.get(p.casefold())

    # footnotes in file order
    parsed, prev = {}, None
    for n in sorted(defs):
        r = parse_footnote(n, defs[n], prev, R)
        parsed[n] = r
        prev = r['state']

    existing = [HEADINGS[h][0] for h, _, _ in entries if os.path.exists(os.path.join(OUT, HEADINGS[h][0] + '.yml'))]
    if existing and not force:
        print('REFUSING to overwrite %d existing files (use --force): %s' % (len(existing), ', '.join(existing[:5])))
        return 1

    names_re = [
        re.compile(r'(?P<ph>\b(?:first mentioned as|mentioned as|known in metrical records as|originally named|previously known as|also known as|known as|referred to this place as))\s+(?P<forms>\*[^*]+\*(?:\s+and\s+\*[^*]+\*)*)', re.I),
        re.compile(r'(?P<ph>\b(?:mentioned|listed)\s[^*.;]{0,100}?\sas)\s+(?P<forms>\*[^*]+\*(?:\s+and\s+\*[^*]+\*)*)', re.I),
        re.compile(r'(?P<ph>\brenamed to)\s+(?:(?P<forms>\*[^*]+\*)|(?P<plain>[^*.;(]+?)(?=\s+in\s+\d{4}|\s+\(|\s+during|[.;,]|$))', re.I),
    ]

    def year_of(sentence):
        m = re.search(r'\bca\. (\d{4}-\d{4})', sentence)
        if m:
            return m.group(1)
        s2 = re.sub(r'\(\d{4}-\d{4}\)', '', sentence)
        m = re.search(r'\b(1\d{3})\b', s2)
        return int(m.group(1)) if m else None

    written = 0
    stats = {'fn': 0, 'maps': 0, 'review': 0}
    for head, status, text in entries:
        slug, register = HEADINGS[head]
        review = []
        # kind
        kind = kind_text = None
        rest = text
        for pref, k in KINDS:
            if text.startswith(pref) and (len(text) == len(pref) or not text[len(pref)].isalpha()):
                kind, kind_text, rest = k, pref, text[len(pref):].strip()
                break
        sents = boundaries(text)
        first_end = sents[0] if sents else len(text)
        if kind is None:
            review.append('kind: no kind word in the entry (it begins "%s")' % text[:first_end].strip())
            rest = text
        fs = rest
        # first sentence of the rest
        b = boundaries(rest)
        fs = rest[:b[0]] if b else rest
        fs = re.sub(r'(\[\^\d+\])+', '', fs).strip().rstrip('.').strip()
        loc_text = fs
        if kind is None:
            if fs.lower().startswith('location unknown'):
                loc_text = ''
            else:
                loc_text = fs[:1].lower() + fs[1:]
        elif re.match(r'^(?:which|that) bordered ', fs):
            loc_text = 'bordered ' + re.sub(r'^(?:which|that) bordered ', '', fs)
        else:
            loc_text = re.sub(r'^(?:(?:which|that) existed|located)\s*', '', fs)
        head_two = text[:(sents[1] if len(sents) > 1 else len(text))]
        precision = 'unknown' if re.search(r'location unknown|unknown location|unknown place', head_two, re.I) else 'described'
        if re.fullmatch(r'(?:with an )?unknown(?: location)?', loc_text, re.I) or loc_text == '':
            loc_text = ''
        relation = relative_to = belongs_to = None
        lt = loc_text
        d = DIRS
        m = None
        if (m := re.match(r'^(?:in|on) the (%s) (?:edge|corner|part) of (.+)$' % d, lt)):
            relation, ph = 'in', m.group(2)
            relative_to = resolve(ph)
        elif (m := re.match(r'^(%s) of and belonging to (.+)$' % d, lt)):
            relation = m.group(1) + '-of'
            belongs_to = relative_to = resolve(m.group(2))
            if relative_to is None:
                review.append('location: "%s" is no entry of the gazetteer' % m.group(2))
        elif (m := re.match(r'^(%s) and (%s) of (.+)$' % (d, d), lt)):
            relation = None
            relative_to = resolve(m.group(3))
            review.append('location: two directions ("%s and %s of %s"), relation left null' % (m.group(1), m.group(2), m.group(3)))
        elif (m := re.match(r'^(%s) of (.+)$' % d, lt)):
            relation = m.group(1) + '-of'
            relative_to = resolve(m.group(2))
            if relative_to is None:
                review.append('location: "%s" is no entry of the gazetteer' % m.group(2))
        elif (m := re.match(r'^near (.+)$', lt)):
            relation = 'near'
            relative_to = resolve(m.group(1))
        elif (m := re.match(r'^between (.+?) and (.+)$', lt)):
            relation = 'between'
            review.append('location: between "%s" and "%s": relative_to left null' % (m.group(1), m.group(2)))
        elif (m := re.match(r'^in .+? (%s) of (.+)$' % d, lt)):
            relation = m.group(1) + '-of'
            relative_to = resolve(m.group(2))
        elif (m := re.match(r'^bordered the southern part of (.+)$', lt)):
            relation = 'near'
            relative_to = resolve(m.group(1))
            review.append('location: "bordered the southern part of" read as near')
        elif lt and kind not in ('river', 'stream'):
            review.append('location: relation not parsed from "%s"' % lt)
        if relation in ('in',) and relative_to is None:
            review.append('location: "%s" not resolved' % lt)
        # text for the YAML: keep editor's words
        location = {'text': loc_text or None, 'relation': relation, 'relative_to': relative_to,
                    'belongs_to': belongs_to, 'precision': precision, 'lat': None, 'lon': None}

        # footnotes
        fn_ns = []
        for x in re.findall(r'\[\^(\d+)\]', text):
            if int(x) not in fn_ns:
                fn_ns.append(int(x))
        footnotes = []
        for fnn in fn_ns:
            if fnn not in parsed:
                review.append('footnote: n=%d has no definition' % fnn)
                footnotes.append({'n': fnn, 'text': None, 'refs': [], 'note': None})
                continue
            p = parsed[fnn]
            for rv in p['review']:
                if rv not in review:
                    review.append(rv)
            footnotes.append({'n': fnn, 'text': defs[fnn], 'refs': p['refs'], 'note': p['note']})
        stats['fn'] += len(footnotes)

        # maps
        occ = []
        for mk, mv in maps.items():
            cited = mv['cited_as']
            for mm in re.finditer(re.escape(cited), text):
                if mm.start() > 0 and text[mm.start() - 1].isalpha():
                    continue
                occ.append((mm.start(), mk))
        occ.sort()
        bset = sorted(set(boundaries(text)) | {i + 1 for i, c in enumerate(text) if c == ';'})
        map_items = []
        for pos, mk in occ:
            cs = max([x for x in bset if x <= pos] or [0])
            clause = text[cs:pos]
            # a ';' or '. ' may sit inside the parentheses that hold the map: keep from clause start
            forms = re.findall(r'\*([^*]+)\*', clause)
            form = forms[0] if forms else None
            if len(forms) > 1:
                review.append('maps: more than one italic form in the clause of %s (%s)' % (maps[mk]['cited_as'], '; '.join(forms)))
            rem = re.sub(r'\*[^*]+\*', ' ', clause)
            rem = re.sub(r'(\[\^\d+\])+', '', rem)
            rem = re.sub(r'\(\s*$', '', rem.strip())
            rem = re.sub(r'[\s,(;]+$', '', rem)
            rem = re.sub(r'^\s*[,;(]+\s*', '', rem)
            rem = re.sub(r'\(\s*,?\s*$', '', rem).strip()
            rem = re.sub(r'\s{2,}', ' ', rem)
            if not re.search(r'\w{2,}', rem):
                rem = ''
            if form is None:
                after_end = min([x for x in bset if x > pos] or [len(text)])
                if '*' in text[pos:after_end]:
                    review.append('maps: the italic form of %s follows the map name in its sentence' % maps[mk]['cited_as'])
            map_items.append({'map': mk, 'form': form, 'note': rem or None})
        stats['maps'] += len(map_items)

        for fm in re.findall(r'Fig\. \d+|Map \d+, Tab\. \d+', text):
            review.append("figure: refers to a figure of the editor's book: %s" % fm)

        # names
        names = [{'form': head, 'year': None, 'note': 'heading', 'footnote': None}]
        for a in aliases_of.get(slug, []):
            forms = [a]
            if a.endswith(', Kolonia'):
                base = a[:-len(', Kolonia')]
                forms = ['Kolonia ' + x for x in base.split('/')]
            else:
                forms = a.split('/')
            for fm in forms:
                names.append({'form': fm, 'year': None, 'note': 'cross-reference', 'footnote': None})
        seen = set()
        found = []
        for rx in names_re:
            for mm in rx.finditer(text):
                fkey = mm.start('forms') if mm.group('forms') else mm.start('plain')
                if fkey in seen:
                    continue
                seen.add(fkey)
                found.append((fkey, rx, mm))
        found.sort(key=lambda z: z[0])
        for _, rx, mm in found:
            ss, se = sentence_span(text, mm.start())
            sent = text[ss:se]
            fnm = re.search(r'\[\^(\d+)\]', sent)
            yr = year_of(sent)
            ph = mm.group('ph')
            if rx is names_re[1]:
                ph = 'mentioned … as'
            if mm.group('forms'):
                fl = re.findall(r'\*([^*]+)\*', mm.group('forms'))
            else:
                fl = [mm.group('plain').strip()]
            for fm in fl:
                names.append({'form': fm, 'year': yr, 'note': ph, 'footnote': int(fnm.group(1)) if fnm else None})

        doc = {
            'slug': slug, 'heading': head, 'register': register, 'status': status,
            'kind': kind, 'kind_text': kind_text, 'location': location,
            'text_en': text, 'names': names, 'aliases': aliases_of.get(slug, []),
            'maps': map_items, 'footnotes': footnotes, 'review': review,
        }
        stats['review'] += len(review)
        header = ('# Imported 2026-10-23 from the editor\'s "Place Names.md" (reference/gazetteer/source/)\n'
                  '# by pipeline/gazetteer/import_place_names.py; edited by hand from here on.\n'
                  '# Plan: docs/GAZETTEER_PLAN.md.\n')
        body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)
        with open(os.path.join(OUT, slug + '.yml'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(header + body)
        written += 1
    print('written %d files; footnotes %d, map appearances %d, review notes %d' % (written, stats['fn'], stats['maps'], stats['review']))
    if stray:
        print('Cross-references with no target (kept nowhere else; for the review list):')
        for h, t in stray:
            print('  *%s* -> See %s' % (h, t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
