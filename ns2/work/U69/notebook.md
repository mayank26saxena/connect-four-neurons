# U69 notebook (layer 0, pole +, threshold 0.589, dev max 1.446)

## Examples
- Top bands are very early games (median ply 6-8), last move most often in column 6 (band 8-9: ~37/70 last col 6).
- Low bands: long games. Last col 2 almost never fires.

## Hypotheses
H1: opponent just played column 6 in an early game.
H2: additive token-level function (layer 0): per-stone weights by (owner, column), averaged over the game (1/ply), plus a bonus for the last move's column.
H3: "I have no stone in column 4" suppression rule.

## Minimal pairs (act)
- 2,3,1,c: last col 0:.30 1:.37 2:-.02 3:.65 4:1.03 5:.77 6:1.35.
- 2,3,1,6 -> 2,3,4,6 (my stone col 1 -> col 4): 1.35 -> 0.17. My stone in col 4 strongly negative everywhere tested.
- Single-stone substitution sweep on base 3,4,2,4,3,4,1,6 (1.08): my stone in col 4 costs ~-0.5 (-0.8 if my latest stone), col 0 ~-0.2, col 3 ~-0.15; their stone in col 6 +0.24, col 1 -0.2, col 3 -0.15; last move: 6=1.08, 3/5 .70, 0/4 .60, 1 .35, 2 low.
- Effects roughly halve from ply 4 to ply 8 -> consistent with attention averaging (1/ply).
- Long games drift below threshold.
=> H2 adopted; H1 is the dominant single term; H3 is one of the weights.

## Score calls
1. p1 additive (owner,column) weights averaged over ply + last-col bonus: F1 0.219 (P .17 R .31), AUROC .633, sim 0.03. FPs are long games -> need a ply penalty.
2. p2 = p1 + ply penalty: F1 0.311 (P .36 R .28), AUROC .63, sim 0.04.
   New minimal pairs: last move in col 4/5 stacked on any stone kills firing (2,3,1,5 .77 vs 5,3,1,5 -.14; 2,3,1,4 1.03 vs 4,3,1,4 .05); stacking in col 3/6 does not. Weights are not stable across plies (O col 3 best at ply 4, O col 6 best at ply 8): non-additive, order dependent.
3. p3 simple rule (ply<=10, last col 6, no my stone in col 4): F1 0.286 (P .49 R .20), AUROC .60, sim 0.05. FPs: my stone in col 5.
4. p4 refined additive + col4/5 stacking penalty: F1 0.292 (P .56 R .20), sim 0.08.
5. p5 = p4 with lower threshold 0.3: F1 0.367 (P .36 R .37), AUROC .675, sim 0.08. Best.
Band-6 firing examples are very diverse (any last col, ply 4-32). Stopped here: no clean board concept; likely an order-dependent layer-0 token mix (or random direction).

## Steer
2,3,1,6; 3,1,6,3; 1,3,6,3,1; long game ending col 0; 6,1,6,3,6: zero and max both change move probabilities by <0.01. No measurable effect.

## Synthesis
2,3,6,1,6 = 1.463, 2,1,6,3,6 = 1.458 (both beat dev max 1.446); 3,1,6,3,6 1.386; 1,3,2,6 1.348; 6,3,6,1,6 1.347.
