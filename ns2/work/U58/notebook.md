# U58 notebook (layer 1, pole -; threshold 0.591, dev max 1.670)

## Examples
- band 9 (30 samples): 27/30 last move landed at (row4, col2) = 5th stone in column 2. Others col4 row3, col1 row2.
- bands 6-8 (90): 44 at (4,2); then (1,6) 13, (3,1) 9, (0,4) 7, (3,5) 4.
- band 5 (30): 11 at (4,2), (1,6) 5, scattered.
- bands 2-4: scattered, mostly not (4,2).

## Hypotheses
H1: fires when the last stone (opponent's) landed at row 4 of column 2 (column 2 now has 5 stones).
H2: H1 plus secondary landing cells (1,6), (3,1), (0,4) -- position-of-last-move detector (layer 1).
H3: depends on colour/contents of column 2 below.

## Tests (act)
- (4,2) landings fire robustly in built games (2,2,2,2,0,2 0.92; 0,0,2,2,2,2,0,2 1.14; fillers up to ply 18 still 0.7-0.95).
  Weaker when col 2 is one colour or built by 5 consecutive col-2 moves (2,2,2,2,2 0.39; 2,0,2,0,2,6,2,6,2 0.35).
  Even ply (second player just moved) tends higher than odd.
- Secondary cells (1,6), (3,1), (3,5), (0,4), (2,0) are context-dependent: 1,1,1,1 0.98 but 3,1,1,1,1 0.12;
  3,3,6,6 0.84 but 3,6,3,6 -0.36. "Stacked on my stone" generalisation fails (0,6,4,4 -0.41 etc).
- Early pure stacks fire: 4,4,4,4 1.62 (near dev max), 5,5,5,5 0.74, 1,1,1,1 0.98.

## Scores
1. p1 last move at (4,2): F1 0.466 (P 0.543, R 0.408), AUROC 0.699, sim share 0.15.
2. p2 cell set {(4,2),(1,6),(3,1),(0,4),(3,5),(2,0)}: F1 0.246 (P 0.148, R 0.744) - secondary cells too common. Dropped.
3. p3 (4,2) or ((1,6) answered directly on my col-6 stone): F1 0.463, sim 0.28. No gain.
4. p4 fires=(4,2), graded level (parity + secondary cells): F1 0.466, sim share 0.30. FINAL.

## Steer
Three positions (two strongly firing, one not), max and zero: move probabilities change by <= 0.01. Effect none measurable.

## Synthesis
Best 4,4,4,4 = 1.622 (dev max 1.670); col-2 builds up to 1.38. None beat the dev max.

## Conclusion
Medium confidence: the main component is clean (last stone at row 4 of column 2), but it covers only ~41% of firing;
the rest is spread over context-dependent landing cells (layer-1 mixture).
