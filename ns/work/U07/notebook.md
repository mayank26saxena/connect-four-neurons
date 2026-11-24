# U07 notebook (layer 2, pole +, threshold 0.622, dev max 7.753)

## Observations from ~100 examples
- Nearly every firing position has odd ply (me = second player, opponent = first player).
- High band: opponent has threat cells, often directly above a landing cell ("poisoned" column: playing there lets them win).
  Column 2 often empty in top examples; column 6 threats frequent.
- But poisoned columns also occur at odd ply with ~0 activation (e.g. threat at (3,3) above landing in col 3).

## Hypotheses
- H1: odd ply AND opponent has a threat directly above a landing cell.
- H2: odd ply, late game, with an empty/low column among tall ones (col 2).
- H3: depends on specific columns of the opponent threat (edge/side columns vs center).

## Tests
- 0,3,3,4,4,5,5 (+6,2): poisoned cols 2 and 6 at ply 7/9 -> no firing (-0.03/-0.18). Early game weak.
- Fill cols 0,1,3,4 alternating, col 2 empty, no threats, ply 27 -> 0.54 (below threshold): low column alone weak.
- Game 0,5,3,6,3,1,1,0,1,1,4,3,4,3,5,6,5,4,0: fires only at odd ply, rises 1 -> 6.5 as ply grows; even plies ~0.2.

## Score log
- call 1/2 (p1.py; call 1 was an accidental double run of the same program): odd ply AND opponent threat directly above a landing cell, ply>=15.
  F1 0.140 (P 0.083, R 0.427), sim share 0.01. Poisoned-column idea rejected.
- Minimal pairs on game 0,5,3,6,3,1,1,0,1,1,4,3,(x),4: firing appears when opponent adds (1,4); X filling (0,2) or (1,4) kills it.
  Synthetic boards (helper mk.py turns a column layout into a move list):
  them (0,3),(1,4),(2,5) + filler -> 0.82; removing any one of the three -> ~0; mirror diagonal (0,3),(1,2),(2,1) -> -0.8.
  Base "- S - FF SF SFF S" (1.40): drop them(0,3) -> 0.32, drop them(1,4) -> 0.45, drop them(2,5) -> 0.88, drop them(1,3) -> 1.12;
  adding MY stone at (2,4) raises 2.58 -> 3.30. When the same stones belong to "me" (even ply, P1 to move) -> ~0.
- call 3 (p2.py): them on all of (0,3),(1,4),(2,5) and odd ply. F1 0.310 (P 0.46, R 0.23), sim 0.07.
  Misses include even-ply positions where the opponent (second player) owns the same cells -> parity is not essential.
- call 4: accidental rerun of p2 (wasted).
- Cell histograms over 400 dev examples (simple counts): top band (>2.0) has them at (0,3) 96%, (1,3) 98%, (1,4) 90%, (2,5) 90%,
  (1,5) 64%; me at (2,4) 86%, (2,3) 58%; (1,2) almost never theirs (usually empty, often their threat cell). 80% of firing at odd ply.
- call 5 (p3.py): weighted count of those cells, no parity. F1 0.365 (P 0.43, R 0.32), sim 0.15.
- call 6 (p4.py): weights 2*(them 03,13,14,25) + them15 + 2*me24 + me23 + me16 - 2*them12 + 2 if odd ply, fire >= 11.
  F1 0.445 (P 0.463, R 0.429), AUROC 0.706, sim share 0.20. BEST.
- call 7 (p5.py): parity bonus 1, threshold 10: F1 0.433, sim 0.22. No gain.
- Remaining misses are heterogeneous (some with X at (0,3), some with column 4 empty); activation also flickers with the
  last move (layer 2, token-sequence effects), e.g. a game with the full pattern oscillates 1.2 / -0.06 / 0.64 on successive plies.

## Steering
- max on 3 positions, zero on 3 positions: changes <= 0.04 in any column. Effect essentially none measurable.

## Synthesis
- Greedy extension of 0,5,3,6,3,1,1,0,1,1,4,3,4,3,5,6,5,4,0,4,0: best 7.972 (beats dev max 7.753) at
  ...,6,3,4,1,6,3 (ply 27): them at (0,3),(1,3),(1,4),(1,5),(2,5), me at (2,3),(2,4), col 2 empty.

## Conclusion
Medium confidence: clear core (opponent's lower-centre "staircase" (0,3),(1,3),(1,4) -> (2,5) under my (2,4)), confirmed by
minimal pairs, but dev F1 only 0.45 and many firing positions lack the full pattern.

## Synthesis revision (orchestrator audit)
- Audit: ...,6,3,4,1,6,3 (move 26) and ...,6,3,6,1 (move 24) complete a four mid-sequence, so they are not legal games.
- Wrote chk.py, which finds the first move that completes a four. I searched 2-move extensions of the valid prefixes and kept only
  sequences where no move completes a four.
- New set (synth): B+6,3,4,1,1,3 = 8.072 (beats dev max), B+6,3,4,3 = 8.010 (beats), and the kept ones: B+6,3,4,1 = 7.645,
  B+6,3 = 7.318, B+6,1 = 7.243 (B = 0,5,3,6,3,1,1,0,1,1,4,3,4,3,5,6,5,4,0,4,0). Only the synthesis field and notes changed.
  No score calls used.
