# U10 notebook (layer 5, pole -)

## Observations
- Band histograms (150 ex/band): firing strongly associated with heights[4] in {1,2} (band9: 85/150 at h4=2, 35 at h4=1) and heights[3] >= 3 (never <2 in band 9). Last move most often col 4.
- Mirror positions (c -> 6-c) of top examples do NOT fire: column-4 specific.
- steer max on non-firing positions: lowers column 3 by ~0.15-0.20, small gains elsewhere. On firing positions forcing zero changes little (<=0.03).
- Example 2778 (7.14): O just played (1,5); O playing col-4 landing (2,4) would make two 3-of-4 diagonals (with (3,3),(1,5)). Replacing the X under (1,5) kills it (-0.26).
- 141753 (7.2): O just played (3,2) making diag (3,2),(2,3) toward col-4 landing (1,4).

## Hypotheses
H1: heights[4] in {1,2} and heights[3] >= 3 (shape).
H4: the opponent playing the column-4 landing cell would give them one or more 3-of-4 lines (a strong cell for them in col 4, low rows).
H2: opponent has a fork-creating move (rejected: open-two on bottom row elsewhere does not fire).

## Dev metric log
- s1 p1 shape (h4 in 1-2, h3>=4): F1 0.112, AUROC 0.60, sim share 0.13. Shape is a correlate only.
- s2 p2 opponent gain (>=2 three-windows) at col-4 landing: F1 0.177, AUROC 0.61, sim 0.12.
- s3 p3 "exactly one non-losing move" (2-ply search, any column): F1 0.142 (P 0.08, R 0.47), AUROC 0.66. Too broad (16% of positions).
- Facts on 25 band-9 examples: in most, the teacher says ONE move saves the game, usually column 4 (sometimes 2 or 6); also my immediate win / must-block in col 4.
- s4 p4 column 4 is the critical move (my win / must-block / only safe move at col 4): F1 0.252 (P 0.24, R 0.27), AUROC 0.62.
- s5 p5 opponent line potential through cell (2,4): F1 0.127. Dropped.
- s6 p6 p4 + "col 4 loses" restricted to low col 4: F1 0.146. Dropped.
- s7 p7 unique critical column (my only win, only must-block, or only non-losing move) is column 4 or column 2: F1 0.302 (P 0.23, R 0.45), AUROC 0.70, sim share 0.13. BEST.
- An 8th scoring call (adding 2-safe-move cases) was blocked by the permission system; not run.

## Minimal pairs
- Single-stone edits of a top example (0,1,3,5,5,3,3,4,3,4,0 -> 7.99): moving either of my stacked col-4 stones (0,4),(1,4) anywhere kills it (< 0); the opponent's last stone can go almost anywhere. Board-based, not last-move-based (reordering moves to the same board keeps 7-8).
- Another top example (141753) is robust to many edits; depends on opponent 2x2 block at cols 2-3 rows 2-3.
- Mirrors (c -> 6-c) of top examples do not fire: strongly column-4 specific.
- Open-two on bottom row without tall col 3 does not fire.

## Effect (steer)
- Forcing max on non-firing positions lowers column 3 by 0.12-0.20 and shifts it to cols 2/4/1. Forcing off at firing positions changes <= 0.03.

## Synthesis
- 0,1,3,5,5,3,3,4,3,4,1 -> 9.64 (beats dev max 8.39). Model plays col 4 at 0.99 there.

## Conclusion
Unit looks like a tactical "position hinges on one column, mostly 4 (or 2)" signal with strong column-4/tall-column-3 bias, but rules capture under half of it. Confidence low.
