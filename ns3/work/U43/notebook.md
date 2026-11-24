# U43 notebook (layer 2, pole +, threshold 0.514, dev max 10.23)

## Examples (40 across bands + 10 band 9)
Top band: almost all have opponent (them) vertical three in column 1 at rows 2-4 with must-block at (5,1).
Bands 5-8: column 1 contains opponent stones at middle heights (rows 2-3), often a 2-3 stack.

## Hypotheses
H1: opponent vertical threat in column 1 (must-block in col 1).
H2: opponent stones at specific cells (2,1),(3,1) [+ (4,1),(1,1)] of column 1 (cell detector, not threat).
H3: generic "opponent stack on top of any column" (ruled out below).

## act minimal pairs (me=X to move, O=them)
- Same stack O x3 + top empty in cols 0,2,3,4,5,6: all < 0.32. Column 1 only. H3 out.
- Col1 O rows0-2 (must-block at row3): -0.40 -> H1 alone wrong (threat at low height doesn't fire).
- Col1 X,O,O,O (rows1-3, block at 4): 2.30; X,X,O,O,O (rows 2-4): 3.5-5.8.
- Col1 X,X,O,O (rows 2-3, no threat): 0.95 fires.
- Col1 X,O,X,O,O,O (rows3-5, full, missing (2,1)): -0.04.
- Col1 X,O,O,X,O: 0.07; O,X,O,X,O,O: 0.30; X,O,X,X,O: 0.26.
- Same board after one more move (perspective flips, stones become 'mine'): drops to ~0.3. So it's THEIR stones.
=> H2: needs their stones at both (2,1) and (3,1); (4,1),(1,1) add; empty (5,1) adds.

## Scores
- s1 p1 (their stones at (2,1) and (3,1)): F1 0.506 (P 0.40, R 0.68), AUROC 0.82, sim share 0.46. FPs: stacks capped by my stone at (4,1).
- s2 p2 (top run of theirs >=2 in col1, height 4-5, no must-block elsewhere): F1 0.389. Worse: (2,1) is essential
  (X,O,X,O,O and O,O,X,O,O don't fire), and must-block elsewhere does not reliably suppress (pos 63262 fires 3.4 with one).
- s3 p3 (their stones at (2,1),(3,1) and (4,1) not mine): F1 0.561 (P 0.64, R 0.50), AUROC 0.75, sim share 0.56. BEST.
  Misses: capped/full columns that still fire in some contexts (e.g. 37123, 115108, 102697), near-threshold positions
  with no column-1 pattern (band 5 often has nothing in col 1) -> treated as noise.

## Clean minimal pairs (filler 5,6,6,5,5,6,6,5 then column 1)
X,O,O,O: 2.94; X,X,O,O: 1.85; capped X,O,O,O,X: 0.28; X,X,X,O,O: -0.05; X,O,X,O,O: -0.04; O,O,X,O,O: 0.19;
X,O,O (top row 2): -0.22; X,X,O: -0.42. Works for me first or second (2.43 when me second). Columns 0/2 filled reduce magnitude (1.9, 0.9) but still fire.
Same stacks in other columns: never fire.

## Steer
- Max on fired col-1 stack positions: column 1 +7 to +21 points (e.g. 0.46->0.67). On unrelated position: shifts 2->3 (-27/+19), col1 +5.
- Zero-ablation: tiny (<5 points); dev max position already 100% col 1 (must-block).
Effect: pushes the model toward playing column 1 (on top of their stack), i.e. blocking/capping their vertical in column 1.

## Synthesis
Hill-climb (climb.py, uses synth only) from the dev-max game: 13.80 > dev max 10.23.

## Final: p3 submitted, confidence medium (F1 0.561). Synthesis 15.24, 14.70, 10.59, 10.56.
