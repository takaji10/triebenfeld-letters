# -*- coding: utf-8 -*-
"""
The unit registry.

One archival unit = one directory under units/, holding its transcription
(corpus.txt), its editorial rulings (rulings.yml) and its provenance (unit.yml,
notes.md). Everything else in the project is either shared reference data or
generated output.

Identifiers. The archive's own document number stays the letter_id and is only
unique within its unit, so three fields carry the namespace:

    unit       oe1bu9454
    letter_id  48                        the archival number, untouched
    uid        oe1bu9454-48              flat global handle
    pad        oe1bu9454-048             sorts correctly; filenames, data keys
    permalink  /documents/oe1bu9454/48/  what the reader sees

Keeping letter_id bare is deliberate: every editorial ruling in rulings.yml is
keyed by it, so those files never have to be re-keyed when a unit is added.
"""
import csv
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
UNITS_DIR = os.path.join(ROOT, 'units')

# The URL space documents live in. Was '/letters/' while the edition held
# only correspondence; a volume of title deeds is not a letter.
DOC_URL_PREFIX = '/documents'


class Unit(dict):
    """A unit.yml, plus resolved paths. Attribute access for the common fields."""

    @property
    def slug(self):
        return self['slug']

    @property
    def dir(self):
        return os.path.join(UNITS_DIR, self['slug'])

    @property
    def corpus_path(self):
        return os.path.join(self.dir, self.get('corpus', 'corpus.txt'))

    @property
    def rulings_path(self):
        return os.path.join(self.dir, 'rulings.yml')

    @property
    def ascii_prefix(self):
        return self.get('scans', {}).get('ascii_prefix', self['slug'])

    @property
    def raw_dir(self):
        return self.get('scans', {}).get('raw_dir', '')

    @property
    def raw_glob(self):
        return self.get('scans', {}).get('raw_glob', '*.jpg')

    # -- transcriptions that arrived matched to the scans -------------------
    # A unit whose source came as one text file per page declares where those
    # files are, so import_pages.py can write the pairing into corpus.txt as
    # [PAGE ...] markers instead of it having to be inferred afterwards.

    @property
    def transcriptions_dir(self):
        return self.get('transcriptions', {}).get('dir', '')

    @property
    def transcriptions_glob(self):
        return self.get('transcriptions', {}).get('glob', '*.txt')

    @property
    def page_id_strip(self):
        """Text to cut out of a transcription filename to leave the page id."""
        return self.get('transcriptions', {}).get('page_id_strip', '')

    def read_corpus(self):
        """The transcription, split into lines. Read-only input, never rewritten."""
        with open(self.corpus_path, encoding='utf-8') as f:
            return f.read().split('\n')

    # -- identifiers -------------------------------------------------------

    def uid(self, letter_id):
        return f'{self.slug}-{letter_id}'

    def pad(self, letter_id):
        """oe1bu9454-048, oe1bu9454-072a - sorts correctly as a filename."""
        m = re.match(r'(\d+)([a-z]*)$', str(letter_id))
        return f'{self.slug}-{int(m.group(1)):03d}{m.group(2)}'

    def permalink(self, letter_id):
        # The single generator. Everything downstream bakes this in -
        # letters.json, letters.csv, corpus/index/, the corpus text headers -
        # so changing it needs a full regenerate.py, not --unit.
        return f'{DOC_URL_PREFIX}/{self.slug}/{letter_id}/'


def slugify(ref):
    """'Oe 1 Bü 9454' -> 'oe1bu9454'. ASCII, lowercase, separators dropped."""
    s = ref.lower()
    for a, b in (('ä', 'a'), ('ö', 'o'), ('ü', 'u'), ('ß', 'ss')):
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]', '', s)


def load_units(slug=None):
    """Every unit, in directory order. With slug, just that one."""
    if not os.path.isdir(UNITS_DIR):
        raise SystemExit(f'no units/ directory at {UNITS_DIR}')
    units = []
    for name in sorted(os.listdir(UNITS_DIR)):
        path = os.path.join(UNITS_DIR, name, 'unit.yml')
        if not os.path.isfile(path):
            continue
        with open(path, encoding='utf-8') as f:
            u = Unit(yaml.safe_load(f) or {})
        if u.get('slug') != name:
            raise SystemExit(f'{path}: slug {u.get("slug")!r} != directory {name!r}')
        units.append(u)
    if slug is not None:
        units = [u for u in units if u.slug == slug]
        if not units:
            have = ', '.join(sorted(os.listdir(UNITS_DIR))) or 'none'
            raise SystemExit(f'no unit {slug!r} under units/ (have: {have})')
    if not units:
        raise SystemExit('units/ holds no unit.yml')
    return units


