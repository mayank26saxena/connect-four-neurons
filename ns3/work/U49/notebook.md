# U49 notebook (layer 2, pole +, threshold 0.731, rate 3%, dev max 1.895)

## Observations (examples, ~360 positions across bands)
- Firing positions are early/sparse: band 9 mean ply ~10 vs band 0 ~22. Top bands almost never have a full column
  (band 8-9: 70/72 have zero full columns; band 0-1: ~26/80). Max column height in top bands mostly 3-4.
- Last move row in top bands is mostly 0-2; last move column skewed to col 5 in dev.
- Activation oscillates strongly with each move (very sequence/last-move dependent). Empty board = 1.04.
- Probe base 3,3 + X at a + O at b: O's last stone in col 0 (or 4) gives high act; O in col 1,2,6 low. Stacking O on my stone helps.
- steer: zero / max changes move probabilities by <=0.01 on 3 positions -> no measurable effect.

## Hypotheses
H1: "sparse board": no full column, max height <=4, ply small.
H2: H1 + last move column effect (O just played in col 0/3/4/5, not 1/2/6).
H3: unit is mostly an unstructured direction (mixture) -> low confidence.

## Tests
- Minimal pairs (act): activation swings by >1.5 when a single stone is moved to another column, in early and late
  positions alike; the direction of the swing is not consistent across bases (e.g. O in col 1 is bad on base 3,3,0 but
  fine on 3,6,3,1,2,3,2,5,3). Order of the same board changes it by ~0.2.
- "Well" (empty column between tall ones): built deep wells (3,5,3,5,... ) -> activation stays < 0. Rejected.
- Full column kill: filling a column lowers it gradually, not a switch.
- Single-feature histograms by band: ply, max height, no full column, col-1 empty, top-stone owner, X-under-O caps,
  col-3 ownership, last row/col: only the "sparse board" family separates bands, and weakly.

## Scores
- s1 p1 (max height<=4 and ply<=16): F1 0.103 P 0.056 R 0.645 AUROC 0.662; sim share 0.02.
- s2 p2 (+ last row<=2, no threats): F1 0.098, AUROC 0.596; sim -0.29. Worse.
- s3 p3 (ply<=10, max h<=3): F1 0.101, AUROC 0.593.
- s4 p4 (col 1 empty, max h<=4, ply<=14): F1 0.121 P 0.076 R 0.304, AUROC 0.597; sim -0.01. Best F1.
- s5 p5 (>=2 columns where O caps my stone, sparse): F1 0.097, AUROC 0.555.
Conclusion: precision never exceeds ~2.5x base rate. Unit looks like a distributed / mixture direction with a bias toward
sparse, early positions. Confidence low.

## Steer
Forcing to max or zero changed move probabilities by <=0.01 on 3 positions (5,6,5,5,3,3; 3,3,0,0; 3,4,2,5).

## Synthesis (hill-climb with act substitutions)
5,0,5,5,3,3 = 2.004; 5,4,5,5,3,3 = 1.994; 5,1,5,5,3,3 = 1.957 (all beat dev max 1.895). Pattern: my two stones in col 5
capped by O, my col-3 stone capped by O, O stone elsewhere on the bottom row.
