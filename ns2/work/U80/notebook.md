# U80 notebook (layer 1, pole -, threshold 0.312, dev max 3.578)

## Examples
- Top bands: last move (opponent's) is overwhelmingly in col 1 (row 2-4) or col 6 (row 1-3); col 2 and col 0 usually empty/low;
  col 4 tall; opponent stones concentrated in cols 1, 4, 5, 6; my stones at (0,0), (1,3) common.
- Single-feature histograms (per-column counts, per-cell occupancy, last-move cell) show many weak, graded shifts, no single crisp cell.

## Hypotheses
H1 last move in col 1/6 high + col 2 empty + col 0 low (positional, distributed).
H2 opponent anti-diagonal (0,6)-(1,5)-(2,4) / their threat at (3,3): act test negative (diagonal alone ~0).
H3 linear in per-column stone counts by owner (attention-average style).

## Minimal pairs (act)
- Board-determined: 4 move orders of the same 9-stone board give 1.41-1.48.
- Base 1,3,1,4,5,3,5,1 + any 9th move fires (0.33-1.98); last move col 1 best, col 2 worst.
- Removing opponent col-5 pair: 0.93 -> -0.05. Removing my col-3 pair: 0.93 -> 0.30.
- Opponent stones added in col 6 / col 1 raise it; opponent stone in col 2 lowers; my stone at (0,0) raises, my stone in col 3 lowers.
- Opponent vertical three in col 6 or col 1 on near-empty board: ~0 (not sufficient).
- Many interacting additive cell effects -> diffuse.

## Scores
1. p1 additive score (last col 1/6, h2 empty, h0<=1, h1 3-5, h4>=5, their col6/col5 low stones, my (0,0),(1,3)): F1 0.241, P 0.19 R 0.32, AUROC 0.64, sim share 0.10.
2. p2 per-cell weights threshold 9: F1 0.075 (threshold too high).
3. p3 per-column count linear: F1 0.207, AUROC 0.66, sim 0.07.
4. p4 simple last-move-cell + col2/col0 low: F1 0.186, sim 0.05.
5. p5 = p1 + their row-3 threat + parity: F1 0.214, sim 0.08.
Best: p1 (0.241). No measurable steering effect (max/zero changes <= 0.01 on 4 positions).

## Conclusion
Diffuse positional unit, possibly a random direction. Confidence low.
