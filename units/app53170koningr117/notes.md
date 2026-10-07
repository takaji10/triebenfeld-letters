# 53/17/0/-/Konin Gr.117 (APP)

Thirteen documents on eighteen pages: entries of the Konin castle court
register, 1778 and 1779 (six messengers' reports, five protests, two
register notes). Latin, two with Polish. Added on 2026-10-07 in the fourth
Prusimski-era batch. Status `translated`. Built and verified locally, **not
published**.

**Read the docstring of `intake/holding.py` first**: it has the table of
which entry is on which leaf, scan and page, what was checked and what was
not.

- **Light check only.** Five of eighteen pages word for word, every heading
  and date line, the judges' names. Documents 2, 3, 4, 5, 7, 8 and 9 (the
  long Latin) are marked `rough` in `rulings.yml` and still carry about 190
  marks of doubt. A full check is an afternoon's work per two pages; the
  editor has not asked for it.
- **"Patrui", not "Patrii".** Paweł Prusimski is Antoni's paternal uncle
  ("sui Manifestantis Patruum", leaf 55), and "Relicta Patrui" is Katarzyna,
  born Rozdrażewska. The editor's text had "Patrii"/"Patris" sixteen times
  and the English "father" fifteen times. Seen on leaf 55 ("Patruj", three
  times); corrected everywhere on that ground. `reference/people.yml`
  (prusimski-pawel) now says how the two were related.
- **"cui ... Ipse Patruo Debitor Extitit"** (leaf 55): it is Tracholz who
  was the uncle's debtor, not Chełmski; the English is changed. Document 8
  bears it out.
- **The decree of 20 October 1777 "injunctae Condescensionis"** is not in
  the edition. It is probably entry no. 17 of that sitting in 53/6/0/-/46,
  which the editor transcribed and which was not built (it names Tracholz).
  In the questions file.
- **Dates.** Read: 1, 2, 7, 11. From the sitting's heading elsewhere on the
  opening (`sitting`): 8, 9, 12. Inferred (`rulings.yml`, basis shown): 3 to
  March 1778; 4, 5, 6 to April 1778 (between 1 and 3 April); 10 to 1778
  (between 25 April and 6 May); 13 to 1779 (the heading at the top of leaf
  507 verso is cut off by the photograph).
- **Not on the photographed pages:** the text "sub signo #" of document 10;
  the heading of document 4.
- **Left as the editor has them:** "Super Manifestationem Antonii Prusimski
  Starosti Niesczevicensis" on leaf 54 verso (the scan has "Sup. Mnem" and
  his autograph "Antoni Prusimski Sta: Niesz..."); "Sokołowski" in the
  heading of document 5, who is not in its text; the name of the mound
  "[T?]urnata"; "Joachimenski[?]" / "Joachimczyki[?]" in document 11 (the
  same man is Jachimowicz and Joachimowicz elsewhere); "In praepositurae
  Trąmpczynen~" in document 8, which the English gives as "at the estate"
  and which is the provost's house.
- Szepczyński, "Providus" and court messenger in his own reports, is
  "Laboriosus", a working man, in Nosalski's protest.
- People: Katarzyna Prusimska's entry takes documents 7 and 8, Paweł
  Prusimski's 3 and 7. Not indexed: Tracholz, the judges Walknowski,
  Zielonacki and Mikorski, Czarnecki, Nosalski, Bogusławski, the messengers
  Jankowski and Matuszkiewicz.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 15 scan(s), 9 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- The questions in `docs/PRUSIMSKI_QUESTIONS.md`, the full check among them.
