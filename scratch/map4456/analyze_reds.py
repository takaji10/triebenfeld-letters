# What are the red numbers? The editor's complete catalogue (reds_all.json,
# 437 readings with user-corrected positions) against the statement:
#   1) spatial clustering per value (do the sites of one value group?)
#   2) the red D-S pairs against the statement's columns directly
#   3) red n near black D-S parcels summing to row n (the farm-number test,
#      now with true positions)
import json
import re
import math
import itertools
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}
colidx = {}
for rn in stmt:
    if not rn.isdigit():
        continue
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        d_, s_ = row[col]["des"], row[col]["saz"]
        if s_ >= 100 and d_ <= 60:
            colidx.setdefault((d_, s_), []).append((int(rn), col))

def canon(t):
    t = t.strip()
    unc = "[" in t
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip(), unc

# all red readings with positions
sites = []       # {v, x, y, unc}
ds_red = []      # {d, s, x, y, unc}
for a in D["answered"]:
    c, unc = canon(a["text"])
    x = a["x"]; y = a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
        ds_red.append({"d": int(m.group(1)), "s": int(m.group(2)),
                       "x": x, "y": y, "unc": unc})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
for n in D["added"]:
    c, unc = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
        ds_red.append({"d": int(m.group(1)), "s": int(m.group(2)),
                       "x": x, "y": y, "unc": unc})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
print("red sites:", len(sites), " red D-S pairs:", len(ds_red))

# ---- 2) the red D-S pairs against the statement's columns --------------------
print("\n== red D-S pairs vs the statement's columns ==")
hit = 0
for p in ds_red:
    refs = colidx.get((p["d"], p["s"]))
    if refs:
        hit += 1
        if hit <= 12:
            print("  %d-%d at (%5.0f,%5.0f)%s -> %s" % (
                p["d"], p["s"], p["x"], p["y"],
                " [unc]" if p["unc"] else "",
                ", ".join("%s/%s" % r for r in refs)))
print("red D-S matching a statement column exactly: %d of %d" % (hit, len(ds_red)))

# ---- 1) spatial clustering per value ----------------------------------------
print("\n== spatial clustering of the red values ==")
by_v = collections.defaultdict(list)
for s in sites:
    by_v[s["v"]].append((s["x"], s["y"], s["unc"]))

def spread(pts):
    if len(pts) < 2:
        return 0
    ds = [math.hypot(a[0] - b[0], a[1] - b[1])
          for i, a in enumerate(pts) for b in pts[i + 1:]]
    return sum(ds) / len(ds)

allpos = [(s["x"], s["y"]) for s in sites]
import random
rng = random.Random(4)
ctrl = []
for _ in range(2000):
    k = rng.choice([len(v) for v in by_v.values() if len(v) >= 2])
    pts = rng.sample(allpos, k)
    ctrl.append(spread(pts))
ctrl.sort()
print("control (random positions, same counts): p25 %.0f p50 %.0f" %
      (ctrl[len(ctrl) // 4], ctrl[len(ctrl) // 2]))
tight, mid, wide = 0, 0, 0
for v in sorted(by_v):
    pts = by_v[v]
    if len(pts) < 2:
        continue
    sp = spread(pts)
    tag = "TIGHT" if sp < ctrl[len(ctrl) // 4] else ("mid" if sp < ctrl[len(ctrl) // 2] else "WIDE")
    if tag == "TIGHT":
        tight += 1
    elif tag == "WIDE":
        wide += 1
    else:
        mid += 1
    if len(pts) >= 3 or tag == "TIGHT":
        print("  red %2d x%d spread %5.0f px  %s" % (v, len(pts), sp, tag))
print("values with >=2 sites: TIGHT %d, mid %d, WIDE %d" % (tight, mid, wide))

# the 97 anomaly
pts97 = by_v.get(97, [])
print("\nred 97: %d sites" % len(pts97))
if pts97:
    xs = [p[0] for p in pts97]; ys = [p[1] for p in pts97]
    print("  x %d..%d  y %d..%d" % (min(xs), max(xs), min(ys), max(ys)))
    print("  first 12:", [(int(x), int(y)) for x, y, u in pts97[:12]])