def one_unit(slug=None):
    """The single unit to act on. Errors if ambiguous, so nothing runs on the wrong one."""
    units = load_units(slug)
    if len(units) > 1:
        raise SystemExit('several units present; pass --unit <slug>: '
                         + ', '.join(u.slug for u in units))
    return units[0]


def unit_arg(argv=None):
    """Read --unit <slug> from argv without disturbing a script's own parser."""
    argv = sys.argv if argv is None else argv
    if '--unit' in argv:
        i = argv.index('--unit')
        if i + 1 < len(argv):
            return argv[i + 1]
        raise SystemExit('--unit needs a slug')
    return None


def utf8_stdout():
    """Windows consoles default to cp1252 and choke on the corpus."""
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_places_authority():
    """reference/places.yml, whole - {places: {slug: record}, reject: [...]}.

    The place authority used to be a flat variant -> spelling map, which could
    say nothing about a place beyond how it was spelled: not that Wrąbczyn is a
    different village from Trąbczyn, not which document a variant was seen in,
    and not how to find the place in the body of a document rather than on a
    dateline. places.yml carries all of that; the flat map below is derived
    from it so every existing caller is unaffected.
    """
    path = os.path.join(ROOT, 'reference', 'places.yml')
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def variant_records(entry):
    """[{form, match, canon, seen_in}] for one entity - a person or a place.

    A variant may be a bare string - the common case, meaning "fold this into
    the entity" - or a mapping. Two independent flags, because they answer two
    different questions:

      match   should this spelling FIND the entity? `false` records a form as
              provenance without asserting it is this entity, which is how an
              unsettled reading is documented rather than silently resolved.
      canon   should the English translation be told to render this spelling as
              the entity's canonical form? `false` for a form that identifies
              the entity without being a misspelling of it - a bare given name,
              an honorific the writers abbreviate, or a spelling that is more
              correct than the one this edition happens to print.
    """
    out = []
    for v in (entry.get('variants') or []):
        if isinstance(v, str):
            v = {'form': v}
        if not isinstance(v, dict) or not (v.get('form') or ''):
            continue
        out.append({'form': v['form'],
                    'match': bool(v.get('match', True)),
                    'canon': bool(v.get('canon', True)),
                    'seen_in': v.get('seen_in') or []})
    return out


def entity_variants(entry):
    """[(form, matched)] - the projection of variant_records() most callers want."""
    return [(v['form'], v['match']) for v in variant_records(entry)]


def load_place_canon():
    """The shared place-name canon, variant (lowercased) -> the edition's form.

    Standalone because it is not a unit's ruling: build_site_data needs it for
    tagging, with no unit in hand. It used to keep a second, much smaller copy
    of its own, so a place normalised on the dateline was not necessarily
    normalised where it was tagged.

    Now derived from reference/places.yml, so adding a variant there both
    normalises the dateline and finds the place in the text. A variant marked
    `match: false` is deliberately absent: it is recorded, not resolved.
    """
    canon = {}
    for slug, e in (load_places_authority().get('places') or {}).items():
        display = e.get('display') or slug
        for form, matched in entity_variants(e):
            if matched:
                canon[form.lower()] = display
    return canon


