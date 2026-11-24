# U18 notebook (layer 4, pole +, threshold 1.050, dev max 8.428)

## Observations
- Top band dominated by early positions like 2,4,2,3 (me X at (0,2),(1,2); them O at (0,3),(0,4)) -> 4.8; 0,5,3,2,4,2,3 -> 8.1.
- Very position specific: mirror 4,2,4,3 -> 0.3; shifting stack to col 3 -> 1.25; col1 -> -0.1.
- In 2,4,2,3: their stone at (2,2),(2,3),(2,4) or (1,5) kills; their stones at (1,3),(1,4),(0,5),(0,6),(1,6),(1,0) do not.
- Midgame (4,3,4,2,0,6,3,3,3,0,2,0,0,6,3,6 = 4.2, me X at (1,2),(1,3),(1,4)): their stone on (2,2) or (2,4) kills/reduces; blocking my threats does not.
- Fires only for one side in a game (alternating plies) - depends on 'me'.
- Histograms by band: column 4 height 1 in 30/40 band-9 examples; col4 rows>=2 nearly always empty in firing bands; (1,2)=me 65% in band 9.
- steer: small effect, forcing high lowers col 3 by ~0.05.

## Hypotheses
H1: col 4 low (<=1-2) and my stone at (1,2) with (2,2) empty.
H2: my stones occupy the top of the centre-left columns on row 1 (1,2)/(1,4) with empty cells above (row 2 empty in cols 2-4).
H3: my non-playable threats (rejected: blocking threats does not reduce).

## Score log
- s1 p1 (col4<=1 & my (1,2) & h2==2): F1 0.130 P .17 R .10 AUROC .54. sim 0.01.
- s2 p2 (top of col2 mine, col4<=2): F1 0.101 P .06 R .24.
- s3 p3 (col4<=1 & >=2 my stones col3 rows1-3): F1 0.106, AUROC .557. Column-4-low alone is weak.

## New observation (band 9 midgame boards)
- Many top boards: my horizontal pair/triple on row 1 or 2 in cols 1-4 (often (r,2),(r,3)) next to an empty column-4 cell.
- Minimal pair: 6,2,2,3,3,4 = 5.7 vs 6,2,2,3,3,0 = -0.6 (only difference: their stone at (0,4) vs (0,0), making (1,4) playable next to my (1,2),(1,3)).
- Covering my row-1 stone (their stone directly above) kills: 2,4,2,3,6,2 / ...,3,3.
H9: my open horizontal shape on row r>=1: a 4-window with no their stones, >=2 mine whose cells above are empty, empty cells playable now or next.
- s4 p4 (open horizontal window with exposed stones): F1 0.046, AUROC .51.
- s5 p5 (col3 - col4 >= 2, col4<=2): F1 0.084 P .05 R .46 AUROC .58.
- s6 p6 (my pair (r,2),(r,3), (r,4) empty): F1 0.089, AUROC .55.
- s7 p7 (col4<=1 & (pair or (1,2)-stack template)): F1 0.104, AUROC .55.
Conclusion: every single-pattern rule gives AUROC 0.51-0.58. The unit responds strongly to a few specific local configurations
(my stack at (0,2),(1,2) next to their (0,3),(0,4); my row-1 pair at (1,2),(1,3) with (1,4) playable) and is very
sensitive to single stones (their stone on (2,2) kills almost everywhere), but no board rule generalises. Looks like a
mixture / possibly a random direction. Using p1 (best F1 0.130) as the submitted program, confidence low.

## Steer
- 6,5,4,2,3,2,3,1,1 (10.8) -> zero: col2 -0.07, col3 +0.07. 0,5,3,2,4,2,3 (8.1) -> zero: col2 -0.10, col3 +0.10.
- 4,3,4,...,3,6 (4.2): no change (forced move). Forcing max in 3,3,4,2 / 2,4,2,3,5,5 / 3,1,4,...: col3 -0.05 to -0.07.
## Synthesis
- 6,5,4,2,3,2,3,1,1 = 10.84; 6,5,4,2,3,2,3 = 8.94; 6,5,3,2,4,2,3 = 8.86; 6,5,4,2,3,2,3,1,0 = 8.43 (all beat dev max 8.428).
