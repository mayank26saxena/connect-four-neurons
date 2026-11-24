# U17 notebook (layer 1, pole +, thr 0.322, dev max 3.255)

## Examples
Top bands dominated by column 1 being tall (3-6 stones) with column 0 and/or 2 empty/short. Topmost stones of col 1 mostly mine (side to move).
One exception seen: 171660 (col 5 tall, no col1).

## Hypotheses
H1: col 1 tall and its top stone(s) belong to me (side to move).
H2: col 1 tall and neighbours (col 0, col 2) short.
H3: generic "my vertical stack" anywhere (mirror test col 5 = -0.23, so no: column-1 specific).

## act tests
- 1,1,1,3,1,5 (col1 X,O,X,X) 1.595; flip ownership by one extra move anywhere (0,2,6,1) -> all < 0 (parity: top stones now theirs).
- same + 4,6 (keeps ownership) 1.656; + 0,6 0.739; + 2,6 0.881 -> stones in col 0/2 reduce but don't kill.
- mirror 5,5,5,3,5,1 -0.226 -> column 1 specific.
- 1,4,1,5,1,6 (X,X,X) 0.77; 1,4,1,5,6,1 (X,X,O top theirs) 0.23.
- 1,1,1,1,4,1,5 (O,X,O,X,X) 2.996 ; 1,1,1,1,1,4 (X,O,X,O,X) 0.687.
=> H1 supported strongly, H2 as modulator.

## score 1 (p1: h1>=3 and top of col1 mine): F1 0.081, P 0.046, R 0.317, AUROC 0.558, sim 0.02. FPs: col 0/2 filled; misses diverse.
## score 2 (p2: + exposure of run to empty neighbour cells): F1 0.118, sim 0.01.
## score 3 (p3: top two of col1 mine + >=2 open neighbour cells beside them): F1 0.124, P 0.098, R 0.169.
More act tests on base 1,1,1,1,4,1,5 (O,X,O,X,X in col1, 3.0):
- every extra stone anywhere lowers it (6,6 -> 2.2; 6,6,6,6 -> 1.1): general ply/stone-count decline.
- col 0 stones hurt most: 0,6,0,6,0,6 -> 0.30; 6,0,6,0,6,0 -> -0.19; vs 2,6 x3 -> 1.14, 4,4,5,5,6,6 -> 1.70.
- top single mine (X,O,X) can be strongly negative (-1.0), top two mine strong.
Band histograms (30/band): top band h0 mean 0.2 (25/30 empty) vs ~2.2 in band 0; h1 mean 4.8 vs 2.6.
H4: col 0 empty (<=1) + col 1 tall with top two mine.

## score 4 (p4: h0<=1, h1>=3, top two of col1 mine): F1 0.172, P 0.30, R 0.12, AUROC 0.556. Best so far but low recall.
Band histogram of last move column: bands 3-6 last move mostly col 1; bands 8-9 last move mostly col 5 (24/40, 20/40).
act: with col1 pattern, last move col sweeps 0..6 gives 0.57,-,0.73,0.92,1.09,1.60,1.40 (gain, peaks col 5). Without pattern, last col 5 is -1.09 (interaction, not additive).
Second route: I played col 1, opponent stacked on it (X then O in col 1) early: 6,2,1,1 0.50; 3,4,1,1 0.55; 0,1,2,1 0.44; 2,2,1,1 0.35. Opponent's col1 stone with no mine under it: strongly negative (3,4,3,1 -2.5).
H5: A (col1 stack, col0 empty) OR B (opp just stacked on my col-1 stone, early game).

## score 5 (p5: A or B): F1 0.236, P 0.31, R 0.19, AUROC 0.589, sim 0.05.
FPs: route B at ply 8-10 (dead by then); route A with opponent stones in col 2.
act: opponent stones in col 2 hurt (6,2 x4 -> 0.18) but my stones in col 2 barely (2,6 x4 -> 0.72, 2,2,2,2 -> 0.78). Col 0 stones of either colour hurt.

## score 6 (p6: + opp stones in col2 <=1, route B ply<=6 & h1==2): F1 0.178, P 0.48, R 0.11. More precise, less recall.
## score 7 (p7: loosened, allow single top-mine stone if h1>=5): F1 0.191, P 0.23, R 0.16. Worse.
Best = p5 (F1 0.236). act tests show heavy context dependence (other columns, ply, last move) -> no clean board rule; unit looks like a mixture/distributed direction.

## steer (4 positions, zero and max): changes <= 2 points on any column. Effect: none measurable.
## synthesis: column 1 = my three stones on top (rows 3-5 or 1-3), col 0 empty, last move col 5: 4.15-4.16 (dev max 3.255). All 5 beat dev max.
Final: p5, confidence low (F1 0.236).
