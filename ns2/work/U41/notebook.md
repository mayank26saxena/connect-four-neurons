# U41 notebook (layer 3, pole +, threshold 2.007, dev max 15.9)

## Observations (examples bands 0-9)
Top examples nearly all have a "well": a low/empty column (very often col 4, else col 2, sometimes 6) flanked by much taller neighbours (col 3 and col 5 at height 4-6).

## Hypotheses
H1: fires when some column c has min(h[c-1],h[c+1]) - h[c] >= 3 (a deep well), strongest for col 4/col 2.
H2: specifically column 4 (or 2) empty while col 3 and col 5 are tall.
H3: related to threats inside the well (stacked threat cells in the well column).

## Key finding via act
Within a game the unit fires only for one side to move (parity). Not well geometry: pure well 3,3,5,5,... gives ~0.
Common factor: OPPONENT stones on the a1-d4 diagonal (0,0),(1,1),(2,2),(3,3); their threat at (2,2) is frequent in top examples.
Minimal pairs: 0,1,1,3,3,3,3,2,6 (their (0,0),(1,1),(3,3)) = 6.0; same with own perspective 0.27; without (1,1) 1.4;
shifted diagonal (0,1)-(3,4): -0.16; mirror diagonal (0,6)-(3,3): -0.2; my stone at (3,3) blocking: -0.1.
H5: fires when opponent has >=2 stones on that diagonal and I have none.

## score 1 (p1: >=2 theirs on (0,0)-(3,3), none mine): F1 0.441 P 0.29 R 0.92 AUROC 0.93, sim share 0.89
## score 2 (p2: >=3 theirs in clean window (0,0)-(3,3) or (1,1)-(4,4)): F1 0.533 P 0.39 R 0.83, sim 0.70
FPs of p2: threat cell was (4,4)/(3,3), not (2,2); (2,2) filled. Misses: (0,0)+(1,1) theirs with (2,2),(3,3) empty fire (2-5).
Minimal pairs on 0,1,1,3,3,3,3,2,6 (6.0): drop (0,0)->0.9, drop (1,1)->1.3, drop (3,3)->1.6.
p3: require (2,2) empty; threat at (2,2) via (0,0)(1,1)(3,3) or (1,1)(3,3)(4,4); or pair (0,0)(1,1) with (3,3) empty.

## score 3 (p3, (2,2)-empty variants): F1 0.528 P 0.47 R 0.60, sim 0.86 -- requiring (2,2) empty was wrong: (0,0)(2,2)(3,3) and (0,0)(1,1)(2,2) also fire.
## score 4 (p4): W1 (0,0)-(3,3) clean with >=3 theirs, or W2 (1,1)-(4,4) clean >=3 with (2,2) empty; pair (0,0)+(1,1) = level 3 only.
   F1 0.650 P 0.541 R 0.814 AUROC 0.898, sim share 0.95. BEST.
## score 5 (p5 = p4 but pair also fires): F1 0.601 P 0.45 R 0.92. Worse; keep p4.
Exceptions: late-game W1 threats sometimes silent (pos 12900 -0.7); pair cases fire inconsistently; some unexplained context effects (their (0,5) stone raised 0,1,1,6,6 from 0.26 to 2.4).

## steer
0,1,1,3,3,3,3,2,6: max -> col0 +0.38, col4 -0.38; zero -> col0 -0.13, col4 +0.14.
48849 game ply15: max -> col1 +0.14, col3/4 -0.06/-0.05; zero -> col1 -0.22, col3 +0.16.
0,1,1,6,5,2,2: small (col3 +0.05). 97259: tiny (col0 +0.05 / col3 +0.07 when zeroed).
Effect: shifts probability toward the far-left columns (0/1) and away from 3/4; col 2 (below the threat) is never raised.

## synth
Local mutation search around dev-max pos 60311: 6,3,5,5,3,3,2,3,1,1,6,0,0,2 = 16.84 (beats 15.91); ...,4,0,0,2 = 16.55; ...,3,0,6,2 = 16.29.
Final: p4 (F1 0.650, sim share 0.95). Confidence medium.
