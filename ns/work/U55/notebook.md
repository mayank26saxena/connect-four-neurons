# U55 notebook (layer 1, pole -)

## Exploration
- 40+ examples across bands; top bands: column 2 is either EMPTY or FULL (h=5/6); col 0 height 0-1; col 4 often 0/1 or 6; cols 5,6 heights ~3,2.
- Row-0 pattern often ".O.XXOX": them at c1r0, c5r0; me at c3r0, c6r0.
- Board-based (transpositions give same activation ~1.3-1.5).
- Minimal pairs on base 1,6,1,5,6,3,4,5,3 (1.31): adding THEIR stone to col 2 kills (~-0.1), my stone in col 2 reduces (0.1-1.1);
  their stone in col 0 reduces to ~0.5. Filling col 2 completely -> 2.35 (near dev max 2.53). col2 height 1-3 -> ~0, 4 -> 0.4, 5 -> 0.6-0.85.
- Isolated col2 full on empty board: 0.54. Cols 0,2,4 empty but no stones on right (1,3,1,3,3,1) -> no fire; right-side structure matters
  (1,6,1,5,6 fires; swapping colors in col 6 kills).
- steer: max/zero changes move probs by <=0.02 on 5 positions -> no measurable effect.

## Hypotheses
H1: col2 empty-or-full (dead column) + col0 near empty + col4 empty/full + mid-game ply.
H2: weighted cell template: row0 them at c1,c5 / me at c3,c6, plus H1's column-2 term.
H3: more general "even columns 0/2/4 unplayed while odd/right columns filled".

## Score calls
1. p1 (ply>=7, h2 in {0,5,6}, h0<=1, h4 in {0,1,6}): F1 0.146 (P 0.107 R 0.227), AUROC 0.583, sim share 0.02. Col-2 rule alone far too broad.
2. p2 (c6 me-under-them + col2 term - their stones in c0/c4): F1 0.087, sim 0.02. Minimal-pair features did not generalise.
3. p3 (6 binary features, >=5): F1 0.127, AUROC 0.548 (binary fires -> AUROC uninformative). sim 0.05.
   -> Switched to histogram contrast (firing bands 7-9 vs bands 0-3, restricted to ply 8-23): firing has col2 empty/full 78% vs 21%;
      col5 height 2-4 (h3 35% vs 12%), col5 rarely empty; col6 height 2-3, top theirs 58% vs 37%; c6r0 mine 64% vs 37%; col0, col4 empty more often.
      90% of firing is ply 8-23.
4. p4 (additive points, graded fires): F1 0.203 (P .289 R .156), AUROC 0.660, sim 0.06.
5. p5 (hand-set per-column height weights): F1 0.144 (P .446 R .086) threshold too high.
6. p6 (+ c6 bottom-mine term, lower threshold): F1 0.237 (P .367 R .175), AUROC .646, sim .07.
7. p7 (col6 top theirs/mine +-0.6): F1 0.255 (P .391 R .190), AUROC .611, sim 0.08.  FINAL.

## Steering
5+ positions, --to max and --to zero: every column changes by <= 0.02. No measurable effect on the move.

## Synthesis
1,6,1,5,6 + column 2 filled (2,2,2,2,2,2) -> 2.816 (dev max 2.534). Variants 2.61-2.78. Column-2-full is the strongest single lever.

## Conclusion
Distributed layer-1 direction: additive mix of column-height states. Top is clean (col 2 empty/full, cols 5/6 part-filled with their stone on top, col6 my stone at bottom, midgame), threshold region diffuse. Best F1 0.255 -> low confidence.
