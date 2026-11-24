# U03 notebook (layer 3, pole -, threshold 1.273, firing 3%)

## Observations (examples)
- Top band: many early positions (ply ~6-14). last_col histogram flat. Ply parity flat overall, but within a game the
  activation alternates by ply (perspective feature).
- Single-cell histograms: band 9 has (2,3)=mine 58% vs band 0 25%; (1,3)=theirs 47 vs 39. Left side (cols 0-2) O-X higher in top bands.
- Steer: effect on move probs is tiny (<=0.06) on 5 positions.

## Minimal pairs (act)
- 6,0,3,3,3,1 = 2.61 (col3 me/them/me, O at (0,0),(0,1)). Mirror 0,6,3,3,3,5 = 0.40 -> asymmetric, left side.
- Removing their stone at (1,3) drops to 0.15-0.8. Removing my (2,3) drops to 0.4-1.6.
- Their stones bottom-left cols 0-2 raise it (two in different cols ~2.0-2.3); their stone at (0,4) kills (~0.2-0.6).
- My stones in cols 0-1 lower it (3,3,0,0,5,1 = 0.09).
- Their stone on top of my (0,2) (2,3,6,3,3,2) = 0.34 vs 2.47.

## Hypotheses
- H1: my stone at (2,3) on top of their stone at (1,3), center column.
- H2: H1 plus their stones on bottom-left and no their stone right of center at low rows (linear template).
- H3: random/diffuse direction (steer effect tiny).

## Score log
- p1 (my (2,3) on their (1,3)): F1 0.065, P 0.037, R 0.295, AUROC 0.531, sim share 0.06. Pattern far too common, barely predictive.
- More histograms (900 high vs 600 low band positions): high bands have fewer stones overall (empties +10-20 pts everywhere),
  center column filled (my (2,3) +22, my (1,3) +9, their (0,3) +8), column 4 emptier (+17-23), mirror-asymmetric.
- act: stones in column 4 suppress (their (0,4) strongly); my stones low on the left suppress; their stones bottom-left raise.
  But many effects are context dependent (e.g. their stone on top of center sometimes raises, sometimes lowers).
- p2 (my (2,3) and col 4 empty): F1 0.107, P 0.088, R 0.138, AUROC 0.547, sim 0.07.
- p3 (hand-weighted template, binary): F1 0.099, P 0.130, R 0.080, AUROC 0.532, sim 0.06.
- p4 (same template, continuous output + ply term): F1 0.117, P 0.107, R 0.130, AUROC 0.607, sim 0.05.  BEST
- p5 (center built, rest of board empty): F1 0.098, AUROC 0.613, sim 0.03.
- Misses include positions with an EMPTY center column (e.g. 23299, 65505), so the center pattern is not necessary.

## Steer
- 9 positions (to zero and to max): change in move probabilities <= 0.06, mostly 0.00. No measurable effect.

## Synthesis
- Hill-climbing with act/synth: 2,4,3,2,3,2,2,3,0,3,3 = 3.391 (beats dev max 3.284). Others 3.197, 3.028, 2.95, 2.87.

## Conclusion
- No clean concept. Weak, diffuse lean toward: few stones, center column built up with my stone in its third cell,
  column 4 empty, opponent stones low on the left. Activation alternates ply-to-ply within a game (perspective).
  No steer effect. Looks like a diffuse or random direction. Confidence low.
