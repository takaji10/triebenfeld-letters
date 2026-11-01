# Dump the inline script of the built red_map.html and audit it: how many
# mousedown handlers, how many labelAt definitions (function declarations
# override each other by position - a stale one later in the file would
# silently replace the current one), duplicate names, undefined references.
import re

h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\red_map.html",
         encoding="utf-8").read()
m = re.search(r"<script>\n\(function \(\) \{(.*?)\n\}\)\(\);\n</script>", h, re.S)
s = m.group(1)

def count(pat, tag):
    hits = [(s[:mm.start()].count("\n") + 1, s[mm.start():mm.start() + 60].split("\n")[0])
            for mm in re.finditer(pat, s)]
    print("%-28s %d" % (tag, len(hits)))
    for ln, txt in hits:
        print("    line %4d: %s" % (ln, txt.strip()[:70]))

count(r"document\.addEventListener\('mousedown'", "document mousedown handlers")
count(r"function labelAt", "labelAt definitions")
count(r"function trySelect", "trySelect definitions")
count(r"function toggleCard", "toggleCard definitions")
count(r"function toggleNews", "toggleNews definitions")
count(r"function drawAll", "drawAll definitions")
count(r"function addLabel", "addLabel definitions")
count(r"viewer\.addHandler\('canvas-click'", "canvas-click handlers")
count(r"canvas-press|canvas-drag\b", "canvas-press/drag handlers")
count(r"selectMode|selbtn", "select-mode remnants")
count(r"v7 dbg|nearestLabel", "v7 dbg remnants")
count(r"cap\.addEventListener", "capture-layer handlers")
count(r"function selectByElement", "selectByElement")
count(r"function selectHit", "selectHit")

# the line numbers of each function definition, to see which is LAST (wins)
print("\nlabelAt definitions in order (the last one wins):")
for mm in re.finditer(r"function labelAt\s*\(([^)]*)\)", s):
    ln = s[:mm.start()].count("\n") + 1
    print("    line %d  params: %s" % (ln, mm.group(1)))
