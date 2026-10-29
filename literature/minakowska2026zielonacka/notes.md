# Minakowska (2026): the page of Helena Zielonacka in Wielka genealogia Minakowskiej

The page of Helena Zielonacka, person 2.976.216 of M. J. Minakowska's online
database (https://www.sejm-wielki.pl/b/2.976.216), its own citation line
"Maria Jadwiga Minakowska, Wielka genealogia Minakowskiej (Wielcy.pl),
wydanie z 22.10.2026". Added 2026-10-22 at the editor's word, "related to
Chełmski". The second of the database's pages (the first:
`minakowska2026prusimski`, whose notes carry the standing rule,
docs/LITERATURE_PLAN.md, section 22).

## The source

The editor's saved page, in their Downloads folder: "Helena Zielonacka
(M.J. Minakowska, Wielka Genealogia Minakowskiego) - Wielka Genealogia
Minakowskiej - M.J. Minakowska.htm". The page is **not** kept in the
repository: its header carries the editor's login and its footer the
visitor's IP address. `make_original.py` makes `original.md` and `full.md`
from it and says what it does.

**The page is the database's English user interface.** The database renders
its pages in the reader's language: the first of these works was saved in
Polish, this one in English. So this work's language is `en` and it has no
`english.md` - the page as saved is the one text the site shows, as
Mączak (1968) is. The names, the offices (kanonik, skarbnik, cześnik) and
the source lines stay Polish whatever the interface, and the Teki
Dworzaczka regest of 1727 in the Notes is Polish. A future page of the
database takes whichever language its saved page carries; the rule is
otherwise unchanged. The work.yml says this in its header comment.

The page is written in ISO-8859-2, as the first one was.

The person's ID carries the database's Boniecki numbering (2.976.…): the
person is one of the entries of article 2.976 of the online Boniecki, the
Chełmscy h. Ostoja - the article whose branch that held Łukomia the edition
holds as `boniecki1900`. Her entry number there, 2.976.216, lies inside the
item range that work brought in (162-240), and the marriage it records is
in its passage c04.

## What is brought in (the standing selection, section 22)

The biography, the parents with the ancestor tree (the database knows
little of it: most of the sixteen ancestors are its "?"), and the two
marriages with their children and grandchildren - to Józef
Ścibor-Chełmski, with Katarzyna, Heliodor, Stanisław, Józefa, Nepomucena
and Tomasz and the grandchildren through them; and to Jakub Rościszewski,
with Agnieszka and the Bronisz line through her. Not brought in: the
siblings, the mother's other marriages (Jan Imieliński, Antoni Wstowski,
with their children), the uncles and aunts and cousins, and the nearest PSB
persons - all in `full.md`. The Notes are not brought in; the person's page
says in a sentence what they hold.

Two of the page's marks are new here, and kept as printed:

- **"«Scibor»"**: the database's marker inside the father's name
  ("Andrzej «Scibor» Ścibor-Chełmski"), setting the name-part apart;
