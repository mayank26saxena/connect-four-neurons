# U24 notebook (layer 1, pole -, threshold 0.870, dev firing 3.0%, dev max 3.581)

## Examples (band 0-9, ~70 viewed)
Top bands: almost always opponent (O) stones in column 4 (often 2+, often at (0,4),(1,4)), and column 5 empty
(sometimes height 1). Many fire at low ply (5-16 moves).

## Hypotheses
H1: >=2 opponent stones in column 4 and column 5 empty (or nearly).
H2: opponent stack at the bottom of column 4 ((0,4) and (1,4) theirs), col 5 empty.
H3: sequence-dependent layer-1 mix (token order matters), no clean board rule.

## act tests
- 0,4,0,4 1.93 F; 6,4,6,4 2.07; 6,4,6,4,6,4 (OOO in col4) 3.18. Single O in col4 ~0.2-0.5 only.
- Two O anywhere else: <0.75. Two O in col4 => 1.93. Column 4 is special.
- Third stone (6,4,6,4 + X@c,O@1): any stone in col 5 lowers (2.07 -> 1.35 / 0.99); stone on top of col4 raises (2.7/2.57).
- But X at (0,4) under O,O: 4,4,0,4 = 0.06; 0,4,0,4,4,4 (O,O,X,O) = 0.07, but 1,4,6,4,4,4,6,6 (same col4) = 3.49 vs 1,4,6,4,4,4 = 0.42.
  -> strong context/sequence dependence; not purely col 4 content.
## steer
Effect tiny: zeroing raises col 3 by ~3-6 points, lowers col 4/1 by ~2-6; forcing max: col 3 -3. Unit weakly suppresses column 3.

## Score 1 (h1: >=2 O in col4 and col5 empty): F1 0.299 (P 0.225, R 0.445), AUROC 0.698, sim share 0.31.
FPs are late-game boards; misses have col5 height 1.

## Sequence tests (same final board, different move order)
- 0,4,0,4,1,1,2,2,6,6 = 0.83 vs 1,1,2,2,6,6,0,4,0,4 = 1.70. Recency of the opponent's col-4 moves matters, and more stones overall lowers.
- Need 2+ opponent col-4 stones; a single recent one ~0.37. One recent + one old is enough (0,4,1,1,2,2,6,6,0,4 = 1.57).
- Odd: an opponent col-4 move landing on a mixed column is low right after it is played (0,4,4,4 = 0.16; 1,1,4,4,0,4,0,4 = 0.00),
  but recovers after a pair of other moves (0,4,4,4,1,1 = 2.69).
- Any stone in col 5 lowers (6,4,6,4 2.07 -> 1.0-1.35).

## Score 2 (h2: >=2 O in col4, col5 h<=1, opp col4 among last 2 opp moves, ply<=24): F1 0.390 (P 0.307 R 0.534) AUROC 0.747 sim 0.37
Recent moves in columns 3 or 5 (either player) strongly suppress: 0,4,0,4,3,3 0.52, 0,4,0,4,5,5 0.56 vs 0,4,0,4,1,1 2.09 / 2,2 1.51.
Older col 3/5 moves suppress less (3,3,0,4,0,4 1.63). -> H3: recency-weighted token score.

## Score 3 (h3: recency-weighted token score, col3/5 moves negative): F1 0.175, AUROC 0.571, sim 0.30. Worse; dropped.
Col heights placed early (then 0,4,0,4): col1 2.85, col2 2.50, col6 1.99, col3 1.63, col5 1.42; 4 stones: col3 1.05, col5 0.87.
-> stones in cols 3 and 5 lower it on the board too, not only when recent.
H4: additive score: base(O in col4) - 0.4 per opponent move since their last col-4 move (beyond 1) - 0.3 per stone in cols 3,5,
  minus a penalty when the last move is an O dropped onto a col 4 that holds my stones (row>=2).

## Score 4 (h4 additive, opp-count base): F1 0.382, AUROC 0.719, sim 0.37. FPs late game; misses with my stones in col 4.
Owner test (col 4 contents, last move elsewhere, ply 4-8): XOX .82, OXX 1.87, XXO 1.93, XOO 2.75, OXO 2.99, OOX 2.71,
OO 2.40, XX .76, XXX 1.12-1.26, O .05, X -.02. -> column 4 HEIGHT matters (2-3+ stones), each opponent stone adds ~0.8.
Suppression right after an O lands on row 3 of col 4, or on row 2 above my stone (0,4,4,4 .16; 1,4,4,4,0,4 .01), recovers after other moves.
Games starting with 4 tend to be lower (4,4,0,4 .06 vs 1,1,4,4,0,4 1.54): token-order effect not captured.
H5: height-based additive score with ply penalty.

## Score 5 (h5): F1 0.385 (P 0.265 R 0.704) AUROC 0.820 sim 0.39. Ranking much better; too many FPs near threshold -> raise threshold to 1.3 (h6).

## Score 6 (h6 = h5 with threshold 1.3): F1 0.425 (P 0.342 R 0.561) AUROC 0.763 sim 0.39.
Tall col 4 kills it: height 5 / 6 -> ~0 (6,4,6,4,4,4,4,4,1,1 = 0.04; 4,4,4,4,4,4,1,1 = -0.24) though height 4 still fires (1.38-1.72).
Recency decay steeper than assumed: 6,4,6,4 + 3 filler pairs 0.72, + 5 pairs -0.29.
H7: HS for heights 4/5/6 = 1.0/-0.5/-2.0, since-penalty 0.6 per opponent move (cap 6).

## Score 7 (h7): F1 0.545 (P 0.566 R 0.526) AUROC 0.756 sim share 0.48. Best so far.
H8: + -0.5 for each of the last 2 moves in col 3/5; mixed-column penalty only when the stone directly below the new row-2 O is mine.

## Score 8 (h8): F1 0.533 (P 0.612 R 0.471) AUROC 0.731 sim 0.48. Not better; final program = h7.
## Synthesis: 1,4,1,4,1,4 (three O stacked in col 4, X in col 1) = 3.628 BEATS dev max 3.581; 1,4,6,4,4,4,6,6 3.49; 1,4,1,4,1,4,4,1 3.43.
## Effect (steer, 4 positions): tiny. Zeroing raises col 3 by ~3-6 points and lowers col 4 / col 1 by 2-6; forcing max lowers col 3 ~3.
