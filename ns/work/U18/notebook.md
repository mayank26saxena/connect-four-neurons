# U18 notebook (layer 2, pole -, threshold 0.888, rate 3%)

## Exploration
- 40 examples + band 9 x4 seeds. Top examples are early-game (mean ply ~9.6 vs ~19 in low bands), sparse boards.
- Cell histograms (band 9 vs bands 1-3): my stones at (0,3),(1,3),(0,5) enriched; their stone at (0,1) enriched.
  Threshold bands (5-6) vs just-below (3-4) are almost indistinguishable cell-wise.
- Last move: col 2 enriched (32% band9 vs 20% baseline), last row 2 enriched (42% vs 24%).
- act minimal pairs: activation is graded/additive in many stones (e.g. base 3,1,5,4,3,X fires for 6 of 7 last moves);
  same final board with different move order differs (2,6,4,2 = 1.43 vs 2,2,4,6 = 0.92): last move matters.
  Their stone at (0,3) strongly negative (2,6,4,3 = -0.50). First move 3 gives -1.0.
- steer: max/zero changes move probs by <= 0.03. Effect essentially none.

## Hypotheses
H1: horizontal gap X_X at a landing cell -> rejected (2,0,4,6 = 0.38).
H2: last stone (theirs) placed on top of my stone -> partial (2,6,4,2 yes, 2,6,4,4 no).
H3: diffuse early-game feature: few stones, my stones low in center col 3, their last move in col 2 / row 2. Likely mixture / random direction.

## Scores
1. p1 (ply<=14, last move col 2, row>=1): F1 0.152 (P 0.129, R 0.184), AUROC 0.573, sim share 0.07.  <- best
2. p2 (hand additive cell score: my (0,3),(1,3),(0,5), their (0,1), cap in cols 2-4, -ply): F1 0.089, AUROC 0.562, sim 0.08.
3. p3 (ply 4-12, their (0,3) negative, my col-3 base, their (0,0)/(0,1), last col 2): F1 0.145, AUROC 0.599, sim 0.09.
4. p4 (their last stone capped my stone in cols 2-4, ply<=16): F1 0.096, AUROC 0.561, sim 0.08.
Aggregate board features (OoverX, pairs, centre counts, row0 counts) all just track ply; firing is early-game
(band 9 mostly ply 4-11) but most early positions don't fire. Activation is board-determined (move order mostly irrelevant,
3,1,5,4,3,3 / 3,1,3,4,5,3 / 5,1,3,4,3,3 all ~1.95) and graded/additive over many stones with mixed-sign contributions
(their stone at (0,3) strongly negative; their stones at (0,0)/(0,1) positive; capping effect positive in cols 3-4, negative in col 5).
No single rule. Stopped at 4 calls: further hand-tuned cell weights would be overfitting.

## Steer
3,1,5,4,3,3; 1,4,6,2,2; 1,4,1,1,6,2,2; 2,3,3,...,0,4; 3,4,3,3,5,1: max -> changes <= 0.01; zero -> <= 0.03. No measurable effect.

## Synthesis
best 3,4,3,3,5,1 = 2.153 (dev max 2.216), 1,4,1,1,6,2,2 = 2.149; 2-move extensions and single-stone swaps only lowered it.

## Conclusion: low confidence; looks like a diffuse early-game mixture (possibly a random direction).
