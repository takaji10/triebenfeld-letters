# The parcel-index test: attach the black small numbers (1..8) to the black
# D-S parcels beneath them, group the parcels into contiguous farm groups,
# and check whether each group's leads run 1..k (the editor's reading) —
# plus the red/black per-parcel cross-check (black D-S vs the nearest red
# stacked pair).
import json
import math
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]

def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("o", "").replace("O", "")
    return s.strip(".")

black = [lab for lab in LAB if lab["ink"] == "black"]
red = [lab for lab in LAB if lab["ink"] == "red"]

# ---- 1) rebuild every black label's (lead, d, s) ----------------------------
def label_parse(lab):
    lines = [clean(l) for l in lab["lines"] if clean(l)]
    d = s = None
    for s_ in lines:
        m = re.fullmatch(r"(\d{1,2})[-/](\d{3,4})", s_)
        if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
            d, s = int(m.group(1)), int(m.group(2))
    if d is None:
        for i, s_ in enumerate(lines):
            m = re.fullmatch(r"(\d{1,2})[-/]+", s_)
            if m:
                for j in range(i + 1, len(lines)):
                    m2 = re.fullmatch(r"(\d{3,4})", lines[j])
                    if m2:
                        dd, ss = int(m.group(1)), int(m2.group(1))
                        if dd <= 60 and ss <= 2399:
                            d, s = dd, ss
                        break
    if d is None:
        for i, s_ in enumerate(lines):
            m = re.fullmatch(r"[-/](\d{3,4})", s_)
            if m:
                for j in range(i - 1, -1, -1):
                    m2 = re.fullmatch(r"(\d{1,2})", lines[j])
                    if m2 and int(m2.group(1)) <= 60:
                        d, s = int(m2.group(1)), int(m.group(1))
                        break
                if d is not None:
                    break
    return d, s, lines

parcels, smalls = [], []
for lab in black:
    cx, cy = lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2
    d, s, lines = label_parse(lab)
    if d is not None:
        parcels.append({"d": d, "s": s, "x": cx, "y": cy, "lab": lab, "lead": None})
        continue
    if len(lines) == 1 and re.fullmatch(r"\d{1,2}", lines[0]):
        v = int(lines[0])
        if 1 <= v <= 12:
            smalls.append({"v": v, "x": cx, "y": cy, "lab": lab})
print("black D-S parcels:", len(parcels), " black smalls 1..12:", len(smalls))

# ---- 2) attach each small to the parcel below it ----------------------------
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
with_lead = [p for p in parcels if p["lead"] is not None]
print("parcels with a lead attached:", len(with_lead),
      " leads:", sorted(collections.Counter(p["lead"] for p in with_lead).items()))

# ---- 3) the contiguous groups of parcels ------------------------------------
GAP = 300
n = len(parcels)
parent = list(range(n))
def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i
for i in range(n):
    a = parcels[i]
    for j in range(i + 1, n):
        b = parcels[j]
        if math.hypot(a["x"] - b["x"], a["y"] - b["y"]) <= GAP:
            pi, pj = find(i), find(j)
            if pi != pj:
                parent[pi] = pj
groups = collections.defaultdict(list)
for i in range(n):
    groups[find(i)].append(parcels[i])
print("\nparcel groups (GAP %d): %d" % (GAP, len(groups)))

seq_groups = 0
for g in groups.values():
    leads = sorted(p["lead"] for p in g if p["lead"] is not None)
    if len(leads) >= 2 and leads == list(range(1, len(leads) + 1)):
        seq_groups += 1
print("groups whose leads run 1..k exactly:", seq_groups)
print("\ngroups with >=2 leads (the evidence):")
for g in groups.values():
    leads = sorted((p["lead"], p["d"], p["s"]) for p in g if p["lead"] is not None)
    if len(leads) >= 2:
        tot = sum(p["d"] * 2400 + p["s"] for p in g)
        print("  group at (%5.0f,%5.0f): %d parcels, leads %s, sum %d/%d"
              % (sum(p["x"] for p in g) / len(g), sum(p["y"] for p in g) / len(g),
                 len(g), [l[0] for l in leads], tot // 2400, tot % 2400))

# ---- 4) the red/black per-parcel cross-check --------------------------------
redstack = []
for lab in red:
    lines = [clean(l) for l in lab["lines"] if clean(l)]
    if len(lines) == 2:
        if re.fullmatch(r"\d{1,2}", lines[0]) and re.fullmatch(r"\d{3,4}", lines[1]):
            redstack.append({"d": int(lines[0]), "s": int(lines[1]),
                             "x": lab["x"] + lab["w"] / 2, "y": lab["y"] + lab["h"] / 2})
    elif len(lines) == 1 and re.fullmatch(r"\d{1,2}[-/]\d{3,4}", lines[0]):
        m = re.fullmatch(r"(\d{1,2})[-/](\d{3,4})", lines[0])
        redstack.append({"d": int(m.group(1)), "s": int(m.group(2)),
                         "x": lab["x"] + lab["w"] / 2, "y": lab["y"] + lab["h"] / 2})
print("\nred stacked pairs available:", len(redstack))
agree = 0
for p in parcels:
    for r in redstack:
        if math.hypot(r["x"] - p["x"], r["y"] - p["y"]) <= 300:
            if r["d"] == p["d"] and abs(r["s"] - p["s"]) <= 25:
                agree += 1
                break
print("black parcels with an equal red stack within 300 px:", agree, "of", len(parcels))
