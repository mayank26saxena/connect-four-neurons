# U42 notebook (layer 5, pole +, threshold 0.718, dev max 56.2)

## Examples (bands 0-9, ~90 seen)
- Bands 7-9 (act 20-56): essentially all have a must-block (opponent immediate win) at a cell in COLUMN 0, mostly
  the opponent just played column 0 making 3 O stacked vertically. Some are diagonal (pos 100266, last col 2, 20.9) or
  horizontal (pos 29087, (3,0), 14.8).
- Band 5-6 (0.7-14): must-blocks in other columns (col 6, col 2, col 5) give weak firing ~1-6; also some with
  two O stacked in col 0 after last move col 0 (~10) and some with nothing obvious.

## Hypotheses
H1: opponent has an immediate (playable) win in column 0.
H2: last move col 0 making a vertical three (subset of H1, strongest).
H3: generic must-block anywhere (weak part of firing).

## Minimal pairs (act)
- 3,0,3,0,4,0 vertical O three in col0: 29.1. Same in col 6: 1.5; col 1: -0.1.
- 5,0,5,0,4,0: 34.4. 0,0,3,0,3,0 (threat at row 4): 29.9. threat at row 5 (0,1,0,0,3,0,3,0): 23.2
- then X plays 4 (ignores), O plays 6: threat still there but last move col 6: 6.85 -> recency of col-0 move matters.
- horizontal O at 1,2,3 row 0, threat (0,0) only: 2.07 / 1.2 (fires weakly).
- 3,0,3,0,0,0 (col0 O,O,X,O no threat): -0.13. When it is the threat-owner's turn (my win, not theirs): 0.38.

## score 1 (p1: any must-block in column 0; level 9 if last col 0): F1 0.526 P 0.682 R 0.429 AUROC 0.711; sim nan (ceiling negative)
FPs are mostly col-0 must-blocks that are horizontal/other lines near top of full boards.

## More minimal pairs
- diagonal threat at (3,0) via O at (2,1),(1,2),(0,3) [down-right diag]: 16.7; break diagonal: -0.2
- horizontal row-1 threat at (1,0) (O at 1,2,3 row 1): -0.01 (NOT firing)
- up-right diagonal threat at (0,0) via O (1,1),(2,2),(3,3): 0.04 (NOT firing)
- two O stacked on col 0: ~0.1; three: ~30.
=> H4: must-block in column 0 made by a vertical three or a down-right diagonal (cells (r-1,1),(r-2,2),(r-3,3)).

## score 2 (p2: col-0 must-block via vertical three or down-right diagonal): F1 0.534 P 0.910 R 0.378 AUROC 0.688
Precision fixed; recall limited by the many weak firings (0.7-19).
## Steer: raises column 0 (zeroing at a vertical col-0 threat: col0 1.00->0.90; at pos 92285 0.90->0.59; max on 3,3,2,2: col0 +0.32).
Teacher scores in mid-band misses often make column 0 the best/only move -> unit looks like "column 0 is urgent".
## More act
- my own vertical three in col 0 (my win): 0.45-0.94 (weak)
- their col-0 vertical threat two plies later (other moves in between): 13.3 (decays from 29)
- vertical threats in other columns: col5 3.3, col2 0.25/1.5, col6 0.6-1.5, col3/col4 ~-0.3. inconsistent, weak.
- dev examples: horizontal col-0 threat at row 3 fires (6.6, 8.7), at row 1/2 does not (0.0, 0.35).
- my win at (3,0) after opponent just played col 0: 4-11 in 3 dev examples.

## score 3 (p3: + horizontal row>=3 col-0 threat + my col-0 win after their col-0 move): F1 0.549 P 0.787 R 0.422 AUROC 0.709
Small gain; my-win clause adds FPs (late-game boards). Misses are weak (1-2) vertical threats in other cols etc.

## score 4 (p4: graded; drop my-win clause as firing, weak levels for other must-blocks): F1 0.548 P 0.851 R 0.404 AUROC 0.834
Chosen as final. Sim share is nan for every program (tool reports a negative perfect-reader ceiling, -42.9%).
Remaining misses: diffuse weak activations (0.7-3): vertical threes in other columns, positions where col 0 is the
engine's best move without an immediate threat. No clean single rule found; stopped at 4 score calls.

## Synthesis (hill-climb with act on mutated dev sequences; validity checked locally for no fours)
- 1,1,6,3,1,4,4,5,2,4,4,3,1,1,0,3,3,0,2,3,5,0,5,5,1,4,3,0 -> 57.31 (beats dev max 56.16)
- 1,1,6,3,1,4,4,5,2,4,4,3,1,1,0,3,3,5,5,0,2,3,5,0,5,5,1,4,3,0 -> 56.43 (beats)
- 6,0,5,0,6,0 -> 37.0 (minimal clean case)
