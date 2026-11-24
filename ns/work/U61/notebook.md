# U61 notebook (layer 2, pole +, threshold 0.897, dev rate 3.0%, dev max 7.03)

## Observations from examples (bands 0-9)
- Firing positions are mostly early/mid game (ply 3-16).
- Two recurring top-band shapes:
  (a) bottom row with THEIR stones at (0,1) and (0,5), often MY stone at (0,2) (".OX..O.", ".OXX.O.")
  (b) column 3 stacked them,them,me,them (rows 0-3), often with my stone at (0,2).
- Last move modulates strongly but position matters (same position + different last col: -1.6 .. 4.7).

## Candidate hypotheses
H1: weighted sum of cell ownership: theirs at (0,1),(0,5),(1,3),(3,3); mine at (0,2),(2,3).
H2: "opponent has stones on b- and f-files at the bottom (cols 1 and 5)" alone.
H3: random/distributed direction (no clean concept).

## Minimal-pair findings (act)
- Ply-3 grid (them a, me b, them c): fires mainly with THEIR stones at (0,1)+(0,5) and MY stone at (0,2) (5,2,1 = 3.42; 1,2,5 = 2.53).
  Their stone at (0,6) strongly suppresses (0,2,6 = -3.6; 5,2,1,4,6 = -0.5 vs 5,2,1,4,0 = 2.8). My stone at (0,5) suppresses.
- Column-3 tower (their (1,3) and (3,3), my (2,3)) is a second route: 3,3,1,4,3,3 = 1.26 but removing their (3,3) -> ~0.
- My stone at (0,2) present in 32/32 top-band examples checked (except the 1-ply opening "1", which fires at 0.996).
- Activation fades with ply; almost nothing fires after ply ~16.
- Last-move order matters noticeably (same final stones, different order: 4.4 - 6.2).

## Dev metric
1. p1 bottom (0,1)+(0,5) or tower, no ply gate: F1 0.111 (P .07 R .28)
2. p2 + ply<=16 + ply1 rule: F1 0.346, AUROC 0.69, sim share 0.07
3. p3 weighted cells, M(0,2) gate, no ply gate: F1 0.274
4. p4 weighted, ply<=15: F1 0.412, AUROC 0.71
5. p5 + tower weights, threshold 3.0: F1 0.373, AUROC 0.74
6. p6 (p4 + tower + my (0,5) negative): F1 0.440 (P .415 R .468), AUROC 0.72, sim share 0.07  <- best

## Steer
Max/zero on 5 positions: changes <= 0.04 in any column; effectively no measurable effect.

## Synthesis
0,3,2,5,2,3,3,3,0,1 = 7.124 beats dev max 7.029 (local search via act).

## Conclusion
Distributed cell-template unit; no single clean concept; medium-low confidence (best F1 0.44).
