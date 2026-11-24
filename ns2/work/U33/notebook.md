# U33 notebook (layer 0, pole +, thr 0.559, rate 3%)

## Observations
- Top band (>1.1) almost all ply 4 openings: me (first player) on bottom row cols 1 and 3 (or 1,5), them at 0/4, last move col 4/0/3.
- Probes at ply 4 (base 1,0,3,4 = 1.541): my stones best in cols 1,3,5; worst 4,6 (-1.0). Their stone at 0 best. Last move: 4 best, 3/0 good, 5,6,2 bad.
- Late game (ply>=10) firing: last move fills a column (last_row 5): 50% of band 7-8 vs 11% band 0. Last col 6/3/0 frequent.
- Strongly context-dependent (layer-0 attention mixing); synthetic column fills at 3 and 0 did not fire.

## Hypotheses
H1: early opening (ply<=6) with my stones in odd columns 1/3/5 and last move col 0/3/4.
H2: late game, opponent's last move fills a column (lands on top row), esp. cols 0/3/6.
H3: unit is a messy additive token-mix (possibly random direction) -> low confidence.

## Tests
- Activation is exactly invariant to move order and to stacking order within a column: a function of (my stones per column, their stones per column, last-move column). This is a layer-0 bag-of-stones readout.
- Early: my stones in cols 1/3 strongly positive; my stones in 4/6 strongly negative; last move 4 best, 5 worst. Not translation or mirror invariant.
- Column weights flip with context (ply 10: my col 5 worst, col 4 mild; ply 33: my col 0/2 best). Strongly nonlinear, so an additive model fails.
- Late: an opponent move filling column 3 (top row) often lifts it to 0.6-0.8, but not reliably (one example scored -0.16).

## Dev metric
- p1 (early rule + last move on top row in col 0/3/6): F1 0.215, P 0.146, R 0.401, AUROC 0.665, sim 0.08
- p2 (hand-weighted early score + late top/col3): F1 0.197 (first attempt crashed on last_col None, not counted)
- p3 (additive fractions from probes): F1 0.143, AUROC 0.60 -> additive model is wrong
- p4 (early: ply<=6, my stones mostly in cols 1/3, last not 5/6; late: column 3 just filled): F1 0.256, P 0.20, R 0.34, sim 0.07
- p5/p6 (score-based, ply<=10 + late col 3/6 top): F1 0.223
- p7 (p4 with early part extended to ply<=8 when all my stones are in 1/3): F1 0.257, P 0.202, R 0.354, AUROC 0.656, sim 0.07 (BEST)

## Steer
- 4 positions, set to max: changes of 0.01 or less (largest -0.03). Set to zero: no change. No measurable effect.

## Synthesis
- 1,0,3,4 = 1.541 (ties the dev max). Variants 3,0,1,4 at 1.539, 1,0,1,4 at 1.375, 1,0,3,3,1,4 at 1.355, 1,0,3,0,1,4 at 1.265.

## Conclusion
Mixture or near-random direction: a crisp opening component plus a diffuse late-game component. Low confidence.
