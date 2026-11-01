# Farm 87 checked: the editor's field readings against statement row 87
# (Khaupt Vilgelm; doc 6: buildings 0/321, arable 3/2021, meadow 0/0,
# pasture 3/1980, unusable 0/408, total 7/2330).
readings = [
    ("1.", "288"), ("1.", "1-50"), ("", "68"), ("", "47"),
    ("2.", "1-867"), ("-", "102"), ("", "37"), ("", "28"),
    ("2.", "1-2005"), ("-", "74"), ("-", "8"), ("-", "432"),
    ("", "301"), ("", "36"), ("", "12"), ("", "2"),
]
def val(a):
    if "-" in a:
        d, s = a.split("-")
        return int(d) * 2400 + int(s) if d else int(s)
    return int(a)

plots, tracks = {}, []
for lead, a in readings:
    v = val(a)
    if lead.rstrip(".").isdigit():
        plots.setdefault(int(lead.rstrip(".")), []).append((a, v))
    else:
        tracks.append((a, v))

rt = 7 * 2400 + 2330
cols = {"buildings": 321, "arable": 3 * 2400 + 2021, "meadow": 0,
        "pasture": 3 * 2400 + 1980, "unusable": 408}
print("row 87: Khaupt Vilgelm, total 7/2330 =", rt)
psum = 0
for k in sorted(plots):
    vs = plots[k]
    tot = sum(v for _, v in vs)
    psum += tot
    print("  plot %d: %d pieces (%s) = %d des %d saz" % (
        k, len(vs), " + ".join(a for a, _ in vs), tot // 2400, tot % 2400))
tsum = sum(v for _, v in tracks)
print("  unled (tracks etc.): %s = %d saz" % (
    " + ".join(a for a, _ in tracks), tsum))
total = psum + tsum
print("identified total: %d des %d saz of %d (%.0f%%); missing %d saz"
      % (total // 2400, total % 2400, rt, 100 * total / rt, rt - total))

print("\n== the column checks ==")
for name, cv in cols.items():
    cands = [(k, sum(v for _, v in plots[k])) for k in sorted(plots)
             if abs(sum(v for _, v in plots[k]) - cv) <= 400]
    print("  %-10s %6d  nearest plot(s): %s" % (
        name, cv, ["plot %d (off %+d)" % (k, s - cv) for k, s in cands] or "-"))
# every near-miss of any piece/sum against any column
print("\n== near-misses (within 120 saz of a column) ==")
allf = [(a, v) for k in plots for a, v in plots[k]] + tracks
for a, v in allf:
    for name, cv in cols.items():
        if abs(cv - v) <= 120:
            print("  %-8s (%6d) vs %s %6d  off %+d" % (a, v, name, cv, v - cv))
