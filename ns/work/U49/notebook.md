# U49 notebook (layer 5, pole -; threshold 0.430, dev max 5.442)

## Observations (examples bands 0-9, ~80 positions)
- Top firing: the engine/model move is almost always COLUMN 1 (sometimes column 4), usually forced:
  must-block at (3,1)/(4,1) or (4,4), or column 1 the only non-losing move (all others ~ -970).
- In 24 firing band 6-8 positions the model put >0.5 prob on col 1 in ~16, col 4 in 2.
- Simple synthetic vertical must-blocks in col 1 or 4 early game do NOT fire (col4 row3: -1.24; col1 row3: 0.11).

## Hypotheses
H1: fires when column 1 is my forced move (must-block in col 1, or col 1 the only move that doesn't hand them a win).
H2: plus forced block at (4,4) / column 4.
H3: it is about the opponent's threat cells in column 1 (rows 3-5) making other columns poisoned.

## Scores so far
- v1 (forced move = col 1): F1 0.190, P .23 R .16, AUROC .57, sim share 0.02
- v2 (last stone at hot cells (2,1),(3,1),(3,4)): F1 0.190, P .14 R .31
- v3 (must-block directly above the opponent's last stone, row>=2): F1 0.143
## Cell histograms (band 9 vs bands 1-3)
- band 9: column 1 holds 2-4 stones, opponent stones at (1,1),(2,1) ~55%; col 1 empty above row 3; columns 2 and 3 nearly full.
- Minimal pairs: base with cols 2,3 full (3x6,6,2x6) + col 1 = them/me/them(last) fires 0.87; without col 3 full: -0.74; flipping ownership of cols 2-3 kills it.
H4: opponent just played in column 1 (rows 1-3), columns 2-3 tall.
- v4 (last move col 1 rows 1-3 + cols 2,3 tall): F1 0.158
- v5 (any forced move landing on top of an opponent stone, rows 2-4): F1 0.130
- v6 (col-1 shape: height 2-4, their stone on top, cols 2/3 tall; or (4,4) block above last stone): F1 0.168, sim 0.05
- v7 (points: last stone at (2,1)/(3,1)/(3,4) + single forced move, bonus if forced col is 1/4 or equals last col): F1 0.227 (P .34 R .17), AUROC .58, sim 0.03  <- best
## Steer (to max): tiny effects. Largest: undecided position 1,0,0,0: col 1 +0.13, col 3 -0.18; 3,3,4: col 2 +0.13, col 3 -0.15; forced positions ~0 change.
## Synthesis: single-move edits of dev-max game; 0,5,2,2,5,2,2,2,5,1,0,0,2,0,3,0,0,1,1,3,1 = 5.495 (beats 5.442).
## Conclusion: no simple board rule found; top firing concentrates on opponent's last stone in column 1 (rows 2-3) or (3,4) with a forced reply in column 1/4, but this explains little of firing. Possibly a mixture or random direction. Confidence low.
