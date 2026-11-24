# U78 notebook (layer 1, pole +, threshold 0.388, dev max 2.132)

## Observations
- Examples: firing is dominated by the opponent's LAST move: last col 3 (78/150 of band 9) and col 0 (45/150); col 1 enriched near threshold (bands 5-6).
- Last-move cell histogram band 9: (1,3) 52, (1,0) 21, (2,3) 20, (0,0) 13, (0,2) 11, (2,0) 11, (3,4) 11.
- Activation alternates ply-to-ply within a game (fires only after one player's moves at a time) -> last move dominates.
- Same board reached in different move order gives different activation (e.g. 6,6,2,6,3 1.76 vs 6,6,3,6,2 1.25): order/last-move sensitive.
- Context modulates: e.g. base 6,3,2,6,3 = 1.60; removing O at (0,6) (5,3,2,5,3) 0.15; O at (0,1) instead of (0,2): -0.15. O at (0,1)/(0,4) lowers, O at (0,2) raises.

## Hypotheses
H1: fires when last (opponent) move lands at one of a few cells: (1,3),(2,3),(0,0),(1,0),(2,0),(0,2),(3,4).
H2: H1 plus context: opponent stone at (0,2) / O-O horizontal pair in cols 2-3 near bottom, col 4 low.
H3: generic "opponent two-in-a-row near bottom left-center" (diagonal (0,2)-(1,3), horizontal (0,2)-(0,3)).

## Tests and score calls
- score 1 (p1, last-move cell lookup): F1 0.101, P 0.059, R 0.359, AUROC 0.595, sim share 0.01. Last-move cell alone is far too broad.
- Minimal pairs (act): in short games the unit behaves like an additive vote over the stones/move tokens: their stones in col 2 (strongest) and 3 (and 0) raise it, their stones in col 1 lower it strongly; my stones in col 6 (and 1) raise it, mine in col 0 lower it. Each extra stone dilutes it (prefixing 4,4 drops 1.76 -> 0.55; cols 4/5 stones kill it). Last move into col 1 is strongly negative.
- Mirror test: 0,3,4,0,3 = 0.02 vs 6,3,2,6,3 = 1.60 (not symmetric).
- Order matters: same board via different move order differs (1.76 vs 1.25), and in longer games the last-move effect changes sign with context (e.g. last col 5 best in one 35-move game, col 0/6 best in another).
- score 2 (p2, column-count template / ply + last col): F1 0.158, AUROC 0.562, share 0.06.
- score 3 (p3, act-derived column weights, mean over stones + last col): F1 0.145, AUROC 0.627, share 0.08.
- score 4 (p4, cell template from single-cell band histograms): F1 0.152 (P 0.33, R 0.10), AUROC 0.602, share 0.07.
- score 5 (p5 = p4 + last-move column + my-last-move column): F1 0.181, AUROC 0.690, share 0.08.
- score 6 (p6 = p5 + their previous move column, weights from act scans): F1 0.207 (P 0.256, R 0.174), AUROC 0.688, share 0.09. Best. Stopped here; 2 calls unused.
- Steer (zero on 5 firing positions, max on 3 non-firing): changes <= 0.09 in probability; the largest was +0.04 to col 4 / -0.04 col 1 in 2,6,6,6,3. Effectively no measurable effect.
- Synthesis: 6,1,2,6,3,6,3 reaches 2.132 (= dev max, not above); 6,1,3,6,2,6,3 2.121; 6,6,2,1,3,6,3 2.117; 0,6,3,6,2,6,3 2.094; 6,6,2,6,3,1,3 2.085.

## Conclusion
Layer-1 unit that looks like a diluted, order-sensitive vote over the move history rather than a board concept. Best F1 0.21 -> confidence low. Could be a random direction or a mixture.
