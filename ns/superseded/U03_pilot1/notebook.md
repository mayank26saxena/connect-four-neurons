# U03 notebook (layer 4, pole +, thr 0.821, dev firing 3.0%, dev max 12.2)

## Observations (examples, 40 + band 9 x16, plus 1860 sampled across bands/seeds in ex/)
- Top band (>4.8) is dominated by sparse early positions (ply 4-10), me to move, centre column 3 (or 4) empty or low,
  opponent's last stone often stacked on a stone (row 1-2). Below the top, firing positions look diverse (mid/late game).
- Engine/tactics: no consistent immediate win/must-block pattern.

## Hypotheses
- H1: I have an open horizontal two on the bottom row (window with >=2 mine, 0 theirs). Local weighted F1 ~0.15. Rejected.
- H2: early game (ply<=10) and column 3 empty/low. Local weighted F1 ~0.2.
- H3: opponent just stacked on a stone early in the game. Weak (rate 4-7%).

## Minimal pairs (act)
- 1,6,2,x: x=1 6.3, x=5 7.0, x=6 5.4, x=0 3.0, x=2 1.8, x=3 0.7 (blocking (0,3) kills most of it).
- 2,1,x,1: x=5 8.1, x=3 6.6, x=4 3.2, x=0 2.2, x=6 1.9, x=1 -0.03. 2,1,5,1 vs 5,1,2,1 same (order-independent).
- Any further stone by me (5th move) drops it to ~0 (5,1,2,1,+3/4/0 -> 0.2/0.3/0.0).
- X at (0,2),(0,3) bottom (2,6,3,x) ~0; X at (0,3),(1,3) ~0.
- Responses are large but not organised by any single board concept I could find.

## Feature scan
- Per-cell firing rates (mine/theirs/landing) all within 0.4-7%; no cell is strongly diagnostic.
- Counts of threats, playable wins, empty columns: max rate ~9% (4 empty columns).
- Gradient-boosted classifier on cells+landing+last-move+ply (5-fold CV, weighted to dev mix): F1 ~0.25.
  Even a flexible model over board features cannot predict firing well -> likely a random direction / mixture.

## Steer
- 1,6,2,1 (6.3->0): no change. 5,1,2,1 (8.3->0): col4 +0.05. 4,5,6,4,2,2,4 (5.7->0): col2 +0.06.
- to max on 3,3,4: col2 +0.05/col5 -0.05; on 1,3,3,6,...: col3 +0.06, col1 -0.06; two others 0.

## Dev metric
- call 1 p1.py (ply 3-10 and column 3 empty): F1 0.213 (P 0.156 R 0.335) AUROC 0.638; sim share 0.03.
- call 2 p2.py (broader: col3 height<=1, graded level): F1 0.192, AUROC 0.661; sim 0.02. Broader rule adds FPs.
- call 3 p3.py (p1 fires, level focused on very early + stacked last move): F1 0.213; sim 0.03.
- Mid/late firing examples often have threat cells in column 3 above the landing cell, but this rule alone: local F1 0.06.
- Bottom-row immediate win for me: local precision ~0.6 but recall 3%.
- call 4 p4.py (p1 OR my bottom-row immediate win; level adds bottom-row three-maker): F1 0.226, AUROC 0.651; sim 0.02. Best.

## Synthesis (act-guided search over 4/6/8-move games)
- 5,5,2,5,4,0 -> 15.88 (X .X X on bottom, O stacked in col 5, I can win at (0,3)); 5,5,2,5,3,0 -> 13.53; 5,5,2,5,1,1 -> 12.91.
  All three beat the dev max 12.22. 5,5,2,5,4,0,6,4 -> 11.18.

## Steer
- Zeroing at 15.9 / 13.5 / 8.3 / 6.3: no change in move probabilities (model already ~certain). to-max: at most +-0.06.

## Conclusion
- No simple description exceeds F1 ~0.23; a boosted classifier on board features gets ~0.25 in CV. Strongest activations
  are sparse early games (centre column empty, my bottom-row stones building toward a horizontal three/four through col 3/4),
  but most firing mass is spread over unremarkable positions. Confidence low; possibly a random direction or mixture.
