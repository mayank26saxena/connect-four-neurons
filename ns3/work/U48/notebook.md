# U48 notebook (layer 1, pole -, thr 0.569, dev max 1.578)

## Observations
- Steer: forcing max changes move probs by <0.01 -> effect none measurable.
- Activation oscillates strongly move to move (layer 1: driven by last move cell + column contents).
- Top bands: last move col 4 landing on row 5 (filling col 4) or row 0 (opening an empty col 4 late game);
  early games with col 0 stacked (3+ stones) and last move in col 0/2/4; last move at (2,0).
- act: 0,0,0,0,2 = 1.554; 0,0,0,0,0,2 = 1.593 (beats dev max). Stacking col 0 raises, stacking col 3 lowers.
  6,6,6,6,0 = 0.04 (last into empty col 0 with col 6 stacked: low).

## Hypotheses
H1: last move col 4 into the top or bottom row.
H2: column 0 tall (>=3) in an early game.
H3: last move into (2,0).

## score 1 (p1: last (4,5)/(4,0)/(2,0) or early col0>=3 & last in 0/2/4): F1 0.275 P 0.20 R 0.44 AUROC 0.69, sim 0.04
- Transposition test: same board, different move order -> same activation (+-0.02). Board-state function.
- Same board, different last move: 0.37-0.87 -> last-move cell matters plus board context.
- Weighted single-feature histogram of last cell (bands): (4,5) est. 37% fire, 21% of firing; (2,0) 20%/11%; (4,0) 19%/10%; (0,0) 8%/6%.
- Bottom-row minimal pairs (last (4,0)): 1,0,3,4=1.06, 1,3,0,4=0.55, 0,1,6,4=-0.42: my stone on (0,3) next to their new stone helps. Context effects big and not clean.

## score 2 (p2: weighted last-cell level): F1 0.268 P 0.195 R 0.43, sim 0.08. No gain.
## Bottom-row minimal pairs at ply 4 (me = mover): my stones on cols 1 and 3 + their last on 4 (or 2) = 1.06; mine at 5/6 strongly negative; roughly additive in early game.
## score 3 (p3: additive bottom-row weights + last cell + col0): F1 0.084, fires on 37% (bottom row is full late -> weights are not global). Abandoned.
- Ply histogram: firing rate 8% at ply 4-7 (31% of firing), ~1.5% midgame, 4-6% at ply 32-39.

## score 4 (p4: last-cell rules gated by ply): F1 0.260 P 0.245 R 0.276
## Early-game additive map (act, ply 4): my bottom stones on cols 1/3 (+0.5 each), 2/4 (+0.3), 6 (-0.4);
   their bottom stones on 2/4 (+0.2..0.3), 5 (-0.35); col-0 stack height adds about +0.3 per stone.
## score 5 (p5: early additive bottom-row + col0 height for ply<=9; late: last move (4,5) or (4,0) at ply>=28):
   F1 0.317 P 0.289 R 0.351 AUROC 0.66, sim share 0.03  <- best
## score 6 (p6: widen windows to ply<=11 / >=24): F1 0.290. Worse; keep p5.
## Steer (3 positions, max and zero): move-probability changes <= 0.01. Effect: none measurable.
## Synthesis: 0,0,0,0,1,0,3,2 = 1.667; 1,0,0,0,0,0,3,2 = 1.649; 0,0,1,0,0,0,3,2 = 1.619; 0,0,0,0,1,2 = 1.612; 0,0,0,0,0,2 = 1.593 (all beat dev max 1.578).
## Conclusion: no clean concept. Looks like a diffuse cell-weighted readout of the board (layer 1) plus a last-move-cell term,
   with two families: early games with a tall col 0 and/or my stones at bottom cols 1-3 with their stone just
   dropped on (0,2)/(0,4); late games where the opponent just filled col 4 (row 5) or opened an empty col 4. Confidence low.
