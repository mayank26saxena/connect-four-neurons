# U52 notebook (layer 4, pole -, threshold 1.664, rate 3%)

## Observations (examples, 600 sampled across bands, single-feature histograms)
- Strongest single correlate: opponent has a playable win (must-block): band0 7%, band4 18%, band5 20%, band7 48%, band9 73%.
  Number of their threat cells also rises with band. Column-4 cells slightly overrepresented (their threats in col 4, col 4 upper rows empty).
- Activation alternates strongly ply to ply within a game; last-move column matters little in some positions (minimal pairs on last move).
- steer to zero: essentially no change in move probabilities (<0.02) on 3 positions.

## Hypotheses
H1: opponent has an immediate threat I must block.  Minimal pairs: open bottom three 2-3-4 fires (1.9), gapped 2,3,_,5 does not (-2.5);
    vertical threes: only column 4 fires (2.2), other columns -0.8..0.4. So H1 is at best partial.
H2: it is a mixture / near-random direction with a weak "opponent threat" component.
H3: column-4 specific threat feature (threat cells in column 4).

## Score log
- p1 (fires = opponent has must-block; level by threats): F1 0.114 (P 0.068 R 0.343) AUROC 0.600, sim share 0.07.
- p2 (threat cells (0,1)&(0,5) for either side +4, threat cells in col 4 +2 each, must-block +1; fire >=3): F1 0.131 (P 0.083 R 0.310) AUROC 0.603, sim 0.07. BEST.
- Minimal pairs (early game): bottom three in cols 2,3,4 (or 2,_,4) of one colour with (0,1),(0,5) empty fires 2-5; filling (0,1) or (0,5) with
  the other colour drops it to ~0.5-1.5; same shape shifted to 1-3 or 3-5 does not fire. Owner matters little (fires for my three too).
  Many other tiny positions fire for no visible reason (2,5,0,2 = 2.18 but 0,5,0,2 = -0.24).
- p3 (only the bottom 2-3-4 shape + double must-block): F1 0.090 (P 0.25 R 0.055) -> the shape is a small slice of firing.
- p4 (late game: other columns full, col 4 low with threat cells; plus bottom shape): F1 0.114 AUROC 0.557.
- Conclusion: no clean rule; most mid/late firing is unexplained. Treat as near-random / polysemantic direction. Confidence low.

## Steer
- 5 positions (zeroing at 3.1-5.1, or forcing max): all column probabilities change by <= 0.02. Effect: none measurable.

## Synthesis
- 4,6,2,6,3,6,0 = 5.134 and 4,6,3,6,2,6,0 = 5.123 beat dev max 5.077 (bottom O O O O? no: X at 0,2,3,4 w/ (0,1),(0,5) empty; O three stacked in col 6).
