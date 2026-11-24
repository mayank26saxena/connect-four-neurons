# U19 notebook (layer 3, pole -, threshold 0.798, dev max 13.95)

## Exploration
- Examples: many early-game firings; top ones have opponent (O) stone at (1,5) sitting on my X at (0,5).
- Minimal pairs: c,c for all columns -> only 5,5 fires (1.24). 3,5,5 = 4.7; 3,5,5,5 (X fills (2,5)) = 0.01. So O at (1,5) with (2,5) empty is key.
- 2,5,3,4,{c}: c=5 (O at 1,5) 8.7; c=4 (O at 1,4) 0.04; c=3 6.6; c=2 3.0. O at (1,4) kills it.
- Secondary: O at (0,2)+(0,3) with my X at (0,5): 2,5,3 = 1.5.
- Late-game firings: often O at (1,5) (with (2,5) filled, e.g. 141343 at 7.7), and also late positions with an almost-empty column 3 / 2.
- Not value: teacher score does not track activation.
- Hist (240 hi vs 180 lo): O(1,5) 66% vs 24%; O(1,5)&(2,5) empty 43% vs 4%.

## Hypotheses
H1: O stone at (1,5) with (2,5) empty (column 5 = X then O, landing row 2).
H2: weighted bag of O stones on rows 0-1 cols 2-5 (O at (0,2),(0,3),(1,3),(1,5)), minus O at (1,4).
H3: late-game component: column 3 (centre) nearly empty late.

## Score calls
1. p1 O(1,5) & (2,5) empty: F1 0.155 (P 0.11, R 0.27), AUROC 0.60, sim 0.07.
2. p2 hand-weighted cells (no (1,4) gate): F1 0.159, AUROC 0.65, sim 0.04.
3. p3 opponent line potential through (1,4): F1 0.118, AUROC 0.60. Worse; row-1 threats elsewhere (cols 0-3, 3-6) do not fire at all in act tests.
4. p4 weighted cells gated on (1,4) empty: F1 0.208 (P 0.19 R 0.22), sim -0.79 (bad level).
5. p5 = p4 + (0,6) empty/X(0,4) weights, level only above threshold: F1 0.225 (P 0.30 R 0.18), AUROC 0.58, sim 0.01. BEST.
6. p6 = p5 OR late rule (ply>=18, O(1,5), >=3 O on row 1): F1 0.150. Rejected.

## Key minimal pairs
- 2-ply grid: only 5,5 fires; O at (0,3) gives +0.3..0.9 everywhere.
- X(0,5),O(1,5)+O(0,c): c=3 4.7, 4 3.3, 2 3.1, 0 1.8, 1 1.2, 6 0.7.
- Filling (1,4) by either side kills it (8.7 -> 0.9 with X, 0.04 with O). Filling (2,5) kills (4.7 -> -0.07 X, 0.27 O). Any stone at (0,6) cuts 4.7 -> ~0.6-0.8.
- O at (1,2)/(1,3) adds: 2,5,3,4,5,0,3 = 11.5; +0,2 = 16.6 (O then has a playable win at (1,4)).
- Same O row-1 three with hole (1,4) but (1,4) not playable: 0.44; row-1 threats at other holes: ~0.
- Late game: activation jumps on single moves and resets, many late firings break the (1,4)-empty rule (e.g. (1,4) X or O). Not captured.
- Move order mostly irrelevant for the core pattern (permutations of the same board 6.5-9.1), but 2,5,3 (1.49) vs 3,5,2 (0.65).

## Effect (steer)
3,5,5,4,2: max -> col3 -8, col1 +6; zero -> col3 +12. 2,5,3,4,5: max col3 -9, col1 +5; zero col3 +17. Late game / forced positions: ~no change.

## Conclusion
Core early-game pattern is clear (opponent stone on top of mine at (1,5), (2,5),(1,4),(0,6) empty, opponent at (0,2),(0,3),(1,2),(1,3)), but it explains only ~20% of firing; late-game firing is diffuse. Looks like a mixture -> confidence low.
