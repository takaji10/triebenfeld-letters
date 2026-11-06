# The GEDCOM parser (PLAN.md section 4.1).
#
# A focused parser for the Gramps 5.5.1 dialect the family database is
# exported in, not a general one: the file is well-formed and its shape was
# profiled before this was written (4,439 INDI, 1,555 FAM, 2,000 media files
# carried inline at their point of reference, 440 sources, dates in the full
# 5.5.1 grammar).
#
# It works in two passes. First every line becomes a Node holding its
# children (the file is ~100k lines; the tree costs a few MB). Then each
# level-0 record is walked by a handler per record type. CONT/CONC lines are
# folded into their parent's text as they arrive; the inline OBJE blocks the
# GEDCOM repeats at every reference are deduped by normalised path, and each
# reference records its holder so media can be withheld for living or
# excluded people later.

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Dates. GEDCOM 5.5.1 dates in this file come in these shapes (examples from
# the file itself): "23 MAY 1933", "ABT 1874", "BEF 1910", "AFT 15 MAR 1902",
# "BET 1890 AND 1900", "FROM 1905 TO 1912", "FEB 1731/32", and the calendar
# prefix form "@#DGREGORIAN@ 25 DEC 1900". The raw text stays for display;
# the numbers exist for sorting and for the living-person test.

MONTHS = {m: i + 1 for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
     "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])}

_LINE = re.compile(r"^(\d+) (?:(@\w+@) )?([A-Za-z_]+)(?: (.*))?$")
_GED_PATH = re.compile(r"^[A-Za-z]:[/\\](.*)$")

_DATE_TOKEN = re.compile(
    r"(?:@#D[A-Z]+@\s*)?"          # optional calendar prefix
    r"(?:(\d{1,2})\s+)?"           # day
    r"([A-Za-z]{3})?\s*"           # month
    r"(\d{1,4})(?:/(\d{2}))?"      # year, optional double year
)


# ---------------------------------------------------------------------------
# Dates.

@dataclass
class Date:
    raw: str
    qual: str = ""          # "" | abt | cal | est | bef | aft | bet | from
    y1: int | None = None
    m1: int | None = None
    d1: int | None = None
    y2: int | None = None   # second bound of BET..AND / FROM..TO
    m2: int | None = None
    d2: int | None = None

    @property
    def sort(self) -> int | None:
        """Sortable integer; ranges sort by their first bound."""
        if self.y1 is None:
            return None
        return self.y1 * 10000 + (self.m1 or 0) * 100 + (self.d1 or 0)

    @property
    def year(self) -> int | None:
        return self.y1

    def __bool__(self) -> bool:
        return self.y1 is not None


def _parse_one(token: str) -> tuple[int | None, int | None, int | None]:
    token = re.sub(r"@#D[A-Z]+@\s*", "", token.strip())
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d{2}))?", token)   # ISO form
    if m:
        return int(m.group(1)), int(m.group(2)) or None, \
            int(m.group(3)) if m.group(3) else None
    m = _DATE_TOKEN.fullmatch(token)
    if not m:
        return None, None, None
    day = int(m.group(1)) if m.group(1) else None
    mon = MONTHS.get((m.group(2) or "").upper()) if m.group(2) else None
    return int(m.group(3)), mon, day


def parse_date(raw: str) -> Date | None:
    if not raw:
        return None
    d = Date(raw=raw.strip())
    s = re.sub(r"@#D[A-Z]+@\s*", "", d.raw)
    low = s.lower()

    m = re.match(r"^(bet|from)\s+(.+?)\s+(?:and|to)\s+(.+)$", low)
    if m:
        d.qual = m.group(1)
        d.y1, d.m1, d.d1 = _parse_one(m.group(2))
        d.y2, d.m2, d.d2 = _parse_one(m.group(3))
        return d

    m = re.match(r"^(abt|cal|est|bef|aft)\s+(.+)$", low)
    if m:
        d.qual = m.group(1)
        d.y1, d.m1, d.d1 = _parse_one(m.group(2))
        return d

    d.y1, d.m1, d.d1 = _parse_one(s)
    return d


# ---------------------------------------------------------------------------
# Model records.

