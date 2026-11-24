# U03 notebook (layer 4, pole +, threshold 0.821, dev max 12.217, firing 3%)

## Examples (bands 0-9, ~100 boards)
- Top bands are mostly early game (mean ply ~8 in band 9 vs ~19 in band 1).
- Centre column underplayed: share with heights[3] <= 1 rises from ~0.25 (bands 1-3) to 0.82 (bands 7-8) and 0.90 (band 9).
- Many top boards have my stone at (0,1) with (0,0),(0,3) empty (e.g. .XX...O), but this is not required.

## Hypotheses
- H1: I have a move that creates two immediate wins (bottom-row open three). Suggested by .XX..OO (7.0) vs .XXX.OO made (0.84).
- H2: centre column (3) nearly empty after the opening (ply >= 3, h3 <= 1).
- H3: a specific stone mixture (X at (0,1), stones in col 6 help, col 0 stones hurt) -- possible random direction.

## Minimal pairs (act)
- a,6,b,6 grid (X at a,b bottom; O stacked col 6): fires whenever X at col 1 (2.0-5.4), almost never otherwise.
- a,0,b,0 grid (O stacked col 0): mostly negative; no mirror symmetry with the col-6 grid.
- 1,6,2,5 -> 6.98; same with col 3 blocked by O (1,6,2,3) -> 0.72; with XXX completed (1,6,2,6,3,6) -> 0.84.
- 3,6,4,0 (X 3,4 could make open three) -> 0.13; 2,0,3,0 -> -0.28. So H1 is not general.
- Stacks: 5,5,5,5 -> 2.96, 4,4,4,4 -> -1.93, 0,0,0,0 -> -1.04, 1,1,1,1 -> 0.0. Idiosyncratic.
- steer to max (12.2) on 5 positions: changes <= 0.08 in any column, no consistent direction.

## Score calls
- call 1 was wasted (accidentally ran score twice on h1.py; same result).
- h1.py (double-threat setup move): F1 0.037, P 0.11, R 0.02, AUROC 0.51. Rejected.
- h2.py (ply 3-14 and h3 <= 1): F1 0.183, P 0.11, R 0.56, AUROC 0.70, sim share 0.02. Centre-empty is the strongest single correlate but far too broad.

## Enrichment counts (bands 6-9 vs 1-3, ply 3-16)
- Centre column empty +0.41 (bottom); my (0,5) +0.29; their (0,6) +0.30; their (1,5) +0.26; my (1,6) +0.15; my (0,1) +0.09;
  my (0,0) -0.19, their (0,1) -0.16, their (0,5) -0.12, my (0,6) -0.12.

## More minimal pairs
- Right-corner crossing 5,6,6,5 (me (0,5),(1,6); them (0,6),(1,5)) -> 3.06 and stays firing with most additions, even with col 3 filled
  (3,3,5,6,6,5 -> 4.27). Same crossing at cols 1-2 (1,2,2,1) -> 2.15. At cols 0-1, 2-3, 3-4, 4-5 -> ~0. Opposite colouring (6,5,5,6) -> 0.25.
- My bottom pair (0,1)+(0,2) fires robustly with col 3 filled (3,3,1,6,2,6 -> 4.9; 3,3,2,6,1,6 -> 4.7); pair (0,4)+(0,5) 3.5;
  pairs (0,0)+(0,1) -> 0.25 and (0,5)+(0,6) -> -0.35. Adding my (0,0) kills it (3,3,1,6,2,1,0,0 -> 0.13).
- Hollow-centre "well" (2,2,4,4,2,2,4,4) -> -0.41: not about column geometry.

## Score calls continued
- h3.py (opening gate ply 3-16, h3 <= 1, + hand weights on bottom-row cells): F1 0.225, P 0.21, R 0.245, AUROC 0.61, sim share 0.03.
- h4.py (pattern only: my (0,1) with my (0,2) or their cap, mirror at (0,5)): F1 0.072 (fires on 36%). Pattern needs the opening context.
- h5.py (additive score, no centre gate): F1 0.126. Worse.
- h6.py (h3 + pair bonuses): F1 0.225, same as h3; keep the simpler h3.

## Steering
- to max on 5 non-firing positions and to zero on 4 firing ones: every column changes by <= 0.08, no consistent direction. Effect: none measurable.

## Synthesis
- Beam search with act from 1,6,2,1,5,5: best 9.34 (1,6,2,1,5,5,6,5); dev max 12.22 not beaten.

## Conclusion
- Fires mostly in the opening when the centre column is still empty and the bottom row has my stones on columns 1/2 and/or 4/5
  with the opponent in the right corner; very sensitive to individual stones (no mirror symmetry, single stones flip it).
  Looks like a mixture / possibly a random direction. Best F1 0.225 -> confidence low.
