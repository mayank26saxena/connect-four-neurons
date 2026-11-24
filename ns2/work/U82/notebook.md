# U82 notebook (layer 4, pole +, threshold 1.383, dev max 4.504)

## Observations (examples, ~140 across bands)
- Firing positions mostly have a must-block, and the must-block cell is usually directly above the opponent's last stone
  (same column as last move). Losing positions (teacher ~ -980) common at top.
- Some firing with no threat at all, often early (ply 5-8), e.g. 2,3,3,1,3,0 (2.81) and 4,2,3,5,2 (2.27).
- Steering: zero/max changes move probs by <= 0.03 on 6 positions -> effect basically none.

## Hypotheses
- H1: cell directly above the opponent's last stone is an opponent win cell (their must-block on top of their own move).
- H2: any must-block exists (weaker; many must-block positions sit at 0.5-1.0).
- H3: losing position (engine scores) -- not available in Board API, skip.

## Tests
- score 1 (p1.py, H1 cell above opponent's last stone is their win): F1 0.171 (P 0.109, R 0.397), AUROC 0.647, sim share 0.02.
  FPs include plain vertical threes (e.g. col0 three at -0.54). Clean test: vertical three built in each column 0-6 -> all
  negative (-0.2 to -1.75). So threats per se are not the driver.
- Band histograms (150 ex/band): their_wins count and must-block rise with band (mb 12% band0 -> 84% band9); top band mostly
  engine-lost (-96x) positions, threshold band (5) mostly neutral (-10..+14) with no threat.
- score 2 (p2.py, non-vertical must-block): F1 0.139, AUROC 0.596. Worse.
- Open horizontal threes (double threat, lost) give -2.0 -> not "I am lost" either.
- score 3 (p3.py, unstoppable threat: 2 mbs / stacked wins): F1 0.097, AUROC 0.559.
- Minimal pairs on early firing 2,3,3,1,3,0 (2.81): needs O at (0,0),(0,1) + X at (0,2) and X at (1,3); shifting the pattern one
  column or removing any of these drops below 1.3; mirror image fires 1.79. Same board with other move order fires (2.57),
  so board-driven. 4,2,3,5,2 (2.27) fires only with the last O on top of X(0,2). Enclosed O 2x2 square between X columns fires
  (1.62) but the same square without flanking X is -1.38.
- score 4 (p4.py, dead O horizontal runs flanked by X/wall + H1): F1 0.080, AUROC 0.564.
- Conclusion: no single board concept; the top end loosely tracks "opponent has threats / I'm losing", the threshold band is a
  mix of specific local stone patterns. Looks like a mixture or random direction. Keep p1 (best F1 0.171). Confidence low.
- Steering: zero/max on 8 positions changes move probabilities by <= 0.03: no measurable effect.
- Synthesis: extensions of dev pos 56721 prefix (1,2,5,0,0,4,2,1,2,0,4,2,5,1,4,4,5) + two moves reach 4.7-5.3 (> dev max 4.504).
Stopped at 4 score calls: remaining ideas were not principled.
