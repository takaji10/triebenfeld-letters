# Farm 13 checked: the editor's field readings against statement row 13
# (Shteinbord Iulian, 11 des 103 saz; buildings 0/594, arable 5/2144,
# meadow 1/2104, pasture 2/2058, unusable 0/393).
readings = [
    ("4.", "198"), ("4.", "1926"), ("4.", "1-1584"), ("4.", "288"),
    ("-", "52"), ("", "47"), ("4.", "-684"), ("", "20"),
    ("3.", "-766"), ("-", "26"), ("3.", "2-194"), ("3.", "-72"),
    ("3.", "-328"), ("-", "112"), ("1.", "594"), ("", "108"),
    ("2.", "1-188"), ("2.", "1-1802"), ("", "18"),
]
def val(a):
    if "-" in a:
        d, s = a.split("-")
        return int(d) * 2400 + int(s) if d else int(s)
    return int(a)

pieces = [(lead, a, val(a)) for lead, a in readings]

plots = {}
tracks = []
for lead, a, v in pieces:
    if lead.rstrip(".").isdigit() and lead != "-":
        plots.setdefault(int(lead.rstrip(".")), []).append((a, v))
    else:
        tracks.append((a, v))

print("== the plots (lead n. = the plot's number; its pieces share it) ==")
psum = 0
for k in sorted(plots):
    vs = plots[k]
    tot = sum(v for _, v in vs)
    psum += tot
    print("  plot %d: %d pieces, %s = %d des %d saz" % (
        k, len(vs), " + ".join(a for a, _ in vs), tot // 2400, tot % 2400))
tsum = sum(v for _, v in tracks)
print("  unled smalls (tracks): %s = %d saz" % (
    " + ".join(a for a, _ in tracks), tsum))
total = psum + tsum
print("identified total: %d des %d saz  of the row's 11 des 103 saz (%.0f%%)"
      % (total // 2400, total % 2400, 100 * total / 26503))
print("missing (parcels outside the three crops): %d saz" % (26503 - total))

print("\n== the checks against the statement's columns ==")
print("  plot 1 (594) vs buildings 0/594: %s" % ("EXACT MATCH" if
      sum(v for _, v in plots.get(1, [])) == 594 else "no"))
print("  unled smalls (%d) vs unusable 0/393: off %d saz" % (tsum, 393 - tsum))
print("  pasture 2/2058 = 5058: plot 3's 2-194 (4994) + -72 (72) = 5066, off %d"
      % (5066 - 5058))
print("    (one digit: 2-186 instead of 2-194 -> 4986+72 = 5058 EXACT)")
print("  arable 5/2144 = 14144: 1-1802 (4202) + 1-1584 (3984) + 1-188 (2588)")
print("    + 1926 + -684 + -766 (766) = %d, off %d (one digit: -760 -> EXACT)"
      % (4202 + 3984 + 2588 + 1926 + 684 + 766,
         4202 + 3984 + 2588 + 1926 + 684 + 766 - 14144))
