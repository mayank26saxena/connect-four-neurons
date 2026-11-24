# U07 notebook (layer 5, pole +, threshold 1.501, dev max 29.1)

## Examples (bands 0-9, 52 positions read)
- Firing positions are mostly mid/late game; the player to move almost always has threat cells (my_wins), often
  several, often stacked in one column (e.g. (1,1),(2,1)), and teacher scores show me WINNING (~+970) for most moves.
- Not firing: early bottom-row double threat 2,2,3,3,4,0 (-4.9) even though winning; positions where opponent is winning.

## Hypotheses
- H1: I have a horizontal three / horizontal win cell. act: 2,2,3,3,4,0 = -4.9, elevated row-1 three 3,2,2,4,4,6,3,x ~ -0.1..-0.8. Rejected as sufficient.
- H2: I have two of my threat cells stacked vertically. Partly: 13209, 116302, 102502, 40819 all stacked; constructed
  stacked position 3,2,2,4,4,0,3,6,3,3,2,0,4,6 = 4.84 (fires) but non-stacked 3,2,2,4,4,0,3,6,3,3 also fires 3.25.
- H3: "player to move is (decisively) winning", a value-like unit. Trajectories: in games 102502/40819 it fires on every
  ply where the winning side is to move and is ~0 on the other side's turns. Minimal pair 3,2,2,4,4,0,3,6 (-0.08, teacher
  mixed 13/983) vs ...,3,3 (3.25, teacher all 981+). But 2,2,3,3,4,0 (all 991, immediate wins) = -4.9 -> exception for
  early immediate bottom-row wins.

## Key finding: column 1 asymmetry
- Mirroring games (c -> 6-c): 102502 18.1 -> 2.6; 77509 15.2 -> 1.7; symmetric 40819 17.1 -> 17.2.
- Constructed stacked threats in col 1 (3,2,2,4,4,5,3,5,3,3,2,0,4,5[,5,6]) = 7.4 / 7.9; mirror (stack in col 5) = -0.8 / 1.3.
- Single col-1 threat directly above an empty col 1 (3,2,2,4,4,5,0,5,3,6) = -0.24; early immediate col-1 win (..,3,1) = 0.09.
- steer max on 3 positions: raises column 1 (+0.71, +0.34, +0.17); zero on top examples lowers col 1 (-0.11, -0.05).
- Misses also include many late-game positions where I am clearly winning with wins elsewhere (value-like component),
  and a few losing positions -> looks like a mixture: "column 1 is a winning move" + generic "I am winning".

## Dev metric
| call | program | F1 | P | R | AUROC | sim share |
|---|---|---|---|---|---|---|
| 1 | len(my_wins)>=2 | 0.150 | 0.08 | 0.72 | 0.74 | -0.42 |
| 2 | stacked my wins in col 1 | 0.166 | 0.31 | 0.11 | 0.55 | 0.28 |
| 3 | my win in col 1 at landing..landing+2 | 0.206 | 0.14 | 0.41 | 0.67 | 0.88 |
| 4 | p3 OR late immediate win OR stacked anywhere | 0.294 | 0.18 | 0.83 | 0.86 | 0.16 |
| 5 | strict col-1 rules | 0.248 | 0.22 | 0.28 | 0.62 | 0.69 |
| 6 | col-1 rules (needs >=2 threats or stack) OR (ply>=12, immediate win + another threat) OR stacked | 0.318 | 0.21 | 0.71 | 0.81 | 0.52 |
| 7 | p6 minus positions with opponent must-block | 0.312 | 0.21 | 0.64 | 0.78 | 0.50 |
| 8 | p6 fires + col-1-weighted level | 0.318 | 0.21 | 0.71 | 0.81 | 0.64 |
Final = p8. Precision never exceeded ~0.3: lots of positions with these threat patterns do not fire; the unit tracks
something closer to the engine's judgment that col 1 (or the position) is won, which board patterns only approximate.

## Synthesis (greedy act search from dev-like lines): best 22.85 (below dev max 29.1).
