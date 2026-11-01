# Fixed spatial test + the des/saz stacked-pair test.
import json
import random
import collections
import math

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

stmt = REF["statement"]

# value -> set of row numbers (distinctive values only, any column)
val_rows = collections.defaultdict(set)
for rn in stmt:
    row = stmt[rn]
    for kk in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        vv = row[kk]
        for x in (vv["saz"], vv["des"]):
            if x >= 100:
                val_rows[x].add(rn)

# (des, saz) pairs by row+column, des 0..60, saz >= 100
pair_index = collections.defaultdict(list)   # (des,saz) -> [(row, col)]
for rn in stmt:
    row = stmt[rn]
    for kk in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        d, s = row[kk]["des"], row[kk]["saz"]
        if s >= 100 and d <= 60:
            pair_index[(d, s)].append((rn, kk))
print("distinctive saz values:", len(val_rows), " des/saz pairs:", len(pair_index))

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
    if t["conf"] < 0.5:
        continue
    ps = norm_parts(t["text"])
    if not ps:
        continue
    toks.append({"text": t["text"], "x": t["x"], "y": t["y"],
                 "w": t["w"], "h": t["h"], "parts": ps,
                 "big": [v for v in ps if v >= 100],
                 "small": [v for v in ps if v <= 60]})
big_toks = [t for t in toks if t["big"]]
print("tokens conf>=0.5:", len(toks), " with big part:", len(big_toks),
      " with small part:", len([t for t in toks if t['small']]))

# ---- test A: co-located same-row (fixed) --------------------------------
NEAR = 700
def cohits(ts):
    n = 0
    pairs = []
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = ts[i], ts[j]
            if math.hypot(a["x"] - b["x"], a["y"] - b["y"]) > NEAR:
                continue
            common = a.get("rows", set()) & b.get("rows", set())
            if not common:
                continue
            ok = False
            for rn in common:
                rvals = set()
                row = stmt[rn]
                for kk in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
                    rvals.add(row[kk]["saz"])
                    rvals.add(row[kk]["des"])
                va = [v for v in a["parts"] if v in rvals]
                vb = [v for v in b["parts"] if v in rvals]
                if va and vb and set(va) != set(vb):
                    ok = True
            if ok:
                n += 1
                pairs.append((a["text"], b["text"], sorted(common)))
    return n, pairs

for t in toks:
    t["rows"] = set().union(*(val_rows.get(v, set()) for v in t["big"])) if t["big"] else set()
obsA, pairsA = cohits(toks)
print("\nA) co-located same-row pairs, NEAR=%d: observed %d" % (NEAR, obsA))
for a, b, rows in pairsA[:15]:
    print("   %-9s + %-9s rows %s" % (a, b, rows))

# ---- test B: stacked des+saz pair matching one row-column ---------------
STACK = 260   # vertical stack distance for a two-line figure
def pairhits(ts):
    n = 0
    hits = []
    smalls = [t for t in ts if t["small"]]
    bigs = [t for t in ts if t["big"]]
    for s in smalls:
        for b in bigs:
            if s is b:
                continue
            if abs(s["x"] - b["x"]) > 160:
                continue
            dy = b["y"] - s["y"]
            if not (0 < abs(dy) <= STACK):
                continue
            for d in s["small"]:
                for z in b["big"]:
                    if (d, z) in pair_index:
                        n += 1
                        hits.append((s["text"], b["text"], (d, z), pair_index[(d, z)],
                                     int(abs(dy))))
    return n, hits

obsB, hitsB = pairhits(toks)
print("\nB) stacked des/saz pairs matching a row-column: observed %d" % obsB)
for s, b, pz, refs, dy in hitsB[:25]:
    print("   %-7s above %-7s pair %s -> %s (dy %d)" % (s, b, pz, refs, dy))

# ---- controls ------------------------------------------------------------
rng = random.Random(13)
def randomize(ts):
    out = []
    for t in ts:
        nt = dict(t)
        nt["parts"] = [rng.randint(0, 2399) for _ in t["parts"]]
        nt["big"] = [v for v in nt["parts"] if v >= 100]
        nt["small"] = [v for v in nt["parts"] if v <= 60]
        nt["rows"] = set().union(*(val_rows.get(v, set()) for v in nt["big"])) if nt["big"] else set()
        out.append(nt)
    return out

for label, fn, arg in (("A (NEAR=700)", cohits, toks), ("B (stack pairs)", pairhits, toks)):
    counts = []
    for _ in range(800):
        c, _ = fn(randomize(toks))
        counts.append(c)
    counts.sort()
    p = sum(1 for c in counts if c >= (obsA if label.startswith("A") else obsB)) / 800
    print("control %s: mean %.2f, 95th %d, max %d, p=%.4f" %
          (label, sum(counts) / len(counts), counts[int(0.95 * len(counts))],
           counts[-1], p))
