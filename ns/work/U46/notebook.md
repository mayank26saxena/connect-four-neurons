# U46 notebook (layer 0, pole -, thr 0.337, dev max 2.54)

## Examples (40 + 12 band-9)
Firing positions almost always have a tall column 2 (4-6 stones), columns 0/1 nearly empty, and relatively few
other stones (col-2 share of all stones high). Single move [2] fires (0.441).

## Probes (act)
- 2,2,2,2 = 0.77; 2,2,2,2,2,2 = 1.81; 2,2,2,2,2,2,5 = 2.16; 4,2,2,2,2,2,2,5 = 2.63 (> dev max).
- dilution: 4x4 then 2x6 then 5 = 1.85; 6x4 then 2x6 then 5 = 1.30 -> share of moves in col 2 matters.
- cols 0/1 suppress: 2,0 alternating x4 = 0.06; 2,1 alternating = 0.16; 2,2,2,2,1,1,1,1 = 0.19, but 2,2,2,2,4,4,4,4 = 1.18.
- sequence-dependent (layer 0): 2,2,2,2,0,0,0,0 = 0.33 vs 0,0,0,0,2,2,2,2 = 0.02 (same board).
- consecutive 2,2 helps: 2,2,4,4 = 0.50 vs 2,4,2,4 = 0.12.

## Hypotheses
H1: column 2 holds a large share of the stones: (h2 - 0.5*(h0+h1)) / ply >= ~0.3 with h2 >= 3 (or ply==1 & col 2).
H2: plain h2 >= 4 and h2/ply >= 0.3.
H3: mixed-colour col-2 stack (consecutive 2s in the move list) matters.

## Score log
1. p1 col-2 share (h2-0.5(h0+h1))/ply>=0.3, h2>=3: F1 0.540 (P .55 R .53) AUROC .76, sim share 0.23.
2. p2 per-column weights on share: F1 0.537, AUROC .79, sim 0.22. Misses had col1/col5 stones -> colour matters.
   Probes: with fixed last token, ORDER does not matter (bag of stones). Colour relative to mover matters:
   adding a col-2 stone of either colour +0.5; opponent stones in cols 0 and 3 cost ~0.3 each, col 1 ~0.2,
   col 4/5/6 ~0.1; my stones elsewhere ~neutral (my col 4 slightly +, my col 5 slightly -). Last move col 5 boosts.
3. p3 "opponent stones in col 2 >= 3": F1 0.137 (no dilution -> fires all over late game). Dropped.
4. p4 absolute score (h2 - colour-weighted penalties) >= 2.8: F1 0.493, AUROC .834 (best ranking), over-fires.
5. p5 score/ply >= 0.37: F1 0.434 (P .81 R .30). Dilution by ply too strong.
6. p6 score/(ply+4) >= 0.3 + last-col-5 bonus: F1 0.367 (P .92 R .23).
7. p7 absolute score + col5 bonus - 0.04*ply >= 3.0: F1 0.551 (P .68 R .46), AUROC .73, sim 0.25.
8. p8 same, threshold 2.6: F1 0.597 (P .56 R .64), AUROC .81, sim 0.25. FINAL.

## Steering
Forcing to max (2,2,2,2,5; 4,2x6,5; 3,2,4,6,2,5; a band-9 game) or to zero (2,2,2,2; 2,3,2,3,2,3,4):
move probabilities change by <= 0.02. No measurable effect on the move (layer-0 unit).

## Synthesis
4,2,2,2,2,2,2,5 = 2.626 and 2,2,2,2,2,2,4,5 = 2.638 beat dev max 2.54 (full column 2, few other stones, last move col 5).

## Conclusion
Layer-0 "column 2 is stacked tall relative to the rest of the board" detector, with colour-dependent penalties
for opponent stones in cols 0/1/3. Graded, not crisp; F1 ~0.6 -> medium confidence.
