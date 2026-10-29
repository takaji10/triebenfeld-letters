# Breyer (1938): notes

## How it came in (2026-10-19)

From the editor's folder "Books_2": "Albert Breyer - [1938] Die deutschen
ländlichen Siedlungen des mittelpolnischen Warthebruchs.pdf", Jutta
Dennerlein's digital reissue of the article (UpstreamVistula.org, version
1.0, November 2010). Breyer's article first appeared in the *Deutsche
Wissenschaftliche Zeitschrift für Polen*, Heft 34 (1938); the PDF does not
give the pages of that print, so the work is cited by the reissue's pages
("N von 59" in its running head). The editor has allowed the reissue to be
used.

`original.md` is made from the PDF's text layer, not retyped:

    python pipeline/literature/upstream_pdf.py "<Books_2>/Albert Breyer - [1938] Die deutschen ländlichen Siedlungen des mittelpolnischen Warthebruchs.pdf" breyer1938 --skip 2 --label 30=Karte --insert "14=[Karte: „A. Breyer. Die deutschen ländlichen Siedlungen des mittelpolnischen Warthebruchs“, gez. A. Breyer. Die Wörter der Karte stehen nicht in der Textschicht der Vorlage.]"

- `--skip 2` leaves out Dennerlein's foreword (the editor, 2026-10-19: "leave
  Dennerlein's forwards out of it for the Breyer texts").
- `--label 30=Karte`: the picture on p. 30 is a map of the places of origin.
- `--insert 14=...`: the map on p. 14 is a picture; its words (the villages
  and their founding years) are not in the text layer, so a line says so.
- The statistics of chapter VI (pp. 45 to 47) are printed on pages turned on
  their side. The script draws each such page upright on a page of its own
  before reading it; read through the turn, the words came out in pieces.

The English (`english.md`) is Claude's (2026-10-19), page by page against the
German. It keeps the German word in brackets beside a term of the time
(Holländerei, Schulz "headman", Erbpacht "hereditary lease", Gratialgut "gift
estate", Sachsengängerei, Entdeutschung "de-Germanisation", völkisch); the
village names and the names of people are left as Breyer spells them.

## What is Dennerlein's, not Breyer's

Two additions of the reissue stand in the text, marked by her initials: "[Viertel,
Ergänzung J.D.]" on p. 16, and footnote 14 (on the Tinf, a coin), which ends
"Ergänzung von J.D." They are kept, as the source has them, and are not
Breyer's words.

## Slips in the source, kept

Nothing is corrected (docs/EDITORIAL_RULES.md). The English shows a slip in
square brackets where the reader needs the German word, and renders the
sense:

- Breyer's text: "Dürfe", "angengigen", "beibehalte", "Bieberjäger",
  "Müntzmacher", "derene", "Groszny", "Ortsaften", "Herkunfsangaben",
  "Dąbroszyr" (in the statistics), "Moderwiesen Die", "nasw", and possibly
  "Rasenerzschwöler". Whether a slip is Breyer's, the printer's or the
  reissue's cannot be told without the print of 1938.
- The charter of Leśnik (pp. 49 to 56, a copy of 1802 of the contract of
  1796): "Gottfreid", "gesonen" (gesonnen, minded), "casirten" (cavirten,
  gave surety), "nährbekannt", "Bufall" and "Buffal", "Kanka", "Kant" and
  "Kunt" for what may be one man, "cull." (a currency), "probandis",
  "Retihabilierung" (ratification).

## What the PDF's tables leave behind

The tables are read cell by cell from the PDF. Four leftovers stand, because
they are the reading of the source and not worth a rule of their own:

- In the statistics (p. 45) the second row of the header (200, 100, up to 50,
  under 50) stands as a row of the table, under the line that marks the
  header.
- The header of the summary (p. 47) has only "Nr." and "Kreis"; its other
  columns are those of the statistics.
- Golina (p. 47, commune 7): its figures stand on the row after its name, as
  the print sets them.
- On p. 25 a passage set in italic is broken at the word "so".

