# U15 notebook (layer 3, pole +, threshold 0.666, dev max 12.735)

## Examples (bands 0-9, ~120 positions)
- Top band (>3.9): almost all early (ply 4-8), even ply (me = first player), opponent stone on bottom-left corner (0,0)
  and/or bottom-right (0,6), my stones on the bottom row in cols 1-3 / center.
- Even-ply share by band (seed 7, n=40): bands 0-4 ~50-60%; band 8 83%; band 9 98%. Mean ply drops to ~7 at the top.
- Mid-game firing (bands 5-7) is mixed parity and harder to read.

## Hypotheses
H1: me = first player, opponent holds bottom corner(s) (0,0)/(0,6), early game.
H2: "side to move is winning" (engine eval). 
H3: opponent has stones on edge columns (0,1,6) with my stones central.

## Minimal pairs (act)
- 1,6,3,0 = 4.53; 1,6,3,5 = -0.02; 1,6,3,4 = 0.16 -> O on (0,0) is crucial.
- 3,a,3,c grid (me 2 stacked at col 3): with O on (0,0) or (0,6): 1.2-6.2; both corners 6.2; neither corner: 0.07-1.6 (3,1,3,2 =1.65 the only one >1).
- 3,6,3,0 = 5.15 but 3,6,3,0,3 (odd ply) = 0.33; 0,3,6,3 (mirror roles, me second) = 0.23 -> parity / me-first matters strongly early.
- 3,0,3,6,x,1 (O also at (0,1)): 8-10.
- H2 rejected: game 2,0,3,4... fires on even plies; game 4,2,3,3,... fires at ply 19 where me eval = -8 and not at ply 20 where me eval = +8. 0,6,1,5,2,4 (I have immediate win) = -0.1.
- Steering: max or zero changes move probs by <= 0.06 in 6 positions; one zero-ablation +0.12 col0/-0.11 col6.

## Score calls
1. p1 (me_first & O on a bottom corner & ply<=12): F1 0.168, P 0.121, R 0.271, AUROC 0.606, sim share 0.08.
2. p2 (corner O & >=2 my stones in row0 cols1-5, any parity): F1 0.071, AUROC 0.569 (program fires on 48%) - far too broad.
3. p3 (weighted: O(0,0) +4, O(0,1) +1, O(0,6) +2.5, me_first +1.5, early bonus, my (0,3) +1, O on top at (1,3) -3, O at (0,3) -2): F1 0.179, P 0.132, R 0.275, AUROC 0.610, sim 0.08. BEST.
4. p4 (fires iff (1,3) is mine): F1 0.111, R 0.68 but fires on 33%; AUROC 0.680 (best AUROC) sim 0.01.
5. p5 (p3+p4 mix with low edge cells): F1 0.146, AUROC 0.646.
6. p6 (live-window advantage + parity): F1 0.078, AUROC 0.525 - rejected.
7. p7 (no opponent stone in column 3 & corner O): F1 0.150, AUROC 0.601.

## More minimal pairs
- 3,4,3,6,4,0 = 12.69; 3,4,4,0,3,6 = 13.10 (beats dev max). Adding an odd-ply move to any of these drops to ~0.
- 1,0,3,6 vs 3,0,3,3 (O on my center stone): 4.35 vs 0.15; 1,a,3,c grid: O on (1,3) kills it in every row.
- Midgame: opponent's last move into bottom/low edge cells raises it (game A ..,0 =1.2 vs ..,6 =-0.05; game B ..,0/..,6 = 2.5 vs ..,5 =0.3).
- Engine eval / threats: no relation (fires at both + and - evals).

## Steering
- Almost no effect in 8 positions (|change| <= 0.06) at moderate activation.
- At extreme activation (12-13) zeroing raises col 3 by ~0.2 and lowers col 4 by 0.11-0.15: strong activation shifts mass from center to col 4.

## Conclusion
Top of the distribution is clean (early game, me = first player, opponent's stones on bottom corners (0,0)/(0,6), my stones in
the center/bottom row, center column free of opponent stones). But the 97th-percentile firing set is mostly midgame and not
captured by any simple board rule (best F1 0.18). Looks like a mixture or random direction. Confidence low.
