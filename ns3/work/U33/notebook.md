# U33 notebook (layer 0, pole -, threshold 2.100, dev max 11.375)

## Examples (ex1.txt + band 4/5 seeds 2,3)
- Every band 6-9 example: last move in column 5. Top (10.8-11.4): ply 4, last move 5, col 5 otherwise empty.
- Band 5 (2.1-4.3): late-game col-5 moves, and ply-4 positions with last move col 0.
- Band 4 non-firing col-5 moves: column 5 already had stones.

## Hypotheses
H1: last move in col 5 (token-level, layer 0). H2: suppressed by earlier stones in col 5. H3: ply-4 col-0 secondary.

## act minimal pairs
- 3,4,2,5 = 11.4; 3,4,2,5,...,5 (second 5, earlier one by mover-to-move) = -1.9.
- 3,5,2,4,5 = -2.75 (col5 has a stone of the side to move) vs 5,3,2,4,5 = 2.07 (col5 stone of same player as last mover) vs 3,4,5,2,5 = 2.23.
- 3,4,5,5 = -1.97 ; 3,4,2,2,4,4,5,5 = -1.96 ; 3,3,2,2,4,5,4,5 = 2.38.
- first stone in col 5 at plies 4-13 with various other stones: 5.5-9.4 always fires; decreases mildly with ply.
- ply4 last col 0: 2.1-2.6 (borderline); same at ply 5-6: 1.4-1.8 (not).
=> Rule: last move col 5 and column 5 contains no stone of the player to move. Strength ~ first stone in col 5 > stacked on their own stones.

## score calls
1. p1 (last col 5 & no mover stone in col 5; plus ply4 col0): F1 0.823 (P 0.71 R 0.98), AUROC 0.984, sim share 0.79. FPs: col-5 stacks of 3 even of one colour (-1.7), ply-4 col0 with col0 already occupied.
   Extra acts: 3-high col-5 stacks negative (3,5,2,5,6,5 = -1.35); 2-stacks on own colour ~1.5-3.9, higher when the last mover is the second player (4,5,6,5 = 3.9; 5,3,2,3,5 = 1.86).
2. p2 (last col 5 and it is the first stone in col 5): F1 0.834 (P 1.00 R 0.715), sim share 0.80.
3. p3 = p2 + (2nd stone in col 5 on top of the same player's stone, mover was second player): F1 0.888 (P 0.93 R 0.85), sim 0.80.
4. p4 = p3 + (ply 4, last move col 0, first stone in col 0): F1 0.896 (P 0.90 R 0.89), AUROC 0.944, sim 0.80. FINAL.
   Remaining misses: late-game col-5 moves at 2.3-2.8; FPs late-game 2-stacks (1.2-2.0).

## steer
- 3,4,2,5 zero: col 3 0.98 -> 0.77 (-21), col1 +13. 4,6,6,5 zero: col4 -6, col5 +5. 0,1,0,5 zero: col0 -6, col6 -10, col2 +11.
- 3,3,2,2,4,4,5 zero: no change. Max on non-firing positions: <=7 pts.
=> small, position-dependent effect; mostly sharpens the model's current favourite reply; no fixed column.

## synthesis
6,4,3,5 = 11.562 (beats dev max 11.375); 3,4,2,5 = 11.375 (ties). Best = ply 4, second player's first stone in col 5, centre stones.
