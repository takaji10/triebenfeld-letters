# The linked list of the Olęders: every farmstead number joined across the
# five tables —
#   doc 1  APŁ 39/98/0/-/6603-1  the 1868 liquidation table (name, dues)
#   doc 2  APŁ 39/98/0/-/6603-2  the 1869 copy (name variants)
#   Breyer APP 53/968/0/-/716-4  the 1868 extents in Morgen/rods + his pencil
#                                note of who held the farm in 1875
#   doc 4  APŁ 39/98/0/-/6603-4  the 1894 inscription (land for the given-up
#                                servitudes: 4/5/6 Morgen by number)
#   doc 6  APŁ 39/98/0/-/6603-6  the 1896 survey statement (name, areas)
#   the map  Pełzucki 1896       black farm-number sites (farm_locations.json)
# Output: scratch/map4456/oleders_linked.csv + .json
import csv
import io
import json
import re
import collections

DOCS = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\dataset\documents"
OUT_CSV = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\oleders_linked.csv"
OUT_JSON = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\oleders_linked.json"

def rows_of(uid):
    doc = json.load(open(r"%s\%s.json" % (DOCS, uid), encoding="utf-8"))
    return doc["text_english"]

def parse_csv_rows(text):
    out = []
    for row in csv.reader(io.StringIO(text)):
        if row and row[0].strip().isdigit():
            out.append(row)
    return out

# ---- doc 1: the 1868 table --------------------------------------------------
d1 = {}
draft_of = {}
for r in parse_csv_rows(rows_of("apl399806603-1")):
    no = int(r[0])
    if not (1 <= no <= 97):
        continue
    name = r[1].strip()
    draft = int(r[2]) if len(r) > 2 and r[2].strip().isdigit() else None
    rr = r[13].strip() if len(r) > 13 else ""
    kk = r[14].strip() if len(r) > 14 else ""
    d1[no] = {"name": name,
              "dues_r": int(rr) if rr.isdigit() else None,
              "dues_k": kk}
    if draft is not None:
        draft_of[no] = draft
print("doc1 rows:", len(d1))

# ---- doc 2: the 1869 copy ---------------------------------------------------
d2 = {}
for r in parse_csv_rows(rows_of("apl399806603-2")):
    no = int(r[0])
    if 1 <= no <= 97:
        d2[no] = r[1].strip()
print("doc2 rows:", len(d2))

# ---- Breyer's copy: order-aligned; name — pencil 1875 -----------------------
btext = rows_of("app539680716-4")
brows = []
for row in csv.reader(io.StringIO(btext)):
    cells = [c.strip() for c in row]
    if not any(cells):
        continue
    if cells[0].isdigit():
        brows.append([cells[0], cells[1],
                      cells[2] if len(cells) > 2 else "",
                      cells[3] if len(cells) > 3 else ""])
    elif len(cells) > 2 and cells[2].isdigit():
        # part-II rows begin with an empty no: school, cemetery, ...
        brows.append(["", cells[1], cells[2],
                      cells[3] if len(cells) > 3 else ""])
    elif brows and any(cells):
        # a true continuation of the previous row (the cemetery's pencil note)
        brows[-1][1] += " " + " ".join(c for c in cells if c)
print("Breyer raw rows:", len(brows))

# expected Breyer part-I numbers, from doc1's draft numbering
exp = [draft_of[i] for i in range(1, 92)]
got = [int(r[0]) for r in brows if r[0].isdigit()]
if got != exp:
    for i, (a, b) in enumerate(zip(exp, got)):
        if a != b:
            print("ALIGN mismatch at position %d (doc1 row %d): expected draft %s, Breyer no %s"
                  % (i, i + 1, a, b))
    print("lengths: expected %d, got %d" % (len(exp), len(got)))
else:
    print("Breyer part-I numbering matches doc1's draft column exactly (%d rows)" % len(got))

partI = [r for r in brows if r[0].isdigit()]
partII = [r for r in brows if not r[0].isdigit()]
print("Breyer rows: part I %d, part II %d" % (len(partI), len(partII)))

breyer = {}
for i, r in enumerate(partI):
    no = i + 1                       # order-aligned to doc1 1..91
    name = r[1]
    if " — " in name:
        n1868, n1875 = name.split(" — ", 1)
    elif " - " in name and not name.lower().startswith("heirs"):
        n1868, n1875 = name.split(" - ", 1)
    else:
        n1868, n1875 = name, ""
    breyer[no] = {"b1868": n1868.strip(), "b1875": n1875.strip(),
                  "morgen": int(r[2]) if r[2].isdigit() else None,
                  "rods": int(r[3]) if r[3].isdigit() else None,
                  "bno": int(r[0]) if r[0] else None}
for i, r in enumerate(partII):
    no = 92 + i
    name = r[1]
    if " — " in name:
        n1868, n1875 = name.split(" — ", 1)
    else:
        n1868, n1875 = name, ""
    breyer[no] = {"b1868": n1868.strip(), "b1875": n1875.strip(),
                  "morgen": int(r[2]) if r[2].isdigit() else None,
                  "rods": int(r[3]) if r[3].isdigit() else None,
                  "bno": None}

