# U61 notebook (layer 4, pole -, threshold 0.965, dev max 8.826)

## Observations
- Band 9 cell histogram: (2,3) mine 97%, (1,3) theirs 89%, (3,3) theirs 82%, (1,2) mine 83%, (3,2) theirs 55%, (2,2) mine 54%.
  Band 7: (2,3) mine 77%, (1,3) theirs 73%. Band 0: ~26/36 baseline.
- Mild even-ply bias. No threats needed (most top examples have no threat cells).
- steer: effects small (<=0.1), inconsistent.
- act minimal pairs: many cells contribute (distributed); e.g. 0,0,0,4,3,3,3,0 = 4.9, but 6,0,0,4,... = 0.3 (col 0 colors swapped).

## Hypotheses
H1: center column has me-over-them sandwich: (1,3) theirs, (2,3) mine (optionally (3,3) theirs).
H2: H1 plus my stone at (1,2) (rising diagonal (1,2)-(2,3)).

## Tests (act minimal pairs)
- Base 3,2,2,5,5,4,3,4,3,3 (6.6): adding a their-stone at (2,2), (2,4), (3,4) or (0,1) kills it (<0.3); my stone at (2,4) halves it.
- Base 3,3,3,3,3,4,0,4 (6.2; col3 me/them/me/them/me, col4 them x2): their stone at (0,1), (0,2), (2,4), or (1,5) (over my (0,5)) kills it.
- Base 0,0,0,4,3,3,3,0 (4.9): their stone at (0,1)/(0,2) kills; swapping col-0 colours kills (0.3). Odd-ply continuations drop it.
- Pure col3 alternation 3,3,3,3 + neutral pairs: only 1-2.5. Capped horizontal pair hypothesis (XX under OO on bottom row): ~0, rejected.
- Diagonal (1,2)-(2,3) alone with col3 O,O,X: ~0.2, rejected as sufficient.
- Conclusion: many cells contribute additively; no single clean predicate.

## Scores
- p1 (2,3) mine & (1,3) theirs: F1 0.139 (P .079 R .578), sim 0.03
- p2 (2,3) mine & h4<=2 & (2,2) not theirs: F1 0.177, sim 0.03
- p3 hand-weighted cell sum: F1 0.174, sim 0.04
- p4 strict col-3 alternation: F1 0.132
- p5 (2,3) mine, (2,4),(3,4) empty, no their stone at (2,2),(0,1),(0,2), h3>=3: F1 0.206 (P .215 R .198), AUROC .587, sim 0.08  <- best
- Stopped at 5 calls: gains are small; unit looks distributed (could be a random direction); mid-band firing (bands 5-6) is diverse.

## Steer
- 6 positions, |change| <= 0.10 in every column, no consistent direction. Effect: none measurable.
- Synthesis best 7.873 (3,4,0,0,1,2,3,4,3,3,2,5,5,3); greedy search plateaued near 7.4-7.9, below dev max 8.826. Final: p5, confidence low.
