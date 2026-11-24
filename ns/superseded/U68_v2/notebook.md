# U68 notebook (layer 5, pole -, thr 0.349, dev max 4.098)

## Exploration
- 120 firing examples (bands 6-9): ~53% have a must-block; of those ~39/64 are in column 0 (rows 3-5), i.e. the opponent
  has three stacked at the top of column 0. Must-blocks in other columns are rarer (col 2: 10, col 4: 9).
- Minimal pairs: vertical O-three in col 0 fires strongly (0,3,0,4,0 -> 2.15; 3,0,4,0,6,0 -> 1.46); horizontal must-block at (0,0) does NOT fire
  (~0). Vertical three in cols 1,3,4,5,6 does not fire; col 2 sometimes (2,5,2,3,2 -> 1.59 but 2,0,2,4,2 -> 0.12).
- My stone at (0,1) lowers it.
- The other ~half of firing has no threat; top examples (4.1, 3.5, 3.1) are quiet positions. In 133872 the jump to 4.1 came
  from O's last move (2,2); the activation persists after further neutral moves (feature of the board, not last move).
  Many of these have col 1 low (h 0-1) and O stones at (1,0)/(2,0)/(0,0).
- Steering: tiny effects (<= 0.05 probability), e.g. zeroing lowers the predicted column by ~0.03.

## Hypotheses
H1: opponent has a vertical three at the top of column 0 with the cell above empty (must-block on top of col 0).
H2: opponent stones in bottom-left (column 0 rows 0-2) with column 1 low.
H3: column 2 vertical three as a weaker variant.

## Tests (act, minimal pairs)
- Col-0 vertical O-three: 0,3,0,4,0 2.15; 3,0,4,0,6,0 1.46; X,O,O,O stack 2.14; X,X,O,O,O 0.83. Extra stones in col 1/2 weaken it
  (+1,1 -> 0.85; +1,1,1,1 -> 0.34). My own vertical three in col 0 does not fire (0.07).
- Horizontal must-block at (0,0): ~0. Diagonal their-threat at (3,0): -0.27. Horizontal their-threat at row 2 of col 0: ~0.6.
- Mirror images of firing positions (c -> 6-c) do NOT fire (left-side specific).
- Quiet top examples (133872 4.10, 23349 3.54, 21911 2.69) jump on a single opponent move; the trigger varies (O at (1,0) matters in
  some, a blocking move in others); no single cell/threat pattern explains them. Pair/single-cell counts over ~120 firing vs
  ~140 non-firing sample boards found no feature with lift > ~2.5 other than the col-0 three.
- Activation is sensitive even to far-away filler stones (O at col 6 vs col 5: 0.69 vs -0.41) -> looks like a mixture.

## Dev metric
1. p1 vthree col0: F1 0.237 (P 0.53, R 0.15), AUROC 0.57, sim share 0.01   <- best
2. p2 any must-block: F1 0.120 (P 0.07, R 0.33)
3. p3 vthree col0 & h1<=3: F1 0.187 (P 0.69, R 0.11)
4. p4 vthree0 or any their-threat in col 0: F1 0.114 (P 0.08)
5. p5 vthree0 or must-block col0 row>=2: F1 0.222 (P 0.34, R 0.16)
Conclusion: the col-0 vertical three is a clean, strong trigger (most of the top bands) but covers only ~15% of firing;
the rest (mostly near-threshold) is diffuse. Confidence low.

## Steering
Effects tiny everywhere (<=0.06 probability): e.g. 3,3,4 max -> col 2 +0.05, col 5 -0.05; 133872 zero -> col 2 -0.03, col 5 +0.03;
must-block positions unchanged.

## Synthesis
Combining the 21911 quiet trigger with a col-0 O-three: 2,3,1,3,3,2,1,2,3,4,4,4,4,0,0,6,0,6,0 = 6.93 (dev max 4.10).
