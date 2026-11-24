# U39 notebook (layer 1, pole -, threshold 0.427, dev max 2.419, rate 3.0%)

## Exploration
- 40 examples + 60/band (seed 7) saved as ex_b*.txt. Height histograms by band: top bands have
  cols 4,5,6 nearly empty (mean h 0.6-1.0) while cols 2,3 are normal/tall (h3 ~3.6). Ply ~11-13 at the top
  vs ~18 overall; even ply (me = first player) over-represented (62%).
- Per-cell: top band has col 3 bottom = theirs 69%, col 5 bottom = mine 65%, col 4 nearly empty above row 0.
- Tall col 3 alone (3,3,3,3,3) does NOT fire (0.09). Shape-only rules (cliff h3-h4>=3) are too common in low bands.
- Minimal pairs on 2,2,0,3,2,3,2,3,3,0 (1.56): last move anywhere still fires (0.58-1.56); appending 1,1 kills (0.26),
  appending 0,0 / 5,5 / 4,4 keeps firing. Appending one move (odd ply) kills (0.2-0.39).

## Hypotheses
H1: centre-left stacks (cols 2-3 h>=3) with the right side (cols 4-6) nearly empty, mid-early game.
H2: something parity-/colour-specific about the centre stack (to be tested).
H3: col 1 empty matters (1,1 kills).

## Tests (act)
- Shift test: cols 2+3 stacked to h4 at ply 8 (2,3,2,3,3,2,2,3) fires 1.10; same shape on cols 3+4 = 0.07, cols 1+2 = 0.33.
  Mirror (cols 3-6 filled) never fires; left side (cols 0-3 filled) fires.
- Colour permutations of the 8-stone 2/3 stack: 0.18-1.10; best when col 2 top is mine and col 3 top is theirs,
  worst XXXX/OOOO splits. Ply 6 versions do not fire, ply 8 do.
- Single-move substitutions on a 1.73 position: earlier moves change act only by +-0.8 (diffuse, bag-of-moves like);
  the last move matters most (opp last move to 6: 1.73, 0: 1.44, 4/5: ~0.85, 1/2: ~0.15, 3: -0.57).
- Playing in column 1 (either side) quickly kills it; opponent stones in cols 4-6 lower it.
- Early exceptions: 2,2,6 (0.83), 5,2,2,6 (0.79): col-2 stack + opponent's last move to col 6.
- Count histograms: top bands ply 8-16 (~100%), opponent rarely in cols 1,4,5,6, opponent heavy in col 3 (bottom of col 3 theirs 69%),
  my stone at bottom of col 5 (65%), right side cols 4-6 nearly empty.

## Scores
1. p1 (h2+h3>=6 & h4+h5+h6<=3): F1 0.264 P0.216 R0.340 AUROC 0.651, sim -0.01 (call 1 was an accidental duplicate run of p1).
2. p2 hand-weighted move-count score S (+2 their col3, +h2, -2 their cols 1/4/5/6, -1 my cols 0/4/6), ply 7-17, S>=1:
   F1 0.287 P0.213 R0.438 AUROC 0.694 sim 0.04.
3. p3 = S + last-move term (0/6 +2, 1/2 -3) + bottom-cell terms, S>=4: F1 0.331 P0.319 R0.345 AUROC 0.661 sim 0.02. BEST F1.
4. p4 simple: ply 8-16, last move not col 1/2, h4+h5+h6<=3, h2+h3>=5: F1 0.328 P0.314 R0.344 AUROC 0.660, sim 0.00.
5. p5 graded version of p3 (ply penalties, fires as 0-1): F1 0.324 AUROC 0.724 sim 0.04. Chosen as final (best AUROC).
FPs look visually like the hits; the unit is a diffuse layer-1 sum over who-played-where and the last move, not a crisp concept.

## Steer
Max and zero on 4 positions (incl. 2.71 synth): move probabilities change by <= 0.02. Effect: none measurable.

## Synthesis (hill-climb with act from a constructed position)
2,3,2,3,3,2,6,3,5,0,0,0 = 2.713 (beats dev max 2.419); 2,3,2,3,3,2,6,3,5,0,1,0 = 2.615.

## Conclusion
Low confidence: best F1 0.33. Description = left/centre-heavy midgame with empty right side, opponent's last move to an edge.
