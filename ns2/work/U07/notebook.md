# U07 notebook (layer 4, pole -, threshold 1.378, dev max 6.025)

## Examples (60+ viewed)
- Band 9 (3.6-6.0): almost all = opponent's last move in column 3 completes a vertical 3-stack of O at top of col 3, open cell above (must-block at top of col 3).
- Band 7-8: same, plus some vertical 3s elsewhere (col 5 in 117875).
- Band 5 (threshold): heterogeneous; early-game positions, two-O stacks, some last moves not col 3.

## Hypotheses
- H1: opponent has a vertical three (3 O stacked, cell above empty) in column 3 that was just made.
- H2: any opponent vertical three in any column (vertical must-block), strongest in center.
- H3: graded by number of consecutive O at top of column 3 (2 -> weak, 3 -> strong).

## act tests
- Vertical O three, same game shifted across columns: col3 5.32, col1 1.59, col2 0.82, col0 0.68, col4 -0.99, col5 -1.58, col6 -0.73 -> column 3 specific.
- My own immediate win suppresses it (3,3,1,3,0,3 -1.18; 3,3,6,3,5,3 -0.14 vs no-win twins 1.3-3.4).
- After the three is blocked, or a move later, it drops (0.6, -1.2).
- 2-stacks of O in col 3 do NOT fire (0.2-0.4); but 2-stacks in cols 1,2,4 with X at 5,6 fire (2.0-2.5). Early-game firing has a strong left/right asymmetry (O on left, X on right fires; mirror ~0 or negative). No simple rule found for it.
- Horizontal bottom threes: some fire (O 4,5,6 1.87; O 1,2,3 open both ends 1.69), mirror O 0,1,2 does not (0.55).
## score log
- p1 (any must-block in col 3, no my win): F1 0.258 P .365 R .199, sim 0.01
- p2 (vertical three just played in cols 1-3): F1 0.221
- p3 (p1-core + col3 empty and O mostly left): F1 0.184 (side rule is noise)
- p4 (p1 + ply<=28 + cols 1-2 verticals): F1 0.224
- p5 (vertical O three on top of col 3, cell above empty, no my win): F1 0.285 P .779 R .175, sim 0.01  <- BEST
- p6 (p5 + opponent double playable threat): F1 0.273
## steer
- forced-block positions: no change (col 3 already ~1.0). Ambiguous positions: forcing high lowers col 3 by 3-6 points; zeroing ~no change.
## synthesis
- 3,2,1,3,3,2,3,5,3 = 6.498 beats dev max 6.025.
## conclusion
- Clean high-precision subcase (vertical three in col 3) explains top bands but only ~18% of firing; the rest is diffuse early-game firing without a simple rule. Confidence low.
