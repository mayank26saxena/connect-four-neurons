# U37 notebook (layer 0, pole -)
## Observations
- Firing is concentrated in the early game (band 9: mostly ply 4-11). Last move col 0 or 3 dominate top bands.
- act: 1,3,3,x fires for every x. A stone of MINE in column 0 kills it (0,3,3,0 -0.85; 3,3,0,0 -0.84; 1,3,3,0,0 -1.07).
  Opponent stone in column 0 boosts (3,3,3,0 2.27 vs 3,3,3,3 1.04). Centre-column stones help; ply decreases it.
## Hypotheses
- H1: ply<=10, col 3 has >=2 stones, no stone of mine in col 0.
- H2: H1 plus opponent stone at (0,0) as booster for level.
- H3: generic "early game" (ply only).
## score 1 (H1): F1 0.329 P .23 R .57 AUROC .757 sim share .13 -> too crude.
## Further act findings
- Unit behaves like a bag-of-moves (layer 0): order of my moves irrelevant (1,3,5,0 == 5,3,1,0), roughly invariant to
  repeating the whole sequence (1,3,3,0 2.59; x2 2.34; x3 2.15) => depends on the SHARE of moves per (player, column).
- My stones: col0 very negative, col1 and col3 strongly positive, col2 mild, col4/6 ~0.
- Their stones: col3 strongly positive, col1 negative, others ~0; last move into col 0 gives an extra boost.
## H2: weighted share of stones by (owner,column) / ply.
## score 2 (p2, binary weighted share): F1 0.548 P .42 R .79 AUROC .878 sim .21
## score 3 (p3, opp col0 weight lowered, opp col1 negative): F1 0.487 AUROC .717 -> opp col0 must stay high (1,0,1,2 .9 vs 1,2,1,2 .41)
## score 4 (p4, continuous fires, thr .72): F1 0.525 P .63 R .45 AUROC .923 sim .19
## score 5 (p5, thr .66, me c2/c5 up): F1 0.541 AUROC .914
## score 6 (p6, thr .69): F1 0.561 P .53 R .60 AUROC .917 sim .18  <- final
## Exceptions / doubts
- Strong context interactions (layer-0 attention): e.g. 0,1,1,6,0,0,2,1,2,2,1,6,4,5,0 = -1.40 but adding opp move 2 -> +0.79,
  although I then own three col-0 stones. Linear share model plateaus at F1 ~0.55.
- Steer: forcing max or zero changes move probabilities by <= 2 points in 4 positions: no measurable effect.
- Synthesis: could not beat dev max 2.591 (3,3,1,0 equals it; 1,3,3,0 2.588).
