# APP 53/968/0/-/545

Albert Breyer's research sheets on the Polonisation of surnames in the gmina
Zagórów ("Polonisierta Namen [gmina Zagórów - nazwiska mieszkańców]"): ten
photographed sheets of his own notes, German and Polish. Added on
2026-10-25 at the editor's request. **The transcription is a draft, waiting
on the editor's answers to the sheet "Readings in Breyer's sheets 1".**

## The images

Image00024 to Image00034 in the editor's folder of that name on J:.
Image00024 is the photograph of the folder itself and is left out (the
editor, 2026-10-25). Image00025 to Image00034 are ten photographed sheets,
each one page, no fold: `intake/build_pages.py` copies them into
`processed/` as `Image00025_a.jpg` ... `Image00034_a.jpg`.

What each sheet carries (from the machine reading of 2026-10-25):

- **0025** — a short list headed "P. Winkler Polonisiert Namen": pairs of a
  German surname and its Polonised form, with years (7. 1855; 1843).
- **0026** — a list headed "Poloniatura"(?), numbered 1-19: German surname -
  Polonised form (Mittmann - Nowak ... Brodel - Brudel).
- **0027** — an alphabetical list A-Z of Polonised surnames (Arminski ...
  Wilmański), the letters C, E, T, U, V and Z apparently empty.
- **0028** — Breyer's excerpt in his own hand of a Breslau print of 1741:
  "deutsche Briefe von George Schlag, Morgenprediger zu St. Hieronymi u.
  der polnischen Schule verordneter Moderator. Breslau, den 18. September
  1741", with nine pairs of a Polish name and its German form (Wojciech
  Wilkotek - Albrecht ...). The editor ruled that every page of this holding
  is Breyer's own notes, so this is his copy, not a photographed print.
- **0029-0030** — one continuous numbered list of Polonised surnames,
  1 to 53, running across three columns of 0029 and onto 0030; the top of
  0029 has a heading read as "Polonisazja techniczna"(?) and a block of
  pairs of a German name and its Polonised translation (Gross - Grosz(?),
  Erdmann - Zieminski(?), Hoppe - Chmielewski).
- **0031-0034** — dense handwritten German prose, Breyer's discussion of the
  Polonisation of names. **Not yet transcribed**: see below.

## How the reading was made

The session that made this draft could not see the images: the scans were
read only through the lunaroute document converter (the reader of Kraus 2001
and Werner 1904), whole page first, then in overlapping bands cut with PIL
at 2 to 3 times the size, then single lines and blocks where the bands
disagreed. Tesseract 5.5.3 was tried first and produced nothing on these
pages: the hand is handwriting, not print. The list sheets (0025-0030) came
out well enough to draft; the prose sheets (0031-0034) defeated it — the
band readings there contradict one another and invent German where the hand
defeats them, so nothing of those pages is in the transcription.

Every doubtful reading is marked `[?]` in the draft and asked on the sheet:
`python units/app539680545/intake/spot_sheet1.py` (port 4103), answers to
`review/app539680545/readings1_answers.json`, 31 rows, one per strip that
carries a doubtful reading.

## Documents (draft, to confirm with the editor)

1. 0025, the "P. Winkler" list.
2. 0026, the numbered list of 19 pairs.
3. 0027, the alphabetical list.
4. 0028, the 1741 excerpt.
5. 0029-0030, the numbered list of 53 with its heading and pairs.
6. (0031-0034, the prose — not built yet.)

The corpus has not been assembled: `transcriptions/` holds the six list
pages only, and the prose pages wait on a reading that can see the pages.
