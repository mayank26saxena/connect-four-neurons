# U58 notebook (layer 3, pole -, threshold 0.349, dev max 4.378)

## Exploration
- 40+ examples per band (5 seeds x 100). Activation flips with perspective (alternating plies), board-state driven, little dependence on last move column.
- Cell-difference counts (firing vs bands 0-3), strongest: them at (2,0) and (1,0) [col 0 rows 1-2]; me at (2,4); them at (0,3) with me on top (1,3); them at (1,4).
- Top-firing set (>0.95): O(2,0) 75% vs 19%; X(2,4) 66% vs 15%; O(0,3)+X(1,3) 60% vs 22%.
- Steer: effect tiny (<=0.05 prob change on any column) in 6 positions.

## Hypotheses
- H1: additive sum of three local stone patterns: (a) them (0,3) under me (1,3); (b) me (2,4) on them (1,4); (c) them stacked at (1,0),(2,0).
- H2: me has a diagonal line through (1,3),(2,4) (diag (0,2)-(3,5)). Against: O at (0,2) boosts rather than kills (0.95 -> 1.96).
- H3: open-ish threat cells for me. Against: 62906 fires 2.66 with no threat cells.

## Minimal pairs (mk.py builds sequences from boards)
- 5,5,5,3,3,2 =1.78; P1 skip (1,3) -> 0.07; me at (0,3) instead of them -> -0.42.  (a) confirmed.
- 83565 (3.2): removing me at (2,4) -> ~0.45; removing me at (3,3) -> ~1.07; others small.
- Constructed O...X../O..XO../X..OX.. = 1.36; without (2,4) X = -0.09; swap (0,3)/(0,4) colours = 0.21; add O(0,2) -> 1.95.
- Single features alone give ~0.25-0.4 (near threshold); they add up.

## Dev metric log
1. p1 (>=2 of: them(0,3)+me(1,3); them(1,4)+me(2,4); them(1,0)+(2,0)): F1 0.133 (P 0.095 R 0.218) AUROC 0.578, sim share 0.28.
2. p2 hand-weighted cell sum (weights read off the cell-difference counts), thr 6: F1 0.147 (P 0.090 R 0.399) AUROC 0.639.
3. p3 "I have a non-immediate threat cell, no immediate wins/blocks": F1 0.068, AUROC 0.55. Rejected.
4. p4 conjunction col3 them/me AND (col0 them rows1-2 OR col4 me/them/me): F1 0.140 (P 0.114 R 0.181).
5. p5 = p2 with thr 8: F1 0.167 (P 0.133 R 0.223) AUROC 0.59. BEST.
6. p6 open diagonal lines (>=2 own, no opponent) through (1,3)/(2,4)/(0,3)/(1,4): F1 0.108. Rejected.

## Why low confidence
- Minimal pairs show strong, non-additive context effects: the 2x2 checkerboard them(0,3),(1,4)/me(0,4),(1,3) fires (0.93) at cols 3-4 and 4-5 but not at cols 0-1 or 2-3; adding one far stone pair (me (0,0), them (0,6)) kills it (-0.04); swapping colours of a col-2 pair moves a 3.0 position to -0.07 or 3.57.
- Activation is a board function (same board, many orders: nearly identical), perspective-dependent, mid-game heavy, but no single cell/line rule gives precision above ~13%.
- Possibly a random direction or a strongly polysemantic mixture.

## Steer
- 8 positions, to zero and to max: change <= 0.05 probability on any column. Effect: none measurable.

## Synthesis (greedy add-a-pair hill climb with act, then order search)
- 0,0,5,0,5,3,3,5,3,2,2,3,3,1,2,3,6,2 = 4.528 (beats 4.378); 0,3,5,0,5,0,3,5,3,2,2,3,3,1,2,3,6,2 = 4.486 (beats); 0,6,4,6,3,3,4,4,3,3,0,6,0,0,0,2,6,4,1 = 4.353.
