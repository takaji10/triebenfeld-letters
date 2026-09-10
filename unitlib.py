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
    permalink  /letters/oe1bu9454/48/    what the reader sees

Keeping letter_id bare is deliberate: every editorial ruling in rulings.yml is
keyed by it, so those files never have to be re-keyed when a unit is added.
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
UNITS_DIR = os.path.join(ROOT, 'units')


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
        return f'/letters/{self.slug}/{letter_id}/'


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

def load_place_canon():
    """The shared place-name canon, variant (lowercased) -> the edition's form.

    Standalone because it is not a unit's ruling: build_site_data needs it for
    tagging, with no unit in hand. It used to keep a second, much smaller copy
    of its own, so a place normalised on the dateline was not necessarily
    normalised where it was tagged.
    """
    path = os.path.join(ROOT, 'reference', 'place_canon.yml')
    with open(path, encoding='utf-8') as f:
        return (yaml.safe_load(f) or {}).get('canon') or {}


def load_rulings(unit):
    """The unit's editorial decisions, plus the place canon shared by all units.

    Names match the constants build_db.py used to carry inline, so the loading
    is the only thing that changed.
    """
    with open(unit.rulings_path, encoding='utf-8') as f:
        r = yaml.safe_load(f) or {}
    canon_path = os.path.join(ROOT, 'reference', 'place_canon.yml')
    with open(canon_path, encoding='utf-8') as f:
        c = yaml.safe_load(f) or {}

    places = r.get('places') or {}
    dates = r.get('dates') or {}
    docs = r.get('documents') or {}
    damage = r.get('damage') or {}

    def tuples(d):
        return {k: tuple(v) for k, v in (d or {}).items()}

    return {
        'PLACE_CANON':    c.get('canon') or {},
        'PLACE_REJECT':   set(c.get('reject') or []),
        'PLACE_OVERRIDE': places.get('overrides') or {},
        'SUPPLIED':       tuples(dates.get('supplied')),
        'TWIN':           tuples(dates.get('twin')),
        'INFERRED':       tuples(dates.get('inferred')),
        'NO_DATE':        set(dates.get('no_date') or []),
        'DOC_TYPE':       docs.get('doc_type') or {},
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
