# Refined sequence test on the black numbers: two-digit values only
# (11..97), conf >= 0.6 — fragments and misreads hit single digits hardest.
# Adjacency chains (n near n+1 near n+2) would be the farm-street signature.
import json
import math
import collections
from geo_fit import px_to_ll

TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_black.json", encoding="utf-8"))

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

toks = []
for t in TOK:
    ps = norm_parts(t["text"])
    if len(ps) == 1 and 11 <= ps[0] <= 97 and t["conf"] >= 0.6:
        toks.append({**t, "v": ps[0]})
print("clean two-digit tokens:", len(toks))
by_val = collections.defaultdict(list)
for t in toks:
    by_val[t["v"]].append(t)
print("distinct values:", sorted(by_val))

# consecutive pairs
pairs = []
for v, ts in by_val.items():
    for a in ts:
        for b in by_val.get(v + 1, []):
            pairs.append((v, a, b, math.hypot(a["x"] - b["x"], a["y"] - b["y"])))
pairs.sort(key=lambda p: p[3])
print("\nconsecutive pairs by distance:")
for v, a, b, d in pairs:
    print("  %2d->%2d  d %5.0f  (%5d,%5d)-(%5d,%5d) conf %.2f/%.2f"
          % (v, v + 1, d, a["x"], a["y"], b["x"], b["y"], a["conf"], b["conf"]))

# control: median distance between random clean two-digit pairs
import random
rng = random.Random(5)
rand = []
for _ in range(3000):
    a, b = rng.choice(toks), rng.choice(toks)
    if a["v"] == b["v"]:
        continue
    rand.append(math.hypot(a["x"] - b["x"], a["y"] - b["y"]))
rand.sort()
print("\nrandom pairs median %.0f, p25 %.0f" % (rand[len(rand) // 2], rand[len(rand) // 4]))

# where do the clean tokens sit? lat/lon quick list for the closest-spaced ones
print("\nclean tokens by position (lat/lon), conf >= 0.7:")
for t in sorted(toks, key=lambda t: (t["y"], t["x"])):
    if t["conf"] < 0.7:
        continue
    lon, lat = px_to_ll(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2)
    print("  %2d at (%5d,%5d) ll(%.5f,%.5f) conf %.2f" % (t["v"], t["x"], t["y"], lon, lat, t["conf"]))
