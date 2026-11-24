# U40 notebook (layer 5, pole +, threshold 0.739, dev max 12.0)

## Observations (examples, 40+ across bands)
- Firing is mostly early game (ply 4-12), plus some late (30+) positions with one nearly empty column (1-3).
- Top band: O (opponent) stones at (0,1),(0,3),(1,2),(1,3),(2,2); column 4 nearly empty (no stones above row 0).
- Steer: zeroing the unit lowers column 3 by ~3-8 points and gives it to col 2/1. Effect small.

## Hypotheses
H1: opponent stones clustered low in columns 1-3 (esp. (1,2),(1,3),(2,2)) while column 4 is empty/low.
H2: opponent building lines that run into column 4 (row 1, rising diagonals ending in col 4) -> column 4 poisoned.
H3: late game: a nearly empty column among full ones.

## act minimal pairs
- 1,6,3,2,3 = 7.56 (O (0,1),(0,3),(1,3), X (0,2)). Remove O(0,1) -> -0.18; move X(0,2) -> -0.27; O(1,3)->(1,2): 1.79.
- Translating the same shape one column right or mirroring: ~0 (very location specific).
- 3,3,x,2 (X (0,3); O (1,3),(0,2)) fires for every x tried (1.4-5.6).
- O vertical three in col 2 (6,2,6,2,5,2) = 1.78.
- Adding far stones changes act a lot (7.56 -> 0.28 .. 4.75): highly conjunctive/noisy.

## More act tests
- Grid 3,3,a,b: O at (0,2) (with O(1,3) over my X(0,3)) fires for any a; most other b do not.
- Grid 3,3,1,2,a,b: O at (1,1) kills (to -1.8..-2.9), O on (1,4) kills, O far right (0,5)/(0,6) boosts (10.25 for X(0,4),O(0,6)).
- Poisoned col 4 (O threat above col-4 landing, 1,2,3,3,6,1,6,2) does NOT fire: not a "col 4 is bad" detector.
- Rising O diagonal pairs and O-enclosed X stones do not fire when translated by one column.
- Same board, different move orders -> similar activation (board-determined).
- Bottom-row alternation XOX/OXO at cols 1-3 fires weakly; O at (0,0) kills.

## Histograms (ply 4-12, firing vs low bands)
O enriched at (1,2) 43 vs 21%, (1,3) 48 vs 21, (2,2) 29 vs 8; (1,4) and (1,1) nearly always empty; col 0 empty,
col 1 height 1, col 2 >= 1, col 3 >= 2, col 4 <= 1. Late (28+) firing: some column 1-3 at height ~2, but weak.

## Score calls
1 p1 O count in 6 low cells >=3, h4<=1, ply<=16: F1 0.215 P .165 R .309 AUROC .631, sim -0.07
2 p2 weighted O cells: F1 0.183, AUROC .571
3 p3 height profile (h3>=2,h2>=1,h4<=1,h1<=1,h0=0) + O in (1-2,2-3), ply<=14: F1 0.222 P .174 R .306 AUROC .632 (best)
4 p4 my low stone in cols 2-3 with >=3 O neighbours: F1 0.179
5 p5 bottom alternation cols 1-3: F1 0.142
6 p6 p3 + negatives (O at (1,1),(1,4),(0,0)), strict: F1 0.116 (P .34 R .07)
7 p7 p6 looser: F1 0.214
Simulation share always slightly negative (-0.05..-0.08).

## Effect (steer)
Forcing high: col 3 +25..30 points, col 4 -9..-19 points (e.g. 3,3,6,6; 3,2,4,4). Zeroing in firing positions: col 3 -3..-8 points.

## Conclusion
No clean concept. Highly conjunctive, not translation-invariant, sensitive to far stones. Possibly a random direction
or a mixture. Confidence low.

## Synthesis
3,3,1,2,4,6,1,0 = 12.19 and 1,2,3,3,4,6,1,0 = 12.30 beat dev max 12.03.
