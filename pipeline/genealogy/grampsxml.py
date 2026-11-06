# The data.gramps reader (PLAN.md sections 4.2 and the media-region rule).
#
# The GEDCOM export drops two things the editor wants: the focus rectangles
# drawn on media references (Gramps calls them regions; 1,456 live on the
# objref elements, in percent coordinates) and the media checksums. The
# gpkg's data.gramps has both.
#
# Regions belong to the reference, not the file: a headstone photograph is
# often one file behind two media objects, one per spouse, each with its own
# rectangle. So the map this module returns is keyed by media path and each
# entry lists the persons the rectangle belongs to; the viewer shows the
# rectangle drawn for the person whose page is open, or none.
#
# Person and source ids match the GEDCOM xrefs one to one (verified against
# the 2026-11-05 export: 4,439/4,439 people, 440/440 sources), so no fuzzy
# joining is needed anywhere.

from __future__ import annotations

import gzip
import re
import shutil
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path


def ensure_extracted(gpkg_path: str, cache_dir: str) -> Path:
    """Unpack data.gramps from the gpkg into the cache (once) and return the
    decompressed XML path. The gpkg is a tar.gz whose data.gramps is itself
    gzipped; the 4.9 GB scan takes about a minute the first time."""
    cache = Path(cache_dir)
    out = cache / "data.gramps.xml"
    if out.exists() and out.stat().st_size > 1_000_000:
        return out
    raw = cache / "data.gramps"
    if not raw.exists():
        cache.mkdir(parents=True, exist_ok=True)
        import tarfile
        with tarfile.open(gpkg_path, "r|gz") as tf:
            for entry in tf:
                if entry.name.split("/")[-1] == "data.gramps":
                    with tf.extractfile(entry) as src, open(raw, "wb") as dst:
                        dst.write(src.read())
                    break
            else:
                raise FileNotFoundError("data.gramps not found in " + gpkg_path)
    with gzip.open(raw, "rb") as src, open(out, "wb") as dst:
        shutil.copyfileobj(src, dst)
    return out


def _strip_drive(src: str) -> str:
    m = re.match(r"^[A-Za-z]:[/\\](.*)$", src or "")
    if m:
        src = m.group(1)
    return unicodedata.normalize("NFC", src.replace("\\", "/").lstrip("/"))


def read_regions(xml_path: str) -> dict:
    """Returns {'regions': path -> [{'region': (x1,y1,x2,y2) percent,
    'persons': [I-ids]}], 'checksum': path -> md5, 'object_id': path -> O-id,
    'stats': {...}}.

    Ownership: each objref is traced upward to its holding record - a person
    directly, or an event or citation, which are resolved to the persons and
    families that reference them (family owners expand to their members, so
    the viewer can match a spouse)."""
    root = ET.parse(xml_path).getroot()
    m = re.match(r"\{(.+?)\}", root.tag)
    ns = "{%s}" % m.group(1)

    objects = {}          # handle -> path
    obj_id = {}
    checksum = {}
    for obj in root.find(ns + "objects"):
        h = obj.get("handle")
        f = obj.find(ns + "file")
        if f is None:
            continue
        path = _strip_drive(f.get("src", ""))
        objects[h] = path
        obj_id[h] = obj.get("id")
        checksum[h] = f.get("checksum", "")

    people = {p.get("handle"): p for p in root.find(ns + "people")}
    families = {f.get("handle"): f for f in root.find(ns + "families")}
    events = {e.get("handle"): e for e in root.find(ns + "events")}
    citations = {c.get("handle"): c for c in root.find(ns + "citations")}

    # event handle -> referencing person/family handles; citation handle ->
    # referencing person/family/event handles. Handles throughout: ids are
    # read off the elements when the owner is finally resolved.
    event_holders: dict = {}
    citation_holders: dict = {}
    for h, p in people.items():
        for er in p.findall(ns + "eventref"):
            event_holders.setdefault(er.get("hlink"), []).append(h)
        for cr in p.findall(ns + "citationref"):
            citation_holders.setdefault(cr.get("hlink"), []).append(h)
    for h, f in families.items():
        for er in f.findall(ns + "eventref"):
            event_holders.setdefault(er.get("hlink"), []).append(h)
        for cr in f.findall(ns + "citationref"):
            citation_holders.setdefault(cr.get("hlink"), []).append(h)

    for h, ev0 in events.items():
        for cr in ev0.findall(ns + "citationref"):
            citation_holders.setdefault(cr.get("hlink"), []).append(h)

    def expand_to_persons(handles: list) -> list:
        """Resolve owner handles to person ids, expanding families to their
        members and events to the people that reference them."""
        out = []
        for h in handles or []:
            if h in people:
                out.append(people[h].get("id"))
            elif h in families:
                f = families[h]
                for rel in ("father", "mother"):
                    ref = f.find(ns + rel)
                    if ref is not None and ref.get("hlink") in people:
                        out.append(people[ref.get("hlink")].get("id"))
                for cr in f.findall(ns + "childref"):
                    if cr.get("hlink") in people:
                        out.append(people[cr.get("hlink")].get("id"))
            elif h in events:
                out.extend(expand_to_persons(event_holders.get(h, [])))
        return sorted(set(out))

    regions: dict = {}
    objref_count = 0
    with_region = 0

    def collect(objref, persons):
        nonlocal with_region
        path = objects.get(objref.get("hlink"))
        if not path:
            return
        reg = objref.find(ns + "region")
        if reg is None:
            return
        with_region += 1
        regions.setdefault(path, []).append({
            "region": (float(reg.get("corner1_x")), float(reg.get("corner1_y")),
                       float(reg.get("corner2_x")), float(reg.get("corner2_y"))),
            "persons": persons,
        })

    # people hold their gallery media directly
    for h, p in people.items():
        for objref in p.findall(ns + "objref"):
            objref_count += 1
            collect(objref, [p.get("id")])
    # events and citations hold theirs on behalf of the people and families
    # that reference them (the holder maps already carry those ids)
    for h, ev in events.items():
        for objref in ev.findall(ns + "objref"):
            objref_count += 1
            collect(objref, expand_to_persons([h]))
    for h, c in citations.items():
        for objref in c.findall(ns + "objref"):
            objref_count += 1
            collect(objref, expand_to_persons(citation_holders.get(h, [])))

    return {
        "regions": regions,
        "checksum": {path: checksum[h] for h, path in objects.items()},
        "object_id": {path: obj_id[h] for h, path in objects.items()},
        "stats": {"objrefs": objref_count, "regions": with_region,
                  "paths": len(objects)},
    }
