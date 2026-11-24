# U86 notebook (layer 1, pole -, threshold 0.600, dev max 1.536)

## Examples
- Firing last_col histogram (bands 6-9): ~50% col 4, ~33% col 2, some col 6; bands 0-2 flat.
- Firing skews early game (band 9: 64% ply<8), but late-game firings exist.
- Top boards: opponent (O) stones on bottom row at cols 2 and 4, often with the last move there.

## Hypotheses
H1: last move in col 2 or 4 (opponent stone), early game.
H2: opponent owns bottom cells (0,2) and (0,4); opponent stones in col 0 / col 5 suppress.
H3: mixture / linear bag of token features (layer 1).

## Minimal pairs (act)
- 3,3,5,1,x: x=4 1.02, x=2 0.76, others 0.12-0.37.
- 0,y,0,4: y=2 1.02, y=1 .63, y=3 .62, y=5 .40, y=6 .57  -> them at (0,2)+(0,4) best.
- 0,y,0,2: y=4 .99, y=1 .90, y=6 .77, y=3 .70, y=5 .38.
- 2,2,4,4 (them at (1,2),(1,4) on top of mine) -0.55 -> bottom row matters.
- 0,2,0,4,0 (me holds 2,4; them col0) 0.32 -> must be opponent's stones.
- 2,0,4,0,x: x=1 .84, 3 .83, 6 .42, 0 .08 -> opponent stone in col 0 suppresses; last col 6/0 weaker.
- 0,4,0,2,6,x: x=6 1.31, 3 .87, 1 .73, 5 .33, 0 .08.
- 4,4,4,4 -1.1: repeated col-4 stacking strongly negative.

## score 1 (p1: additive last_col + them bottom (0,2)/(0,4) - them in cols 0/5): F1 0.177, AUROC 0.575, sim -0.03. Bad.
Key finding after: landing ROW of last stone matters. Col-4 last move: row0 ~1.0, row1 0.2, row2-3 negative, row4 0.5, row5 0.7-0.9.
Histogram of last-stone cell by band (2x100 examples/band): band 9 = c2r0 66, c4r0 56, c4r5 37, c6r1 20; band 7 adds c1r1, c4r4, c2r5.
Bands 0-1 flat. -> H4: unit = "last stone landed on one of a few specific cells": (0,2),(0,4),(5,4),(4,4),(5,2),(1,6),(1,1).

## score 2 (p2: last cell in {(0,2),(0,4),(5,4),(1,6)}): F1 0.308 (P .21 R .60), AUROC 0.764, sim 0.20.
Grid a,t,a,4 (me stacks col a, them bottom col t, then them plays (0,4)):
me0: t1 .63 t2 1.02 t3 .62 t5 .40 t6 .57 | me1: t0 .10 t2 .66 | me3: t2 .99 t5 .78 | me5: all <= .41 | me6: t2 .71
-> them on (0,2) +, my stones in col 5 -, them in col 0 -. Modulations ~ +-0.3 around threshold.

## score 3 (p3: cell weights + bottom-row modifiers, threshold strict): F1 0.300 (P .375 R .25), AUROC .618, sim .20. Too strict.
Looked at low-band (0.3-0.5) examples whose last stone is (0,4)/(0,2): the cell alone gives ~0.3-0.5, near threshold;
bottom-row neighbours decide: other of (0,2)/(0,4) held by them = boost, held by me = suppress; my stone on (0,5) suppresses; their stone on (0,0) suppresses.
(1,6) firing cases: their stone on top of MY (0,6); FPs had their own stone below.

## score 4 (p4: bottom-row neighbour modifiers, ply<=8 bonus): F1 0.303 (P .23 R .44), AUROC .70, sim .19. No gain.
Miss 40587 (3,1,4,1,5,2: last (0,2) with MY stones on (0,3),(0,4),(0,5)) = 0.89 contradicts "my (0,4) suppresses". Modifiers are interaction-heavy.
More pairs: them's own previous move column matters more than my last move (100373 variants: my move varies .96-1.10; their previous move .64-.85).
Their stones in col 0 (any height) suppress strongly (1,0,1,0,6,0,6,2,6,6,0,4 = .30 vs 0,1,0,1,0,2,0,4 = .92).

## score 5 (p5: cells {(0,2),(0,4),(5,4)}=3, (1,6) on my (0,6)=3, (4,4),(5,2),(1,1)=2; -1 per their col-0 stone, -1 my (0,5), +1 ply<=8; fire>=3):
F1 0.345 (P .32 R .38), AUROC .68, sim .18. Best so far.
## steer: max/zero on 5 positions (0,2,0,4; 3,3,5,1,4; 100373; 3,1,4,1,5,2; 6,0,0,6): change <= 0.01 on every column -> no measurable effect.
## synth: col-6 stack (my (0,6), their (1,6),(2,6)) is very strong: 0,6,5,0,6,4,6 = 1.555 (beats dev max), 5,6,0,0,6,4,6 = 1.536 (= dev max pos).
Here their col-0/col-5 stones do NOT suppress -> modifiers are cell-specific.

## score 6 (p6: p5 + any their stone at (1,6)/(2,6) over my (0,6)): F1 0.307 (P .21 R .54), AUROC .74, sim .20. Col-6 rule too broad; revert to p5.
## Conclusion: unit keys on the cell where the opponent's last stone landed (mostly (0,4), (0,2), top of col 4, col 6 just above my stone),
strongest early in the game, with interaction-heavy modulation from other bottom-row stones. Best F1 0.345 -> confidence low (below 0.4).
Stopped at 6/8 score calls; remaining ideas were modifier tweaks unlikely to change the picture.
