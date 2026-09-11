# Context Brief: Trąbczyn Documents Website

*A framing document for the site that will let users browse scans, transcriptions, and translations of the Trąbczyn estate archive by timeline. Intended to be introduced to a separate project/assistant building the site, so it inherits the research framing rather than treating documents as a flat archive.*

---

## 1. Governing Thesis (must shape every design decision)

This site is built from the archive supporting a scholarly book, *Traces in the Sand — Uncovering Three Centuries of German Olęder Settlement on the Trąbczyn Estate Through the Zelmer Family History*.

The book's framing principle, and therefore the site's:

> **Olęders are the focus. The Zelmer family is the analytical lens. Estate ownership history (Prusimski → Hohenlohe-Ingelfingen → Miączyńska) is the mechanism, not the subject.**

This matters concretely for the website: if documents are organized primarily by *estate owner* or *noble family dispute*, the settler community — the actual subject of the research — becomes background scenery in its own archive. Owner-era should function as a navigational/chronological scaffold, not the thematic headline.

---

## 2. Era Schema (build the full structure now, populate incrementally)

The site is currently being populated with only the Hohenlohe-Ingelfingen era. To avoid restructuring later, the data model should include all eras from the start, even empty ones:

| Era | Approx. dates | Key parties | Status |
|---|---|---|---|
| Trąbczyn–Łukom boundary dispute | c. 1589–1788 | Prusimski, Chełmski families | Not yet populated |
| Hohenlohe-Ingelfingen ownership | 1796–1807 | Prince Friedrich Ludwig zu Hohenlohe-Ingelfingen, P. F. A. von Triebenfeld | **Currently being built** |
| Prusimska/Miączyńska restitution | 1807 onward | Michalina z Prusimskich Dąbska/Miączyńska | Not yet populated |

Each document record should carry an `era` field so the timeline view doesn't need re-architecting when the other two eras are added — only backfilling.

---

## 3. Document Metadata Schema

Based on how documents are actually tracked in the research project, each entry should carry:

- **Archival reference** (e.g., `III. HA MdA III Nr. 12765`, `I. HA GR Rep. 7 C Nr. 3570`)
- **Repository** (APP Poznań, GStA PK Berlin, Hohenlohe-Zentralarchiv Neuenstein, AGAD Warsaw)
- **Original language** (German, Polish, Latin, French)
- **Document type** (deed, complaint, court decree, correspondence, lease, census/liquidation record, etc.)
- **Era tag** (per Section 2)
- **Corpus role**: is this a *central* document (e.g., the 1776 boundary commission decree) or *supporting evidence*?
- **Transcription status** (not started / Transkribus draft / manually cleaned / final)
- **Translation status** (not started / draft / reviewed / final)
- **Linked entities** (see Section 4)

---

## 4. Key Figures as Cross-Cutting Entities

Figures should be modeled as standalone entities linked across documents and eras — not attributes of a single era's document set. Several figures span eras and this needs to be visible in navigation:

- **Michalina z Prusimskich Dąbska (later Miączyńska)** — the restitution-era figure, but her claims directly reference earlier Prusimski-era holdings
- **Antoni Prusimski** — Starost of Niszczewice, central to the boundary dispute era, but his ownership is also the legal baseline Hohenlohe-era documents dispute
- **The Zelmer/Celmer family** — the genealogical throughline across all three eras; this is the connective tissue the site should make easy to follow regardless of which era a user starts browsing

If figures are treated as first-class entities with cross-references, a user following "Michalina" or "the Zelmer family" through the timeline should be able to move across eras seamlessly once those eras are populated.

---

## 5. Terminology and Voice Constraints

The book enforces a strict no-paraphrase policy on source text and has settled several terminology corrections. These should extend to *site copy describing documents*, not just to the translations themselves, to avoid reintroducing already-corrected errors:

- *Sąd grodzki* = municipal court; *sąd ziemski* = land court — these are distinct terms, not interchangeable
- *Hippocaustorum/hypocausti* = heated room/stove room (confirmed reading) — not "chestnut" (a prior misreading to avoid resurrecting)
- *Pastor* in Latin documents = shepherd, not "Lutheran pastor"
- *Roboracja* = formal court enrollment giving binding legal force, distinct from simple contract-signing
- The 1746 Olęder founding date is the primary chronological anchor of the whole project — if the site has any single "start point" moment, this is it

General voice: measured, source-grounded, no rhetorical flourish — matching the book's own prose conventions rather than a typical "museum website" tone.

---

## 6. Current Build State (as of this writing)

- Only the **Hohenlohe-Ingelfingen era** (1796–1807) is currently being described/populated
- The Prusimski-era boundary dispute and the Miączyńska restitution era exist in the underlying research but have **not yet** been added to the site
- The book itself references an existing interactive bilingual (German/English) website concept with a language toggle — worth confirming whether this new site is that same effort or a distinct one, since document translation work is already tracked toward that bilingual goal

---

## 6. Name and Place Standardization

The book already operates under a settled standardization rule, and the site should inherit it rather than re-deciding it independently:

**Governing rule:** All personal names and place names are kept in their original Polish form, with Polish diacritics preserved. Spelling variants of the same name are standardized to the *most frequent form* found across the documents — applied silently, with no editorial note calling attention to the standardization.

**Name display order:** Personal names follow English reading order — given name, then family name, then titles/honorifics. Predicate particles (*z*, "of") follow the family name when they indicate origin (e.g., "Józef Brzeziński of Brzyzna," not the Polish-order interleaving of titles).

**Known place-name variant sets requiring resolution on the site:**
- Łukom / Łukomia
- Trąbczyn / Trąpczyn
- Trąbczyńskie Stare Olędry / Łazińsk / Łaziny
- Michalinów Oleśnicki vs. Michalinów Olędry

**Known person-name complexity:** The Trąmpczyński, Prusimski, and Chełmski families reuse the same given names across two centuries, so name alone is not a reliable identifier — generational disambiguation (cross-checked against Boniecki, Pachoński, and the *Polski Słownik Biograficzny*) is necessary. One specific flagged case: the primary-source form "Albertus Trąmpczyński Otha" versus the later-reference form "Wojciech Trąmpczyński" is a documented divergence between source generations, not an error to silently merge into one canonical spelling.

**Recommended entity model for the site:** Mirror the book's own Consistency Register structure for Persons and Places — each entity gets a canonical name, a list of spelling variants encountered (with the document/location each variant appears in), and open questions/notes. Concretely, each person or place entity should carry:
- Canonical display name (Polish diacritics preserved)
- List of source-spelling variants, for search/matching purposes
- First appearance and later appearances across the corpus
- Linked documents
- Open questions or unresolved identity conflicts (flagged, not silently resolved)

This lets site search match on any variant a user might type while always *displaying* the canonical form — and keeps the site's entity index consistent with the book's own Consistency Register rather than drifting into a separate, competing standardization.

## How to use this brief

The intent is for the receiving project to treat Sections 2–4 as the shape of the data model (even before all data exists), Section 1 as the interpretive lens for any editorial/UI copy, Section 5 as a hard constraint on terminology used anywhere on the site, and Section 6 as the standard the site's own name/place entity index should follow — so it stays interoperable with the book's Consistency Register rather than diverging from it.
