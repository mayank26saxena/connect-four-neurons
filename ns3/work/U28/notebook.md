# U28 notebook (layer 5, pole +, threshold 0.756, dev max 40.8)

## Examples
- Bands 7-9 (act 10-40): ALL have opponent (O) three stacked vertically in column 0 with empty cell above (must-block in col 0).
- Band 5-6 (0.8-4.8): mixed; many have last move col 0, other vertical threats (col 2, col 5), must-block/win cells in col 0.

## Hypotheses
H1: opponent open vertical three in column 0 (strong).
H2: weaker: opponent vertical three in cols 1,2,6; any opponent threat in col 0 landing.
H3: last move in col 0 generally (weak).

## act minimal pairs
- 2,0,6,0,5,0 -> 36.0; 2,0,6,0 (two) -> -0.3; blocked (+0) -> 0.07; my own three in col 0 -> -1.35.
- three in col 0 stays strong when last move is elsewhere (2,0,6,0,5,0,1,3 -> 25.5); elevated three (rows 2-4) -> 28.
- same vertical three in col 1: 1.29, col 2: 1.43, col 3: 0.67, col 4: -0.23, col 5: -0.47, col 6: 1.17.
- opponent horizontal three 1,2,3 with only threat at (0,0): 1.38 (weak fire).

## Score 1 (p1: vertical O-three in col 0): F1 0.485 P 0.98 R 0.32. Simulation share nan (perfect reader -139%; zero-ablation hurts nothing measurable?).
## Steer: forcing high pushes the move to column 0 (+0.85 on a quiet opening, +0.63 midgame); zeroing on a col-0 vertical threat moves 0.20 from col 0 to col 3.
## Score 2 (p2: + any must-block in col 0): F1 0.503 P 0.64 R 0.42. FPs: double threats (0,0)+(0,4), near-full boards.
Misses inspected: many are opponent VERTICAL threes in other columns (cols 1,2,5) mid-game (act ~0.8-1.3).
H3: any opponent open vertical three (weak), col 0 strong.
## Score 3 (p3: + any vertical O-three anywhere, level 3): F1 0.355 P 0.25 R 0.60. Other-column vertical threes fire only sometimes -> dropped.
act: horizontal threat completing at (0,0) fires weakly (0.9-1.4) only when it is the only must-block; with a second must-block at (0,4) -> -0.01.
## Score 4 (p4: vertical O-three in col 0, OR the only must-block is in col 0): F1 0.517 P 0.68 R 0.42 (best). FPs: late-game boards with a non-vertical col-0 block.
Other-column vertical threes re-tested in varied contexts via act: mostly < 0.4 -> not part of the rule.
Remaining ~58% of firing is weak (0.76-2) and heterogeneous (various must-blocks elsewhere, col 0 a plausible move); no clean pattern found.
Simulation share: nan for all programs (the perfect reader's recovery is negative: zero-ablating the unit is not measurably harmful on dev).
## Synthesis: best 6,5,2,0,6,0,2,0 = 38.7 (dev max 40.8); none beat dev max.
Decision: submit p4, confidence medium (strong part is a clean board pattern, overall F1 0.52).
