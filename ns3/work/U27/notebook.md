# U27 notebook (layer 5, pole +, threshold 0.953, dev max 19.87)

## Observations (examples, 40 + 30/band x8)
- steer: forcing U27 high raises column 2 strongly (3,3,4,2: col2 0.26 -> 0.92); zeroing it lowers col 2 by 0.02-0.28 in top positions.
- Histogram of "length of my own run on top of column 2" rises with band: band0 2/30 >=2, band9 18/30 >=2 (none with 0 except full col).
  Same histogram for cols 1,3,4,5 flat -> col-2 specific.
- Must-block present in ~50% of firing bands vs ~25% in band 0; teacher scores in band 9 often show nearly all moves losing (critical positions).
- Several top examples share a must-block at (3,6) on diagonal (0,3)-(1,4)-(2,5).
- Col 2 full is also over-represented in band 9 (8/30).

## Hypotheses
H1: my stones stacked (>=2) on top of column 2, column not full (vertical build in col 2; strongest when 3 = immediate win).
H2: critical positions (must-block / most moves lose).
H3: random-ish direction / mixture.

## Minimal pairs (act)
- 5,1,2,4,2,4 = 6.1; nearly every one-stone change drops it below 1 (X(0,5)->(0,6) 0.74; O(0,1)->(0,0) 0.79; O col4 stack->col3 -0.3).
- 2,4,2,4 = -0.26 (only the stack); 2,4,2,4,5,1 = 6.0; 2,4,2,4,0,6 = 4.6; 2,4,2,4,6,0 = 0.0. Very context sensitive.
- 5,1,2,4,2,4,2,6 (XXX in col 2, immediate win) = 12.5.
- 4,5,6,4,2,2,4,2,5,4,5,2,x (XXX col2 win): 7-26 for every last move -> immediate col-2 vertical win is robust.
=> H1 is necessary-ish but not sufficient for run=2; run=3 (win) is robust.

## Score log
- s1 p1 (my run>=2 on top of col 2, not full): F1 0.201 (P 0.161 R 0.265) AUROC 0.612, sim share 0.25
- s2 p2 (+ vertical four must still fit): F1 0.227 (P 0.206 R 0.253) AUROC 0.612, sim share 0.31
- s3 p3 (p2 + full col 2 with my stones at rows 4,5 capped by theirs): F1 0.199 (P 0.139 R 0.352), sim 0.32
- s4 p4 (p3 gated by last move in cols 4-6, unless my open three): F1 0.189, sim 0.30 -> gate hurts
- s5 p5 (p2 + any my threat cell in col 2): F1 0.142 (P 0.085 R 0.449), sim 0.24
- p6: load error (function name contained the banned substring "open(") -> rejected before scoring; same logic renamed as p6b.py.
- s6b p6b (open three in col 2, or my stones at row idx 2,3 with idx 4 empty): F1 0.165 (P 0.355 R 0.108), sim 0.30
- s7 p7 (p2 + opponent just stacked vertically in col 5/6, col 2 non-empty): F1 0.176 (P 0.113 R 0.401), sim 0.30
Conclusion: p2 best (F1 0.227). Col 2 own vertical stack is a real but partial component (and the steer effect is +col 2);
the rest of firing is diffuse. Confidence low.
Steer: max on 3,3,4,2 col2 0.26->0.92; zero on 6 firing positions: col2 -0.02..-0.28.
Synthesis (all beat dev max 19.87): 4,4,6,5,2,2,4,2,5,4,5,2,6 (25.7); 4,5,6,4,2,2,4,2,5,4,5,2,6 (25.6); 2,5,2,6,2,4,4,6 (22.7); 2,5,2,6,2,4 (22.4); 4,5,6,4,2,2,4,2,5,6,5,2,4 (22.3).
