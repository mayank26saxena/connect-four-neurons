# U29 notebook (layer 3, pole +, thr 0.862, dev max 7.187)

## Observations (examples, bands 0-9, per-cell histograms)
- Band 9: cell (4,3) (row 4 = 5th row, centre column) is THEIRS in 85% (band 0: ~12%, band 1: 17%).
- (4,4) is empty in ~100% of band 9; (3,4) never mine (O 34%, empty 66%).
- Column 3 tall (h3 5-6), column 4 low; h3-h4 shifted positive at high bands.
- Their threat (3,4) / my threat (2,4) common but < 1/3 of band 9.
- Steer: essentially no effect on move probabilities (<0.07) in 5 positions.

## Hypotheses
H1: their stone at (4,3) and (4,4) empty (column 4 height <= 4).
H2: column 3 much taller than column 4 (h3-h4 >= 2).
H3: weighted sum of cell cues (4,3)=O, (4,4) empty, (3,4) not mine, (5,3) not O.

## Minimal pairs (base "OX,O,OOXO,XXOXO,O,XX,XO" bottom-up per column, X=me) = 2.68
- (4,3) O->X: 1.25 ; remove (4,3): 1.51  (helps but not alone)
- (4,4) filled with O: 0.67 ; with X: -0.05   (filling (4,4) kills it)
- col4 "OX": 4.10 ; "OXO": 2.65 ; "OXOX" ((3,4) mine): 1.86
- simple 3,3,3,3,3 (O at (4,3), nothing else): 0.26 only -> context needed
- activation builds every other ply: only when (4,3) is opponent's.

## Dev metric log
- s1 p1 ((4,3) theirs, (4,4) empty, (3,4) not mine): F1 0.237 (P .148 R .593) AUROC .744, sim share .13
- s2 p2 (hand-weighted cell cue count from band-9 vs band-1 histograms): F1 0.310 (P .234 R .459), sim .19
- s3 p3 (p1 + (5,3) not theirs + ply<=28): F1 0.293 (P .206 R .509), sim .13
- s4 p4 (cue sum incl. last move at row 3): F1 0.168 - last move alone does not help a rule
- s5 p5 (their stone at (4,3) OR at (3,4)): F1 0.257, AUROC .755
- s6 p6 (p3 core AND >=5 cell cues): F1 0.366 (P .309 R .450), AUROC .709, sim share .19  <- best

## Further findings
- Strong move-order dependence: the SAME board gives 0.55 .. 3.18 depending on move order; last move
  landing at (3,4) (row 3, col 4) gives the highest values (band 9: last move on row 3 in 57%, col 4 in 38%).
- Activation is spread over many cells; removing/adding far stones (col 0/6) changes it by 2+ units.
  Simple positions with only the key cells do not fire. Looks like a distributed / mixture direction.
- Steer (6 positions, zero and max): changes move probabilities by <= 0.07; effectively no effect.
- Synthesis: board "XXO,,OOXX,XOXOOX,OOXO,OXOX,XXO" with their last move at (3,4) reaches 9.755 (dev max 7.187).
## Conclusion: low confidence. Best description: opponent stone at (4,3) with (4,4) empty, mid-game, plus diffuse context.
