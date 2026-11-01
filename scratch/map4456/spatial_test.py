# The decisive test: spatial coherence. If the map carries the statement's
# figures, then two tokens near each other should hit the SAME row's
# different columns (a parcel's figures stand together). Compared against
# the permutation null (shuffled values, same geometry).
import json
import random
import collections
import math

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

stmt = REF["statement"]
# index: value -> set of (row) — distinctive values only (>=100), any column
val_rows = collections.defaultdict(set)
row_vals = collections.defaultdict(set)
for n, r in stmt.items():
    for k, v in r.items():
        if k == "name":
            continue
        for x in (v["saz"], v["des"]):
            if x >= 100:
                val_rows[x].add(n)
                row_vals[n].add(x)
print("distinctive values:", len(val_rows))

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
    big = [v for v in norm_parts(t["text"]) if v >= 100]
    if not big:
        continue
    toks.append({"text": t["text"], "x": t["x"], "y": t["y"],
                 "parts": big, "rows": set().union(*(val_rows.get(v, set()) for v in big))})
print("big-part tokens:", len(toks))

NEAR = 450   # px, ~ the largest parcels' internal distances

def cohits(ts):
    n = 0
    pairs = []
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = ts[i], ts[j]
            d = math.hypot(a["x"] - b["x"], a["y"] - b["y"])
            if d > NEAR:
                continue
            common = a["rows"] & b["rows"]
            if common:
                # require different values (two different figures of one row)
                ok = any(va != vb for va in a["parts"] if va in row_vals[r]
                         for vb in b["parts"] if vb in row_vals[r])
                if ok:
                    n += 1
                    pairs.append((a["text"], b["text"], sorted(common), int(d)))
    return n, pairs

obs, obs_pairs = cohits(toks)
print("\nco-located same-row pairs (observed):", obs)
for a, b, rows, d in obs_pairs:
    print("   %-9s + %-9s rows %s  dist %d px" % (a, b, rows, d))

rng = random.Random(11)
def randomize(ts):
    out = []
    for t in ts:
        nt = dict(t)
        vals = [rng.randint(100, 2399) for _ in t["parts"]]
        nt["parts"] = vals
        nt["rows"] = set().union(*(val_rows.get(v, set()) for v in vals))
        out.append(nt)
    return out

counts = []
for _ in range(1500):
    c, _ = cohits(randomize(toks))
    counts.append(c)
counts.sort()
mean_r = sum(counts) / len(counts)
p = sum(1 for c in counts if c >= obs) / 1500
print("\npermutation control: mean %.2f, 95th pct %d, max %d" %
      (mean_r, counts[int(0.95 * len(counts))], counts[-1]))
print("observed %d -> p = %.4f" % (obs, p))