@dataclass
class Media:
    """One media file. Referenced by xref from people, families, events and
    citations; the FILE record itself carries path, title and form, and
    data.gramps supplies the object id and the focus rectangle (regions
    live only there)."""
    path: str               # normalised relative POSIX path
    title: str = ""
    form: str = ""          # jpg | png | tif | docx | txt
    xref: str = ""          # "@O1884@" when it came from a shared record
    object_id: str = ""     # Gramps O#### id, when data.gramps matched
    region: tuple | None = None   # (x1, y1, x2, y2) percent, from data.gramps
    checksum: str = ""

    @property
    def is_image(self) -> bool:
        return self.form.lower() in ("jpg", "jpeg", "png", "tif", "tiff")

    @property
    def is_doc(self) -> bool:
        return not self.is_image and self.form.lower() not in ("", "txt")


@dataclass
class Citation:
    source: str = ""        # source xref, e.g. "@S0010@"
    page: str = ""
    data_date: str = ""
    text: str = ""
    media: list = field(default_factory=list)     # Media objects


@dataclass
class Event:
    tag: str                # BIRT | BAPM | DEAT | ... | EVEN | FACT | OCCU
    value: str = ""         # the line value (OCCU's occupation, FACT's claim)
    type: str = ""          # the TYPE sub-line
    date: Date | None = None
    place: str = ""
    coords: tuple | None = None   # (lat, lon) from the PLAC's MAP
    citations: list = field(default_factory=list)
    note: str = ""


@dataclass
class Name:
    raw: str = ""
    given: str = ""
    surname: str = ""
    nick: str = ""
    suffix: str = ""
    type: str = ""          # birth | married | aka | ...

    @property
    def display(self) -> str:
        parts = [self.given, f'"{self.nick}"' if self.nick else "",
                 self.surname, self.suffix]
        return " ".join(p for p in parts if p) or "(unknown)"


@dataclass
class Person:
    xref: str
    names: list = field(default_factory=list)
    sex: str = ""
    famc: list = field(default_factory=list)      # child in these families
    fams: list = field(default_factory=list)      # parent in these families
    events: list = field(default_factory=list)
    citations: list = field(default_factory=list) # person-level citations
    notes: list = field(default_factory=list)
    media: list = field(default_factory=list)     # person-level Media
    changed: str = ""
    refs: dict = field(default_factory=dict)      # REFN / WWW / etc.

    @property
    def name(self) -> Name:
        return self.names[0] if self.names else Name(raw="")

    @property
    def display(self) -> str:
        return self.name.display


@dataclass
class Family:
    xref: str
    husb: str = ""
    wife: str = ""
    chil: list = field(default_factory=list)
    events: list = field(default_factory=list)    # MARR, DIV, ...
    citations: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    media: list = field(default_factory=list)
    changed: str = ""


@dataclass
class Source:
    xref: str
    title: str = ""
    author: str = ""
    publication: str = ""
    repo: str = ""
    callno: str = ""
    notes: list = field(default_factory=list)
    media: list = field(default_factory=list)


@dataclass
class Repository:
    xref: str
    name: str = ""
    note: str = ""


@dataclass
class Model:
    people: dict = field(default_factory=dict)    # "@I0005@" -> Person
    families: dict = field(default_factory=dict)
    sources: dict = field(default_factory=dict)
    repos: dict = field(default_factory=dict)
    notes: dict = field(default_factory=dict)     # "@N0001@" -> text
    media: dict = field(default_factory=dict)     # path -> Media
    media_by_xref: dict = field(default_factory=dict)  # "@O1884@" -> Media
    header: dict = field(default_factory=dict)
    stats: dict = field(default_factory=dict)

    def person(self, xref: str) -> Person | None:
        return self.people.get(xref)


# ---------------------------------------------------------------------------
# Pass 1: lines to nodes.

class Node:
    __slots__ = ("level", "xref", "tag", "value", "children")

    def __init__(self, level, xref, tag, value):
        self.level, self.xref, self.tag, self.value = level, xref, tag, value
        self.children: list[Node] = []

    def child(self, tag: str) -> "Node | None":
        for c in self.children:
            if c.tag == tag:
                return c
        return None

    def text(self, tag: str) -> str:
        """The value of the first child with this tag, CONT/CONC joined."""
        c = self.child(tag)
        if c is None:
            return ""
        return _join(c)

    def all(self, tag: str) -> list["Node"]:
        return [c for c in self.children if c.tag == tag]


def _join(node: Node) -> str:
    out = node.value
    for c in node.children:
        if c.tag == "CONT":
            out += "\n" + c.value
        elif c.tag == "CONC":
            out += c.value
    return out