def load_rulings(unit):
    """The unit's editorial decisions, plus the place canon shared by all units.

    Names match the constants build_db.py used to carry inline, so the loading
    is the only thing that changed.
    """
    with open(unit.rulings_path, encoding='utf-8') as f:
        r = yaml.safe_load(f) or {}
    c = load_places_authority()

    places = r.get('places') or {}
    dates = r.get('dates') or {}
    docs = r.get('documents') or {}
    damage = r.get('damage') or {}

    def tuples(d):
        return {k: tuple(v) for k, v in (d or {}).items()}

    return {
        'PLACE_CANON':    load_place_canon(),
        'PLACE_REJECT':   set(c.get('reject') or []),
        'PLACE_OVERRIDE': places.get('overrides') or {},
        'SUPPLIED':       tuples(dates.get('supplied')),
        'TWIN':           tuples(dates.get('twin')),
        'INFERRED':       tuples(dates.get('inferred')),
        'NO_DATE':        set(dates.get('no_date') or []),
        'DOC_TYPE':       docs.get('doc_type') or {},
        # Era and themes. Both are EDITORIAL ASSIGNMENTS and neither is derived
        # from a date: 196 of 348 documents fall outside their era's nominal
        # ownership years, because the dispute outlived the possession. The era
        # default lives in unit.yml, so a holding assigns itself in one line and
        # this table carries only the exceptions.
        'DOC_ERA':        docs.get('era') or {},
        'DOC_THEMES':     docs.get('themes') or {},
        # Language, where the document is not in the German of the rest of the
        # holding. Recorded per document because it is a property of the
        # document, and a queryable one: this volume holds a Polish protocol
        # and a Latin-and-Polish chapter instrument.
        'DOC_LANGUAGE':   docs.get('language') or {},
        # Dates the editor read off the document's own dateline, recorded here
        # only because the parser cannot reach them - a different fact from a
        # date supplied by a researcher, and labelled differently to the reader.
        'DATE_READ':      tuples(dates.get('read')),
        'DUP_OF':         docs.get('duplicate_of') or {},
        'SPLIT_NOTE':     docs.get('split_note') or {},
        # Typed links between documents in this holding: which decree confirms
        # which instrument, which contract supersedes which. Each entry is
        # {kind, target, note}; target is a document number in the same unit.
        'RELATIONS':      docs.get('relations') or {},
        'DAMAGE_LETTERS': set(damage.get('letters') or []),
    }


def require_fresh_corpus(*extra):
    """Refuse to spend money on German that is no longer the transcription.

    The transcription is authored in units/<slug>/corpus.txt; everything that
    costs money reads corpus/letters.json, which regenerate.py derives from it.
    Apply a correction and translate without rebuilding in between and the model
    is handed the superseded text, pays for it, and caches the result as though
    it were finished work. That happened: letter 73 was translated twice from a
    reading the editor had already overturned, and nothing objected either time.

    Compared by modification time, which is crude but has no false negatives
    that matter: rebuilding when nothing changed is free, and the failure this
    guards against costs a batch.
    """
    generated = os.path.join(ROOT, 'corpus', 'letters.json')
    if not os.path.isfile(generated):
        sys.exit('corpus/letters.json is missing. Run: python regenerate.py')
    built = os.path.getmtime(generated)
    sources = [os.path.join(u.dir, 'corpus.txt') for u in load_units()]
    sources += [os.path.join(u.dir, 'rulings.yml') for u in load_units()]
    sources += list(extra)
    newer = sorted(os.path.relpath(p, ROOT).replace(os.sep, '/')
                   for p in sources
                   if os.path.isfile(p) and os.path.getmtime(p) > built)
    if newer:
        sys.exit('corpus/letters.json is older than what it is built from:\n'
                 + '\n'.join('  ' + p for p in newer)
                 + '\nTranslating now would pay for superseded text.'
                   '\nRun: python regenerate.py')


def load_documents(root=None):
    """Every document, read from the per-document files.

    corpus/documents/<uid>.json is the primary form: one file per document, so
    a reader can take the few it needs. This assembles the whole set for the
    callers that genuinely want it - the site builder and the verifier, both of
    which walk every document once.

    corpus/letters.json holds the same content as a single array. It is an
    intermediate - build_dataset.py reads it and writes the per-document files -
    and it is kept because tools outside this pipeline read it. Neither form is
    canonical: units/<slug>/corpus.txt is, and both are rebuilt from it.
    """
    root = root or ROOT
    index = os.path.join(root, 'corpus', 'index', 'documents.json')
    docs_dir = os.path.join(root, 'corpus', 'documents')
    if not os.path.isfile(index):
        # The dataset has not been built yet in this run; fall back so a
        # half-built tree still works rather than failing obscurely.
        legacy = os.path.join(root, 'corpus', 'letters.json')
        with open(legacy, encoding='utf-8') as f:
            return json.load(f)
    with open(index, encoding='utf-8') as f:
        manifest = json.load(f)
    out = []
    for row in manifest:
        with open(os.path.join(docs_dir, row['uid'] + '.json'), encoding='utf-8') as f:
            out.append(json.load(f))
    return out


