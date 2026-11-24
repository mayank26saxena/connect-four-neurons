# U45 notebook (layer 2, pole -; threshold 0.710; dev max 6.455)

## Exploration
- 40 examples + 180 hi (bands 7-9) / 160 lo (bands 0-3), seed 3. Height histograms:
  firing positions are early/mid game (ply 6-20), column 2 empty in 79% (142/180) vs ~18% of low bands;
  column 1 also often empty (52%). Non-col-2 firing examples usually have some other empty column.
- Minimal pairs on 3,4,3,0,3,3,3,0 (3.41): last move 6 -> 0.97, 1 -> -0.02, 2 -> -0.32. A stone at the bottom of col 2 kills it.
- 0,6,6,0,0,0,4,5,4,x: x=1 3.8, x=0 2.2, x=2/3 1.3, x=4 -1.3 (opponent taking (2,4) atop my two-stack kills it).
- Steer: effect tiny (<=0.02 prob) on two positions.

## Hypotheses
H1: column 2 empty in the early/middle game.
H2: generic "empty columns remain" (early game), col 2 weighted most.
H3: a mixture / near-random direction.

## Score calls
- call 1/2 (p1, same program run twice by mistake): col2 empty & ply 6-20. F1 0.277 (P .18 R .61), AUROC .76, sim share .07.
- call 3 (p2): + col1 height<=1. F1 0.275 (P .23 R .35). Column-1 condition hurts recall; dropped.
- call 4 (p3): hand score w/ last-move terms, threshold too strict. F1 0.211.
- call 5 (p4): graded score: col2 empty(+3)/height 5(+2), ply window, ownership terms
  (mine at (0,3),(2,3),(1,4),(2,4); theirs at (1,3), col 0 bottom). F1 0.319 (P .35 R .30), AUROC .715, sim .09.
- call 6 (p5): p4 + roughness term (sum |h[c]-h[c+1]| above the ply-expected value). F1 0.340 (P .27 R .47), AUROC .808, sim .10. BEST.
- call 7 (p6): roughness weight .5, higher threshold. F1 0.325. Kept p5.

## More findings
- Strong perspective dependence: along a game the activation alternates sign ply to ply (e.g. 2.1,-0.5,2.1,0.1),
  so ownership of stones matters, not just shape. Mirror-image positions do NOT fire (asymmetric; column 2 specific).
- Firing positions are rougher than matched-ply references (tall columns next to empty ones): rough 10.6 vs 8.5 at ply 6-10.
- Top dev example (6.455): column 2 built 5 high with columns 1 and 3 empty. Column-2 height distribution at top band is 0 or 5.
- Opponent stone landing at (1,4)/(2,4) or bottom of cols 2-3 kills firing in minimal pairs; opponent stone on col 0 keeps it.
- Steer: effect tiny everywhere (<=0.08 prob; e.g. -0.08 col 2 / +0.06 col 3 in one position, -0.08 col 3 in another; most <0.02).
- Conclusion: distributed, partly perspective-dependent feature; col 2 empty is the best single cue. Confidence low.
- Synthesis: local search (single-move edits, 2-move extensions) did not beat dev max; best 6.455 (=dev max pos 31504), 6.352, 6.030.
