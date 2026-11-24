# U28 notebook (layer 5, pole +, threshold 1.976, dev max 40.08)

## Examples (60+ viewed across bands)
- Bands 7-9 (act>8): nearly all have last move in column 0 and must-block at the landing cell of column 0 (opponent made vertical three in col 0, sometimes other threat lines).
- Bands 5-6 (2-8): diverse; many last_col 0 but no must-block; others misc.

## Hypotheses
H1: opponent just played col 0 and now threatens to win at landing cell of col 0 (must-block in col 0).
H2: opponent vertical three in col 0 specifically (vs horizontal/diagonal threat in col 0).
H3: weaker: any last move in col 0 / any must-block in an edge column.

## Minimal pairs (act)
- 0,1,0,1,0 (opp vertical three col0, me to move) 25.9; 0,2,0,2,0 35.8; same in col1 (1,0,1,0,1) 0.09, col6 -0.25.
- 0,1,0,1,0,2 (I failed to block, now it's the 3-stacker's turn = my own win in col0) -0.2 -> only the OPPONENT's three.
- 0,1,0,1,0,2,3 (three persists, last move elsewhere) 24.3 -> last move need not be col0.
- Two opp stones only in col0: ~0. Horizontal opp threat at (0,0): 0.5-0.66 (no). Diagonal opp threat at (3,0): 7.4 (fires).
- Early-game drop into col0 making height 3 (3,3,4,4,0,0,2,0): 0.44; mid/late game drops to height 3 often 2-6.

## Score calls
1. p1 vertical three col0 (call accidentally duplicated; calls 1+2 both p1): F1 0.425 P0.97 R0.27, sim 0.31.
3. p2 + any opp must-block in col0: F1 0.445 P0.62 R0.35 sim 0.28.
4. p3 + opp just dropped into col0 at row 2 (+ graded levels): F1 0.444, AUROC .73, sim 0.82.
5. p4 + threat cells at (3,0) any height, my playable wins: F1 0.337 (precision collapsed), sim .65.
6. p5 threat (3,0) only when height 2: F1 0.429, sim .78.
7. p6 = p3 with drop restricted to ply>=12 and (4,0) not opp win cell: F1 0.448 P.43 R.46 AUROC .72 sim 0.82. FINAL.
Lower firing (2-8) is a graded, diffuse "column 0 is hot" signal (height 2-3, nearby threats at (3,0)/(4,0)); band 4 (just under threshold) has the same features, so threshold cuts through a continuum. No sharp rule found.

## Steer
Effect: pushes the move toward column 0. 3,3,4,2 forced max: col0 0->0.35. 70747-type (act 8.3): zero col0 .72->.47, max ->.99. Diagonal case 7.4: zero .97->.94. At vertical-three positions the move is already 1.00 col0 (no change).

## Synthesis
0,1,3,3,0,3,3,4,1,4,0 = 40.52 and 0,1,3,3,0,3,3,4,4,4,0 = 40.32 beat dev max 40.08.
