# U37 notebook (layer 2, pole -, threshold 1.732, dev max 6.614)

## Examples
- ~19/20 firing examples in bands 5-9 have column 2 at height exactly 2 with an opponent (O) stone on top at (1,2), cell (2,2) empty.
- Last move is very often column 2 (opponent just landed at (1,2)); band 9 dominated by last_col==2.
- Non-firing near-threshold (band 4) also includes col2 height 2 with O on top (1.2-1.3), so not sufficient alone.

## Hypotheses
H1: fires iff heights[2]==2 and grid[1][2]==O (opponent stone at (1,2), (2,2) empty).
H2: H1 strengthened when the last move was that stone (last_col==2, last_row==1).
H3: depends also on neighbours (e.g. (1,3)/(1,1) mine rather than theirs).

## act tests
- 0,4,1,4,3,2,3,4,4,2: 4.96 (O just landed at (1,2)); +move 6 elsewhere: 1.89; then my stone at (2,2): -3.79 -> (2,2) must be empty.
- 4,3,3,1,1,0,2,2: 4.80; variant 4,3,3,1,1,0,2,6,2 (col2 = O,O with opponent just playing there, but (1,1),(1,3) theirs too): 0.67 -> neighbours matter (H3).
- 3,2,4,2: 0.95 (col2 O,O, early game); 2,2 alone -0.41 (height 2 but colour pattern ...).

## Score calls
- call 1/2 (p1, H1 gate only; call 1 wasted by re-running the same file): F1 0.593 (P 0.433, R 0.939), AUROC 0.950, sim share 0.53.
- call 3 (p2, hand-weighted flanks + early-game penalty): F1 0.483 (P 0.557, R 0.427). Early-game penalty and O-flank weights wrong (misses e.g. 22458 ply 5 at 2.69, 41271 with O at (1,3) at 4.79).
- more act tests on base 3,0,6,4,6,0,6,6,3,2,2 (4.79): any two extra moves drop it to ~3 (recency of the col-2 stone matters ~1.5-2); O at (2,3) drops to 1.35; X at (2,3) 3.28; O at (0,1) 3.67. On base 4,3,3,1,1,0,2,2: O at (3,3) above my (2,3) -> 1.85, O at (3,1) -> 2.41, far stones ~no effect.
- call 4 (p3, last_col bonus, O(2,3) penalty, X flank bonus, thr 1): F1 0.531 (P 0.504, R 0.561).
- call 5 (p4, gate + sum over 6 neighbours of (2,2) mine +1 / theirs -1, +1 if last move col 2, -1 if ply<6, thr >=1): F1 0.587 (P 0.598, R 0.577), AUROC 0.783, sim 0.54.
- call 6 (p5 = p4 with thr >=0): F1 0.601 (P 0.468, R 0.838), AUROC 0.904, sim 0.54. BEST -> submitted.

## Steer
Effects tiny: zeroing at 3 firing positions moves col 2 by -0.01 to -0.03 and col 3 by +0.01 to +0.05; forcing to max moves <=0.01. Weak push toward playing column 2 (on top of the O).

## Synthesis
Best 6.08 (4,3,3,1,1,6,1,6,3,6,1,0,4,0,2,2): opponent just stacks O at (1,2) on my X, my stones at (1,1),(1,3),(2,1)... ; all below dev max 6.614.

## Conclusion
Core gate is clear (recall 0.94): opponent stone on top of a 2-high column 2, (2,2) empty. Magnitude graded by surroundings of (2,2) and recency; I could not find a clean rule for which gate positions cross threshold (precision ~0.45-0.6). Medium confidence.
