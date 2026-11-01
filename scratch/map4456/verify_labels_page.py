import re

h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\label_sheet.html",
         encoding="utf-8").read()
print("unsure handler present:", "save('unsure')" in h)
print("empty-unsure allowed:", "works empty too" in h)
print("keydown ctrl-enter unsure:", "ev.key === 'Enter' && ev.ctrlKey" in h)
m = re.search(r"<script>\n\(function \(\) \{.*?\}\)\(\);\n</script>", h, re.S)
s = m.group(0) if m else ""
print("inline script found:", bool(m), " braces balanced:", s.count("{") == s.count("}"))
