# U48 notebook (layer 1, pole -, thr 0.476, dev max 4.341)
## Observations (ex1, ex9, ex5)
- Top band: columns 0-3 full (esp. column 3 full), columns 4-6 nearly empty (col4 often 0-2). Left half filled, right half empty.
- Threshold band: many have last move in column 3; some early positions with col3 stones.
## Hypotheses
- H1: column 3 full (or tall) while column 4 (right neighbor) is low; level ~ fill of left side vs right side.
- H2: imbalance: sum heights of cols 0-3 much greater than cols 4-6.
- H3: last move in column 3 (weak, threshold band).

## Tests (act)
- Filling cols 0,1,2,3 completely (0x6,1x6,6,2x6,3x6) -> 1.36; only 0,1,2 -> 0.18; 0,1,3 -> 0.19-0.49; 1,2,3 -> -0.7; 2,3 -> -0.8; mirror of a top example (cols 3-6 full) -> 0.06. Needs ALL of cols 0-3 near full; col 0 is key (adding col0 stones to 1-3-full board: -0.7 -> 1.48).
- Any one left column at height 5 (or col3 at 4) still fires ~1-2.
- Move order hardly matters for the same board (0.96-1.07).
- Last move: into left cols or col 6 boosts; into col 4/5 (esp. low) suppresses (A,4 0.20, A,5 0.21, A,6 1.95). Inconsistent though (dev 56170 last col5 = 1.77).
- Right-side fill lowers it gradually (~0.1-0.25 per stone beyond ~6-8).
- Early-game positions with a vertical pair in col 0 sometimes fire near threshold (2,0,3,0 0.65; 0,3,0,3 0.9) but 0,6,0,5 -0.4: sequence-specific, not captured.
## Scores
- p1 left sum>=22: F1 0.493 P0.39 R0.66, sim share 0.16
- p2 + right<=10: F1 0.396 (right cap hurts recall)
- p3 heavier last-move penalty + early col0 pair rule: F1 0.297 (early rule all FPs)
- p4 left + last-move bonus/penalty - right penalty, thr 22.5: F1 0.554 P0.74 R0.44, share 0.25
- p5 col0 double weight: F1 0.540 P0.83 R0.40, share 0.27
- p6 col0 1.5x, col6 bonus: F1 0.525, share 0.28
- p7 p4 + 0.5*(h0-5), stronger right penalty, thr 21.75: F1 0.640 P0.70 R0.59 AUROC 0.79 share 0.28  <- BEST
- p8 p7 + col6 bonus, thr 21.25: F1 0.621 P0.59 R0.66 share 0.28
## Steer: tiny effects (<=0.09 prob) on 5 positions; at A,4,4 max raises col4 +0.09, lowers col6 -0.09; elsewhere ~0.
## Synthesis: last move completing column 0 with cols 1-3 full and right side sparse -> 4.65 (beats dev max 4.34).
