# The yard readings against the statement — which farm numbers stand confirmed,
# which are uncertain, and what the uncertain ones cannot be.
#
# The method (the editor's, from the farm-13 and farm-9/15 probes): the yard's
# pieces are the plots marked as primary in the page, and the statement's
# buildings column records the yard separately. Tests, in order:
#   1. a piece's figure equal to the claimed row's buildings figure -> confirmed
#      (rows sharing the same figure are resolved by the marks' positions)
#   2. a SUBSET of the pieces summing to it -> confirmed-sum (a yard recorded
#      in several pieces; pieces beyond the subset are noted)
#   3. a subset sum within 15 sazhens -> sum-near (one stroke in one piece)
#   4. otherwise: exact matches on OTHER rows (points-elsewhere, the distance
#      to that row's red sites as a hint only — neighbouring pieces of forest
#      carry different numbers, so distance alone does not decide), then
#      one-digit-off matches, the claim's own row first (a digit slip)
#   5. a confident figure matching nothing is the elimination: as read it
#      cannot be any row's yard figure — the read or the claim is wrong
#   6. an unread piece ("[?]") is a piece whose size is unknown: if the read
#      pieces sum to LESS than the row's figure, the unread piece could carry
#      the remainder — noted as a gap, not a contradiction
# Uncertain reads ([..?]) matching the claim count as weak confirmation; a
# claim typed uncertain ("3[7?]") is resolved when the mark sits on a red tag
# whose number is one of the claim's candidates.
#
# Input: yards_read.json (the export), reds_all.json + the export's red_fixes
# and red_added (the corrected red catalogue), reference_numbers.json (rows).
# Output: yard_analysis.json and this console summary.
import json
import re
from collections import defaultdict, Counter
from itertools import combinations

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456"

EX = json.load(open(ROOT + r"\yards_read.json", encoding="utf-8"))
D = json.load(open(ROOT + r"\reds_all.json", encoding="utf-8"))
R = json.load(open(ROOT + r"\reference_numbers.json", encoding="utf-8"))
ST = {k: v for k, v in R["statement"].items() if k.isdigit()}

# ---- the corrected red catalogue: row -> [(x, y), ...] ----------------------
fixes = EX.get("red_fixes", {})
def canon(t):
    return t.strip().replace("[", "").replace("?]", "").replace("?", "").strip()

sites = defaultdict(list)
pos_rows = defaultdict(set)          # a mosaic position -> the rows tagged there
def add_site(n, x, y):
    sites[n].append((x, y))
    pos_rows[(x, y)].add(n)

for a in D["answered"]:
    c = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    k = str(x) + "," + str(y)
    n = int(fixes[k]) if k in fixes and str(fixes[k]).isdigit() else \
        (int(c) if c.isdigit() else None)
    if n is not None:
        add_site(n, x, y)
