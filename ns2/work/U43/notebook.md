# U43 notebook (layer 5, pole +, thr 0.312, dev max 4.169)

## Observations
- Top bands (8-9): col 6 rows 2-5 always empty (heights[6]<=2), (0,3)=O 75%, (1,4)=O 62%. Mostly early/mid game.
- Steer: effect negligible (<0.03 everywhere; max-steer slightly lowers col 6 in one position).
- Minimal pairs on 3,2,6,3,2 (1.43): needs O at (0,3), O at (0,6), O at (1,2) on X(0,2); X at (0,4) or (0,5) kills; X elsewhere fine.
- 6,6,1,2,2 (1.60): O(0,1),O(1,2),O(0,6). Moving O(0,6) away kills.
- P=3,3,4,2,4,4,5,6,3,3,5,4,3,4,4,6,2 (3.65): playing col 2 (exposing their threat (3,2)) -> -4..-8; filling (2,6) kills.
## Hypotheses
H1: O on bottom-row right side ((0,3)/(0,6)) with col 6 low.
H2: opponent's not-yet-playable threat above a landing cell (refuted by P,0,6 = -0.01).

## Score log
- s1 p1 (O at (0,3) & heights[6]<=2): F1 0.073, AUROC 0.54, sim share 0.28.
- s2 p2 (landing at row 2, none at row 3, col6 low): F1 0.056, AUROC 0.50.
- s3 p3 (bottom-row window cols 3-6 has no X and >=2 O): F1 0.088 (P 0.13, R 0.07), AUROC 0.53, sim 0.29. Best.
- s4 p4 (count of O in 7 center/right low cells, col6 low): F1 0.067.
- s5 p5 (O at (0,6), (0,4),(0,5) not X, col6 low): F1 0.056.
## Other tests
- Board-based (move order irrelevant for same board). Very conjunctive: in 6,6,1,2,2 (1.60) moving any single O stone kills firing; swapping colors in col 6 kills.
- In deep position P: making a column land on row 3 (esp. exposing their threat (3,2)) drives it strongly negative.
- Steer zero/max: changes <=0.03 everywhere. No measurable effect.
- Ply parity, last column: no clear relation.
## Conclusion
No simple board pattern found; every hypothesis AUROC ~0.5. Likely random direction or mixture. Confidence low.
Synthesis: hill-climbed P to 3,3,4,2,4,4,5,6,3,3,5,4,3,4,3,6,2 = 4.097 (below dev max 4.169).
