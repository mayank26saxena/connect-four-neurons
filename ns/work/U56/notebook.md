# U56 notebook (layer 5, pole +, threshold 0.774, dev max 44.4)

## Examples
- Band 8-9 almost all: opponent (O) has an immediate win in column 6 (must-block in col 6), mostly a vertical three in col 6 just played (last move col 6), sometimes horizontal threat into (1,6).
- Band 5-6 (act 0.8-5): must-blocks in other columns (col 0, col 5, col 2...), some with no must-block at all.

## Hypotheses
H1: fires when opponent has a playable winning cell in column 6 (must-block in col 6). Level highest for vertical.
H2: fires for any must-block (weak for columns other than 6).
H3: mixture/edge columns.

## act tests
- 6,3,6,3,6 (O vertical three col6): 39.5. Same in col0: 2.7, col5: 1.3, col4: 0.97. -> column 6 specific, others weakly over threshold.
- Horizontal three O at row1 cols 3-5, (1,6) playable: 31.1; same with col6 empty (threat not playable): 1.96.
- Bottom-row O 3,4,5 with (0,6) must-block: -0.15 (!), with double threat (0,2),(0,6): -7.7. Bottom-row col6 must-block does not fire. 
- O row1 3-5 must-block (1,6) while I also have an immediate win: 5.1 (reduced).
- 6,3,6,3,6,2,1 (col6 vertical three left open for 2 plies, not just created): 3.5 vs 39.5 when just created. Freshness matters a lot for strength.
- Other-column verticals just created: col0 2.7, col1 1.7, col2 0.36, col3 -0.1, col4 3.9, col5 1.3.

## Dev metric
(call 1 was an accidental duplicate run of p1)
- p1 any col6 must-block: F1 0.510 (P 0.71, R 0.40), AUROC 0.70. FPs include bottom-row (0,6) blocks; misses are weak (0.8-4) firing on other-column threats and miscellany.
- p2 col6 must-block row>=1 OR any vertical must-block: F1 0.473 (P 0.36, R 0.70).
- p3 col6 must-block row>=1 created by last move: F1 0.468 (P 0.89, R 0.32). Very precise for the strong core.
- p4 any last-move-created must-block row>=1: F1 0.382 (P 0.27, R 0.64).
- p5 col6 must-block row>=1 (any age) OR just-created vertical three in cols 0,1,4,5: F1 0.528 (P 0.44, R 0.66), AUROC 0.82. BEST.
- p6 like p5 but col6 only if just created: F1 0.494.
Simulation: tool reports ceiling negative (-19.7%), share nan: not meaningful for this unit.

## Steer
- forcing max on neutral positions (3,3,4,2,1 and 2,3,4,4) moves ~95% of probability to column 6. Zeroing changes nothing (positions where it fires already play col 6 with p=1; redundant).

## Synthesis
Best 6,3,6,3,6 = 39.5 (dev max 44.4); none beat dev max.
Conclusion: strong core = "opponent just made a playable win in column 6 (mostly vertical three in col 6), must block at col 6". Long weak tail (0.8-5) on other must-blocks, especially fresh verticals in edge-ish columns, plus noise. Medium confidence.
