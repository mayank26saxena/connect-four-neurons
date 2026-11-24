# U69 notebook (layer 4, pole +, thr 3.693, dev max 18.737)

## Observations (60 examples)
- Firing positions are all late game (ply ~25-40). Nearly always the centre column 3 is empty or holds just 1 stone while most other columns are tall/full.
- Top band (>11): col 3 height 0-1, all other columns nearly/fully full.
- Some band-5 firing cases have col 3 full but another column (4 or 2) nearly empty (e.g. pos 18952 col 4 h=1).
- Low bands: early game or col 3 filled.

## Hypotheses
H1: fires when heights[3] <= 1 and the board is mostly full (ply >= ~24); level grows with ply / how tall the rest is.
H2: more general: some column with height <=1 while total stones high ("deep empty well"), strongest for column 3.
H3: about the number of legal moves being small (few columns open) - activation reflects the restricted move set rather than col 3 itself.

## Round 1 findings
- Counts over 500 examples (biased to top bands): ZERO firing positions with column 1 not full. Column-1-full is (nearly) necessary.
- Score call 1 (p1.py; accidentally counted twice, calls 1-2 used): col1 full & 4..14 empty cells -> F1 0.377 (P 0.24, R 0.87), AUROC 0.90, sim share 0.42.
- Many col1-full endgames do NOT fire (e.g. pos 58189: only col 5 open, draw). Minimal pairs along game trajectories
  (141845, 58189): activation alternates with ply; high exactly when the engine says the side to move is LOST
  (all teacher scores negative), low when the side to move is winning/drawing.
- H5: fires when column 1 is full AND the player to move is losing the endgame. Need a board proxy: try a small exact
  endgame solver in the program (feasible when few empty cells).

## Score calls
- call 3 (p2.py): col1 full AND exact endgame solver (<=14 empty, node budget) says side to move is lost
  -> F1 0.597 (P 0.493, R 0.758), AUROC 0.867, sim share 0.51.
- Minimal pair (game of dev pos 16914): plies 31/33/35 are LOST for the mover with column 1 NOT full -> act -1.1..-1.4;
  ply 37 lost with column 1 just filled -> 17.2. Column-1-full really is a gate, not a proxy for game length.
- Along the 141845 and 58189 games activation alternates ply by ply in step with the sign of the teacher score
  (lost -> 6-12, won/drawn -> ~-1..3).
- FPs: genuinely lost col1-full positions with low activation (e.g. 17689 lost in 5, act -1.7). Misses: some won/drawn
  col1-full endgames fire (21481 draw, 40083 win). Weighted histograms over ~2400 band examples: within lost col1-full,
  no single clean separator (slightly more firing for loss-in-1, fewer legal moves, mover = second player).
- call 4 (p4.py): lost within <=7 plies -> F1 0.643 (P 0.566, R 0.743), sim 0.47.
- call 5 (p5.py): same, also solve 15-16 empty with small budget, level = 3 + #full columns for lost -> F1 0.649
  (P 0.558, R 0.776), AUROC 0.879, sim share 0.47. FINAL program.

## Steering
- 16914 ply 32 (legal 0,1,2, act -0.5) forced to max: column 1 prob 0.32 -> 0.00, mass goes to 0 and 2.
- 35298 (legal many): forced max lowers column 3 0.63 -> 0.31, spreads to others (flatter policy).
- 3,3,4,2 opening: max lowers column 3 0.69 -> 0.33, spreads to 2/4/6.
- Zeroing in firing positions (78352, 141845, 39145): change <= 0.05 (those are near-forced endgames).
=> effect: tells the model column 1 is unplayable and flattens/lowers its favourite (centre) move; little effect when removed.

## Synthesis
Hill-climb (swap two same-player moves, keep legal, no earlier win) from dev games 16914 / 164594: five positions at
23.00, 22.99, 21.70, 21.50, 20.01 (dev max 18.74), all of them: column 1 just filled, a single open column, mover lost.

## Final
p5.py, F1 0.649, sim share 0.47, confidence medium (graded unit, clear exceptions).
