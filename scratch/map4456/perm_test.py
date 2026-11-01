# Is the match rate above chance? Permutation test: same tokens with
# shuffled digit strings of the same length; compare exact-match rates
# against the statement's saz/des/dues value sets. Also list the
# distinctive (3-4 digit) hits and which rows they name.
import json
import random
import collections

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

stmt = REF["statement"]
dues = REF["dues1868"]

saz_vals = set()
des_vals = set()
for n, r in stmt.items():
    for k, v in r.items():
        if k == "name":
            continue
        if v["saz"]:
            saz_vals.add(v["saz"])
        if v["des"]:
            des_vals.add(v["des"])
dues_vals = {v["roubles"] for v in dues.values()}

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
    # drop trivial 1-2 digit tokens for the saz test (they match too easily)
    tokens.append({"text": t["text"], "kind": t["kind"],
                   "big": [v for v in ps if v >= 100],
                   "all": ps})

print("tokens conf>=0.5:", len(tokens))
print("with a part >=100:", sum(1 for t in tokens if t["big"]))

def hit_count(ts, vals):
    n = 0
    hits = []
    for t in ts:
        h = [v for v in t["big"] if v in vals]
        if h:
            n += 1
            hits.append((t["text"], h))
    return n, hits

n_saz, hits_saz = hit_count(tokens, saz_vals)
print("\nbig-part tokens hitting a saz value >=100:", n_saz, "of",
      sum(1 for t in tokens if t['big']))
for txt, h in hits_saz:
    refs = sorted({(rn, k) for v in h for (rn, k2) in
                   [(rn, k) for rn, r in stmt.items() for k, vv in r.items()
                    if isinstance(vv, dict) and vv.get('saz') == v]}
                  )
    print("   %-8s -> %s" % (txt, refs))

# permutation control: shuffle the digits within each token's length
rng = random.Random(7)
def randomize(ts):
    out = []
    for t in ts:
        nt = dict(t)
        nt["big"] = []
        for v in t["big"]:
            s = str(v)
            # same-length random number, first digit nonzero
            nv = rng.randint(10 ** (len(s) - 1), 10 ** len(s) - 1)
            nt["big"].append(nv)
        out.append(nt)
    return out

trials = 2000
counts = []
for _ in range(trials):
    n, _ = hit_count(randomize(tokens), saz_vals)
    counts.append(n)
counts.sort()
mean_r = sum(counts) / len(counts)
p = sum(1 for c in counts if c >= n_saz) / trials
print("\npermutation control (%d trials): mean hits %.1f, 95th pct %d, max %d"
      % (trials, mean_r, counts[int(0.95 * trials)], counts[-1]))
print("observed", n_saz, "-> p = %.4f" % p)
