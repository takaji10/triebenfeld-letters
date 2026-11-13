# The owners of Trąbczyn: a second family tree (plan, 2026-11-12)

The editor's request (2026-11-12): a family tree of the
Otto-Trąmpczyński, Prusimski and Miączyński families, "as much as makes
sense for the context of the book ... something that reflects roughly when
each family held the estate, so that the people included in the tree are
relevant"; the Genealogy page split into two, the Zelmer tree and this one,
behind a dropdown; the new tree in the same format and experience as the
Zelmer explorer. Built 2026-11-12 and 2026-11-13, published 2026-11-13. Decisions marked **(editor)**
wait on the editor; the plan takes the default shown until they rule.

## 1. What goes in the tree

**The spine is the line of holders**, era by era, as the edition's
documents give it:

| Family | Held Trąbczyn | From the documents |
|---|---|---|
| Otto-Trąmpczyński | to 1698 | the 1522 division; Wojciech and Jan's sons (1584-1596); Stanisław (d. 1642-44); Władysław (d. before 1693); his sons' partition (1693) and sale (1698) |
| Prusimski | 1698-1794, restored 1807 | Jan na Kolno (bought 1698); Krzysztof (by 1713); his sons (Paweł d. 1754, Antoni, Stefan); Stefan's son Antoni, the Starost (fled 1794); Michalina (restored 1807, d. 1851) |
| Miączyński | 1810s-1892 | Stanisław Adam (Michalina's second husband); Włodzimierz (d. 1879); the nephew Władysław (heir 1879); the sale to Countess Wielopolska (1892) |

**Who is included** - the inclusion rule, applied person by person:

1. Every holder of Trąbczyn or of a share in it, and every spouse of one.
2. Their children, by name, whether or not they held: a child who did not
   hold gets no spouse or descendants unless rule 3 or 4 brings them in.
3. The connecting people: whoever links one holder to the next (Jan na
   Kolno's father, Stefan as the Starost's father, Aleksander Miączyński
   as Władysław's father).
4. People the documents make parties to the estate: the sisters' heirs of
   the 1784 succession, Maciej Debrzyński (1642), Anna Bojanowska's
   Goliński children as far as the 1784 decree charges them on the estate.

What stays out: the ancestors of an in-married spouse beyond their
parents, the descendants of a child who did not hold, and the collateral
lines the documents do not bring into the estate's business. The
database's long Dąmbski, Malczewski, Golińska ancestries are not taken.

The owners who are not of these families - Hohenlohe-Ingelfingen
(1796-1807), Triebenfeld, and the medieval holders of the Kodeks - stay
out of the tree; the timeline and the People page carry them (the
editor's default, accepted 2026-11-12).

**The Wielopolski question** (the editor, 2026-11-12: "I have a hypothesis
that this family (Wielopolska/Wielopolski) is somehow related to the other
families. If you can prove that, it could settle a detail of whether the
Trąbczyn estate 'stayed in the family'"). Słowo of 4 January 1892 has
Trąbczyn sold by Count Miączyński to "Countess Władysławowa Wielopolska",
the wife of a Władysław Wielopolski. Steps A-D look for any kinship
between her (her maiden name, her husband's mother) and the Miączyński,
Prusimski or Dąmbski lines. If one is proved from a source the edition can
cite, the Wielopolskis enter the tree by rule 3 and the 1892 sale is shown
as a sale within the family; if not, she stays out and the question is
recorded in NEEDS_CONFIRMATION with what was found.

## 2. The rule for facts and dates

- **The documents first**, as everywhere: a fact the edition's documents
  state is taken from them and cited to the document (its uid and page);
  where the literature or the database differs, the document stands and
  the difference goes to NEEDS_CONFIRMATION.
- **Minakowska's database** supplies names, kinship and marriages the
  documents do not, cited to the person's ID (sw.*, 4.285.*, 7.885.* ...).
  **Its dates are taken only when exact**: a full date (day, month,
  year), or a year it gives without "?", "ok.", "około", "prawdopodobnie",
  a range or a trailing slash, and only where its own source line backs
  it (a metrical act, a PSB entry, a regest). Every other date of the
  database is dropped. The builder enforces this: a date sourced to the
  database must carry `exact: true` and the source line it rests on, or
  the build fails.
- **Teki Dworzaczka regests** the database cites (its "sw." and "dw."
  numbers) are brought into `literature/tekidworzaczka` as passages (c05
  onward) whenever a fact rests on one, so the tree cites the regest, not
  only the database.
- **Places carry coordinates where they can be had**: the edition's own
  (`reference/place_coords.yml`, `reference/places_osm.yml`, the
  gazetteer) first, then the place's modern locality; a place the edition
  cannot fix is left without, never guessed. They go into the GEDCOM as
  PLAC with MAP LATI/LONG, which the Zelmer parser already reads, so the
  explorer's map works for this tree as for the other.
- **A date range of the documents stays a range** ("d. 1642-1644", "d.
  before 1693"): the explorer's date model (Gramps qualifiers BEF, AFT,
  BET ... AND) already carries these.

## 3. Where the tree lives and how it is built

- **Authored in the repository**, not in Gramps: `reference/estate_tree.yml`,
  one record per person (names, sex, parents, marriages, events with
  date, place, source and page), the same discipline as
  `reference/genealogy.yml`. The editor's Gramps database stays the Zelmer
  tree's source; this tree's source is the edition.
- **Built through the Zelmer pipeline**: `pipeline/genealogy/build_estate.py`
  writes the YAML out as a GEDCOM (`site/genealogy/trabczyn/estate.ged`,
  committed - the editor can open it in Gramps), then runs the existing
  `gedcom.py` parser and `build_data.build_all()` on it, so the JSON is the
  Zelmer JSON's shape by construction. Output:
  `site/genealogy/trabczyn/data/`. No media, no privacy step (no living
  person), no exclusion step.
- **Sources** are the edition's: each source record names a holding, a
  work of the literature or a database page, with its URL on the site (a
  document's page, a literature passage, /people/<slug>/ where a person
  page exists) or on the web (the database's page). The explorer gains a
  `url` on a source and shows it as a link.
- **Checks**: the builder fails on a fact with no source, a database date
  without `exact: true`, a parent or spouse ID that does not exist, or a
  person whom no rule of section 1 admits (each record names its rule).
  `pipeline/verify_site.py` checks the second explorer's page and data are
  present and every source URL on the site resolves.

## 4. The explorer: two trees, one app

The app (`site/genealogy/src`, Svelte, built by Vite into
`site/genealogy/assets/`, committed) loads its data relative to its page,
so a second page in a subfolder serves a second tree with the same code:

- **Both trees in subfolders** (the editor, 2026-11-12): the Zelmer tree
  moves to `/genealogy/zelmer/` (its data with it, the Python build's
  output path changed), the new one is `/genealogy/trabczyn/`; both
  `index.html` are made from the one shell by `prepare.cjs`, pointing at
  the shared `../assets/`. `/genealogy/` itself becomes a small chooser
  page that forwards an old link with a hash (`/genealogy/#/person/I0012`)
  to `/genealogy/zelmer/` with the hash kept, so no link from outside
  breaks; every link inside the site and the pipeline is updated.
- What is hard-coded becomes per tree, read from the tree's `meta.json`:
  the title ("Zelmer Family Explorer" / the new label), the start person
  of the big tree (`START_PERSON`), the "back to the site" link's depth,
  and whether there is media.
- A switch between the two trees in the app's own header, besides the
  site's.
- Person pages of the edition and the tree link each other: a tree person
  with a page on /people/ shows "Their page in the edition"; a person page
  shows "In the family tree".
- `check_tree_layout.mjs` (the layout battery) runs on both trees.

## 5. The site

- The header's **Genealogy** becomes a dropdown like Sources: "The Zelmer
  family" and "Owners of Trąbczyn" (German "Die Familie Zelmer", "Die
  Besitzer von Trąbczyn"; the default, accepted 2026-11-12).
- The German page: the explorer is bilingual in its own i18n; the new
  strings are added to it.

## 6. The work, and who does it

The browser work needs the editor's sign-in and stays in the main
session; the bulk reading and the code go to Sonnet sub-agents with
written briefs, and their output is read before it is used.

| Step | What | Who |
|---|---|---|
| A | The edition's statements of kinship and holding for the Prusimskis (the Konin court books, the decrees of 1775 and 1784, the citation of 1782, the AGAD restitution file, Żychliński 1885, the PSB, Pachoński) into a facts table with uid and page | Sonnet sub-agent |
| B | The same for the Miączyńskis and Dąmbskis (Oe 1 Bü 9454, the summons of 1860, the death notice of 1879, Słowo 1892, Breyer's notes, Żychliński 1891, the Minakowska pages held) | Sonnet sub-agent, in parallel with A |
| C | Minakowska: the editor signs in in the browser pane; the main session opens the IDs the spine needs and saves each page's text to `review/minakowska/` (gitignored: the pages carry the login) | main session |
| D | The database pages into the facts table, with the exact-date filter, the source line beside each date | Sonnet sub-agent, after C |
| E | Reconcile A, B, D and the Trąmpczyński pages already written into `reference/estate_tree.yml`; differences to NEEDS_CONFIRMATION | main session |
| F | `build_estate.py` (YAML to GEDCOM to JSON) and its checks | Sonnet sub-agent, from a written spec, in parallel with C-E |
| G | The app: data per tree, meta-driven title and start person, source links, the switch; the Vite build; the layout battery on both trees | Sonnet sub-agent, in parallel with F; the main session reviews the diff |
| H | The site dropdown, the cross-links, verify_site, the browser check on desktop and phone, the docs | main session |

Order: A, B, F and G start together; C waits for the editor's sign-in;
D follows C; E follows A, B and D; H last. The editor's review comes
before anything is published.

## 7. Settled before building (2026-11-12)

The editor accepted the defaults: the label "Owners of Trąbczyn"; the
non-family owners out (Wielopolska pending the question above); the work
of the morning committed on `trampczynski-family` and the tree built on the
same branch. Added: the Zelmer tree at `/genealogy/zelmer/`, coordinates
for the tree's places.

## 8. The editor's two charts checked (2026-11-12)

The editor sent two charts (the Prusimski line from Jan na Kolno to Antoni
the Starost; Antoni to the Miączyński grandchildren), red boxes marking
owners of Trąbczyn, and asked for them to be checked. Against the
documents, the Teki Dworzaczka regests and Minakowska's pages:

- **Jan na Kolno's children**: the sources give Sebastian, Krzysztof,
  Ludwik, Teresa (m. Jan Otto-Trąmpczyński) and **Anna** (m. Maciej
  Watta-Belęcki, then Jan Dobrogost Brudzewski; childless; the decree of
  1784). The chart's **Konstancja (b. ~1680, d. 1726)** has no source: the
  only Konstancjas are Krzysztof's daughter (m. Jan Wierusz-Kowalski) and
  Konstancja Krusińska, Teresa Golińska's mother. **Ludwik** (d. before
  23 July 1708) is missing from the chart. Anna's "d. 1707" is the
  database's "1707/", which marks a date she was alive, not her death.
- **Sebastian should be red**: Trąbczyn fell to him in the division of 1700
  and he sold it to his elder brother Krzysztof in 1720 (regest c10).
- **Krzysztof's children**: add **Bogumił** (d. childless before 1738,
  the citation of 1782); Wiktoria married three times (Wysocki,
  Odechowski, Tworowicz). **Stefan "b. ~1670"** cannot be (his father was
  born about 1680 on the same chart); no source dates his birth.
- **Who held Trąbczyn after 1720**: Krzysztof; then his sons together
  until the division of 1740, in which **Paweł** took the scheda with
  Trąbczyn (Antoni the elder took Wierzbno, Brzezno and Szetlewko, Stefan
  Kolno and Kamionna); Paweł's widow **Katarzyna** held it for life from
  1754; the Starost **Antoni** was heir by 1766. So Antoni the elder and
  Stefan held only as co-heirs before 1740.
- **Marianna Dąmbska's death**: dead before the Venice dispatch of 14
  December 1796 (I. HA GR Rep. 7 C Nr. 1414, doc. 2): the first chart's
  "~1804" is wrong, the second's "~1796" right as a bound.
- **Józef Dąmbski "b. ~1790, d. 1809"**: the database's "około 1790" is
  an estimate (impossible for a man married in the 1790s), and 1809 is
  the death year of his **father** Stanisław Dąmbski; the PSB has Józef
  dying in 1798.
- **Bronisława Kalkstein "b. 1810, d. 1869"** repeats her husband
  Aleksander's years; she lived 1825-1858.
- **Klementyna "Glyńska"** is Glińska (1826-1895).
- **Tadeusz Miączyński (1857-1923) in red**: right. The editor reported
  on 2026-11-13 that the town history sign at Trąbczyn has him buying the
  estate back in 1896; Breyer's notes (1936) have "Graf Miączyński" owning
  it about 1911. Entered as a holder; the act of 1896 is still to be found.
- **Stanisław Adam Miączyński in red**: the documents make Michalina the
  owner (1807, 1827, 1846); the judgment of 1827 has him co-lord with her,
  and his legitimation of 1838 calls him "dziedzic dóbr Trąbczyn". Kept
  as a holder.

**The owner mark** (the editor asked whether to keep it): kept, and made
consistent by deriving it from the data. Every person whose `rule` is
`holder` in `reference/estate_tree.yml` carries the mark in the explorer,
with a legend. A holder is anyone the sources show holding Trąbczyn or a
share of it: heirs and co-heirs, buyers, and widows holding it for life
(Anna z Słończyc 1644, Katarzyna Rozdrażewska 1754). The Zelmer tree has
no holders and shows no mark.

**Remarriages** (the editor: "is there a standardised way of showing
this?"): the standard of genealogical charts, as the editor's second chart
draws it: the person once, each spouse beside them in marriage order (two:
first on the left, second on the right; three or more: in order to the
right, the marriage lines numbered), each marriage's children hanging from
that couple's own line. The Zelmer tree has 43 people with children by two
or more marriages and 20 married three times or more; the explorer drew
all children under one spouse until 2026-11-12.
