# U34 notebook (layer 5, pole -, threshold 1.697, dev max 114.7)

## Examples (40, bands 0-9)
- Bands 8-9: all have opponent vertical three in column 5 with the cell above empty (must-block on top). Activation 60-113.
- Bands 5-7: vertical threes in other columns (2, 6, 1) give 1.5-9; col 5 horizontal must-block 3.8.
## Hypotheses
H1: opponent (just-moved player) has a vertical three in column 5, open on top. Level scales strongly with column 5.
H2: any must-block in col 5 (incl. horizontal/diagonal).
H3: any vertical three threat by opponent, weighted by column (5 >> others).

## act minimal pairs
- O vertical three in col 5 (open top), just made: 50-115. Same after X plays elsewhere and O plays elsewhere (lingering): 7-18.
- X (mover) owns the col-5 three: 0.1. Col 5 full above three: 0.5. Horizontal must-block landing in col 5: ~0.
- Vertical threes in other columns (6 contexts each): col1 mostly 3-5 (fires), col6 mostly 2-5, col4 mixed, col0/col2 mostly <1, col3 ~0.
- My immediate win elsewhere halves col-5 activation (64 -> 32); suppressed some col-2 cases fully.
## score log
- p1 vthree col5 only: F1 0.425 (P 0.986, R 0.270), AUROC 0.635, sim 54.6%.
- p2 vthree any column: F1 0.516 (P 0.389, R 0.766), AUROC 0.864.
- p3 vthree cols 1,4,5,6: F1 0.556 (P 0.521, R 0.597), AUROC 0.790.
- p4 any must-block: F1 0.305 (P 0.184, R 0.898), AUROC 0.887 -> unit is a broad must-block reader but only vertical threats push it over threshold reliably.
- p5 vthree all but col3: F1 0.550 (P 0.433, R 0.754).
- p6 = p5 but non-col5 require no immediate win of mine; graded level: F1 0.557 (P 0.445, R 0.744), AUROC 0.858, sim 72.8% (ceiling reported as nan / negative).
FPs remaining: vertical threes in cols 0,2,4 where unit stays < 1.7; no clean separator found (top-row threats suspected, contradicted by act).
## steer
- Max forces column 5 to ~100% (from col 1 block -> col 5 +0.99; from quiet opening -> col 5 +1.00). Zero on col-5 block lowers col 5 by 0-20 points (redundant with other features).
## synthesis
5,4,5,0,3,1,5 (115.5), 5,4,5,0,5 (115.2), 5,4,5,1,3,0,5 (115.1) beat dev max 114.7.
