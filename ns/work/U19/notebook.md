# U19 notebook (layer 3, pole -, threshold 0.798, dev max 13.95)

## Examples (bands 0-9, ~70 viewed)
- Top firing mostly early-game (ply 3-12) with low stones in centre-right; also some late-game boards with an empty/short column.
- Many top boards: column 4 height 1 (or 0), its landing cell (1,4) empty, O stones at (1,3) and/or (1,5) / O at bottom near col 2-3, X at (0,4),(0,5).

## Hypotheses
H1: landing cell of column 4 is empty and flanked by opponent stones (O at (r,3)/(r,5) on landing row).
H2: opponent can build a horizontal/diagonal through the col-4 landing cell.
H3: (alternative) generic "early game, opponent stones low on right-centre".

## Minimal pairs
- 2,5,3,4,3 = 6.56; replace last with 5 -> 8.66; with 2 -> 3.05; 0 -> 1.42; 6 -> 1.34; 1 -> 0.42 (O three on bottom, must-block); 4 (O fills (1,4)) -> 0.04.
- steer zero on 2,5,3,4,5: col3 prob +0.17, col1/col2 -0.09/-0.06.

## More minimal pairs (act)
- Pattern is tied to absolute cells: mirror (3,1,1,2,3 = 0.52) and shift-left (2,4,4,3,2 = 0.19) of 3,5,5,4,3 (8.39) are silent.
- O on top of my (0,5): 5,5 = 1.24; 0,4,0,5,5 = 2.17 vs 0,4,0,5,x for x != 5 = about 0.1. 3-ply grid: the top firing is 3,5,5 / 4,5,5 / 2,5,5 (O at (1,5)).
- O at (0,2),(0,3),(1,3) to the left of my (0,4)+(0,5): 2,4,3,5,3 = 6.93; without my (0,4) (3,4,3,6,0) = -0.32.
- My stones close by suppress it: from 2,4,3,5,3,6,5 (10.0), adding my stone at (2,5)/(2,3)/(1,4)/(1,2)/(0,6) cuts it to 1.7-3.9; adding O at (1,2) raises it to 14.7.
- My (0,3) flanked by O (0,2),(0,4) (0,4,3,2) = 2.1; with my stone at (0,6) instead = 0.2.
- Late-game firing is weak (1.1-1.4) and diffuse; walking back through those games shows no single clear trigger.

## Dev metric (8 calls; calls 1-2 were the same program, run twice by mistake)
1-2. p1 O at (1,5): F1 0.103 (P .057 R .53), sim 0.02
3. p2 cell template (counts only): F1 0.120, sim 0.01
4. p3 signed template: O at (0,2),(0,3),(1,2),(1,3),(1,5) +, my (0,4),(0,5) +, my stones at (0,1),(0,6),(1,2-5),(2,2-5) -, threshold 3.5: F1 0.259 (P .19 R .40, AUROC .67), sim 0.16  <- BEST
5. p4 hemming rules split by branch: F1 0.227
6. p5 = p3, left O only counted if column 4 is occupied: F1 0.256
7. p3 with threshold 4.0: F1 0.211;  8. p3 with threshold 3.0: F1 0.222 (R .50)
Plateau around 0.26. Most of the misses are weak late-game firing.

## Steer
Zeroing it at top positions: column 3 +0.12 to +0.17, columns 1-2 -0.05 to -0.09 (2 positions); about 0 on 2 others. Forcing it to max on non-firing positions: small (column 3 +0.16 / column 2 -0.10 in one case, about 0 elsewhere).

## Synthesis
2,4,3,5,3,0,5,0,2 = 16.13 (beats the dev max of 13.95); 3,5,5,4,3,0,2,0,2 = 16.00; 2,4,3,5,3,6,5,0,2,0,0 = 15.66; 2,4,3,5,3,0,5,6,2 = 14.94; 2,4,3,5,3,6,5,0,2 = 14.66.
