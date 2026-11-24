# U59 notebook (layer 5, pole +, threshold 1.217, dev max 7.073)

## Observations from examples (40 + 3x10 band 9)
- Many firings are ply-1 positions: single opponent stone in col 1-5 (act: c0 0.97, c1 1.35, c2 1.32, c3 1.58, c4 2.54, c5 1.29, c6 1.217 just at threshold).
- Non-opening firings: early/mid game (ply 3-17), often bottom rows with a capped three (e.g. .XOOOX.), or split pairs O.O with gap.
- Top: 6,6,4 = 7.07 (O at (0,4),(0,6), X on (1,6)). Minimal pairs: 6,6,x for x != 4 all < 1.2; 6,0,4 0.43; 5,6,4 0.51. Very configuration-specific.
- Steer: zeroing lowers col 3 by ~1-3 pp; max gives ~0. Effect small.

## Hypotheses
H1: ply-1 opening (opp stone in cols 1-5). Baseline to measure coverage.
H2: opponent has two stones in a row with an empty gap (O.O) on a low row with the gap playable.
H3: a horizontal three capped on both sides on the bottom rows.

## Score log
1. p1 (ply==1, opp stone in col 1-5): F1 0.837 (P 1.00, R 0.72), AUROC 0.86, sim share 0.12. 72% of all firing = the one-stone opening.
2. p2 (+ ply<=20, no threats, O on (0,4), h4>h3): F1 0.476 (P 0.34). Abandoned.
3. p3 (+ ply 3-12, last move col 4, h4>h3, no threats): F1 0.606 (P 0.50). Abandoned.
4. p4 = p1 with graded level by column (col 4 strongest): F1 0.837, sim share 0.13. FINAL.

## Non-opening firing (28% of firing, but carries most of the highest activations)
- Early/middle game (mean ply ~9), quiet positions (usually no threat cells), last move in col 4 enriched (40% vs 13%), col 4 taller than col 3, col 3 short.
- Minimal pairs are very configuration-specific and order-sensitive: 6,6,4 = 7.07 (dev max) but 6,6,x for x!=4 < 1.2, 0,0,6,6,4 0.97 vs 6,6,0,0,4 1.33 (same board).
  2,2,4 2.85 vs 1,1,4 0.0; 3,3,2,4 2.19 vs 3,4,2,4 0.0; game 5,2,2,5,0,2,5,4,4,3 + any O move fires (X three 2-4 on bottom capped at 5) but X-capped-three constructions elsewhere do not.
- Tried capped-three, O split pair (O.O), col-height rules: none gave precision > 0.5. Looks like a mixture / sequence-specific; left as an exception.
- Brute force all 3-move games: 6,6,4 is a singular outlier (next 2,2,4 2.85). Brute force of 5-move games around it: best 6,6,4,4,2 4.71. Could not beat dev max.

## Steer
- 6,6,4: zero -> col 3 -3pp. 4,4,2,5,3,1,3 / 0,5,3,2,4,2,5,3,2,4 / 3,5,4,5,2,1,3: zero -> col 3 -1 to -3pp.
- max on non-firing: 2,2,4,4,0 col 3 +8pp, col 1 +4, col 5 -12; 3,4,1,3 col 3 +2; late game 4,2,...,3,0 col 3 +6, col 0 -6.
- Effect: modest push toward the centre column 3.
