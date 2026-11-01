# Near-miss test: D-S labels within a digit error of a row total or column,
# and the positional split (east edge vs the allotment's core).
import json
import re
import math
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

def canon(t):
    t = t.strip()
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

ds = []
for a in D["answered"]:
    c = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)), "x": x, "y": y,
                   "text": c})
for n in D["added"]:
    c = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)), "x": x, "y": y,
                   "text": c})

print("== D-S labels within 250 saz of a row total (a digit's error) ==")
for p in ds:
    v = p["d"] * 2400 + p["s"]
    for n, rt in row_total.items():
        if abs(rt - v) <= 250:
            print("  %-8s (%5.0f,%5.0f) off %4d saz from row %2d total [%s]"
                  % (p["text"], p["x"], p["y"], rt - v, n,
                     stmt[str(n)]["name"][:24]))

print("\n== the east/north-edge split ==")
core = [p for p in ds if p["x"] < 11000]
edge = [p for p in ds if p["x"] >= 11000]
print("west/core group (%d):" % len(core),
      ", ".join("%s@(%d,%d)" % (p["text"], p["x"], p["y"]) for p in core))
print("east group (%d):" % len(edge),
      ", ".join("%s@(%d,%d)" % (p["text"], p["x"], p["y"]) for p in edge))
print("\nsum of all D-S labels: %d des %d saz (the whole allotment: 1068/1272)"
      % (sum(p["d"] * 2400 + p["s"] for p in ds) // 2400,
         sum(p["d"] * 2400 + p["s"] for p in ds) % 2400))
