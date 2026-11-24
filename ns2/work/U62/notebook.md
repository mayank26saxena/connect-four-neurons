# U62 notebook (layer 2, pole -, threshold 1.013, dev max 8.975)

## Observations from examples
- Nearly every firing example: column 0 has height 3 (landing cell (3,0)) with an opponent stone on top at (2,0).
- Top band (5.5-9): col 0 = O,O,O (opponent vertical three, must-block at (3,0)), last move in col 0.
- Threshold band: col 0 = X,X,O / O,X,O / X,O,O with top O, last move often elsewhere.

## Hypotheses
H1: fires when heights[0]==3 and grid[2][0]==theirs; stronger with more O below, and if last move was col 0.
H2: about their threat at (3,0) (must-block) -- top cases.
H3: generic "opponent vertical three" -- REJECTED: OOO in col 1/3/6 gives ~ -0.1.

## act tests
- 3,0,3,0,4,0 (OOO col0) 1.09; +0 (X on top, h4) -2.7; col0 h4 O,X,O,O -8.3 (strong negative when col0 height 4).
- side matters: 3,0,3,0,4,0,1 (col0 now mine from mover's view) -0.07; then ...,4 -> 1.04.
- 1,0,1,0,2,0 3.1; 2,0,2,0,1,0 2.5: context in nearby cols adds.
- O,O h2 -> -0.6; X,O,O / O,X,O h3 in tiny positions -> negative (-0.6,-1.1), so mixed stacks need context.

## Score calls
1. p1 (h0==3 and (2,0) theirs): F1 0.636 (P 0.488, R 0.913), AUROC 0.942, sim share 0.50.
   FPs: mixed stacks (X,X,O / O,X,O) at ~0.1-0.8. Misses: col0 O,O,O already capped by X (h4/h5) in busy boards.
2. p2 (+ at least 2 theirs in col0): F1 0.616 (P 0.547, R 0.706). Mixed stacks are too often firing to drop.
3. p3 (core and (last move col0 or >=2 theirs)): F1 0.646 (P 0.536, R 0.814), AUROC 0.896, sim 0.50. BEST.

## More act findings
- Perspective: fires only on the mover for whom the col-0 top stone is the opponent's; alternates on/off as play continues elsewhere (XOO stack: 1.1, 2.5, 1.3, 1.9...).
- Higher bands (>2.5) nearly always last move = col 0 and O,O,O. Col 1/2 stones add (1,1,1,1,... prefixes push to 9+).
- Height-4 column 0 in small positions gives strong opposite (negative) activation.
- Mixed stacks are graded by context I could not pin down (col1 occupancy helps somewhat); likely ceiling for a simple rule.

## Steer
- XOO col0 (0,0,6,1,1,0): max raises col 0 from 0.34 to 0.52 (+18 pts), col 3 -10. Zero: small.
- 0,0,6,1,1,0,6,5: max col0 +9 pts; zero -2.
- Forced-block OOO position: no change (already 1.00 on col 0). Busy pos 19633: ~none.

## Synthesis: 1,1,1,1,3,2,2,2,0,6,0,5,0 = 9.74 (beats 8.975); 4 others 9.4-9.6.
