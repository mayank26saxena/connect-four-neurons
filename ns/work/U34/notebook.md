# U34 notebook (layer 4, pole +, thr 1.433, dev max 21.665)

## Observations (ex1 + band 9 seed 2)
- Every firing example has column 5 EMPTY (or low) with neighbours occupied.
- 39634 (act 15): facts show their only threat cell (1,5), directly above empty landing (0,5); teacher says col 5 = -985.
- 55159 (17.3): row1 O O . O -> their threat (1,5) too.

## Hypotheses
H1: opponent has a win cell directly above column 5's landing cell (playing 5 gives them the win).
H2: same but any column (poisoned landing cell anywhere).
H3: just column 5 empty with cols 4 and 6 occupied (shape).
## call3 h5 (opp open windows through empty col5 cells, heights5==0, score>=3): F1 0.497 P0.395 R0.671 AUROC 0.819 sim 0.14
## call4 h7 (simulate me at col5 landing, them above: new win cells / immediate win above; heights5<=1; no forcing moves): F1 0.482 P0.43 R0.548 AUROC 0.762 sim 0.34. Misses: sparse early boards with col5 empty.
## call5 h8 = h5 opp_score + 2*danger(h7), heights5==0, no forcing exclusion, thr>=5: F1 0.615 P0.541 R0.713 AUROC 0.847 sim 0.40
## call6 h9 = h8 but opp windows only through (0,5),(1,5); zero if (1,5) not their win and [(2,5) their win or any immediate win/must-block]: F1 0.695 P0.812 R0.608 AUROC 0.802 sim 0.51
## call7 h10 = h9 + my threat at (1,5) fires + thr 4: F1 0.611 P0.566 (worse; reverted to h9)
## call8 h11 = h10 with thr 5: F1 0.621. my-(1,5)-threat rule hurts. FINAL = h9.

## Steer
- Max on non-firing 3,0,1,4,1,3,3,3,0: col 5 0.16 -> 0.00, mass to 4/6/0/2.
- Zero on firing positions: col 5 stays ~0 (other circuits also suppress it); prob moves e.g. col3 -0.23 / col6 +0.34, col3 -0.20 / col1 +0.20, small elsewhere.
## Synthesis: best 20.26 (1,3,4,3,3,3,1,1,4,4,4,6,3,6); none beat dev max 21.665 (greedy pair search from top dev games).