def records_by_pad(root=None, unit=None):
    """Every document, keyed by pad - the one address that carries its holding.

    The archive's own number is unique only inside its holding, and both units
    have a document 2. Keying on it made check_translations.py check every deed
    against the letter of the same number, and summarise.py pair one holding's
    English with another's record. Both bugs were written independently, in the
    same shape, because each script built its own dictionary.

    So there is one dictionary and this is it. `pad` is what the cache files,
    the published translations and the summaries are named by, so a file's own
    name is enough to find its record:

        recs = unitlib.records_by_pad()
        rec = recs.get(os.path.splitext(filename)[0])
    """
    root = root or ROOT
    with open(os.path.join(root, 'corpus', 'letters.json'), encoding='utf-8') as f:
        recs = json.load(f)
    return {r['pad']: r for r in recs
            if unit is None or r.get('unit') == unit}


PAD_RE = re.compile(r'^([a-z0-9]+)-\d+[a-z]*(?:\.|$)')


def pad_unit(filename):
    """'oe1bu9454-048.yml' -> 'oe1bu9454'. '' if the name is not a pad."""
    m = PAD_RE.match(os.path.basename(filename))
    return m.group(1) if m else ''


def scope_to_unit(names, slug):
    """Keep only the pad-named files belonging to one unit.

    The translation cache and the published translations are one flat directory
    for the whole project, keyed by pad - and pad carries the unit. So scoping a
    run is a filename test, and a file whose name is not a pad is left in:
    dropping it silently would hide state the caller may need.
    """
    if not slug:
        return list(names)
    return [n for n in names if pad_unit(n) in ('', slug)]


def resolve_unit(slug):
    """The unit to act on, honouring --unit and erroring when it is ambiguous.

    For the translation scripts, which declared --unit in their help and then
    ignored it: several of them cost money per run, so processing every holding
    because a flag was forgotten is worse than stopping.
    """
    units = load_units()
    if slug:
        if slug not in [u.slug for u in units]:
            raise SystemExit(f'no unit {slug!r} under units/ (have: '
                             + ', '.join(u.slug for u in units) + ')')
        return slug
    if len(units) > 1:
        raise SystemExit('several units present; pass --unit <slug>: '
                         + ', '.join(u.slug for u in units))
    return units[0].slug


def review_dir(slug):
    """review/<slug>/, created on demand.

    The review sheets used to sit directly in review/, one slot for the whole
    project - so whichever unit ran last overwrote the others' findings. Each
    unit gets its own directory, as build_db and match_scans already assume.
    """
    p = os.path.join(ROOT, 'review', slug)
    os.makedirs(p, exist_ok=True)
    return p


def load_vocabulary(name, key):
    """A controlled vocabulary from reference/<name>.yml, as {slug: record}.

    eras, themes and repositories are all the same shape and all read the same
    way. Kept here rather than in a build script because the rulings loader
    validates against them, and a typo'd slug is otherwise invisible: it does
    not error, it just makes a document absent from the facet it belongs to.
    """
    path = os.path.join(ROOT, 'reference', name + '.yml')
    if not os.path.isfile(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return (yaml.safe_load(f) or {}).get(key) or {}


def load_eras():
    return load_vocabulary('eras', 'eras')


def load_themes():
    return load_vocabulary('themes', 'themes')


def load_repositories():
    return load_vocabulary('repositories', 'repositories')


def load_scan_map(unit):
    """{(letter_id, page): image filename} for one unit.

    The pairing of a transcript page to its photograph is established by
    match_scans.py and reviewed by hand; this is the authority for it. Read here
    rather than in each script that wants it, because four of them did, and the
    page record itself carried an empty `scan` field the whole time - so the
    dataset could say which line a name sits on and not which image to look at.
    """
    path = os.path.join(unit.dir, 'page_scan_map.csv')
    if not os.path.isfile(path):
        return {}
    out = {}
    with open(path, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            if row.get('letter') and row.get('page') and row.get('image'):
                out[(row['letter'], int(row['page']))] = row['image']
    return out
