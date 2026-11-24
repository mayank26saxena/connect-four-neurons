# U23 notebook (layer 5, pole -)

## Examples (120 across bands, 3 seeds)
- Firing positions are all late (ply ~26-41), most columns full. In every firing example column 5 is full.
- Game traces (act): activation jumps when col 5 becomes full (e.g. ply 24->25: -13.4 -> 9.2; 25->26: 0.9 -> 27.9),
  then climbs steadily as the board fills, higher on even ply (me = first player).
- Counterexample to "late, few legal moves": pos 129048, ply 38, only col 5 open (2 stones) -> -0.9.
- Col 5 with 5 stones (top cell empty) gave a strong negative value (-13).
- Some mid-game moderate activations (12 at ply 20) with col 5 empty but their threat directly above col5 landing; not firing.

## Hypotheses
H1: fires when column 5 is full and board is mostly filled (ply high); level rises with ply.
H2: poisoned column (their threat directly above my landing cell) - rejected by 129048 / ply-30 trace (~0).
H3: "I am losing" (teacher ~ -960) - rejected (129048 is lost but -0.9).

## Score log
- p1 (col5 full & ply>=30; level by ply): F1 0.368 (P 0.231 R 0.911) AUROC 0.911, sim share 0.26. Too broad.
- p2 (col5 full & <=2 legal columns): F1 0.479 (P 0.356 R 0.733) AUROC 0.847, sim -2.36 (bad level).
- Found via facts: within one game, activation alternates by ply and is high exactly when the side to move is
  losing by force (teacher ~-960), low when winning (e.g. ply 28/29/30/31: 4.9 win / 16.8 lost / 5.6 win / 26.7 lost;
  pos 39143 ply 24, 5 legal cols, lost: 31.8, next ply winning: 9.2). Added a small forced-loss search (depth 10).
- p3 (col5 full & side to move lost): F1 0.447 (P 0.338 R 0.656), sim share 1.38. Misses: draws with 1 legal column.
- p4 (points: legal 1/2/3 -> 3/2/1, lost +2, I-win -1, ply>=34 +1; >=3): F1 0.529 (P 0.391 R 0.817) AUROC 0.890, sim -17 (level too aggressive).
- p5 (points: legal 1/2/3 -> 3/2/1, lost +1, an open column with <=1 stone +1; >=3; conservative level): F1 0.525
  (P 0.391 R 0.799) AUROC 0.882, sim share 1.56.  <- chosen
- p6 (p5 with lost +2): F1 0.470 (P 0.322 R 0.873). Worse.
- FPs are mostly near threshold (10-19), misses 20-25: graded unit with a fuzzy boundary. Some winning positions
  also fire high (pos 4039: 36 while winning), so "lost" is a modulator, not the whole story.

## Effect (steer)
- Forcing max where col 5 is still legal removes col 5 probability (-0.42, -0.25) and spreads it to other columns.
- Zeroing in firing positions changes nothing (col 5 already illegal). So it is a "column 5 is unavailable" signal.

## Synthesis
Random-continuation search with act from top positions. Best 41.9 (dev max 43.5), so nothing beat the max.

## Final
p5. Confidence medium (F1 0.525, clear exceptions).