- the office lines joined with a comma ("Heliodor, kanonik [poz] Poznań
  (1765)"), the English interface printing the office on its own line.

The dropped status line: the page's header carries "Not belonging to the
Genealogy of descendants of the Great Sejm" - the database's statement that
Helena is not one of its Sejm-Wielki descendants proper. It is dropped as
chrome with the rest of the site's furniture, and recorded here because it
says something of the person. (The first work's page carried its own status
line, "Najbliższa rodzina uczestnika Sejmu Wielkiego", dropped the same
way: a status line is chrome, and the fact it carries goes into the work's
notes, not into the site's text.)

## Against the documents (the documents first)

- **The husband.** Józef Ścibor-Chełmski, heir of Łukomia (Łukom) and
  Łomowo, son of Andrzej, ensign of Sandomierz: the land court's decree of
  1728 (APP 53/6/0/-/40) names "Franciscus et Josephus Ścibor Chełmscy",
  heirs of Łukom and Łomowo, the sons of Andrzej - as Boniecki's article
  does (c04: "Z Pałuskiej miał synów: Franciszka bezpotomnego i Józefa,
  żonatego z Heleną Zielonacką"). The database's page agrees with both, and
  adds the name of the mother (N. née Pałuska, unknown to Boniecki) and the
  arms and seat (z Chełmu i Woli h. Ostoja).
- **The sons.** Heliodor and Stanisław are the brothers of the boundary
  decree of 1775 (APP 53/17/0/-/Konin Gr.145) and of the edition's potash
  suit and estates: Stanisław at law with Katarzyna Prusimska 1761-1763
  (APP 53/6/0/-/45), heir of the four estates from 1766, already "Treasurer
  of Wschowa" in April 1778 (Konin Gr.117, document 4). The page's offices
  agree with Boniecki's (canon of Poznań 1765; Treasurer of Wschowa 1779),
  with the decree's "canon of Chełmno" and the 1778 document's earlier
  title left as the differences the edition's NEEDS_CONFIRMATION already
  carries for Boniecki; the edition follows the documents.
- **The marriage year.** The page's "about 1720" is the database's
  estimate, and is not used (EDITORIAL_RULES, 2026-10-22). The record of
  1727 (below) has her already married by then, and the database's estimate
  does not gainsay it.
- **Her dates.** "Born possibly in 1700" is the database's estimate: no
  dates of hers are shown anywhere. Her children's birth years on the page
  are the database's estimates too (?1730-, ?1760-, ?1770-) and none is
  shown; the grandchildren's years, where the page gives them without an
  estimate (1793, 1794-1821, 1789-1845, 1795-1867, 1807-1877, and the
  Bronisz line's 1794-1860, 1835-1917, 1849-1913), are stated by the
  database and shown on the person's page with the work as their source,
  the "ca" of Izabela (ca 1799-1839) and Franciszek Ksawery (ca 1779-1844)
  kept as it stands.
- **The regest of 1727** (the Notes; Teki Dworzaczka, Regesty: Księgi
  grodzkie konińskie, nr 13049, Nr. 76): Józef Ścibor Chełmski, heir of
  Łukom and Łomowo, "having received 3,000 złp from Kazimierz Zielonacki
  for Helena Z., daughter of the late Andrzej Z. by Joanna Kowalska, now
  his wife, his ward as well (stryja, i op.), against her portion from her
  father's estates (na poczet pos. z dd. jej ojcz.), recorded the sum on
  his own estates" (fol. 196 verso). Kazimierz Zielonacki, not named
  elsewhere on the page, was presumably her brother or uncle - the page's
  siblings section names only a sister, Marianna (NEEDS_CONFIRMATION).
  This is the Chełmski family's own record, from a Konin municipal-court
  book of 1727 - the edition holds Konin books from 1754 on and the land
  court's decree of 1728, but not this register. Whether the holding behind
  it is to be sought is the editor's (NEEDS_CONFIRMATION). The regest stays
  in `full.md`.

The database's page and Boniecki agree on the family; where the page adds
names and dates Boniecki does not give (the mother Pałuska, the children's
names, the Bronisz line), the source is the database's compilation, and the
person's page carries the work as the source beside every fact.

## The index

The work's 6 hits were read in context (Claude, 2026-10-22) and ruled in
`literature/index.yml`: all are the Chełmski family entry (`chemski`), whose
ruling "Chełmski: yes" now carries the comment - the "Chełmski" of
"Ścibor-Chełmski" on this page are her husband (the decree of 1728's), his
and her son Tomasz, and Tomasz's sons. Her sons Heliodor and Stanisław are
of the family too, but their names stand on the page without the surname
("Heliodor"; "Stanisław, skarbnik [poz] Wschowa"), so the pattern does not
take them. No other person or place of the edition is named in the
brought-in text.

## The person's page

/people/helena-zielonacka/ (German /de/personen/helena-zielonacka/), the
first for a person who has no entry of the edition: a standalone block of
`reference/genealogy.yml` (`standalone: true`), with its own heading and
biography, no list of documents, and the literature named by hand -
`boniecki1900/c04` (the marriage as Boniecki records it) and the work's own
marriage passage. The machinery is `pipeline/build/person_pages.py`; the
rule is in `docs/LITERATURE_PLAN.md`, section 22.

## Links

None written yet. The obvious one, when the editor wants it: the work's
marriage passage against the decree of 1728 (APP 53/6/0/-/40) and Boniecki
c04 - the same family, the database's page adding what the decree does not
say.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> Józef is the heir of Łukomia and Łomowo whom the decree of 1728 names with
> his brother Franciszek; Heliodor and Stanisław are the Chełmski brothers of
> the boundary decree of 1775; Józefa and Nepomucena married the Bieńkowski
> brothers. Boniecki's article (t. II, s. 364) is Boniecki (1900) on the
> Literature page. The whole page is kept in the work's folder as full.md. The
> tags in brackets ("[poz]", "[san]") are the site's marks of the province of
> an office.
