# U47 notebook (layer 5, pole +, threshold 0.697, dev max 11.268)

## Observations (examples, ~1800 positions over bands, seeds 11/21/22)
- Top band: many positions where opponent has a vertical three in column 0 (must-block at top of col 0). ~50% of band 8-9 have a must-block vs ~12% in band 0.
- Column 1 is low: P(heights[1] <= 1) rises from ~0.35 (bands 0-3) to 0.91 (band 9); heights[1]==1 most common.
- Opponent's last stone at row 2 enriched (40% vs 18%).
- Steer: forcing unit high raises column 1 (+0.2 to +0.4 prob), at expense of whatever was best; zeroing lowers col 1.

## Hypotheses
H1: opponent has a must-block (esp. vertical three, esp. col 0), and col 1 is low.
H2: "opponent's open line with room near the left edge" -- opponent 2+ stones in a no-X window.
H3: col-1 move attractiveness / output feature ("play col 1"), gated by col 1 height <= 1.

## Minimal pairs (act)
- 2,0,5,0,2,0 (O vertical three col 0) 3.53. Vertical threes elsewhere: col0 1.1-3.3 always fires; col6 0.15-2.06; col4/5 sometimes ~0.95; col2/3 almost never; col1 negative (-0.77; col1 height 3).
- Adding 2 stones to col 1 before (1,1,...) drops 3.5 -> 0.44; 1,1,1,6 prefix -> -0.17. 6,6 prefix -> 1.47; 3,3 prefix -> 0.02 (center stones suppress too).
- I having an immediate win kills it (3,0,4,0,5,0 -> -0.08).
- 160622 (0,0,5,3,3,3,3,x): only x=1 (O at (0,1)) fires strongly 3.96, x=3 0.97.
- 119968: O stacking vertical two on col 5 -> 6.2.

## Dev metric log
- s1 p1 (must-block & h1<=1 & no my win): F1 0.207 (P 0.177 R 0.249) AUROC 0.607, sim share 0.10.
- s2 p2 (their win cell in col 0/2 row>=2 & h1<=1 or full): F1 0.138. Worse (full col 1 and many threats without firing).
- s3 p3 (additive score: h1<=1, last_row==2, (3,2)/(3,0) threat, must-block, col0/2 threat): F1 0.249 (P 0.214 R 0.297) AUROC 0.632, sim 0.13.
- s4 p4 (any must-block or poisoned col 0/1/2/6, h1 gate incl. full): F1 0.143 (program fires 14%; too broad).
- s5 p5 (narrow left-side threats, h1<=1): F1 0.176.
- s6 p6 (p3 + harsher h1 penalty, non-central must-block only, poisoned col 2): F1 0.254 (P 0.205 R 0.334) AUROC 0.648, sim 0.12. BEST.

## Further findings
- Teacher: col 1 is NOT more often the best move in firing bands (so not a "col 1 is best" detector).
- Top activations (band 9): opponent win cell at (3,2) in 42%, usually directly above col 2's landing cell (col 2 "poisoned"), often from a diagonal (0,5)-(1,4)-(2,3)-(3,2); also opponent vertical three in col 0 (must-block (3,0)).
- Activation very sensitive to unrelated stones (e.g. adding 3,3 prefix kills 3.5 -> 0.02; single bottom-row stone swaps change 1.7 -> 0.02). Bands 5-7 (bulk of firing) show only weak single-feature enrichments. Looks like a distributed/mixed direction.
- Vertical-three must-block fires strongly in col 0, sometimes col 4-6, never col 2/3; col 1 three negative.

## Steer
- 48459: zero -> col1 -0.25, col3 +0.20. 119968: col1 -0.19. 4 low positions forced to max: col1 +0.19..+0.43. Forced must-block positions: no change.

## Synthesis (hill-climb with act)
- 1,5,6,4,2,2,0,3,3,4,4,3,3,5,4,3,4,4 -> 12.27 (beats dev max 11.27); their diag win at (3,2) directly above col-2 landing.
- 5,0,2,4,4,4,2,4,1,4,4,0,0,6,3,3,3,3,3,6,6 -> 11.55 (beats); same (3,2) poison.
- Original dev max game 11.268, 48459-variant 7.9.

## Conclusion: confidence low (best F1 0.254).
