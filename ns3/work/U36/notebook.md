# U36 notebook (layer 5, pole +, threshold 0.673, dev max 77.2)

## Examples
- Bands 8-9 (acts 37-77): every example = opponent has 3 stacked vertically on top of column 4, cell above empty (must-block at col 4).
- Band 7 (2.4-38): mostly same in col 4 (lower when 3-stack sits higher?), plus some col 5/6 vertical threes (~2-4), odd opening positions.
- Bands 5-6 (0.67-2.4): mixed: vertical threes in cols 5/6, horizontal must-blocks at col 4, early openings. No obvious single pattern.

## Hypotheses
H1: their vertical three on top of col 4 with empty cell above (huge activation).
H2: same in any column (weak in other columns).
H3: generic must-block (any kind).

## act tests
- 4,6,4,5,4 -> 63; adding two quiet moves (0,1) keeps 27.6 (need not be last move).
- Same three owned by me (side to move) -> 0.46; blocked (stone on top) -> -0.35.
- Three on X base (4,4,6,4,5,4) -> 26; rows 2-4 via 4,4,6,4,5,4,0,4 -> 65.
- Vertical three in col 0/1/2/3/5/6 in quiet openings: -0.18..1.41, mostly below threshold (col2 1.41, col6 0.69/1.96 context-dependent).
=> H1 strongly supported; H2 only weak/noisy; H3 not tested well yet.

## Score 1 (p1: their vertical 3 on top of col 4, room above): F1 0.417 (P 0.994, R 0.264), AUROC 0.632, sim recovers 40.2% of zero-ablation damage (ceiling reported as nan).
Misses are all weak firing (0.67-~3), heterogeneous.
## act tests on other columns (without my own immediate win confound): cols 0 and 6 vertical threes fire weakly (1.2-2.7), col 2 ~0.75, cols 1,3,5 ~0.
## Score 2 (p2: add cols 0 and 6): F1 0.408 (P 0.427, R 0.391). Late-game edge threes often do not fire. Reverted to p1.
## Low-band histograms: must-blocks enriched in bands 5-6 (33%/59% vs ~15-20%); their 2-stack atop col 4 enriched in band 6 (25% vs 6-10%) but act shows only ~0.6-1.1, too weak/base-rate too high to help. Several early (ply 5) openings fire weakly (my 2-stack in an edge column) - no clean rule.
## Steer: max -> moves all probability to column 4 (e.g. 1,6,3,6,1: col4 0.27 -> 1.00; 3,3,2,2: col1/col4 50/50 -> col4 1.00). Zero: no change on col-4-three positions (block already certain).
## Synthesis: best ~71 (4,2,2,4,3,4,1,4 = 70.98), below dev max 77.2.
