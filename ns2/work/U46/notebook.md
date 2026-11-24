# U46 notebook (layer 0, pole -)
## Examples
Top bands: almost all ply 27 (odd, second player to move), any last col; also ply 4 with last move col 5.
Trace over one game: fires at ply 25,27,29,31 (odd), peak 27; even plies negative.
H1: positional: odd ply in 25-31 (peak 27), modulated by last col.
H2: ply 4 with last move in col 5 (early opening token).
## Score 1 (p1: ply in 25/27/29/31 or ply4 & last in 5/6): F1 0.323 (P 0.20, R 0.82), AUROC 0.86, sim share 2.47 (weird >1)
Ply alone too broad. Substitution sweeps at ply 27: single moves change act by <=0.002; two ply-27 games differ 0.006 vs 0.001
-> cumulative, column-count (= heights) dependent. Mirroring changes it -> asymmetric.
Band histograms at odd late plies: firing = tall cols 3,4 (2,5), short cols 0,1; last move 4/6 favoured, last move 5/3 disfavoured.
Ply 4: last move col 5 with no stone in col 4/6 earlier.
H3: odd ply 25-31 and s=(h3+h4)-(h0+h1) above ply-specific threshold (27 lowest), adjusted by last col.
## Score 2 (p2: s=(h3+h4)-(h0+h1), last-col adj, ply-specific base; ply4 last5): F1 0.556 (P .61 R .51) AUROC .75 sim 1.69
## Score 3 (p3: add cols 2,5 positive, h6 negative, double weight 0/1): F1 0.514 (P .45 R .60), sim 0.86. Worse.
Misses incl. ply-4 games like 6,1,3,5 (my h6==0 condition was wrong).
Ply-4 sweep of all x,y,z,5: additive; earlier stones in col 4 (and 5) suppress, cols 0-3 support. Never fires without last=5 except some last=6.
Steer (3 positions, max and zero): zero change in move probabilities (<0.01). Effect none measurable.
## Score 4 (p4: weighted 2h3+h4+h5-h0-2h1-h6, early graded by h4/h5): F1 0.512 (P .42 R .66), sim 0.65. Worse; more weights do not help.
Back to p2 late rule; fix early rule to simply ply 4 & last move col 5.
## Score 5 (p5 = p2 with early rule = ply4 & last col 5): F1 0.573 (P .60 R .55) AUROC .77, sim share 1.70
## Score 6 (p6 = p5 + ply 33 base -2): F1 0.575 (P .60 R .56) AUROC .77, sim share 2.54. Best; final program.
Synthesis: at ply 27, substituting my (second player's) moves with col 5 raises act to 0.008-0.009, but several such
sequences contain a completed four; searching for legal variants above dev max 0.008.
Interpretation: layer-0 unit; mostly a position (move-count) detector for ply 27 (and 25/29/31, ply 4 after a col-5 move),
modulated by how many moves went into each column (centre 3/4 tall, 0/1 short) and the last move's column.
No measurable steering effect. Doubt: may be a random direction; the "board" part is really token-frequency.
Synthesis: greedy one-move searches from three 0.008 bases; every 0.009 variant completes a four (col-5 stacking). Best legal = 0.008 (ties dev max). Hand-built full-centre games only 0.004-0.005.
Final: p6. Confidence low-medium -> medium? F1 0.575 but rule is mostly a move-count (ply) lookup plus token-frequency modulation, no steering effect -> choose low.
