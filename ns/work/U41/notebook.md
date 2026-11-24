# U41 notebook (layer 0, pole +, threshold 1.224, dev rate 2.9%, dev max 4.664)

## Examples (40 + 45 extra in bands 4/5)
- Every firing example in bands 5-9 is the EMPTY board (act 4.664 = dev max, constant).
- Band 4 (just below threshold): single-stone openings: [4] 1.224 (exactly threshold), [3] 1.064, [5] 0.846, [6] 0.798, [5,1] 1.019, [1,4,3] 0.817.
- Dev firing rate 2.9% ~ 1 empty-board position per ~35-ply game.

## Hypotheses
H1: fires iff board is empty (ply 0, first player to move). Strongly supported.
H2: graded "early game" signal: decays with ply (ply1 ~0.8-1.2, later <0.7). Matters only for level().
H3 (borderline): [4] opening sits exactly at threshold; act shows "FIRES" at 1.224, examples does not. Float tie.

## act tests
- 4,4,3,3,2: 4.664 FIRES, 1.224 (borderline), 0.351, 0.696, 0.351, 0.195
- 0,1,2,6,5: 4.664 FIRES, 0.784, 0.707, 0.155, 0.455, 0.277
Consistent with H1; activation drops sharply after the first stone.

## Dev metric
- score 1 (p1: fires=ply==0; level 9/2/1/0 by ply): F1 1.000, P 1.000, R 1.000, AUROC 1.000; sim 13.3% vs ceiling 62.5% -> share 0.21
- score 2 (p2: binary level): F1 1.000; sim share 0.11 -> graded decay helps simulation
- act: ply-1 activation by opening column: 0:.78 1:1.18 2:-.08 3:1.06 4:1.224 (threshold tie) 5:.85 6:.80; decays to ~0.2-0.4 by ply 3, ~0 or negative by ply 5-6.
- score 3 (p3: col-2 opening -> 0, ply2-4 -> 1): F1 1.000; sim share 0.22 (marginal). Stopped tuning.

## Steer
- empty board, zero: no change (max 0.00). [4] max: <=0.01. [3,3,2,4] max: +0.02 col 3 / -0.02 col 4. [0,6,1] max: ~0.01. Effect negligible.

## Synthesis
- empty board = 4.664 = dev max (tool says beats/equals). Nothing else came close (best ply-1 is 1.224).

Conclusion: a layer-0 "start of game / empty board" detector (likely a position-0 / no-token feature). High confidence.
