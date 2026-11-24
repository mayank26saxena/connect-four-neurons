# U50 notebook (layer 5, pole -, thr 1.613, rate 3%)

## Observations
- Top band (12-30): nearly all have MY threat cell in column 6, often from horizontal XXX at cols 3-5 (rows 1-4), (r,2) blocked, col 6 low.
- Fires on side-to-move only (alternates on/off in 92783 game as turn flips).
- Lower firing bands are messy: vertical threes, open horizontal threes, even no threats.
- Row-0 minimal pairs: X at 2,3,4 with (0,5) open fires (5); blocked at (0,5) no. X at 3,4,5 fires only when both (0,2),(0,6) open. X at 1,2,3 never fires.
- Vertical own three fires for col 0 and 5 only; their vertical three in col 2 fires. Odd column selectivity.

## Hypotheses
H1: I have a threat cell in column 6.
H2: horizontal open/half-open three pointing right.
H3: unit is a mixture / random direction.

## Tests (act minimal pairs)
- Row-1 my XXX at cols 3-5, col 6 empty, me to move: 7.7. (1,2) blocked by O: 5.45. (1,6) blocked by O: 0.2. Both blocked: -0.3.
- Same three as opponent's (me must block): -0.08. Unit only fires when the side to move owns the three.
- Row-1 XXX at cols 2-4 (both ends open, unplayable): 0.1. XXX 4-6: 1.8. Diagonal three to (3,6): -0.1. So column 6 end of a 3-5 horizontal is special.
- Row 0 is different: 2-4 open threes fire (either colour), 3-5 needs both ends, 1-3 never.
- O stone right above the middle of my three ((2,4)) kills it (0.7); my stone there boosts it (11.6). O at (2,3): 2.1.
- Second player version also fires (3.7).

## Scores
- p1 my threat anywhere in col 6: F1 0.252 (P .19 R .36), sim share 0.30
- p2 my XXX at cols 3-5 with (r,6) empty, not undercut by their threat at (r-1,6): F1 0.231 (P .29 R .19), sim 0.20
- p3 any threat (either side) in col 2 or 6: F1 0.128 (R .61)
- p4 any horizontal threat of mine: F1 0.142 (P .08 R .59)
- p5 = p2 OR opponent has 2+ immediate wins: F1 0.283 (P .31 R .26), AUROC .62, sim 0.20  <- best
- p6 col-6 threat mine and none of theirs in col 6, OR lost: F1 0.259, sim 0.03
- p7 = p5 minus O-above-middle exclusion: F1 0.241 (lost recall)

## Steer
- Top example 92783: zeroing drops col 6 (the winning move) from 0.51 to 0.28.
- Forcing max raises col 6: +0.18 (3,2,4,5,2,3), +0.83 (30264), +0.30 (0,1,2,3,4,5,6,0); once raised col 2 (+0.11, 3,3,4,4).

## Conclusion
The top of the range is clear (my horizontal three in cols 3-5 aiming at an open column-6 cell, side to move). Below that the unit
fires on many other threat patterns with odd column selectivity, and the best rule only reaches F1 0.28. Confidence low.

## Synthesis
Built from dev game 122837 plus continuations; best 29.47 (dev max 29.69). Did not beat it.
