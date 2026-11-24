# U88 notebook (layer 3, pole -, threshold 1.232, dev max 3.30, firing 3%)

## Observations (examples, 10 bands x 80)
- Firing skewed to early/mid game (ply 4-12 common), boards with low max height and no full columns,
  few of my threat cells. Teacher evals in top band are often negative for me (but not a board feature).
- Weak single-feature hint: col 3 = me at bottom, them on top, rest empty (18/80 in band 9 vs ~5/80 low bands).
- Activation alternates strongly ply to ply within a game; no consistent parity.
- steer to max / zero: changes move probabilities by <= 0.03 on 6 positions. Effect essentially none.

## Minimal pairs
- 4,5,2,X (vary their 2nd stone): 0.58,1.28,1.61,0.90,0.02,1.50,2.19 -> no clean cell rule.
- 3,a,1,b grid (49 openings): values -0.4..1.4 non-additive, no row/column structure.
- Col-3 hypothesis (me under them in col 3): swapping move order to put them under me sometimes lowers
  (3,3,6,5,1,2 2.17 vs 6,3,3,5,1,2 0.68) and sometimes raises (3,3,4,6 0.34 vs 4,3,3,6 1.96). Rejected.
- Transposition 3,3,6,5,1,2 (2.17) vs 3,2,6,5,1,3 (2.56): same board, different value -> order-sensitive.

## Hypotheses
H1: open early board (no full column, low max height, no my threats) -> coarse proxy.
H2: col-3 me-under-them pattern (rejected by minimal pairs).

## Dev metric
- p1 (ply<=14, no full column, no my threat cells; level by ply): F1 0.107 (P 0.059, R 0.600), AUROC 0.651, sim share 0.03.
- p2 (col 3 height 2 with them on top, or height 4 them/me alternating; no full col): F1 0.102, AUROC 0.552, sim -0.04.
- p3 (p1 board restriction AND col-3 hint): F1 0.095, AUROC 0.540, sim -0.09.
Stopped spending score calls: no hypothesis gave a real signal, and every minimal-pair family was non-additive and order-sensitive.

## Further single-feature histograms (by band)
last move column/row, |last - previous col|, threat counts, centre stone balance: none separate the bands beyond the
"emptier board" trend. Per-cell occupancy: high bands are emptier everywhere; the only relative excess is col 3 (them at (1,3)).

## Steer
6 positions (incl. 3 top firing): forcing to max or zero changes move probabilities by <= 0.03. No measurable effect.

## Synthesis
Hill-climbed from dev examples with act: best 5,5,2,2,3,4,2,3,4,4,1,0 = 3.197 (dev max 3.300, not beaten).

## Conclusion
No clean concept. Looks diffuse or like a random direction: mild preference for early, open boards. Confidence low.
