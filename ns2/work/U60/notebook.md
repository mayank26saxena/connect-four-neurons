# U60 notebook (layer 1, pole -, threshold 0.685, dev max 1.831)

## Observations
- Top band (9): almost all early games (ply 4-8) where opponent's last move is col 5 landing at row 1, on top of my stone at (0,5).
- Bands 5-8: also many late-game positions where last move filled column 2 (row 5, top cell).
- Tally of 283 firing samples (band-oversampled): (last_col,last_row) (5,1) 95, (2,5) 71, (4,2) 17, (5,5) 12, ...
- Non-firing bands also contain (5,1) and (2,5) last moves, mostly mid/late game with act 0.4-0.67.

## Hypotheses
H1: fires when opponent just played col 5 landing on row 1 on top of my stone, early in the game (stronger at low ply).
H2: fires when the last move filled column 2 (top cell, row 5).
H3: unit is a layer-1 "last-move position" detector; strength decays with ply.

## act tests
- 0,6,5,5: 1.77; 0,6,4,4: 0.59; 0,6,2,2: 0.73; 0,6,3,3 0.34; 0,6,1,1 0.22; 0,6,6,6 0.24 -> col 5 specific (col 2 weaker)
- 0,5,6,5 (O on O at col 5): 0.04 -> requires MY stone under it
- 5,0,6,5: 1.46 (X at bottom of col 5, me first player) fires
- 0,6,5,5,5,5 (row 3): 0.08 -> row 1 specific
- 0,6,5,5 + later moves elsewhere: drops to 0.1-0.66 -> must be the LAST move
- 3,3,5,5 0.93; 3,3,3,3,5,5 0.71; 1,2,3,4,5,5 0.54 -> decays with ply / other stones

## Score log
- s1 p1 [(5,1) on my stone any ply OR (2,5)]: F1 0.401 (P .366 R .443), AUROC .710, sim share 0.12
- s2 p2 [+ (5,r>=4) + col4 rows0-2 ply<=10]: F1 0.258 (P .167) -> additions too common
- s3 p3 [(5,1) on mine, levels by ply; (2,5)]: F1 0.414 (P .431 R .398), AUROC .691, sim 0.12  <- BEST
- s4 p4 [p3 + early row1-2 landings in cols 2-4]: F1 0.272 -> early landings fire only weakly; reject
- s5 p5 [p3 + (5,r>=4)]: F1 0.304 -> top-of-col-5 too unreliable; reject

## More act tests
- (5,1) activation decays with ply: 0,6,5,5 1.77 -> 0,6,0,6,5,5 1.25 -> 8 plies 0.77 -> 10 plies 0.54
- Other cols row 1 early: 0.2-0.8 (col 2/4 sometimes fires), col 5 always 1.0-1.8.
- Col 2 top cell (row 5) in a late game: 0.59-1.0 regardless of my previous move.
- Late-game top cells of col 5 (rows 4-5) sometimes fire (~0.8) but often not (s5 shows low precision).

## Steer: 5 positions, max and zero: change <=0.01 on any column. Effect: none measurable (layer 1).
## Synth: 0,6,4,4,5,5 1.843; 4,6,0,4,5,5 1.841; 4,4,0,6,5,5 1.834 (all beat dev max 1.831).
## Conclusion: core = opponent's stone at (row1,col5) on my stone, early game; secondary = col 2 filled.
Rest of firing is diffuse over last-move cells; looks like a mixture/partly unstructured layer-1 direction. Confidence low.
