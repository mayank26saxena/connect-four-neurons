# U13 notebook (layer 0, pole +, threshold 0.009, dev max 0.038)

## Observations
- Band 9 (top 0.1%) is almost entirely ply == 6 (6 stones, me = first player, last move by opponent).
- Bands 5-8: ~55% ply 6; rest mostly late game even ply (28, 30, 32, some 36) with last move in column 0 (also 2, 5).
- Layer 0 => probably positional-embedding driven (specific token positions) modulated by the column tokens.
- act: 4,5,0,5,0,4 -> 0.037 (near max); all single substitutions of earlier moves keep it >0.023.
  But 3,3,3,3,3,x ~0.003; 0,1,0,1,5,5 0.001; 0,6,0,6,0,6 0.008. Same board shape (0,1,0,1,5,5 vs 4,5,0,5,0,4) gives very
  different activation -> depends on which columns, not geometry. Roughly additive per-move contributions.
- Late game test game: ply 30 last 0 -> 0.011, ply 32 last 0 -> 0.011, last 2 -> 0.010, last 5 0.007, last 6 0.001; odd plies ~0.

## Hypotheses
H1: fires at ply 6 (any content) -- positional.
H2: H1 plus late-game even ply 28-32 when the opponent just played column 0.
H3: within ply 6, content score: stacking (many moves in one column, esp. col 3) lowers it; last col 5/0 lowers it.

## Tests (act minimal pairs)
- Ply-6 substitutions (bases 4,5,0,5,0,4 / 0,1,0,1,5,5 / 5,4,3,3,5,1): roughly additive per move slot.
  My stones (slots 0,2,4): cols 0,4,2 raise it; 3,5 lower it. Opponent slots 1,3: cols 2,5 raise; 0,1,6 lower.
  Last move: 4,6 best, then 1,3, then 0,2,5. A hand-built additive score predicted 8 random ply-6 sequences well.
- Late regime: the synthetic game (cols 3,1,6 filled, then 5,5,5,5,4,4,2,2,0,0,0,0) gives 0.017 at ply 30; the same with
  cols 2,4,5 filled gives 0.000. Last col 0/2 good, 5 mid, 4/6 bad. Tall 1/3/6 good, tall 2/4 bad. But the per-token
  effects are small and dense (+-0.002 each); a heights-only score had real FPs (0,1,3,5,3,1,... scored high, act 0).

## Dev metric
- s1 p1 (ply6 any + ply28/30/32 & last col 0): F1 0.471 P .375 R .634 AUROC .801
- s2 p2 (ply6 additive score>=10 + ply28/30/32 & last 0/2): F1 0.484 P .422 R .567
- s3 p3 (heights score for every ply>=12): F1 0.310 P .193 R .785 AUROC .842 -> threshold far too loose
- s4 p4 (ply>=20, last 0/2, fill>=14): F1 0.377
- s5 p5 (ply6 score>=9 + ply28/30/32 & last 0 & fill>=8): F1 0.592 P .605 R .580 AUROC .784  <- best
- s6 p6 (p5 with plies widened to 26-34 incl. odd): F1 0.528 -> reverted
- Simulation reported nan on every call; steering at max/zero changes move probabilities by <0.01 (no measurable effect).

## Synthesis
4,2,0,5,4,4 -> 0.040 (dev max 0.038); 4,2,4,5,0,4 / 4,2,0,5,4,6 / 4,2,4,5,0,6 -> 0.039; 4,5,0,5,2,4 -> 0.038.

## Conclusion
A layer-0 mixture: a strong positional spike at exactly 6 stones (modulated by which columns were played) plus a weak,
diffuse late-middlegame component (opponent just played col 0 at ply 28-32, board with tall 1/3/6). Confidence medium.
