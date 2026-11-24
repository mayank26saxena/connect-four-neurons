# U22 notebook (layer 5, pole +, threshold 0.705, dev max 6.644)

## Observations
- Examples (40 + band 9 x 12 + 10 bands x 40 seed 3): no obvious tactical motif; no threat/must-block pattern.
- Board-based (move order permutation keeps activation), but NOT mirror symmetric (1,5,0,2,1 = 3.85; mirror 5,1,6,4,5 = -0.25).
- Very sensitive to single stones, especially the last one.
- Steer: forcing max raises column 6 (+0.03..+0.21), takes from col 4/2/1. Zeroing on top positions: small changes (<0.15).
- Height histograms (single feature per column, band 0-4 vs 7-9): in firing positions, columns 0-5 almost never have
  exactly 5 stones; col 6 almost never has 2-4 stones; col 3 rarely odd (1,3); col 2 and col 4 rarely 2; col 0 rarely 3-4,
  col 1 rarely 4, col 5 rarely 4.
- Minimal pairs on 140475 and 22860 (vary last move only): the variants that fire are exactly those that leave column
  heights in the "allowed" sets; making col6 = 2, col3 odd, col1 = 4, col0 = 5 each kills it.

## Hypotheses
H1: column-height configuration detector: fires when every column height is in an allowed set (see p1.py).
H2: opponent stacked pair / X flank local motif (47013, 118617) - too specific, not pursued.
H3: random direction / mixture.

## Score log
- s1 (p1, H1 heights all-in-allowed-set): F1 0.146 (P 0.088, R 0.427), AUROC 0.645, sim share 0.11. Heights are a weak correlate only.
- Minimal pairs after s1: early game, an opponent vertical pair at the bottom of column 3 with my two stones on row 0
  fires (0,3,2,3 = 3.96; a,3,b,3 fires for most a,b). Pair in other columns mostly does not (4,c,6,c fires only c=3,4).
  Mirror images do not fire. Adding one more pair of stones usually kills it, except specific cells (O at (0,5) keeps
  it: 0,3,2,3,0,5 = 2.70). Activation looks like a sum of many cell-specific +/- contributions.
- s2 (p2, opponent vertical pair at top of any column + heights): F1 0.125 (P 0.10, R 0.17), AUROC 0.56, sim 0.08. Worse.
- s3 (p3, strongest height dislikes + quiet, graded): F1 0.129 (P 0.072, R 0.653), AUROC 0.696, sim 0.08.
- Quiet positions: bands 6 and 9 are 100% without immediate wins/must-blocks, but lower bands are 78-88% too; weak.
- Course: no clean concept found; unit behaves like a cell-weighted (polysemantic or random) direction. Heading for low.
- s4 (p4, opponent owns (0,3),(1,3) + height filter): F1 0.097, AUROC 0.544, sim 0.12. Centre-pair motif is an early-game special case only.

## Effect (steer)
- to max on 12 band-1 positions: col 6 +0.03..+0.21 (mostly taken from col 4, 2 or 1); zero on top positions: col 6 -0.04..-0.14
  (140475: col6 -0.12/col0 +0.10; 155591: col6 -0.14/col5 +0.12; synth 2,3,3,3,5,2,0,1,3,2: col6 -0.09/col2 +0.07).

## Synthesis (hill-climb with act, climb.py)
- 0,3,2,3 = 3.96 (local max); 2,1,5,3,3,1 = 4.20; 0,3,2,2,3,3,3,2,5,1 = 5.37; 0,5,0,4,4,5,3,2,6,4,5,4,1,2,3,2,2,1,1,4,4,2,2 = 5.24;
  2,3,3,3,5,2,0,1,3,2 = 6.23 (all below dev max 6.644 so far).
- pair-replacement climb from 6.228: no improvement (local max). Best synth 6.23 < dev max 6.644.
