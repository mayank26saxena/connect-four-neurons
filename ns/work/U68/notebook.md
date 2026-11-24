# U68 notebook (layer 5, pole -, thr 0.349, dev max 4.098)

## Examples
- Band 9/8 dominated by must-block positions, especially opponent vertical three in column 0 (must-block directly above last move), also col 2, col 4, (4,3), horizontal (0,4).
- Some top firing without must-block: often teacher scores show a single non-losing move (e.g. column 4 poisoned: their threat directly above landing in col 4).
- Lower bands (5-6): diffuse, many quiet openings (1,6,6; 6,0,2,1; 0,5,5,5,2).

## Hypotheses
H1: opponent just made a vertical three (must-block above last move).
H2: there is a must-block cell, in columns 0/2(/4) specifically.
H3: forced-move positions in general (only one non-losing move).

## act tests
- Vertical three c,a,c,b,c (first-player threat): fires strongly for c=0 (0.46-2.15) and c=2 (0.49-2.2, strongest when mover has a stone at col 3), NOT for c=1,3,4,5,6 (all < 0.12).
- 3,0,3,0,6,0 (second player vertical three in col 0) fires 0.46; same in cols 1,2,4,5,6 does not.
- So H1 alone is wrong; column-specific (0, 2) with context.
- steer: on must-block positions no effect (saturated). On quiet firing positions max-steer moves ~2-9 points, raises col 2, lowers col 5 (4,2,3,1,3,4,2,3: +8 col2, -9 col5; 6,0,2,1: +3 col2 -3 col5); 3,5,0,3,...: -3 col3 +2 col2.

## Scores (dev)
- call 1: p1 (any must-block in col 0/2/4): F1 0.182 (P .136, R .276), AUROC .61, sim share 0.01. (call 2 was an accidental re-run of p1.)
- call 3: p2 (opponent vertical three just made in col 0/2/4, or any must-block in col 0): F1 0.219 (P .211 R .226).
- call 4: p3 = p2 + "col 4 poisoned (their threat above landing)": F1 0.127 - poisoning too common, dropped.
- call 5: p4 (opponent has three stacked on top of col 0, 2 or 4 with empty cell above, and I have no immediate win): F1 0.243 (P .283 R .212). BEST.
- call 6: p5 = p4 but col 4 only when opponent moved first: F1 0.232. Reverted to p4.

## Further act findings
- Horizontal must-block at (0,0) (4,1,6,2,6,3) does NOT fire; vertical col-0 three does (0.46-2.1). Mirror (col 6) does not.
- Col 4 vertical three fires only sometimes (2,2,4,2,4,2,4: 0.48; 6,4,...,4 dev: 1.57; 4,a,4,b,4 from floor: no).
- Strength depends on my stones near the centre: 2,3,2,4,2 = 2.2 but 2,6,2,6,2 = 0.0; 0,3,0,4,0 = 2.15 vs 0,1,0,2,0 = 0.46.
- Bands 5-6 (about 2/3 of firing) are diffuse quiet positions with no common feature found (histograms of heights/last col flat); must-blocks only ~20-30% there. Looks like a mixture: a clear top-end concept plus diffuse low-level firing.

## Steer
- must-block positions: no change (move already certain).
- quiet firing positions, forced to max: shifts 2-9 points toward column 2 (sometimes 1) and away from column 5 or 3 (4,2,3,1,3,4,2,3: +8 col2 -9 col5; 0,3,3,4: +8 col2 -8 col5; 6,0,2,1: +3/-3; 1,6,6: -3 col3). Zeroing: <=2 points.

## Synthesis
Greedy pair insertion around 0,3,0,4,0 (2.15): 2,6,0,3,0,4,0 = 3.07; 2,4,2,6,0,3,0,4,0 = 3.51; 2,4,2,6,0,3,3,6,0,4,0 = 3.72 (best, below dev max 4.10).

## Final
Submitted p4 (F1 0.243, sim share 0.01), confidence low.
