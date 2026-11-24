# U21 notebook (layer 3, pole +, thr 0.595, dev max 8.52)

## Observations from examples (bands 0-9, ~70 positions)
- Empty board = 0.582 (just under threshold).
- Top examples: I (mover) have a horizontal three-with-gap on row 2 (third row from bottom), e.g. XX.XX / X.XX / XXX.,
  gap column on the left half (cols 1-3) with height 0-1 (threat not yet playable). Opponent stones on row 3 directly
  above (often OO.OO, their own threat at (3,c)) amplify it to 5-8.

## Hypotheses
H1: my (not yet playable) win cell on row 2 in columns 1-3; stronger with opponent stones on row 3 next to the gap.
H2: any stacked threat pair (mine at (2,c), theirs at (3,c)).  H3: opponent's last move created a threat (rejected: 137682 last move unrelated).

## Minimal pairs (act)
- base B=0,1,1,0,3,3,0,0,1,1,3,3 (my XX.X row2, their OO.O row3, gap col 2 empty): 2.32
- remove O row3 -> 0.45; only OO at (3,0),(3,1) -> 1.99; O at (3,0),(3,3) -> 2.91 (their threat not needed)
- remove my X at (2,3) (no my threat) -> 0.20: my row-2 threat is the core
- colors swapped (my threat on row 3, theirs on row 2) -> 0.27: asymmetric
- shift up one row (my threat row 3) -> -0.26; down (my threat row 1) -> 0.40: ROW 2 specific
- gap col: 1 -> 1.93, 2 -> 2.32, 3 -> 0.91 / -0.27, 4 -> -0.27 / -3.0, 5 -> 0.16, 0 -> -1.3: LEFT/center-left specific
- mover parity (me first vs second) doesn't matter (2.69 vs 2.32); gap col height 0 or 1 both fire.

## Dev metric log
- call 1+2 (p1, same file scored twice by mistake): any my_wins cell on row 2 in cols 1-3, column height<2. F1 0.128 (P 0.084, R 0.271), sim share 0.05.
- call 3 (p2): horizontal-only row-2 three-with-gap in cols 1-3. F1 0.200 (P 0.167, R 0.250), sim 0.06.
- call 4 (p3): any col 0-3 with my stone on row 2 capped by their stone on row 3. F1 0.089 (P 0.047, R 0.678): pattern present in most firing but far too common.
- call 5 (p4): p3 + adjacent low column. F1 0.125 (P 0.072, R 0.503).
- call 6 (p5): p2 AND a cap in cols 0-4. F1 0.204 (P 0.173, R 0.249).
- call 7 (p6): p5 with gap restricted to cols 1-2, caps cols 0-3. F1 0.208 (P 0.222, R 0.196), AUROC 0.59, sim share 0.07. BEST.

## Further minimal pairs
- 163745-like board 0,3,6,1,3,3,2,0,3 = 3.57 with NO row-2 threat: needs my X at (1,0) (removing it -> 0.34) and X at (0,1) (-> 1.13);
  an O dropped on (2,0) -> -1.12; any O in column 4 (bottom rows) suppresses strongly (3.57 -> 0.34; B 2.3 -> 0.07-0.6).
- Single col-3 stack XOXO alone: 0.32. Early openings: idiosyncratic (0,6,1 = 1.33; most 3-move openings < 0.4). Empty board 0.58.
- Activation behaves like a sum of many cell-level contributions (left-side row 1-3 cells, column 4 negative), not a clean concept.

## Steer
- 4 positions (B 2.3, 0,3,6,1,3,3,2,0,3 at 3.6, 52233 at 8.1, 137682 at 7.7): forcing to max or zero changes move probs by <= 5 points
  (largest: +5 col 3 / -5 col 2). Effect essentially none measurable.

## Synthesis
- 5,3,0,3,0,2,0,0,1,2,2,2,3,3,5,5,2,3,2,3 = 8.616 (beats dev max 8.522). Greedy additions from dev example 137682.

## Conclusion
Top activations (>3) are consistently "my horizontal three-with-gap on row 2, gap in col 1-2 still low, opponent stones capping
my row-2 stones on row 3", but this covers only ~20-25% of firing; the rest (mostly weak, 0.6-1.2) is diffuse. Looks like a
mixture / possibly random direction. Confidence low.