for m in D["added"]:
    c = canon(m["text"])
    if c.isdigit():
        add_site(int(c), m["x"] + (m.get("w", 0)) // 2,
                 m["y"] + (m.get("h", 0)) // 2)
for m in EX.get("red_added", []):
    if str(m.get("n", "")).isdigit():
        add_site(int(m["n"]), m["x"], m["y"])

# ---- the rows' buildings figures -------------------------------------------
def b_total(row):
    b = row["buildings"]
    return b["des"] * 2400 + b["saz"]

B = {int(k): b_total(v) for k, v in ST.items()}
ZERO_ROWS = sorted(r for r, b in B.items() if b == 0)
BY_B = defaultdict(list)
for r, b in B.items():
    BY_B[b].append(r)

def lev(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]

def dist_to(p, row):
    ds = [abs(p["x"]-sx) + abs(p["y"]-sy) for sx, sy in sites.get(row, [])]
    return min(ds) if ds else None

# ---- parse a read -----------------------------------------------------------
def parse_yard(area):
    a = area.strip()
    lead = None
    unc_lead = False
    # a bracketed LEAD needs a separator (or a dot inside): [6?]. 193,
    # [7?]. 80, [1.?] -276, [?]. 120 — while consecutive bracketed digits
    # belong to the figure: [9?][6?] reads "96", both digits uncertain
    m = re.match(r"^[\[(]([0-9.?/]+)[\])]\s*([.,]?)\s*(.*)$", a)
    if m and (m.group(2) or "." in m.group(1)):
        inner = m.group(1)
        digits = re.sub(r"[.?/]", "", inner)
        lead = int(digits) if digits else None
        unc_lead = True
        fig = m.group(3).strip()
    else:
        m2 = re.match(r"^(\d+)\s*[.,]\s*(.*)$", a)
        if m2:
            lead = int(m2.group(1))
            fig = m2.group(2).strip()
        else:
            fig = a
    neg = fig.startswith("-") or fig.startswith("[-")
    s = fig.replace("[", "").replace("]", "").replace(" ", "")
    uncertain = ("?" in s) or unc_lead
    s = s.replace("?", "")
    # digit alternatives "4/7" — both readings are live
    orig = s.lstrip("-")
    variants = [orig]
    for a1, a2 in re.findall(r"(\d)/(\d)", orig):
        nxt = []
        for v0 in variants:
            if a1 + "/" + a2 in v0:
                nxt.append(v0.replace(a1 + "/" + a2, a1, 1))
                nxt.append(v0.replace(a1 + "/" + a2, a2, 1))
            else:
                nxt.append(v0)
        variants = nxt
        if len(variants) > 8:
            break
    vals = [int(v) for v in sorted(set(variants)) if v.isdigit()][:8]
    val = vals[0] if vals else None
    unread = val is None                 # '[?]': a piece with no figure read
    return {"lead": lead, "val": val, "vals": vals, "uncertain": uncertain,
            "neg": neg, "unread": unread, "raw": a}

# ---- group the reads by claimed farm ---------------------------------------
groups = defaultdict(list)
for y in EX["yards"]:
    claim = y["farm"]
    claim = int(claim) if str(claim).isdigit() else str(claim)
    p = parse_yard(y["area"])
    p["farm"] = claim
    p["x"] = y["rx"]; p["y"] = y["ry"]
    groups[claim].append(p)

# a claim typed uncertain resolves when the mark sits on a red tag whose
# number is one of the claim's candidates ("[3?]1" on a red-31 tag -> 31)
def resolve_claim(claim, pieces):
    if isinstance(claim, int):
        return claim, None
    cands = [int(d) for d in re.sub(r"[\[\]?]", "", str(claim)).split("/")
             if d.isdigit()]
    if not cands:
        return claim, None
    at = set()
    for p in pieces:
        at |= pos_rows.get((p["x"], p["y"]), set())
    hit = sorted(at & set(cands))
    if len(hit) == 1:
        return hit[0], ("the claim " + str(claim) + " resolves to row " +
                        str(hit[0]) + " — the mark sits on its red tag")
    return claim, None

resolved = {}
for claim in list(groups):
    new, note = resolve_claim(claim, groups[claim])
    if note:
        groups[new].extend(groups[claim])
        for p in groups[new]:
            p["farm"] = new
        del groups[claim]
        resolved[str(claim)] = note

# ---- evaluate each farm's group --------------------------------------------
out = []
for claim, pieces in sorted(groups.items(), key=lambda kv: str(kv[0])):
    g = {"farm": claim, "pieces": pieces, "verdict": None, "candidates": [],
         "notes": []}
    valpieces = [p for p in pieces if p["val"] is not None]
    unread = [p for p in pieces if p["val"] is None]
    conf = [p for p in valpieces if not p["uncertain"]]
    weak = [p for p in valpieces if p["uncertain"]]
    if not isinstance(claim, int):
        g["verdict"] = "claim-uncertain"
    elif not valpieces:
        g["verdict"] = "unreadable"          # nothing readable at all
    elif claim in ZERO_ROWS and conf:
        g["verdict"] = "impossible"          # the row records no buildings
    else:
        b_claim = B.get(claim)
        # hits by ANY variant of a read (the / alternatives)
        hit = [p for p in conf if b_claim in p["vals"]]
        weakhit = [p for p in weak if b_claim in p["vals"]]
        sumhit = None
        if len(valpieces) <= 6:
            for k in range(1, len(valpieces) + 1):
                for cset in combinations(valpieces, k):
                    if sum(p["val"] for p in cset) == b_claim:
                        sumhit = cset
                        break
                if sumhit:
                    break
        sumnear = None
        if len(valpieces) <= 6:
            for k in range(1, len(valpieces) + 1):
                for cset in combinations(valpieces, k):
                    off = abs(sum(p["val"] for p in cset) - b_claim)
                    if 0 < off <= 15 and (sumnear is None or off < sumnear[0]):
                        sumnear = (off, cset)
        if hit:
            g["verdict"] = "confirmed"
            twins = [r for r in BY_B[b_claim] if r != claim]
            if twins:
                g["notes"].append("the figure is shared with row(s) " +
                                  ",".join(str(r) for r in twins) +
                                  " — resolved by position")
            if len(hit) < len(conf):
                g["notes"].append("extra confident pieces beyond the yard figure")
        elif sumhit:
            g["verdict"] = "confirmed-sum"
            rest = [p for p in valpieces if p not in sumhit]
            if rest:
                g["notes"].append("pieces beyond the matching subset: " +
                                  ", ".join(p["raw"] for p in rest))
            if any(p["uncertain"] for p in sumhit):
                g["verdict"] = "confirmed-sum-weak"
                g["notes"].append("the matching subset includes an uncertain read")
        elif weakhit:
            g["verdict"] = "confirmed-weak"   # the uncertain read agrees
        elif sumnear:
            g["verdict"] = "sum-near"
            off, cset = sumnear
            g["notes"].append("pieces %s sum to %d, the row's %d (off %d)" %
                              (" + ".join(p["raw"] for p in cset),
                               sum(p["val"] for p in cset), b_claim, off))
        else:
            g["verdict"] = "open"
            total_known = sum(p["val"] for p in valpieces)
            if unread and total_known < b_claim:
                g["verdict"] = "open-gap"
                g["notes"].append("the unread piece(s) (%s) would carry the "
                                  "remaining %d saz of the row's %d" %
                                  (", ".join(p["raw"] for p in unread),
                                   b_claim - total_known, b_claim))
            for p in conf:
                done = set()
                for r in [rr for rr in BY_B.get(p["val"], []) if rr != claim]:
                    done.add(r)
                    g["candidates"].append({"piece": p["raw"], "row": r,
                                            "name": ST[str(r)]["name"],
                                            "dist": dist_to(p, r),
                                            "kind": "exact"})
                own = lev(str(p["val"]), str(b_claim)) if b_claim else 9
                if 0 < own <= 1:
                    g["candidates"].append({"piece": p["raw"], "row": claim,
                                            "name": ST[str(claim)]["name"],
                                            "dist": dist_to(p, claim),
                                            "kind": "near-claim", "edits": own})
                near = sorted((lev(str(p["val"]), str(b)), r)
                              for r, b in B.items() if b > 0 and r != claim)
                for d, r in [t for t in near if t[0] <= 1][:3]:
                    if r in done:
                        continue
                    g["candidates"].append({"piece": p["raw"], "row": r,
                                            "name": ST[str(r)]["name"],
                                            "dist": dist_to(p, r),
                                            "kind": "near", "edits": d})
            if not g["candidates"] and g["verdict"] == "open":
                # the elimination proper: only a CONFIDENT figure that fits
                # nothing is a contradiction; weak or unread reads stay open
                if conf:
                    g["verdict"] = "no-match"
                elif unread:
                    g["verdict"] = "open-gap"
                    if not g["notes"]:
                        g["notes"].append("the unread piece(s) leave the test open")
                else:
                    g["verdict"] = "open-weak"
    out.append(g)

# ---- the summary ------------------------------------------------------------
vc = Counter(g["verdict"] for g in out)
print("yards:", sum(len(g["pieces"]) for g in out),
      "pieces for", len(out), "farm claims")
for k, v in vc.most_common():
    print("  %-20s %d" % (k, v))
if resolved:
    print()
    print("CLAIMS RESOLVED BY THE MARK'S OWN RED TAG:")
    for k in sorted(resolved):
        print("  " + k + " -> " + resolved[k])

print()
print("CONFIRMED (a piece, or a subset of the pieces, = the row's figure):")
for g in out:
    if g["verdict"].startswith("confirmed"):
        figs = ", ".join(p["raw"] for p in g["pieces"])
        print("  farm %-3s B=%-5s %-19s (%s)" % (str(g["farm"]),
              B.get(g["farm"], "?") if isinstance(g["farm"], int) else "?",
              g["verdict"], figs))
        for n in g["notes"]:
            print("        - " + n)

print()
print("SUM-NEAR (the pieces close on the row's figure within a stroke):")
for g in out:
    if g["verdict"] == "sum-near":
        print("  farm %-3s B=%-5d" % (str(g["farm"]), B[g["farm"]]))
        for n in g["notes"]:
            print("        - " + n)

print()
print("OPEN-GAP (read pieces fall short; an unread piece could carry the rest):")
for g in out:
    if g["verdict"] == "open-gap":
        figs = ", ".join(p["raw"] for p in g["pieces"])
        print("  farm %-3s B=%-5s (%s)" % (str(g["farm"]), B.get(g["farm"], "?"), figs))
        for n in g["notes"]:
            print("        - " + n)

print()
print("OPEN / OPEN-WEAK (untested; candidates on other rows would show below):")
for g in out:
    if g["verdict"] in ("open", "open-weak"):
        figs = ", ".join(p["raw"] for p in g["pieces"])
        print("  farm %-3s B=%-5s (%s)" % (str(g["farm"]),
              B.get(g["farm"], "?") if isinstance(g["farm"], int) else "?", figs))

print()
print("POINTS ELSEWHERE / NEAR (candidates on other rows, with distance hints):")
any_c = False
for g in out:
    if not g["candidates"]:
        continue
    any_c = True
    print("  farm %-3s (%s)" % (str(g["farm"]), g["verdict"]))
    for c in g["candidates"][:8]:
        d = (", %s px" % c["dist"]) if c.get("dist") is not None else ""
        e = (", %d edit%s" % (c["edits"], "" if c["edits"] == 1 else "s")) \
            if "edits" in c else ""
        print("      %-14s -> row %-3s %-24s%s%s [%s]" %
              (c["piece"], str(c["row"]), c["name"], d, e, c["kind"]))
if not any_c:
    print("  (none)")

print()
print("NO-MATCH (elimination: a confident figure that is no row's yard figure):")
for g in out:
    if g["verdict"] == "no-match":
        figs = ", ".join(p["raw"] for p in g["pieces"]) or "-"
        print("  farm %-3s (%s)" % (str(g["farm"]), figs))

print()
print("IMPOSSIBLE / UNREADABLE / CLAIM-UNCERTAIN:")
for g in out:
    if g["verdict"] in ("impossible", "unreadable", "claim-uncertain"):
        figs = ", ".join(p["raw"] for p in g["pieces"]) or "-"
        print("  %-15s farm %-3s (%s)" % (g["verdict"], str(g["farm"]), figs))

json.dump({"groups": out, "zero_rows": ZERO_ROWS, "resolved": resolved,
           "sites": {str(k): v for k, v in sites.items()}},
          open(ROOT + r"\yard_analysis.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print()
print("wrote yard_analysis.json")
