# Spread review

Proof images are in this folder; the red line is the proposed cut.
Edit the `verdict` column, then run:

    python scripts/split_spreads.py --apply-review processed/_spreads_review/INDEX.md

Only rows with verdict `split` are acted on. `skip` / `manual` / `split (done)` are ignored.

| crop | WxH | AR | fold_frac | confidence | content | origin | verdict |
|---|---|---|---|---|---|---|---|
| Oe 1_Bü 14525_0018_a.jpg | 3325x2506 | 1.33 | 0.502 | high | text both sides | review | split |
| Oe 1_Bü 14525_0028_a.jpg | 3313x2506 | 1.32 | 0.505 | high | text both sides | review | split |
| Oe 1_Bü 14525_0035_a.jpg | 3301x2506 | 1.32 | 0.541 | high | text both sides | review | split |
| Oe 1_Bü 14525_0056_a.jpg | 3289x2530 | 1.30 | 0.527 | high | text both sides | review | split |
| Oe 1_Bü 14525_0057_a.jpg | 3289x2518 | 1.31 | 0.529 | high | text both sides | review | split |
| Oe 1_Bü 14525_0058_a.jpg | 3302x2518 | 1.31 | 0.525 | high | text both sides | review | split |
| Oe 1_Bü 14525_0059_a.jpg | 3302x2530 | 1.31 | 0.525 | high | text both sides | review | split |
| Oe 1_Bü 14525_0060_a.jpg | 3302x2530 | 1.31 | 0.523 | high | text both sides | review | split |
| Oe 1_Bü 14525_0078_a.jpg | 3302x2494 | 1.32 | 0.541 | high | text both sides | review | split |
| Oe 1_Bü 14525_0116_a.jpg | 3314x2482 | 1.34 | 0.548 | high | text both sides | review | split |
| Oe 1_Bü 14525_0118_a.jpg | 3314x2506 | 1.32 | 0.477 | low | text both sides | review | manual |
| Oe 1_Bü 14525_0120_a.jpg | 3302x2494 | 1.32 | 0.545 | high | text both sides | review | split |
| Oe 1_Bü 14525_0126_a.jpg | 3314x2482 | 1.34 | 0.530 | high | text both sides | review | split |
| Oe 1_Bü 14525_0128_a.jpg | 3289x2482 | 1.33 | 0.530 | high | text both sides | review | split |
| Oe 1_Bü 14525_0130_a.jpg | 3289x2494 | 1.32 | 0.545 | high | text both sides | review | split |
| Oe 1_Bü 14525_0132_a.jpg | 3290x2494 | 1.32 | 0.532 | high | text both sides | review | split |
| Oe 1_Bü 14525_0134_a.jpg | 3278x2482 | 1.32 | 0.527 | high | text both sides | review | split |
| Oe 1_Bü 14525_0136_a.jpg | 3290x2494 | 1.32 | 0.534 | high | text both sides | review | split |
| Oe 1_Bü 14525_0138_a.jpg | 3290x2482 | 1.33 | 0.532 | high | text both sides | review | split |
| Oe 1_Bü 14525_0140_a.jpg | 3277x2470 | 1.33 | 0.537 | high | text both sides | review | split |
| Oe 1_Bü 14525_0142_a.jpg | 3302x2494 | 1.32 | 0.571 | high | text both sides | review | split |
| Oe 1_Bü 14525_0153_a.jpg | 3253x2494 | 1.30 | 0.548 | high | text both sides | review | split |
| Oe 1_Bü 14525_0154_a.jpg | 3253x2494 | 1.30 | 0.559 | high | text both sides | review | split |
| Oe 1_Bü 14525_0156_a.jpg | 3253x2470 | 1.32 | 0.532 | high | text both sides | review | split |
