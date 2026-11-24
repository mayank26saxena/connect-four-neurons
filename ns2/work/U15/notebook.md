# U15 notebook (layer 5, pole +, thr 3.755, dev max 11.06)

## Examples (ex1.txt, ex9.txt)
- Top band: late game (ply 28-41), a nearly empty column (often col 3/4) containing threat cells for one or both players,
  typically the opponent's threat directly above my landing cell (poisoned column). Few legal columns.
- Early exceptions: ply 5-7 with opponent open three on bottom row (two must-blocks) -> also fires (6.3-6.7).
- Trace of game 110396: jumps 0.3 -> 7.1 when the opponent fills another column, so I have fewer safe moves
  (engine flips from +962 to -962 for mover). Looks zugzwang-ish.

## Hypotheses
H1: some legal column is poisoned: the cell right above its landing cell is a threat cell for the opponent.
H2: any opponent threat cell in a column with empty cells (above landing), weighted by few legal moves.
H3: lost-by-zugzwang: poisoned column + even count of remaining safe cells.

## Score 1 (H1 poisoned column): F1 0.079, P 0.043, R 0.54, AUROC 0.59, sim share -0.05. Rejected.
Misses were forced endgames with only cols 4/5 open, and early vertical must-blocks in col 3.

## New direction: which columns are full
Histogram of full-column rates by band (examples --n 300 seed 3): band 9: col0 97%, col1 100%, col2 77%, col3 87% full,
col4 13%, col5 0%, col6 63%. Bands 0-2: col1 rarely full. -> Unit tracks "left side (esp. col 1, col 0) full,
cols 4/5 still open".
Minimal pairs (game 110396 at ply 31, alternatives for 32nd move): fill col1 -> 7.07; col0 (5th stone) 1.87; col3 2.08;
fill col4 -> -1.51; fill col5 -> -1.34. So closing col 4 or 5 kills it, closing col 1 drives it.
Toy (no tactics): cols 0,1 full + 5,6 full: 2.0 (no). cols 0,1,2,6 full, legal {3,4,5}: 3.96 (just fires); +3,3: 4.24.
Parity wobble: even ply (me first) a bit higher.

## Score 2 (weighted full-left-columns, cols 4/5 open): F1 0.476, P 0.38, R 0.64, AUROC 0.80, sim share 0.31.
Misses: early positions with opponent must-blocks: bottom-row open three (double threat), vertical three in col 3.
Minimal pairs: 2,2,3,3,4 -> 6.45; 1,1,2,2,3 -> 4.90; 3,3,4,4,5 -> 6.94 (open three, two must-blocks: fires);
0,0,1,1,2 (single threat at (0,3)) 0.65; 4,4,5,5,6 (single) 1.52. Blocking one end (3,3,4,4,2,5) -> 0.11.
Vertical col-3 three toy (3,0,3,1,3) only ~1.9; but dev 59221 (3,6,2,4,2,1,3,1,3) 5.18. Col 6/2/0 vertical threes: negative.
Band 6 (seed 5) teacher scores: mostly 1-2 legal columns, forced/decided endgames; one oddity all-winning opening.
Steer: max raises col 4 (+0.19..+0.29); zeroing moves mass 4 -> 5 at top example. No effect when move is forced.
H4: union of (a) late game with left columns full & col 4/5 open, (b) opponent double threat, (c) col-3 must-block.

## Score 3 (H4 union): F1 0.425, P 0.30, R 0.73, AUROC 0.84, sim 0.28. Recall up, precision down.
FP 57083: col-3 must-block at row 3, act -0.30 -> col-3 must-block component unreliable; drop it.
Toy fill tests (12-move alternating pair fills, no tactics): full {0,1,2,6} 3.96; {0,6,1,5} 3.26; {1,2,5,6} 2.96;
{0,1,2,3} 3.23; {0,3,1,6} 2.55; {0,1,5,6} 1.67; {0,4,1,5} -0.45; {3,4,5,6} -2.15; {4,5,0,6} -2.82.
=> filled col 4 strongly negative, col 5 mildly negative; col 1/0/2 positive. Tactics push it higher in real games.

## Score 4 (p2 endgame with stronger col-4 penalty + opponent double threat): F1 0.457, P 0.35, R 0.66, sim 0.32.
Misses like 6097/23544: cols 2,3,6 (or 0,2,3) full with cols 1,4,5 open -> my col-1 weighting too narrow.
Toy order effect: same full set {0,1,2,3} gives 3.23 or 1.86 depending on fill order -> history matters; board-only rule capped.
Next: linear height score, w=[1,1.5,1,0.7,-1.5,-0.5,0.7] (hand-set from toy fills + per-band mean heights), threshold 16.

## Score 5 (linear heights): F1 0.284 - worse. Full/closed columns matter, not heights.
Minimal pairs on 110396@31 (+moves): col0 full only 0.71; col1 full (col0 5/6) 4.87; col0+col1 full 9.2-10.2;
col1 full then fill col4 2.28 / col5 2.22; col1 full + col3 stones 4.0 -> 6.5.
=> Key: BOTH left columns 0 and 1 full, cols 4/5 open. Others (2,3,6) full add.

## Score 6 (both cols 0,1 full as gate): F1 0.473, P 0.43, R 0.53, AUROC 0.75, sim 0.28.
FPs: cols 0,1 full but many other columns open (46275, act 1.4). Misses: 19655 (cols 0,1,2,4,6 full, legal 3,5) 7.46 ->
col-4-full penalty too strong when the rest is closed.
Teacher-value check on 110396 variants: activation is NOT the game value (fill-col4 variant also lost but act -1.5;
1,0 variant winning but act 4.9). Structural feature of which columns are closed.
p7: weighted closed-column score: 3*col0 + 3*col1 (1.5 each if 5/6 filled) + 1.5*col2 + col3 + col6 - 2*col4 - col5,
fires >= 7.

## Score 7 (p7 weighted closed columns): F1 0.472, P 0.49, R 0.45, AUROC 0.72, sim 0.23. Plateau ~0.47.
Misses now: late boards where a whole column (0, 1, 4 or 5) is still empty and most others are full (24639, 11825, 30909).
FPs: col 4 open with only 1-2 cells left and no empty column (31242 -0.66, 38230 0.90).
Final attempt p8: p2 (best) + penalty when >=5 columns still legal + early double threat (ply<=14).

## Score 8 (p8 = p2 + penalty if >=5 legal columns + early double threat): F1 0.507 (best), P 0.41, R 0.66, AUROC 0.815,
sim share 0.23 (p2/p4 had best sim share 0.31/0.32). No calls left.

## Steer
- 110396 top (10.2 -> 0): col4 0.44 -> 0.28, col5 0.49 -> 0.65.
- 43510 (2.1 -> max): col4 +0.29, col3 -0.23. Toy legal{3,4,5} (3.96 -> max): col4 +0.23, col5 -0.14, col3 -0.09.
- 2,4,2,1,3,3 (-0.3 -> max): col4 +0.19, col2 -0.22. Forced positions (44593, 59221, 3,3,4,4,2): no change.
Effect: pushes the move toward column 4.

## Synthesis (random same-player reorderings of best 110396 variant; checked with synth)
11.453, 11.340, 11.112 beat dev max 11.057; 11.027, 10.899 just below.
