# U66 notebook (layer 5, pole +, threshold 1.348, dev max 5.221)

## Examples (80+ seen across bands)
- Top bands (8-9): most are "opponent just stacked a vertical THREE in column 5, cell above empty" (must-block in col 5).
- A few top: horizontal bottom-row threats with block at col 1/2 (e.g. O.OO.XX, OO.OO.X).
- Many firing (bands 5-8) have no must-block at all; boards are late-game, often with col 4 (or col 1) low/empty
  and teacher favouring cols 5/6.

## Hypotheses
H1: opponent has a vertical three in column 5 with empty cell above (their playable win in col 5).
H2: any must-block (their playable win), weighted toward col 5.
H3: something about columns 4/5 structure in late game (unclear) for the non-must-block mass.

## act minimal pairs
- 0,5,1,5,0,5 (O vertical 3 in col5): 2.54 FIRES. Same pattern in cols 0,1,2,3,4,6: -1.7..1.1, no fire. => column-5 specific.
- 0,5,1,5,0,4 (only two in col5): -1.15.
- vertical 3 col5, last move elsewhere (0,5,6,5,0,5,1,3): 1.64 fires (weaker).
- O three col5 at rows 2-4 (5,0,5,5,6,5,0,5): 2.04 fires.
- horizontal bottom threats: O.OO.XX 2.39 fires; OO.OO.X 3.95; but block-in-col5 horizontal (1,2,1,3,6,4) 0.90 no.
- steer zero on firing positions: no change (moves already forced). steer max on neutral: small (+0.07..0.12 to col 1).

## Score calls
1. p1 vert5 (their vertical three on top of col 5, cell above empty): F1 0.302 (P 0.70, R 0.19), AUROC 0.595, sim share -0.02.
2. p2 vert5 OR (cols 2,3 full, <=1 other full col): F1 0.277 (P 0.20, R 0.48), AUROC 0.707.
3. p3 any single must-block in col 5: F1 0.254 (P 0.31, R 0.21). Broadening beyond vertical hurts precision.
4. p4 vert5 OR (cols 2,3,4 full-or-poisoned, col 5 open, no immediate wins): F1 0.272 (P 0.20, R 0.42).
5. p5 vert5 OR (ply<=30, cols 2,3 full, col 4 full or poisoned, col 5 open & safe, no immediate wins): F1 0.319 (P 0.35, R 0.30). BEST.

## More act findings
- Vertical three in col 5 fires from both sides (player to move must block col 5). Same in col 4 drives it strongly NEGATIVE (-3.9/-4.6).
- Horizontal must-block landing in col 5 (single): 0.9-1.8; in col 1: 0.8-1.2 (sub-threshold); double threats (lost): -5 to -7.
- Own immediate win in col 5: does not fire (-1.7).
- On a firing late-game board (13705 ply 22, 3.25), changing the last opponent move so the only good move becomes col 0 or col 4 drops it to -2.4 / -1.2; when best moves stay at col 5/6/1 it stays 1.7-2.2.
  => unit looks like it tracks "the move goes to column 5 (right side), not center/col 4/col 0" — the model's move choice, which a board program can only approximate.
- Histograms by band: firing positions often have cols 2 and 3 full mid-game (ply 22-31) with outer columns open; band 0 has both full only near end of game.

## Steer
- zero on 6 firing positions: change <= 0.02. max on 7 neutral positions: up to +0.12 col 1, +0.07 col 5/4, -0.05..-0.11 cols 2/3. Weak effect.

## Synthesis
Best 4.96 (3,4,0,4,6,5,4,3,5,1,5,4,3,3,5), below dev max 5.22.

## Conclusion
Clean core: opponent's vertical three in column 5 to block (precision 0.7) but only ~20% of firing. The rest is diffuse late-game positions where the centre (cols 2-4) is closed and play goes to col 5/6/1. Looks like a mixture / move-choice-related unit. Confidence low (best F1 0.32).
