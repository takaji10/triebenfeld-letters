# One-shot: the era of the Middle Ages (working name) at the head of reference/eras.yml (CRLF).
# Written 2026-10-16 and tried; held back until the Kodeks's first entries are in, since an era with
# no documents would show empty on the site. Run it once then, from the project root, and then
# write the era's band on the timeline, its timeline note and its section of the story page
# (docs/WORKING_NOTES.md, 'A new era needs four things').
import io

p = 'reference/eras.yml'
b = io.open(p, 'rb').read().decode('utf-8')
assert 'medieval:' not in b
anchor = 'eras:\r\n  prusimski-boundary:\r\n'
assert b.count(anchor) == 1
era = '''eras:
  # A working name until the editor names it (the editor, 2026-10-16: a new
  # era for the Kodeks Dyplomatyczny Wielkopolski, 984 to 1444). Its texts
  # are written when the first entries are in.
  medieval:
    order: 0
    status: populated
    label_en: "Trąbczyn in the Middle Ages"
    label_de: "Trąbczyn im Mittelalter"
    ownership_en: "Before the Prusimski family: the medieval documents of Greater
      Poland that name Trąbczyn and its neighbours. To 1444"
    ownership_de: "Vor der Familie Prusimski: die mittelalterlichen Urkunden
      Großpolens, die Trąbczyn und seine Nachbarn nennen. Bis 1444"
    blurb_en: >-
      Medieval charters and records of Greater Poland that name Trąbczyn, its
      neighbours and the families that held them, from the printed edition of
      the documents of Greater Poland, the Kodeks Dyplomatyczny Wielkopolski.
    blurb_de: >-
      Mittelalterliche Urkunden und Aufzeichnungen Großpolens, die Trąbczyn,
      seine Nachbarn und die Familien nennen, die sie besaßen, aus der
      gedruckten Edition der großpolnischen Urkunden, dem Kodeks Dyplomatyczny
      Wielkopolski.

  prusimski-boundary:
'''.replace('\n', '\r\n')
b = b.replace(anchor, era)
io.open(p, 'wb').write(b.encode('utf-8'))
print('ok')
