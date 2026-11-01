# The black numbers: are they the farmstead numbers of the statement?
# 1) the value distribution; 2) the sequence test: are tokens whose values
# are consecutive (n, n+1) nearer each other than random pairs? 3) the
# cross-check: red stacks near black n matching row n's columns.
import json
import math
import random
import collections
from geo_fit import px_to_ll

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_black.json", encoding="utf-8"))
stmt = REF["statement"]

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
    if t["conf"] < 0.4:
        continue
    ps = norm_parts(t["text"])
    if not ps:
        continue
    toks.append({**t, "v": max(ps)})
print("black tokens conf>=0.4:", len(toks))

vals = [t["v"] for t in toks]
print("value range:", min(vals), "-", max(vals))
in_range = [t for t in toks if 1 <= t["v"] <= 97]
print("values in 1..97:", len(in_range), "of", len(toks))
big = [t for t in toks if t["v"] > 97]
print("values >97:", len(big), sorted(set(t['v'] for t in big))[:30])
dist = collections.Counter(t["v"] for t in in_range)
print("distinct values in 1..97:", len(dist))
print("values seen:", sorted(dist.items())[:60])

# ---- the sequence test -----------------------------------------------------
rng = random.Random(3)
NEAR_BY = [t for t in in_range if t["conf"] >= 0.5]
def seq_score(ts):
    """mean distance between consecutive-value pairs"""
    by_val = collections.defaultdict(list)
    for t in ts:
        by_val[t["v"]].append(t)
    ds = []
    for v, ts_ in by_val.items():
        for a in ts_:
            for b in by_val.get(v + 1, []):
                ds.append(math.hypot(a["x"] - b["x"], a["y"] - b["y"]))
    return ds

ds = seq_score(NEAR_BY)
if ds:
    ds.sort()
    print("\nconsecutive-value pairs:", len(ds),
          " median dist %.0f px, p25 %.0f, p75 %.0f"
          % (ds[len(ds) // 2], ds[len(ds) // 4], ds[3 * len(ds) // 4]))
    # control: random value pairs
    rand = []
    for _ in range(4000):
        a, b = rng.choice(NEAR_BY), rng.choice(NEAR_BY)
        if a["v"] == b["v"]:
            continue
        rand.append(math.hypot(a["x"] - b["x"], a["y"] - b["y"]))
    rand.sort()
    print("random pairs:            median dist %.0f px, p25 %.0f, p75 %.0f"
          % (rand[len(rand) // 2], rand[len(rand) // 4], rand[3 * len(rand) // 4]))

# ---- the cross-check with red stacks ---------------------------------------
RED = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\red_stacks.json", encoding="utf-8"))
colidx = collections.defaultdict(list)
for rn in stmt:
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        d, s = row[col]["des"], row[col]["saz"]
        if s >= 100 and d <= 60:
            colidx[(d, s)].append((rn, col))

R = 380
print("\nblack n with a red stack within %d px matching row n's columns:" % R)
hits = 0
for t in NEAR_BY:
    n = t["v"]
    near = [st for st in RED if math.hypot(st["x"] - t["x"], st["y"] - t["y"]) <= R]
    for st in near:
        key = (st["d"], st["s"])
        refs = [r for r in colidx.get(key, []) if r[0] == n]
        if refs:
            hits += 1
            lon, lat = px_to_ll(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2)
            print("  black %2d at (%5d,%5d) = %s; stack (%d,%d) -> %s/%s  ll(%.5f,%.5f)"
                  % (n, t["x"], t["y"], stmt[str(n)]["name"][:28] if str(n) in stmt else "?",
                     st["d"], st["s"], refs[0][0], refs[0][1], lon, lat))
            break
if hits == 0:
    print("  (none yet)")
