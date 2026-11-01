# Build the reference figures from the liquidation-table documents:
# doc 6 (the survey statement, des/saz per kind per farmstead) and
# doc 1 (the 1868 table's dues, roubles/kop). Output: reference JSON used by
# the alignment check.
import json
import re

DOCS = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\dataset\documents"
OUT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json"

def parse_saz_pairs(fields):
    """columns come in des,saz pairs; empties are zero"""
    out = []
    for i in range(0, len(fields) - 1, 2):
        d = fields[i].strip()
        s = fields[i + 1].strip()
        dd = int(d) if d.isdigit() else 0
        ss = int(s) if s.isdigit() else 0
        out.append((dd, ss))
    return out

doc = json.load(open(DOCS + r"\apl399806603-6.json", encoding="utf-8"))
# the statement's csv text
csv_text = None
for key in ("text_english", "en"):
    v = doc.get(key)
    if isinstance(v, str) and "Statement" in v:
        csv_text = v
        break
if csv_text is None:
    # search blocks
    for b in doc.get("blocks", doc.get("pages", [])):
        pass
print("keys:", [k for k in doc.keys() if "text" in k.lower() or k == "en"])

rows = {}
kinds = ["buildings", "arable", "meadow", "pasture", "unusable", "total"]
for line in csv_text.splitlines():
    f = line.split(",")
    if len(f) < 13:
        continue
    no = f[0].strip()
    if not no.isdigit():
        continue
    n = int(no)
    if not (1 <= n <= 97):
        continue
    vals = parse_saz_pairs(f[2:14])
    if len(vals) != 6:
        continue
    rec = dict(zip(kinds, vals))
    # rows are in saz: buildings,arable,meadow,pasture,unusable,total
    # desiatinas first of each pair already; keep raw
    rows[n] = {"name": f[1].strip(), **{k: {"des": v[0], "saz": v[1]} for k, v in rec.items()}}

print("doc6 rows:", len(rows))
print("row1:", rows.get(1))
print("row2:", rows.get(2))

# doc 1: the 1868 table's dues per farmstead (roubles, kop)
d1 = json.load(open(DOCS + r"\apl399806603-1.json", encoding="utf-8"))
t1 = d1.get("text_english") or d1.get("en") or ""
dues = {}
for line in t1.splitlines():
    f = line.split(",")
    if len(f) < 16:
        continue
    no = f[0].strip()
    if not no.isdigit():
        continue
    n = int(no)
    if not (1 <= n <= 97):
        continue
    r = f[13].strip(); k = f[14].strip()
    if r.isdigit():
        dues[n] = {"name": f[1].strip(), "roubles": int(r), "kop": k}
print("doc1 dues rows:", len(dues))
print("due1:", dues.get(1), "due9:", dues.get(9))

# the statement's own closing line, unnumbered
rows["_extra"] = {"name": "Unusable land, besides the rows",
                  "buildings": {"des": 0, "saz": 0}, "arable": {"des": 0, "saz": 0},
                  "meadow": {"des": 0, "saz": 0}, "pasture": {"des": 0, "saz": 0},
                  "unusable": {"des": 12, "saz": 741},
                  "total": {"des": 12, "saz": 741}}
json.dump({"statement": rows, "dues1868": dues}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("saved", OUT)
