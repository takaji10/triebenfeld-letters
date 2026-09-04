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
        'DUP_OF':         docs.get('duplicate_of') or {},
        'SPLIT_NOTE':     docs.get('split_note') or {},
        'DAMAGE_LETTERS': set(damage.get('letters') or []),
    }
