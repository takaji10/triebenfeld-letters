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

## Every fold checked by hand

Seven openings gave neither a shadow nor a clear gap and were left whole; they were then
placed by hand in `review_folds.py`, landing at 0.528 to 0.547, which is where the
shadow cluster sits and well right of the 0.434 to 0.470 the old fallback had guessed.

All 141 automatic decisions were then reviewed the same way. **43 were corrected, and
every one moved to the right**, by a median 23px and up to 207px. Twenty of the 43 had
been placed by the text-gap rule at almost exactly 0.500.

Final folds: 148 splits, median 0.5321, stdev 0.0115, range 0.496 to 0.559.

## What those 43 corrections taught the splitter

They are real ground truth, and scoring the rules against them showed the text-gap
midpoint was biased, not noisy: median error 67px, always left of the truth. The fold
sits right of the middle of the writing gap, because the left leaf's outer margin is
wider than the right leaf's inner one.

The fix is the unit's own evidence. A book photographed in one sitting puts its fold in
nearly the same place every time, so the median of the folds the shadow *did* find is
the best estimate for the openings where it found none:

| fallback | fires | median error | bias |
|---|---|---|---|
| gap midpoint | 11/43 | 67px | -67px |
| unit fold median | 11/43 | **31px** | **-6px** |
| shadow, for reference | 26/43 | 18px | -18px |

`split_spreads.py` now takes a first pass over the batch to find the unit's fold median
and uses that wherever no shadow appears. The writing gap survives only as a last resort
when a unit has too few shadows to form a prior, and is marked low confidence.

## Trimming

Sheets in this volume differ in size, so a split page usually carried a strip of the leaf
underneath along one edge, often with that leaf's own writing on it. Every page was
checked in `review_trim.py` and **261 of 342 were trimmed**, 128 on the left and 133 on
the right, removing a median 204px and up to 474px.

The untrimmed images are kept in `processed/_untrimmed/`, so `apply_trims.py --undo`
restores them and a second pass always cuts from the original rather than compounding.

## A gap that had to be repaired

While the trim tool was being built it turned out **52 of the 342 page images were
missing**, though the manifest still listed all 342. The pattern was one crop absent per
affected scan, and re-running the cropper on one recreated it, so they had existed and
were removed later, during the re-split work. The cause was not reproducible and the
evidence was gone.

The unit was rebuilt from the 172 raw scans, which were never touched, and all 148 fold
decisions were re-applied from the manifest. Everything checks: 342 images, 148 originals
kept, manifest and disk in exact agreement, 148/148 folds reproduced.

`split_spreads.py` now compares the manifest against the disk after every run and reports
either way, because a page that quietly disappears stays invisible until the
transcription comes up short.

## Next

Transcribe to `corpus.txt`, marking each document with `[LETTER N]` on its own line.
