# U13 notebook (layer 4, pole +, threshold 0.556, dev max 33.2)

## Examples (bands 0-9, ~85 looked at)
- Bands 7-9 (act 4-33): almost all = opponent has three stacked in column 0 with the cell above empty (must-block in col 0), usually last move col 0.
- Bands 5-6 (act 0.56-1.7, about 2/3 of firing positions): mixed, many early-game positions (e.g. 1,4,3; 3,3,1), no obvious pattern. Empty board = 0.512 (just below threshold).

## Hypotheses
H1: their vertical three in col 0, top empty.
H2: any must-block in col 0 (incl. horizontal/diagonal).
H3: weak firing = some early-game / generic background.

## Minimal pairs (act)
- 3,0,4,0,3,0 -> 17.4; same in col 6 -> -0.08; col 2 -> -0.05. Column-0 specific.
- 3,0,3,0,6,0,6,5 (their col-0 three, last move elsewhere) -> 14.9: last move not required.
- horizontal threat at (0,0) (O at 1,2,3) -> 0.24: H2 rejected, vertical only.
- blocking it (add X on top) -> -1.76.
- my own vertical three in col 0 -> 0.95 (weak fire).

## Score calls
1. v1 (their col-0 vertical three, cell above empty): F1 0.442 (P 0.990, R 0.285), AUROC 0.642, sim share 0.74. Only 6 FPs. Misses (1438) are almost all weak 0.56-2 activations with no visible pattern.
2. v2 (their top-2+ stacked in col 0): F1 0.214 (P 0.153). Rejected: two stacked fires only sometimes (3,0,0,0,3,0 -> 2.1 but 0,3,0,0,4,0 -> -1.8).
3. v3 (v1 OR my own col-0 vertical three; level 9 for theirs, 6 if I also have an immediate win, 1 for mine): F1 0.452 (P 0.975, R 0.294), sim share 0.84. FINAL.

## Weak band
160 sampled band 5-6 positions: spread over all plies and last-move columns; col-0 top contents not distinctive. Treated as diffuse background; not described.
Extra pairs: 1,0,1,0,1,0 (I have an immediate win in col 1) -> 8.3 vs 2,0,2,0,2,0 -> 18.8: own win lowers it. Full col 0 -> ~0. Four stacked (terminal) -> ~43.

## Steer
- 3,0,4,0,3,0 to zero: no change (block in col 0 still 0.99). 4,1,6,...,0 (act 13) to zero: no change. Ablation is redundant.
- 3,3,2,4,2,2 to max: col 0 +82 points (from 0.01 to 0.83), col 1 -59.
- 3,3,4,2 to max: col 3 -28, cols 2/4 +11 each; 6,3,6,3,3,2,6 to max: no change (col 6 block stays 1.00).
Effect: when forced high it can push the move toward column 0 (blocking), but inconsistently; zeroing it does not matter.

## Synthesis
Best 30.9 (0,5,0,0,6,0,6,5,5,0): their three at rows 2-4 of col 0, my stones far right. Below dev max 33.2. Higher stacks and my stones away from col 0 raise it.
