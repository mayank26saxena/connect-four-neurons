# U43 notebook (layer 3, + pole, thr 1.499, dev max 7.80)

## Examples (60+ viewed, bands 0-9)
- Every firing example I checked (~45) has column 6 at height exactly 3 (landing cell (3,6) = 4th row of right edge).
- Top examples mostly mid/late game (ply 17-39), mostly odd ply (me = second player).
- Band 4 near-misses (27477, 146821) also have col6 height 3 -> modulated by something else.

## Hypotheses
H1: fires iff heights[6] == 3 (landing cell (3,6)).
H2: H1 modulated by ply / side to move (odd ply higher).
H3: H1 modulated by threats at (3,6) / pieces around it.

## act tests
- Game 0,3,4,4,4,3,3,4,4,4,3,6,3,3,6,6 + X: X=0 5.0, 1 2.7, 2 1.06, 5 1.29, 6 (col6 -> 4) -1.73.
- Game ...,6 + X at ply 31: X=0/2/5 ~6, X=6 -> -2.5. Col6 height 3 is the switch.
- Early-game col6=3 (6,6,6 then few moves) is strongly negative; fills of central cols 3,4 raise it (3x6+4x6 then 6,6,6,0,0 -> 5.1; cols 0,1 filled instead -> 0.5).
- Last move into col 6 often suppresses (0,6 -> -1.8), but not always (several misses had last_col 6).
- Parity (odd ply) shows up in single games but did not generalise (p2).

## Dev metric
1. p1 h6==3 & last!=6 & ply>=14: F1 0.565 (P .476 R .696) AUROC .836, sim share 0.75
2. p2 h6==3 & odd ply & ply>=13: F1 0.480, sim 0.80 -> parity dropped
3. p3 h6==3 & h3+h4>=9: F1 0.589 (P .618 R .564), sim 0.79; misses where other cols are full
4. p4 h6==3 & >=3 of cols 0-5 have height>=4: F1 0.657 (P .533 R .858) AUROC .917, sim 0.80  <- best F1
5. p5 = p4 + last_col!=6 when exactly 3 tall: F1 0.647, sim 0.83
6. p6 weighted (central) tall count: F1 0.642, sim 0.84 -> no gain, dropped (overfit)
7. final = p4 fires + p5 level: F1 0.657, AUROC .917, sim share 0.83

## Steer (small, ~<=10 points, on col 6, sign position-dependent)
- 12884 (act 5.0): zero -> col6 -6, col0 +5. 
- game2 ply31 (5.9): zero -> col6 +10 (col0/col5 -4/-5).
- 14089 (2.3): max -> col6 +7. 30939 (2.6): max -> col6 -3.

## Synthesis: suffix search from game2 prefix; best 7.315 (below dev max 7.80).
