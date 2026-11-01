import re

h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\yard_map.html",
         encoding="utf-8").read()
m = re.search(r"<script>\n\(function \(\) \{(.*?)\n\}\)\(\);\n</script>", h, re.S)
s = m.group(1)
checks = {
    "v2 stamp": "v2 · click farm, draw, Enter" in h,
    "no farm input field": 'id="farm"' not in h,
    "refs clickable": "pointer-events: auto" in h,
    "setActive flow": "function setActive" in s,
    "draw auto-on at farm click": "if (!drawMode) toggleMode()" in s,
    "rows carry no buildings": "buildings" not in s,
    "enter without farm guarded": "click a farm number first" in s,
    "yard-then-ref hit order": ("r.idx !== undefined" in s and
                                "r.ref !== undefined" in s),
    "braces balanced": s.count("{") == s.count("}"),
}
print(checks)
