# U19 notebook (layer 5, pole +, thr 2.035, max 46.9)

## Examples
Bands 7-9 (act 6-47): almost all last move col 5 with must-block in col 5 = opponent vertical three in column 5.
Bands 5-6 (2-6): mixed; must-blocks in cols 1/2/3, some no threat at all.

## Hypotheses
H1: opponent has three stacked on top of column 5 with the cell above empty (vertical threat in col 5).
H2: any opponent threat at the col-5 landing cell (horizontal/diag too).
H3: vertical three in any column (col-dependent strength).

## act tests
- 5,0,5,0,5 -> 32.4; same three in col 1/2 -> 3.7-3.9; col 0/3/4/6 -> ~0.1. Col 5 specific.
- horizontal three 3,4,5 bottom (3,3,4,4,5) -> 0.27; 2,3,4 (threat at (0,5)) -> 0.12. Not H2 (horizontal).
- three in col 5 at rows 1-3 / 2-4 -> 27-31 (height doesn't matter much); full column (no empty above) -> ~0.
- opponent three in col5, then two other moves (last move elsewhere) -> 13.9 (still fires, weaker).
- MY own vertical three in col5 -> 5.0 (fires, weak). Opp two-stack in col5 -> ~1.6-2.8.
- col 2/1 opponent three when last move elsewhere or raised -> 0.1-1.3 (doesn't fire).

## Scores
- s1 p1 (vertical three on top of col 5, either side; level 9 if opp & last move col5, 6 opp, 2 mine): F1 0.428 P 0.944 R 0.277 AUROC 0.638. Sim share nan (perfect reader -28%).
  -> core is clean; misses are the weak band 2-6.
- s2 p2 (+ any opponent playable threat in cols 1/2/5): F1 0.425 P 0.303 R 0.713 AUROC 0.831.
- s3 p3 (+ only threats in cols 1/2/5 whose line includes the last stone, i.e. just created): F1 0.458 P 0.393 R 0.549 AUROC 0.762. BEST.
- s4 p4 (p3 + threats made playable by a stone directly below): F1 0.432 P 0.311 R 0.710.
Weak band (2-6) is diffuse: newly created opponent threats, mostly cols 1/2, sometimes other cols, context-dependent
(col1/2 vertical threes fire at some heights, not others). Stopped scoring: diminishing returns.

## Steer
- neutral 3,3,4,2: max -> col2 +37, col3 -36. neutral 0,1,6,6,2,3,3: col5 +22, col2 +12, col3 -33.
- 3,2,4,5,3,3,4: max -> col5 0.55->0.94. 5,0,5,0,5,1,6 zero -> col5 0.77->0.65 (col0 +10).
- saturated blocks (5,0,5,0,5): no change. Effect = push toward blocking in col 5 (and col 2), away from center.

## Synth
3,2,3,3,1,1,5,4,5,0,5 -> 47.53 (beats dev max 46.93); 3,4,3,3,1,1,5,2,5,0,5 -> 46.42; 3,2,3,3,1,1,0,4,5,0,5,6,5 -> 45.48.
