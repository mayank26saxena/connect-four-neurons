# U69 notebook (layer 4, pole +, threshold 3.693, dev max 18.737)

## Observations from examples (bands 0-9, ~60 positions)
- Firing positions are all late game (ply ~28-40) with one nearly empty column (height 0-2) while the rest are almost full.
- Top band (9): almost always column 3 (center) empty or with 1 stone.
- Bands 5-8: the empty column is sometimes col 0, 1, 2, 4 (weaker).
- Band 4 (just below): also late game with a near-empty col 3 but ply lower / other partial cols.

## Hypotheses
- H1: late game (ply>=~26) and some column has height<=1; strongest for center.
- H2: column 3 nearly empty, level grows with ply (number of filled cells elsewhere).
- H3: count of empty cells concentrated in a single column (other columns near full).

## Tests
- act on 107200: -0.98 at ply 35 -> 13.9 at ply 36 (col 1 filled, only col 3 left). Activation alternates by ply in a game (150454: fires plies 29,31,33, not 30,32): fires when one particular side is to move.
- facts: in firing positions the opponent (last mover) has threat cells stacked in the near-empty column, and teacher usually says I am lost.
- H5 (opponent has two vertically adjacent threat cells): score call (note: accidentally ran score twice, calls 1-2 identical) F1 0.207 P 0.134 R 0.448 AUROC 0.68, sim -0.01. Rejected.
- New H6 (zugzwang parity): opponent has a threat cell on "their" parity row (row index even if opponent moved first, odd if second), i.e. a threat that the column-filling order will hand to them. All 6 checked firing positions satisfy it; the non-firing alternate plies did not.
- p2 score (call 3): F1 0.149 P 0.082 R 0.831 AUROC 0.776, sim -0.12. (Call 4 wasted by an accidental re-run with output discarded.) High recall, needs precision.
- p3 (ply>=26, their threats>=2 and > mine), call 5: F1 0.252 P 0.169 R 0.493 AUROC 0.71, sim -0.05.
- H7: unit = endgame 'I am lost by force' signal (explains per-ply alternation). p4 = exact endgame solver (alpha-beta, plain python), fires if ply>=28 and side to move loses with best play.
- p4 score (call 6): F1 0.395 P 0.267 R 0.758 AUROC 0.848, sim -0.82 (level hurts: too many FPs get high level).
  FPs are lost positions with 4-5 legal columns spread out (45343, 54588) or ply 28-29; misses include positions where I WIN (66354: one column left, I win immediately; 17464) and late draws (32699 ply 40).
  Lost position 64210 (4 legal cols) does not fire; firing lost positions have 1-3 legal columns.
- H9: lost by force AND at most 3 playable columns (play confined to a few columns). Level by how few columns remain.
- p5 score (call 7): F1 0.481 P 0.380 R 0.655 AUROC 0.812, sim -0.79. Best F1 so far. Steer: forcing the unit high in a non-firing position (107200 ply 35) moves 0.95 probability from the winning col 1 to the empty col 3; in 53037 +0.08 to the empty col 2; zeroing does nothing measurable in firing positions.
- Synthesis: 11419 extended with 5,6 (only col 3 left, lost) = 16.4; none beat dev max 18.7.
- p6: same fires as p5, softer level (1 col 9, 2 cols 6, 3 cols 3) to test whether the negative simulation comes from over-injecting at false positives.
- p6 score (call 8): identical (F1 0.481, sim -0.79); level scale does not matter, the negative simulation comes from false positives / misses. Final = p5. Confidence medium (F1 in 0.4-0.7, clear exceptions: some fires when I am winning or drawing with 1-2 columns left; lost positions with 4+ open columns do not fire).
