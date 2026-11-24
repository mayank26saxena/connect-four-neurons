# U30 notebook (layer 2, pole -, threshold 0.848, rate 3%, dev max 2.123)

## Observations (examples, histograms)
- Firing positions skew early (band 9 median ply 11 vs ~21 in band 0). Col 3 full is rare in firing; cols 2/4 often empty.
- Opponent stones in cols 2 and 4 are depleted among firing (band 9: 43/60 have <=1 O there vs ~11/60 in band 0).
- ~18% of firing has a must-block (often an O vertical three in col 1 or 3), similar to non-firing rate.
- Single-feature histograms (last col, last row, parity, stack length) show nothing distinctive.
- steer --to zero: changes < 0.02 on 4 top positions. Effect ~none.

## Minimal pairs
- Within a game the unit alternates by ply (fires only for one side to move): it depends on the board as seen by the mover.
- Base 5,0,5,3,3,5,3,6,2,0 (2.02): substituting MY earlier moves barely matters; substituting THEIR moves matters.
  Low when O lands at (1,2), (2,0) [O vertical three], (3,3) [O capping my XX in col 3]. O on row 0 elsewhere fine.
- 95070 1,3,0,3,4,0,1,+c: O at (3,3) (vertical three) 2.12; O(1,4) 0.15, O(2,0) 0.05, O(2,1) 0.59, O(0,5) 1.18.
- Conflicting: O capping my pair sometimes kills, sometimes not. Looks distributed.

## Hypotheses
H1: opponent has few stones in columns 2 and 4 (esp. above the bottom row), early/mid game.
H2: opponent vertical three / must-block (subset only).

## Scores
- p1 (ply<=20, no O at (1,2),(2,2),(1,4),(2,4)): F1 0.096, P 0.055, R 0.40, AUROC 0.595, sim share 0.02.
- p2 (opponent vertical three with open top): F1 0.072, AUROC 0.526. Vertical-three motif in top examples is not general.
- p3 (early + few opponent diagonal/horizontal links + col3 odd height - O in cols 2/4): F1 0.074, AUROC 0.526.
- p4 (cell cues from single-cell histograms; them at (1,3),(0,6),(0,1),(2,1),(2,5) +, them at (1,2),(2,2),(1,4),(2,4),(1,5) -, me (1,1),(1,5) +, me (0,1),(0,2) -, col3 full -, late -): F1 0.115, P 0.08, R 0.20, AUROC 0.566, sim 0.04. BEST.

## More minimal pairs
- Strongly left-right asymmetric: mirror of 95070 (2.12) gives -0.03; mirror of 5,0,5,3,3,5,3,6,2,0 gives 1.22.
- Same column heights, different colourings: 6/8 still fire -> height profile matters partly, colours too.
- In 5,0,5,3,4,5,3,6,2,0 (2.19) my stack X,X in col 5 capped by O is critical (moving either of my col-5 stones -> ~0.5), yet the same col-5 pattern alone in small positions does not fire. Effects of single stones are strongly context-dependent (O capping my stones lowers it in some boards, raises it in others).
- Sweep-style exploration was denied; stuck to targeted pairs.

## Steer
- --to zero on 4 firing positions: changes <= 0.02. --to max on 3 non-firing: changes <= 0.05 (one case +0.05 col 3, -0.05 col 1). Effect essentially none.

## Conclusion
Looks like a diffuse/mixed direction: early-to-mid game, opponent stones low and away from cols 2/4 rows 1-2, many context-dependent stacking interactions. No clean rule found. Confidence low.
Synthesis: 5,0,5,3,4,5,3,6,2,0 = 2.187 (beats dev max 2.123).
