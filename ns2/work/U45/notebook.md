# U45 notebook (layer 0, pole -, threshold 0.001, dev max 0.004)
Observations from ~400 examples across bands (histograms of single features):
- Top bands: ply even (me = first player) ~85% vs ~47% in band 0.
- Last move column: band 9 is col 4 (53%) or col 1 (32%), some col 2; rarely 0/3/5/6.
- Move share: cols 1 and 4 over-represented (~0.22 vs 0.12-0.16), cols 5,6 under (~0.06 vs 0.11-0.16).
- act trajectory: alternates strictly with parity: odd ply always negative, even ply positive when last col in {1,2,4,5}.
Hypotheses:
H1: even ply AND last move in col 1 or 4.
H2: weighted bag-of-moves: parity + last col (1,4 >2,5 > 0,3,6) + stones in cols 1,4 - stones in cols 5,6.
H3: something tactical (no sign of this; must-block/wins look irrelevant).

## Tests (act minimal pairs)
- Base 2,0,1,4,6,1,6,3,3,6,4,3,4 + last col: 1,2,4,5 fire (0.002), 0,3,6 do not; same base at odd ply: all negative.
- Second-to-last move barely matters.
- Per-player: 4,1,4,1,... (me col4, them col1) fires; 1,4,1,4,... (me col1, them col4) -0.004. Relative to mover, works at odd ply too.
- Conjunction: my col4 alone ~0.000; their col1 alone -0.004; both 0.001-0.003. With their col1 fixed, only my col 4 fires; with me in col 3, no their-column fires.
- Their col 5 stones strongly negative; their col 6, my 1/5/6 mildly negative. Weak extra parity bonus (me = first player).
- (Discarded probes that accidentally contained completed fours.)
## Scores
- p1 even ply & last col in {1,4}: F1 0.178, AUROC 0.69
- p2 linear on per-player column shares: F1 0.305, AUROC 0.72
- p3 min(my col4 share, their col1 share) + penalties: F1 0.318, AUROC 0.765
- p4 count-based conjunction: F1 0.236 (shares beat counts)
- p5 p3 + extra my-col4 term + their col4 penalty: F1 0.351 (P 0.26, R 0.53), AUROC 0.74 <- best
- Simulation: nan every time (unit's ablation damage appears to be ~0).
## Steer: no measurable change on 3 positions at max, zero or 10x max. Effect none.
## Synth: 4,1,4,1,4,1 openings + filler reach 0.004 = dev max, not beyond.
Conclusion: low confidence, tiny-magnitude layer-0 direction, bag-of-moves composition; could be a random direction.
