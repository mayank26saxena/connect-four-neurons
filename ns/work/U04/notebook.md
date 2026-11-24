# U04 notebook (layer 1, pole +, threshold 1.990, dev max 6.0)

## Examples (60+ viewed, bands 0-9)
Firing positions are late-game, many columns full. Top band: column 6 almost always full, column 2 empty or 1 stone,
last move often col 6 or 0.

Hypotheses:
H1: column 6 is full (height 6) and column 2 is low (0-1 stones).
H2: generic "board nearly full / few legal moves".
H3: last move filled column 6.

## act tests
- Fill 6,5,4,3,1 leaving 0,2 empty: fires from ply 14 up to 3.8. Also filling col 0: stays ~3.5.
- Fill 6,5,3,2,1 (col 4 empty, col 2 full): fires only briefly (ply 16-20 ~2.3), then drops to 1.3 as col 2 fills.
- Fill 0,1,4,3,5 (col 6 empty, col 2 empty): never above 0.62. => col 6 full is essential; H2 rejected.

## score 1-2 (call 1 was an accidental duplicate run of p1 via a pipe; counts as 2 calls)
p1: col6 full & >=3 full cols & h2<=3 -> F1 0.366 (P .41 R .33), AUROC .66, sim share 0.38.
p2 (call 3): last move landed in row 5 (or row 4 in cols 0/6) -> F1 0.191, too broad.

## Key finding (act)
Tallied 300 firing examples (bands 5-9): column 6 is full in EVERY one. Last move (6, row5) is half of them.
Game trace 145230: after col 6 is topped off, activation alternates with parity: 5.3, -0.1(ply31?), 3.1, 0.9, 4.3, 0.5, 2.8, 0.06...
=> fires when the TOP CELL of column 6 (row 5) holds an OPPONENT stone (from the mover's view). When that stone is mine, ~0.
Same in game 72908 (col 6 topped by first player at move 37; position seen by second player -> theirs -> 4.6).
H4: grid[5][6] == theirs. Strength decays as more moves are played after it, lower when col 2 is filled.

## score 4 (call 4): p3 fires = grid[5][6]==theirs -> F1 0.614 (P .47 R .88), AUROC .93, sim share 0.49
Misses: col 6 top is mine but (4,6) is theirs (acts ~2.1-2.5). FPs: top theirs but act 1.4-1.97.
Counts over sampled examples (T-top positions): firing ones have lower col 2 (3.4 vs 4.6), fuller cols 4 & 5,
and col 6 topped more recently. act minimal pairs (6x6 then other cols): col 4 stones raise, col 2 stones lower.

## score 5 (call 5): p4 T-top & bonus(last6*2, h2<=3 *2, h4 full) >=2 -> F1 0.617 (P .64 R .60). Lost recall.
FPs had cols 5 low; misses had cols 4/5 full.
## score 6 (call 6): p5 T-top & bonus>=2 where bonus = [last move col 6] + [h2<=3] + [h4>=5] + [h5>=5]
-> F1 0.705 (P .649 R .771), AUROC .879, sim share 0.48.
## score 7 (call 7): p6 col 6 full; w = 2*[top theirs] + [row4 theirs] + bonus; fires w>=4
-> F1 0.701 (P .588 R .868), AUROC .925, sim share 0.51. Chosen as final (similar F1, better AUROC/sim).
One score call left unused.

## steer
- 145230 (5.3): zeroing drops col 4 from .59 to .36, raises 0/2/5. 
- 68638 (act 1.2, col 6 has 1 cell left): forcing max lowers col 6 by 12 pts (unit says "col 6 closed").
- 5 other positions: changes <= 4 pts. Effect is small; mostly in col 6 / near positions.

## synth
Best: 2,0,3x6,5x6,1x6,4x6,6,6,6,0,6,6,0,6 -> 6.109 (beats dev max 6.0); 2,0,3x6,1x6,5x6,4x6 + same tail -> 6.086.
Recipe: fill cols 1,3,4,5, leave col 2 (nearly) empty, opponent tops off column 6 on the last move.

## Synthesis redo (orchestrator audit, after submission)
Audit: all 5 original synthesis sequences passed through a finished game (e.g. move 21, col 4, completed row 0).
Wrote ns/work/U04/legal.py (four-in-a-row checker, legality only) and gen.py/gen2.py to enumerate column-fill
orders with single separator stones and col-6/col-0 tails, kept only sequences with no completed four, ranked by `act`.
New synthesis (all legal, no immediate wins/must-blocks at the end per `facts`):
- 3x6,2,5x6,1x6,0,4x6,0,6,6,6,6,0,6,6 -> 6.014 (beats dev max 6.0)
- 3x6,2,5x6,1x6,0,4x6,0,0,6,6,6,0,6,6,0,6 -> 6.012 (beats)
- 3x6,2,5x6,1x6,0,4x6,6,6,6,0,6,6,0,0,0,6 -> 5.936
- 3x6,2,5x6,1x6,0,4x6,6,6,0,6,0,0,6,0,6,6 -> 5.721
- 2,0,5x6,1x6,0,3x6,0,4x6,6,6,6,0,6,6,0,6 -> 5.659
Only the synthesis field and one notes line changed in final.json; no score calls used.