def read_tree(ged_path: str) -> tuple[list[Node], dict, dict, dict]:
    """Returns (records, notes, header, stats). Shared NOTE records are
    lifted out here because their text is plain CONT continuation."""
    roots: list[Node] = []
    stack: list[Node] = []
    notes: dict = {}
    header: dict = {}
    skipped = 0
    with open(ged_path, encoding="utf-8-sig", errors="replace") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            m = _LINE.match(line)
            if not m:
                if line.strip():
                    skipped += 1
                continue
            level, xref, tag, value = (int(m.group(1)), m.group(2),
                                       m.group(3), m.group(4) or "")
            node = Node(level, xref, tag, value)
            while stack and stack[-1].level >= level:
                stack.pop()
            if level == 0:
                roots.append(node)
                stack.append(node)
                continue
            if stack:
                stack[-1].children.append(node)
            else:
                skipped += 1
            stack.append(node)
    for rec in roots:
        if rec.tag == "NOTE" and rec.xref:
            notes[rec.xref] = _join(rec).strip()
    return roots, notes, header, {"skipped_lines": skipped}


# ---------------------------------------------------------------------------
# Pass 2: the record handlers.

def parse(ged_path: str) -> Model:
    model = Model()
    roots, notes, header, stats = read_tree(ged_path)
    model.notes = notes
    model.header = header
    model.stats.update(stats)

    # OBJE records first: the INDI/FAM/SOUR handlers resolve media by xref.
    # Several xrefs may point at one file (spouses sharing a headstone
    # photograph); each xref keeps its own Media object so its object id
    # and focus region survive, while the path catalog dedups for the
    # derivative build.
    for rec in roots:
        if rec.tag == "OBJE" and rec.xref:
            file_node = rec.child("FILE")
            path = norm_path(_join(file_node)) if file_node is not None else ""
            m = Media(path=path, title=file_node.text("TITL") if file_node else "",
                      form=(file_node.text("FORM") or "").lower() if file_node else "",
                      xref=rec.xref)
            model.media_by_xref[rec.xref] = m
            if path and path not in model.media:
                model.media[path] = m

    for rec in roots:
        if rec.tag == "INDI":
            _person(rec, model)
        elif rec.tag == "FAM":
            _family(rec, model)
        elif rec.tag == "SOUR":
            _source(rec, model)
        elif rec.tag == "REPO":
            r = Repository(xref=rec.xref, name=rec.text("NAME"),
                           note=rec.text("NOTE"))
            model.repos[rec.xref] = r
        elif rec.tag == "HEAD":
            for c in rec.children:
                if c.tag != "CHAN":
                    model.header[c.tag] = _join(c)
    return model


def _person(rec: Node, model: Model) -> None:
    p = Person(xref=rec.xref)
    model.people[rec.xref] = p
    for c in rec.children:
        if c.tag == "NAME":
            n = Name(raw=_join(c), type=c.text("TYPE"))
            n.given = c.text("GIVN")
            n.surname = c.text("SURN")
            n.nick = c.text("NICK")
            n.suffix = c.text("NSFX")
            if not n.given and not n.surname:
                m = re.match(r"^(.*?)/(.+?)/(.*?)$", _join(c))
                if m:
                    n.given, n.surname, n.suffix = (g.strip() for g in m.groups())
            p.names.append(n)
        elif c.tag == "SEX":
            p.sex = c.value
        elif c.tag == "FAMS":
            p.fams.append(c.value)
        elif c.tag == "FAMC":
            p.famc.append(c.value)
        elif c.tag in _EVENT_TAGS:
            p.events.append(_event(c, model))
        elif c.tag == "NOTE":
            if c.value.startswith("@"):
                p.notes.append(model.notes.get(c.value, ""))
            else:
                p.notes.append(_join(c))
        elif c.tag == "OBJE":
            for m in _obje(c, model):
                if m not in p.media:
                    p.media.append(m)
        elif c.tag == "SOUR":
            p.citations.append(_citation(c, model))
        elif c.tag == "CHAN":
            p.changed = c.text("DATE") + (" " + c.text("TIME") if c.text("TIME") else "")
        elif c.tag in ("REFN", "WWW"):
            p.refs.setdefault(c.tag, []).append(_join(c))


def _family(rec: Node, model: Model) -> None:
    f = Family(xref=rec.xref)
    model.families[rec.xref] = f
    for c in rec.children:
        if c.tag == "HUSB":
            f.husb = c.value
        elif c.tag == "WIFE":
            f.wife = c.value
        elif c.tag == "CHIL":
            f.chil.append(c.value)
        elif c.tag in _FAMILY_EVENT_TAGS:
            f.events.append(_event(c, model))
        elif c.tag == "NOTE":
            if c.value.startswith("@"):
                f.notes.append(model.notes.get(c.value, ""))
            else:
                f.notes.append(_join(c))
        elif c.tag == "OBJE":
            for m in _obje(c, model):
                if m not in f.media:
                    f.media.append(m)
        elif c.tag == "SOUR":
            f.citations.append(_citation(c, model))
        elif c.tag == "CHAN":
            f.changed = c.text("DATE") + (" " + c.text("TIME") if c.text("TIME") else "")


