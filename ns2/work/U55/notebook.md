# U55 notebook (layer 4, pole +, threshold 3.082, dev max 42.7)

## Examples (40, seed 0)
All 20 firing examples have >=2 of MY stones stacked on top of column 0 (leftmost) with the cell above empty.
Near-misses (band 4) also have X,X on top of col 0 but with a must-block / immediate win elsewhere (2.5, 1.6, 1.7).

Hypotheses:
H1: my vertical run on top of column 0 (>=2 stones, room to reach 4). Strength grows with run length (3 = immediate win, ~25-30).
H2: H1 but suppressed by an opponent must-block elsewhere.
H3: generic "my vertical threat in any column" (rejected below).

## act minimal pairs
- 0,3,0,4 (X,X col0) 9.3; same with X,X in col 6 0.08, col 1 -0.06, col 3 -0.06 -> column 0 only (H3 rejected).
- 0,3,0,0 (opponent caps col0) 0.58 -> top must be mine.
- 0,3,0,4,0,5 (X,X,X, immediate win) 29.2; next 0 capping -> -0.09.
- opponent's 3-stack in col 0 (0,0,3,0,4,0): 0.4 -> only my stones.
- O,O,O,X,X (no room to make 4): 0.31; O,X,X: 12.3; O,O,X,X: 6.2 -> needs room.
- 2-stack value varies 1.1-12 depending on rest of board (e.g. 5,0,3,0,2 = 1.1, 2,0,3,0,5 = 1.5).

## score calls
1. p1 (my run of >=2 on top of col 0 with room to reach 4; level 3-run=9, 2-run=5): F1 0.795 (P 0.66, R 0.99), AUROC 0.989, sim share 1.64.
   FPs: many late-game, several with an opponent threat cell in column 0 just above my landing cell (playing 0 would hand them a win).
2. p2 (+ exclude when opponent threat at (landing+1, 0)): F1 0.830 (P 0.73, R 0.97), sim 1.69.
3. p3 (+ exclude when opponent threat anywhere in col 0 above landing): F1 0.836 (P 0.74, R 0.96), AUROC 0.974, sim 1.69. FINAL.

## other tests
- 2-stack strength is context-dependent (1-12); no clean recency effect (0,3,0,4,... stays 5-9 over 10 plies; other games decay).
  Engine scores do not explain it. Left as noise / exception.
- A raised 3-stack (O at bottom then X,X,X) is the strongest: 1,0,0,4,0,4,0,3 = 51.6.
- Opponent must-block elsewhere can lower it (1,0,2,0,0,3,0,4,0,6 = 9.0 vs ~40 without).

## steer
- 0,3,0,4 (2-stack): max -> col0 +0.15, col2 -0.20; zero -> col0 -0.03.
- 6,2,0,5,0,3,4,4,2,3: max -> col0 +0.12, col3 -0.19.
- 3,2,1,4 (no col0 stones): max -> col0 +0.15.
- 0,3,0,4,0,5 (3-stack win): zero -> col0 0.77 -> 0.30 (-0.47); max -> +0.15.
Effect: pushes the model to play column 0 (extend/complete the vertical).

## synth
1,0,0,4,0,4,0,3 = 51.6; 2,0,0,4,0,4,0,3 = 49.2; 2,0,0,3,0,3,0,4 = 46.1; 6,0,0,4,0,5,0,6 = 43.4 (all beat dev max 42.7).
