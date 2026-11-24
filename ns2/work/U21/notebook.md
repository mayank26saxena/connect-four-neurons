# U21 notebook (layer 2, pole +, thr 0.845, dev max 1.927)

## Observations
- Firing examples skew strongly to early game (band 9: 131/150 have ply < 12) and to boards with empty columns
  (col 1 empty 81/150 in band 9 vs 22/150 in band 0; col 5, 0, 2 similar).
- steer max/zero on 4 positions: change <= 0.01 on every column -> no measurable effect.
- Minimal pairs are erratic: 6,4,4,4 = 1.66 but 6,3,3,3 = -0.36; 3,6,6,3,3,4 = 1.86 but 3,0,6,3,3,4 = 0.26;
  4,1,2,2,3,5 = 1.58 but 4,1,2,0,3,5 = 0.09. Single stones swing it by >1.5 with no consistent tactical meaning.
- Per-cell histograms band 9 vs band 0: weak checkerboard tendency in cols 3-4 (me on (1,4),(0,3),(2,3),(3,4); them on (1,3),(2,4)),
  but col 6 goes the other way and minimal pairs (3,3,3,4,4,4 only 0.86; 4,1,2,2,3,5 mostly 'wrong' cells yet 1.58) contradict it.

## Hypotheses
H1: early game / many empty columns (generic sparsity).
H2: checkerboard colouring of cols 3-4 (rejected by minimal pairs).
H3: no clean concept (random direction or mixture).

## Score calls
1. p1 early game & >=2 empty columns: F1 0.092 (P 0.052 R 0.413) AUROC 0.585, sim share -0.00.
2. p2 column-height shape (col1/col5 empty, col3 h3-4, col4 h3, col6 h2/4, col0 h1): F1 0.099, AUROC 0.560, sim -0.12.
3. p3 checkerboard colouring of cols 3-4: F1 0.061, AUROC 0.512 (chance). H2 rejected.
4. p4 last-move cell in {(3,6),(2,0),(2,4)} (level adds (1,6),(0,5),(0,6),(4,3)): F1 0.116 (P 0.081 R 0.203), AUROC 0.564, sim -0.03. BEST.
   (From a plain histogram of last-move cell by band: firing is 2.5-4x enriched for those cells.)
5. p5 last stone caps a their/mine/their sandwich in its column: F1 0.051, AUROC 0.477 (chance).

## Minimal pairs on the last-move idea
- Col 6 = them, me, me, them (last at (3,6)) recurs in top examples (66035, 129256, 74715); 3,6,6,3,3,4,6,6 = 1.951.
  But the same column pattern in other contexts gives 0.42-1.30, so it is context dependent.
- Col 0 = three of theirs (last (2,0), must-block) recurs in top examples; constructed versions give 0.38-1.01.

## Effect (steer)
- 5 positions, max and zero: every column changes by <= 0.02. None measurable.

## Synthesis
- 3,6,6,3,3,4,6,6 = 1.951 beats dev max 1.927. 3,6,6,3,3,4 = 1.864, 3,6,6,3,3,5,6,6 = 1.764, 6,4,4,4 = 1.663.

## Conclusion
No clean concept. Firing is skewed to early, sparse boards and to a few last-move cells, but single stones swing it
by >1.5 with no consistent tactical meaning and every rule tried is near chance. Likely a random direction or mixture. Confidence low.
