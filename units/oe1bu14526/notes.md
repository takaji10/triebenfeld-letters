# Oe 1 Bü 14526

Cropped and split; not yet transcribed.

## Provenance

Hohenloher Zentralarchiv Neuenstein. 172 archival scans, 675 MB, about 3400x2750 each.
Unlike Oe 1 Bü 9454, this is a bound volume photographed open: almost every scan is one
opening, two written leaves either side of the fold.

## Intake

```
172  raw scans
194  crops from crop_scans.py     (46 single leaves, 148 openings)
335  page images after splitting  (141 openings split, 7 held back)
```

The 141 originals are kept in `processed/_spreads_unsplit/`. Nothing was overwritten.

## The fold in this unit

`split_spreads.py` was written for Oe 1 Bü 9454, where the fold is a low-ink gap and the
cut goes in the widest band of bare paper. That is the wrong rule here. The book is
photographed open, the gutter is a dark shadow, and the clearest band of paper is a page
margin instead. On the first pass it put 109 of 148 cuts in the wrong place, by a median
6% of the width, and on scan 0055 it cut straight through the left page's writing.

Two strategies now run ahead of the old one:

- **The fold shadow**, the column with the longest unbroken dark run. Writing cannot
  imitate it: pen strokes are short and scattered, a shadow runs a third of the height or
  more without a break.
- **The text gap**, the space between the innermost written columns on either side of
  centre. Clear paper by construction, whatever the lighting did to the gutter.

Cuts went from a bimodal 0.427 to 0.579 of the width, to 0.49 to 0.56 about a median of
0.530. High-confidence detections went from 24 to 141.

Each half also keeps 0.8% of the width past the fold. In a bound volume the writing runs
into the gutter, so a cut exactly on the fold clips the last stroke of some lines; the
overlap costs a sliver of the facing page and loses no ink. Checked on scan 0033, where
several lines on the left page reach the fold and now survive whole.

## Held back

Seven openings found neither a shadow nor a clear gap, so they were left whole rather
than cut on a guess:

```
0055  0083  0124  0126  0155  0162  0170
```

Their proofs are in `processed/_spreads_review/`. To finish one, set its verdict to
`split` in `INDEX.md`, correct `fold_frac` by eye, and run `--apply-review`. 0055 and
0124 have writing close to the fold and are worth doing carefully.

## Next

Transcribe to `corpus.txt`, marking each document with `[LETTER N]` on its own line.
