# The red figures as parcels: pair tokens into des/saz stacks (des above
# saz), convert to square sazhens, cluster neighbouring stacks into local
# groups, and compare group sums with the statement's row totals.
# Also: the black "farm number" cross-check hooks (row -> position).
import json
import math
import collections

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
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
    toks.append({**t, "v": ps[0] if len(ps) == 1 else max(ps)})

# ---- pair stacks: des token above saz token -------------------------------
STACK_X = 170
STACK_DY = (10, 240)
used = set()
stacks = []
singles = []
bigs = sorted([t for t in toks if t["v"] >= 100], key=lambda t: t["y"])
smalls = [t for t in toks if t["v"] <= 60]
for b in bigs:
    if b["conf"] < 0.5:
        continue
    best = None
    for s in smalls:
        if id(s) in used:
            continue
        if abs(s["x"] - b["x"]) > STACK_X:
            continue
        dy = b["y"] - s["y"]
        if not (STACK_DY[0] <= dy <= STACK_DY[1]):
            continue
        if best is None or abs(dy) < abs(best["dy"]):
            best = {"s": s, "dy": dy}
    if best:
        used.add(id(best["s"]))
        d = best["s"]["v"]
        stacks.append({"d": d, "s": b["v"], "val": d * 2400 + b["v"],
                       "x": (b["x"] + best["s"]["x"]) / 2,
                       "y": (b["y"] + best["s"]["y"]) / 2,
                       "conf": min(b["conf"], best["s"]["conf"]),
                       "bx": b["x"], "by": b["y"]})
for s in smalls:
    if id(s) not in used and s["conf"] >= 0.5:
        singles.append({"d": None, "s": s["v"], "val": s["v"],
                        "x": s["x"], "y": s["y"], "conf": s["conf"]})
print("tokens", len(toks), "-> stacks", len(stacks), "unpaired singles", len(singles))

# ---- cluster stacks into local groups (parcels of one place) ---------------
items = stacks + singles
parent = list(range(len(items)))
def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i
LINK = 380
cells = collections.defaultdict(list)
CS = 400
for i, it in enumerate(items):
    cells[(int(it["x"]) // CS, int(it["y"]) // CS)].append(i)
for (cx, cy), idxs in cells.items():
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for j in cells.get((cx + dx, cy + dy), []):
                if j <= i:
                    continue
                a, b = items[i], items[j]
                if math.hypot(a["x"] - b["x"], a["y"] - b["y"]) <= LINK:
                    pi, pj = find(i), find(j)
                    if pi != pj:
                        parent[pi] = pj
groups = collections.defaultdict(list)
for i in range(len(items)):
    groups[find(i)].append(items[i])
print("local groups:", len(groups))
gs = []
for g in groups.values():
    total = sum(it["val"] for it in g if it["val"] >= 100)
    n_stack = sum(1 for it in g if it["d"] is not None)
    gs.append({"n": len(g), "n_stack": n_stack, "total_saz": total,
               "x": sum(it["x"] for it in g) / len(g),
               "y": sum(it["y"] for it in g) / len(g),
               "items": g})
gs.sort(key=lambda g: -g["n"])

# ---- compare group sums with row totals ------------------------------------
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"] for n, r in stmt.items() if n.isdigit()}
print("\ngroups with >=2 stacks (candidate farm groups):",
      sum(1 for g in gs if g["n_stack"] >= 2))
print("\ntop groups and any row total they match (tol 12%):")
shown = 0
for g in gs:
    if g["n_stack"] < 2 or g["total_saz"] < 5000:
        continue
    hits = [(n, v) for n, v in row_total.items()
            if abs(v - g["total_saz"]) <= 0.12 * v]
    if shown < 25:
        vals = sorted((it["d"], it["s"]) for it in g["items"] if it["d"] is not None)
        print("  group at (%5.0f,%5.0f) stacks %d sum %6d  %s%s" % (
            g["x"], g["y"], g["n_stack"], g["total_saz"], vals,
            "  == rows " + str(hits) if hits else ""))
        shown += 1
json.dump(gs, open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\red_groups.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
