# U11 notebook (layer 2, pole -)
## Observations
- Top examples: early-middle positions, centre column 3 has THEIR stone at row 1 (74% of firing) with MY stone at row 2 (71%); column 4 low/empty above row 1 (84% empty at (2,4)); (0,2) occupied (O 59%).
- Per-cell histogram (hist.py, plain single-cell occupancy by band) supports this.
- Not translation invariant: same pattern shifted to col 2 or 4 gives ~0 / 1.5 vs 4.9 at col 3.
## Minimal pairs
- 3,3,4,5,3 (+any O) fires 0.8-4.9; 3,3,3,c fires only for c=2 (1.4) or c=5 (1.0).
- On 3,3,4,5,3,2 (4.92): me at (1,4) -> 1.0; them at (1,4) -> 3.8; me at (1,5) -> 0.17; me at (1,1) -> 0.57.
## Hypotheses
H1: their stone at (1,3), (2,3) not theirs, column 4 has no stone at row 2 and not mine at (1,4).
H2: alternating-row parity pattern in centre (their row 1, my row 2, their row 3).
H3: weighted cell pattern (mixture), positional.

## Score calls
1. p1 (H1 hard rule: their (1,3), (2,3) not theirs, (2,4) empty, (1,4) not mine): F1 0.196 (P .12 R .50), AUROC .69, sim share 0.01. Pattern too common.
2. p2 (hand-weighted cell score, threshold 6): F1 0.301 (P .28 R .33), AUROC .65, sim 0.10.
3. p3 (H2 alternating stripe rows 1-4 in cols 2-3 + col-4 terms): F1 0.277, sim 0.06. Stripe idea no better.
4. p4 (p2 + col-4/row-1/bottom-row terms + ply penalty, threshold 7): F1 0.311 (P .37 R .27), AUROC .63, sim 0.11.
5. p5 (p4 with (0,4)/(1,4) up-weighted, graded fires): F1 0.322 (P .34 R .30), AUROC .785, sim 0.10. FINAL.

## Further minimal pairs
- Absolute-colour histogram (first/second player) is much less discriminative than me/them: the unit is in mover's frame.
- Same board, different move order -> same activation (board-based, not sequence-based).
- Not translation/mirror invariant; no single cell drives it (4-stone grid 4,4,c,d: all < 1). Behaves like an additive
  positional code over low centre cells: mine at (0,3),(0,4),(2,3); theirs at (1,3),(1,4),(0,2),(0,5); (2,4) empty;
  my stones on row 1 to the right and any stone at (2,4) suppress it. Misses include positions with the colours at (0,3)/(1,3) swapped (2,5,4,3,3,5 = 1.4).
- Looks like a distributed / mixture direction; confidence low.

## Steering
zeroing on 4 firing positions (3,3,4,5,3,2 / 0,1,5,3,3,3,5,4,2 / 5,2,...,2 / 2,3,2,4,3,3,4) and forcing max on 3 non-firing: changes <= 8 points, inconsistent direction. Effect: none measurable.

## Synthesis
3,3,3,5,4,2 = 5.048 (dev max 5.431, not beaten); 3,3,4,5,3,2 4.92; 4,5,3,3,3,2 4.89; 3,3,3,5,4,2,3,5 4.65; 3,3,3,5,4,2,0,4 4.61.
