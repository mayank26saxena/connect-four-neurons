# U53 notebook (layer 1, pole -)

## Examples (40, all bands)
Nearly every firing example (bands 5-9) has column 2 with exactly 2 stones (one exception: pos 828 h2=3).
Top band: early positions, col 2 = X bottom, O on top (opponent stacked on my stone), h2=2.
Non-firing near threshold: h2=3 or h2=2 (145120, 1.34).

Hypotheses:
H1: fires iff column 2 has exactly 2 stones (landing(2)==2).
H2: H1 modulated by contents (O on top of col 2) / early game.
H3: count-of-moves-in-col-2 parity feature (h2 even small).

## act tests
- 2 -> 0.86, 2,2 -> 1.84 FIRES, 2,2,0 -> 2.35, 2,2,2 -> 0.05, 2,2,2,0 -> 1.49
- 3,3,2,2 -> 2.59; 4,4,2,2 -> 1.93; +2 -> 0.01; +2 -> -2.43 (h2=4 strongly negative)
So h2==2 is the main driver; h2=3 is intermediate.

## Score 1 (p1: h2==2): F1 0.385 (P 0.244, R 0.900), AUROC 0.905, sim share 0.60
Precision poor: h2==2 is 11.7% of positions. Exploring FPs: strong dependence on game stage.
act: 2,2 + spread moves at ply 10 -> 0.86 (flat board, so not about heights elsewhere); stacked
columns also lower it; very late game (most columns full) it recovers and fires (dev late-game firings common).
Col-2 colours at ply 4: XO 2.89, OO 2.29, OX 1.95, XX 1.86; at ply 6: XO 1.88, OO 1.49, OX 1.30, XX 1.22.
=> me-bottom / them-top best; game stage (ply) is the main modulator: early (<=7) and late (>=28) fire, mid suppressed.
Also h2==3 fires in very late games.

## Score 2 (p2: h2==2 & (ply<=7 | ply>=26 | XO), h2==3 & ply>=30): F1 0.550 (P 0.389 R 0.939), AUROC 0.945, sim 0.71
## Score 3 (p3: XO only up to ply 12, late >=28, h2==3 >=31): F1 0.670 (P 0.530 R 0.911), AUROC 0.942, sim share 0.75  <- best
## Score 4 (p4: finer colour split by ply): F1 0.668, sim 0.74 -> no gain; keep p3 (simpler).
Remaining FPs/misses look like graded noise around threshold (mid-game h2==2 with various colours, late-game nonfirers).

## Steer
2,2 / 0,2,2 / 2,1,1,2 / 2,2,5,6,5,6: max or zero changes move probs by <=0.01.
0,2,3,5,3,3,3,5,2,0,1: max -> col2 -0.02, col5 +0.03. Late game (ply 31): max -> col2 -0.03, col0 +0.03; zero reverses.
Effect: very small; if anything slightly lowers playing column 2 (onto the 2-stack).

## Synthesis
Best: 4,2,2,5,0 -> 4.074 (beats dev max 4.053); 3,2,2,5,0 -> 4.053 (ties). Pattern: ply 5, col2 = my stone under theirs, few singleton stones on row 0.
