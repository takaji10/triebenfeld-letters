# The farm-locator test: for each black number n, do red tokens within
# reach carry row n's figures? (also rows n-1/n+1, since parcels of
# neighbouring farms interleave). Prints the candidate farm locations.
import json
import math
import collections
from geo_fit import px_to_ll

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
BLACK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_black.json", encoding="utf-8"))
RED = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
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

blacks = []
for t in BLACK:
    ps = norm_parts(t["text"])
    if len(ps) == 1 and 1 <= ps[0] <= 97 and t["conf"] >= 0.6:
        blacks.append({**t, "v": ps[0]})

reds = []
for t in RED:
    if t["conf"] < 0.45 or t["kind"] != "red":
        continue
    ps = norm_parts(t["text"])
    if not ps:
        continue
    reds.append({**t, "v": max(ps)})

# row -> set of all its column values (des and saz, both)
row_vals = collections.defaultdict(set)
for rn in stmt:
    if not rn.isdigit():
        continue
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        row_vals[int(rn)].add(row[col]["des"])
        row_vals[int(rn)].add(row[col]["saz"])

R = 420
print("black farm numbers supported by a nearby red figure of the same row:")
supported = []
for b in blacks:
    n = b["v"]
    targets = {n} | ({n - 1} if n > 1 else set()) | ({n + 1} if n < 97 else set())
    hits = []
    for r in reds:
        if r["v"] < 100:
            continue
        d = math.hypot(r["x"] - b["x"], r["y"] - b["y"])
        if d > R:
            continue
        for tn in sorted(targets):
            if tn in row_vals and r["v"] in row_vals[tn]:
                # the value must not be ubiquitous across rows
                n_rows = sum(1 for rn in row_vals if r["v"] in row_vals[rn])
                if n_rows <= 12:
                    hits.append((r["text"], r["v"], tn, int(d), n_rows))
    if hits:
        lon, lat = px_to_ll(b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
        supported.append((n, b, hits, lon, lat))
        name = stmt.get(str(n), {}).get("name", "?")
        print("  black %2d (%s) at ll(%.5f,%.5f) conf %.2f  red: %s"
              % (n, name[:26], lon, lat, b["conf"],
                 "; ".join("'%s'=%d row %d d %d (in %d rows)" % h for h in hits)))

print("\ntotal supported:", len(supported), "of", len(blacks), "black numbers")

# frequency check: how many times each supported number appears
freq = collections.Counter(b["v"] for b in blacks)
print("\nfrequency of the supported numbers:", {n: freq[n] for n, _, _, _, _ in supported})
