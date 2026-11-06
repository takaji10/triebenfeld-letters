# The media derivative builder (PLAN.md section 4.5).
#
# Turns the gpkg's originals into the web copies the media repo publishes:
# a display JPEG (long edge <= 2000 px, quality 80, progressive, metadata
# stripped) and a 400 px thumbnail for every image; PDFs for the docx files
# when LibreOffice is available. Derivatives are named by content hash, so
# every build only adds files and nothing ever changes under a published
# URL.
#
#   python pipeline/genealogy/media_build.py --dest J:\genealogy-media
#
# Everything withheld (living people) or excluded (the pruned branch) is
# skipped here too, so the media repo never contains what the site may not
# show. The manifest.json this writes is the join between the site's media
# paths and the published URLs.

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
from datetime import date
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parent))

MAX_EDGE = 2000
THUMB_EDGE = 400
JPEG_QUALITY = 80

Image.MAX_IMAGE_PIXELS = 300_000_000   # genealogy scans are big but trusted


def _hash_name(data: bytes, ext: str, suffix: str = "") -> str:
    h = hashlib.sha1(data).hexdigest()[:10]
    return f"{h}{suffix}.{ext}"


def _jpeg_bytes(img: Image.Image) -> bytes:
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_EDGE:
        scale = MAX_EDGE / max(w, h)
        img = img.resize((round(w * scale), round(h * scale)),
                         Image.LANCZOS)
    out = BytesIO()
    img.save(out, "JPEG", quality=JPEG_QUALITY, progressive=True,
             optimize=True)
    return out.getvalue(), img.size


def _avatar_bytes(img: Image.Image, region=None) -> bytes:
    """A face avatar: the region box cropped square around the head and
    scaled to 96 px. The region is the focus rectangle the editor drew
    on the media reference (percent coordinates); without one the image
    is not used as an avatar at all - a whole-scan face is nobody's."""
    w, h = img.size
    if region:
        x1, y1, x2, y2 = region
        cx = (min(x1, x2) + max(x1, x2)) / 200   # percent -> centre
        cy = (min(y1, y2) + max(y1, y2)) / 200
        box_w = abs(max(x1, x2) - min(x1, x2)) / 100 * w
        box_h = abs(max(y1, y2) - min(y1, y2)) / 100 * h
        # square around the box centre, at least the box's own extent
        side = max(box_w, box_h) * 1.15
        side = min(side, min(w, h))
        left = max(0, min(w - side, cx * w - side / 2))
        top = max(0, min(h - side, cy * h - side / 2))
        img = img.crop((int(left), int(top),
                        int(left + side), int(top + side)))
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    img = img.resize((96, 96), Image.LANCZOS)
    out = BytesIO()
    img.save(out, "JPEG", quality=82, optimize=True)
    return out.getvalue()


