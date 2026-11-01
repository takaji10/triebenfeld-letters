# The region labels re-read, take 3: cut each label crop into lines by its
# ink-row projection (stacked text is reliably split this way; EasyOCR's own
# boxes merged/split wrongly - only 9 D-S labels survived), OCR each line,
# then join D-S pairs across lines. Output: region_labels3.json + the
# parcel/lead/stack lists, and the parcel tests re-run.
import json
import math
import re
import collections
import numpy as np
import pyvips
import easyocr

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
reader = easyocr.Reader(["en"], gpu=False,
                        model_storage_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easymodels",
                        user_network_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easynets",
                        verbose=False)

REG = json.load(open(ROOT + r"\scratch\map4456\region_polygon.json", encoding="utf-8"))
POLY = REG["polygon"]
def pip(x, y):
    ins = False
    n = len(POLY)
    for i in range(n):
        x1, y1 = POLY[i]; x2, y2 = POLY[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            ins = not ins
    return ins

RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))

def cluster(group, gap=58):
    n = len(group)
    parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(n):
        a = group[i]
        for j in range(i + 1, n):
            b = group[j]
            gx = max(b["x"] - (a["x"] + a["w"]), a["x"] - (b["x"] + b["w"]))
            gy = max(b["y"] - (a["y"] + a["h"]), a["y"] - (b["y"] + b["h"]))
            if gx <= gap and gy <= gap:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pi] = pj
    out = {}
    for i in range(n):
        out.setdefault(find(i), []).append(group[i])
    return list(out.values())

def split_lines(crop_a, pad=14):
    """cut the crop into text lines by the ink-row projection"""
    R = crop_a[:, :, 0].astype(int); G = crop_a[:, :, 1].astype(int); B = crop_a[:, :, 2].astype(int)
    lum = (R * 299 + G * 587 + B * 114) // 1000
    redness = np.clip(R - np.maximum(G, B), 0, 255)
    ink = ((lum < 150) | (redness > 40))
    prof = ink.mean(axis=1)
    on = prof > 0.045
    lines = []
    y0 = None
    for i, v in enumerate(on):
        if v and y0 is None:
            y0 = i
        elif not v and y0 is not None:
            if i - y0 >= 12:
                lines.append((y0, i))
            y0 = None
    if y0 is not None and len(on) - y0 >= 12:
        lines.append((y0, len(on)))
    return lines

def read_line(crop_a, ys, xs, ink_kind):
    y0, y1 = ys
    sub = crop_a[y0:y1, max(0, xs[0] - 4):min(crop_a.shape[1], xs[1] + 4)]
    if sub.shape[0] < 10 or sub.shape[1] < 8:
        return None
    if ink_kind == "red":
        R = sub[:, :, 0].astype(int); G = sub[:, :, 1].astype(int); B = sub[:, :, 2].astype(int)
        redness = np.clip(R - np.maximum(G, B), 0, 255)
        g = (255 - np.clip(redness * 2.0, 0, 255)).astype(np.uint8)
        sub = np.stack([g] * 3, -1)
    try:
        res = reader.readtext(sub, allowlist="0123456789-/.",
                              text_threshold=0.35, low_text=0.3, link_threshold=0.25)
    except Exception:
        return None
    if not res:
        return None
    res.sort(key=lambda r: min(p[0] for p in r[0]))
    return " ".join(r[1].strip() for r in res), float(min(r[2] for r in res))

