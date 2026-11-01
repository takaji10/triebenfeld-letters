import re

for page in ("label_sheet", "red_sheet"):
    h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\%s.html" % page,
             encoding="utf-8").read()
    m = re.search(r"<script>\n\(function \(\) \{.*?\}\)\(\);\n</script>", h, re.S)
    s = m.group(0) if m else ""
    checks = {
        "pointer-events none gone": "pointer-events: none" not in h,
        "drag handlers": "modeAt" in s and "pointerdown" in s and "pointermove" in s,
        "global H keydown": "document.addEventListener('keydown'" in s,
        "ctrl-enter unsure": "ev.key === 'Enter' && ev.ctrlKey" in s,
        "box saved": "a.box = [it.ox + B.bx" in s,
        "braces balanced": s.count("{") == s.count("}"),
    }
    print(page, checks)
