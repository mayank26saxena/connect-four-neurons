# U22 notebook (layer 3, pole -, threshold 0.813, dev max 9.563)

## Observations
- Examples bands 0-9 read. Per-cell occupancy histograms by band (single features): in bands 8-9, opponent stone at (3,3) in ~95%
  (my stone there ~0%); opponent at (2,4) ~85%; col 2 height mostly 1-3 (rarely 0); col 3 height >= 4.
- Activation alternates in a game: once it fires it tends to fire at every ply of the same side to move (board-state, persistent).
- Steer to zero on 3 top positions: tiny effects (<= 0.09 prob shifts).

## Hypotheses
- H1: opponent at (3,3) and (2,4) (diagonal pair). Minimal pair constructions with just those stones (3,3,3,4,4,4,0,3 etc.)
  do NOT fire (-0.3..-0.6). Even a 3-in-anti-diagonal (3,3),(2,4),(1,5) did not fire.
- H2: opponent vertical pair at (2,3),(3,3): mixed: 3,3,6,3,0,3 fires 1.5, 3,0,3,3,6,3 = 0.03, 3,5,3,3,6,3 = 0.78.
- H3: opponent anti-diagonal threat at (4,2): facts show their threat (4,2) in several top examples, but construction failed.
Minimal pairs disagree with simple rules: the unit looks context dependent.

## score 1 (p1: their (3,3) & their (2,4)): F1 0.284 (P 0.195, R 0.521), AUROC 0.728. Simulation: unit effect tiny (ceiling negative, share nan).
Misses include same structure shifted (col 4 vertical pair) and positions without (2,4).

## Grid experiments (two-move continuations)
- From firing P=1,1,3,4,3,1,4,3,6,4,1,2 (1.86): X at (3,3) kills it in every case; O at (3,3) boosts to 2.4-5.2; X at (3,4) mostly kills.
- From non-firing 3,3,3,4,4,4,0,3 (their (3,3),(2,4) but mine (2,3),(1,4)): no continuation fires. So (3,3) theirs is not sufficient.
- From 89300 (ply 15): every continuation still fires (robust board state).
- Removing my stones at (3,1),(4,1) in P drops it 1.86 -> 0.32.
Row-3 histogram profile of firing: (3,3) theirs ~90%, never mine; (3,2) usually empty; (3,5) rarely theirs; (3,1) often mine.
Steer max/zero: changes <= 0.04-0.09 in probs, slightly lowers col 3/4. Effect basically none.

## score 2 (p2: their (3,3),(2,4); (3,2) empty; (3,5) not theirs): F1 0.333 (P 0.306 R 0.365) AUROC 0.670
## score 3 (p3: hand-set cell weights from histograms): F1 0.327, AUROC 0.715. No gain -> cell-weight view not enough.
## score 4 (p4: 'poisoned column' (their threat right above a landing cell) + centre): F1 0.131. Dropped.
## score 5 (p5: their (3,3), (3,2) empty, (3,5) not theirs, and their (2,4) or (2,3)): F1 0.337 (P 0.255 R 0.496) AUROC 0.726. Best.
FPs of p2/p5 often have the same centre stones but the unit stays off (e.g. 3,4,3,3,4,4,0,3 = -0.40 despite their
(2,3),(2,4),(3,3)); strong dependence on stones far away (my stones at (3,1),(4,1) add ~1.5). Looks distributed/mixed.
Simulation share undefined (nan): zero-ablating the unit barely changes moves (perfect reader ceiling is negative).
## Synthesis: greedy two-move search from game 1,1,3,4,3,1,4,3,1,4,1,2,6,4,0,3 gave 10.0-10.6 (> dev max 9.563);
boards have their 2x2 block at (2-3, 3-4) + (4,3). Steer zero there: col 3 prob +0.07 (unit slightly lowers col 3).
Confidence: low (F1 < 0.4).
