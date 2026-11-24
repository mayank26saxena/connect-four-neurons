# U05 notebook (layer 5, pole -, threshold 0.984, dev max 35.25)

## Examples (bands 0-9, plus band 9 x2 seeds, band 5 x3 seeds)
- Band 9 (18-35): EVERY example has a single must-block cell in column 1 ((0,1),(1,1),(5,1)).
- Bands 7-8 (3-18): must-blocks in col 1 mostly; also col 0, col 2, col 5, or two must-blocks.
- Band 5 (just above threshold): mostly no must-block at all; looks like noise / no clean pattern.

## Hypotheses
H1: fires when opponent has an immediate win at the column-1 landing cell (I must block in col 1).
H2: H1 but only for horizontal/diagonal lines (vertical col-1 threes do not count).
H3: generic "must-block" unit with column-1 preference.

## Minimal pairs (act)
- X.OOOX. (must-block (0,1)) 29.7; replace X0 by X6 still 24.4. Adding second must-block (0,5) -> 3.4 / 3.6 (double threat suppresses).
- Vertical three in col 1: -0.6, -13.4, -6.7, -0.2 -> vertical does NOT fire (H2 > H1).
- Vertical col 0: 4.9; vertical col 2: 1.0; vertical col 3: -6.
- Row-0 gaps: _OOO at (0,1)=20, 14; O_OO (O at 0,2,3) only 3.55; OOO_ (0,3) 1.36; (0,0) 6.9; (0,2) 1.2-2.2; (0,4),(0,5),(0,3 from right) ~0.
- 4,0,6,3,4,2 (threat) 19.8 vs 4,0,6,3,4,5 (no threat) -0.2.
## Steer
- max: +0.9 prob to column 1 in quiet positions (3,3,6,4; 1,3,6,5,2; 4,0,6,3,4,5), taken from col 3 mostly. In double threat +0.09 col1. zero in forced position: no change (block already certain).

## Score calls
1. p1 (col-1 must-block via horizontal/diagonal line): F1 0.240 (P 0.354, R 0.181), AUROC 0.585, sim -36.8 share. FPs: late-game, my own immediate win, double threats, rows 2-4.
2. p2 (any must-block): F1 0.167 (P 0.101, R 0.492). Generic must-blocks mostly do not fire.
3. p3 (p1 + single must-block + >1 legal): F1 0.215 (P 0.358). No help.
   Found: band 9 must-block rows are always 0, 1 or 5 of col 1; act test row-2 col-1 threat 0.18 (no fire). Also MY immediate win at col-1 landing fires (12.5).
4. p4 (col-1 landing cell in row 0/1/5 completes a horizontal/diagonal four for them [single block, no other win for me] or for me): F1 0.326 (P 0.823, R 0.203).
   act: same vertical (3,4) threat decays with ply: 11.7 (ply 8), 7.8 (10), 5.4 (12), 1.1 (14). Early must-blocks fire anywhere (except col 3, vertical col 1).
5. p5 (p4 OR any must-block with ply <= 10): F1 0.422 (P 0.488, R 0.372), AUROC 0.680. BEST.
6. p6 (p4 OR must-block not in col 3 with ply <= 12, graded): F1 0.407. Slightly worse.
7. p7 intended as level-baseline probe but sed bug broke _kind -> F1 0.087; ignore (wasted call).
Simulation is ~ -27x to -38x share for every program; could not find why (unit is huge negative on many positions, our level 0 maybe a poor stand-in). Not fixed.
Remaining misses: ~60% of firing sits in 0.98-1.3 band with no visible pattern (no threats), looks like noise around threshold.

## Synthesis
Bottom row O at 2,3,4 (last move col 2), col 1 open, X at 5 and 4/5 above: 5,4,5,3,4,2 = 34.1; +0,0 = 34.98 (dev max 35.25, not beaten). Ordering matters (last O stone placed adjacent to col 1 best).
