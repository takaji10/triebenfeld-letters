# Pinkas Hakehillot (1976): Zagórów, Pyzdry, Konin, in JewishGen's English

Three entries of *Pinkas Hakehillot Polin: Encyclopedia of Jewish
Communities, Poland*, vol. I (Yad Vashem, Jerusalem), in the English
translation by Morris Gradel on JewishGen's Yizkor Book Project (project
coordinator Morris Wirth). Added 2026-10-21 at the editor's word, from:

- Zagórów, p. 103: https://www.jewishgen.org/Yizkor/pinkas_poland/pol1_00103a.html (updated 5 Sep 2005)
- Pyzdry, pp. 202-203: https://www.jewishgen.org/Yizkor/pinkas_poland/pol1_00202.html (updated 1 Sep 2005)
- Konin, pp. 235-238: https://www.jewishgen.org/Yizkor/pinkas_poland/pol1_00235.html (updated 7 Sep 2005)

## Rights: kept as Seidel

Each page says: "This material is made available by JewishGen, Inc. and the
Yizkor Book Project for the purpose of fulfilling our mission of
disseminating information about the Holocaust and destroyed Jewish
communities. This material may not be copied, sold or bartered without
JewishGen, Inc.'s permission. Rights may be reserved by the copyright
holder." Claude asked how to keep it; the editor ruled (2026-10-21): "Add
as you did with Seidel": in the public repository, with `visible: false`.
The site lists the work and its page holds only the detailed summary in
`work.yml` (the editor, the same day: a summary for every work not
published), none of the text; `pipeline/verify_site.py` checks that.

## The text

`make_original.py` takes each entry from a saved copy of its page (not
kept), from its page reference to its end: heading, translator's line,
tables (Konin's contents list too), section headings, paragraphs, the Konin
photograph's caption and the translator's notes, as given: the "Z" for
Zagórów, "Andaks" (the Endeks, the National Democrats), the translation's
spellings ("Lódz", "Jozefów Bilgorajski") and slips. Left out: JewishGen's
acknowledgements and disclaimer above each entry (quoted above), the images
and the site's links. The page references become the page marks "[p. 103]",
"[p. 202-203]", "[p. 235-238]": one passage per entry. Every letter of each
entry was checked against its page (2026-10-21: all three agree). The
original is Hebrew; the edition has only the translation, so the work is
English with no english.md. The year 1976 and the editors (Danuta
Dąbrowska, Abraham Wein) are from the Encyclopedia of Camps and Ghettos
(2012), which cites p. 103; JewishGen's pages give neither.

## Against the documents (the documents first)

- **Zagórów's town status.** The entry: 1368. The edition's document is
  King Władysław II's privilege of 19 November 1407 (Kodeks Dyplomatyczny
  Wielkopolski; the edition's KDW, doc. 14), letting the abbot and convent
  of Ląd found a town at their village of Zagórów under Magdeburg law, with
  a weekly market. A difference: the edition follows the document
  (NEEDS_CONFIRMATION).
- **Jews about 1800.** The Zagórów entry has them settle at the turn of the
  eighteenth and nineteenth centuries; the table of the souls of the parish
  of Zagórów of 1791 (ADWł 85, doc. 2) counts only Catholics and dissidents
  in the town (275 men, 298 women). Agrees.
- **Pyzdry and Konin.** No document of the edition speaks of their Jews; the
  KDW speaks of "the town of Pyzdry" in 1377 (doc. 11), after the entry's
  1247. Nothing to settle.
- No document gives the population figures.

## Against the other literature

The Encyclopedia of Camps and Ghettos (2012) cites these entries and
differs on details of 1940-1941; neither is a document, so the edition
rules on neither:
- the Zagórów and Pyzdry entries bring the Jews of Słupca and Pyzdry to
  Zagórów, Rzgów and Grodziec; the Encyclopedia sends 1,000 Jews of Słupca
  to Rzgów (p. 100) and names Kleczew, Golina and Wilczyn for Zagórów
  (p. 120);
- the Zagórów entry has "some 2,000" in the ghetto early in 1941; the
  Encyclopedia 2,170 in 1940, from the Jewish Council's letters;
- the entries date the murder at Kazimierz Biskupi to October 1941; the
  Encyclopedia to late September 1941 (p. 121), and its Grodziec entry to
  "probably between September 24 and October 3" (p. 58).
