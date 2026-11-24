# U53 notebook (layer 5, pole +, threshold 0.786, dev max 17.63)

## Examples (40 + band 5/6/7 samples)
- Bands 8-9 (act 6-17): every one has a must-block at (3,6): opponent has three stacked vertically in column 6 with the cell above empty.
- Band 7 (3-6): mostly must-block at (3..5,6), again vertical O-three in col 6.
- Bands 5-6 (0.8-2.8): mixed; many have last move in column 6, often O,O on top of col 6; some no obvious pattern.

Hypotheses:
- H1: opponent vertical three in column 6 with empty cell above (vertical must-block in col 6).
- H2: any must-block in column 6 (incl. horizontal/diagonal).
- H3: last move in col 6 / opponent stones on top of col 6 (weak band).

## act minimal pairs
- 6,5,6,1,6 (O three in col 6) 12.3 FIRES; same in col 0: 0.08; col 5: 0.01. -> column-6 specific.
- my own vertical three in col 6: -6.9 / -8.1 (strongly negative pole). 
- horizontal O-three with threat cell (0,6): 0.06 / -0.06 -> H2 rejected (horizontal threat at col 6 does not fire).
- O two-stack in col 6 (rows 0-1, rows 1-2, rows 2-3): -0.08..0.5 -> not firing; needs three.
- O three at rows 3-5 with column full (no threat): 0.16 -> requires open cell above.
- O three rows 1-3 over X: 6.6; rows 2-4: 4.6; rows 0-2: 10-12. Higher stack lower in column -> stronger.

## Score calls
- s1 (p1: opponent vertical three in col 6 with open cell above; level by height): F1 0.446 (P 0.895, R 0.297), AUROC 0.648, sim share 0.04.
  Misses: many weak firings (0.8-2.5), often opponent just played col 6 / O on top of col 6, but not reliably.
- Further act: two O on top of col 6 fires in some positions (2.2-2.7, e.g. 3,6,6,3,5,5,1,1,6) but not in others (6,6,1,6; 3,3,3,4,6,6,4,6).
  Inconsistent, confounded with other must-blocks / my own threats.
- s2 (p2: + "opponent just stacked two in col 6, no other tactics"): F1 0.376 (P 0.364, R 0.388). Secondary clause far too broad; dropped.
- Misses in s2 include a diagonal must-block at (3,6) firing 1.46 -> try any must-block in col 6 above row 0
  (horizontal row-0 threat at (0,6) does NOT fire in act tests).
- s3 (p3: vertical three in col 6 OR any must-block in col 6 at row >= 1): F1 0.501 (P 0.690, R 0.393), AUROC 0.694, sim 0.04.
- s4 (p4: same fires, level adds 1-2 when last move is col 6 / two O stacked): F1 0.501, sim 0.05. Not worth more calls:
  the remaining ~60% of firing is a diffuse weak band (0.8-2.5) without a pattern I can find with act; activations
  fluctuate move to move in those games.

## Steer
- 3,3,3,4,6,6,4,6 (act -0.2) -> max: col 6 +0.21 (0.77->0.97), cols 3/4 down.
- 3,6,6,3,5,5,1,1,2 -> max: col 6 +0.02. 3,3,4,2,4 -> max: col3 +0.13, col4 -0.13, col 6 +0.01 (no clear effect).
- 6,5,6,1,6 zero: no change (already 1.00 on col 6). 108382 / 116427 zero: col 6 -0.02.
- Effect: pushes toward playing column 6 (blocking the column-6 stack), small when the model already blocks.

## Synthesis
- Plain 6,x,6,y,6 openings: 9-12.7. Double threats through (3,6) reduce it (6-8).
- Hill-climb from the top dev game (14.86): 2,5,6,0,6,2,2,0,1,0,0,4,5,2,4,1,4,1,2,2,6 -> 17.40 (just under dev max 17.63).
- Round 2 hill-climb: 2,5,6,0,6,2,2,0,1,0,0,4,5,2,4,4,4,1,2,2,6 -> 17.648, BEATS dev max (synth). Others 17.40, 14.96, 12.67 below.
## Final: p4 program. Best F1 0.501 (s3/s4), sim share 0.05. Confidence medium (F1 in 0.4-0.7; core rule clean, weak band unexplained).
