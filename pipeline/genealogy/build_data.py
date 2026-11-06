# The data builder (PLAN.md section 4.6).
#
# Turns the parsed, pruned, redacted model into the JSON shards the app
# loads: one small index for browsing and search, one shard per person
# loaded on demand, one families file, the places and sources summaries and
# the media manifest. Everything written here is already public: exclusion
# and privacy have run before this module is called.

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
LIVING_GIVEN = "[Living]"


def _date_json(d) -> dict | None:
    if d is None:
        return None
    out = {"raw": d.raw, "qual": d.qual}
    if d.y1 is not None:
        out["y"] = d.y1
        if d.m1:
            out["m"] = d.m1
        if d.d1:
            out["d"] = d.d1
        if d.y2 is not None:
            out["y2"] = d.y2
    return out


def _coords_json(c) -> list | None:
    if not c:
        return None
    return [round(c[0], 6), round(c[1], 6)]


def _media_json(m, person_xref=None, regions=None) -> dict:
    out = {"path": m.path, "form": m.form}
    if m.title:
        out["title"] = m.title
    if m.object_id:
        out["oid"] = m.object_id
    if person_xref and regions:
        for entry in regions.get(m.path, []):
            if person_xref in entry["persons"]:
                out["region"] = list(entry["region"])
                break
    return out


def _citation_json(cit, withheld=None) -> dict:
    out = {"s": cit.source.strip("@")}
    if cit.page:
        out["page"] = cit.page
    if cit.data_date:
        out["dd"] = cit.data_date
    if cit.text:
        out["text"] = cit.text
    media = [m for m in cit.media if not withheld or m.path not in withheld]
    if media:
        out["m"] = [{"path": m.path, "form": m.form,
                     **({"title": m.title} if m.title else {})}
                    for m in media]
    return out


_EVENT_LABEL_ORDER = [
    "BIRT", "BAPM", "CHR", "BAPL", "ADOP", "CONF", "EDUC", "GRAD",
    "RESI", "OCCU", "PROP", "IMMI", "EMIG", "NATU", "CENS", "MILIT",
    "_MILT", "RETI", "MARR", "DIV", "ANUL", "EVEN", "FACT", "DEAT",
    "BURI", "CREM",
]


def person_shard(model, xref: str, regions=None, withheld=None) -> dict:
    p = model.people[xref]
    withheld = withheld or set()
    name = p.name
    is_living = name.given == LIVING_GIVEN

    def _sort_key(e):
        s = e.date.sort if e.date else None
        return (s is None, s or 0)

    # every event of the person, personal and family, as decorated
    # (sortkey, dict) pairs so the merged timeline sorts by date
    decorated = []

    def add(e, ev):
        s = e.date.sort if e.date else None
        decorated.append(((s is None, s or 0), ev))

    for e in sorted(p.events, key=_sort_key):
        if e.tag == "OCCU" and not (e.value or e.date or e.place):
            continue
        ev = {"tag": e.tag}
        if e.value and e.value != e.tag:
            ev["value"] = e.value
        if e.type:
            ev["type"] = e.type
        dj = _date_json(e.date)
        if dj:
            ev["date"] = dj
        if e.place:
            ev["place"] = e.place
        cj = _coords_json(e.coords)
        if cj:
            ev["coords"] = cj
        cits = [_citation_json(c, withheld) for c in e.citations]
        if cits:
            ev["citations"] = cits
        if e.note:
            ev["note"] = e.note
        add(e, ev)

    # the family events of the person's own unions - the marriage in the
    # life events timeline with everyone else (the editor's ruling,
    # 2026-11-06: everything belongs in the timeline). Each carries the
    # spouse's id and name so the row can say who it was with.
    for fam_xref in p.fams:
        fam = model.families.get(fam_xref)
        if not fam:
            continue
        spouse = fam.wife if fam.husb == xref else fam.husb
        spouse_name = None
        if spouse and spouse in model.people:
            spouse_name = model.people[spouse].name.display
        for e in fam.events:
            if e.tag not in ("MARR", "DIV", "ANUL"):
                continue
            ev = {"tag": e.tag}
            if spouse:
                ev["sp"] = spouse.strip("@")
                if spouse_name:
                    ev["with"] = spouse_name
            dj = _date_json(e.date)
            if dj:
                ev["date"] = dj
            if e.place:
                ev["place"] = e.place
            cj = _coords_json(e.coords)
            if cj:
                ev["coords"] = cj
            cits = [_citation_json(c, withheld) for c in e.citations]
            if cits:
                ev["citations"] = cits
            if e.note:
                ev["note"] = e.note
            add(e, ev)

    events = [ev for _, ev in sorted(decorated, key=lambda pair: pair[0])]

    media = [_media_json(m, xref, regions) for m in p.media
             if m.path not in withheld]

    notes = [n for n in p.notes if n and n.strip()]

    return {
        "id": xref.strip("@"),
        "name": name.display,
        "surname": name.surname,
        "given": name.given,
        "sex": p.sex,
        "living": is_living,
        **({"nick": name.nick} if name.nick else {}),
        **({"suffix": name.suffix} if name.suffix else {}),
        "names": [{"given": n.given, "surname": n.surname,
                   **({"type": n.type} if n.type else {}),
                   **({"nick": n.nick} if n.nick else {})}
                  for n in p.names[1:]],
        "famc": [f.strip("@") for f in p.famc],
        "fams": [f.strip("@") for f in p.fams],
        "events": events,
        "media": media,
        **({"notes": notes} if notes else {}),
        **({"changed": p.changed} if p.changed else {}),
    }


