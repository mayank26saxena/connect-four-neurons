# U89 notebook (layer 2, pole +, thr 0.676, dev max 9.70)

## Observations
- Top examples: opponent (O) stones on the anti-diagonal (0,4),(1,3),(2,2) pointing at (3,1); column 1 mostly empty.
  Many top boards have their_threat (3,1).
- Cell histograms (top bands vs low): O(0,4) 85% vs 38%; O(1,3) 55% vs 42%; O(2,2) 40% vs 21%; X(0,5) 69% vs 33%; (0,1) empty much more.
- Minimal pairs (5-stone base 0,5,3,2,4 = 3.27): moving O off (0,4) -> 0.0; off (0,3) -> 0.2; O(0,0)->O(0,6) -> 0.0.
  X(0,5) -> elsewhere reduces (0.9). (0,3)+(0,4) O with X(0,5) fires robustly with most other stones.
- 9544 (5.8): O on (0,4),(2,2) and (0,3); X filling col1 kills (-0.06). Their must-block (vertical) gives -0.38.
- Mirror images (diag toward (3,5)) do NOT fire: side-specific.

## Hypotheses
H1: opponent building the anti-diagonal (0,4)-(1,3)-(2,2)-(3,1) (+ row-0 pair (0,3),(0,4)), with col 1 empty/unblocked.
H2: generic "opponent has stones at (0,4) and (0,3)/(1,3)" additive score.
H3: their threat at (3,1).

## Score 1 (p1: weighted anti-diagonal cells + threat(3,1)): F1 0.173, P 0.10 R 0.52, AUROC 0.69, sim share 0.05. Too many late-game FPs.
## Score 2 (p2: same with col-1 height multiplier): F1 0.237, P 0.19, R 0.31, sim 0.04.
- Ply/col-1 histogram: top bands are early game (ply<12), col 1 nearly empty (mean height 0.2 vs 3.0 in band 0).
- Sweep of all 210 row-0 5-stone positions (3 O, 2 X): top = O.XOOX. 3.28, O..OOXX 3.17, XO.OOX. 2.52, X..OOXO 2.33, OX.OOX. 2.24.
  => core pattern: opponent pair at (r,3),(r,4) capped on the right by my stone at (r,5). Mirror (pair at 2-3 capped at 1) does not fire.
- Re-reading misses: many have the same O-O-X pattern at cols 3-5 in row 1 or 2 (58569, 55007, 19716, 16380).
H4: opponent horizontal pair on columns 3-4 in some row, my stone at column 5 in that row.

## Score 3 (p3: O-O-X at cols 3-5 in any row, col-1 multiplier): F1 0.108, AUROC 0.55. The row-0 motif does not generalize to other rows/contexts.
## Score 4 (p4: hand-weighted cells chosen from early-game single-cell histograms): F1 0.260 P0.28 R0.24 AUROC 0.61, sim 0.07.
- Early-game cell histograms (ply<=16, top vs low bands): O(2,2) 39 vs 8%, X(1,2) 47 vs 18, O(0,4) 82 vs 43, X(0,5) 63 vs 32, O(0,0) 56 vs 30, O(1,3) 51 vs 26; col 1 nearly empty.
- Minimal pairs on 156920 (3.98): removing any one of X(0,2)/X(1,2)-under-O(2,2), O(0,0), O(0,3), O(1,4) drops it to ~0.5-1.2 -> conjunctive, many-part pattern.
## Score 5 (p5: gate ply<=18, O(0,4), col1 height<=1; points for X(0,5), O(1,3), O(2,2), X(1,2), O(0,0)): F1 0.262, sim 0.09.
## Score 6 (p6: two motifs, row-0 OOX and col-2 X-under-O): F1 0.226. Worse.
## Score 7 (p5 with threshold 2): F1 0.290 (P 0.24, R 0.36), AUROC 0.66, sim share 0.09. BEST.
- Steer: tiny effects (<= 5-7 points), shuffles probability between the top 2 candidate columns; no consistent column.
- Synthesis: order search on the core board; 0,2,0,2,4,5,4,0,3,5,0,6,2 = 9.97 and 0,2,0,2,4,5,4,0,3,5,0,0,2 = 9.92 beat dev max 9.70.
Conclusion: unit is a conjunctive/distributed early-game pattern on the lower left-centre; no simple rule above F1 0.3. Confidence low.