def label_lines(g, ink):
    x0 = max(0, min(t["x"] for t in g) - pad_)
    y0 = max(0, min(t["y"] for t in g) - pad_)
    x1 = min(W, max(t["x"] + t["w"] for t in g) + pad_)
    y1 = min(H, max(t["y"] + t["h"] for t in g) + pad_)
    crop = np.frombuffer(im.crop(x0, y0, x1 - x0, y1 - y0).write_to_memory(),
                         np.uint8).reshape(y1 - y0, x1 - x0, 3)
    R = crop[:, :, 0].astype(int); G = crop[:, :, 1].astype(int); B = crop[:, :, 2].astype(int)
    redness = np.clip(R - np.maximum(G, B), 0, 255)
    darkpx = (255 - (R * 299 + G * 587 + B * 114) // 1000) > 100
    xs_ink = ((darkpx) | (redness > 40))
    cols = np.where(xs_ink.any(axis=0))[0]
    xs = (int(cols.min()), int(cols.max())) if len(cols) else (0, crop.shape[1])
    out = []
    for ys in split_lines(crop):
        got = read_line(crop, ys, xs, ink)
        if got:
            out.append({"text": got[0], "conf": round(got[1], 2),
                        "cy": y0 + (ys[0] + ys[1]) // 2})
    return {"ink": ink, "x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0,
            "n_tokens": len(g), "lines": out}

pad_ = 12
labels = []
for ink, toks in (("black", BLACK), ("red", RED)):
    grp = []
    for t in toks:
        cx, cy = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
        if pip(cx, cy):
            grp.append({"ink": ink, **t})
    cs = cluster(grp)
    print(ink, "clusters:", len(cs), flush=True)
    for g in cs:
        labels.append(label_lines(g, ink))
    print(ink, "labels done:", len(labels), flush=True)

json.dump(labels, open(ROOT + r"\scratch\map4456\region_labels3.json", "w",
                       encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- parse the grammar ------------------------------------------------------
def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("O", "0")
    return s.strip(".")

parcels, smalls, redstack, redsingles = [], [], [], []
for lab in labels:
    lines = [clean(l["text"]) for l in lab["lines"] if clean(l["text"])]
    if not lines:
        continue
    cx, cy = lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2
    if lab["ink"] == "red":
        for i, s in enumerate(lines):
            m = re.fullmatch(r"(\d{1,2})[-/](\d{3,4})", s)
            if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
                redstack.append({"d": int(m.group(1)), "s": int(m.group(2)),
                                 "x": cx, "y": cy})
            elif re.fullmatch(r"\d{3,4}", s) and i > 0 and re.fullmatch(r"\d{1,2}", lines[i - 1]):
                redstack.append({"d": int(lines[i - 1]), "s": int(s), "x": cx, "y": cy})
            elif re.fullmatch(r"\d{2}", s):
                redsingles.append({"v": int(s), "x": cx, "y": cy})
            elif re.fullmatch(r"\d{3,4}", s):
                redsingles.append({"v": int(s), "x": cx, "y": cy})
        continue
    d = s = None
    for i, s_ in enumerate(lines):
        m = re.fullmatch(r"(\d{1,2})[-/](\d{3,4})", s_)
        if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
            d, s = int(m.group(1)), int(m.group(2))
    if d is None:
        for i, s_ in enumerate(lines):
            m = re.fullmatch(r"(\d{1,2})[-/]+", s_)
            if m and i + 1 < len(lines):
                m2 = re.fullmatch(r"(\d{3,4})", lines[i + 1])
                if m2 and int(m.group(1)) <= 60 and int(m2.group(1)) <= 2399:
                    d, s = int(m.group(1)), int(m2.group(1))
    if d is None:
        for i, s_ in enumerate(lines):
            m = re.fullmatch(r"[-/](\d{3,4})", s_)
            if m and i > 0:
                m2 = re.fullmatch(r"(\d{1,2})", lines[i - 1])
                if m2 and int(m2.group(1)) <= 60:
                    d, s = int(m2.group(1)), int(m.group(1))
    if d is not None:
        parcels.append({"d": d, "s": s, "x": cx, "y": cy})
    elif len(lines) == 1 and re.fullmatch(r"\d{1,2}", lines[0]) and 1 <= int(lines[0]) <= 12:
        smalls.append({"v": int(lines[0]), "x": cx, "y": cy})

print("\nblack D-S parcels:", len(parcels))
print("black smalls 1..12:", len(smalls))
print("red stacked pairs:", len(redstack))
print("red singles:", len(redsingles))
json.dump({"parcels": parcels, "smalls": smalls,
           "redstack": redstack, "redsingles": redsingles},
          open(ROOT + r"\scratch\map4456\region_parsed.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---- the parcel tests ---------------------------------------------------------
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

# attach smalls to parcels below
used = set()
for sm in smalls:
    best = None
    for p in parcels:
        if id(p) in used:
            continue
        if abs(p["x"] - sm["x"]) > 170:
            continue
        dy = p["y"] - sm["y"]
        if not (6 <= dy <= 260):
            continue
        if best is None or dy < best[0]:
            best = (dy, p)
    if best:
        best[1]["lead"] = sm["v"]
        used.add(id(best[1]))
with_lead = [p for p in parcels if p.get("lead") is not None]
print("\nparcels with a lead attached:", len(with_lead))

# contiguous groups + the lead sequence + sum match
GAP = 340
n = len(parcels)
parent = list(range(n))
def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i
for i in range(n):
    for j in range(i + 1, n):
        if math.hypot(parcels[i]["x"] - parcels[j]["x"],
                      parcels[i]["y"] - parcels[j]["y"]) <= GAP:
            pi, pj = find(i), find(j)
            if pi != pj:
                parent[pi] = pj
groups = collections.defaultdict(list)
for i in range(n):
    groups[find(i)].append(parcels[i])
print("parcel groups:", len(groups))
seq = 0
for g in groups.values():
    leads = sorted(p["lead"] for p in g if p.get("lead") is not None)
    if len(leads) >= 2 and leads == list(range(1, len(leads) + 1)):
        seq += 1
print("groups whose leads run 1..k exactly:", seq)
matched = []
for g in groups.values():
    tot = sum(p["d"] * 2400 + p["s"] for p in g)
    for rn, rt in row_total.items():
        if abs(tot - rt) <= 0.05 * rt:
            matched.append((g, tot, rn, rt))
print("\ngroups summing to a row total within 5%:", len(matched))
for g, tot, rn, rt in matched:
    leads = sorted(p["lead"] for p in g if p.get("lead") is not None)
    print("  %d parcels at (%5.0f,%5.0f) sum %d/%d = row %d %d/%d [%s] leads %s" % (
        len(g), sum(p["x"] for p in g) / len(g), sum(p["y"] for p in g) / len(g),
        tot // 2400, tot % 2400, rn, rt // 2400, rt % 2400,
        stmt[str(rn)]["name"][:24], leads))
