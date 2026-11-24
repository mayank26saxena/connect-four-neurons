# U39 notebook (layer 4, pole -, thr 0.657, dev max 17.4)

## Examples (ex1, ex2, band 9)
- Firing is overwhelmingly early (ply 4-10), left-centre. Typical top: col1 height 2, col3 height 2, col0 empty, col2 height <=1.
- Common motif: stones at (1,1) and (1,3) of opposite colours, (1,2) empty (often the col-2 landing cell).
- Late-game firing is weak (band 5-6) and varied.

## Hypotheses
H1: (1,1) and (1,3) filled with opposite colours and (1,2) empty -> fires.
H2: relative colours matter: (1,1)=me,(1,3)=them,(0,2)=me strongest (base 3,1,1,3,2,6 = 10.3; 3,3,2,1,1,5 = 15.9).
H3: random/mixture direction.

## Minimal pairs (act)
- 3,3,2,1,1,x fires for every x (5-16). Moving X off (1,1): 1.3-3.2. O(0,1)->X: 1.0.
- 3,1,1,3 + (2,6)=10.3, (6,6)=2.1, (5,6)=4.1.
- 3,1,1,3,2,6 + 6 (O to move, X now at (1,6)) -> -0.2 ; +6,6 -> 4.3. Strong parity/side dependence.
- Mirror 3,3,4,5,5,1 = 1.6: left side specific.
- steer: zeroing lowers col 3 by 5-8 points, small effect.

## Score calls
- s1 p1 (absolute colours P1@(1,1), P2@(1,3), (1,2) empty): F1 0.090, AUROC 0.54, sim share 0.01.
- Cell histograms by band (ex3, 400 examples): firing enriched for me@(1,1) 49% vs 24%, them@(1,3) 60% vs 34%, me@(0,3) 65% vs 43%, me_first 72% vs 57%, sparser boards. So colours are relative to the mover.
- s2 p2 (relative conjunction me(1,1)&them(1,3)&(1,2) empty): F1 0.109, sim 0.07.
- s3 p3 (additive score of those cells + me_first + ply<=12 + col0 empty, fire >=7): F1 0.186 (P 0.16, R 0.22), AUROC 0.59, sim share 0.10. BEST.
- s4 p4 (stricter additive, >=8): F1 0.158.

## Other tests
- Motif is location-specific: shifted one column left/right or mirrored gives ~0 to 1.6.
- Near-threshold firing (bands 5-6) is diffuse: no shared pattern found (looked at "well" columns, flanked landing cells; act tests did not support them).
- Move order matters at the top: same 6 stones give 16.2-17.5 depending on order.
- steer: at the strong motif, zeroing moves ~5-8 points off column 3; driving to max on weak positions raised col 3 (+35 in one case, taking from col 2) or col 1/5 elsewhere; mostly negligible.
- Synthesis: 3,1,2,5,1,3 = 17.525 and 2,1,3,5,1,3 = 17.416 beat dev max 17.409.

## Conclusion
Top tail is a clean early-game motif in columns 1-3; bulk of firing near threshold unexplained. Confidence low.