# ---- doc 6: the 1896 statement ----------------------------------------------
d6 = {}
for r in parse_csv_rows(rows_of("apl399806603-6")):
    no = int(r[0])
    if not (1 <= no <= 96):
        continue
    f = (r[2:14] + [""] * 12)[:12]
    def pair(i):
        a, b = f[2 * i].strip(), f[2 * i + 1].strip()
        dd = int(a) if a.isdigit() else 0
        ss = int(b) if b.isdigit() else 0
        return {"des": dd, "saz": ss}
    d6[no] = {"name": r[1].strip(),
              "cols": [pair(i) for i in range(6)]}
print("doc6 rows:", len(d6))

# ---- doc 4: the 1894 land for the given-up servitudes -----------------------
def expand(spec):
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if " to " in part:
            a, b = part.split(" to ")
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out

m4 = expand("1 to 7, 9 to 13, 15 to 46, 48 to 58, 60, 62, 64, 65, 67 to 74, 76 to 91, 96")
m6 = expand("8, 14, 59, 61, 63, 66, 75")
m5 = expand("47")

# ---- the map's black farm-number sites ---------------------------------------
loc = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\farm_locations.json",
                     encoding="utf-8"))
sites = collections.defaultdict(list)
for o in loc:
    sites[o["n"]].append({"lon": o["lon"], "lat": o["lat"], "conf": o["conf"],
                          "status": o["status"]})

# ---- assemble ----------------------------------------------------------------
def norm(s):
    s = re.sub(r"\[uncertain:([^]]*)\]", r"\1", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.lower().split())

def toks(s):
    return set(norm(s).split()) - {"heirs", "of", "the"}

def change_kind(a, b):
    """'same' | 'reordered' | 'shortened' | 'changed', after stripping the
    area notes doc 1 carries in its name column (' — 18 282')"""
    a = re.split(r"\s+—\s+", a)[0]
    ta, tb = toks(a), toks(b)
    if ta == tb:
        return "same"
    if ta and tb and sorted(ta) == sorted(tb):
        return "reordered"
    if ta and tb and (ta <= tb or tb <= ta):
        return "shortened"
    return "CHANGED"

linked = []
for no in range(1, 98):
    e = {"no": no}
    e["name_1868"] = d1.get(no, {}).get("name", "")
    e["dues_1868"] = ("%s r %s k" % (d1[no]["dues_r"], d1[no]["dues_k"])
                      if no in d1 and d1[no]["dues_r"] is not None else "")
    e["name_1869"] = d2.get(no, "")
    b = breyer.get(no, {})
    e["holder_1875"] = b.get("b1875", "")
    e["morgen_1868"] = b.get("morgen")
    e["rods_1868"] = b.get("rods")
    e["land_serv_1894"] = ("4 Morgen" if no in m4 else
                           "6 Morgen" if no in m6 else
                           "5 Morgen" if no in m5 else "")
    s6 = d6.get(no)
    if s6:
        e["name_1896"] = s6["name"]
        t = s6["cols"][5]
        e["total_1896"] = "%d des %d saz" % (t["des"], t["saz"])
        e["changed"] = change_kind(e["name_1868"], s6["name"]) \
            if e["name_1868"] else ""
    else:
        e["name_1896"] = ""
        e["total_1896"] = ""
        e["changed"] = ""
    e["map_sites"] = sites.get(no, [])
    e["n_sites"] = len(e["map_sites"])
    linked.append(e)

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["no", "name_1868", "name_1869", "holder_1875_breyer",
                 "morgen_1868", "rods_1868", "dues_1868", "land_serv_1894",
                 "name_1896", "total_1896", "name_changed",
                 "n_map_sites", "map_positions"])
    for e in linked:
        pos = "; ".join("%.5f,%.5f%s" % (s["lon"], s["lat"],
                                         "*" if s["status"] == "supported" else "")
                        for s in e["map_sites"])
        wr.writerow([e["no"], e["name_1868"], e["name_1869"], e["holder_1875"],
                     e["morgen_1868"] or "", e["rods_1868"] or "", e["dues_1868"],
                     e["land_serv_1894"], e["name_1896"], e["total_1896"],
                     e["changed"] or "", e["n_sites"], pos])
json.dump(linked, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", OUT_CSV)

# ---- the report ---------------------------------------------------------------
ch = [e for e in linked if e["changed"] not in ("", "same")]
print("\nrows whose 1896 name differs from 1868:", len(ch))
for e in ch:
    print("  %3d [%s]  %s  ->  %s" % (e["no"], e["changed"], e["name_1868"], e["name_1896"]))
n1875 = sum(1 for e in linked if e["holder_1875"])
print("\nBreyer's 1875 pencil notes:", n1875, "of 97 rows")
located = [e for e in linked if e["n_sites"]]
print("rows with map sites:", len(located))
zel = [e for e in linked if "tselmer" in norm(e["name_1868"] + " " + e["name_1896"] + " " + e["name_1869"])]
print("Zelmer-family rows:", [(e["no"], e["name_1868"], e["holder_1875"]) for e in zel])
