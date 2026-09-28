# Spread review

Proof images are in this folder; the red line is the proposed cut.
Edit the `verdict` column, then run:

    python scripts/split_spreads.py --apply-review processed/_spreads_review/INDEX.md

Only rows with verdict `split` are acted on. `skip` / `manual` / `split (done)` are ignored.

| crop | WxH | AR | fold_frac | confidence | content | origin | verdict |
|---|---|---|---|---|---|---|---|
| Oe 1_Bü 9454_0003_a.jpg | 2735x1670 | 1.64 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0007_a.jpg | 2921x1816 | 1.61 | 0.523 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0009_a.jpg | 2684x1639 | 1.64 | 0.445 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0013_a.jpg | 2673x1613 | 1.66 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0019_a.jpg | 2889x1752 | 1.65 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0025_a.jpg | 2961x1762 | 1.68 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0029_a.jpg | 2670x1614 | 1.65 | 0.516 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0031_a.jpg | 2675x1620 | 1.65 | 0.445 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0033_a.jpg | 2817x1637 | 1.72 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0036_a.jpg | 2691x1654 | 1.63 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0039_a.jpg | 2645x1626 | 1.63 | 0.529 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0041_a.jpg | 2895x2456 | 1.18 | 0.495 | high | text both sides | review | split |
| Oe 1_Bü 9454_0042_a.jpg | 2895x2466 | 1.17 | 0.500 | high | text both sides | review | split |
| Oe 1_Bü 9454_0044_a.jpg | 2626x1642 | 1.60 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0046_a.jpg | 2662x1599 | 1.66 | 0.539 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0048_a.jpg | 2523x1869 | 1.35 | 0.496 | high | text both sides | review | split |
| Oe 1_Bü 9454_0050_a.jpg | 2456x1758 | 1.40 | 0.496 | high | text both sides | review | split |
| Oe 1_Bü 9454_0052_a.jpg | 2672x1596 | 1.67 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0054_a.jpg | 2788x1708 | 1.63 | 0.520 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0056_a.jpg | 2631x1605 | 1.64 | 0.536 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0058_a.jpg | 3234x2493 | 1.30 | 0.512 | high | text both sides | review | split |
| Oe 1_Bü 9454_0060_a.jpg | 2607x1611 | 1.62 | 0.546 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0062_a.jpg | 2618x1610 | 1.63 | 0.541 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0064_a.jpg | 2618x1610 | 1.63 | 0.536 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0066_a.jpg | 2815x2448 | 1.15 | 0.545 | low | text both sides | review | split |
| Oe 1_Bü 9454_0068_a.jpg | 3202x2518 | 1.27 | 0.496 | high | text both sides | review | split |
| Oe 1_Bü 9454_0070_a.jpg | 2612x1615 | 1.62 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0074_a.jpg | 2636x1648 | 1.60 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0076_a.jpg | 2607x1636 | 1.59 | 0.530 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0080_a.jpg | 2647x1624 | 1.63 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0082_a.jpg | 2629x1603 | 1.64 | 0.543 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0084_a.jpg | 2657x1633 | 1.63 | 0.543 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0086_a.jpg | 2819x1642 | 1.72 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0090_a.jpg | 2649x1648 | 1.61 | 0.523 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0096_a.jpg | 2873x2446 | 1.17 | 0.502 | high | text both sides | review | split |
| Oe 1_Bü 9454_0101_a.jpg | 2620x1638 | 1.60 | 0.546 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0113_a.jpg | 2661x1639 | 1.62 | 0.529 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0115_a.jpg | 2693x1612 | 1.67 | 0.534 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0119_a.jpg | 2638x1611 | 1.64 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0121_a.jpg | 2513x1792 | 1.40 | 0.498 | high | text both sides | review | split |
| Oe 1_Bü 9454_0122_a.jpg | 2531x1791 | 1.41 | 0.505 | low | text both sides | review | split |
| Oe 1_Bü 9454_0126_a.jpg | 2690x1650 | 1.63 | 0.532 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0128_a.jpg | 2647x1637 | 1.62 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0131_a.jpg | 2619x1607 | 1.63 | 0.529 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0133_a.jpg | 2661x1620 | 1.64 | 0.523 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0135_a.jpg | 2718x1623 | 1.67 | 0.530 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0137_a.jpg | 2656x1624 | 1.64 | 0.516 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0141_a.jpg | 3194x2488 | 1.28 | 0.498 | high | text both sides | review | split |
| Oe 1_Bü 9454_0143_a.jpg | 2589x1570 | 1.65 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0153_a.jpg | 3253x2468 | 1.32 | 0.536 | low | text both sides | review | split |
| Oe 1_Bü 9454_0156_a.jpg | 2973x2407 | 1.24 | 0.495 | high | text both sides | review | split |
| Oe 1_Bü 9454_0157_a.jpg | 2973x2397 | 1.24 | 0.498 | high | text both sides | review | split |
| Oe 1_Bü 9454_0160_a.jpg | 2610x1605 | 1.63 | 0.546 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0163_a.jpg | 2741x1642 | 1.67 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0165_a.jpg | 2663x1631 | 1.63 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0167_a.jpg | 2664x1610 | 1.65 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0170_a.jpg | 2647x1628 | 1.63 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0178_a.jpg | 2654x1632 | 1.63 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0180_a.jpg | 2697x1623 | 1.66 | 0.539 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0182_a.jpg | 2656x1614 | 1.65 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0184_a.jpg | 2682x1621 | 1.65 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0186_a.jpg | 2652x1621 | 1.64 | 0.541 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0191_a.jpg | 2628x1634 | 1.61 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0194_a.jpg | 2664x1638 | 1.63 | 0.541 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0196_a.jpg | 2627x1667 | 1.58 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0198_a.jpg | 2654x1632 | 1.63 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0200_a.jpg | 2651x1620 | 1.64 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0203_a.jpg | 2660x1626 | 1.64 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0205_a.jpg | 2653x1635 | 1.62 | 0.543 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0208_a.jpg | 2703x1729 | 1.56 | 0.532 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0209_a.jpg | 2693x1720 | 1.57 | 0.543 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0216_a.jpg | 2689x1609 | 1.67 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0218_a.jpg | 2667x1645 | 1.62 | 0.546 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0220_a.jpg | 2688x1643 | 1.64 | 0.529 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0222_a.jpg | 2677x1643 | 1.63 | 0.532 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0224_a.jpg | 2664x1619 | 1.65 | 0.543 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0233_a.jpg | 2643x1603 | 1.65 | 0.539 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0235_a.jpg | 2585x1587 | 1.63 | 0.530 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0244_a.jpg | 2678x1637 | 1.64 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0245_a.jpg | 2662x1639 | 1.62 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0247_a.jpg | 2666x1611 | 1.65 | 0.527 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0252_a.jpg | 2713x1633 | 1.66 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0254_a.jpg | 2713x1671 | 1.62 | 0.550 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0263_a.jpg | 2669x1637 | 1.63 | 0.527 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0265_a.jpg | 2669x1627 | 1.64 | 0.527 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0271_a.jpg | 2600x1627 | 1.60 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0273_a.jpg | 2681x1605 | 1.67 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0275_a.jpg | 2671x1627 | 1.64 | 0.489 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0277_a.jpg | 2671x1618 | 1.65 | 0.523 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0289_a.jpg | 2683x1587 | 1.69 | 0.534 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0301_a.jpg | 2664x1676 | 1.59 | 0.539 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0306_a.jpg | 2621x1599 | 1.64 | 0.534 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0310_a.jpg | 2689x1590 | 1.69 | 0.541 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0315_a.jpg | 2620x1833 | 1.43 | 0.484 | high | text both sides | review | split |
| Oe 1_Bü 9454_0318_a.jpg | 2671x1590 | 1.68 | 0.529 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0324_a.jpg | 2666x1592 | 1.67 | 0.536 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0326_a.jpg | 2660x1589 | 1.67 | 0.536 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0329_a.jpg | 2685x1674 | 1.60 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0333_a.jpg | 2675x1697 | 1.58 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0344_a.jpg | 2653x1683 | 1.58 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0352_a.jpg | 1334x946 | 1.41 | 0.498 | low | text both sides | review | split |
| Oe 1_Bü 9454_0353_a.jpg | 2547x1563 | 1.63 | 0.537 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0355_a.jpg | 2587x1569 | 1.65 | 0.536 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0357_a.jpg | 2601x1577 | 1.65 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0360_a.jpg | 2605x1625 | 1.60 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0362_a.jpg | 2607x1618 | 1.61 | 0.527 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0364_a.jpg | 2593x1591 | 1.63 | 0.520 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0368_a.jpg | 2697x1586 | 1.70 | 0.516 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0373_a.jpg | 2701x1622 | 1.67 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0375_a.jpg | 2693x1618 | 1.66 | 0.498 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0377_a.jpg | 2484x1736 | 1.43 | 0.518 | low | text both sides | review | split |
| Oe 1_Bü 9454_0382_a.jpg | 2705x1780 | 1.52 | 0.445 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0383_a.jpg | 2703x1808 | 1.50 | 0.498 | low | text both sides | review | split |
| Oe 1_Bü 9454_0386_a.jpg | 2661x1667 | 1.60 | 0.529 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0393_a.jpg | 2703x1685 | 1.60 | 0.527 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0396_a.jpg | 2654x1661 | 1.60 | 0.523 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0402_a.jpg | 2875x2395 | 1.20 | 0.550 | low | text both sides | review | split |
| Oe 1_Bü 9454_0403_a.jpg | 2885x2406 | 1.20 | 0.541 | low | text both sides | review | split |
| Oe 1_Bü 9454_0404_a.jpg | 2885x2406 | 1.20 | 0.498 | high | text both sides | review | split |
| Oe 1_Bü 9454_0406_a.jpg | 2711x1651 | 1.64 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0415_a.jpg | 2769x2281 | 1.21 | 0.502 | high | text both sides | review | split |
| Oe 1_Bü 9454_0419_a.jpg | 3350x2602 | 1.29 | 0.534 | low | text both sides | review | split |
| Oe 1_Bü 9454_0420_a.jpg | 3364x2602 | 1.29 | 0.536 | low | text both sides | review | split |
| Oe 1_Bü 9454_0421_a.jpg | 3360x2613 | 1.29 | 0.527 | low | text both sides | review | split |
| Oe 1_Bü 9454_0423_a.jpg | 3407x2635 | 1.29 | 0.443 | low | text both sides | review | split |
| Oe 1_Bü 9454_0424_a.jpg | 3334x2556 | 1.30 | 0.502 | high | text both sides | review | split |
| Oe 1_Bü 9454_0426_a.jpg | 2721x1666 | 1.63 | 0.523 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0428_a.jpg | 2710x1618 | 1.67 | 0.521 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0432_a.jpg | 3020x2502 | 1.21 | 0.509 | low | text both sides | review | split |
| Oe 1_Bü 9454_0433_a.jpg | 3343x2514 | 1.33 | 0.550 | low | text both sides | review | split |
| Oe 1_Bü 9454_0434_a.jpg | 3303x2527 | 1.31 | 0.554 | low | text both sides | review | split |
| Oe 1_Bü 9454_0436_a.jpg | 1616x1342 | 1.20 | 0.498 | low | text both sides | review | split |
| Oe 1_Bü 9454_0437_a.jpg | 2699x1650 | 1.64 | 0.514 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0439_a.jpg | 2718x1652 | 1.65 | 0.525 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0441_a.jpg | 2673x1629 | 1.64 | 0.477 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0446_a.jpg | 2755x1704 | 1.62 | 0.512 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0448_a.jpg | 2684x1697 | 1.58 | 0.545 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0450_a.jpg | 2722x1741 | 1.56 | 0.539 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0451_a.jpg | 2761x1726 | 1.60 | 0.548 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0457_a.jpg | 2788x1641 | 1.70 | 0.546 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0458_a.jpg | 2748x1617 | 1.70 | 0.534 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0460_a.jpg | 2574x1710 | 1.51 | 0.543 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0466_a.jpg | 2691x1683 | 1.60 | 0.552 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0467_a.jpg | 2691x1702 | 1.58 | 0.550 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0469_a.jpg | 2686x1670 | 1.61 | 0.445 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0471_a.jpg | 2848x2395 | 1.19 | 0.473 | high | one side sparse | review | split |
| Oe 1_Bü 9454_0484_a.jpg | 2863x2400 | 1.19 | 0.484 | low | text both sides | review | split |
| Oe 1_Bü 9454_0492_a.jpg | 2657x1584 | 1.68 | 0.541 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0496_a.jpg | 2424x1641 | 1.48 | 0.498 | high | text both sides | review | split |
| Oe 1_Bü 9454_0498_a.jpg | 2744x1660 | 1.65 | 0.521 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0500_a.jpg | 2734x1634 | 1.67 | 0.521 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0505_a.jpg | 2432x1648 | 1.48 | 0.500 | high | text both sides | review | split |
| Oe 1_Bü 9454_0512_a.jpg | 1827x1471 | 1.24 | 0.564 | low | text both sides | review | split |
| Oe 1_Bü 9454_0520_a.jpg | 2824x1801 | 1.57 | 0.530 | low | text both sides | auto | split (done) |
| Oe 1_Bü 9454_0522_a.jpg | 3124x2566 | 1.22 | 0.541 | low | one side sparse | review | split |
| Oe 1_Bü 9454_0523_a.jpg | 2976x2571 | 1.16 | 0.486 | low | one side sparse | review | split |
| Oe 1_Bü 9454_0524_a.jpg | 2682x1807 | 1.48 | 0.514 | high | text both sides | review | split |
| Oe 1_Bü 9454_0525_a.jpg | 2671x1820 | 1.47 | 0.477 | high | text both sides | review | split |
| Oe 1_Bü 9454_0526_a.jpg | 2554x1790 | 1.43 | 0.502 | high | text both sides | review | split |
| Oe 1_Bü 9454_0535_a.jpg | 2828x2231 | 1.27 | 0.559 | low | one side sparse | review | split |
| Oe 1_Bü 9454_0536_a.jpg | 2756x2265 | 1.22 | 0.500 | high | text both sides | review | split |
| Oe 1_Bü 9454_0539_a.jpg | 2648x1651 | 1.60 | 0.454 | low | text both sides | auto | split (done) |
