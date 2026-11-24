# U64 notebook (layer 1, pole -, thr 0.223, rate 3%)

## Observations (examples, bands 0-9, n=60 per band, seed 3; plain single-feature histograms)
- Top band (9): 56/60 odd ply (me = second player), ply 15-19 dominant; column 0 has exactly my one stone (or two mine) ~75%;
  column 1 often holds their stones at rows 0-2; last move often lands high (row 4-5) in cols 2-4.
- Threshold bands (5-7): flatter; ply 5-9 common; col0 height 1-2 enriched, col0 height 0 and >=3 depleted.
- Activation flips sign ply to ply; very sensitive to the last move (e.g. 26325: last=2 0.96, others ~0.25, last=0 0.04).
- First move "2" alone -> 1.03, "5" alone -> 0.94 (not scored, <4 stones).
- Steer (zero on 2 top positions, max on 1): no measurable change in move probs (<=0.01).

## Hypotheses
H1: me second player, col0 = my single stone (or two), plus central stack -> fires.
H2: opponent vertical three in col1 -> tested by act: does NOT fire alone (1,0,1,3,1,1 etc. <0.23).
H3: last move filled a column top (row 5) -> partial: 3,3,3,... / 0,4,4,... fills don't fire.
Minimal-pair: 3,0,3,3,... (col0 single P2 stone) fires at even ply (0.34) not odd -> H1 contradicted in early game.

## Score calls
- s1 p1 (me second player, col0 = my 1-2 stones, ply>=11): F1 0.121 (P 0.087 R 0.198) AUROC 0.566, sim share 0.01.
- Larger histograms (150/band): strongest single signal = column 0 holds only the SECOND player's stones (1-2 of them),
  in either parity; col0 height>=3 almost absent among firing; col2 empty and earlier ply enriched.
  Minimal pairs: 3,0,3,3 0.34 vs 3,6,3,3 0.14 / 0,3,3,3 0.11; 3,3,3,0 0.36. But 3,0,4,4,3,3,4 -0.16 (odd ply) -> context-dependent.
- s2 p2 (col0 = only second-player stones, h 1-2): F1 0.146 (P 0.088 R 0.418) AUROC 0.640, sim 0.00. BEST.
- s3 p3 (p2 + last move not col0 + first player at (0,1)): F1 0.117. worse.
- s4 p4 (p2 + last move not col0 + ply<=21): F1 0.145 (P 0.096 R 0.297). no gain.
- Activation oscillates ply-to-ply and swings hugely with the last move (159789: last=0 0.20, last=3 1.07); FPs like 65317
  (P2 just played col0) go strongly negative. No clean board rule found; looks like a distributed/possibly random direction.

## Steer: zero on 3 top positions, max on 2 others: all changes <= 0.01 -> no measurable effect.
## Synthesis (search over 2-move extensions of dev top 159789): 1.480, 1.394, 1.316 beat dev max 1.291.
## Conclusion: confidence low.
