# The Hohenlohe-Ingelfingen years: plan for the era page

The era page (`site/hohenlohe.md`, German `site/de/hohenlohe.md`) is the
story of the era told from all of its holdings. This file is its plan: what the
page is for, what goes in, the sections, the sources each section rests on, and
what happens to the page when a holding is added. Read it before changing the
page. Settled with the editor on 2026-10-02.

## Why a plan

The page was written on 2026-09-29 from two holdings (the letters, Oe 1 Bü 9454,
and the contracts, Oe 1 Bü 14526). The era now has nine, and more are coming:
smaller files from the Geheimes Staatsarchiv, more on Michalina Prusimska's
complaints, some contracts. No single large file is expected. So the page is
rebuilt once now, on a frame that later files can be added to section by
section, rather than rewritten each time or held back until the sources are
complete.

## Voice (editor, 2026-10-02)

Story voice: the page tells what happened, in order, and may quote the
documents. Metaphor is kept to a minimum. Every statement is a fact the
documents give or a fact of standard history, said plainly; no verdicts and no
flourishes ("the relationship curdles", "a river decides everything", "one
woman, and she wins" are the kind of sentence to take out). Inference is
marked as inference. The house style applies throughout (first mention takes
"a"; a person is introduced once in full and then called by name; no dashes in
English prose; no method).

## What goes in

The test for anything on the page: **does it tell the reader who held these
estates, on what terms, what they yielded, or what happened to the people on
them, from the confiscation of 1794 to the end of the claim in 1820?** If yes,
it goes in, with its names, sums and dates, and a link to the document that
shows it.

- **The routine goes on the holdings' own pages.** Every settler contract,
  every loan, every arrears letter: the page states the pattern, with a count
  and one or two linked examples.
- **Background is a sentence each**, enough to follow the story: the
  partitions, the uprising of 1794, Jena, Tilsit, the Duchy of Warsaw, the
  Congress of Vienna. The glossary and the timeline carry the rest.
- **Other eras get a paragraph and a link.** The Prusimski family before 1794
  belongs to the boundary-dispute era; Michalina Prusimska's tenure of the
  estates after 1807, and her own lawsuits over them, to the restitution era.
  On this page she appears where she acts on the Hohenlohe ownership: her
  complaints of 1800 to 1802, the seizure of 1807, her answers to the claim.
- **The Prince's other affairs come in only where they reach these estates**:
  his Silesian estates and ironworks, his debts, Jena and Prenzlau, his death.
- **Nothing about method.** That is in About this edition.
- **Primary sources first; Seidel with care** (editor, 2026-10-03). The
  documents in this edition and the editor's own research come first. Seidel's
  biography of Hohenlohe-Ingelfingen is a secondary source: it may hold a fact
  the documents do not, and can be cited for it, but it covers the South
  Prussian estates only briefly and makes assumptions the documents correct.
  Where the two disagree, the documents decide; a fact from Seidel alone is
  cited to him as such. The same holds for the timeline
  (`site/_data/timeline.yml`).

Length follows the evidence: about 5,000 to 7,000 words now, under the section
headings below, in English and German written separately.

## Figures that change

The page does not write the era's document count, its span or its number of
holdings into the prose. They come from `site.data.eras` and `site.data.units`
at build time, so a new holding updates them without an edit. The same goes for
the standfirst. (The era's blurb in `reference/eras.yml` also counts years,
"eleven years ... and nine more"; it is corrected with the page: the claim now
runs to 1820.)

## Sections

Each section lists what it says, the holdings it rests on, and the incoming
files expected to add to it. **Status**: *written* is on the page from the
holdings named (all sections, 2026-10-02); *provisional* will change when a
file now pending is read. When a section needs a new holding worked in, mark
it *revise* until it is done.

### Opening, and who is who (*written*)

What the era is, where the estates lay (around Konin and Kalisz, in South
Prussia, Prussia's share of partitioned Poland), and the people the reader
meets throughout: Prince Friedrich Ludwig of Hohenlohe-Ingelfingen; his
building and economy councillor Johann Wilhelm Glenck, who managed the estates
first; Peter Friedrich von Triebenfeld, general agent from 1805; Antoni
Prusimski, the owner they were confiscated from; his daughter Michalina.
Counts and span from the data.

Sources: all holdings. Spellings as settled in `reference/places.yml`
(Zagórów, Kamionna, not Zagorowo, Kaemen).

### I. Confiscation and grant, 1794 to 1797 (*written*; *provisional*)

The uprising of 1794 and Antoni Prusimski's part in it; the confiscation, by
a judgment given at Thorn. Count Hoym's report of 14 July 1796, the cabinet
order of 23 July, and the charter of 9 August 1796 to Hohenlohe-Ingelfingen,
with the six officers granted estates at the same time. What the charter gave
(Kamionna, Kolno, Trąbczyn and its villages, Brzyce) and Hoym's figure of
4,000 Thaler a year. The second charter of 19 June 1797: sixteen former church
villages, Zagórów and Pszczew among them, because Prusimski's estates had
proved heavily indebted; the payment to the crown and the clergy's
maintenance. The handover, which left pledge and lease holders in possession,
and the registration of title, which ran into the Treasury's resignation and
the missing confiscation judgment.

Sources: Nr. 3570 (Hoym's report, the cabinet order, the draft charter);
Oe 1 Bü 14525 (the charters, Hoym's letters, the handover order, the title
papers, the valuations).

Incoming: *Deed of donation* is Nr. 3570, already in. *Anton Prusimski Venice
Residence* and *Minor Prusimska's claims to father's ...*, if they concern the
confiscation and the grant, belong here; their era is to be confirmed when they
are added.

### II. The exchange scheme, 1798 to 1800, and the first challenge, 1800 to 1802 (*written*; *provisional*)

The attempt to trade the scattered estates for the crown domains of Krotoszyn
and Polajewo, and Voss's report against it. As now on the page, without the
flourishes.

Then Michalina Prusimska's complaints to the King against Hohenlohe-Ingelfingen,
1800 to 1802. Nr. 3709 is transcribed (2026-10-04) and the paragraph is
written from it: the suit for Brzyce, the King's orders of 1800, the Prince's
request for other judges, the judgment of 9 December 1800, her petition of 1802.

Sources: Oe 1 Bü 9454 (letters 77 to 101); Nr. 3709.

Incoming: *Complaint of Prusimska against Hohenlohe* is Nr. 3709, in and
transcribed. *Minor Prusimska's claims to father's ...* belongs here or in I.

### III. Dividing the estates, 1798 to 1806 (*written*)

The sale of Kamionna and Kolno to George Conrad Leixner for 142,000 Rthl. The
settlers: Moravian Brethren, Mennonites, the Hauländer; the punctation of
April 1805 for 270 Hufen; the terms the contracts repeat. One lease followed
from contract to court record: Christoph Erbet's Hufe in the Trąbczyn forest,
recorded by the patrimonial court at Mariantów on 31 March 1806. The lease
that failed: Oleśnica, whose three lessees paid half the entry money and then
nothing, and Triebenfeld's petition to the King of September 1805 to have it
sequestered. The revenue survey of 1806. The debts growing faster than the
rents: Countess Schlabrendorff, the Invalids' Fund loan of 1805.

Sources: Oe 1 Bü 14526; Oe 1 Bü 9454; 53/71/0/-/57 (Erbet); 53/968/0/-/801
(the consent of 28 January 1806, the Drzewce lease); I. HA Rep. 162, Nr. 295
(the bond to the Invalids' Fund and the Zagórów mortgage certificate, 1805);
Nr. 3705 (Oleśnica); Oe 1 Bü 14525 (the mortgage entries, the loan of 250,000 Rthl on
Zagórów).

Incoming: *Olesnica estate lease from Hohenlohe* is Nr. 3705, already in.
*Capital on the Zagorow estates* belongs here; further contracts add examples,
not new paragraphs, unless they change the pattern.

### IV. The entail of 1805 (*written*)

The will of 7 October 1805 and the King's confirmation of 19 December 1805,
which bound the South Prussian lordships with the Silesian estates to one heir
and named the third daughter, Auguste, to receive them if the male line ended:
made in the same year as the estates were being let out in parcels. Short.

Sources: Oe 1 U 199; Oe 1 Bü 9454 where the letters touch it.

### V. War, and the loss of the estates, 1806 to 1807 (*written*)

Jena and Prenzlau in a sentence each, and what the letters say (letter 26).
Tilsit; the Duchy of Warsaw; Michalina Dąbska's petitions at Dresden and the
Governing Commission's resolution of 21 July 1807 (added 2026-10-04); the
transfer of the estates to her fourteen weeks after the peace, without a
judgment. The patrimonial court still issuing settlers their papers in January
1808. Her tenure after this is the restitution era's, linked.

Sources: AGAD 1/174/0/2/73 and 1/174/0/1/6 (the petitions and the resolution
of July 1807); Oe 1 Bü 9454 (letters 26, 27, 28, 265b); Nr. 12765 (the petition of
March 1815, which states the sequence); Oe 1 Bü 14526 (contracts 6 and 7).

Incoming: *Hohenlohe operations after Jena* gives one or two sentences at
most, and only if it bears on the estates.

### VI. Lawsuits and arrears, 1808 to 1812 (*written*)

Triebenfeld's arrest in Berlin and flight; the thirteen powers of attorney of
March 1809; thirty-one lawsuits in January 1811; the tribunal at Kalisz
declaring itself without authority to set aside the commission's order; the
settlers in arrears, the remission of 1811, and the proposal to drive them out.

Sources: Oe 1 Bü 9454; Nr. 12765 (the tribunal); Oe 1 Bü 14526 (the relief
clause, the Althütte contract).

Incoming: the two files *Klage der Gräfin Michalina von Miączyńska ...* and
*Miaczynska compensation for confiscation* go here only as far as they concern
the Hohenlohe claim; if they are her own suits over the estates, they open the
restitution era and this section links to them. To be decided as each is added.

### VII. The claim, 1814 to 1816 (*written*)

Vienna: Triebenfeld's petitions to Hardenberg (Paris, May 1814; Vienna,
October 1814 and March 1815), the claim for nine years' revenue, Hohenlohe-
Ingelfingen's own letters to Stein and Hardenberg and his figures, the frontier
on the Prosna, the Hundred Days. Zerboni di Sposetti's report of November 1815
against the claim. The instruction to St Petersburg in April 1816 and the
Russian refusal of November 1816. The widow von Brehmer's petition. The end of
Triebenfeld's letters, his death in early 1816, and the liquidation protocols
with their 142 creditors.

Sources: Oe 1 Bü 9454 (the Vienna letters, letter 303); Nr. 12765.

Incoming: *Claims of Hohenlohe on Trabczyn* is Nr. 12765, already in.

### VIII. After Hohenlohe-Ingelfingen's death, 1818 to 1832 (*written*)

His death in 1818; the heirs' claim recommended by Duke Eugen of Württemberg;
Alopeus's answer of 31 January 1820 that it had been refused in 1816; the
ministry's last step. Short. Then the debts he left on Trąbczyn: Miączyńska's
request of 1819 that Prussia pay them, the refusal, and the Polish judgments
of 1819 to 1827 that struck out the mortgages of Weigel, the Lichnowski
brothers and Grotowski's widow (added 2026-10-04). Last, Prussia's effort at
Warsaw from 1828 to 1832 to have Weigel compensated: Mohrenheim's answers,
Lubecki's exchange with Weigel over the sum, and the valuation ordered again
after the rising (added 2026-10-04).

Sources: Nr. 12765 (documents 27 and 29); III. HA MdA, III. Nr. 12366 and Nr. 12367.

### The people you will keep meeting (*written*)

As now, with the people the new holdings add: Hoym, Glenck as manager,
Leixner, Zerboni di Sposetti, Schöler, Antoni Prusimski. Links to the People
page.

### What to read first (*written*)

Fifteen documents in the order of the sections, drawn from all the holdings
and not only the letters: at least the charter of 1796, the entail, the
Oleśnica petition, the Erbet record, and the Russian refusal.

## The incoming files from the Geheimes Staatsarchiv

From the editor's folder list (2026-10-02; titles as the folders give them,
some cut short). "In" means already in the edition.

| Folder | Holding | Section, or era to confirm |
|---|---|---|
| Deed of donation of Hohenlohe esta... | Nr. 3570, in | I |
| Complaint of Prusimska against Hoh... | Nr. 3709, in | II |
| Olesnica estate lease from Hohe... | Nr. 3705, in | III |
| Claims of Hohenlohe on Trabczyn | Nr. 12765, in | VII, VIII |
| Anton Prusimski Venice Residence | to add: I. HA GR, Rep. 7 C, Nr. 1414 (1797) | I, or the boundary era: confirm |
| Minor Prusimska's claims to father's ... | to add: I. HA GR, Rep. 7 C, Nr. 1413 (1796-1798) | I or II |
| Capital on the Zagorow estates | I. HA Rep. 162, Nr. 295 (copies of 1805), in | III |
| Hohenlohe operations after Jena | to add | V, a sentence at most |
| Biography of Hohenlohe (IV. HA) | to add | Opening, for his life; not a source for the estates |
| Klage der Gräfin Michalina von Miac... (two) | both in: III. HA MdA, III. Nr. 12366 (1818-1827) and Nr. 12367 (1828-1832), placed in the Hohenlohe era for now | VIII; the editor to confirm the era (Hohenlohe or restitution) |
| Miaczynska compensation for confisc... | to add | VI or VII, or the restitution era: confirm |

## When a holding is added

1. Assign its era (`units/<slug>/unit.yml`, `era:`), using the boundary
   above.
2. Find its section in the table above, or add a row.
3. If it only adds examples of what a section already says, add its links
   and nothing more. If it changes what a section says (a new event, a
   correction, a gap filled), rewrite that section in both languages.
4. Update this file: the section's sources and status, and the table.

`docs/NEW_UNIT.md`, section 8 ("What the holding owes the rest of the site"), points here.
