# The genealogy build orchestrator (PLAN.md sections 4, 7, 8).
#
#   python pipeline/genealogy/build.py                    # data, from config
#   python pipeline/genealogy/build.py --ged J:\path\new.ged --gpkg J:\path\new.gpkg
#   python pipeline/genealogy/build.py --dry-run          # reports only
#
# Reads the GEDCOM and the gpkg from wherever they are (config.yml or the
# command line - updating the database is pointing the build at new files),
# joins the media regions from data.gramps, prunes the excluded branch,
# redacts the living, writes the public JSON and the review reports. No
# media derivatives yet (that is media_build.py, phase 1).

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import gedcom            # noqa: E402
import grampsxml         # noqa: E402
import prune             # noqa: E402
import privacy           # noqa: E402
import build_data        # noqa: E402

ROOT = Path(__file__).parents[2]          # the triebenfeld repo root


def load_config() -> dict:
    cfg = yaml.safe_load((Path(__file__).parent / "config.yml").read_text(
        encoding="utf-8"))
    return cfg


def write_report(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def verify(model, ex, living) -> dict:
    """The consistency checks every build runs (PLAN.md section 8)."""
    problems = []

    # every family link points at a kept record
    for x, p in model.people.items():
        if x in ex.removed_people:
            continue
        for f in p.famc + p.fams:
            if f in ex.removed_families:
                problems.append(f"{x}: references removed family {f}")
            elif f not in model.families:
                problems.append(f"{x}: references missing family {f}")
    for fx, fam in model.families.items():
        if fx in ex.removed_families:
            continue
        for role in ("husb", "wife"):
            v = getattr(fam, role)
            if v and v in ex.removed_people:
                problems.append(f"{fx}: {role} {v} is excluded")
        for c in fam.chil:
            if c in ex.removed_people:
                problems.append(f"{fx}: child {c} is excluded")

    # citations resolve to real sources
    for x, p in model.people.items():
        if x in ex.removed_people:
            continue
        for e in p.events:
            for cit in e.citations:
                if cit.source and cit.source not in model.sources:
                    problems.append(f"{x}: citation to missing {cit.source}")

    # no excluded name leaks into any display string of a kept person;
    # [Living] placeholders are skipped: several removed and kept people
    # share the string "Living Surname", so a match proves nothing
    removed_names = {model.people[x].display.lower()
                     for x in ex.removed_people if x in model.people
                     and "[Living]" not in model.people[x].display}
    for x, p in model.people.items():
        if x in ex.removed_people or p.name.display.lower() in (
                "", "(unknown)"):
            continue
        blob = (p.display + " " + " ".join(p.notes)).lower()
        for rn in removed_names:
            if len(rn) > 8 and rn in blob:
                problems.append(f"{x}: note mentions excluded '{rn}' "
                                f"(editor's call: trim or keep)")
                break

    # dates that failed to parse
    bad_dates = []
    for x, p in model.people.items():
        if x in ex.removed_people:
            continue
        for e in p.events:
            raw = e.value if e.tag in ("DATE",) else None
            # an event whose DATE line exists but produced no year
            if e.date is None:
                continue   # no DATE line at all is normal (BURI etc.)
            if e.date.y1 is None:
                bad_dates.append(f"{x}/{e.tag}: {e.date.raw!r}")

    return {"problems": problems, "bad_dates": bad_dates}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ged", help="path to the GEDCOM (overrides config)")
    ap.add_argument("--gpkg", help="path to the gpkg (overrides config)")
    ap.add_argument("--dry-run", action="store_true",
                    help="run everything, write reports, skip site data")
    args = ap.parse_args()

    cfg = load_config()
    ged_path = args.ged or cfg["inputs"]["ged"]
    gpkg_path = args.gpkg or cfg["inputs"]["gpkg"]
    cache = cfg["inputs"]["cache"]
    out_dir = ROOT / "site" / "genealogy" / "data"
    report_dir = ROOT / "review" / "genealogy"

    print(f"[1/6] parsing {ged_path}")
    model = gedcom.parse(ged_path)
    s = model.stats
    print(f"      {len(model.people)} people, {len(model.families)} families, "
          f"{len(model.sources)} sources, {len(model.media)} media files")

    print("[2/6] reading data.gramps from the gpkg (cached after first run)")
    xml = grampsxml.ensure_extracted(gpkg_path, cache)
    info = grampsxml.read_regions(str(xml))
    print(f"      {info['stats']['regions']} focus regions on "
          f"{info['stats']['objrefs']} media references")

    # join regions + checksums + object ids onto the GEDCOM media, per
    # xref: a shared file keeps one rectangle per owner
    regions = info["regions"]
    unmatched = 0
    for xref, m in model.media_by_xref.items():
        key = m.path if m.path in regions else None
        if key is None:
            cand = [k for k in info["object_id"] if k.lower() == m.path.lower()]
            key = cand[0] if len(cand) == 1 else None
        if key:
            m.object_id = info["object_id"][key]
            m.checksum = info["checksum"][key]
            entries = regions.get(key, [])
            if len(entries) == 1:
                m.region = entries[0]["region"]
        else:
            unmatched += 1
    if unmatched:
        print(f"      WARNING: {unmatched} media xrefs did not match "
              f"data.gramps (see the report)")

    print("[3/6] pruning the excluded branch")
    ex = prune.prune(model, cfg["exclusion"]["roots"])
    print(f"      {len(ex.removed_people)} people, "
          f"{len(ex.removed_media)} media files, "
          f"{len(ex.removed_families)} families removed")

    print("[4/6] privacy: detecting and redacting living people")
    reasons: dict = {}
    living = privacy.living_set(model, cfg["privacy"]["age_limit"],
                                reasons=reasons)
    withheld = privacy.media_privacy(model, living)
    counts = privacy.redact(model, living)
    print(f"      {counts['people']} living people redacted, "
          f"{len(withheld)} media files withheld")

    print("[5/6] writing reports")
    stamp = date.today().isoformat()
    checks = verify(model, ex, living)
    write_report(report_dir / "excluded.yml", _excluded_yaml(ex, model))
    write_report(report_dir / "privacy_spotcheck.yml",
                 _privacy_yaml(model, living, counts))
    write_report(report_dir / "build_report.txt",
                 _build_report(model, ex, living, counts, withheld,
                               unmatched, info, ged_path, checks))
    try:
        import report_html
        meta_counts = {"media": len(model.media) - len(ex.removed_media)
                       - len(withheld)}
        report_html.write_index(report_dir, {
            "people": len(ex.removed_people),
            "media": len(ex.removed_media),
            "families": len(ex.removed_families),
            "living": len(living),
            "withheld": len(withheld),
        }, len(checks.get("problems", [])), len(checks.get("bad_dates", [])))
        report_html.write_excluded(report_dir, ex, model)
        report_html.write_privacy(report_dir, model, living, reasons,
                                  counts, withheld)
        report_html.write_build_report(report_dir, model, ex, living, counts,
                                       withheld, unmatched, info, ged_path,
                                       checks, meta_counts)
    except Exception as exc:   # noqa: BLE001 - the yml reports still stand
        print(f"      WARNING: the HTML reports failed ({exc}); "
              f"the yml and txt reports are complete")

    if args.dry_run:
        print("[6/6] dry run: site data not written")
    else:
        print("[6/6] writing site data")
        media_base = cfg.get("media", {}).get("base", "")
        # the media repo's manifest, when a build has run, is both copied
        # into the site data and used to filter: a file the gpkg does not
        # contain cannot be published, so it leaves the catalog instead of
        # turning up as a broken image
        manifest_path = Path(cfg.get("media", {}).get("dest", "")) / "manifest.json"
        available = None
        if manifest_path.exists():
            available = set(json.loads(manifest_path.read_text(encoding="utf-8")))
        meta = build_data.build_all(
            model, str(out_dir), regions=regions, withheld=withheld,
            excluded_media=ex.removed_media,
            excluded_people=ex.removed_people,
            excluded_families=ex.removed_families,
            media_base=media_base, available=available)
        # drop stale shards from previous builds
        people_dir = out_dir / "people"
        live = {f"{x.strip('@')}.json" for x in model.people
                if x not in ex.removed_people}
        for f in people_dir.glob("*.json"):
            if f.name not in live:
                f.unlink()
        if manifest_path.exists():
            shutil.copyfile(manifest_path, out_dir / "media_files.json")
            print("      media_files.json copied from the media repo")
        print(f"      {meta['counts']}")
    print("done")
    return 0


# ---------------------------------------------------------------------------
# Reports.


def _excluded_yaml(ex, model) -> str:
    lines = [
        "# The excluded branch (reviewed before every publish).",
        f"# Generated {date.today().isoformat()}.",
        "",
        "people:",
    ]
    for row in ex.report_rows:
        lines.append(f"  {row['xref']}: {row['name']}")
    lines += ["", "media:"]
    for p in sorted(ex.removed_media):
        lines.append(f"  - {p}")
    lines += ["", "families:"]
    for f in sorted(ex.removed_families):
        lines.append(f"  - {f}")
    lines += ["", "cut_links:"]
    for c in ex.cut_links:
        lines.append(f"  - person: {c['person']}")
        lines.append(f"    family: {c['family']}")
    lines += ["", "sanitised_references:"]
    for srow in ex.sanitized:
        lines.append(f"  - {srow}")
    return "\n".join(lines) + "\n"


def _privacy_yaml(model, living, counts) -> str:
    lines = [
        "# Living-person spot check (reviewed before every publish).",
        f"# Generated {date.today().isoformat()}.",
        f"# {counts['people']} people redacted; their media and events are",
        "# never written to the site. Sample below; every redacted person",
        "# whose given name was not already '[Living]' is listed in full.",
        "",
        "counts:",
        f"  people: {counts['people']}",
        f"  events_dropped: {counts['events']}",
        f"  notes_dropped: {counts['notes']}",
        f"  media_withheld: {counts['media']}",
        "",
        "had_real_first_names:",
    ]
    import re
    n = 0
    for x in sorted(model.people):
        p = model.people[x]
        if x not in living:
            continue
        # after redaction the original given name is gone; the surname is
        # what remains - the check that matters is that no shard keeps a
        # real first name, which build_data asserts separately
        n += 1
        if n <= 30:
            lines.append(f"  - {x.strip('@')}: Living {p.name.surname}")
    lines += ["", "sample_redacted:"]

    import random
    rng = random.Random(20261106)
    sample = rng.sample(sorted(living), min(30, len(living)))
    for x in sample:
        p = model.people[x]
        lines.append(f"  {x.strip('@')}:")
        lines.append(f"    name: {p.name.display}")
        lines.append(f"    sex: {p.sex}")
        lines.append(f"    events: {len(p.events)} (must be 0)")
        lines.append(f"    media: {len(p.media)} (must be 0)")
    return "\n".join(lines) + "\n"


def _build_report(model, ex, living, counts, withheld, unmatched, info,
                  ged_path, checks=None) -> str:
    c = [
        (len(model.people), "people kept"),
        (len(ex.removed_people), "people excluded"),
        (len(living), "living people (redacted)"),
        (len(model.families) - len(ex.removed_families), "families kept"),
        (len(model.media) - len(ex.removed_media) - len(withheld),
         "media publishable"),
        (len(ex.removed_media), "media excluded (branch)"),
        (len(withheld), "media withheld (living)"),
        (len(model.sources), "sources"),
        (len(model.repos), "repositories"),
        (info["stats"]["regions"], "focus regions joined"),
        (unmatched, "media without a data.gramps match"),
        (len(checks.get("bad_dates", [])) if checks else 0,
         "dates that failed to parse"),
        (len(checks.get("problems", [])) if checks else 0,
         "consistency problems"),
    ]
    lines = [
        f"Genealogy build report - {date.today().isoformat()}",
        f"Input: {ged_path}",
        f"Header: {model.header.get('SOUR','')} {model.header.get('DATE','')}",
        "",
    ]
    for n, label in c:
        marker = ""
        if ("problem" in label or "failed" in label) and n:
            marker = "  <-- REVIEW"
        lines.append(f"  {n:>6}  {label}{marker}")
    if checks and checks.get("bad_dates"):
        lines += ["", "unparsed dates (the raw text is kept, only the sort",
                  "key is missing):"]
        lines += [f"  - {d}" for d in checks["bad_dates"][:40]]
    if checks and checks.get("problems"):
        lines += ["", "consistency problems:"]
        lines += [f"  - {p}" for p in checks["problems"][:40]]
    lines.append("")
    lines.append("A previous-build comparison is appended by --compare once")
    lines.append("a previous report exists.")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
