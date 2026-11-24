# U33 notebook (layer 2, pole +, threshold 0.521, dev max 8.036)

## Examples (band 0-9, ~70 viewed)
Top bands dominated by: opponent (O) has 2-3 stones stacked on top of column 6 (rightmost), often vertical three (must-block (3,6)).
Secondary: column 3 / 2 with X,X,O stacking; early-mid game, low boards.

## Hypotheses
H1: opponent's stones stacked at the top of column 6 (run >=2), me to move.
H2: generic "opponent vertical stack capping a column" (any column).
H3: X stones in center + O stack col 6 (open-row threat context).

## act tests
- 6,5,6,2,6 (O three in col6) 3.6; at 3 moves (O two in col6 but X just... ) 0.06.
- x,6,y,6 with X in cols 2-4: 3-4.5 fire. X at 0,1 : -0.64 (no fire!). X at 0,5: -0.1. X at 0,2: 2.4. X at 1,1: 1.28.
- O stack col6 only fires when O just moved (me to move); after X moves (O to move) -> negative.
- Col 0 OO stack with X 3,4: 0.32 (no); col2 OO: 0.65; col 6 is special.
- col3 XXO alone (without col6 OO) ~0.1; with col6 OO 3.6. 4,3,2,3,3 1.48 (no col6 stones) - exception.
- 0,6,1,6 = -0.64 vs 0,6,2,6 = 2.4: something about X in col 0+1 suppressing.

## Score calls
- call 1 (accidental duplicate of call 2, same program p1).
- call 2 p1 (opp top-run >=2 in col 6): F1 0.166 (P 0.119, R 0.273), AUROC 0.604, sim share 0.01. Many late-game FPs.
- call 3 p2 (p1 + ply<=16): F1 0.214 (P 0.281 R 0.172), AUROC 0.579, sim 0.04.
- call 4 p3 (column-weighted opp vertical pairs, any column, ply fade): F1 0.201 (P 0.137 R 0.381), AUROC 0.652, sim 0.05.
- call 5 p4 (bottom-row template: col6 O stack + cols 1,5 empty + (0,6)=O + (0,2)=O + (0,3)=X, ply fade): F1 0.268 (P 0.49 R 0.18), sim 0.09.
- call 6 p5 (p4 + penalty (0,3)=O + bonus for O pair at top of col 0/2, threshold 3.5): F1 0.306 (P 0.35 R 0.27), AUROC 0.629, sim 0.10. BEST.

## More act findings
- Strongly context-dependent: same O stack in col 6 gives 4.5 (X at 2,3) vs -0.64 (X at 0,1). O at (0,3) suppresses (3,3,6,2,6 -0.17 vs 2,2,6,3,6 5.3).
- Fires only on my turn right after O stacked; after my reply it goes negative.
- Count comparisons (160 firing vs 160 low-band heads): firing positions have cols 1 and 5 empty (0.53/0.62 vs 0.14/0.17), O at (0,6), O at (0,2), X at (0,3), mostly ply <= 12.
- Looks like a distributed early-game bottom-row/col-6 pattern, not one clean concept.

## Steer
Max/zero on 7 positions: changes <= 0.07 in any column (one +0.07 to col 3); mostly 0.00. No measurable effect.

## Synthesis
0,3,2,2,6,3,6,0,6 = 9.05; 2,3,0,2,6,3,6,0,6 = 8.97; 2,3,6,2,6,0,6 = 8.77; 2,3,6,2,6,3,6 = 8.63; 2,3,6,3,6,2,6 = 8.59 (all beat dev max 8.04).
Recipe: O vertical three in col 6 + O at (0,2), X at (0,3)/(1,2)/(1,3), cols 1 and 5 empty.

## Conclusion
Confidence low (best F1 0.31). Core: opponent stacking in column 6 in the opening, modulated by bottom-row layout.
