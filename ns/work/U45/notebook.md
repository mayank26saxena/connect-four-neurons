# U45 notebook (layer 2, pole -, threshold 0.710, dev max 6.455)

## Exploration
- 40 examples + band 9 (16) + 150/band histograms of single features.
- Firing positions: mostly ply 7-14; column 2 empty in 83-87% of band 8-9 (27% band 0); col 1 often empty too.
- Cell histograms (band 8/9): (0,2) never mine; (0,3) mine ~60%; (1,3) theirs ~50%; (2,4) never theirs.
- Activation flips strongly with each move (parity-sensitive: e.g. 3,4,3,0,3,3 fires 1.08, +3 -> -1.83, +0 -> 3.4).
- Steer max/zero on 4 positions: change <= 0.01 on every column. No measurable effect.

## Hypotheses
H1: column 2 empty in the opening/middlegame (ply <= ~16), with stones in column 3.
H2: a specific stone configuration around the col 2-4 lower cells (me at (0,3), them at (1,3), not them at (2,4)).
H3: random direction / mixture with no clean concept.

## Minimal pairs (act)
- From 3,3,3,3,3,3,4,4,4,4,4,4 (3.16): adding a pair in col 2 -> -0.30, col 1 -> 0.63, col 0 -> 2.61, col 5/6 -> ~1.1-1.4.
- From 3,4,3,0,3,3,3 + last opp move: col 0 3.4, col 6 0.97, col 5 0.72, col 4 0.11, col 1 -0.02, col 2 -0.32.
- From 154088 (5.40): replacing last move with col 2 -> 0.25; every other column keeps firing.
- Single stacks: 4x6 3.0, 5x6 2.0, 3x6 1.3; 0x6/1x6/2x6 about -1.1..-1.4; 6x6 -4.0. 4x6+5x6 4.7, then +2,2 -> 0.22.
- Opponent stones in col 4 above row 0 lower it (3,4,3,0,3,3,3,0 + 6,4 -> 0.21; + 4,6 -> 1.33).
- Short openings with col 2 empty (3,3; 4,5,4,5) are strongly negative: needs a fairly full centre.
- Conclusion: a stone in column 2 reliably switches it off; stones in cols 3-5 (esp. tall stacks) push it up; but
  the rest is nonlinear/order- and ownership-dependent. Looks like a distributed mixture rather than one concept.

## Dev metric
1. call 1 accidentally consumed by a duplicate run of p1 (output piped twice).
2. p1 (col2 empty, ply 6-20, h3+h4>=3): F1 0.267 (P 0.18, R 0.52), AUROC 0.725, sim share 0.04.
3. p2 (col2 empty, my stone at (0,3), ply 6-22): F1 0.291 (P 0.235, R 0.384), AUROC 0.673, sim 0.07.
4. p3 (hand-weighted cell points: col2/col1 empty, centre-column ownership, opp stones in col 4 negative): F1 0.301, AUROC 0.634, sim 0.07.
5. p4 (col2 empty + full centre cols 3-5 + no immediate tactics): F1 0.213.
6. p5 (empty column 2 or 3 with stones on both sides): F1 0.220 (R 0.60), AUROC 0.74.
7. p6 ("deep well": empty column next to a tall one): F1 0.197 (R 0.68), AUROC 0.76.
Misses include positions with col 2 TALL and cols 0-1 or col 3/4 empty, so "col 2 empty" is only part of it.
Nothing exceeds F1 0.31 -> confidence low. Submitting p2 (simplest, near-best).

## Steering
5 positions, --to max and --to zero: every column changes by <= 0.03. No measurable effect.

## Synthesis
6,0,4,5,5,5,4,5,4,5,5,4,4,4,3,0 = 6.96 (beats dev max 6.455); 6,0,...,4,6,0 = 6.86 (beats);
6,0,4,5,5,5,4,5,4,5,5,4,4,4 = 5.93; 0,0,...,3,0 = 5.96; 5x6,4x6 = 4.98.
Recipe: tall alternating stacks in cols 4 and 5, a few stones in cols 0/3/6, columns 1 and 2 empty.
