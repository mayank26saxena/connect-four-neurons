# U36 notebook (layer 3, pole -, threshold 1.849, dev max 2.723, rate 3.0%)

## Examples
- Bands 5-9 (all fires) across seeds 0-3: ~69 of 70 sampled firing positions are the EMPTY board (act 2.322 exactly).
  One exception: 2,0,0,6,6,2,2 (act 1.989). Band 4 (just below threshold) = assorted early/mid positions, no obvious pattern.
- Empty board at 1/(avg game length+1) of positions ~ 3%, matching the firing rate.

## Hypotheses
H1: fires only on the empty board (ply 0), i.e. a "start of game" detector.
H2: a weaker, noisy component fires on scattered early positions (values swing +-2 move to move, e.g. 2,0,0,6,6 = 1.33, +2 = -0.70, +2 = 1.99); no clean pattern seen.
H3: early-game (low ply) generally - contradicted: 1 stone (col 1) = -0.82, 3,3 = 0.69.

## act tests
- 2,0,0,6,6,2,2: -1.19, -0.22, 1.33, -0.70, 1.99 -> alternating, parity-ish noise, not a stable feature.
- 0,3,3,3,3,5: 0.79, 0.39, 0.67, 0.11, 1.76.

## score 1 (p1.py: fires iff ply==0)
F1 0.986 (P 1.000, R 0.972), AUROC 0.986; simulation share of ceiling 0.01 (recovers 1.3% of a small zero-ablation damage).
57 misses: scattered mid-game positions just above threshold (1.9-2.1), e.g. 0,1,3,2,5,0,2,3,3 (2.097), 2,0,0,6,6,2,2 (1.989).
No shared pattern found (checked last-move stacking, parity, ply); activation on non-empty boards swings by +-2 per move.
Decided not to spend more score calls: the remaining 3% of firing looks like noise.

## steer
Empty board (to zero), 2,0,0,6,6,2,2 / 0,1,3,2,5,0,2,3,3 / 3,3 / 1,2,2,2,1,5,4 (to max): all changes <= 0.02. No measurable effect.

## synth
Empty board 2.322, 0,1,3,2,5,0,2,3,3 2.097, 2,0,0,6,6,2,2 1.989, 0,3,3,3,3,5 1.756: none beats dev max 2.723.
Greedy one-move extensions/substitutions around the 2.097 position did not improve it.
