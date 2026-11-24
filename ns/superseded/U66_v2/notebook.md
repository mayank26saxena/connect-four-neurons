# U66 notebook (layer 2, pole -, thr 0.422, dev max 4.143)

## Examples (40 + 60/band for bands 2,5-9)
- Top band: opponent's last move very often in an edge column (col 6 most, then col 0), often stacking on their own stone
  (band 9: 46/60 last move in col 0/6; 37/60 on top of an O). Band 2 (non-firing): 16/60 edge.
- Top of column 4 being MY stone rises with band (0.35 in band 2 -> 0.75 band 9); top of col 6 being O 0.35 -> 0.75.
- Bands 5-6 (near threshold) are much more mixed (half non-edge last moves).
- steer on 6,4,4,0 (act 2.46): zero/max change <= 0.01 on every column -> no measurable effect.

## Hypotheses
H1: opponent just played in an edge column (0 or 6), especially stacking on own stone.
H2: additive: O-top in col 6/0 + X-top in col 4 + last move at edge.
H3: mixture / distributed direction (possibly random) -> low confidence.

## Minimal pairs (act)
- 4,4,c (ply 3): c=0 1.27, 2 0.44, 5 0.25, 6 0.21, 1 0.07, 3 0.02.
- 6,4,4,c: c=0 2.46, 6 1.24, 2 1.06, 5 0.80, 1 0.78, 3 0.39, 4 -0.41 (O on top of col 4 kills it).
- 4,4,4,0 0.05 vs 6,4,4,0 2.46 (X at bottom col 4 / O above kills it).
- 3,6,3,6 0.13 vs 4,6,3,6 0.56 vs 3,6,4,6 0.57 (X in col 4 helps).
- 3,0,3,0 0.00; 3,0,0,0 -0.10 (edge stacking alone not enough).
- single stones at ply 1: all < 0.14.

## Score calls (note: call 1 was spent twice by accident -> p1 shows as call 2)
- p1 (last move edge + stacks on own stone + top of col 4 mine): F1 0.111 (P 0.069 R 0.277) AUROC 0.578, sim share 0.06.
- p2 (adds col-6 O top, cols 1/5 empty): F1 0.130, AUROC 0.587, sim 0.06.
- More exploration: last-move cell is very concentrated at the top: (2,6) 26/60 in band 9, then (3,6),(0,0),(1,2),(5,3).
  Board cell tables (band 8-9 vs bands 0-3): O(1,6) 68% vs 22%, O(2,6) 58 vs 13, X(1,3)/X(1,4) ~47 vs 30, O(0,3)/(0,4) ~56 vs 38,
  X(0,2) 54 vs 35, O(1,2) 43 vs 27, (0,1) empty 57 vs 26.
- Synthetic template O3,X2,O2,X6,O6,X3,O4,X4,O6 -> 4.957 (beats dev max 4.143). Colour-swapped parity gives ~0
  (act along real games alternates fire / ~0 by ply), so it is a colour-relative board template.
- Minimal pairs on template: 3,3,4,4,0 2.54 (their two centre stones under mine), 3,3,4,4 (swapped colours) 0.36,
  3,3,4,4,3 0.27 / 3,3,4,4,4 -0.03 (they cover centre), 6,6,0,6 alone 0.30 (col-6 part alone is weak).
- p3 (centre X-on-O + col 6 + edge): F1 0.089, AUROC 0.561.
- p4 (positive-only cell template, ply penalty): F1 0.117, R 0.418, AUROC 0.615.
- p5 (signed template, mismatches negative): F1 0.109, AUROC 0.542.
- p6 (signed template, half-weight mismatches, edge/centre-cover/ply terms, graded fires): F1 0.145 (P 0.109 R 0.218),
  AUROC 0.707, sim share 0.05. BEST. Stopped at 7/8 calls.
- Many dev firings contradict the template (e.g. 2,1,4,3,0 bottom row OXOXO fires 0.53), so firing near threshold is diffuse.

## Steer
- 6,4,4,0 (2.46): max/zero change <= 0.01 everywhere.
- synth 3,2,2,6,6,3,4,4,6 (4.96): zero -> col 3 +0.05, col 4 -0.05; max ~0.
- dev top 57937 (3.14): no change (forced col 6 block).
=> no measurable effect on move.

## Conclusion
Distributed, colour-relative low-board template; no simple rule (best F1 0.145). Confidence LOW; could be a random direction.
