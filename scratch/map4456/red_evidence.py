# The red system, settled: quantify the clustering evidence and the
# statement-row correspondence of the special values (97 = the roads, etc.),
# then write the notes section.
import json
import math
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))

def canon(t):
    t = t.strip()
    unc = "[" in t
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip(), unc

sites = []
for a in D["answered"]:
    c, unc = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
for n in D["added"]:
    c, unc = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})

by_v = collections.defaultdict(list)
for s in sites:
    by_v[s["v"]].append((s["x"], s["y"]))

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
for _ in range(4000):
    k = rng.choice([len(v) for v in by_v.values() if len(v) >= 2])
    ctrl.append(spread(rng.sample(allpos, k)))
ctrl.sort()
p25 = ctrl[len(ctrl) // 4]
tight = [v for v in by_v if len(by_v[v]) >= 2 and spread(by_v[v]) < p25]
multi = [v for v in by_v if len(by_v[v]) >= 2]
print("values with >=2 sites:", len(multi), " tight (below the control's p25",
      int(p25), "px):", len(tight))
# the exact binomial tail: how unlikely is >=62 of 79 at p=0.25?
from math import comb
n_, k_, p_ = len(multi), len(tight), 0.25
tail = sum(comb(n_, i) * p_ ** i * (1 - p_) ** (n_ - i) for i in range(k_, n_ + 1))
print("binomial tail P(>=%d of %d at p=0.25) = %.2e" % (k_, n_, tail))
print("sites covered by the tight values:",
      sum(len(by_v[v]) for v in tight), "of", len(sites))

# the special rows' red sites: 92 school, 93 cemetery, 94 common land,
# 95 village head, 96 Reikh, 97 roads
print("\nthe statement's special rows and their red sites:")
for rn, name in ((92, "school"), (93, "cemetery"), (94, "common land"),
                 (95, "village head"), (96, "Reikh"), (97, "roads")):
    pts = by_v.get(rn, [])
    print("  row %2d %-12s: %d sites%s" % (rn, name, len(pts),
          ("  spread %d px" % spread(pts)) if len(pts) >= 2 else ""))

# singletons: values seen once (expected for one-parcel farms)
singles = [v for v in by_v if len(by_v[v]) == 1]
print("\nvalues seen once:", len(singles), sorted(singles))
print("values never seen (of 1..97):",
      [v for v in range(1, 98) if v not in by_v])
