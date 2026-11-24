# U17 notebook (layer 5, pole +, threshold 0.657, dev max 11.458)

## Observations (examples, 40+ across bands, plus band 9 x50)
- Top bands are early game (ply 5-9), flat boards (max col height 2-3). Mid bands (5-6, 0.66-1.2) are mostly mid/late-game and look noisy.
- Many top boards: opponent stone at bottom of col 1 next to my stone at (0,2), or mirror O(0,5) with my X(0,4); opponent stones on row 1 over my stones near center.
- steer: max raises col 1 (and 5), lowers col 2 (and 4); zeroing in top positions moves ~0.2-0.3 prob from col1/col5 to col2.

## Hypotheses
- H1: all my stones on bottom row, opponent has a stone above it. Broken by many top examples (X on row 2).
- H2: d = (#O above row 0) - (#X above row 0) >= 1. Broken by minimal pairs (1,2,5,4,4,0,0 d=2 -> -0.06).
- H3: bottom-row config O(0,1)+X(0,2) (or O(0,5)+X(0,4)) on a flat early board.

## Minimal pairs (act)
- 5,2,1,4,x: fires for every x (2..11). Replacing O(0,1) by O(0,0) kills it (-0.5); by O(0,6) halves (1.3).
- 4,2,5,3,1 (.OXXOO.) 7.2; last O at 0 instead of 1 -> -0.3; at 6 -> 0.24. X(0,2)->X(0,0) 1.5. X(0,3)->X(0,6) 6.6 (irrelevant).
- 1,2,5,4,4 (11.0) + my stone stacked on any column (rows>=1) kills it (~0); + my stone on row 0 keeps it (1.2-6.7).
- 1,2,5,4,4,0,2 = 14.2 (beats dev max). Not mirror symmetric: 5,4,4,3,3 = 8.5 vs 1,2,2,3,3 = 0.13.
- Opponent immediate threat (2,0,4,1,5) -> -5.9; tall centre stack 3,3,3,3,1 -> -10.

## Score log
- p1 (row-1 opponent stones, my stones only on bottom, no must-block): F1 0.145 (P .135 R .157), AUROC .563, sim share -0.97. FPs include strong negatives with my immediate win (-21.8).
- p2 (weighted sum of O(0,1)/O(0,5)/row-1 O, minus my stacked stones): F1 0.165 (P .237 R .127), AUROC .557.
- Histograms: must-block presence flat across bands (so not a reason to exclude); my immediate win nearly absent at top. Mid bands (5-6, which are 2/3 of firing) show almost no bottom-row or column signal: diffuse.
- p3 (O(0,1)+bottom motif, xhi==0): F1 0.078, P .51, R .04.
- p4 (left motif O(0,1),X(0,2),(0,4) occupied; or right motif): F1 0.097, P .52, R .05.
- Bottom-row cell histogram by band: band 9 has O(0,5) 70%, X(0,4) 64%, X(0,2) 51%, O(0,1) 52%, (0,3) empty 52%, O(0,0) 5%. => ".OX.XO." motif.
- p5 (motif>=4 and <=1 of my stones above row 0): F1 0.091, P .33.
- p6 (ply 5-11, no my win, [no stacked stones of mine & motif>=2] or [one stacked & motif>=4]): F1 0.181 (P .257 R .139), AUROC .563, sim share -0.28. BEST.

## Steer
- zero at top positions: col 1 (or col 5) loses 0.2-0.25, col 2 gains ~0.3. max at quiet/non-firing positions: col 1 +0.12..+0.20, col 5 +0.03..+0.08, col 2 -0.10..-0.25, col 4 -0.09. Effect is small in forced positions.

## Synthesis
- 1,2,5,4,4,6,2 = 16.8; 5,4,1,2,4,6,2 = 16.8; 1,2,5,4,2,6,4 = 16.2; 5,4,1,2,2,6,4 = 16.1; 1,2,5,4,2,0,4 = 14.9 (dev max 11.46).
  Board: bottom .OX.XOX, row 1 ..O.O.. : my two stones on (0,2),(0,4) each capped by an opponent stone, flanked by opponent at (0,1),(0,5), centre column empty.

## Conclusion
The strongest firing is a specific early-opening shape; most firing (near threshold, mid/late game) is diffuse and not captured by any simple feature I found. Possibly a random direction or a polysemantic mix. Confidence low.
