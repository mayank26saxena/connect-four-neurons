# U48 notebook (layer 0, pole -)

## Exploration
- Dev threshold 0.765, max 1.554. Top bands are dominated by ply-1 positions: first move 5 -> 1.554, 3 -> 0.991, 4 -> 0.828 (fire); 0 .385, 1 .272, 2 -.09, 6 -.71 (no).
- Ply 2: fires for 1,5 (1.29), 3,5 (1.19), 2,5 (.78), 5,3 (.765 borderline). Last move in col 5 helps; last move 4/6 hurts at ply 2.
- Later-game firing examples (~1/3 of fired samples) mostly last move col 4 or 5, some 1,2,3,6.

## Hypotheses
H1: opening detector: ply==1 and the first stone is in column 3,4,5.
H2: H1 plus later positions where last move is col 5/4 with some feature (TBD).
H3: generic "last move col 5 early in game" token/position feature.

## Tests (act, minimal pairs)
- Layer-0 unit: activation is mostly a function of the LAST move's column, modulated by the bag of earlier stones (order barely matters; 0,4,4,4,4,0,4 == 0,0,4,4,4,4,4).
- Last move col 4: fires when col 4 is nearly full (stone lands row 4-5); rises with number of prior col-4 stones (row sweep .14 -> .62 -> .97). Tall stacks in cols 0, 2, 3, 6 lower it; low stones in cols 1/5 raise it.
- Last move col 5: best when col 5 low and few stones elsewhere (1,5 1.29; 1,1,1,1,1,1,5 0.00). Stacked context lowers it in general.
- Late-game firings with last move 0/1/2/5/6 occur when cols 2-3 are full and col 4 is empty, but cols 2-3 full alone does not suffice (0.3). Distributed, board-cell-like readout; no crisp rule found.

## Scores
1. p1 ply==1 & first stone in col 3/4/5: F1 0.601 (P 1.00, R 0.43), AUROC .715, sim -0.11
2. p2 + ply<=3 col-5 + col-4 row>=4: F1 0.459 (P .35)
3. p3 + loose col-5/col-1-3 context rules: F1 0.394 (P .27) - too loose
4. p4 = p1 + strict ply2-3 col-5 + col4 row>=4 with col4 >= 27% of stones: F1 0.632 (P .665 R .603)
5. p5 replace fraction by ply<=22 & edge limits: F1 0.613
6. p6 = p4 + h0<=3, h6<=4, h3<=5: F1 0.643 (P .72 R .58), AUROC .787, sim -0.02  <- best

## Steer
max/zero on [5], [3,5], [4], [1,1,4,4,4,4,2,4], a late col-5 position: all changes 0.00. No measurable effect on the move. Sim share ~0 is consistent.

## Synthesis
Dev max 1.554 is the single opening stone in col 5; could not beat it. Best others: 5,1,3,1,4x6 1.364; 1,5,2,1,4x6 1.334; 1,5 1.294.
