# U65 notebook (layer 5, pole +, threshold 0.512, dev max 7.681)

## Observations
- Firing examples are early-game (ply ~4-17, mean ~10); non-firing spread over all plies.
- Band 9 cell histograms: column 6 nearly empty; column 3 tall with alternating X(0,3)/O(1,3)/X(2,3)/O(3,3); O at (1,5) 65%.
- Minimal pairs are very idiosyncratic: 1,3,3,3 = 1.75 but 0,3,3,3 / 2,3,3,3 ~ -0.1. 4,4,3,5,5 = 3.2 but changing almost
  any single stone kills it (4,4,2,5,5 = 2.3 and 4,4,6,5,5 = 1.26 survive). 5,4,3,3,5,2 = 4.75; needs O(0,4) and X(1,5).
- Strong dependence on whose move: after one more reply the activation usually collapses.
- Steer: tiny effects (<= 0.10 prob), e.g. 1,3,3,3 max -> col6 +0.10, col5 -0.09.

## Hypotheses
H1: generic "early game, column 6 empty, centre column built up" (crude baseline).
H2: some local pattern around cells (0,4),(1,4),(0,5),(1,5) (2x2 block right of centre) - not consistent across examples.
H3: random/polysemantic direction (no clean concept).

## Score 1 (p1, H1 crude early/col6-empty): F1 0.114, P 0.073, R 0.259, AUROC 0.578, sim share 0.00. Too broad.
- Grid 1,3,3,3,k,j: my stone at (0,6) kills firing; their reply in col 5/6/2 kills; replies col 1,3,4 keep it.
- Early-game histogram (ply<=14) high vs low: enriched O(1,3), X(2,3), O(3,3), O(1,5), X(1,1), O(0,2); depleted X(0,6), X(0,2).
H2 (p2): additive hand-weighted cell score from those single-cell histograms, ply<=16.
## Score 2 (p2): F1 0.150, P 0.133, R 0.172, AUROC 0.568, sim 0.06. Misses include many mid/late-game positions.
H3 (p3): ply<=14, no my stone in col 6, (0,2) not mine, opponent stone at (1,3) or (1,5).
## Score 3 (p3): F1 0.152, P 0.112, R 0.240, AUROC 0.590, sim 0.03.
- Last-move variations on top examples: high activation usually needs one specific final opponent move.
- "Opponent stacks on my last stone": act tests mostly negative (0,6,2,2 / 2,2,4,4 / 0,0,3,3 all ~0).
- Opening 1,a,b,c family (my stone at (0,1)): fires when the two opponent stones are ADJACENT in cols 3-5
  (10/10 fire cases), never when non-adjacent (8/8), but adjacent pairs still fail when my 2nd stone is at (0,6) or (0,0)/(0,3) sometimes.
H4 (p4): ply<=14, no my stone col 6, (0,2) not mine, opponent has an adjacent pair inside cols 2-5 rows 0-4.
## Score 4 (p4): F1 0.125, P 0.082, R 0.264, AUROC 0.585, sim 0.00. Adjacent-pair idea does not generalise.
H5 (p5): ply<=14, no my stone in col 6, opponent stone capping my stone at (0,3)->(1,3) or (0,5)->(1,5).
## Score 5 (p5): F1 0.137, P 0.101, R 0.211, AUROC 0.576, sim 0.01.
Conclusion: no hypothesis beats F1 ~0.15; activation depends on idiosyncratic joint configurations (single-stone edits
flip it in ways no simple rule explains). Treat as no clean concept (possible random direction / mixture). Submit p3 (best F1).
Steer: effects <= ~0.10 probability, direction inconsistent across positions.
Synthesis: top examples extend 1,5,5,3,4,0,3,4,4,3,3 (opponent diagonal (3,3),(2,4),(1,5) aiming at (0,6)); variants reach 8.13-8.41 (beat dev max 7.68).
