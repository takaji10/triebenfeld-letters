# The grammar-aware re-read inside the editor's polygon. The editor's field
# grammar: black parcel labels «n // D-S» (parcel number over area, the dash
# separating desiatinas from sazhens; also single-line "1-1294"), black
# edge figures often hyphen-prefixed (line lengths), red numbers (a second
# system), angles in circles (86° - not land data).
# Method: cluster the region's OCR tokens into label groups by proximity,
# re-OCR each group's merged crop line by line (EasyOCR, dashes kept),
# parse the grammar, then run the three hypothesis tests on the leading
# number: farm-number (sums per n == statement row totals), parcel-index,
# sequential. Output: scratch/map4456/region_labels.json
import json
import math
import re
import numpy as np
import pyvips
import easyocr

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")

REG = json.load(open(ROOT + r"\scratch\map4456\region_polygon.json", encoding="utf-8"))
POLY = REG["polygon"]
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

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

toks = []
for t in RED:
    cx, cy = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
    if pip(cx, cy):
        toks.append({"ink": "red", **t})
for t in BLACK:
    cx, cy = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
    if pip(cx, cy):
        toks.append({"ink": "black", **t})
print("tokens in region:", len(toks))

# ---- cluster tokens into label groups, per ink ------------------------------
GAP = 58
def clusters(group):
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
            if gx <= GAP and gy <= GAP:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pi] = pj
    out = {}
    for i in range(n):
        out.setdefault(find(i), []).append(group[i])
    return list(out.values())

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
reader = easyocr.Reader(["en"], gpu=False,
                        model_storage_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easymodels",
                        user_network_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easynets",
                        verbose=False)

def read_label(g):
    """merged crop of the group, read line by line"""
    x0 = max(0, min(t["x"] for t in g) - 14)
    y0 = max(0, min(t["y"] for t in g) - 14)
    x1 = min(W, max(t["x"] + t["w"] for t in g) + 14)
    y1 = min(H, max(t["y"] + t["h"] for t in g) + 14)
    crop = np.frombuffer(im.crop(x0, y0, x1 - x0, y1 - y0).write_to_memory(),
                         np.uint8).reshape(y1 - y0, x1 - x0, 3)
    try:
        res = reader.readtext(crop, allowlist="0123456789-/. ",
                              text_threshold=0.35, low_text=0.25, link_threshold=0.25)
    except Exception:
        return None
    lines = []
    for box, txt, conf in res:
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        lines.append({"text": txt.strip(), "conf": round(float(conf), 2),
                      "x": x0 + int(min(xs)), "y": x0 and 0 or 0,
                      "cy": y0 + int(sum(ys) / len(ys)),
                      "cx": x0 + int(sum(xs) / len(xs)),
                      "h": int(max(ys) - min(ys))})
    lines.sort(key=lambda l: l["cy"])
    return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0,
            "n_tokens": len(g), "ink": g[0]["ink"], "lines": lines}

labels = []
for ink in ("black", "red"):
    grp = [t for t in toks if t["ink"] == ink]
    cs = clusters(grp)
    print(ink, "clusters:", len(cs), flush=True)
    for g in cs:
        r = read_label(g)
        if r:
            labels.append(r)
print("labels read:", len(labels))

# ---- the grammar ------------------------------------------------------------
def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("o", "").replace("O", "")
    s = s.strip(".")
    return s

def parse_label(lab):
    """returns dict: lead (int or None), d, s, raw lines, flags"""
    out = {"lead": None, "d": None, "s": None, "lines": [l["text"] for l in lab["lines"]],
           "flags": []}
    ds_found = None
    for l in lab["lines"]:
        s = clean(l["text"])
        m = re.fullmatch(r"(\d{1,2})[-/.](\d{3,4})", s)
        if m:
            d, sa = int(m.group(1)), int(m.group(2))
            if ds_found is None and d <= 60 and sa <= 2399:
                ds_found = (d, sa)
            else:
                out["flags"].append("second D-S? " + s)
            continue
        m2 = re.fullmatch(r"(\d{1,2})", s)
        if m2:
            v = int(m2.group(1))
            if out["lead"] is None and v <= 99:
                out["lead"] = v
            else:
                out["flags"].append("extra small " + s)
            continue
        m3 = re.fullmatch(r"(\d{3,4})", s)
        if m3:
            v = int(m3.group(1))
            if v <= 2399 and out["s"] is None:
                out["s"] = v
                out["flags"].append("saz-only line")
            continue
        out["flags"].append("unread " + l["text"])
    if ds_found:
        out["d"], out["s"] = ds_found
    elif out["s"] is not None and out["lead"] is not None and out["lead"] <= 60:
        # "n // S" with the dash lost: des = n? ambiguous - flag, not assert
        out["flags"].append("dash lost? n=%d s=%d" % (out["lead"], out["s"]))
    return out

parsed = []
for lab in labels:
    p = parse_label(lab)
    parsed.append({**lab, **p})
json.dump(parsed, open(ROOT + r"\scratch\map4456\region_labels.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

n_ds = sum(1 for p in parsed if p["d"] is not None)
n_lead = sum(1 for p in parsed if p["lead"] is not None)
print("labels:", len(labels), " with D-S:", n_ds, " with a lead number:", n_lead)

# ---- the three hypothesis tests on the lead number --------------------------
by_lead = {}
for p in parsed:
    if p["lead"] is not None and p["d"] is not None:
        by_lead.setdefault(p["lead"], []).append(p["d"] * 2400 + p["s"])
print("\n== test A: leading number = the statement's farm number ==")
hits = 0
for n in sorted(by_lead):
    tot = sum(by_lead[n])
    rt = row_total.get(n)
    if rt and abs(tot - rt) <= 0.15 * rt:
        hits += 1
        print("  n %2d: %d labels, sum %d des-saz %d/%d ~ row %d total %d/%d  MATCH"
              % (n, len(by_lead[n]), tot, tot // 2400, tot % 2400,
                 n, rt // 2400, rt % 2400))
print("A: %d of %d lead values match a row total within 15%%" % (hits, len(by_lead)))

print("\n== test B: distribution of lead values ==")
cnt = {}
for p in parsed:
    if p["lead"] is not None:
        cnt[p["lead"]] = cnt.get(p["lead"], 0) + 1
vals = sorted(cnt.items())
print("  distinct lead values:", len(vals), " range:", vals[0][0], "-", vals[-1][0])
print("  most frequent:", sorted(cnt.items(), key=lambda kv: -kv[1])[:12])
print("  singles:", sum(1 for _, c in vals if c == 1), "of", len(vals))

# ---- exact column matches (a parcel equal to a row-column total) -----------
colidx = {}
for rn in stmt:
    if not rn.isdigit():
        continue
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        d, s = row[col]["des"], row[col]["saz"]
        if s >= 100 and d <= 60:
            colidx.setdefault((d, s), []).append((int(rn), col))
exact = 0
for p in parsed:
    if p["d"] is not None and (p["d"], p["s"]) in colidx:
        exact += 1
print("\nlabels whose D-S equals a statement column exactly:", exact)
