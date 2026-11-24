# U16 notebook (layer 2, pole -)
## Observations (examples bands 0-9)
Nearly all firing positions: column 0 has exactly 4 stones, top stone (row 3, col 0) is the opponent's (O). Top band: sparse boards, last move = col 0.
## Hypotheses
H1: grid[3][0]==2 and heights[0]==4 (O on top of a 4-high col 0).
H2: H1 but strength depends on last move being that stone / sparse board.
H3: generic "opponent stone on 4th row of an edge column" (col 6 too?).
## Tests (act)
- 0,5,0,3,0,0 (col0 XXXO, last move col0) 5.6; +1 move (cell becomes mine) -0.7; +2 moves elsewhere 3-4 (decays with recency/ply).
- other columns (1,2,6) same pattern: ~0. Column 0 specific.
- col0 pattern below matters: XXXO >> XXOO/OXOO (~2.4) > XOOO (1.2). Dense board weakens (5.6 -> 2.1 at ply 22).
- height 5: XXXOX fires 3.1, OOOXO 3.5, XXXOO -1.6 (O on O kills), XXXXOX 2.5, OOOXXO -0.3, XXXOOO -2.9.
## Scores
- p1 (h0==4, g30 theirs, g20 mine): F1 .704 P.58 R.89 AUROC .934 sim share .70
- p2 (h0==4, g30 theirs, and last_col==0 or g20,g10 mine): F1 .736 P.63 R.88 sim .60
- p3 (p2 + ply caps): F1 .736 P.77 R.70 sim .54 (level worse)
- p4 (added "their stone at row 4 on my row-3 stone" case B): F1 .378, P .24 -> case B is common on dev and rarely fires; my sparse act tests misled. Dropped.
- p5 (p2 fires + level emphasising stone pattern under row 3, ply tiers, +1 recency): F1 .736 P.63 R.88 AUROC .931, sim share .71. FINAL.
## Steer (4 positions)
Forcing max or zero changes move probs by <= 0.07; at 0,0,4,3,3,0,5,3,5,4,0 max raises col3 +7pts, lowers col5 -5; at 0,1,0,3,2,3,3,3,2,0,0 zeroing lowers col2 -5. Otherwise ~0. Effect weak.
## Synthesis
Best 9.04 (0,1,2,0,1,0,0: col0 bottom-up O X X O, just completed by them, rest of board nearly empty). All 5 below dev max 9.83.
