# U30 notebook (layer 4, pole +, threshold 2.96, dev max 10.4)

## Examples
- Firing positions are all late (ply ~19-38), often only 1-3 legal columns, deep wells.
- Facts: firing positions are mostly LOST for the side to move (teacher ~ -960..-980) with opponent threat cells
  (their_wins) above landing cells. Sub-threshold ones (band 3-4) often have a winning move or are only partly poisoned.
- Trajectory test (game 3,6,2,4,...): ply 22 me winning w/ my threats -> -0.3; ply 23 same threats now theirs -> 8.85.
  So the unit cares about the OPPONENT's threats (side-specific).
- Early lost positions (double open threat on row 0, e.g. 3,3,4,4,2) do NOT fire (-0.16). So not plain "lost".

## Hypotheses
H1: opponent has threat cells (their_wins) and I have fewer/none, late game.
H2: "poisoned columns": legal columns where the cell directly above the landing cell is an opponent threat; count/fraction.
H3: general "I am lost late in the game" (not computable directly).

## score 1 (p1: their_wins>=1, >= my count, ply>=14): F1 0.106, P 0.057, R 0.84, AUROC 0.71, sim -0.01. Far too broad.
Misses typically have both sides' threats in one column; common element is an opponent threat directly ABOVE a landing
cell (poisoned column). Moving to H2.

## score 2 (p2: any poisoned column): F1 0.128, P 0.069, R 0.875, AUROC 0.76. Still far too broad; threats not the key.

## Big clue (minimal pair, game 41795 at ply 31): after 30 moves -0.9; last move col 4 (fills col 4) -> 8.74; last move col 6
(fills col 6, same threats) -> -0.84; col 2 -> -0.97; col 5 -> -0.84. Almost every firing example has COLUMN 4 FULL.
Sub-threshold band 3-4 examples also have col 4 full. FPs from p1/p2 had col 4 open. But colors matter: in game 1, ply 22 and 23
both have col 4 full yet -0.3 vs 8.85 (perspective flip).
H4: column 4 full (+ something about stone colours in/around it).

## score 3 (p3: heights[4]==6): F1 0.238, P 0.135, R 0.997, AUROC 0.90, sim 0.23. Column 4 full is (nearly) NECESSARY.
Within col-4-full: band histogram of heights / col-4 colours shows no clean height or colour pattern.
Adjacent-move swaps (colour flips of 2 stones) in a firing game barely matter.
Parity alternation inside games: in game 4,4,1,3,... plies 29/33 (me has threats, they have none) -1.2/-1.7;
plies 30/34 (they have the threats) 3.4/4.6. Game 3,6,2,... same: ply 22 my threats -0.3, ply 23 their threats 8.85.
H5: column 4 full AND opponent has at least one threat cell (their_wins non-empty).

## score 4 (p4: col4 full & their_wins non-empty): F1 0.270, P 0.157, R 0.975, AUROC 0.91, sim 0.24. Small gain.
Within-game alternation tracks the engine value: plies where side-to-move is LOST (with col 4 full) are high, winning plies low
(game 5,1,2,...: ply 31 win 0.9 / 32 lost 1.6 / 35 win -1.5 / 36 lost 3.5). But exceptions: 41795@31 (col 6 wins) = 8.7;
misses 31278 / 59171 fire with my immediate win available. So value is only part of it.
H6: col 4 full AND most of my legal moves lose at 2-ply (poisoned column, or must-block not answered).

## score 5 (p5: col4 full & >=half of legal moves lose at 2-ply): F1 0.371, P 0.274, R 0.574, AUROC 0.76, sim 0.25.
Precision up, recall down. Misses: col 4 full, opponent threats stacked in an open column, but not 2-ply lost.
Next: union of "mostly bad moves" and "opponent has more threat cells than me", graded level.

## score 6 (p6: union rule): F1 0.338, P 0.216, R 0.771, AUROC 0.84, sim 0.25. Worse F1 than p5; union adds too many FPs.
Final candidate p7 = p5 fires + p6-style graded level (all col-4-full positions get a nonzero level).

## score 7 (p7 = p5 fires + graded level): F1 0.371, P 0.274, R 0.574, AUROC 0.76, sim share 0.25. Final.
Steer: zeroing in firing positions changes move probs by <=3 points (col 4 already full). Forcing to max where col 4 is open
can suppress column 4 (3,3,4,2,4: col 4 0.50 -> 0.01, col 3 +0.48); elsewhere ~0-6 points. Reads as a "column 4 unavailable" signal.
Synthesis: continuations of game 3,6,2,4,... (col 4 full, opponent with stacked threats in cols 0/5) reach 11.7-13.4 (dev max 10.4).
Confidence medium-low: col 4 full is a near-necessary condition (recall 0.997), but what grades the activation inside that set
is only partly captured by a "my moves lose" proxy. F1 0.37 < 0.4 => low.
