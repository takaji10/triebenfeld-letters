# Exact-sazhen matching (no rounding): every editor D-S label against every
# statement column and total; and each D-S label vs the red value repeated
# around it (is the D-S the area of that red-n cluster's parcels?).
import json
import re
import math
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

def canon(t):
    t = t.strip()
    unc = "[" in t
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip(), unc

sites, ds = [], []
for a in D["answered"]:
    c, unc = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)), "x": x, "y": y,
                   "text": c, "unc": unc})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y})
for n in D["added"]:
    c, unc = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)), "x": x, "y": y,
                   "text": c, "unc": unc})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y})

# exact matches against any statement cell
print("== exact sazhen equality ==")
for p in ds:
    v = p["d"] * 2400 + p["s"]
    hits = []
    for rn in stmt:
        if not rn.isdigit():
            continue
        row = stmt[rn]
        for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
            cv = row[col]["des"] * 2400 + row[col]["saz"]
            if cv == v:
                hits.append("%s/%s" % (rn, col))
    # the dominant red value within 800 px
    near = [(s["v"], math.hypot(s["x"] - p["x"], s["y"] - p["y"]))
            for s in sites if math.hypot(s["x"] - p["x"], s["y"] - p["y"]) <= 800]
    dom = collections.Counter(v_ for v_, _ in near).most_common(1)
    dom = "%s x%d" % (dom[0][0], dom[0][1]) if dom else "-"
    print("  %-8s -> %s   dominant red value within 800px: %s%s" % (
        p["text"], hits or "no exact match", dom, "  [unc]" if p["unc"] else ""))
