# U01 notebook (layer 5, pole +, threshold 1.154, dev max 97.4)

## Examples (ex1, ex5, ex6)
- Top bands (40-97): opponent has a vertical three in column 3 (center), cell above empty = must-block in col 3.
- Band 7 (4-40): vertical threes elsewhere (col 0), col-3 threats that are not vertical.
- Bands 5-6 (1.2-4.5): nearly all have a must-block (their_playable_wins) in any column; a few with none.
- Non-firing positions with must-blocks exist (e.g. 109408, 112078 at (3,4)) - late, crowded boards.

## Hypotheses
H1: fires when opponent has an immediate threat I must block; strength scales with center column, max for vertical three in col 3.
H2: only vertical threes (any column).
H3: a "center column threat" detector.

## act minimal pairs (vertical three of O, X to move)
col0 0.99, col1 4.3, col2 0.55, col3 51, col4 -0.14, col5 1.4, col6 4.2 -> column 3 dominates.
col3 vertical with X having an own threat elsewhere: 29 (lower). Last move elsewhere (3,0,3,1,3,5,6): 43, still fires.
Horizontal threat at (0,3): 0,6,1,6,2 -> 6.8; 4,0,5,0,6 -> 3.8; 0,6,1,5,2,6 -> 14.6. Horizontal open-two-ends 2,0,3,0,4 -> 2.4.
Removing threat (0,3,0,3,4,0) -> -0.08.
=> H1 favoured: any must-block makes it fire weakly; col 3 strongly; vertical col 3 hugely.

## Score calls
1. p1 (any must-block): F1 0.234, P 0.14, R 0.70. Must-blocks are 14.8% of positions; too broad.
2. p2 (playable win/block in col 3, either side): F1 0.352, P 0.41, R 0.31. FPs = late (ply 34-36) col-3 horizontal threats; misses = early openings w/o threats, own wins elsewhere, side-column verticals.
   act: horizontal block at (0,c) for c=0,1,2,4,5,6 -> 0.22,0.00,0.37,-0.43,0.03,0.91; c=3 -> 6.2. Column 3 specific.
   act: own immediate wins: vertical in other cols mostly < 1, horizontal own threes 3-12.
   Crowded board damps: col-3 vertical at ply 29 -> 9.3 vs 61 early.
3. p3 (col-3 vertical three of either side; col-3 playable win/block if ply<30; opp vertical three col 1/6 if ply<30): F1 0.418, P 0.42, R 0.42.
4. p4 = p3 + my immediate win anywhere if ply<20: F1 0.437, P 0.42, R 0.45, AUROC 0.72. BEST.
5. p5 = p4 without col 1/6 verticals: F1 0.417 (P 0.57, R 0.33).
Simulation: ceiling is negative (perfect reader -274.5%), share = nan; not informative.

## Unexplained firing
Some early openings with no threats fire (2,6,2,2 -> 9.9 but 2,0,2,2 -> -0.16); these look like "model strongly prefers column 3" cases that I cannot express as a board pattern.

## Steer
Zeroing at 3,0,3,0,3 (act 51): col 3 prob 1.00 -> 0.67. Max at 2,6,2,0: col 3 0.41 -> 1.00; at 4,6,4,4: 0.18 -> 1.00. Effect: pushes the move to column 3.

## Synthesis
Best 83.5 (6,6,6,0,1,1,3,2,3,4,3): opponent three stacked at bottom of col 3, early. Dev max 97.4 not beaten.
