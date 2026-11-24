# U74 notebook (layer 5, pole -)
## Examples (seed 0, seed 3)
Almost every firing position has a must-block (opponent has an immediate playable win), and I have no immediate win.
Band 9: double must-block (two open ends of horizontal three on bottom row). Bands 5-8: mostly single must-block, often vertical three by last move.
Some non-firing with must-block: only one legal move (pos 126281), early vertical threat ply 11 (act 2.5).
H1: fires iff b.their_playable_wins nonempty and no my_playable_wins.
H2: level scales with number of must-block cells (2 -> top).
H3: maybe specific to threat created by last move.

## Minimal pairs (act)
- Opp vertical three, empty above: col2 ~7-10, col4 ~6-9, col3 2.5-9 (weaker when threat cell is row 3), col1 0.1-1.9, col0 1.3, col5 -2..-3.6, col6 -2.3.
- Opp horizontal open three on bottom row (two playable wins): 9-16. Same three with one end blocked (single horizontal threat): -2..0.6. Single horizontal threat on row 1: ~0.
- My own open three (double win): 4.6-7.6; my vertical three: 0.3-3.
- Opp vertical threat in col 4 robust to where my two other stones are (2.1-6.3, mostly fires).

## Scores
- p1 (any must-block, no my win, >1 legal): F1 0.317 (P 0.19, R 0.86). Must-blocks are 13% of positions; too broad.
- p2 (opp >=2 playable wins, OR opp vertical three in col 2-4 with no win for me): F1 0.733 (P 0.76 R 0.71), AUROC 0.85, sim share 0.01.
- p3 (p2 + my double win): F1 0.697 - worse precision, dropped.
- p4 (p2 + diagonal single threats in cols 2-4): F1 0.596 - many FPs, dropped.
- p5 (p2 fires, graded level incl. col 5/6 must-block = lowest): F1 0.733, sim share 0.02. Simulation stays near 0 whatever the level; the unit's ablation effect seems to live in non-firing positions.
Most negative dev activations: single must-block in column 5.

## Steer
Zeroing at firing positions: no change (forced block still played). Forcing max in quiet openings: column 3 loses 0.2-0.3, columns 1/2 gain (or favored off-center move gains), edges/col 5 lose a bit.

## Synthesis
O open three on bottom row 1-3 plus O vertical in col 1: 2,2,3,6,1,5,1,6,1 = 17.96 (dev max 17.49). Four others also beat dev max.
Submitted.
