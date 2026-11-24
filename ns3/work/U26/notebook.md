# U26 notebook (layer 4, pole +, threshold 0.585, dev max 33.2)

## Examples
- Bands 7-9 (act 2.4-33): almost all = opponent has three stacked at top of column 0, cell above empty (must-block on col 0).
- Bands 5-6 (0.6-2.4, ~2/3 of firing!): diverse, early-game boards, some vertical threes in cols 2/3/6. No obvious pattern.

## Hypotheses
H1: opponent vertical three at top of col 0, open above. (strong core)
H2: any vertical opponent three (weaker for other cols).
H3: weak band = generic / noise.

## act minimal pairs
- 4,0,4,0,3,0 -> 16.7; same in col6/col1/col2/col3 -> ~0 (H2 rejected: col-0 specific).
- Block it (add 0) -> 0.26. Last move need not be col 0 (1,0,6,0,6,0,2,5 -> 16.9).
- Three on top of a X stone (3,0,0,0,3,0,4,0) -> 19.8. col0 O,O,O,X,O (not top three) -> 0.3.
- My own vertical three in col 0 -> ~2 (fires weakly).
- Horizontal threat at (0,0) -> 0.06: only vertical.

## Scores
- s1 p1 (their col-0 vertical three): F1 0.483 (P 0.988, R 0.320), AUROC 0.66, sim share 0.74.
- s2 p2 (+ my col-0 vertical three): F1 0.493 (P 0.974, R 0.330), sim share 0.74. BEST.
- s3 p3 (+ their vertical three in any column): F1 0.301 (P 0.22, R 0.46). Rejected.
- s4 p4 (+ their vertical three in col 6 only): F1 0.446 (P 0.55). Rejected.
- Remaining ~2/3 of firing is the weak tail (0.6-2.4 vs max 33), no clean pattern found via histograms
  (last col, ply, col-0 height/top owner, their_wins counts all only mildly enriched). Other-column vertical
  threes give inconsistent small activations in act tests (0.0-1.8).
- s5 p5 (p2 fires; graded level: last move col0 9 / older 7 / mine 5 / other-col vertical three 3 / any must-block 2): F1 0.493, sim share 0.77. FINAL.

## Steer
- Zeroing on 1,0,6,0,6,0,2,5 drops P(col 0, the block) 1.00 -> 0.59 (+0.37 to col 3). Other firing positions: no change (block already certain).
- Forcing max on non-firing boards: tiny diffuse changes (<0.3), does not by itself create a col-0 preference.
## Synthesis
- Their three on rows 2-4 of col 0 above two of my stones, just played, with some stacked stones in cols 5/6: 34-35 (> dev max 33.2).
