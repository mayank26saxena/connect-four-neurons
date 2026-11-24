# U79 notebook (layer 1, pole +, thr 0.549, dev max 1.365)

## Examples
- Band 9 (top 0.1%): ~70% are "opponent's last move in col 5 lands at row 2 making a pure 3-stack of their stones from the floor" (col5 'OOO'). Also col 6 OOO.
- Bands 5-7 (bulk of firing) are diverse: col5/col6 OO or OOO stacks, first stone in col 4, assorted.
- No relation to general new threats, parity, horizontal neighbours (single-feature histograms).

## Hypotheses
H1: last move completes a pure vertical stack (>=2, from the floor) of the opponent's stones, in column 5 (also 6, 0).
H2: unit is graded: activation rises with stack height (OOO > OO) and is highest in col 5.
H3: residual firing is a diffuse mixture tied to specific move tokens (layer 1).

## act tests
- Pure OOO stack in col 5: 0.52-0.88 depending on unrelated stones (fires most of the time); col 0 OOO 0.86, col 6 0.57, col 4 -0.6, col 3 0.2, col 2 0.05, col 1 0.23.
- xOOO (run not from floor) in col 5: 0.35 -> floor matters (or height of row).
- OO in col 5: 0.05-0.33 at ply 4; but OO appears in bands 7-9 in later games.
- Other stones modulate strongly (5,3,5,3,5 = 0.29 vs 5,4,5,4,5 = 0.84).

## Score calls
1. p1 (last move completes a pure floor stack of their stones: col 5 height 2-3, col 0/6 height 3): F1 0.223 (P 0.230, R 0.216), AUROC 0.597, sim share 0.00. FPs include late-game col-6 OOO stacks with act ~0.
2. p2 (opponent has a must-block in col 5): F1 0.160, AUROC 0.561, sim -0.01. General col-5 threats are not it.
3. p3 (pure floor stack of theirs in col 5, height 3 any last move, or height 2 just played): F1 0.199 (P 0.28, R 0.15), AUROC 0.571.
Stopped scoring: further rules would be fishing.

## Other tests
- Bands 5-7 (about 80% of firing) have no must-block mostly, no consistent last-move column, stack pattern, threat or height signature. act traces of missed games fluctuate move to move with no pattern.
- Persistence: once opponent has an open col-5 floor triple, unit stays high over the next moves unless I block (5,4,5,4,5,0,6 = 0.95; ...,6,1,2 = 1.08), but sensitive to unrelated stones (5,3,5,3,5 = 0.29 vs 5,4,5,4,5 = 0.84).
- steer (max and zero) on 5 positions: move probabilities change by <= 0.01. No measurable effect.

## Synthesis
4,0,2,3,3,1,6,3,5,3,5,3,3,0,5 = 1.390 and 4,0,6,3,3,1,2,3,5,3,5,3,3,0,5 = 1.372 beat dev max 1.365 (opponent col-5 floor triple + col-3 stack).

## Conclusion
Only the extreme tail is clean (col-5 open vertical three of the opponent from the floor). The bulk of firing is diffuse; no effect on move. Looks like a mixture or random direction. Confidence low.