def _source(rec: Node, model: Model) -> None:
    s = Source(xref=rec.xref, title=rec.text("TITL"),
               author=rec.text("AUTH"), publication=rec.text("PUBL"))
    for c in rec.all("REPO"):
        s.repo = c.value
        s.callno = c.text("CALN")
    for c in rec.all("NOTE"):
        s.notes.append(model.notes.get(c.value, "") if c.value.startswith("@")
                       else _join(c))
    for c in rec.all("OBJE"):
        for m in _obje(c, model):
            if m not in s.media:
                s.media.append(m)
    model.sources[rec.xref] = s


_EVENT_TAGS = {"BIRT", "BAPM", "CHR", "BAPL", "DEAT", "BURI", "CREM",
               "RESI", "IMMI", "EMIG", "CENS", "NATU", "RETI", "CONF",
               "ADOP", "PROP", "EDUC", "EVEN", "FACT", "_MILT", "GRAD",
               "MILIT", "CAST", "RELI", "ORDI"}
_FAMILY_EVENT_TAGS = {"MARR", "DIV", "ANUL", "EVEN", "RESI"}


def _event(node: Node, model: Model) -> Event:
    ev = Event(tag=node.tag, value=_join(node))
    for c in node.children:
        if c.tag == "DATE":
            ev.date = parse_date(_join(c))
        elif c.tag == "PLAC":
            ev.place = _join(c)
            m = c.child("MAP")
            if m is not None:
                ev.coords = _coords(m.text("LATI"), m.text("LONG"))
        elif c.tag == "TYPE":
            ev.type = _join(c)
        elif c.tag == "NOTE":
            ev.note = model.notes.get(c.value, "") if c.value.startswith("@") else _join(c)
        elif c.tag == "SOUR":
            ev.citations.append(_citation(c, model))
        elif c.tag == "OBJE":
            ev.citations.append(Citation(source="", page="", media=_obje(c, model)))
    return ev


def _coords(lat: str, lon: str) -> tuple | None:
    """GEDCOM writes hemisphere letters: N49.895537, W97.138458."""
    def one(v: str) -> float | None:
        v = (v or "").strip()
        if not v:
            return None
        sign = -1.0 if v[0].upper() in ("S", "W") else 1.0
        if v[0].isalpha():
            v = v[1:]
        try:
            return sign * abs(float(v))
        except ValueError:
            return None
    a, b = one(lat), one(lon)
    return (a, b) if a is not None and b is not None else None


def _citation(node: Node, model: Model) -> Citation:
    cit = Citation(source=node.value)
    for c in node.children:
        if c.tag == "PAGE":
            cit.page = _join(c)
        elif c.tag == "DATA":
            cit.data_date = c.text("DATE")
            cit.text = c.text("TEXT")
        elif c.tag == "NOTE":
            cit.text = cit.text or model.notes.get(c.value, _join(c))
        elif c.tag == "OBJE":
            cit.media.extend(_obje(c, model))
        elif c.tag == "QUAL":
            pass
    return cit


def _obje(node: Node, model: Model) -> list[Media]:
    """An OBJE reference resolves to the shared media record by xref; an
    inline FILE block (other exports) is handled as a fallback."""
    if node.value.startswith("@"):
        m = model.media_by_xref.get(node.value)
        return [m] if m else []
    file_node = node.child("FILE")
    if file_node is not None:
        path = norm_path(_join(file_node))
        m = model.media.get(path)
        if m is None:
            m = Media(path=path, title=node.text("TITL"),
                      form=(node.text("FORM") or "").lower())
            model.media[path] = m
        return [m]
    return []


def norm_path(p: str) -> str:
    """GEDCOM FILE paths are absolute Windows paths into the media tree;
    gpkg entries carry the same tree. Normalise to one relative POSIX form,
    folding unicode composition differences away."""
    s = (p or "").strip().replace("\\", "/")
    m = _GED_PATH.match(s)
    if m:
        s = m.group(1)
    while s.startswith("../"):
        s = s[3:]
    s = s.lstrip("/")
    return unicodedata.normalize("NFC", s)
