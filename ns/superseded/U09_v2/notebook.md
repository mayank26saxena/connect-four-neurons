# U09 notebook (layer 4, pole -, threshold 0.909, dev max 14.55)

## Exploration
- Top examples (5-14): opponent (O) stones massed in lower-left-center, esp. (2,2), (1,3), (2,1), (1,2); many have their threat at (3,1)/(3,0)/(4,0) on the anti-diagonals (3,1)-(2,2)-(1,3)-(0,4) and (3,0)-(2,1)-(1,2)-(0,3).
- Cell histogram (420 firing vs 100 nonfiring examples sampled): O(2,2) 64% vs 29%; O(1,3) 58 vs 34; X(2,2) 8 vs 17; X(1,3) 15 vs 32; X(0,4) 18 vs 48; O(3,1) 31 vs 11; O(2,1) 35 vs 17.
## Hypotheses
- H1: O occupies (2,2) plus support on the anti-diagonal / col 2 (O mass in rows 0-2, cols 1-3).
- H2: opponent threat cell at (3,0)/(3,1)/(3,2)/(4,0).
- H3: forced/many-losing-moves position (teacher scores) - many top examples have only one non-losing move.
## Minimal pairs (act)
- 142409 base (13 ply) last move alternatives: O to (2,1) -> 14.2; other columns ~2; O to (3,3) -> -0.5.
- 15848: only last move O->(2,2) fires (5.6); any other column ~0.
- Opp vertical three, open top, in col c (5-ply): c0 1.29, c1 -0.08, c2 4.69, c3 0.83, c4-6 ~0. Col2 vertical three capped by X: -0.48. Two in col 2: -0.2. Three at rows1-3 of col2 (X at bottom): 4.4.
- O anti-diagonal (0,4),(1,3),(2,2), (3,1) empty, col1 empty: 0.0; col1 filled to make (3,1) a must-block: 0.47-1.10. So H2 alone weak.

## Dev metric log
- call 1 (accidental duplicate run of p1) / call 2 p1: O(2,2)&O(1,3) -> F1 0.141 (P .095 R .275) AUROC .60, sim -0.01.
- call 3 p2: any opp threat cell in {(3,0),(3,1),(3,2),(4,0),(2,3)} -> F1 0.125 (P .073 R .458). Threat location alone is weak.
- call 4 p3: opp open vertical three in col 2 OR (O at (2,2)&(1,3), (0,4),(3,1) not mine) -> F1 0.206 (P .192 R .223), AUROC .60. BEST.
- call 5 p4: hand-weighted O/X cell sum from minimal pairs -> F1 0.180.
- call 6 p5: O(2,2) + O(1,2)|O(1,3) + >=3 cluster stones, (0,4) not mine -> F1 0.128.
- call 7 p6: p3 OR O(2,2)&>=5 O in box rows0-2 cols1-3 -> F1 0.137.

## More minimal pairs
- O triangle (1,2),(1,3),(2,2) over my (0,2),(0,3): 2.16 fires. Shifted one column left/right: ~0. Very location specific.
- From that base, a single X at (0,4), (0,1), (2,3) or (3,2) kills it (<0.3); O at (0,1) raises to 3.9.
- O pair (1,2),(2,2)+(0,3): 0.45 with my stones on col 6, 2.19 with my stones on col 5, 0.13 on col 0 -> strong, idiosyncratic context dependence.
- Dense O blob (0,2),(1,2),(2,2),(0,3),(1,3),(1,1),(2,1): 14-21 (synthesis).
- Random self-made games: last move landing on (2,2) fires 9/53; 27% of all fires.
- Many misses are lost/near-lost positions (teacher scores ~-980 for most moves, multiple opp threats) with no cluster at (2,2).
## Steer
- Effects small, <=0.15 probability, inconsistent: 2,2,3,3,6,2 max -> col4 +0.14, col1 -0.15; 10028 max -> col5 +0.13, col3 -0.10; others ~0.
## Conclusion
Looks like a mixture / possibly a random direction: strongest drive is opponent stones massed at (2,2) and the cells around it (cols 1-3, rows 0-2), especially with col-2 vertical three or (2,2)-(1,3) diagonal, but highly context-dependent and best F1 is 0.21. Confidence low.
