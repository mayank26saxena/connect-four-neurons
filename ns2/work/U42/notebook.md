# U42 notebook (layer 0, pole -, threshold 0.702, dev max 1.551)

## Observations (examples, ~2100 sampled positions across bands)
- Band 9 is dominated by late games where the opponent's last stone went into column 0 and landed on a high row (often filling col 0, row 5).
- A second mode: very early positions (ply 4-5), e.g. 2,5,4,1,3 (1.25), 4,2,6,4 (1.16).
- Last column histogram by band: col 0 and col 4 over-represented in high bands, col 2 and col 5 under-represented.
- Odd ply (I am second player) somewhat over-represented in band 9 (72%).
- act: on 40167 board, changing the final move to cols 1,3,4 still fires (~0.8) but col 0 gives 1.33: board context + last move both matter.

## Hypotheses
H1: last stone in column 0 on a high row (>=3).
H2: weighted sum of last-cell (col,row) term + context (e.g. column 2 sparse, ply).
H3: early-game horizontal pattern (opponent stones central, mine on flanks).

## score 1 (p1: last col 0, row>=3): F1 0.209, P 0.15, R 0.33, AUROC 0.64, sim 0.04. Far too broad and misses early mode.

## Key finding from ply histogram + act
- Firing is strongly ply-and-parity dependent: early EVEN plies (4-14, I am first player) and late ODD plies (23-35, I am second player) fire; early odd (except 5) and late even almost never.
- Stacking-columns artificial game: never fires, so the base is not just ply.
- At ply 4 almost any position fires (4,2,6,x: 22/28 variants), last move into an edge column (0 or 6) lowers it there.
- Late odd plies: last stone in col 0 on row>=4 is strongest (~0.9-1.0 mean), col 6 row 4-5 next.
- Changing last move between cols 1 and 6 in one artificial context changed nothing; col 0 is the special token.
H4: activation ~ ply/parity base + last-cell bonus. Hard threshold sits mid-distribution so precision will be limited.

## score 2 (p2: ply/parity base + last-cell rules, level>=5): F1 0.187, P 0.11, R 0.73, AUROC 0.77, sim 0.20.
Recall good, precision terrible (program fires 20.7% vs 3%). Example bands over-sample firing, so my per-class rates were inflated.

## More act tests
- Order invariance: 3,6,3,5,6,5 and 3,5,3,6,6,5 give identical -0.803. The unit depends on the board (bag of stones per player per column) plus the last move, not move order.
- Ply 8 single-stone swaps: each earlier stone shifts activation by ~0.1-0.4; last move into col 0 early = -0.17 (vs 0.7 for col 1), col 2 = 0.24.
- Late (ply 31) single-stone swaps: moving a stone out of the last move's column (col 1) raises activation ~0.2 => last-stone ROW matters, col-dependent: col 0 wants high rows, col 1 low rows.
- Interpretation: a layer-0 token x position mixture: (ply, parity) base + (last col, last row) term + small distributed board terms. No clean tactical concept.

## score 3 (p3: hand points model, fire >=0.8): F1 0.300, P 0.41, R 0.24, sim 0.20. Early-mode threshold too strict (6,2,4,4 =1.15 missed); late FPs are ply-33 last-col-0-row-5 positions at 0.37-0.62.
## Late single-stone swaps (ply 31, last col 0, base 1.288): moving a col-3 stone elsewhere +0.2..0.27; moving a col-0 stone elsewhere -0.13..-0.18; others ~0. => late: column-0 stones up, column-3 stones down.
## Early swaps (ply 4/8): opponent stones in col 0 (-0.3..-0.6) and col 6 bad, opponent last move in col 0 very bad (-0.8), col 2 bad; my col 6 stones good.
Found 1,4,5,3,6,5,... (S3->4 variant) at 1.554 > dev max.

## score 4 (p4: added early per-stone terms, looser threshold, ply 5 on): F1 0.250, P 0.17, R 0.49. Worse; early mode over-fired (ply 5 and stacked early boards).
## Early act sweeps (ply 6 and 10): last move col 0 ~ -0.2, col 2 ~0.0-0.4, cols 1/4/5/6 ~0.6-1.0. Opponent stone in col 0 -0.3..-0.5. My stones in col 3/6 best, col 0/4/5 worst. Non-additive: opponent stones clustered right (3,6,3,5,6,5) -> -0.8; stacked boards (2,2,2,4) low. Early regime hovers around threshold; fragile.
Verified near order invariance with other last-two moves: 3,6,3,5,6,5 / 6,6,3,5,3,5 / 3,5,6,6,3,5 all -0.81; 4 reorderings of a ply-8 game all 0.70-0.71.

## score 5 (p5: late odd 23-37 points rule >=0.8 OR early even<=10 with last col in {1,3,4} row<2, no opp stones in cols 0/5/6, none of mine in col 0): F1 0.382, P 0.37, R 0.40, AUROC 0.69, sim 0.16. Best so far.
FPs: several ply-37 late positions; misses: late EVEN plies with last col 0 high (0.75-0.78, near threshold).
p6: same, late window capped at ply 35.

## score 6 (p6: p5 with late window capped at ply 35): F1 0.385, P 0.39, R 0.38, AUROC 0.68, sim 0.16. Best F1.
## steer (4 positions: 40167 ply35, 4,2,6,4, 2,5,4,1,3, 3,3,2,4,4,2,5,1): max and zero both change move probabilities by <0.01. No measurable effect.
## synthesis: hill-climb with act over legal, unfinished sequences (no four), mostly late ply-31 boards ending with a col-0 fill; reached 1.727 (dev max 1.551).

## score 7 (p7: p6 fires + graded level for early/late): F1 0.385, sim 0.22. Final program. 1 score call left unused.
Conclusion: low confidence; ply-parity x last-cell mixture, no move effect.
