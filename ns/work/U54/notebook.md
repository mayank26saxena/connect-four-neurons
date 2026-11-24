# U54 notebook (layer 2, pole -, thr 0.823, dev max 2.353)

## Exploration
- 40 examples + 300 firing (bands 5-9, seeds 1-3) and 270 low (bands 0-2) tallied (simple counts).
- Firing is skewed to early game (78% ply<=16 vs 44%), lower rows, emptier boards.
- Cell lifts: their stone at bottom-centre (0,3) 61% vs 42%; my stone at (0,3) 24% vs 42%; (0,5) empty 51% vs 23%;
  I have no stone in column 3: 50% vs 25%. Must-block present 22% vs 11%.
- Last-move column: col 3 overrepresented (31%), otherwise flat. No parity effect (me_first ~50/50).
- Activation oscillates strongly move to move within a game (e.g. high at every B-to-move ply from 9-17 in one game,
  low at the A-to-move plies) -> depends on whose perspective the board is read from, not on a single cell.
- 2-ply grid: fires for X elsewhere + O at (0,3) (1,3 / 2,3 / 4,3 / 6,3) and for 3,5; strongly negative when O is in col 1.
- Vertical-three for them: fires in col 2 and 3, not in col 1/4/5 -> not a clean threat detector.
- Steer: forcing to max or zero changes move probabilities by <= 0.01 on 4 positions -> no measurable effect.

## Hypotheses
H1: opponent owns bottom-centre (0,3), I have nothing in column 3, early game (additive score).
H2: generic "opponent has a must-block threat" (lift only 2x; weak).
H3: no clean concept / distributed direction (possibly a random control).

## Dev metric log
- call 1/8: p1 (additive: their (0,3), no mine in col 3, (0,5) empty, early, must-block). Output lost (I piped through tail
  and re-ran); wasted a call.
- call 2/8: p1 again: F1 0.189 (P 0.154, R 0.245), AUROC 0.602, sim share 0.03.
- call 3/8: p2 (continuous additive score: their (0,3) +, mine (0,3) -, theirs at (0,5)/(0,6)/(0,1) -, ply 2-16 +,
  ply>24 -, last stone stacked on the opponent's own stone +, no mine in col 3 +): F1 0.207 (P 0.159, R 0.296),
  AUROC 0.682, sim share 0.03.  BEST.
- call 4/8: p3 (simple: ply<=16 and they outnumber me in column 3): F1 0.138, AUROC 0.624. Worse.
- Stopped at 4 calls: every single-stone minimal pair moves the activation by 0.2-0.7 in a column-dependent,
  context-dependent way (e.g. bottom row OXOO.XX 0.98, OXO.OXX 0.33, OXOOXX. 1.31; stacking-own-stone fires for
  2,4,2 but not 4,2,4 / 0,6,0). No discrete concept found; looks distributed.

## Steering
- 7 positions (4,3; 1,0,5,2,6,1,6,3; 4,5,5,...,0; 4,3,5,...,5; 6,5,4,...,2; 3,0,3,4,3; 6,3,3,3,1,3,0,1):
  max or zero changes every column by <= 0.01. No measurable effect.

## Conclusion
Low confidence. Weak tendencies only: early/mid game, opponent stone on bottom-centre, I have little in column 3.
Behaves like a distributed (possibly random) direction.
- Synthesis: greedy pair search with act from 1,0,5,2,6,1,6,3 reached 1.874 (1,0,5,2,6,1,6,3,6,4); best dev-derived 1.705, 1.651. None beat dev max 2.353.
