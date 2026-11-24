# U39 notebook (layer 0, pole -)
Threshold 1.509, dev max 7.34.
## Examples
Bands 7-9 almost all: last move in column 1. Top (6.5-7.3) are ply-4 positions with last move col 1 landing at row 0.
Band 5 has many ply-4 positions with other last columns (ply-4 baseline ~1.5, at threshold).
## Hypotheses
H1: last move is the FIRST stone in column 1 (lands at row 0); strength decreases with ply (ply4 ~7, ply5 ~3.5, ply 21 ~2.7).
H2: last move col 1 regardless of row.
H3: ply-4 positions in general (weak baseline).
## act minimal pairs
- 3,3,3,3,1 -> 3.43 fires; then 1 again (row1) -> -2.0; row2 -2.6.
- ...5,5 + 0 / 2 / 6 -> 0.26/0.27/0.13; + 1 -> 2.10 fires; +1,1 -> -1.9.
- first col1 stone at ply 21 -> 2.74 fires; ply 8 after col 0,6 -> 1.84.
=> H1 strongly supported; H2 rejected (second stone in col1 suppresses strongly). Dev exceptions with col1 row 1 firing (pos 80839, 69669) occur late in game where previous col1 stone is far back (layer-0 attention dilution?).
## More act
- Second col1 stone: if previous col1 stone is MINE (other player) -> strongly negative (-2). If both col1 stones are THEIRS (same player) -> moderate, fires early (3,1,3,1 3.8; 0,1,0,4,3,1 2.27; 3,1,4,4,3,1 2.81) but not later (3,3,3,3,1,4,1 1.23).
- Ply-4 openings without col1: hover 1.3-1.75 (threshold 1.51); distinct columns tend to fire, stacking (3,3,3,x) lowers; a non-last col1 stone at ply 4 suppresses (1,2,3,4 -0.42).
## Scores
- p1 (last col1, heights[1]==1): F1 0.793 P .976 R .667, sim share 0.65. Misses: ply-4 openings, early second col1 by same player.
- p2 (+ col1 all theirs any count, + ply4 >=3 distinct cols): F1 0.628 P .46 R .97. Too broad.
- p3 (p1 + ply4 4-distinct-columns no col1): F1 0.831 P .908 R .766, sim 0.70.
- p4 (p3 + second col1 stone when both theirs and ply<=6): F1 0.857 P .901 R .817, AUROC .907, sim 0.70. Remaining errors: ply-4 near-threshold noise.
## Steer
4,6,3,1 / 3,3,4,4,3,3,4,4,5,5,1 / 2,2,3,4,5 / 6,6,0,0,5,5,3 / 4,4,3,3,2,2,5 to max: changes <= 5 points on any column; essentially no measurable effect.
## Synthesis
Sweep of a,b,c,1 (no col1 before): best 3,5,4,1 7.565 and 4,5,3,1 7.560 beat dev max 7.34. Final = p4.
