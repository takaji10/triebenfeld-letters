# Do the map's numbers align with the liquidation tables? Compare the
# EasyOCR tokens (numbers_easy.json) with the survey statement (doc 6) and
# the 1868 table's dues (doc 1). Prints the match report and saves
# scratch/map4456/numbers_matched.json with every hit annotated.
import json
import collections
import csv

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

stmt = REF["statement"]
dues = REF["dues1868"]

# --- reference value sets -------------------------------------------------
saz_of_kind = collections.defaultdict(list)   # saz value -> [(row, kind)]
des_of_kind = collections.defaultdict(list)   # des value -> [(row, kind)]
total_pairs = collections.defaultdict(list)   # (des,saz) -> [row]
for n, r in stmt.items():
    for k, v in r.items():
        if k == "name":
            continue
        if v["saz"]:
            saz_of_kind[v["saz"]].append((n, k))
        if v["des"]:
            des_of_kind[v["des"]].append((n, k))
    total_pairs[(r["total"]["des"], r["total"]["saz"])].append(n)

saz_values = set(saz_of_kind)
des_values = set(des_of_kind)
dues_r = {v["roubles"] for v in dues.values()}
dues_pair = {(v["roubles"], v["kop"]) for v in dues.values()}

def norm(t):
    t = t.strip().strip(".,-/").strip()
    return t

def parts(t):
    """the token's readings: whole, and the pieces split on separators"""
    t = norm(t)
    out = []
    if t.isdigit():
        out.append(int(t))
    for sep in " ,./-":
        if sep in t:
            ps = [p for p in t.replace("/", " ").replace(",", " ")
                  .replace(".", " ").replace("-", " ").split() if p.isdigit()]
            out.extend(int(p) for p in ps)
    return out

def match_one(tok):
    """annotate a token against the reference sets; returns dict of matches"""
    ps = parts(tok["text"])
    m = {"saz": [], "des": [], "total": [], "num97": [], "dues": []}
    for v in ps:
        if v in saz_values:
            m["saz"].append((v, saz_of_kind[v]))
        if v in des_values:
            m["des"].append((v, des_of_kind[v]))
        if 1 <= v <= 97:
            m["num97"].append(v)
        if v in dues_r and v <= 60:
            m["dues"].append(v)
    # a des,saz pair read as one token "6 703"
    digs = [p for p in t_parts_raw(tok["text"]) if p.isdigit()]
    if len(digs) == 2:
        pair = (int(digs[0]), int(digs[1]))
        if pair in total_pairs:
            m["total"].append((pair, total_pairs[pair]))
    return m

def t_parts_raw(t):
    return t.replace("/", " ").replace(",", " ").replace(".", " ") \
            .replace("-", " ").split()

matched = []
for tok in TOK:
    if tok["conf"] < 0.3:
        continue
    m = match_one(tok)
    any_hit = any(m[k] for k in ("saz", "des", "total", "dues"))
    if any_hit:
        matched.append({**tok, "matches": {k: v for k, v in m.items() if v}})

print("tokens kept (conf>=0.3):", sum(1 for t in TOK if t["conf"] >= 0.3))
print("matched:", len(matched))
by_kind = collections.Counter(t["kind"] for t in matched)
print("matched by ink:", by_kind)
n_saz = sum(1 for t in matched if t["matches"].get("saz"))
n_des = sum(1 for t in matched if t["matches"].get("des"))
n_dues = sum(1 for t in matched if t["matches"].get("dues"))
n_total = sum(1 for t in matched if t["matches"].get("total"))
print("saz hits:", n_saz, " des hits:", n_des, " dues hits:", n_dues, " total-pair hits:", n_total)

# baseline: how often would a random 3-4 digit number land on a saz value?
import random
rng = random.Random(42)
saz_range = [v for v in saz_values if v > 0]
pool = [rng.randint(1, 2399) for _ in range(5000)]
base = sum(1 for v in pool if v in saz_values) / len(pool)
print("baseline random-in-saz rate: %.1f%% (distinct saz values %d of 2400)"
      % (base * 100, len(saz_range)))

rows_hit = collections.Counter()
for t in matched:
    for v, refs in t["matches"].get("saz", []):
        for (r, k) in refs:
            rows_hit[r] += 1
    for v, refs in t["matches"].get("des", []):
        for (r, k) in refs:
            rows_hit[r] += 1
print("rows of the statement hit at least once:", len(rows_hit), "of 96")

print("\nsample saz matches:")
shown = 0
for t in sorted(matched, key=lambda t: -t["conf"]):
    if t["matches"].get("saz") and shown < 25:
        v, refs = t["matches"]["saz"][0]
        print("  %-10s conf %.2f %s at (%5d,%5d) %dx%d -> %s %s"
              % (t["text"], t["conf"], t["kind"], t["x"], t["y"], t["w"], t["h"],
                 v, refs[:4]))
        shown += 1

json.dump(matched, open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_matched.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
