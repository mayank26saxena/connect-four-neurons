# U16 notebook (layer 1, pole -, threshold 0.823, dev max 5.038)

## Examples (40, bands 0-9)
Nearly every firing example has last move in column 0 (one band-5 example: last move col 6), with the stone landing high
(row 3-4, i.e. 4th/5th stone in column 0). Low bands: last moves elsewhere.

Hypotheses:
- H1: opponent's last stone was in column 0 and landed on row 3 or 4 (column 0 now 4-5 high).
- H2: any edge column (0 or 6), high stone.
- H3: column-0 height alone (regardless of last move).

## act tests
- 0,0,0,0 -> 2.83 fires; 0,0,0,0,0 -> 2.94; 0,0,0,0,0,0 (row 5) -> -0.03; 1,0,0,0,0,0,0 (row5) 0.245.
- 3,0,0,0 (row 2) -0.25; 3,0,3,0,3,0 (row 2) -0.73. 0,1,0,1,0,1,2,0 (row 3) 1.98.
- 6,6,6,6 / 6,6,6,6,6 ~0: column 6 does NOT do it (H2 rejected). 3,3,3,3 col 3 no.
- Game with col0 height 4 but last move col 5: -0.38 (H3 rejected; last move needed).
=> H1 supported. Stone colours inside column 0 seem not essential (0,0,0,0 alternating vs 3,0,0,0,0,0).

## Score calls
- call 1/2 (p1: last_col 0 and last_row in {3,4}): F1 0.719 (P 0.614, R 0.870), AUROC 0.927, sim share 0.95.
  (call 1 was an accidental duplicate run of the same program.)
- call 3 (p2: + "move before last was col0 row3/4"): F1 0.544. That clause mostly does not fire in dev; dropped.
- act: tall columns 1 and 2 suppress (row 3 with col1 full 1.03, col2 full 0.74, both 0.23; row 4 robust 2.3-3.4).
  Row 5 (6th stone) inconsistent: fires only when col1 full in tests.
- call 4 (p3: linear est base(row) - heights of col1/2, row 5 if col1 full): F1 0.726, sim 0.78. Row-5 rule = FPs late game.
- call 5 (p4: no row 5 rule, milder height coefs): F1 0.762 (P 0.679 R 0.869), sim 1.05.
- call 6 (p5: row-3 base decays with ply): F1 0.842 (P 0.852 R 0.833), AUROC 0.914, sim 1.05.  <- final
- call 7 (p6: also ply decay on row 4): F1 0.842, sim 1.06; no gain, keep p5.
Remaining misses: column 0 reached 4-5 high a few plies ago (activation decays over 1-3 later moves).
Remaining FPs: very late game, row 4 with tall cols 1/2.

## Steer
Three positions (0,3,1,1,0,4,5,4,4,3,0,0,5,4,0 ; 1,1,0,0,0,0,0 ; 3,3,0,0,0,0): max and zero change move probs by <= 0.02. No measurable effect.

## Synthesis
Best ~4.68 (0,5,0,5,5,0,0,1,1,5,6,0), 4.63, 4.56; none beats dev max 5.04. Early game, col0 5 stones, cols 1-2 low.
