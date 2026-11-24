# U11 notebook (layer 3, pole +, threshold 1.068, dev max 2.866, rate 3%)

## Observations (examples, 40 + band9 16 + band8 14 + 300-sample histograms)
- Firing positions are a bit earlier (mean ply 13.6 vs 16-20 for non-firing), but no cell or column
  occupancy histogram separates bands strongly. Last-move column/row, parity: no signal.
- Teacher scores: some firing positions bad for mover, but non-firing too. No signal.
- Steer: zeroing/maxing changes move probs by <=0.03 in 6/7 positions; one +0.11 on col 3.
- Activation mostly depends on the board, not move order (4 orders of same board give ~same act),
  but single-stone swaps shift it a lot (2.5 -> 0.8 by swapping owners of (2,4)/(3,4) in pos 26824).
- Simple 4-stone positions: X(me) on both edge cols 0 and 6 with O on cols 2/5 -> 2.1; putting
  a stone in col 3 tends to lower it (but not consistently).

## Hypotheses
H1: early-ish position with empty centre-ish columns and my stones on the edges (weak).
H2: opponent has an unplayable (elevated) threat cell (seen in 26824, 141828, 49220) - but many firing
    positions have no threats at all, so at most partial.
H3: random direction / no clean concept.

## Score log
- s1 (p1: no full column, >=2 empty columns, ply>=6): F1 0.098, P 0.055, R 0.454, AUROC 0.607, sim share 0.02.
  Misses are threat-rich mid-games with a low/empty column; FPs are ordinary open positions.
- p2 failed to load (helper name contained the forbidden substring "open(" ); it was never scored. I did not
  re-run it under a new name; p3 below is a different rule.
- More single-feature histograms (threat counts, elevated threats, height shape): no separation beyond
  the general "earlier, fewer full columns, lower centre column" trend.
- 4-stone minimal pairs (me on cols 0 and 6, them on a,b): them on col 2/5 raises (up to 1.8-2.2), them on 3/4
  lowers (-0.2); with them on 2,5 and me on a,b: me on 0+6 = 1.8, me on any centre column -> -0.5 to -1.4.
- s3 (p3: early-game points, ply/empty cols/low centre): F1 0.065, AUROC 0.521, sim 0.02. Early game is not it.
- s4 (p4: deep well, a column >=2 lower than both neighbours, no full column): F1 0.071, AUROC 0.537, sim 0.01.
- Steer on 6 positions: changes <= 0.04 on any column except one +0.11 on col 3 (pos with act -1.4 -> max).
- Synthesis: greedy/2-step search from pos 26824 board; best valid 3.390 (3,0,4,5,3,3,4,1,4,4,5,3,6,0,2,0,0).

## Conclusion
No board concept found. Activation depends on the board (move order barely matters) but in a highly
nonlinear way: single-stone swaps move it by 1.5+, and no single feature histogram (heights, cell
occupancy, threats, centre control, ply, last move) separates firing from non-firing. Best rule p1 F1 0.098,
AUROC 0.61. Consistent with a random direction or a highly polysemantic mixture. Confidence low.
