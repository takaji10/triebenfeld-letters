# Breyer (1935a): notes

## How it came in (2026-10-19)

From the editor's folder "Books_2": "Albert Breyer - [1935] Deutsche Gaue in
Mittelpolen.pdf", Jutta Dennerlein's digital reissue (UpstreamVistula.org,
version 1.0, October 2006) of Breyer's survey, first printed in the
*Ostdeutsche Heimathefte*, Heft 4 (1935), and in the *Deutsche Monatshefte
in Polen*, April 1935. The reissue's own note says it follows the text and
pictures of the *Heimathefte*, with the pictures set slightly differently.
The work is cited by the reissue's pages ("N von 79").

**Only the Kalisz and Konin chapters are taken in** (editor, 2026-10-19:
"For the 1935 article, only bring in Kalisz and Konin"): chapter V, "Der
Warthebruch" (pp. 35 to 38; Konin county and its neighbours along the
Warthe), and chapter VI, "Das Kalischer Land" (pp. 39 to 45; the country
between Zagórów, Konin and Kalisz). Chapter IV, on the Kuyavian lakes, also
names Konin county twice (a picture of Żółwieniec, p. 29; the branch
congregation of Maślaki, p. 34) and is left out with the rest. The
reissue's foreword (PDF page 2) is left out (editor); so is its table of
contents, which lists the whole survey.

    python pipeline/literature/upstream_pdf.py "<Books_2>/Albert Breyer - [1935] Deutsche Gaue in Mittelpolen.pdf" breyer1935gaue --skip 2 --pages 35-45

Two rules were added to the script for this work, and the work of 1938
came out of it unchanged after them: its chapter headings are set large
(Verdana, 12 points) and not bold, and "1000 km²" has a raised 2 that is
not a footnote mark. Footnotes 1 and 2 of the article fall on pages left
out; footnote 3 (p. 39) is the only one here.

The English (`english.md`) is Claude's (2026-10-19).

## Slips in the source, kept

"sielungsfreie" (p. 42, for siedlungsfreie: free for settlement),
"menschenentlegenen" (p. 41, remote from men: an odd word, not a slip that
can be shown). The word "Hollände-reien" is divided over pp. 41 and 42, as
the reissue divides it.

## Points for the reader

- **"Paul von Kolno-Prusiński"** (p. 41) is Breyer's spelling for the owner
  of Trąbczyn who let the woods south of the estate to Olęders in 1746, out
  of which Łazińsk Holland arose. He is Paweł Prusimski, the King's
  chamberlain, who died in 1754 (the editor, 2026-10-20). The year and the
  founder rest on the documents, not on Breyer: the boundary decree of 1775
  (Konin Gr.145, p. 76) cites "the rights granted them in 1746", given by
  "the uncle of Prusimski", and the summons of 1860 (APP 53/968/0/-/783,
  p. 2) names the grantors of that privilege, "Paweł z Kolna Prusiński"
  and his wife Katarzyna z Rozdrażewskich, whom the inspection of 1754
  names as Paweł Prusimski's widow. That the privilege was a hereditary
  lease (Erbpacht) is Breyer's alone: the documents say it settled the
  relations between the owners and the Hollanders.
- **Leśnik's ground money.** Breyer writes here (p. 36), as again in 1938
  (Breyer (1938), p. 20), that the colonists of Leśnik paid Milewski 189
  Thaler of ground money for 10 Hufen. The charter he printed in 1938
  (Breyer (1938), pp. 49 to 56) has no such figure: it sets 1150 Polish
  Gulden of purchase money for each Hufe and a yearly rent of 138 Gulden.
  Where the 189 Thaler come from is not said.
- **The language of 1935.** The chapters praise the settlers and regret
  those townspeople who "shed their inherited nationality" (p. 36). The
  account on the work's page says so.

## Links to the documents (written 2026-10-19, `literature/links.yml`)

- `breyer1935gaue-hollanders`: p. 41 (Łazińsk Holland, founded by Paul von
  Kolno-Prusiński in 1746) to the boundary decree of 1775 (Konin Gr.145,
  document 1), the summons of 1860 (APP 53/968/0/-/783, document 1) and
  Konin Gr.136, document 1, the inspection of Trąbczyn of 9 July 1754,
  made for the widow of Paweł Prusimski the chamberlain. Written first
  (2026-10-19) to the inspection alone, with "the edition has no document
  of 1746": the corpus had not been searched, and the decree and the
  summons both cite the privilege of 1746; the two were added on
  2026-10-20. The privilege itself is not in the edition. The inspection
  names Olędry among the estate's places, counts fifteen Olęders at Nowa
  Wieś with a sixteenth plot empty, and says they took the best wood with
  their plots.

Not written:
- p. 41 to APŁ 39/98/0/-/6603, the liquidation table of the Łazińsk colony:
  the table is of 1868 and later and says nothing of the founding or the
  founder, so it does not bear on Breyer's sentence.
- p. 35 (Sophiental, Friedrichsfeld, Ludwigslust, Ingelfingen, Adelhof) to
  APP 53/968/0/-/801, document 3: the lease of 1806 names none of these
  settlements, only the forest of Drzewce and the takers' home villages.
