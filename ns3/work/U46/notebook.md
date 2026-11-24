# U46 notebook (layer 5, pole +, threshold 2.274, dev max 40.08)

## Examples
Bands 7-9 (act 10-40): almost all have the opponent with three stacked stones on top of column 0 (must-block at (3,0)/(4,0)/(5,0)), usually just played in col 0.
Bands 5-6 (2.3-9): mixed, many with last move col 0, some with no obvious col-0 feature.

## Hypotheses
H1: opponent has a vertical three on top of column 0 with the cell above empty (column-0 vertical must-block).
H2: any opponent playable threat at column 0 (incl. horizontal/diagonal).
H3: last move in column 0 generally.

## act minimal pairs
- 3,0,3,0,6,0 -> 22.0 ; same vertical three in cols 1-6 -> ~0 (col-0 specific)
- 3,0,3,0,6,0,6,5 (last move elsewhere) -> 10.3 (still fires; last move not required, but boosts)
- 0,0,3,0,3,0 (three at rows1-3 over my stone) -> 14.5
- my own vertical three in col 0 -> -0.17 (opponent's only)
- horizontal three to (0,0) (4,1,6,2,5,3) -> -0.06 : H2 rejected
- two stacked in col 0 -> ~0 ; three blocked by my stone on top -> 0.6
=> H1 favored.

## Scores
- p1 (opp vertical three on top of col 0, cell above empty): F1 0.465 (P 0.96, R 0.31), AUROC 0.65, sim share 0.35. Very clean core; misses are the weak tail (2.3-9).
- More act: diagonal must-block at (3,0) -> 2-4; my immediate win at (3,0) -> 9; horizontal threat at (1,0) -> 0.7. So "column 0 is the urgent move" generalises weakly.
- p2 (+ any playable win/block in col 0 at row>=2): F1 0.516 (P 0.67, R 0.42), sim 0.32. FPs are late games with col 0 almost full (rows 4-5).
- p3 (+ urgent rows 2-3 only, + opp just played to (2,0) with ply>=10): F1 0.500 (P 0.48, R 0.53), sim 0.65.
- p4 (fresh col-0 stone at row 1-2): F1 0.384, worse; reverted.
- p5 (fires = vertical three OR col-0 win/block at row 2-3; level adds fresh-(2,0) rung): F1 0.554 (P 0.82, R 0.42), AUROC 0.71, sim share 0.65. BEST.
- Weak tail (2.3-9) is diffuse: often the opponent just played into column 0 (minimal pairs: replacing that last move with another column drops 4.7 -> <0), and column 0 tends to be the engine's best move, but early-game versions of the same column-0 stacks do not fire. No clean board rule found.

## Steer
- 33.7 position (forced block): already 1.00 on col 0, no change.
- 574 (3.8): max -> col 0 0.12 -> 0.93; zero -> -0.05.
- 12778 (7.4): max -> +0.14 col 0; zero -> -0.11 col 0.
- 88274 (-0.19): max -> col 0 0.01 -> 0.45 (taken from col 4).
Effect: a "play column 0" vote.

## Synthesis
3,3,0,1,0,3,3,6,0 -> 40.44 (beats dev max 40.08). Others 38-39.
