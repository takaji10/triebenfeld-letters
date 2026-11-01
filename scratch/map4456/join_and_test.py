# Join the split D-S fragments, build the black parcel-area list, then the
# decisive test: red value n (10..97) with nearby black parcels summing to
# row n's statement total. If red = the farm number written on each parcel,
# farms with k parcels show red n k times.
import json
import math
import re
import itertools
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("o", "").replace("O", "")
    return s.strip(".")

# ---- rebuild each label's numbers, joining dash fragments across lines ------
# a line dict was overwritten to a plain string in the saved json; the label
# carries x/y of the whole crop, so lines are re-sorted only by their text
def label_nums(lab):
    """returns (lead, d, s, note) parsing the label's lines jointly"""
    lines = [clean(l) for l in lab["lines"] if clean(l)]
    lead = None
    d = s = None
    notes = []
    # pass 1: full D-S on one line
    for s_ in lines:
        m = re.fullmatch(r"(\d{1,2})[-/](\d{3,4})", s_)
        if m and d is None:
            dd, ss = int(m.group(1)), int(m.group(2))
            if dd <= 60 and ss <= 2399:
                d, s = dd, ss
    if d is None:
        # pass 2: join a trailing-dash line with the next numeric line
        for i, s_ in enumerate(lines):
            m = re.fullmatch(r"(\d{1,2})[-/]+", s_)
            if m:
                for j in range(i + 1, len(lines)):
                    m2 = re.fullmatch(r"(\d{3,4})", lines[j])
                    if m2:
                        dd, ss = int(m.group(1)), int(m2.group(1))
                        if dd <= 60 and ss <= 2399:
                            d, s = dd, ss
                            notes.append("joined %s+%s" % (s_, lines[j]))
                        break
    if d is None:
        # pass 3: a leading-dash line with a numeric line before it
        for i, s_ in enumerate(lines):
            m = re.fullmatch(r"[-/](\d{3,4})", s_)
            if m:
                for j in range(i - 1, -1, -1):
                    m2 = re.fullmatch(r"(\d{1,2})", lines[j])
                    if m2:
                        dd, ss = int(m2.group(1)), int(m.group(1))
                        if dd <= 60 and ss <= 2399:
                            d, s = dd, ss
                            notes.append("joined %s+%s" % (lines[j], s_))
                        break
    # the lead: a standalone small number that is not the des half just used
    smalls = []
    for s_ in lines:
        if re.fullmatch(r"\d{1,2}", s_):
            smalls.append(int(s_))
    if smalls:
        cand = [v for v in smalls if d is None or v != d]
        if cand:
            lead = cand[0]
    return lead, d, s, notes, lines

parcels = []   # black area labels: d, s, position
red_vals = []  # red labels: value, position
for lab in LAB:
    cx = lab["x"] + lab["w"] / 2
    cy = lab["y"] + lab["h"] / 2
    if lab["ink"] == "red":
        for l in lab["lines"]:
            s_ = clean(l)
            if re.fullmatch(r"\d{1,2}[-/]\d{3,4}", s_):
                m = re.fullmatch(r"(\d{1,2})[-/](\d{3,4})", s_)
                parcels.append({"d": int(m.group(1)), "s": int(m.group(2)),
                                "x": cx, "y": cy, "src": "red-DS"})
            elif re.fullmatch(r"\d{2,4}", s_) and lab["n_tokens"] == 1:
                v = int(s_)
                if 10 <= v <= 97:
                    red_vals.append({"v": v, "x": cx, "y": cy})
                elif 100 <= v <= 2399:
                    parcels.append({"d": None, "s": v, "x": cx, "y": cy,
                                    "src": "red-S"})
        continue
    lead, d, s, notes, lines = label_nums(lab)
    if d is not None:
        parcels.append({"d": d, "s": s, "x": cx, "y": cy, "lead": lead,
                        "note": ";".join(notes)})
print("black/red D-S parcels recovered:", len(parcels),
      " (with lead:", sum(1 for p in parcels if p.get('lead') is not None), ")")
print("red single-value labels 10..97:", len(red_vals))
rc = collections.Counter(r["v"] for r in red_vals)
print("red value frequencies (10..97):", sorted(rc.items()))

# ---- the decisive test ------------------------------------------------------
R = 620
hits = []
for n in sorted(rc):
    sites = [r for r in red_vals if r["v"] == n]
    rt = row_total.get(n)
    if not rt:
        continue
    for site in sites:
        near = [p for p in parcels
                if p["d"] is not None
                and math.hypot(p["x"] - site["x"], p["y"] - site["y"]) <= R]
        found = None
        for k in range(1, min(9, len(near) + 1)):
            for combo in itertools.combinations(near, k):
                tot = sum(p["d"] * 2400 + p["s"] for p in combo)
                if abs(tot - rt) <= 0.05 * rt:
                    found = (combo, tot)
                    break
            if found:
                break
        if found:
            hits.append((n, site, found[0], found[1], rt))
print("\n== red n with nearby black parcels summing to row n ==")
for n, site, combo, tot, rt in hits:
    print("  red %2d at (%5.0f,%5.0f): %d parcels sum %d/%d ~ row %2d %d/%d  [%s]"
          % (n, site["x"], site["y"], len(combo), tot // 2400, tot % 2400,
             n, rt // 2400, rt % 2400, stmt[str(n)]["name"][:26]))
print("hits:", len(hits), "of", sum(1 for n in rc if n in row_total), "red values tested")

# frequency vs parcel count: for the hit farms, red count vs parcels in combo
print("\nred frequency vs the statement's farms (top frequencies):")
for v, c in rc.most_common(10):
    name = stmt.get(str(v), {}).get("name", "-")
    print("  red %2d x%d   row %2d = %s" % (v, c, v, name[:30]))
