# U14 notebook (layer 2, pole -, threshold 0.861, dev rate 3.0%, dev max 2.191)

## Observations
- Top examples are mostly early game (ply 4-10); last stone (opponent's) often lands in row 2 (third row), usually on top of my stone.
- Histogram (150/band): band 9 last_row=2 in 95/150; ply<8 in 82/150. Band 0: flat rows, flat ply.
- Steer (zero) on 4 top positions: changes <= 0.03 in any column -> effect essentially none.
- act minimal pairs are messy: last column matters a lot (col 3 fires in nearly all below-configs, col 0 never, col 5 only some);
  other stones' placement shifts activation by ~0.5.

## Hypotheses
H1: opponent's last stone landed in row 2, early game.
H2: last stone in centre-ish columns (3,4) on top of my stone.
H3: mixture / random direction (no clean concept).

## Tests (act minimal pairs)
- Fixed 6-stone base, vary last column: only some columns fire (base 6,0,6,3,2,3: col 3 -> 2.19, col 6 -> 0.22).
- Col-3 stack X,X,O (O last, row 2) fires robustly when other stones are moved one at a time (1.0-2.2).
- But it is not general: random ply-6 positions ending with O at col 3 row 2: 0/14 fired (0.21-0.59), including XXO stacks.
- Same pattern in cols 0,1,6 does not fire; in cols 2,4,5 it fires only sometimes.
- Being the LAST move matters: two more moves after the pattern drops it from 1.2 to 0.3-0.4.
- Cell histograms by band: firing early positions have the tallest column exactly 3 (74% band 9 vs 25% band 0), row 3 empty.
- (prev,last) move pairs, colour-absolute cell maps: nothing clean.

## Dev metric
- p1 last_row==2 & ply<=12: F1 0.160 (P .117 R .254) AUROC .598, sim -0.03
- p2 last_row==2 & (col3 or col 2/4/5 with mine below): F1 0.160, AUROC .612, sim 0.05
- p3 last_row==2 & max height<=3: F1 0.169, AUROC .592, sim 0.02
- p4 last_row==2, cols 2-5, my stone below, max height<=3: F1 0.195 (P .205 R .186), AUROC .582, sim 0.02  <- best
Stopped scoring at 4/8: every variant was around 0.16-0.20, so more calls would only overfit.

## Effect
steer zero/max on 7 positions: every column changes by <= 0.03. No measurable effect.

## Conclusion
A weak, diffuse unit tied to the opponent's last move: an early-game stone landing in row 2. The activation depends on context
in ways I could not compress into a rule. It may be a random direction. Confidence low.
