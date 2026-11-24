# U52 notebook (layer 1, pole +, threshold 0.572, dev max 1.398)

## Exploration
- ~300 firing examples (bands 5-9): 68% at ply <= 8; top band almost all ply 2-9 (e.g. 1,0,0; 4,4,4,4; 3,3,3,3; 2,0,0).
- No single last-move cell dominates: (2,3),(0,1),(0,6),(1,0),(3,3),(0,0),(2,2),(4,4) all common.
- "last move on same column as previous move" 37% of firing vs 15-33% in lower bands: weak.
- Ply-2 act table: value mostly set by last move column: col 3 ~ -1.2, col 4 ~ -0.5, col 6 ~ +0.6, col 2/5 ~ +0.45.
  But col 3 row 0 late in a game (ply 19) gives +0.8: ply interacts.
- Late-game fires (25228, 160921, 70873) all have column 4 empty; adding one stone to col 4 drops 0.58 -> 0.16.
  But 4,4,4,4 fires at 1.16 (col 3 empty there), and 3,3,3,3 fires (col 4 empty).
- steer max/zero on 7 positions: change <= 0.01 everywhere. No measurable effect.

## Hypotheses
H1: early game (ply <= 6) and the last move was not on the bottom of a center column (3 or 4).
H2: column 3 or column 4 is empty (center column untouched), stronger early.
H3: random direction / mixture of last-token-column x ply x column-occupancy; no clean concept.

## Dev metric log
1. h1 (ply<=6, last move not center bottom): F1 0.195 (P 0.12, R 0.54), AUROC 0.71, sim share 0.01.
2. h2 (col 3 or 4 empty, ply<=10): F1 0.195 (P 0.12, R 0.63), AUROC 0.74, sim 0.02.
3. h3 (ply<=9, last move off-centre, or col 3/4 stacked row>=2): F1 0.220, AUROC 0.77, sim 0.06.
   act checks: x,3,3,3 fires for every x tried (0.58-0.99); x,4,4,4 does not (0.15-0.39), 4,4,4,4 does -> col 4 needs row>=3.
   With a stone at the bottom of col 3 or 4, off-centre last moves go negative (3,4,1 -0.13; 2,4,6 -0.40).
4. h4 (col 3 row>=2 / col 4 row>=3 stacking early, or early game with cols 3 and 4 empty and last move in 0,1,2,6): F1 0.284 (P 0.19, R 0.55), AUROC 0.74, sim 0.05. BEST.
5. h5 (h4 + ply>=24 with col 4 empty, ply cap 16): F1 0.219. Worse; reverted to h4.
Ply-3 tables (7 contexts x 7 moves) show strong, irregular context dependence; no clean rule. Stopped scoring at 5/8.

## Steering
steer max/zero on 7 positions (early and late): every column changes by <= 0.01. No measurable effect.

## Synthesis
4,4,4,4,4 -> 1.413 (beats dev max 1.398); 2,4,4,4,4,4 -> 1.406 (beats); 2,4,1,4,4,4,4 1.378; 2,1,4,4,4,4,4 1.331; 4,1,4,4,4,4 1.243.

## Conclusion
Low confidence. Mostly early-game unit with an irregular dependence on the last move and on centre occupancy, best rule F1 0.28;
no steering effect. Consistent with a random direction or a mixture.
