# U17 notebook (layer 1, pole -, threshold 0.313, dev max 2.206)

## Examples (60+ viewed, bands 0-9)
- Top bands dominated by ply-3 positions (opponent = first player has 2 stones, I have 1), esp. opponent stones in cols 3/4/5 and my stone in col 4 (5,4,3 = 1.94; 4,4,3 = 1.58; 0,4,3 = 1.48).
- Some later-game firings, often last move in col 6 on top of a stack, or odd ply mid-game; mixed.

## Hypotheses
H1: early-game (ply 3, sometimes 5) detector: second player to move, opponent has stones in the centre (cols 3-5).
H2: late-game part: something about last move/col 6 stacks (unclear).
H3: generic "opening position with opponent centre stones" mixture.

## act tests
- ply 3: 5,4,3 1.94; 4,4,3 1.58; 3,4,3 1.41; 4,6,3 1.11; 4,0,4 1.0; 4,1,4 0.16(!); 5,4,1 0.01(!); 5,4,0 0.71
- ply 3 with no opp centre stones: 0,0,0 / 6,6,6 / 0,1,2 / 1,1,1 ~0; 3,3,3 -0.08; 3,5,5 -0.30 (my stone in 3/5 hurts)
- ply 2: mostly no (4,3 0.56 and 4,5 0.37 fire, others <0.1)
- ply 4: all no (< 0.25). ply 5: several fire (3,4,4,3,5 0.70; 3,3,3,4,4 0.57)
- So odd ply (me = second player) in the opening, with opponent centre stones.
- score p1 (ply==3): F1 0.212 P .217 R .208, sim share 0.03. (accidentally ran twice; 2/8 used). ~80% of firing is NOT ply 3 -> study mid-game.
- score p2 (early rule: odd ply<=9, opp >=2 stones in cols 3-4 or 1 in 3-4 + 1 in 5, no my stone in col1; ply2 4,{3,4,5}): F1 0.209 P .198 R .220, sim 0.04. No gain.
- Late-game (ply>=10) firings (~75% of firing): counts of last-move col, capping, top-owner per column, heights, opp-minus-mine per column: all only weakly different between firing and near-miss bands. Activation in late game is a board-level baseline (+-0.3 by last move col), swings sign with tiny colour changes (e.g. same stone layout with colours swapped: 0.50 vs 0.04/-0.75).
- Big constructed max: 4,6,4,6,5,6,6 = 2.48, 4,6,4,6,3,6,6 = 2.21, 4,6,3,6,4,6,6 = 2.19 (opponent centre stones + my 3-stack in col 6 capped).
- steer: 5,4,3 zero -> no change; 4,6,4,6,5,6,6 max/zero -> 0.00; 4,4,3 -> 0.00; late board (20 moves) max -> col4 -0.03. Effect essentially none.
- Suspicion: random direction; extreme values in the opening are what any direction shows on atypical early residuals.
- score p3 (ply-3 table-derived rule + ply 5/7 discounted, ply 2 cases): F1 0.346 P .419 R .294 AUROC .641, sim share 0.07
- score p4 (drop ply 7; ply 5 needs last move in cols 3-5): F1 0.363 P .581 R .264 AUROC .629 sim 0.07
- score p5 (ply-5 tightened): F1 0.362 P .626 R .254. Same. Final = p4. Stopping at 6/8 calls: remaining ~70% of firing is mid/late-game, near-threshold, with no structure found by counts or minimal pairs; steering effect ~0. Confidence low (possible random direction).
