# Reading a Prussian government file

What was learned from GStA PK, III. HA MdA, III Nr. 12765 (the foreign
ministry's file on the Trąbczyn claim, 1814-1820), written down for the next
file of this kind. The editor confirmed the findings on 2026-10-01. How to take
such a file through the pipeline is in `NEW_UNIT.md` ("A file the office wrote
on"); this is how to read what is on its pages.

## What the pages are

A ministry kept the letters it received and, instead of its own letters, the
drafts of them. So a file alternates between two kinds of page:

- **An incoming letter**, an original in the sender's clean hand, with the
  office's marks added round it: when it came in, whose desk it went to, what
  to answer. Sometimes the whole reply is drafted in the blank space beneath.
- **A draft** (Konzept) of an outgoing letter, in a hurried chancery hand,
  written down the right half of the page with the address, journal number and
  dispatch notes in the left half. Corrections and insertions are everywhere.
  A recognition model reads these badly; expect garbled passages.

A fair copy that was engrossed and then not sent stays in the file too, marked
"cessat". An enclosure sent with a letter is a copy ("Abschrift", "Copie").

## Marks that are not prose

| On the page | Meaning |
|---|---|
| `pr.` and a date, often after a number: `C. 558 pr. 31. Dec. 1814` | praesentatum: the day the letter came in, with its journal number |
| `No. 3205`, `N 6360`, `ad No. 2278. C.` | the journal number the draft goes out under; `ad` ties a paper to an earlier number |
| `Dec: H. L. R. Balan`, or just a name at the head of a letter | Decernent: the official the matter is assigned to (here Herr Legationsrath Balan) |
| `mund.`, `Hg. 3. July mund.` | mundirt: the fair copy has been made |
| `abg.`, `abgegangen`, `den 30. z. Post`, `zur Post` | sent, and when |
| `cessat` (`Cessat et vid. die anderweite Verfügung vom ...`) | cancelled; see the later order |
| `c. a.`, `cum actis`, `appon.` | with the file; attach (the earlier papers) |
| `ad acta` | nothing more to do: file it |
| `vorzulegen`, `dem H. ... vorzulegen` | to be laid before the named official |
| `Ew. p.`, `Ew. pp`, `In p.`, `etc.` in a draft | the clerk fills in the full form of address when engrossing |
| `N. S. D.`, `Ns. S. D.`, `N. Sr. Durchl.` under a draft | Namens Seiner Durchlaucht: issued in the State Chancellor's name. **Not a signature** |
| `M. d. a. A. 3te S.` under a draft | Ministerium der auswärtigen Angelegenheiten, 3te Section: the issuing office. **Not a signature** |
| `B. 18. Juny 16.`, `W. d. 17. März 15` | **the place and date**: Berlin, Wien. The letter before a date is the place, not an initial |
| `1.`, `2.` opening short imperative paragraphs (`Committat dem ...`, `Notificatus dem ...`) | a decree: the orders from which the clerk then writes the drafts |

A transcriber who does not know these reads them as words or names. In 12765
"N. S. D." came out as "M. S. S.", the section line as "M. v. Z. M. Y S.", and
"vorzulegen" as "rengütigen".

## Paraphs

An official approves a draft with a paraph: a few letters of his name, usually
with the day and month. One paraph alone is rarely readable, and the
recognition model guesses a word for it ("Hoym", "Stein", "St.").

**Compare them all before reading any.** Crop every paraph and signature in the
file and lay them side by side, grouped by shape. In 12765, thirty marks sorted
into four hands, and each mark the editor could not read alone fell into a
group with one that could be read. `units/iiihamdaiiinr12765/intake/signature_sheet.py`
builds such a sheet; copy it for a new file.

What then identifies a hand, strongest first:

1. The same mark written out further somewhere ("Bal" for the two strokes
   elsewhere; "Stgm" for "Stg.").
2. A name the file itself gives for that role: the Decernent in the docket, the
   official a paper is "to be laid before", the minister a draft is issued "in
   the name of".
3. Where the mark stops. Hardenberg's paraph is on every draft of 1814-1816
   and on none of 1820, by when he no longer led the foreign ministry.
4. Who held the office at that place and date. This only supports the others.

A date in old style and new (`23/11ten November`, `23. Mai/4. Juin`) is one
day twice: Russian calendar and western. The later is the western date.

## The hands found so far

Vienna (the State Chancellor's chancery at the Congress, 1814-15) and Berlin
(the foreign ministry, 1816-1820):

| Paraph | Who | Where it stands |
|---|---|---|
| a tall initial read `Hbg`, with day and month | Hardenberg, State Chancellor | every draft issued in his name, 1814-1816 |
| `Stg.`, once `Stgm`: "St" in one stroke, then g | Stägemann, Staatsrath | beside Hardenberg's at Vienna; under opinions written in the margin, 1816 |
| `Hoffm` with day and month | an official Hoffmann, probably the counsellor J. G. Hoffmann | Berlin drafts, 1816 and 1820 |
| two tall strokes joined, once written out `Bal`; transcribed `B.` | Balan, Legationsrath, the Decernent | closes each decree, initials each draft, from 1816 |
| `Küster` | of the chancery at Vienna | notes that a petition was handed on |
| `Bever`, `Strenger` | registry clerks | registry notes; Bever also in I. HA GR, Rep. 7 C, Nr. 3570 |

They are in `reference/people.yml`. Once a hand is identified the paraph is
expanded in brackets in the text, like any settled abbreviation:
`H[arden]b[er]g 28/4`, `St[ä]g[emann].`, `Hoffm[ann] 12/8.`, `B[alan].`, and the
place before a date likewise, `B[erlin]. 18. Juny [18]16.` The expanded forms
are what the name patterns match; a bare `B.` could not be matched, since it is
also Berlin.

## Mistakes made on 12765

- Guessing an official from context before comparing the shapes: "Stein[?]"
  was taken for Jordan because a docket named him, and was Stägemann.
- Putting a misreading into a person's `variants:`. The variants are folded
  into the match pattern, so "Hoym" under Hoffmann claimed every mention of
  Minister Hoym in the edition. A misreading belongs in the `identity:` text.
- Asking the editor about one paraph at a time. Four of nine questions came
  back "can't tell"; the side-by-side sheet answered all four.
