# U25 notebook (layer 0, pole +, threshold 0.467, dev max 1.188)

## Observations
- Top band dominated by ply 5-7 openings with no stones in cols 3/4 (e.g. 1,6,5,2,0 = 0.994) and mid-game ply ~20-24 with column 3 full.
- Histograms by band: col 3 height is bimodal {0,6} in firing bands (band 8: 43 empty, 138 full, almost none 1-5). Col 4 height in {0,5,6}. Last move in col 4 is rare in firing.
- act trajectory on 0,3,5,6,2,3,3,3,5,2,5,5,2,2,0,3,2,3: activation rises as col 3 fills: last move to col3 row5 (filling it) = 0.904; prefix one move earlier (h3=5) = 0.319.
- Sweep 1,6,5,2,X: X=0 .99, 1 .86, 5 .81, 2 .53, 3 .52, 4 .42, 6 .20. Last col matters too (4 and 6 low here).
- 3,3,4,4,x: all strongly negative (center stones mid-height).

## Hypotheses
H1: fires when the centre columns hold no "partial" stacks: col 3 empty or full, col 4 empty or (nearly) full; last move not in col 4.
H2: early-game variant: no stones in cols 3-4 at all (ply<=8).
H3: last-move column/row specifics (layer-0 token effect) modulate.

## Tests and scores
- score 1 (p1, H1 centre cols empty/full, last!=4): F1 0.157 (P 0.089, R 0.684), AUROC 0.731, sim share 0.66. Far too broad (program fires 23.6%).
- Histogram: ply 8-16 almost never fires (bands 8-9), ply 4-7 and 18-26 enriched -> positional effect.
- score 2 (p2, early branch ply<=7 no centre stones >=3 cols; late branch col3 full, col4 empty/near-full, col5 <=4): F1 0.218 (P .138 R .528), sim .45.
- score 3 (p3, hand-set points: centre cols, ply, last col, col5 height, their stones in col3): F1 0.223, sim .31.
- score 4 (p4, simpler centre rule + ply exclusion): F1 0.173, sim .63.
- score 5 (p5, early branch + late col3 full with >=4 of their stones or last move into col3): F1 0.233 (P .170 R .371), AUROC .657, sim share 0.67. Best.
- Move-order transpositions that keep the same board leave activation unchanged unless the LAST move changes -> function of board + last move.
- 1,6,5,2,X sweep, single-substitution sweeps: every earlier stone shifts the value by 0.1-0.6, column-1/5/6 stones positive, column 3/4 stones negative in openings; but in midgame a FULL column 3 is positive. Non-monotone, diffuse.
- steer max/zero on 4 positions: all changes <= 0.01 probability. No measurable effect.
- Synthesis: 5,6,1,1,0 = 1.190, 1,6,5,1,1,6,0 = 1.189, 1,6,5,1,1 = 1.188 (beat/tie dev max 1.188).

## Conclusion
Diffuse layer-0 feature: openings (ply 4-7) with stones on the flanks (cols 1, 5, 6, 0) and none in the centre, or mid-games (ply ~17-26) where column 3 is full (mostly opponent stones). Never F1 > 0.25; looks like a mixture / possibly a random direction. Confidence low.
