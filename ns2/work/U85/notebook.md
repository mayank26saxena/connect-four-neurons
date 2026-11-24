# U85 notebook (layer 2, pole -, threshold 0.380, rate 3%)

## Observations
- Per-cell histograms of bands 8-9 vs 0-1: col 3 has exactly 3 stones (row 3 empty ~98% in band 9), col 2 has >=4 stones (100%),
  (3,2) is theirs ~78%. Not left/right symmetric: mirror (col 4) gives little.
- act: 3,3,3,2,2,2,2 fires 0.79; replacing last (3,2) stone by col 0 -> -0.8; col3 height 4 -> 0.04; col2 height 5 (my stone on top) -> -0.04.
- ownership of (2,3) not required (both X and O fire).
- Extra stones change level a lot (0.2 to 1.3) in ways not yet understood.

## Hypotheses
H1: heights[3]==3 and heights[2]>=4 and (3,2) theirs.
H2: heights[3]==3 and heights[2]>=4 (any owner).
H3: H1 but (3,2) theirs is key, col 2 height exactly 4.

## Score log
- s1 H1 (h3==3, h2>=4, (3,2) theirs): F1 0.273 (P .49 R .19), AUROC .59, sim share 0.09. Top-band pattern is crisp but covers <20% of firing.
- s2 landing(3) in {3,4} and left cell (L,2) theirs: F1 0.314, sim 0.10.
- s3 same but (L,2) any owner: F1 0.335 (P .29 R .39), sim 0.12.
- s4 hand-weighted cell points (h3==3 +3, (3,2) theirs +2, (2,2) filled, (1,3) mine, (0,3) theirs, (2,1)/(3,1)/(4,2)/(4,4) theirs), fire >=6: F1 0.391 (P .40 R .38), AUROC .68, sim 0.18. BEST.
- s5 added col1/col2 tall terms: F1 0.360 (recall up, precision down). s6 same, threshold 6.5: F1 0.385.
- Near-threshold firing (bands 5-6, ~2/3 of firing) is heterogeneous; no single board pattern found. Stopped at 6 calls.

## Steer
Effect negligible on 7 positions (max change ~3 points; e.g. 3,3,3,2,2,2,2: col3 -2, col5 +2).

## Synthesis
Greedy from dev pos 18863 (3.017): adding left-side stones raises it; right-side stones lower it; one extra move (perspective flip) kills it.
4,1,0,2,0,1,1,0,3,2,2,3,4,3,2,1,1,0,0 = 4.443 (beats dev max 3.646).
