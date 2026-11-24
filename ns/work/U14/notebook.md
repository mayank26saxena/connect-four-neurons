# U14 notebook (layer 5, pole +, threshold 0.579, dev max 7.70)

## Exploration
- examples bands 0-9 (~90 positions). Top band (>2.46): 11/16 have column 4 at height exactly 4 with MY stone on top at (3,4)
  (often X at (3,3) too, "...XX.." on row 3). Others: col 4 top mine at other heights, or no obvious pattern.
- Early-game firing is common but irregular (2-ply table: e.g. 5,4 1.41; 0,4 0.99; 4,1 0.96; but 3,x never fires).
- Minimal pairs (game 3,2,3,2,6,3,4,5,3,4,4,5,4 + O last move):
  O plays anywhere except col 4 -> 1.7-5.7; O plays col 4 (covers (4,4)) -> 0.48. Same in a second game (0.15 vs 2.1-5.4).
  Replacing my move onto (3,4) by any other column -> <=0.54. So "my stone at (3,4) with (4,4) empty" is causal there.
- Steer (zero) on top example: removes ~ +0.03 from cols 3 and 4; max lowers 3/4 slightly. Small effect.

## Hypotheses
H1: col 4 height 4 and grid[3][4] mine (top of column 4 is my stone at row 3, landing cell (4,4)).
H2: generalisation: top stone of column 4 is mine (any height).
H3: unit is partly a mixture with an early-game component (non-center opening positions).

## Dev metric log
1. h1 (col4 height 4, my stone at (3,4)): F1 0.130 (P 0.113, R 0.153), AUROC 0.557, sim share 0.01.
2. h2 (top of col 4 mine, h 2-5, ply<=26): F1 0.087, AUROC 0.547. Generalising the top-band pattern loses precision.
3. h4 (some empty column, ply>=8; many top examples have an empty column): F1 0.062, AUROC 0.508. Nothing.
4. h8 (last move in col 3/6 + top of col 4 mine): F1 0.074, AUROC 0.527.
5. h9 (col4 = O,X,X stack at height 4, left side low): F1 0.071, P 0.19, R 0.04.
Stopped at 5/8 calls: every structural hypothesis gives AUROC ~0.5-0.56.

## Other observations
- Activation flips with perspective: in a continued game it is high on every ply where the first player is to move and near 0
  on the others, and decays as the board fills, while the board barely changes. Very context dependent: the same
  col-4 stack built in a fresh opening gives 0.05-2.8 depending on unrelated stones.
- 2-ply openings: never fires if either move is col 3 or col 6; fires for 0-4, 0-5, 4-1, 5-4 ... no clean rule.
- Top-band examples cluster in a few dev games (68230/68234/68236, 22280/22282, 7570/7572, 20145/20147).
## Steer
- Forcing max: lowers the model's favoured centre column (3 or 4) by 0.02-0.13 and spreads it to flank columns
  (5,4: col4 -0.09; 3,0: col4 -0.13; 4,6: cols 3/4 -0.07/-0.08, col2 +0.09). Zeroing a top example: cols 3/4 +0.03..+0.06.
## Synthesis
- 3,2,3,2,6,3,4,5,0,4,4,5,4,6 -> 8.511 (beats dev max 7.70); 3,2,3,2,0,3,4,5,0,4,4,5,4,6 -> 8.248; +0,1 -> 7.952.
## Conclusion
Low confidence: looks like a mixture / possibly a random direction. Best partial rule = h1, covering part of the top band.
