# U59 notebook (layer 3, pole +, threshold 1.124, dev max 2.947)

## Examples (bands 0-9, ~500 positions incl. seeds 1-3)
- Top examples are visually heterogeneous: very early openings (ply 4, e.g. 2,5,6,1 -> 1.95) and midgame forced positions
  (opponent vertical 3 / must-block, teacher shows only one non-losing move).
- Single-feature histograms by band: firing skews to lower ply (mean ~12-13 vs ~19-20), lower col 0 / col 6 heights,
  fewer "my threat" cells (19-36% have any vs ~50%), slightly more must-blocks (25-30% vs 12-18%). No cell-level pattern.
- last_col and me_first: flat across bands.

## Hypotheses
- H1: opponent just created a must-block (vertical three etc.). act test: stacking O three in col 0/2/3/4 in openings does NOT fire (-1.5..0.7; 6,0,6,0,5,0 = 1.11 borderline). Rejected as main driver.
- H2: specific stone configuration in row 0 (O at cols 1 and 5, X at 2). act: 2,5,6,1=1.95, 2,5,0,1=1.95, 2,1,6,5=1.28 (order matters!), 2,4,6,1=0.44. Looks lookup-like, no general rule found.
- H3: general "early, I have no threats of my own" (diffuse correlate).
- Perturbation of 98915 (4,3,5,5,5,4,3,4,0,4): changing any of the last 4 moves changes act by 0.5-2, many alternatives still fire; dependence spread over many stones.
- Perturbation of 78021-like (1,1,4,3,3,4,4,2,3): last move col 3 2.42, col 1 1.84, col 6 1.49, col 4 0.00.

## Steer
- zero on 3 firing positions: change <= 0.01 in every column. max on 4 non-firing positions: <= 0.04. Effect: none measurable.

## Score calls
- s1 p1 (ply<=14 and no my threats): F1 0.087, P 0.048, R 0.509, AUROC 0.601, sim share 0.00.
- s2 p2 (additive points: col6 empty, col4 low, cols 2&5 occupied, ply<=16, no my threats, col0 low): F1 0.088, AUROC 0.529.
- s3 p3 (opening: ply<=6, cols 3,4 empty, cols 2,5 occupied; OR opp has threat cells and I have none, ply<=20): F1 0.091, P 0.057, R 0.223, AUROC 0.556, sim 0.00.
- s4 p4 (col6 empty, col0<=1, col4 not above col3, no my threats): F1 0.091, AUROC 0.545.

## Full ply-4 scan (all 2401 openings via act)
- 122/2401 fire. Strongest: stones in cols 2 and 5 (bottom row) with cols 3 and 4 empty (fire rate 12.5% when 3,4 empty vs 0.9% when both occupied); my stone at col 2, their stones at cols 1/5 best (2,5,5,1 = 2.48).
- Mirror correlation of the activation over openings = 0.08: the unit is NOT left-right symmetric, and stone order matters (2,5,6,1 = 1.95 vs 2,1,6,5 = 1.28).
- "Valley/hole" hypothesis (a column lower than both neighbours) failed minimal pairs (2,4,2,4,4,2 = -0.02; 4,6,6,4,4,6 = 1.15; 0,2,2,0,0,2 = -0.45).
- Firing midgame positions often look forced/lost for the mover per engine scores, but that is not readable from the board API and minimal pairs with an opponent vertical three did not fire.

## Steer
- zero on 4 firing positions incl. synth 2.897: max change 0.02. max on 4 non-firing: max change 0.04. None measurable.

## Synthesis
- local search from dev example 38014: 0,3,5,6,6,3,3,0,3,6,3,3,4,4,5,5,6,5,4,1,1,2,0 = 2.897 (dev max 2.947, not beaten).

## Conclusion
Unit looks distributed / possibly a random direction: no single board pattern, asymmetric, order-sensitive, nothing above F1 0.09. Confidence low.
