# U04 notebook (layer 2, pole +, threshold 0.525, dev max 16.75)

## Examples
Bands 7-9 (act 3-16): almost all = opponent has 3 stacked on top of column 0 with the cell above empty (must-block at top of col 0).
Bands 5-6 (0.5-2.5): mixed; many with 2 opponent stones stacked on top of col 0; others no obvious pattern.

## Hypotheses
H1: opponent's vertical three at top of column 0, cell above empty.
H2: graded by number of opponent stones on top of col 0 (2 -> weak, 3 -> strong).
H3: any must-block in col 0 (horizontal/diagonal) -- tested.

## act tests
- 2,0,5,0,6,0 -> 9.4 (O three in col0). Same pattern col1/col3/col6 -> ~0.0-0.2. Column-0 specific.
- 2,0,5,0,6,0,3,4 -> 8.0 (last move not in col0): depends on board, not last move.
- After the side owning the three is to move: -2.1 (needs to be THEIR three).
- Horizontal threat at (0,0) (O on 1,2,3 row0): -0.04. H3 rejected.
- Three O at top of a full col0 (no room): -1.3. Needs an empty cell above.
- 2 O on top of col0 with room: 1.8 (rows 2-3), 2.5 in dev ex.; 0.3 at rows 0-1; -0.9 rows 1-2 (ply 6).
- O three + I have an immediate win elsewhere: 5.4 (reduced but fires).

## Score log
- p1 (their 3-stack on top of col0, cell above empty): F1 0.492 (P 0.995, R 0.327), AUROC 0.663, sim share 1.46. Misses: weak 0.5-2.5 band, many with 2 of theirs on top of col0.
- p2 (+ their 2-stack h<=4, + my 3-stack): F1 0.336 (P 0.24). Low 2-stacks and my threes do not fire. Rejected.
- act: 2-stack of theirs fires only when it sits on rows 2-3 (col0 height exactly 4): 1.8, 4.7, 2.2; rows 0-1 0.3, rows 1-2 -0.9, rows 3-4 (no room) -1.3. My own 3-stack: -0.3, 0.4, 0.9.
- p3 (their 3-stack with room -> 9; their 2-stack on rows 2-3 with col0 height 4 -> 4): F1 0.682 (P 0.904, R 0.547), AUROC 0.773, sim share 1.53. Best. Remaining misses diffuse, near threshold.

## Steer
- 1,0,0,0,3,0 (act 4.7): max -> col0 +0.27 (0.07->0.34), col3 -0.23. zero -> ~no change.
- dev must-block pos (0,6,6,2,...,4,0): zero -> col0 1.00 -> 0.71.
- 0,4,6,4,...,3,0 (2-stack, 2.2): max -> col2 +0.18; zero no change.
- 2,0,5,0,6,0: already 1.00 col0, no change.
Effect: pushes the model to block at the top of column 0; partly redundant with other circuitry.

## Synthesis
6,3,0,0,6,0,4,0 = 17.21 (beats dev max 16.75); 6,3,0,0,6,0,5,0 16.57; 3,5,0,0,5,0,4,0 16.47; 6,5,0,0,3,0,4,0 16.39; 5,0,0,3,0,4,0 15.93.
Strongest: early game, me on bottom of col0, their three on rows 1-3.
