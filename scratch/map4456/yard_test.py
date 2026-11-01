# The yard test: farm 15 (1. = -288?) and farm 9 (1. = 144) against the
# statement's buildings column — the exact check the editor proposed.
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]

def b(n):
    r = stmt[str(n)]
    return r["buildings"]["des"] * 2400 + r["buildings"]["saz"], r["name"], \
        r["total"]["des"], r["total"]["saz"]

print("row 15: buildings %d saz (%s %d/%d)" % b(15))
print("row  9: buildings %d saz (%s %d/%d)" % b(9))

# all rows whose buildings == 288 or 144
print("\nrows with buildings = 288:",
      [n for n in range(1, 98) if str(n) in stmt and b(n)[0] == 288])
print("rows with buildings = 144:",
      [n for n in range(1, 98) if str(n) in stmt and b(n)[0] == 144])
print("rows with buildings = 162 (if 288 read half):",
      [n for n in range(1, 98) if str(n) in stmt and b(n)[0] == 162])
print("rows with buildings near 288 (within 40):",
      sorted((b(n)[0], n) for n in range(1, 98) if str(n) in stmt
             and abs(b(n)[0] - 288) <= 40))
print("rows with buildings near 144 (within 25):",
      sorted((b(n)[0], n) for n in range(1, 98) if str(n) in stmt
             and abs(b(n)[0] - 144) <= 25))
# and the red-9/15 sites on the map for the spatial check
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
def canon(t):
    t = t.strip().replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()
for f in (15, 9):
    pts = []
    for a in D["answered"]:
        if canon(a["text"]) == str(f):
            x, y = a["x"], a["y"]
            if a.get("fixed"):
                x, y = a["fixed"]["x"], a["fixed"]["y"]
            pts.append((x, y))
    for n in D["added"]:
        if canon(n["text"]) == str(f):
            pts.append((n["x"] + n.get("w", 0) // 2, n["y"] + n.get("h", 0) // 2))
    print("red-%d sites:" % f, len(pts), pts[:8])
