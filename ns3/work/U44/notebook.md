# U44 notebook (layer 5, pole -, threshold 0.766, dev max 65.9)

## Examples
- Bands 7-9 (act 5-66): essentially all = opponent just played col 1, must-block at col 1 (vertical three of theirs in col 1, cell above empty).
- Band 5-6 (0.8-4): mix: col-1 must-blocks via other lines (~3), opponent vertical three in col 5 (~3-6), opponent two stacked on top of col 1 (~1.5), misc.

## Hypotheses
H1: opponent has 3 stacked on top of column 1 with empty cell above -> very strong.
H2: weaker: any must-block landing in column 1; vertical three in col 5.
H3: unit is a mixture/generic must-block detector (rejected: horizontal threats in other cols don't fire).

## act minimal pairs
- vertical three of theirs in col 0,2,3,4,6: ~0 (no fire); col 1: 30-56; col 5: 1.3-4.8 (fires weakly).
- three in col1 even if last move elsewhere: 28-30 fires. MY vertical three in col1: 0.35 (no).
- horizontal threat at (0,1): no fire at low ply.
- two of theirs stacked in col1: 1.67 in one context, -0.3 in another (inconsistent).

## Scores
- p1 (col1 vthree=9, any col1 must-block=5, col5 vthree=4; fire>=3): F1 0.454 (P 0.44, R 0.47). Col1 must-blocks via horizontal/diagonal mostly do NOT fire -> dropped.
- p2 (fires = their vertical three on top of col 1, cell above empty): F1 0.432 (P 0.994, R 0.276).
- p3 (vertical three in any column): F1 0.294 (P 0.22) -> rejected; other columns mostly don't fire.
- p4 (p2 + their vertical three in col 5 raised off the floor, height>=4): F1 0.461 (P 0.81, R 0.32). BEST.
- Simulation reported nan share (perfect 10-level reader recovers -357%, so the metric is ill-defined for this unit); my level recovers 2.3% of ablation damage.
- Remaining ~68% of firing is a weak band (act 0.77-4, threshold 0.766) that is diffuse: last-move column histogram at band 5 near-uniform; band 6 over-represents col 1 and 5. Steer zero shows these weak activations do not affect moves. Looks like background noise around a sharp col-1 detector.

## Steer
- Forced high: puts ~all probability on column 1 (e.g. 3,3,2,4,4: col3 0.97 -> col1 1.00; 3,0,1,4,1,3,3,3,0: col1 0.54->1.00; col5 must-block: col1 +0.06).
- Ablated on col-1 three positions: no change (block of col 1 still chosen, redundant).

## Synthesis
- 6,6,1,6,1,2,3,3,3,3,0,4,1 -> 71.8 (beats dev max 65.9); several others 67-70.