def _thumb_bytes(img: Image.Image) -> bytes:
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    img.thumbnail((THUMB_EDGE, THUMB_EDGE), Image.LANCZOS)
    out = BytesIO()
    img.save(out, "JPEG", quality=80, progressive=True, optimize=True)
    return out.getvalue(), img.size


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dest", required=True,
                    help="working copy of the genealogy-media repo")
    ap.add_argument("--ged", help="GEDCOM path (default: config.yml)")
    ap.add_argument("--gpkg", help="gpkg path (default: config.yml)")
    ap.add_argument("--limit", type=int, default=0,
                    help="process only the first N files (testing)")
    ap.add_argument("--report", action="store_true",
                    help="only report what would be built")
    args = ap.parse_args()

    import yaml
    here = Path(__file__).parent
    cfg = yaml.safe_load((here / "config.yml").read_text(encoding="utf-8"))
    ged_path = args.ged or cfg["inputs"]["ged"]
    gpkg_path = args.gpkg or cfg["inputs"]["gpkg"]

    import gedcom
    import grampsxml
    import prune
    import privacy
    import build_data

    print("[1/4] parsing the GEDCOM")
    model = gedcom.parse(ged_path)
    xml = grampsxml.ensure_extracted(gpkg_path, cfg["inputs"]["cache"])
    info = grampsxml.read_regions(str(xml))
    for xref, m in model.media_by_xref.items():
        key = m.path if m.path in info["regions"] else None
        if key:
            m.object_id = info["object_id"][key]
            m.checksum = info["checksum"][key]
    print(f"      {len(model.media_by_xref)} media objects")

    print("[2/4] exclusion + privacy filters")
    ex = prune.prune(model, cfg["exclusion"]["roots"],
                     extra_people=cfg["exclusion"].get("people"))
    living = privacy.living_set(model, cfg["privacy"]["age_limit"])
    withheld = privacy.media_privacy(model, living)
    skip = ex.removed_media | withheld
    print(f"      {len(ex.removed_media)} excluded, "
          f"{len(withheld)} withheld -> {len(model.media)} to build")

    # the avatar crops: person -> (media path, region rect) for the
    # photo/portrait-named media the person owns or is cited in, keyed
    # by the focus rectangle the editor drew on that reference. The
    # region ids come from data.gramps bare (I0001), the GEDCOM xrefs
    # wrapped (@I0001@) - joined through the strip.
    avatar_jobs = {}
    title_re = re.compile(r"photo|portrait|porträt", re.I)
    for x, p in model.people.items():
        if x in ex.removed_people or x in living:
            continue
        bare = x.strip("@")
        cands = []
        for m in p.media:
            if m.path and m.path not in skip:
                cands.append(m)
        for e in p.events:
            for cit in e.citations:
                for m in cit.media:
                    if m.path and m.path not in skip:
                        cands.append(m)
        for m in cands:
            region = None
            entries = info["regions"].get(m.path, [])
            for entry in entries:
                if bare in entry["persons"]:
                    region = entry["region"]
                    break
            if not region:
                continue
            avatar_jobs[x] = (m.path, region)
            break
    print(f"      {len(avatar_jobs)} avatars to crop (region-boxed faces)")

    # what to build: path -> primary Media (title, form, oid)
    wanted = {}
    for path, m in model.media.items():
        if path in skip or not path:
            continue
        wanted[path] = m

    dest = Path(args.dest)
    media_dir = dest / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    print("[3/4] reading the gpkg and converting")
    manifest = {}
    total_bytes = 0
    errors = []
    docx_pending = []
    # the avatar crops, harvested in the same single tar scan: for every
    # wanted file, the persons whose face regions name it
    crop_wanted = {}
    for x, (path, region) in avatar_jobs.items():
        crop_wanted.setdefault(path, []).append((x, region))
    avatars = {}   # person xref -> avatar file name
    # stream the tar once; extract only the members we want
    norm = lambda name: grampsxml._strip_drive(name)
    with tarfile.open(gpkg_path, "r|gz") as tf:
        for entry in tf:
            if not entry.isfile():
                continue
            path = norm(entry.name)
            m = wanted.get(path)
            if m is None:
                continue
            data = tf.extractfile(entry).read()
            form = m.form or path.rsplit(".", 1)[-1].lower()
            try:
                if form in ("jpg", "jpeg", "png", "tif", "tiff"):
                    img = Image.open(BytesIO(data))
                    img.load()
                    disp, size = _jpeg_bytes(img)
                    thumb, tsize = _thumb_bytes(img)
                    name = _hash_name(data, "jpg")
                    tname = _hash_name(data, "jpg", "_t")
                    (media_dir / name).write_bytes(disp)
                    (media_dir / tname).write_bytes(thumb)
                    manifest[path] = {
                        "file": name, "thumb": tname,
                        "w": size[0], "h": size[1],
                        "form": "jpg", "oid": m.object_id,
                        "orig": form,
                    }
                    total_bytes += len(disp) + len(tsize) + len(data)
                    # the face avatars for this file's persons
                    for x, region in crop_wanted.get(path, []):
                        try:
                            av = _avatar_bytes(img, region)
                            aname = _hash_name(av, "jpg", "_a")
                            (media_dir / aname).write_bytes(av)
                            avatars[x] = aname
                            total_bytes += len(av)
                        except Exception as exc:   # noqa: BLE001
                            errors.append(f"avatar {x} from {path}: {exc}")
                    del img
                elif form == "txt":
                    name = _hash_name(data, "txt")
                    (media_dir / name).write_bytes(data)
                    manifest[path] = {"file": name, "form": "txt",
                                      "oid": m.object_id}
                    total_bytes += len(data)
                elif form == "docx":
                    name = _hash_name(data, "docx")
                    (media_dir / "originals").mkdir(exist_ok=True)
                    (media_dir / "originals" / name).write_bytes(data)
                    docx_pending.append((path, name))
                    manifest[path] = {"file": f"originals/{name}",
                                      "form": "docx", "oid": m.object_id}
                    total_bytes += len(data)
                else:
                    errors.append(f"{path}: unknown form {form}")
            except Exception as exc:   # noqa: BLE001 - reported, not raised
                errors.append(f"{path}: {exc}")
            if args.limit and len(manifest) >= args.limit:
                break

    print(f"      {len(manifest)} files built, "
          f"{total_bytes / 1e6:.0f} MB originals+derivatives in this run")

    # which wanted paths never matched a tar entry? (a GEDCOM FILE path that
    # is not in the gpkg, or whose name drifted after the package was made)
    got = set(manifest)
    missing = sorted(set(wanted) - got)
    if missing:
        print(f"      {len(missing)} wanted files are not in the gpkg "
              f"(name drift or packaged earlier); see the report")

    if docx_pending and not args.report:
        soffice = shutil.which("soffice") or shutil.which("soffice.exe")
        if soffice:
            print(f"      converting {len(docx_pending)} docx via LibreOffice")
            for path, name in docx_pending:
                subprocess.run(
                    [soffice, "--headless", "--convert-to", "pdf",
                     "--outdir", str(media_dir / "originals"),
                     str(media_dir / "originals" / name)],
                    check=False, capture_output=True)
                pdf = (media_dir / "originals" / name).with_suffix(".pdf")
                if pdf.exists():
                    manifest[path]["pdf"] = f"originals/{pdf.name}"
        else:
            print("      NOTE: LibreOffice not found; the docx files keep "
                  "their originals and no PDFs were made")

    print("[4/4] writing manifest + report")
    (dest / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    (dest / "avatars.json").write_text(
        json.dumps(avatars, ensure_ascii=False, indent=1), encoding="utf-8")
    lines = [
        f"Media build - {date.today().isoformat()}",
        f"Files built: {len(manifest)}",
        f"Originals read: {total_bytes / 1e6:.0f} MB",
    ]
    if missing:
        lines += ["", "Wanted but not found in the gpkg "
                  "(check in Gramps: the media was probably renamed or "
                  "added after the package was exported):"]
        lines += [f"  - {p}" for p in missing]
    if errors:
        lines += ["", "errors:"] + [f"  - {e}" for e in errors]
    (dest / "build_report.txt").write_text("\n".join(lines) + "\n",
                                           encoding="utf-8")
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
