# U08 notebook (layer 5, pole -, threshold 1.389, rate 3%, dev max 56.9)

## Observations from examples
- Band 9 (23-57): essentially ALL have must-block at (0,4): opponent has a bottom-row three with the gap/end at column 4.
- Band 8 (6-23): must-block (or my win) on bottom row at other columns (0,1),(0,2),(0,3),(0,5),(0,6). Col 4 strongest.
- Bands 5-7: mix; some bottom-row threats, some vertical must-blocks (3,5),(3,6),(4,3), many with no immediate threat.

## Hypotheses
H1: fires when there is a playable threat cell on the bottom row (must-block, maybe also own win); level by column (4 highest).
H2: any must-block (playable opponent win) - broader, vertical/higher rows weaker.
H3: low-band residue = something about the cell being in column 4/5 region?

## Minimal pairs (act)
- Opponent bottom-row three with (0,4) empty winning cell: 15-40 (3,3,6,0,5 = 37; 2,0,3,0,5 = 15.6; 1,0,2,0,3 = 25).
- Same for my own win at (0,4): 12-32. Placing a stone in (0,4) kills it (3,3,6,0,5,4 -> 0.3).
- Opponent bottom win at (0,2),(0,3),(0,5),(0,6): ~2-17, context dependent; at (0,0),(0,1): ~0.
- My own bottom wins away from col 4: usually ~0 (1,6,2,6,4,5 -> 0; 4,6,5,6,6,0 -> 0.2), sometimes fires (2,6,3,6,4,0 = 7.7).
- Vertical must-blocks: no firing (4,4,4,0,4 -> 0.2).
- Open bottom two that a stone at (0,4) turns into an open three (2-3 or 3_5 with ends open): 2.4-6.9, for either side (3,0,2,0 = 6.4).
  Same pattern not involving col 4 (1-2 with 3 empty): ~0. Exceptions: 3,3,2,3,6 = -0.1.
- Late-game col 4 the lowest column: 0.5-1.7, hovers at threshold (diffuse low band).

## Scores
1. p1 any bottom-row win cell, either side: F1 0.352 (P .51 R .27), sim share -90 (level 0 baseline bad)
2. p2 + playable threats rows 1-2: F1 0.253 (P .19 R .40) -> too broad, dropped
3. p3 bottom-row wins cols 2-6: F1 0.352 (P .61 R .25)
4. p4 horizontal-only bottom wins cols 2-6, baseline level 2, 0 if col4 full: F1 0.357 (P .70 R .24), sim share -0.47
5. p5 + "stone at (0,4) would create a bottom open three": F1 0.391 (P .69 R .27), sim -0.47  <- best
6. p6 own wins only at col 4: F1 0.380 (P .73 R .26) -> slightly worse
7. p7 = p5 detection, recalibrated levels (9/8/7/1/0): F1 0.391, sim share -0.46. Final.
Recall is capped: ~2/3 of firing is in 1.39-2.9 band, diffuse (often late games, col 4 low/empty), no clean rule found.

## Steer
- Forcing max raises column 4 (+0.46 on 1,6,0,1,2; +0.96 on a mid-game position). Zeroing a firing position changes nothing (col-4 block already chosen).

## Synthesis
3,3,6,6,2,0,0,1,5 = 60.0 (beats dev max 56.9): opponent has 2,3,_,5,6 on bottom row.
