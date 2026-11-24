# U39 notebook (layer 1, pole -)

## Observations
- Top examples: plies 8-15, stones concentrated in columns 2-3 (tall, h 3-5), column 4 (and 5,6) nearly empty. Some with col3 empty and cols 1-2 tall.
- Cell tally (500 firing vs 500 non-firing examples): col4 rows>=1 almost always empty when firing; cols 2-3 filled up to row 3.
- Height histogram: firing col3 h in {4,5} 63% (or 0: 17%), col4 h<=2 86%, ply 8-15 ~80%.
- Order of moves irrelevant (board-state). Colors matter only mildly.
- steer: negligible effect on move probs (<0.01).

## Hypotheses
H1: column 3 tall (4-5, not full) next to column 2 built up, with column 4 low (cliff on right of center tower).
H2: generalized: two adjacent tall columns (c, c+1 for c in 1..2) flanked by low columns.
H3: just ply 8-15 + concentration (weak).

## Minimal pairs (act)
- 3,3,3,3,2,2,2,2,0 = 1.19; add col4 stones: 0.89, 0.79, 0.38 (1,2,3 stones). col1 1 stone 0.61, 3 stones 0.06.
- col3 h5 alone (3,3,3,3,3) 0.09; + col2 h4 -> 1.31; + col4 h4 instead -> 0.07; col3 full -> -0.7.
- 3,3,2,2,0 (both h2) -0.36; 3,3,3,2,2,2,0 (h3) 0.40; h4 1.38.

## Dev metric log
- call 1+2: p1 (h3 in 4-5, h2>=2, h4<=2). Accidentally scored twice (ran the command twice). F1 0.210 (P 0.155, R 0.325), AUROC 0.635, sim share 0.05. Too broad.
- call 3: p2, hand-weighted score (h3 4-5 +2, h3 1-3 -2, full -3; h2>=3 +1; penalties for stones above row 0 in col4, above row 1 in cols 1/5/6; X at (0,5) +1, O at (0,5) -1, O at (0,1) -1), fires if >=2. F1 0.390 (P 0.408, R 0.373), AUROC 0.678, sim share 0.15. BEST.
- call 4: p3 (removed col1 penalty, added h3==0 bonus, tighter right penalties, threshold 3). F1 0.292, AUROC 0.617. Worse.
- call 5: p4 (p2 + col0>=2 bonus, h3==0&h2>=3 bonus, h3==3 only -1, col2 full -2), threshold 3: F1 0.357 (P 0.475, R 0.286).
- call 6: p5 = p4 at threshold 2: F1 0.387 (P 0.339, R 0.451), AUROC 0.712, share 0.14. Same level as p2.
Misses include late-game boards with a deep empty well next to full columns (e.g. col4 empty between full col3/col5), and col3-empty boards with tall cols 0-2. Looks like a graded sum of many column-height/cell terms (layer 1): a mixture. Stopped spending calls.

## More minimal pairs
- col2 X,O,X,O alone (2,2,2,2) -0.64; add ANY one opponent stone (flip side to move, so col2 reads O,X,O,X) -> +0.3..0.8. Colours/side-to-move matter.
- with col2 h4 + (0,6) stone, varying h3: 0:0.67, 1:-0.13, 2:0.30, 3:0.56, 4:1.54, 5:1.00. h3 = 4 best, 1-2 worst.
- stones added in col1, col5, col6 (above bottom) lower it; col0 stones raise it slightly; col4 stones lower it.
- top dev example (cols 1-2 height 5, col3 empty): any substitution putting a stone in col3 roughly halves it.

## Steer
5 positions, to max and to zero: change in move probabilities <= 0.03 everywhere. No measurable effect.

## Final
Submitted p2 (F1 0.390, share 0.15), confidence low. Synthesis: 0,6,3,3,2,3,3,5,3,2,0 = 2.952 and 0,6,3,2,2,3,3,5,3,2,0 = 2.679 beat the dev max of 2.419 (found by hill-climbing with act).
