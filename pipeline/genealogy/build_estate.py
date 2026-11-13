#!/usr/bin/env python
"""Build the Trabczyn estate-owners tree from reference/estate_tree.yml.

    python pipeline/genealogy/build_estate.py [--yml F] [--ged F] [--out D] [--check]

The YAML is validated, written out as a GEDCOM 5.5.1 file (opens in Gramps),
parsed again with gedcom.py and turned into the explorer's JSON by
build_data.build_all, so the output has exactly the Zelmer data's shape.

Schema (also in reference/estate_tree.SCHEMA.md):

tree: {start: T010}          # the person the big tree opens on
sources:
  <key>:
    title: "..."             # required
    author: "..."            # optional
    url: "/documents/x/1/"   # optional; starts with / (no spaces) or https://
    kind: document | literature | database | web | report   # required; report = reported by the editor, not held by the edition (reference/sources/)
places:
  <key>:
    name: "Trabczyn, Konin district, Greater Poland"   # required
    lat: 52.215              # optional, both or neither
    lon: 17.83
    coord_source: "reference/place_coords.yml"  # required with lat/lon
people:
  <id>:                      # T001 ... (GEDCOM xref without @)
    given: "Jan"
    surname: "Otto-Trampczynski"
    sex: M | F | U
    rule: holder | spouse | child | connector | party
    page: "/people/jan/"     # optional
    events:
      - type: BIRT | DEAT | BURI | RESI | OCCU | EVEN
        label: "Held Trabczyn"   # EVEN: TYPE; OCCU: the occupation; else TYPE
        date: "BEF 6 OCT 1693"   # GEDCOM date phrase; optional
        place: trabczyn          # a places key; optional
        note: "..."              # optional
        cite: [{source: konin145, page: "doc 1, p. 2", exact: true}]  # >= 1
    notes: ["..."]
families:
  <id>:                      # F001 ...
    husb: T001
    wife: T002
    children: [T003, T004]
    cite: [{source: ..., page: ...}]     # required
    marr: {date: "...", place: ..., note: ..., cite: [...]}   # cite required

Validation: all references resolve; every person is in a family (unless alone);
every event/family/marriage is cited; a date citing a `database` source needs a
cite with exact: true; no "?", "ok.", "okolo", "prawdopodobnie" in dates; rule
and sex in their sets; lat/lon both or neither, numeric, inside lat 49-55 /
lon 14-25 (unless coord_source says "outside Poland") and with a coord_source;
a site-relative url has no space.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import gedcom        # noqa: E402
import build_data    # noqa: E402

ROOT = HERE.parents[1]
RULES = {"holder", "spouse", "child", "connector", "party"}
KINDS = {"document", "literature", "database", "web", "report"}  # report: a source the editor reports that the edition does not hold (reference/sources/)
EVENT_TYPES = {"BIRT", "DEAT", "BURI", "RESI", "OCCU", "EVEN"}
BAD_DATE = re.compile(r"\?|\bok\.|około|\bokolo\b|prawdopodobnie", re.I)


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


# ---------------------------------------------------------------- validate

def validate(y: dict) -> list[str]:
    errs: list[str] = []
    src = y.get("sources") or {}
    plc = y.get("places") or {}
    ppl = y.get("people") or {}
    fam = y.get("families") or {}

    start = (y.get("tree") or {}).get("start")
    if not start:
        errs.append("tree.start is missing")
    elif start not in ppl:
        errs.append(f"tree.start {start!r} is not a person")

    for k, s in src.items():
        w = f"source {k}"
        if not s.get("title"):
            errs.append(f"{w}: title missing")
        if s.get("kind") not in KINDS:
            errs.append(f"{w}: kind {s.get('kind')!r} not one of {sorted(KINDS)}")
        u = s.get("url")
        if u:
            if u.startswith("/"):
                if re.search(r"\s", u):
                    errs.append(f"{w}: url {u!r} contains a space")
            elif not u.startswith("https://"):
                errs.append(f"{w}: url {u!r} must start with / or https://")

    for k, p in plc.items():
        w = f"place {k}"
        if not p.get("name"):
            errs.append(f"{w}: name missing")
        lat, lon = p.get("lat"), p.get("lon")
        if (lat is None) != (lon is None):
            errs.append(f"{w}: lat and lon must be given together")
        if lat is not None and lon is not None:
            ok = all(isinstance(v, (int, float)) and not isinstance(v, bool)
                     for v in (lat, lon))
            if not ok:
                errs.append(f"{w}: lat/lon must be numbers")
            else:
                cs = str(p.get("coord_source") or "")
                if not cs:
                    errs.append(f"{w}: coord_source missing")
                if not (49 <= lat <= 55 and 14 <= lon <= 25) \
                        and "outside poland" not in cs.lower():
                    errs.append(f"{w}: ({lat}, {lon}) outside Poland's box "
                                f"(lat 49-55, lon 14-25) and coord_source "
                                f"does not say 'outside Poland'")

    def check_cites(w, cites, date_str):
        if not cites:
            errs.append(f"{w}: no cite")
            return
        has_db = False
        exact = False
        for c in cites:
            sk = c.get("source")
            if sk not in src:
                errs.append(f"{w}: cite source {sk!r} does not exist")
                continue
            if src[sk].get("kind") == "database":
                has_db = True
            if c.get("exact") is True:
                exact = True
        if date_str and has_db and not exact:
            errs.append(f"{w}: database date not marked exact "
                        f"(date {date_str!r}; no cite has exact: true)")

    def check_date(w, d):
        if d and BAD_DATE.search(str(d)):
            errs.append(f"{w}: date {d!r} contains '?' or an estimate word "
                        f"(ok., około, prawdopodobnie)")

    for k, p in ppl.items():
        w = f"person {k}"
        if p.get("sex") not in ("M", "F", "U"):
            errs.append(f"{w}: sex {p.get('sex')!r} not M/F/U")
        if p.get("rule") not in RULES:
            errs.append(f"{w}: rule {p.get('rule')!r} not one of {sorted(RULES)}")
        if not (p.get("given") or p.get("surname")):
            errs.append(f"{w}: no given name or surname")
        for i, e in enumerate(p.get("events") or []):
            ew = f"{w} event {i + 1} ({e.get('type')})"
            if e.get("type") not in EVENT_TYPES:
                errs.append(f"{ew}: type not one of {sorted(EVENT_TYPES)}")
            pl = e.get("place")
            if pl and pl not in plc:
                errs.append(f"{ew}: place {pl!r} does not exist")
            check_date(ew, e.get("date"))
            check_cites(ew, e.get("cite"), e.get("date"))

    in_fam: set = set()
    for k, f in fam.items():
        w = f"family {k}"
        for role in ("husb", "wife"):
            v = f.get(role)
            if v:
                in_fam.add(v)
                if v not in ppl:
                    errs.append(f"{w}: {role} {v!r} is not a person")
        for c in f.get("children") or []:
            in_fam.add(c)
            if c not in ppl:
                errs.append(f"{w}: child {c!r} is not a person")
        check_cites(w, f.get("cite"), None)
        m = f.get("marr")
        if m:
            mw = f"{w} marriage"
            if m.get("place") and m["place"] not in plc:
                errs.append(f"{mw}: place {m['place']!r} does not exist")
            check_date(mw, m.get("date"))
            check_cites(mw, m.get("cite"), m.get("date"))
    if len(ppl) > 1:
        for k in ppl:
            if k not in in_fam:
                errs.append(f"person {k}: appears in no family")
    return errs


# ------------------------------------------------------------------ GEDCOM

class Out:
    def __init__(self):
        self.lines: list[str] = []

    def put(self, level, tag, value="", xref=None):
        head = f"{level} " + (f"@{xref}@ " if xref else "") + tag
        first = True
        for part in (str(value).split("\n") if value != "" else [""]):
            chunks = [part[i:i + 200] for i in range(0, len(part), 200)] or [""]
            for j, ch in enumerate(chunks):
                if first and j == 0:
                    self.lines.append(f"{head} {ch}" if ch else head)
                elif j == 0:
                    self.lines.append(f"{level + 1} CONT {ch}".rstrip())
                else:
                    self.lines.append(f"{level + 1} CONC {ch}")
            first = False


def _hemi(v, pos, neg):
    return f"{pos if v >= 0 else neg}{abs(v):g}"


def write_gedcom(y: dict, path: Path) -> None:
    src, plc = y.get("sources") or {}, y.get("places") or {}
    o = Out()
    o.put(0, "HEAD")
    o.put(1, "SOUR", "estate_tree.yml")
    o.put(2, "NAME", "build_estate.py")
    o.put(1, "DATE", date.today().strftime("%d %b %Y").upper().lstrip("0"))
    o.put(1, "GEDC")
    o.put(2, "VERS", "5.5.1")
    o.put(2, "FORM", "LINEAGE-LINKED")
    o.put(1, "CHAR", "UTF-8")

    def place(pk, lvl):
        p = plc[pk]
        o.put(lvl, "PLAC", p["name"])
        if p.get("lat") is not None:
            o.put(lvl + 1, "MAP")
            o.put(lvl + 2, "LATI", _hemi(p["lat"], "N", "S"))
            o.put(lvl + 2, "LONG", _hemi(p["lon"], "E", "W"))

    def cites(lst, lvl):
        for c in lst or []:
            o.put(lvl, "SOUR", f"@S_{c['source']}@")
            if c.get("page"):
                o.put(lvl + 1, "PAGE", c["page"])
            if c.get("exact"):
                o.put(lvl + 1, "QUAY", "3")

    def event(e, lvl, tag=None):
        tag = tag or e["type"]
        label = e.get("label")
        if tag == "OCCU":
            o.put(lvl, tag, label or "")
        elif tag == "EVEN":
            o.put(lvl, tag)
            if label:
                o.put(lvl + 1, "TYPE", label)
        else:
            o.put(lvl, tag, "Y" if tag in ("BIRT", "DEAT", "MARR") and
                  not (e.get("date") or e.get("place")) else "")
            if label:
                o.put(lvl + 1, "TYPE", label)
        if e.get("date"):
            o.put(lvl + 1, "DATE", e["date"])
        if e.get("place"):
            place(e["place"], lvl + 1)
        if e.get("note"):
            o.put(lvl + 1, "NOTE", e["note"])
        cites(e.get("cite"), lvl + 1)

    ppl, fam = y.get("people") or {}, y.get("families") or {}
    fams_of: dict = {}
    famc_of: dict = {}
    for fk, f in fam.items():
        for r in ("husb", "wife"):
            if f.get(r):
                fams_of.setdefault(f[r], []).append(fk)
        for c in f.get("children") or []:
            famc_of.setdefault(c, []).append(fk)

    for k, p in ppl.items():
        o.put(0, "INDI", xref=k)
        g, s = p.get("given") or "", p.get("surname") or ""
        o.put(1, "NAME", f"{g} /{s}/".strip())
        if g:
            o.put(2, "GIVN", g)
        if s:
            o.put(2, "SURN", s)
        o.put(1, "SEX", p["sex"])
        for e in p.get("events") or []:
            event(e, 1)
        for n in p.get("notes") or []:
            o.put(1, "NOTE", n)
        if p.get("page"):
            o.put(1, "WWW", p["page"])
        for fk in famc_of.get(k, []):
            o.put(1, "FAMC", f"@{fk}@")
        for fk in fams_of.get(k, []):
            o.put(1, "FAMS", f"@{fk}@")

    for k, f in fam.items():
        o.put(0, "FAM", xref=k)
        if f.get("husb"):
            o.put(1, "HUSB", f"@{f['husb']}@")
        if f.get("wife"):
            o.put(1, "WIFE", f"@{f['wife']}@")
        for c in f.get("children") or []:
            o.put(1, "CHIL", f"@{c}@")
        if f.get("marr"):
            event(f["marr"], 1, "MARR")
        cites(f.get("cite"), 1)

    for k, s in src.items():
        o.put(0, "SOUR", xref=f"S_{k}")
        o.put(1, "TITL", s["title"])
        if s.get("author"):
            o.put(1, "AUTH", s["author"])
        if s.get("url"):
            o.put(1, "WWW", s["url"])
        o.put(1, "NOTE", f"Kind: {s['kind']}")
    o.put(0, "TRLR")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(o.lines) + "\n")


# ------------------------------------------------------------------- build

def build(y: dict, ged: Path, out: Path) -> dict:
    write_gedcom(y, ged)
    # gedcom.py's event set lacks OCCU (the Zelmer build never read it);
    # add it for this process only so the Zelmer output stays unchanged
    gedcom._EVENT_TAGS.add("OCCU")
    model = gedcom.parse(str(ged))
    (out / "people").mkdir(parents=True, exist_ok=True)
    for f in (out / "people").glob("*.json"):
        f.unlink()
    build_data.build_all(model, str(out))

    def rd(n):
        return json.loads((out / n).read_text(encoding="utf-8"))

    def wr(path, d, indent=None):
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            if indent:
                json.dump(d, fh, ensure_ascii=False, indent=indent)
            else:
                json.dump(d, fh, ensure_ascii=False, separators=(",", ":"))

    src = y.get("sources") or {}
    plc = y.get("places") or {}
    # (a) sources: url and kind
    sj = rd("sources.json")
    for k, s in src.items():
        e = sj.setdefault(f"S_{k}", {"title": s["title"]})
        if s.get("url"):
            e["url"] = s["url"]
        e["kind"] = s["kind"]
    wr(out / "sources.json", sj)
    # places: coord_source
    pj = rd("places.json")
    for p in plc.values():
        if p["name"] in pj and p.get("coord_source"):
            pj[p["name"]]["coord_source"] = p["coord_source"]
    wr(out / "places.json", pj)

    exact = set()

    def note_exact(lst):
        for c in lst or []:
            if c.get("exact"):
                exact.add((f"S_{c['source']}", c.get("page", "")))

    for p in (y.get("people") or {}).values():
        for e in p.get("events") or []:
            note_exact(e.get("cite"))
    for f in (y.get("families") or {}).values():
        note_exact(f.get("cite"))
        note_exact((f.get("marr") or {}).get("cite"))

    def mark(cits):
        for c in cits or []:
            if (c["s"], c.get("page", "")) in exact:
                c["exact"] = True

    # person shards: rule, page; citations: exact
    for k, p in (y.get("people") or {}).items():
        fp = out / "people" / f"{k}.json"
        sh = json.loads(fp.read_text(encoding="utf-8"))
        sh["rule"] = p["rule"]
        if p.get("page"):
            sh["page"] = p["page"]
        for ev in sh["events"]:
            mark(ev.get("citations"))
        wr(fp, sh)
    # holders carry "h": 1 in the index the tree reads (the owner mark)
    ij = rd("index.json")
    for k, p in (y.get("people") or {}).items():
        if p.get("rule") == "holder" and k in ij:
            ij[k]["h"] = 1
    wr(out / "index.json", ij)
    fj = rd("families.json")
    for k, f in (y.get("families") or {}).items():
        fj[k]["citations"] = [
            {"s": f"S_{c['source']}",
             **({"page": c["page"]} if c.get("page") else {}),
             **({"exact": True} if c.get("exact") else {})} for c in f["cite"]]
        mark((fj[k].get("marr") or {}).get("citations"))
    wr(out / "families.json", fj)
    wr(out / "media_files.json", {}, indent=1)
    # (b) meta
    meta = rd("meta.json")
    meta.update({
        "tree": "trabczyn",
        "title": {"en": "Owners of Trąbczyn", "de": "Die Besitzer von Trąbczyn"},
        "start": y["tree"]["start"],
        "media": False,
        "holder_label": {"en": "Held Trąbczyn", "de": "Besitzer von Trąbczyn"},
        "source": "reference/estate_tree.yml",
    })
    wr(out / "meta.json", meta, indent=1)
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--yml", default=str(ROOT / "reference/estate_tree.yml"))
    ap.add_argument("--ged", default=str(ROOT / "site/genealogy/trabczyn/estate.ged"))
    ap.add_argument("--out", default=str(ROOT / "site/genealogy/trabczyn/data"))
    ap.add_argument("--check", action="store_true", help="validate only")
    a = ap.parse_args()
    ypath = Path(a.yml)
    if not ypath.exists():
        print(f"error: {ypath} not found", file=sys.stderr)
        return 1
    y = load(ypath)
    errs = validate(y)
    if errs:
        print(f"{len(errs)} problem(s) in {ypath}:", file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        return 1
    if a.check:
        print(f"{ypath}: OK ({len(y.get('people') or {})} people, "
              f"{len(y.get('families') or {})} families)")
        return 0
    meta = build(y, Path(a.ged), Path(a.out))
    print(f"wrote {a.ged} and {a.out}: {meta['counts']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
