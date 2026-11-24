# U12 notebook (layer 5, pole +, threshold 4.557, dev max 37.98)

## Examples (bands 0-9, ~70 viewed)
- Band 9 is dominated by: I (side to move) have an immediate playable win, very often at (1,3): column 3 holds 1 stone,
  surrounded by tall columns, win cell just above it. Others: (2,0), (0,3), (2,3).
- Band 5-8: mostly a playable win for me too, but some firing with no immediate win (often a must-block, or a low/empty column in a full board).
- Low bands: early/mid positions without wins.

## Hypotheses
H1: fires when I have an immediate (playable) win.
H2: H1 restricted/strengthened by the win being in a low row / short column (esp. center column 3), late game.
H3: fires on "a nearly empty column in a tall board" (structure), win or not.

## act / facts tests
- 2,2,3,3,4,6 (X row0 2-4, two playable wins) = 13.3 FIRES; 2,2,3,1,4,6 (same but one end blocked, single win) = 0.9.
- 0,0,1,1,2,6 single win (0,3) = 1.2; vertical win 3,4,3,4,3,6 = 0.0.
- Game 84192: activation jumps to 14 at ply 20 / 11.8 at ply 22 with NO immediate win but stacked my threats (1,3),(2,3)
  (teacher: every move wins); 28 at ply 24 with immediate win (1,3) (all moves still win).
- Firing non-win examples: teacher scores show nearly all legal moves decided (|score|>900): 14947 (all but one win),
  1298 (all win), 54981 (double must-block, all lose = 7.0).
H5 (new, leading): fires when the game is DECIDED regardless of my move (mostly: I win whatever I do), e.g. two playable
wins, an immediate win backed by a stacked threat above it, or a double must-block; magnitude larger for wins and late game.
A single, early, "only-move" win does not fire.

## score 1 (p1: >=2 playable wins, or 1 playable win and (ply>=18 or my win directly above it), or >=2 must-blocks)
F1 0.669 (P 0.581, R 0.790), AUROC 0.887, sim share 1.45. FPs are mostly just under threshold (4.0-4.4).
Misses: early-ish immediate wins (ply 16, act 31), and positions with no immediate win but forced win (teacher: all moves win),
e.g. stacked my threats above the landing cell.
Band-9 facts: almost all = playable win with my second win cell directly above (column 3, row 1).

## score 2 (p2: added "two stacked my-win cells anywhere above landing" and dropped the ply rule)
F1 0.278 (P 0.18, R 0.60). Stacked non-playable threats are a massive FP source; the late-game single-win rule carried a lot of recall.
Back to p1 family.

## score 3 (p1 with ply>=14): F1 0.671 (P 0.580 R 0.795), AUROC 0.889, sim 1.45. Ply cutoff hardly matters.
## score 4 (p4: excluded single wins that are also the opponent's must-block): F1 0.650 (P 0.60 R 0.71), sim 1.63. Worse F1; shared cells still fire often.
Misses in s4: no immediate win, but the teacher scores ~+970 for (nearly) every legal move, and I hold 3 threat cells
(e.g. 7463, 23046, 4071, 40461). FP 11483: stacked immediate win but every other move loses -> act ~0.
=> The unit looks like "won no matter what I play" (game decided in my favour), immediate wins being the common case.

## score 5 (p5: + "no immediate win, >=3 my threat cells, no must-block, ply>=14"): F1 0.390 (P 0.25 R 0.86). Far too broad; dropped.
## score 6 (p6 = p3 detection, level graded; 3-threat positions given level 3): F1 0.671 (P 0.580 R 0.795), AUROC 0.889, sim share 1.64. FINAL.

## steer
- 84192 (win at (1,3), act 28): max +0.02 on col 3; zero -0.08 on col 3 (spread to others).
- 966 (act 31): zero -0.07 on winning col 3, +0.04 col 6; max +0.01.
- 3,3,4,1,5,4 double win: ~no change. 7463 (forced win, no immediate): max -0.08 col 2 / +0.07 col 5 (mixed).
- Low-activation single win positions: no change. Effect: small; mainly keeps probability on the winning column in decided positions.

## synthesis (greedy 2-ply extensions from dev pos 171281)
best 42.92: 0,2,2,0,0,5,2,4,3,5,4,4,1,0,1,0,6,5,1,1,6,1,6,6,4,2 (win at (1,3) with my threats (2,3),(3,3) stacked above). Beats dev max 37.98.
