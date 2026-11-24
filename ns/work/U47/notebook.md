# U47 notebook (layer 4, pole +, threshold 2.678, dev max 38.6)

## Examples (bands 0-9, ~70 positions)
Top band (21-38): nearly all have last move in column 1 with the opponent stone landing at row 2 (heights[1]==3),
so the landing cell of col 1 is (3,1). Often (3,1) is a must-block too. One top example (49182) last col 2 but col 1 height 3 and must-block (3,1).
Lower firing bands: more mixed (last col 0,4,5,6...).

Hypotheses:
H1: opponent just played col 1 to row 2 (col 1 now height 3).
H2: col 1 landing cell is (3,1) (height 3) regardless of last move; stronger when last move there / (3,1) is a threat cell.
H3: a threat for them at (3,1) (must-block / their_wins contains (3,1)).

## Tests (act minimal pairs)
- Early toy positions with col 1 height 3 barely move it (1.8 max): context needed.
- 154729 (27.1): replacing the final col-1 move (which made col 1 height 3) with any other column -> 1.6-3.0. Col-1 height 3 + recency drives the peak.
- 2,6,1,3,3,1,4,3,1 (5.5) + one more stone anywhere except col 1 -> 8-16; + col 1 (height 4) -> -0.6. Height exactly 3 is essential.
- Same stones, different owners: B,2,2,0 (I have immediate win at (3,1)) = 15.6; B,0,2,2 (must-block at (3,3)) = 1.3. Urgent move elsewhere suppresses; urgency at (3,1) boosts.
- Immediate win created elsewhere (27424 + col 3) drops 22.9 -> 1.0.
- Sampling bands: h1==3 is in 38/60 of band 4 (95-97 pct), 12/60 of band 3, ~0 of bands 0-2: unit is a graded "col 1 landing row 3" detector; threshold cuts a continuum.

## Score calls
1. p1 last_col==1 & h1==3: F1 0.419 (P .48 R .37), AUROC .68, sim share 0.67.
2. p2 h1==3: F1 0.502 (P .347 R .907), AUROC .926, sim 0.67.
3. p3 h1==3 & no urgent move outside (3,1): F1 0.502 (P .36 R .83), sim 0.64.
4. p4 numeric weighted (last1, top theirs, ply, urgent elsewhere): F1 0.430, AUROC .917, sim 0.72.
5. p5 h1==3 & top stone theirs...: F1 0.472. Ownership of col-1 stones does not help.
6. p6 h1==3 & ((3,1) urgent, or no urgent move anywhere and ply>=12): F1 0.514 (P .388 R .761), AUROC .861, sim 0.91. BEST.

## Steer
- B+0 (14.2) zero: col3 +16, col2 -7, col1 -3, col4 -5. B+6 (15.2) zero: col1 -8, col3 +8.
- 4,1,0,2,0,1,1,3 max: col0 +23, col3 -18. 1,1,1,4,4,3,2,4,2 max: col2 +18, col4 -30, col6 +10. 3,3,1,1,1 max: col2 +14, col4 -12.
- Saturated/forced positions: no change. Effect: modest, shifts probability away from centre (3/4) toward columns 0-2 / col 1; not consistent.

## Synthesis
Hill-climbed move orders (script climb.py using act only): 41.3, 40.1, 39.6 beat dev max 38.6. Peak position: they just played col 1 to row 2, (3,1) is a must-block, several of their threats.
