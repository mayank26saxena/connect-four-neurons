# U34 notebook (layer 3, pole +, threshold 1.109, dev max 3.078)

## Observations
- Empty board activation 6.3, after first move negative. Top band dominated by early positions (ply 4-13) but firing spans ply 4-40.
- Steer to zero/max: no measurable change in move probabilities on 6 positions (<=0.02).
- Minimal pairs on base 6,5,6,5 (1.42): per-column effect of my stones roughly {6,1 high; 0,4 mid; 2,3 low; 5 lowest};
  their stones {5 high, 0 next, 4 lowest}. Sweep 0,3,3,3,6,x: x in 0,2,4 fires, 1,3,5,6 does not. No coherent
  tactical/geometric pattern; looks like scrambled column-occupancy sum, consistent with a random direction.

## Hypotheses
H1: early game (low ply) -> test with score.
H2: additive column weights for my/their stones (from minimal pairs) -> test with score.

## Scores
- s1 p1 (ply<=8): F1 0.104 (P 0.061, R 0.336), AUROC 0.589, sim share -0.15.
- s2 p2 (their last stone horizontally beside my previous stone; suggested by two minimal-pair sweeps): F1 0.044, AUROC 0.503 (chance). Rejected.
- s3 p3 (early + I own a bottom corner, center bottom not mine): F1 0.076, AUROC 0.533. Rejected.
- Histograms (240 sampled examples) of last column, ply parity, column occupancy, center share: no difference firing vs not.
- Transposition test: activation is mostly determined by the board (move order changes it by <0.5).
- Minimal-pair column effects are not consistent across bases (e.g. their stone in col 4 is the most negative on base 6,5,6,5
  but fine on 0,1,5,6). Strongly nonlinear, no readable pattern. Conclusion: looks like a random direction / no clean concept.
- Steer: no measurable effect (<=0.02) on 6 positions.
- Synthesis: greedy single-move edits reach 2.79 (1,1,2,3,1,3,2,2,3), below dev max 3.078.
