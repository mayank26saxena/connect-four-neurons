# U01 lab notebook

Layer 3, pole +, threshold 0.805, dev max 5.531, firing rate 3%.

## Observations (examples, 40 + band 9 x16)
- Top examples are often early games (ply 5-12) but also late games.
- Bottom-row histograms by band (n=60/band): firing bands enrich X (me) at (0,0) (band 0: 22/60, band 7: 49/60),
  O at (0,1), X at (0,3), O at (0,4), O at (0,6) (band 9: 44/60).
- Column 0 contents: "X only" enriched in firing bands, but plenty of firing positions with column 0 empty.
- Steer: effect tiny (<= 0.03 prob) on first 4 positions tried.

## Hypotheses
H1: my stone at bottom of column 0 (corner) -- strong contributor (2,3,6,0,2 = 5.49 vs 2,3,6,1,2 = 0.90).
H2: opponent stone on the right edge (0,6)/(0,5) adds (2,0,6,3,2 = 5.43 vs 2,0,5,3,2 = 2.01).
H3: an additive "bottom-row pattern" unit: X at c0 and c3, O at c1/c2/c4/c6.

## Tests
- Scan of all 3-move openings in scan3.txt (act, unscored, to learn per-stone contributions).

## Scans (act only)
- All 3- and 4-move openings scanned with act (s4.txt). At 3 stones the top is "my stone at (0,0)" plus O at c6/c1/c2
  (2,0,6 = 2.10; 1,0,1 = 1.90; 6,0,2 = 1.77). Moving my corner stone anywhere else kills it.
- Strong side-to-move dependence: the same game alternates firing / ~0 ply by ply (e.g. game of pos 147369 fires on
  every odd ply from 11 on, near 0 on even plies). So it reads stones from "me vs them", not colours.
- Minimal pairs, 5-stone openings: 6,0,2,3,2 = 5.45; 6,0,2,2,2 (my stone on their c2 stone instead) = -0.26;
  3,0,6,3,2 = 0.53; O vertical pair in c1 or c2 fires (4.4, 5.4) but in c3/c4/c5 does not (-0.56, 0.77, -0.45);
  mirror images (0,6,4,5,4) do not fire: strongly left/right asymmetric.
- O on top of my stone at (2,4) (col 4 = ?,X,O) is the most enriched single cell in band 9 (58/80 vs 17/80 in band 0)
  but in neutral contexts (3,4,3,4,1,1,4 = 0.02; 3,0,4,4,4 = 0.09) it does nothing; O at (0,3) strongly suppresses.
- Corners alone do not sustain firing: after 6,0 the unit fades as the centre fills (games tried peak ~1.4 then ~0).

## Score calls
1. p1 "their threat cell directly above a landing cell" (from two late-game examples): F1 0.050, AUROC 0.48. Wrong;
   that pattern holds on 37% of positions. Dropped.
2. p2 additive cell-weight pattern (about 20 (cell, owner) weights picked from single-cell band histograms + minimal
   pairs; fire if points >= 8): F1 0.227 (P 0.151, R 0.460), AUROC 0.690, sim share 0.05. Best.
3. p3 "my stone at (0,0) and theirs at (0,6)": F1 0.092, AUROC 0.566, recall 0.29. Too narrow.
4. p4 p2 + gate (my corner stone, or their stone at (2,4) on mine) + stronger (0,3) penalty: F1 0.220, AUROC 0.605.
Stopped there: no single board pattern found, the cell-wise model saturates around AUROC 0.69, and contributions
interact strongly (O at c1+c1 1.9 but c1+c2 0.04 at 3 stones). Looks like a distributed mixture / possibly a random direction.

## Steer
Max on 5 positions and zero on 3: every column changes by <= 0.04 probability. Effect: none measurable.

## Synthesis
Local search with act around 2,3,6,0,2: 2,3,6,0,2,3,5 = 7.03 (beats dev max 5.53), 6,0,2,3,2,3,5 (same board, other
order) = 6.90, 2,3,6,0,2,3,0 = 5.55.

## Conclusion
Confidence low. Best F1 0.227 (p2).
