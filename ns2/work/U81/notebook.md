# U81 notebook (layer 2, pole +, thr 0.480, dev max 5.977)

## Observations (examples, bands 0-9, ~200 per band histograms)
- Top band: low-mid ply (8-20), left/right edge columns (0, 6) mostly empty above row 0.
- Bottom-row cell occupancy is the most different single feature: X(0,2) 84% in band 9 vs ~45% in band 0;
  O(0,3) ~60%, O(0,6) ~58%, X(0,4) ~58%, O(0,1) ~54%; O(0,2) only 5% (vs 32%).
- Also column 2 = X,X,O and column 3 = O,O,X,X, column 5 X then O,O frequent at the top.
- Strong move-ORDER dependence: 2,6,4,3,4,4,2,2 = 3.29 but 4,6,2,3,2,2,4,4 (same board) = 1.74.
- Fires in alternating plies within a game (one side persistently).
- Ply-2 grid: opponent at col 3 or col 6 drives it (up to 2.69 with X at 2, O at 3).
- steer zero/max: changes move probabilities by <= 0.04; effect essentially none.

## Hypotheses
H1: bottom-row pattern: my stone at (0,2) with their stones at (0,3) and/or (0,6), early/mid game.
H2: additive cell score (hand weights read off the band histograms), bottom row dominant.
H3: last move stacks on mover's own stone (45% top vs 28% bottom) - weak.

## Minimal pairs (ply 4)
2,3,4,6 1.73 | 2,3,0,6 0.84 | 2,3,5,6 0.25 (X at (0,5) kills) | 2,3,6,0 0.11 | 2,3,0,4 0.01 (O at 4 kills)
3,3,0,6 -0.05 (X not at 2, O at (1,3) not (0,3)) | 2,6,6,3 1.81

## Score calls
- s1 (p1: X(0,2) & O at (0,3) or (0,6), col6 h<=1, ply<=24): F1 0.170 (P 0.109, R 0.387), AUROC 0.645, sim share 0.04.
- s2 (p2: hand-weighted additive cell score, weights read off band-9 vs band-0 histograms): F1 0.227 (P 0.197 R 0.270), AUROC 0.618, sim 0.03. BEST.
- s3 (p3: motifs found by minimal pairs: col5 = X,X,O,O(,O); col4 = X,X,O,O; col1 = O,X,X,X,O; col6 = lone O; bottom-row bonuses): F1 0.186, AUROC 0.589, sim 0.01.

## Further minimal pairs
- Same board, different move order: 3.29 vs 1.74 -> strong sequence/order dependence (layer 2).
- Prefix sets a base level; last move modulates (e.g. prefix 1,1,3,4,3,1,4,3,1,4,1,2: every last move fires, 0.9-4.4).
- Column motifs are column-specific, not a general concept: their open vertical three on my pair:
  col5 3.90, col4 1.94, col0 1.23, col2 0.76, col1 0.47, col3 -0.07, col6 -0.10.
  My capped vertical three: col1 2.25 but col0/2/3/4/5 ~0.
- Last move landing at row 4 of col 1/5 (common in band 9) does not fire on its own.

## Steer
5 positions (acts 0.8-5.2), zero and max: all move-probability changes <= 0.04. No measurable effect.

## Synthesis
Best 5.16 (5,3,5,5,2,6,2,5,4,5 and 5,3,5,5,2,6,4,5,2,5), below dev max 5.98.

## Conclusion
Looks like a mixture / possibly random direction: weak, column-specific bottom-row and vertical-stack cues,
strong move-order dependence, no clean board concept. Confidence low.