## Spot check of the English

The page on Hohenlohe's estates (p. 21) and the charter of Leśnik (pp. 49
to 56) were read again against the German after they were written
(2026-10-19). Every table on pp. 45 to 47 was compared cell by cell with the
original: only the headers and the county names are translated.

## Points for the reader

- **Breyer's date for Triebenfeld's contract is 18 May 1805** (p. 21). The
  lease in the edition, APP 53/968/0/-/801 document 3, was engrossed on 21
  March 1806; its beginning is lost, so the copy gives no day on which it
  was made. The chamber's consent to the parcelling (document 2) is of 28
  January 1806. Breyer's date may be that of the first agreement; the
  documents are to be followed.
- **Two more points where the lease does not say what Breyer says**
  (checked 2026-10-19, for the link). The clause he quotes on p. 21 (the
  land to be drained by ditches and a dike on the Warta, with a hundred men
  from the lordship) is in none of the nineteen paragraphs of the edition's
  copy. The copy has all of them; what is lost is only its opening, the
  date and the first of the takers' names, where a clause of this kind is
  not to be expected. It may be from another contract, or a draft. And
  where he says on p. 22 that all the settlers had pasture and wood in the
  Prince's heath, § VIII of the lease gives them no claim to firewood or
  pasture in the lordship's other woods and lets them graze only in the
  part of the woods near Drzewce (the lease's "Drzewiec") the lordship
  kept, until that too is sold.
- **K. G. von Weigel** (p. 22), owner of the Zagórów estates from 1828,
  "a great landowner from Hennersdorf in Silesia". The edition's Weigel is
  Carl Ferdinand Weigel, banker at Breslau, a creditor on the same estates
  from 1810 ("Weigel and son" in the letters). Whether they are one man or
  of one family is not shown; asked in `docs/NEEDS_CONFIRMATION.md`.
- **Breyer calls Triebenfeld "der berüchtigte"** ("the notorious", p. 21)
  without saying why. It is his judgement, not a finding.
- **Leśnik: Breyer against his own appendix.** On p. 20 he writes that the
  colonists of Leśnik paid 189 Taler of ground money and had six free years.
  The charter he prints on pp. 49 to 56 has neither: it sets 1150 Polish
  Gulden of purchase money for each Hufe (§ 6) and has dues paid by
  proportion to the land cleared for three years (§ 21). He gives the 189
  Thaler again in 1935 (Breyer (1935a), p. 36).
- **The language of 1938.** The article was written for a journal of the
  German minority in Poland. It praises the "national (völkisch) bearing" of
  the settlers (pp. 22, 28, 29) and sets "evangelisch gleich deutsch" in its
  statistics (p. 48). The account on the work's page says so.

## Links to the documents

Written 2026-10-19 (`literature/links.yml`):
- `breyer1938-lease`: pp. 21 and 22 to APP 53/968/0/-/801, documents 2 and
  3, with what agrees and the three differences above.
- `breyer1938-weigel`: p. 22 (K. G. von Weigel) to Oe 1 Bü 9454, letters 220
  (1811) and 284 (1815), where Weigel is a creditor on the Zagórów estates.
  The plan named III. HA MdA, III. Nr. 12367 (the banker Weigel's
  compensation, 1828-32); that file is about his mortgage on Trąbczyn, not
  Zagórów, and was not linked.

Still to be considered: p. 38 (Ludwigslust, 1816), p. 39 (Święcia, 1818),
pp. 42 and 43 (Schwenz), pp. 46 and 47 (the villages of the estate in 1921)
to the Łazińsk holdings. Each needs its figures read in the documents
first.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> Albert Breyer (1889-1939) is the man whose notebooks of 1936 are among the
> holdings (APP 53/968/0/-/669 and -/716). Its facts are to be held against
> the documents, and its judgements are Breyer's; it praises German settlers
> and laments "de-Germanisation". Pages 38 and 39, 42 and 43, and 46 and 47
> follow the same villages to 1928.
