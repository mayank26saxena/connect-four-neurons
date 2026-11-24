# U57 notebook (layer 5, pole -; threshold 0.691, dev max 65.9)

## Initial examples
- Top bands (8-9, act 35-66): opponent's last move in column 1, and they now have a must-block cell in column 1 (landing cell of col 1). Mostly vertical three in col 1, some diagonal/horizontal.
- Band 7 (3-15): last move col 1 or 5 with must-block in that same column.
- Band 5-6 (~1-2): mixed; must-block in col 5, some no threats.

## Hypotheses
H1: fires when opponent has an immediate win (must-block) at the landing cell of column 1 (strongest when last move in col 1).
H2: fires when the opponent's last move created a must-block in the same column they played (vertical-ish threat), with column 1 dominant, col 5 weaker.
H3: any must-block in column 1 or 5.

## Minimal pairs (act)
- O vertical three in col 1 with empty cell above: 20-58 (e.g. 0,3,2,6,1,1,3,1,4,1 = 52.6). Same three in col 0/2/4: ~0; col 3/6: <0.5; col 5: 0.8-2.4 (weak secondary).
- Fires even when the last move was elsewhere (…,5,6 appended: 35). Strongest right after O plays into col 1.
- My own vertical three in col 1: -0.4 (no). Horizontal threats landing in col 1 (rows 0 and 1): ~0-0.4 (no). So it is vertical-only, opponent-only.
- Two-stack of O in col 1: mostly ~0, sometimes 1-4 depending on context (not clean).

## Scores
- v1 (col1 O-three OR col5 O-three, vertical, cell above empty): F1 0.441 (P 0.666, R 0.329), AUROC 0.662. Simulation share nan (perfect reader ceiling is negative, -357%; sim metric uninformative).
- v2 (col1 only): F1 0.393 (P 0.994, R 0.245). Col-1 rule is near-perfect precision.
- v3 (v1 + col5 only if ply<=22): F1 0.446 (P 0.768, R 0.314). Tiny gain, ad hoc; kept v1.
- Remaining ~70% of firing is a diffuse tail just above threshold (0.7-3), assorted, often other vertical must-blocks (col 5, col 3) or nothing obvious.

## Steer
- 3,3,4,2 to max: col 1 prob 0 -> 1.00. 2,6,3,6,4,0 max: col1 +0.40. 0,3,2,6,1,4 max: col1 +0.37, col5 -0.37.
- Zeroing at strong-firing positions (col-1 threat): no change (block already chosen via other paths).
Effect: pushes the move to column 1 (block the vertical threat).

## Synthesis
1,5,3,3,1,2,5,4,3,3,6,6,1 = 68.9; 1,5,3,3,1,2,5,4,3,3,1 = 68.7; 1,5,3,3,1,2,6,4,3,3,1 = 67.6 (beat dev max 65.9).
