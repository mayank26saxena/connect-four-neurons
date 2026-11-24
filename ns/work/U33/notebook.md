# U33 notebook (layer 2, pole +, thr 0.521, dev max 8.04, rate 3%)

## Observations
- Top band (9): 43/60 last move col 6; 26/60 must-block (3,6) = opponent vertical three at bottom of col 6.
- Bottom-row histograms: band 9 -> (0,6)=O 55/60, (0,5) empty 54/60, (0,3)=X 43/60. Band 0 no such skew.
- Bands 5-6 (threshold): skew weaker, (0,6)=O ~50%.
- Ply mostly 5-15.

## Hypotheses
H1: opponent owns bottom of column 6 (O at (0,6), ideally stacked), (0,5) empty; strength rises with O stack height in col 6.
H2: also needs no opponent stones elsewhere on bottom row (O at (0,0),(0,1),(0,4),(0,5) kill it in minimal pairs).
H3: mixture / random direction (col6 component + noise).

## Minimal pairs (act)
- 6,3,6,3,6 4.06; 6,2,6,2,6 4.74; 6,5,6,5,6 2.13; 6,0,6,0,6 2.66 (O three in col 6). Same in cols 0,2,3,4,5: no fire. Mirror col 0: no.
- O three at rows 1-3 of col 6 (6,6,0,6,0,6): 0.39 -> needs bottom.
- X owning col 6 stack: no fire. Parity matters: O (just-moved side) must own col 6.
- 6,3,6 (O two stacked) 0.73 fires; 6,3,6,3 + O at col 2 2.33, col 3 3.64, col 4 -0.52, col 1 -0.38, col 0 -1.50, col 5 (6,3,6,3,5) -0.77.
- 2,2,3,6 2.77 vs 2,2,3,5 0.50 / 2,2,3,4 0.89 / 2,2,3,0 -0.03 / 1,1,2,6 -0.57 / 0,0,1,6 -1.58 / 3,6 0.31 / 2,6 0.73.
- steer to zero on firing positions: no change; to max: tiny (<=0.1).

## Dev metric log
- p1 (O at (0,6), (0,5) empty, (0,4) not O): F1 0.164 P0.13 R0.22, sim share 0.02.
- p2 (opponent vertical three, cols except 4/5, or O pair at col 6 bottom): F1 0.174 P0.125 R0.29, sim 0.01. (call 3 was an accidental rescore of p2, same numbers.)
- More minimal pairs: vertical O threes fire in cols 0,1,2,3,6 depending on my stones, never in 4/5 -> threat itself is not the concept.
- Cell histograms bands 7-8 (80 each): col 5 nearly empty (row0 X5/O5 vs ~30 in band 0), col 6 only O (X at (1,6) 0), X at (0,3)/(1,3) high, O at (1,2) high, col 1 often empty, X at (1,4).
- p3 hand additive (col6 O stack, X(0,2),(0,3)): F1 0.188.
- p4 (col5 empty & col6 only O & X(0,3)): F1 0.186, sim 0.08.
- p5 additive score from histogram cues (col5 empty, col1 empty, col6 O-only count, X(0,3),(1,3),(1,4), O(1,2), ply<=14), thr 3.8: F1 0.197 P0.63 R0.12, sim 0.14.
- p6 = p5 thr 3.0: F1 0.344 P0.36 R0.33, AUROC 0.65, sim share 0.14. BEST.

## Steer
- zero on 2,2,3,6 / 6,5,6,2,6 / 6,3,6,3,2,0,6: no change. zero on 2,2,3,6,3,6,0,6: col1 +0.08, col4 -0.08. max on 4,2,6,4,1,2,4: col3 -0.10, col5 +0.06; on 3,3: <=0.02. Effect weak.

## Synthesis
2,2,3,6,3,2,0,6,4,6 10.01; 2,2,3,6,3,6,0,6 9.95; 3,2,3,6,2,6,0,6 9.39; 2,2,3,6,3,6,4,6 8.65; 6,3,2,3,6,2,6 8.62 (dev max 8.04). Recipe: opponent stacks three in col 6, I hold (0,2),(0,3),(1,3), col 5 empty.

## Conclusion
Peak is clear (opponent stack in col 6 + my centre-bottom stones + empty col 5), but most firing is diffuse; looks like a distributed/mixture direction. Confidence low.
