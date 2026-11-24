# U09 notebook (layer 5, pole -, threshold 0.866, dev max 84.4)

## Examples (40 across bands)
Top bands (7-9) all: column 2 holds three opponent stones stacked at its top with the cell above empty (must-block at landing of col 2). Lower firing bands (5-6) mixed, sometimes no col-2 pattern.

Hypotheses:
H1: vertical three (any side) on top of column 2, cell above empty.
H2: any must-block / threat at landing cell of col 2 (incl. horizontal/diagonal).
H3: generic vertical three in any column.

## act tests
- 3,2,3,2,4,2 (opp vertical three col2): 34.7. Same pattern in cols 0,1,3,4,5,6: 1.98, 0.30, -0.01, 0.33, 0.03, -0.02 -> column-2 specific (H3 rejected).
- Block it (…,2): 0.26. Column full with top three O (no cell above): 0.02.
- Horizontal three O on row 0 with hole at (0,2): -0.03/-0.13 -> H2 rejected.
- Three higher in column (rows 2-4 / 1-3): 30-45.
- My own vertical three in col 2 (I can win): 5-10 (fires, weaker). Opp three with last move elsewhere: 24-45 (last move not needed).

## score 1 (p1: vertical three on top of col 2, either side; level 9 opp / 5 mine)
F1 0.433 (P 0.962, R 0.279), AUROC 0.639. Simulation share nan (ceiling itself -607%: zero-ablation does nothing, metric ill-defined here).
Misses are weak firings (0.87-2.5), ~2/3 of firing set; diffuse, many with col 2 low/empty, no obvious single pattern.
act: 6,3,5,6,1 -> 0.98; 6,3,5,6,0 -> 0.03; 4,0,4,1,3,5,3 -> 1.29 vs ...,6 -> -0.02. Teacher often rates col 2 as bad there.
steer: forcing max sends col 2 to ~100%; zeroing changes nothing (blocking already certain). Effect = "play column 2".
Next (p2): add any four-threat (either side, any direction) at col 2's landing cell as weak firing.

## score 2 (p2 = p1 + any threat for either side at col-2 landing cell, level 3)
F1 0.484 (P 0.490, R 0.479), AUROC 0.732. FPs: horizontal must-blocks at col 2 with act < 0. Misses: vertical threes in OTHER columns (cols 1, 5) with weak act 1.5-3.
act: opp vertical three col 0/1 in opening ~1.0-1.1 (fires barely); col 5 ~0.03.
## score 3 (p3 = p2 + vertical three in cols 0/1)
F1 0.461 (P 0.376, R 0.596), AUROC 0.783. Worse F1; vertical threes elsewhere too unreliable.
Next p4: p1 + opponent must-block at col 2 landing only when opponent just played col 2.

## score 4 (p4 = p1 + their must-block at col-2 landing when last move was col 2)
F1 0.536 (P 0.725, R 0.426), AUROC 0.710. Misses include opponent's FRESH vertical three in col 1 (and col 0).
act: opp just made vertical three col 1: 1.06 / 2.15; col 0: 1.75; after I play elsewhere: -0.005 to 0.13; my own three col 1: -0.09.
Next p5: p4 + opponent just completed a vertical three in col 0 or 1.

## score 5 (p5 = p4 + opp fresh vertical three in col 0/1)
F1 0.499 (P 0.463, R 0.541). Worse: those positions often sit just under threshold (0.4-0.7). Reverted to p4.

## steer (3+ positions)
3,2,3,2,4,2 (act 34.7): zero -> no change (col 2 already ~100%). max -> no change.
4,0,4,1,3,5,3 (act 1.3): max -> col 2 from 0.00 to 1.00 (col 3 0.75 -> 0).
3,3,4,4,0,5 (act 0.0): max -> col 2 from 0.00 to 1.00 (col 3 0.94 -> 0).
Effect: strong "play column 2" push; ablation has no visible effect where it naturally fires (redundant with the block).

## synthesis
Best valid: 2,6,2,0,2 (66.0), 2,0,2,6,2 (65.2), 2,3,3,6,4,4,2,4,2 (65.8), 6,2,0,2,6,2 (63.1), 6,2,6,2,0,2 (62.4). None beat dev max 84.4.
(Several 80+ sequences found were invalid: they completed a four in col 2.) Higher-stacked threes are weaker; me-stones on the edges (cols 0/6) help.

## Final: p4. F1 0.536, simulation share nan (ceiling ill-defined). Confidence medium: strong core (vertical three on top of col 2) is clean and verified by minimal pairs; ~half of firing is weak, diffuse (0.87-3) and only partly explained.
