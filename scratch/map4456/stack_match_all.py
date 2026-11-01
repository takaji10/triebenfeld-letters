# Match every red stack (d,s) against every column of every statement row.
# Output: all exact column matches with positions -> partial parcel map.
import json
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

toks = [t for t in TOK if t["conf"] >= 0.4 and norm_parts(t["text"])]
bigs = [t for t in toks if max(norm_parts(t["text"])) >= 100 and t["conf"] >= 0.5]
smalls = [t for t in toks if max(norm_parts(t["text"])) <= 60 and t["conf"] >= 0.5]

# pair into stacks (des above saz)
used = set()
stacks = []
for b in bigs:
    bp = norm_parts(b["text"])
    bv = max(bp)
    best = None
    for s in smalls:
        if id(s) in used:
            continue
        if abs(s["x"] - b["x"]) > 170:
            continue
        dy = b["y"] - s["y"]
        if not (8 <= dy <= 240):
            continue
        if best is None or abs(dy) < abs(best[0]):
            best = (dy, s)
    if best:
        used.add(id(best[1]))
        stacks.append({"d": norm_parts(best[1]["text"])[0], "s": bv,
                       "x": (b["x"] + best[1]["x"]) / 2, "y": (b["y"] + best[1]["y"]) / 2,
                       "conf": round(min(b["conf"], best[1]["conf"]), 2),
                       "dx": int(b["x"] - best[1]["x"]), "dy": int(best[0]),
                       "btext": b["text"], "stext": best[1]["text"]})

# index the statement: (d,s) -> [(row, col)]
colidx = collections.defaultdict(list)
for rn in stmt:
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        d, s = row[col]["des"], row[col]["saz"]
        if s >= 100 and d <= 60:
            colidx[(d, s)].append((rn, col))
print("stacks:", len(stacks), " distinct (d,s) pairs in statement:", len(colidx))

matched = []
for st in stacks:
    key = (st["d"], st["s"])
    if key in colidx:
        st["refs"] = colidx[key]
        matched.append(st)
print("stacks matching a statement column exactly:", len(matched))
for st in matched:
    print("  (%d,%d) conf %.2f at (%5.0f,%5.0f) [dx %+d dy %+d]  -> %s" % (
        st["d"], st["s"], st["conf"], st["x"], st["y"], st["dx"], st["dy"],
        ", ".join("%s/%s" % (r, c) for r, c in st["refs"])))
json.dump(stacks, open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\red_stacks.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
