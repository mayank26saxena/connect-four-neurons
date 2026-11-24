# U23 notebook (layer 0, pole +, threshold 0.380, dev max 1.104)

## Observations (examples, 100/band seed 11)
- Top band dominated by last move in column 1 (82/100 in band 9, ~60% band 8, ~30% band 5).
- Among last-col-1 firings, column 1 mostly has 1 stone (the just-played one), sometimes 2.
- Strong ply effect: almost no firing at ply 20-29; firing at ply <20 and again ply 30+.
- Non-col-1 firings: last col 0/2 early (first stone in an edge-ish column), col 4/5 mid-game
  often when the last two moves were in the same column (4,4 / 5,5), and a broad late-game (ply 30+) set.
- Minimal pairs (6,2,6,x): last col 1 0.90, 0 0.71, 6 0.61, 2 0.49, 3/4/5 ~-0.2.
  Earlier stone in col 1 drops 0.9 -> 0.2; earlier stone in col 4 drops to ~0.44. Centre-heavy prefixes (3,3,4,2) suppress.

## Hypotheses
H1: opponent just dropped into column 1 near the bottom (col 1 height <=2), early game (ply<20).
H2: H1 plus late-game (ply>=30) component.
H3: layer-0 token mixture (last token + positional), no clean board concept.

## Score log
- p1 (last col 1, h1<=2, ply<20): F1 0.312 (P .285 R .343) AUROC .659, sim share 0.12
- p2 (+ no my stone in col 1; + col 0/2 first stone at ply<=8/10): F1 0.333 (P .278 R .414), sim 0.17
- p3 (weighted mean of their stones' columns): F1 0.287 -- worse; their stacking in col 2 (2,0,2,5,2) does not fire.
- p4 (p2 + col-4 density filter): F1 0.320
- p5 (hand-set score: last-col bonus minus my col-1/col-4 (and 3/5) fraction, their col 4): F1 0.309 (P .445 R .236)
- p6 (p5 + their left-side bonus, lower threshold): F1 0.329 (P .353 R .308)
- p7 (p2-style rule + filter "my stones not in col 1, < half my stones in col 4"; graded level from p6 score): F1 0.349 (P .349 R .349) AUROC .665, sim share 0.17  <- best

## More minimal pairs
- 6,2,6,x: x=1 .90, 0 .71, 6 .61, 2 .49, 3/4/5 ~-0.2.  My stone in col 1 instead of 6: .20; my stone in col 4: .44.
- 2,0,y,1 (my y): y=6 .85, 5 .47, 3 .44, 4 -0.01. 5,2,4,0 -0.44 vs 5,2,6,0 .55 -> my col-4 stone is the strongest suppressor.
- their col 0 stone boosts (0,6,2,6,1 = 1.12).
- Late game (ply 31+): last col 1 is LOW (-0.2) and last col 3/5 fire (~0.5); alternate plies fire -> different regime, not captured.
- Ply 20-29 almost never fires; ply 10-14 enriched; ply 30+ ~30% of firing at a low base rate (not usable).

## Steer
4 positions (6,2,6,1; 0,3,2,6,1; 5,0,2,6,0,3,0,2,5,0,6,1; 3,3,4,2,5), max and zero: all changes <= 0.01. No measurable effect.

## Conclusion
Layer-0 unit that reads mostly token identity: strongest when the last move is column 1 (then 0) early in the game,
suppressed by my stones in column 1 or 4. About 40% of firing (late game, mid-game col-4/5 restacks) is unexplained.
Mixture-like; confidence low (F1 0.35).