def living_stub(model, xref: str) -> dict:
    p = model.people[xref]
    return {
        "id": xref.strip("@"),
        "name": f"Living {p.name.surname}".strip(),
        "surname": p.name.surname,
        "sex": p.sex,
        "living": True,
        "famc": [f.strip("@") for f in p.famc],
        "fams": [f.strip("@") for f in p.fams],
        "events": [],
        "media": [],
    }


def family_json(model, fam, withheld=None) -> dict:
    out = {
        "id": fam.xref.strip("@"),
        "husb": fam.husb.strip("@") if fam.husb else None,
        "wife": fam.wife.strip("@") if fam.wife else None,
        "chil": [c.strip("@") for c in fam.chil],
    }
    for e in fam.events:
        key = {"MARR": "marr", "DIV": "div", "ANUL": "anul"}.get(e.tag)
        if key:
            entry = {}
            dj = _date_json(e.date)
            if dj:
                entry["date"] = dj
            if e.place:
                entry["place"] = e.place
            cj = _coords_json(e.coords)
            if cj:
                entry["coords"] = cj
            cits = [_citation_json(c, withheld) for c in e.citations]
            if cits:
                entry["citations"] = cits
            out[key] = entry
    return out


def build_all(model, out_dir: str, regions=None, withheld=None,
              excluded_media=None, excluded_people=None, excluded_families=None,
              media_version="", media_base="", available=None,
              media_manifest=None) -> dict:
    out = Path(out_dir)
    (out / "people").mkdir(parents=True, exist_ok=True)
    withheld = withheld or set()
    excluded_media = excluded_media or set()
    excluded_people = excluded_people or set()
    excluded_families = excluded_families or set()
    media_manifest = media_manifest or {}
    skip_media = withheld | excluded_media
    # when the media repo's manifest is known, a path outside it cannot be
    # served: treat it as unavailable everywhere (the gpkg mismatches)
    unavailable = set()
    if available is not None:
        keys = available.keys() if isinstance(available, dict) else available
        unavailable = {p for p in model.media if p and p not in keys}
    skip_media = skip_media | unavailable

    # ---- index.json: everyone kept, compact -----------------------------
    index = {}
    for x, p in model.people.items():
        if x in excluded_people:
            continue
        name = p.name
        living = name.given == LIVING_GIVEN
        by = dy = None
        br = dr = None
        bp = {}
        dp = {}
        if not living:
            for tag in ("BIRT", "BAPM", "CHR", "BAPL"):
                ev = next((e for e in p.events if e.tag == tag
                           and e.date and e.date.year), None)
                if ev:
                    by = ev.date.year
                    br = ev.date.raw
                    if ev.place:
                        bp = {"bp": ev.place}
                    break
            for tag in ("DEAT", "BURI", "CREM"):
                ev = next((e for e in p.events if e.tag == tag
                           and e.date and e.date.year), None)
                if ev:
                    dy = ev.date.year
                    dr = ev.date.raw
                    if ev.place:
                        dp = {"dp": ev.place}
                    break
        index[x.strip("@")] = {
            "n": f"Living {name.surname}".strip() if living else name.display,
            "sn": name.surname,
            "gn": "" if living else name.given,
            "sx": p.sex,
            "b": by, "d": dy,
            # the raw date texts, for the UI's formatted rendering
            **({"br": br} if br else {}),
            **({"dr": dr} if dr else {}),
            # the birth and death places, for the relations lists
            **bp,
            **dp,
            "L": living,
            "M": any(m.path not in skip_media for m in p.media),
            "fc": [f.strip("@") for f in p.famc],
            "fs": [f.strip("@") for f in p.fams],
        }
        # the portrait: the person's first publishable image, a photo or
        # portrait by name when there is one - person-level media first,
        # then anything the person's citations carry (in this database
        # most media hangs off citations, portraits included) - resolved
        # through the media manifest to its derivative file names (the
        # UI joins them with the media base; a person without
        # publishable media gets the placeholder)
        if not living:
            cands = [m for m in p.media
                     if m.path and m.path not in skip_media]
            cited = []
            for e in p.events:
                for cit in e.citations:
                    for m in cit.media:
                        if m.path and m.path not in skip_media:
                            cited.append(m)
            pool = cands + [m for m in cited
                            if m.path not in {c.path for c in cands}]
            # only a real picture serves as the portrait: a birth record
            # is a document about the person, not a picture of them
            chosen = next((m for m in pool if
                           (m.title and re.search(
                               r"photo|portrait|porträt", m.title, re.I))
                           or re.search(r"photo|portrait|porträt",
                                        m.path, re.I)), None)
            entry = media_manifest.get(chosen.path) if chosen else None
            if entry:
                row = index[x.strip("@")]
                if entry.get("file"):
                    row["pd"] = entry["file"]
                if entry.get("thumb"):
                    row["pt"] = entry["thumb"]

    # ---- surname index with variant groups ----------------------------
    by_surname = defaultdict(list)
    for x, row in index.items():
        sn = row["sn"].strip()
        if sn:
            by_surname[sn].append(x)

    # ---- places: string -> coords + event count + event list ----------
    places = {}
    for p in model.people.values():
        if p.xref in excluded_people:
            continue
        for e in p.events:
            if not e.place:
                continue
            key = e.place
            slot = places.setdefault(key, {"n": 0, "ev": []})
            if e.coords and "c" not in slot:
                slot["c"] = _coords_json(e.coords)
            slot["n"] += 1
            slot["ev"].append([p.xref.strip("@"), e.tag,
                               e.date.year if e.date else None,
                               e.date.raw if e.date else None])
    for fam in model.families.values():
        if fam.xref in excluded_families:
            continue
        for e in fam.events:
            if not e.place:
                continue
            slot = places.setdefault(e.place, {"n": 0, "ev": []})
            if e.coords and "c" not in slot:
                slot["c"] = _coords_json(e.coords)
            slot["n"] += 1
            slot["ev"].append(["F" + fam.xref.strip("@"), e.tag,
                               e.date.year if e.date else None,
                               e.date.raw if e.date else None])
    # sort each place's events by year for the place page
    for slot in places.values():
        slot["ev"].sort(key=lambda r: (r[2] is None, r[2] or 0))

    # ---- sources --------------------------------------------------------
    sources = {}
    for sx, s in model.sources.items():
        sources[sx.strip("@")] = {
            "title": s.title,
            **({"author": s.author} if s.author else {}),
            **({"pub": s.publication} if s.publication else {}),
            **({"repo": s.repo.strip("@")} if s.repo else {}),
            **({"callno": s.callno} if s.callno else {}),
        }

    # ---- repositories ----------------------------------------------------
    repos = {rx.strip("@"): {"name": r.name, **({"note": r.note} if r.note else {})}
             for rx, r in model.repos.items()}

    # ---- media manifest (visible media only) ----------------------------
    # Grouped by path; every focus rectangle known for the file is carried
    # as regions-by-person, so the viewer can draw the right outline for
    # whichever person's page is open.
    media = {}
    for xref, m in sorted(model.media_by_xref.items(),
                          key=lambda kv: kv[1].path):
        if m.path in skip_media or not m.path:
            continue
        entry = media.get(m.path)
        if entry is None:
            entry = {"oid": [], "form": m.form}
            if m.title:
                entry["title"] = m.title
            if m.checksum:
                entry["md5"] = m.checksum
            if regions and regions.get(m.path):
                by_person = {}
                for e in regions[m.path]:
                    rect = list(e["region"])
                    for pid in e["persons"]:
                        by_person[pid] = rect
                if by_person:
                    entry["regions"] = by_person
                elif len(regions[m.path]) == 1:
                    entry["region"] = list(regions[m.path][0]["region"])
            media[m.path] = entry
        if m.object_id and m.object_id not in entry["oid"]:
            entry["oid"].append(m.object_id)

    # ---- families --------------------------------------------------------
    families = {fx.strip("@"): family_json(model, f, withheld)
                for fx, f in model.families.items()
                if fx not in excluded_families}

    # ---- person shards ----------------------------------------------------
    n_shards = 0
    for x, p in model.people.items():
        if x in excluded_people:
            continue
        if p.name.given == LIVING_GIVEN:
            shard = living_stub(model, x)
        else:
            shard = person_shard(model, x, regions=regions, withheld=withheld)
        (out / "people" / f"{x.strip('@')}.json").write_text(
            json.dumps(shard, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
        n_shards += 1

    meta = {
        "built": model.header.get("DATE", ""),
        "source": model.header.get("SOUR", ""),
        "media_version": media_version,
        "media_base": media_base,
        "counts": {
            "people": len(index),
            "families": len(families),
            "sources": len(sources),
            "media": len(media),
            "places": len(places),
            "geocoded_places": sum(1 for v in places.values() if "c" in v),
        },
    }

    (out / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    (out / "surnames.json").write_text(
        json.dumps(dict(sorted(by_surname.items())), ensure_ascii=False,
                   separators=(",", ":")), encoding="utf-8")
    (out / "places.json").write_text(
        json.dumps(dict(sorted(places.items())), ensure_ascii=False,
                   separators=(",", ":")), encoding="utf-8")
    (out / "sources.json").write_text(
        json.dumps(sources, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    (out / "repos.json").write_text(
        json.dumps(repos, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    (out / "media.json").write_text(
        json.dumps(media, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    (out / "families.json").write_text(
        json.dumps(families, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

    return meta
