# U71 notebook (layer 3, pole -; threshold 0.669, dev max 14.64)

## Observations (bands 5-9, ~60 examples)
- Band 9: all have the opponent (O) with 3 stacked stones on top of column 3, cell above empty (must-block at col 3).
- Bands 7-8: often 2 O stacked at top of col 3; sometimes the top-of-column run in col 2/4/1.
- Band 5: noisy; single O on top of col 3, or O runs in other columns.

## Hypotheses
- H1: fires when the top of column 3 is a run of >=2 opponent stones (strength grows with run length: 3 >> 2).
- H2: same as H1 but any column, weighted toward center (col 3 strongest, 2/4 weaker).
- H3: it is just "must-block in a vertical three" (any column).

## Tests (act)
- O,O,O at rows 0-2 of col 3 (threat) only 0.13; X,O,O,O rows1-3 1.65; X,X,O,O,O rows 2-4 5.3-6.1. Height matters.
- Same stacks in col 2: ~0.4-0.7; col 4/1/5: ~0. Very column-3 specific.
- Full col 3 (X,X,X,O,O,O) -0.19; but blocked X,X,O,O,O,X with O to move elsewhere still 1.2.
- Two-stack X,X,O,O (rows 2-3): ~1.0-1.2; X,X,X,O,O (rows 3-4) -0.3; X,O,O rows1-2 ~0.07. Context-dependent.
- Perspective: after my move (stack now 'mine') drops to ~0. Opponent stack only.
- When I have my own immediate win, it drops (6.0 -> 1.5).
## Scores
- p1 (top run of O in col3, 3-run lo>=1 ->9, 2-run covering row2 ->5): F1 0.383, sim share 0.88
- p2 (+ 2-run only if rows 2-3, 3-run at bottom ->4, blocked 3-run under my stone ->4): F1 0.462, P .40 R .55, sim 0.91
- p3 (p2 + cap level when I have an immediate win): F1 0.461, sim 0.72 -> reverted.
- p4 (any O-run of >=3 in col 3 incl. capped by my stone ->5): F1 0.347 (precision .25), sim 0.92. Capped runs mostly do not fire.
- p5 (capped runs -> non-firing 3): F1 0.416, sim 0.90; lost p2's full-column case (O three at rows 2-4 under my stone at row 5).
- p6 (p5 + capped three covering rows 2-4 -> 6): F1 0.462, P .40 R .55, AUROC .76, sim 0.92. FINAL.
- Near-threshold firing (band 5-6) is diffuse: single/double O stones at top of col 3, col 2/4 stacks; two-stacks context dependent.
## Steer
- In must-block positions col 3 already ~1.00, no change. In 3,0,3,3,6,3 (two-stack) max: col3 +16, col4 -18. In 0,3,1,3,6,2: col3 +20, col4 -21. Zero: no change.
## Synthesis
- Extending dev-max pos 7029 with filler pairs: best 15.57 (beats 14.64).
