# Corrected attribution: for every big-part token hitting a statement value,
# list the true (row, kind) references; plus permutation controls for the
# des column and the 1868 dues. Output printed + numbers_hits.json.
import json
import random
import collections

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

stmt = REF["statement"]
dues = REF["dues1868"]

index = collections.defaultdict(list)   # value -> [(row, kind)]
for n, r in stmt.items():
    for k, v in r.items():
        if k == "name":
            continue
        if v["saz"]:
            index[v["saz"]].append((n, k, "saz"))
        if v["des"]:
            index[v["des"]].append((n, k, "des"))
dues_index = collections.defaultdict(list)
for n, v in dues.items():
    dues_index[v["roubles"]].append((n, "roubles"))

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

tokens = []
for t in TOK:
    if t["conf"] < 0.5:
        continue
    ps = norm_parts(t["text"])
    if not ps:
        continue
    tokens.append({**t, "parts": ps, "big": [v for v in ps if v >= 100]})

def hits_for(ts, pool):
    out = []
    for t in ts:
        hs = []
        for v in t["big"]:
            if v in pool:
                hs.append((v, pool[v]))
        if hs:
            out.append({"text": t["text"], "conf": t["conf"], "kind": t["kind"],
                        "x": t["x"], "y": t["y"], "w": t["w"], "h": t["h"],
                        "hits": hs})
    return out

saz_pool = {v: refs for v, refs in index.items() if v >= 100 and any(r[2] == "saz" for r in refs)}
des_pool = {v: refs for v, refs in index.items() if v >= 100 and any(r[2] == "des" for r in refs)}
hits = hits_for(tokens, index)
print("big-part tokens hitting any statement value:", len(hits), "of",
      sum(1 for t in tokens if t["big"]))
n_saz = sum(1 for h in hits if any(any(r[2] == "saz" for r in refs) for _, refs in h["hits"]))
n_des = sum(1 for h in hits if any(any(r[2] == "des" for r in refs) for _, refs in h["hits"]))
print("  hitting a saz column value:", n_saz)
print("  hitting a des column value:", n_des)
print()
for h in sorted(hits, key=lambda h: -h["conf"]):
    refs = []
    for v, rr in h["hits"]:
        refs.append("%d: %s" % (v, ", ".join("%s/%s" % (rn, k) for rn, k, _ in rr)))
    print("  %-9s conf %.2f %s at (%5d,%5d)  %s" % (
        h["text"], h["conf"], h["kind"], h["x"], h["y"], " | ".join(refs)))

json.dump(hits, open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_hits.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# permutation controls
rng = random.Random(7)
def randomize(ts):
    out = []
    for t in ts:
        nt = dict(t)
        nt["big"] = [rng.randint(10 ** (len(str(v)) - 1), 10 ** len(str(v)) - 1)
                     for v in t["big"]]
        out.append(nt)
    return out

def run_control(pool, label):
    obs = len(hits_for(tokens, pool))
    counts = []
    for _ in range(2000):
        counts.append(len(hits_for(randomize(tokens), pool)))
    counts.sort()
    mean_r = sum(counts) / len(counts)
    p = sum(1 for c in counts if c >= obs) / 2000
    print("%s: observed %d, control mean %.1f, 95th %d, p=%.4f"
          % (label, obs, mean_r, counts[int(0.95 * len(counts))], p))

print()
run_control(saz_pool, "saz >=100")
run_control(des_pool, "des >=100")
