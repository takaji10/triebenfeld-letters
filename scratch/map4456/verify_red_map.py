import re

h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\red_map.html",
         encoding="utf-8").read()
m = re.search(r"<script>\n\(function \(\) \{(.*?)\n\}\)\(\);\n</script>", h, re.S)
s = m.group(1)
checks = {
    "v12 stamp": "(v12 · own-box outlines)" in h,
    "selection works (pointer+mouse)": ("addEventListener('pointerdown', onPress, true)" in s and
                                        "addEventListener('mousedown', onPress, true)" in s),
    "diag block present": "MAIN SCRIPT NOT ALIVE" in h,
    "own-box outline for fixed": "a.box[0] + a.box[2]" in s,
    "no default box in toggleCard": "card.x - 35" not in s,
    "no default box in toggleNews": "a.w || 70" not in s,
    "pan-mode click is a no-op": "phantom default box is gone" in s,
    "degenerate click makes no box": "a click, not a drag: no box" in s,
    "text-only commit path": "if (pendRect) {" in s and "a.fix = 'moved'" in s,
    "fly only from sidebar": "toggleCard(a, true)" in s,
    "braces balanced main": s.count("{") == s.count("}"),
}
print(checks)
