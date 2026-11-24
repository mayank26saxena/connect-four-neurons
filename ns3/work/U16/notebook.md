# U16 notebook (layer 4, pole +, threshold 1.462, dev max 4.663)

## Observations from examples (bands 0-9)
- Top band: last move very often col 1 (25/60) or col 6 (13/60), never col 0. Must-block very common at top
  (only ~19/60 band-9 have no must-block vs 55/60 in band 0); (1,1) most frequent, then vertical threes in col 1, col 6 tops.
- Early-game firing without any threats too (1,0,4,2,2 = 3.63; 2,0,4,0 = 2.1).
- steer: small effects (<=0.16), inconsistent direction.

## Hypotheses
H1: opponent has an immediate threat (must-block). Minimal pairs: row-0 three O at 4,5,6 (block 0,3) fires 2.8-3.0;
    three O at 0,1,2 (block 0,3) gives -2.0; vertical col-1 three in 3,1,3,1,4,1 -> -1.2. So not sufficient; side-dependent.
H2: vertical three by opponent in column 1 (top band). 1,5,1,6,1 fires 1.75, 1,3,1,2,1 = 0.24: depends on my stones
    (mine on right / not in centre -> higher).
H3: something about my stones / centre column (col 3 empty in many early firing positions).

## Minimal-pair findings
- Early game: my stone at (0,2) capped by theirs at (1,2) fires robustly (2,6,5,2 = 2.29; 1,0,4,2,2 = 3.63), but the
  same cap in other columns does not (cols 0,1,3,4,5,6 all < 1). Their stone at (2,2) or anything at (0,3) kills it.
- My X.X at (0,2),(0,4) with (0,3) empty and both (0,1),(0,5) empty fires (2,0,4,0 = 2.1); 3,0,4,6 (also a fork) does not.
- Opp row-0 three 4,5,6 open at (0,3) fires (~3); mirror 0,1,2 gives -2. Strong left/right asymmetry everywhere.
- Must-block at (1,1) (opponent plays (0,1) under its own row/diagonal threat) fires; mirror (1,5) does not.
- Opp vertical threes: 0.2-1.5 in synthetic positions (elevated but usually below threshold), depends on my stones
  (my stones in col 3 suppress it).
- Near-threshold (bands 5-6) single-cell histograms differ from bands 1/3 by at most ~10 points: no strong board signal.
- steer: changes almost always < 0.05; occasional 0.1-0.16 swaps between two candidate columns, no consistent direction.

## Dev metric
- s1 p1 any must-block: F1 0.130 (P 0.078 R 0.386) AUROC 0.623, sim share 0.01
- s2 p2 edge vertical three | must-block (1,1) | cap2: F1 0.240 (P 0.198 R 0.304) AUROC 0.633, share 0.02
- s3 p3 block-on-top-of-last-move | cap2: F1 0.145 AUROC 0.651
- s4 p4 must-block in col 1 | col-6 vertical three | cap2(col3 empty): F1 0.244 (P 0.213 R 0.287) AUROC 0.627, share 0.02  <- best
- s5 p5 p4 variants + edge verticals 0/5: F1 0.223
Conclusion: a diffuse, column-asymmetric mixture; no single board concept. Confidence low (possible random direction).

## Synthesis
Prefix B = 3,2,2,5,2,6,3,3,5,2,3,3,3,2,0,2,0,6,6,5 (dev pos 76539 minus last move). B,4,0,1 = 5.23 (beats dev max 4.66);
B,4,0,5,6,1 = 5.12; B,4,0,6,5,1 = 4.87; B,4,0,5,5,1 = 4.69. All: opponent drops a stone at (0,1) beneath its own
row-1 threat at (1,1).
