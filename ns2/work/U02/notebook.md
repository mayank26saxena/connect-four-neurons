# U02 notebook (layer 1, pole +, thr 0.294, dev max 3.839)

## Examples (band 0-9, ~100 read)
- Band 9 dominated by: last move in column 3 landing on row 0 (opponent puts the FIRST stone into the empty centre column), ply 8-30.
  Histogram (seed 5, n=150 per band) of last-move (col,row): band 9: col3 row0 118/150; band 7: 47; band 2: col3 row0 almost absent.
- Lower firing bands (5-6): last move col 3 at higher rows, or first stone in another empty column (1, 6, 0).

## Hypotheses
- H1: opponent's last move was the first stone in column 3, late in the game (ply >= ~8). Strength grows with ply.
- H2: generalisation: last move opened any empty column late; col 3 strongest.
- H3: static "centre column low while neighbours tall" (from 45034, col 3 height 1 / col 2 full) -- partially; see tests.

## Minimal pairs (act)
- 0,2,6,5,0,5,0,0,2,2,1,4 then +3 -> 3.839 (from -0.21); +6/+1/+5 instead -> -0.4..-0.6.
- Ply sweep with col 3 first play: ply4 -0.06, ply8 -0.005, ply9 0.10, ply10 0.19, ply11 0.77, ply12 0.87, ply13 1.77.
- Col 3 at row 1+ as last move (col 3 stone played the move before): -0.13 -> no firing. With earlier col-3 stone by same player far back: 0.2-0.95 (mixed).
- First stone in other empty columns at ply 13: col6 0.63, col1 0.51, col5 0.44, col0 0.17-0.29. Col 3: 1.9.
- Persistence: after col-3 opening at ply 13 (3.84), at ply 15 (same side to move) 1.26, 17 0.54, 19 0.35; at even plies ~0.
- 45034 (col3 has single old O stone, col 2 full, last move col0): 1.99; robust to changing last move; adding stones to col 3 drops it -> some static "their lone stone in low centre column" component.

## Score calls
1. p1 (last move row 0: col 3 ply>=8, or cols 1/5/6 ply>=12): F1 0.198 (P .185 R .213), sim share 0.19. Other-column openings are mostly false positives.
2. p2 (static: col 3 low with their stone at bottom): F1 0.173 (P .116 R .342), sim 0.20. Static component too weak / diffuse.
   -> Histograms: firing positions almost never have col 3 empty; col-3 contents in firing bands are mostly "only their stones" (O, OO).
   -> act: last move col 3 at row 1 fires (1.0-1.7) when the stone below is also theirs, not when it is mine; row 2 (OOO) is strongly negative (-0.7, -1.65).
3. p3 (last col 3, col 3 all theirs, ply>=9, any row): F1 0.247 (P .41 R .18), sim 0.10. Row-2+ cases are FPs.
4. p4 (last col 3 row 0, ply>=9; level by ply+h2+h4): F1 0.243 (P .75 R .145), sim 0.41.
5. p5 (row<=1, all theirs, ply+h2+h4-6*row>=12): F1 0.254 (P .615 R .16), sim 0.36.
6. p6 (p4 + row-1 OO with ply>=13): F1 0.257 (P .623 R .162), sim 0.36.
7. p7 = p6 fires + p4-style level: F1 0.257 (P .623 R .162), AUROC 0.58, sim share 0.44. FINAL.

## Interpretation
The top of the distribution (bands 7-9) is clean: the opponent has just put the first stone (or a second stone on their own first) into the
centre column, late in the game; activation grows with ply and with stones already in columns 2 and 4 (act: 0,0,0,0,1,1,1,1,5,5,5,5,3 -> 0.27
vs 2,2,2,2,4,4,4,4,6,6,6,6,3 -> 1.17). Bands 5-6 (2/3 of all firing) are diffuse: last col 3 only ~1/3, col 3 low, otherwise no clear rule.
That bulk is not captured (recall 0.16). Effect when steered: small, mostly on column 3, sign varies (zeroing at the 3.84 example: col 3 +7, col 2 -7;
forcing max at a 0.31 example: col 3 +4, col 6 -5; two other positions under 2 points).
Synthesis: extending 0,2,6,5,0,5,0,0,2,2,1,4 with more stones in cols 2/4/6 before dropping into col 3 reached 5.82 (dev max 3.84).
Confidence: low (best F1 0.257 < 0.4); the clean top feature is real, but most firing is unexplained.
