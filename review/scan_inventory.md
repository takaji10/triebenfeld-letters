# Scan inventory

`pages/` holds **872 images** across **545 captures** (0001–0546), against **869 transcribed pages**.

Each image is one manuscript page. Blank pages were deleted before this ran, so gaps in the filename sequence are deliberate and are recorded below as pruning, not as damage.


## What each capture yielded

| Composition | Captures | Meaning |
|---|---|---|
| `a1` + `a2` | 232 | spread split into two pages, both kept |
| `a` + `b` | 93 | two documents in the capture, both kept |
| `b` | 84 | the _a crop was blank and removed |
| `a` | 73 | single document, not a spread |
| `a1` | 38 | the right half was blank and removed |
| `a2` | 23 | the left half was blank and removed |
| `a` + `b2` | 1 | horizontal split; _b1 removed |
| `a1` + `b` | 1 |  |

## Pruned counterparts

Expected, not errors — these are the blanks you removed. Listed so the record exists and nothing here is later mistaken for a missing scan.


**first document in the capture removed** — 84

> `0006_a`, `0008_a`, `0012_a`, `0015_a`, `0018_a`, `0020_a`, `0024_a`, `0034_a`, `0043_a`, `0047_a`, `0049_a`, `0053_a`, `0055_a`, `0059_a`, `0061_a`, `0063_a`, `0065_a`, `0071_a`, `0072_a`, `0073_a`, `0075_a`, `0081_a`, `0083_a`, `0085_a`, `0087_a`, `0089_a`, `0095_a`, `0097_a`, `0099_a`, `0100_a`, `0102_a`, `0104_a`, `0108_a`, `0112_a`, `0159_a`, `0161_a`, `0206_a`, `0278_a`, `0287_a`, `0299_a`, `0307_a`, `0323_a`, `0327_a`, `0346_a`, `0354_a`, `0358_a`, `0361_a`, `0367_a`, `0369_a`, `0374_a`, `0376_a`, `0378_a`, `0387_a`, `0389_a`, `0390_a`, `0392_a`, `0395_a`, `0407_a`, `0416_a`, `0431_a` … and 24 more

**left half of a spread removed** — 24

> `0021_b1`, `0035_a1`, `0041_a1`, `0121_a1`, `0123_a1`, `0147_a1`, `0148_a1`, `0157_a1`, `0238_a1`, `0244_a1`, `0245_a1`, `0298_a1`, `0332_a1`, `0334_a1`, `0341_a1`, `0342_a1`, `0345_a1`, `0382_a1`, `0423_a1`, `0467_a1`, `0468_a1`, `0469_a1`, `0484_a1`, `0518_a1`

**right half of a spread removed** — 39

> `0005_a2`, `0009_a2`, `0013_a2`, `0017_a2`, `0025_a2`, `0037_a2`, `0044_a2`, `0048_a2`, `0052_a2`, `0062_a2`, `0070_a2`, `0074_a2`, `0082_a2`, `0084_a2`, `0088_a2`, `0094_a2`, `0096_a2`, `0098_a2`, `0101_a2`, `0122_a2`, `0135_a2`, `0139_a2`, `0170_a2`, `0172_a2`, `0178_a2`, `0184_a2`, `0191_a2`, `0196_a2`, `0224_a2`, `0271_a2`, `0344_a2`, `0352_a2`, `0383_a2`, `0415_a2`, `0430_a2`, `0451_a2`, `0494_a2`, `0511_a2`, `0539_a2`


## Short blocks that are almost certainly not page breaks

**0 of them**, against a shortfall of -3 pages — so this very likely accounts for the whole discrepancy.

These are datelines, signatures and salutations that the transcriber set off with a blank line. Phase 1 read every blank line as a page break, which turned each of these into its own "page". They are the first thing to check in the reviewer: **merge into previous page** is almost always the right call, and the real fix is to remove the blank line from the corpus.

| Letter | Page | Lines | Looks like | Blank line at | Content |
|---|---|---|---|---|---|


## Where the transcript claims more pages than there are images

The likeliest cause is over-segmentation: our page breaks come from blank lines in the transcript, and some of those are probably paragraph breaks rather than page breaks. Each row lists the blank-line positions inside the letter so a suspect break can be checked against the text directly. **Fixing one means editing the corpus** (removing a blank line), not the mapping.


9 letters affected, 9 pages in total.

| Letter | Transcript pages | Images | Excess | Blank lines inside the letter |
|---|---|---|---|---|
| 122 | 1 | 0 | +1 | — |
| 147 | 3 | 2 | +1 | 10663, 10683 |
| 188 | 3 | 2 | +1 | 13359, 13380 |
| 203 | 3 | 2 | +1 | 14485, 14523 |
| 230 | 5 | 4 | +1 | 16764, 16791, 16821, 16850 |
| 232 | 4 | 3 | +1 | 16899, 16923, 16948 |
| 244 | 3 | 2 | +1 | 17625, 17653 |
| 253 | 2 | 1 | +1 | 18124 |
| 301 | 2 | 1 | +1 | 21407 |
