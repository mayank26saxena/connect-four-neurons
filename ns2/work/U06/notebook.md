# U06 notebook (layer 0, pole +, threshold 0.002, dev max 0.009)

## Examples (bands 0-9, ~100 seen + histograms of single features)
- Firing: last move mostly col 1/2/3 (84%), rarely 0/4/5/6.
- Firing boards: opponent (last mover) has many stones in col 2, I have many in col 5 (and 6); col 4 and col 0 sparse.
- Last=1 firing positions tend to be short games (mean ply 13.7 vs 18.6).

## Hypotheses
H1: last move col 3 (or 2), opponent stacked col 2, me in col 5/6.
H2: last move col 1 (or 0), me in col 0, opponent in col 3/4 (found via 5-stone grids).
H3: unit is an additive layer-0 mixture (token-by-player-by-column weights that depend on last move column) -> no crisp concept.

## act tests
- 13-ply top example 5,3,2,3,2,5,2,2,1,1,1,6,3 (0.009): any last move fires there (3 best 0.009, 2 0.006, others 0.003-0.005); one more pair of moves kills it. Single-stone substitutions shift by only ~0.001-0.003: opp stone in col3 -, my stone in col5/6 +.
- Synthetic 2,5,2,5,3 fires 0.003; 2,5,2,5,2,5,3 0.005; 2,5,2,5,2,6,1,6,1,6,3 0.009. Replace them-2 by 1/6/0 or me-5 by 0/6 -> no fire. Last=2 or 1 instead of 3 -> no fire. H1 supported.
- 5-stone grids t,m,t,m,L: L=1: me col0 + them col3 -> 0.008; me col5 kills. L=0: me col0+them col3 0.004. L=3: only them col2 + me col5 (0.003). L=2: nothing fires at 5 stones.
- So the direction mixes at least two different "last move + context" patterns (H2 and H1).

## Score calls
- s1 (p1: hand-weighted per-column stone counts by owner + last-move bonus, plus a short-game mode): F1 0.284, P 0.20, R 0.48, AUROC 0.71. Simulation share nan (the "perfect reader" itself recovers -72%, so the unit has almost no causal effect; simulation is uninformative).
- s2 (p2: retuned weights + 0.2/ply bonus): F1 0.265, AUROC 0.79 (ply bonus over-fires in long games).
- Long-game probes (single-stone substitutions at every index of 25-26 ply firing games): each stone moves the activation only ~0.0005-0.001; the last move's column moves it ~0.003. Along one game, the unit flips on/off with the side to move, matching which player owns cols 2/3/5/6.
- s3 (p3: weights me=[-1,-.3,0,.4,-.5,1,.7], them=[.5,-.3,.7,-1.2,-.5,-.2,-.2], last bonus 3:3 2:1.5 1:2, 0.1/ply, threshold 6.3): F1 0.346, P 0.26, R 0.52, AUROC 0.74.
- Probe-averaged per-stone weights (6 bases, ~50 substitutions per cell, units 0.001): them [+.26,+.09,+.38,-.43,-.22,+.18,-.18], me [-.56,-.05,+.02,+.19,-.30,+.48,+.28], last move [-1.08,-.13,+.99,+1.32,-.28,-.21,-.68]. These come from act minimal pairs, not from dev labels.
- s4 (p4: those weights, threshold 2.8, old short-game mode for <=7 stones): F1 0.427, P 0.37, R 0.51, AUROC 0.74.
- One base (31 ply, last move col 5, act 0.003) showed REVERSED weights (me col0 +, me col5 -, them col3 +), the same as the short-game 5-stone grids. So there is a second mode: activation rises when the context score is very negative and the last move is not col 2/3.
- s5 (p5: second mode applied at all lengths, -ctx + LA >= 2.2): F1 0.284; it over-fires in long games (scores 2.5-3.5 with act ~0). The reversed mode works only in short games.
- s6 (p6: main mode threshold 2.6; reversed mode only for <= 12 stones): F1 0.432, P 0.36, R 0.54, AUROC 0.76. Best. Stopping here (2 calls left unused); remaining errors look like diffuse additive noise rather than a missing concept.

## Steering
5 positions (activations 0.001-0.009), forced to max (0.009) and to zero: move probabilities unchanged to 2 decimals in every case. No measurable effect.

## Synthesis
2,5,2,5,2,6,1,6,1,3,1,5,3 -> 0.011; 2,5,2,5,2,6,1,3,1,6,3, 2,5,2,5,2,6,1,6,1,3,3, 2,5,2,5,2,6,1,3,1,6,1,3,3, 2,5,2,5,2,3,1,6,1,6,3 -> 0.010 (dev max 0.009). Recipe: opponent stacks col 2 (plus col 1), I hold cols 5/6 (and some col 3), opponent's last move is col 3.

## Conclusion
Layer-0 direction with tiny activations (max 0.009), additive over stones: column of the last move plus who owns stones in which columns, plus a reversed short-game mode. Looks like a mixture; no causal effect. Confidence low.
