# U70 notebook (layer 2, pole -, threshold 1.829, dev max 10.199)

## Examples (40 + 12 at band 5)
Nearly every firing position: column 3 (center) has exactly 3 stones and the top one (row 2) is the opponent's (O).
Strongest when O just played there (last_col==3) early in the game.

Hypotheses:
H1: heights[3]==3 and grid[2][3]==THEIRS.
H2: last move was opponent into col 3 landing at row 2 (subset of H1).
H3: generic "opponent stone at center row 2/3" (any height).

## Minimal pairs (act)
- 3,3,3 -> 6.7 fires; 3,3,3,3 (top mine) -> 0.23; 3,3 (2 stones, top theirs) -> -2.96. Height 3 + top theirs is key.
- 3,2,3,3 = 8.57; after my reply 0 (top becomes... still theirs but now it's opponent's view: top mine) 0.02; after their 0 again: 2.79.
- Non-center columns (4,4,4; 2,2,2) do nothing. 4 stones in col 3: off.
- Activation decays with plies since the col-3 stone: 3,2,3,3 + 2 plies elsewhere 2-4.4; +4 plies 1.2-1.9.

## Score calls
Calls 1-2 (prog1 scored twice, second only to re-read the header): prog1 H1 heights[3]==3 & grid[2][3]==theirs: F1 0.803 (P 0.675 R 0.991), AUROC 0.988, sim share 1.06.
Call 3: prog2 H1 & col-3 stone played within last 3 plies: F1 0.886 (P 0.839 R 0.938), AUROC 0.966, sim share 1.07.  <- best
Call 4: prog3 same with <=5 plies: F1 0.859 (P 0.771 R 0.970). Keep prog2.
Misses of prog1: mostly col 3 with 4 stones where row 2 theirs, row 3 mine just placed (weak firing ~2).

## Steer
Zeroing at top positions: changes <= 0.08. Forcing max: lowers the model's favorite (col 2 by 0.17-0.25 in two positions), raises col 3/4 a bit; small, inconsistent.

## Synthesis
3,4,6,6,3,3 9.87; 3,1,6,6,3,3 9.66; 3,6,6,3,3 9.54; 3,1,3,3 9.42; 3,6,6,6,1,3,3 9.20. None beats dev max 10.199.
