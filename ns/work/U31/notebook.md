# U31 notebook (layer 3, pole +, thr 0.653, dev max 8.306)

## Observations (examples, 40 + band9 x16 + seed3)
- Top band: almost all have an opponent stone sitting directly on top of a vertical run of MY stones, mostly column 5 (XXX then O at row 3), sometimes column 3.
- Low firing band: early openings (0,0; 4,4; 5,5; 5,6; 6,0) - opponent stacks on my stone or plays right edge.

## Hypotheses
- H1: an opponent stone caps a vertical run of my stones, column 5 (strongest) or 3; strength grows with run length.
- H2: the last move (opponent) was the capping move.
- H3: parity / first-player effect.

## Minimal pairs (act)
- 5,0,5,0,5,5 (XXX capped col5) 4.47; 5,0,5,0,5,4 (uncapped, my win) 0.51; 5,0,5,0,5,3 0.09.
- cap then two unrelated moves 5,0,5,0,5,5,1,1 -> 5.95 : cap need not be last move (H2 rejected).
- same column cap with "me" = second player 5,0,5,0,5,5,1 -> -0.12 (it's THEIR three capped by me) - must be MY stones capped.
- column dependence of XXX+O (O's elsewhere): col5 4.5/5.4/2.0, col3 2.1/1.3, col6 0.76, col0 0.79, col2 0.6, col1 0.2, col4 ~0 !
- 5,5 2.6, 5,5,5,5 2.8, 5,0,5,5 (XX then O at row2) 0.5 (oddly low).
- 2-move table: stacking a,a fires for 0,1,4,5; O at col 6/0 after X in 4/5/6 fires weakly.

## Score calls
- call 1 (p1, accidentally run twice -> calls 1+2): any column with O directly on my run, column-weighted. F1 0.043 (P 0.022 R 0.505). Far too broad.
- call 3 (p2): O at (3,5) over my stone, or O at (3,3) over my two. F1 0.078, P 0.045. Pattern is common mid-game but unit rarely fires there.
- call 4 (p3): col5 rows0-3 = XXXO or ?XXO, col3 ?XXO, plus 13 ply-2 openings. F1 0.174 (P 0.108 R 0.442).
- call 5 (p4): core pattern minus ply/col-2 penalties, high threshold. F1 0.126 (P 0.20 R 0.09). Even XXXO in col5 is only ~20% precise by itself.
- Found via act: my own other threats suppress strongly (dev FP 2,4,5,6,6,0,4,1,5,0,5,5 = -3.0 with my row-1 XXX threat at (1,3); removing those stones restores firing). Opponent stones in column 2 also suppress (base 9.9 -> 0.87 after adding O in col2).
- call 6 (p5): core pattern, minus their col-2 stones, minus 2 per my threat cell, minus their threat cells, minus ply penalties; plus ply-2 openings. F1 0.397 (P 0.46 R 0.35), AUROC 0.668, sim share 0.09.
- call 7 (p6): p5 with col-2 penalty x2 and early-game (ply<=6) "opponent stacked on my stone in col 0/1/4/5". F1 0.394 (P 0.377 R 0.411), AUROC 0.695, sim share 0.10. Chosen as final (tied F1, better AUROC/sim).

## Steering
- 5,0,5,0,5,5 / 5,6,5,6 / 3,0,3,0,3,3 / 6,0,5,0,5,1,5,5 / 5,5: max or zero changes move probs by <= 0.03.
- 5,0,5,0,5,5,6,6,1,1 (act 9.9): zeroing raises col 3 by +0.07, lowers col 1 by 0.05. Essentially no measurable effect.

## Synthesis
- 5,6,5,6,5,5,0,0,1,1 -> 10.60; 5,6,5,6,5,5,1,1,0,0 -> 9.98; 5,0,5,0,5,5,6,6,1,1 -> 9.93; 5,6,5,6,5,5,1,1,0,0,4,4 -> 9.53 (all beat dev max 8.31).

## Conclusion
Core concept is clear (opponent caps my vertical stack in column 5 at row 3, early-mid game, no other threats), but the unit is heavily modulated by other board content and has a diffuse early-opening component. F1 ~0.40 -> low/medium; I call it low-medium -> "low" boundary; choose medium? F1 0.397 < 0.4 -> low.
