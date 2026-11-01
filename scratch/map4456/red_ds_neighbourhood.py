# What is actually near each red D-S label that equals a row total?
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
rows_by_total = collections.defaultdict(list)
for n, rt in row_total.items():
    rows_by_total[rt].append(n)

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
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
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
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})

print("red D-S labels and their neighbourhoods:")
for p in sorted(ds, key=lambda p: -p["d"] * 2400 - p["s"]):
    v = p["d"] * 2400 + p["s"]
    rows = rows_by_total.get(v, [])
    near = sorted(((math.hypot(s["x"] - p["x"], s["y"] - p["y"]), s["v"])
                   for s in sites), key=lambda t: t[0])[:6]
    print("  %-8s at (%5.0f,%5.0f) = row %s total" % (
        p["text"], p["x"], p["y"], rows or "-"))
    print("      red values within 900 px: %s" %
          ["%d@%d" % (v_, int(d_)) for d_, v_ in near])
