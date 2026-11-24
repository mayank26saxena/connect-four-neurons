# U10 notebook (layer 4, pole +, thr 1.508, dev max 5.017)

## Observations
- Band 9 (3.2-4.2): nearly all = opponent has 3 stacked vertically in column 2 with the cell above empty (must-block above), usually last move on top. A few col 3, one col 5.
- Bands 5-7: mix; some vertical threats, many with no must-block (opponent capping one of my stones?), unclear.

## Hypotheses
H1: opponent vertical three in column 2 (open above). H2: same in any column, col-weighted. H3: secondary: last move stacked on my stone.

## Minimal pairs (act)
- c,o,c,o,c vertical three from floor: col2 2.45 FIRES; col0 -0.45, col1 -0.92, col3 -0.70, col4 0.90, col5 -0.01, col6 0.63.
- with my stone below: col2 1.6-1.8 FIRES, col3 0.4-0.9, col5 1.1, col6 1.0-1.3, col0/1/4 <0.5.
- Horizontal three with must-block at col 2 (row 0): -1.2 to -2.4. Horizontal not it.
- 9434 (4.10): opponent blocks col 2 -> -0.46; threat persists after a non-block exchange -> 2.32 (still fires, last move elsewhere).
- When I have own immediate win too (2,0,2,0,2,0,6 etc.) activation drops (-0.1, 0.55).

## Score log
- s1 p1 vertical opp three in col 2: F1 0.295 (P 0.66, R 0.19), AUROC 0.59, sim 0.00
- s2 p2 vertical three any column: F1 0.202 (P 0.15, R 0.31). Verticals elsewhere mostly do not fire.
- s3 p3 col2 vertical OR early last move in col 2: F1 0.176. Too broad.
- s4 p4 vertical three in col 2 or 3: F1 0.315 (P 0.46, R 0.24)
- s5 p5 + opening term (ply<=8, my stone at (0,1)): F1 0.235. Too broad.
- s6 p6 = p4 minus positions where I have an immediate win: F1 0.316 (P 0.47, R 0.24), sim 0.00. FINAL.

## Further act tests
- Own immediate win suppresses col-2 vertical response (0,2,0,2,0,2 -> 0.55; 4,2,4,2,4,2 -> 0.99).
- My stones in col 3 next to a col-2 threat tend to lower it (2,2,3,2,3,2 -> 0.39), but not always (9434 has X in col 3 and is 4.1).
- Col-3 vertical threats hover around threshold (0.7-2.5) depending on surroundings, e.g. O at (0,2) matters (3.55 -> 0.13 when swapped).
- Opening positions (ply 4-8) fire often for reasons I could not pin down: depends on my stone at (0,1) and where O sits (1,3,6,2 1.97 vs 1,3,6,0 -1.24). Not captured.
- ~70% of firing positions have no vertical threat at all; the remainder looks diffuse.

## Steer
- Effect is negligible: max/zero changes <= 0.02 on 3 positions, one position +0.11 col 5 / -0.09 col 3.

## Synthesis
- Hill-climbed from dev pos 9434 (col-2 vertical three rows 1-3 over my stone) by inserting move pairs before the final O move in col 2: up to 5.45 (dev max 5.02).
