# U01 notebook (layer 2, pole -, threshold 1.462, dev max 9.552)

## Observations (40+ examples)
- Nearly all firing positions: center column (3) holds exactly 4 stones and the top one (row 3) is the opponent's; cell (4,3) is the landing cell.
- Top band: two or more opponent stones stacked at rows 2-3 of col 3.
- Near threshold: some with top stone mine, a few last move elsewhere.

## Hypotheses
- H1: heights[3]==4 and grid[3][3]==theirs. Level grows with contiguous their stones below and last_col==3.
- H2: just "last move landed at (3,3)" (opponent's 4th stone in center).
- H3: center landing row == 4 regardless of color.

## Minimal pairs (act)
- 3,3,3,3 -> 1.51 ; +0 (top becomes mine from mover's view) -> 0.39 ; 3,3,3,3,0,0 (top theirs, last move col0) -> 0.78
- 3,3,3,0,3 (top two theirs) -> 4.06 ; 3,3,0,3,3 (top theirs, below mine) -> 1.10
- 3,3,3,3,3 (height 5) -> -7.2 ; height 3 -> ~ -0.2..-0.7
- same in col 2 / col 4 -> ~0 (center-specific)
- 0,3,0,3,0,3,1,3 (col3 all theirs) -> 2.95 ; col3 mine,mine,mine,theirs -> 1.18
=> H1 supported; H3 rejected (color matters); H2 partial (last move in col3 helps but not required).

## Dev metric log
1. h1 (base: h[3]==4 & (3,3) theirs): F1 0.680 (P .526 R .964) AUROC .968; sim share 1.04. Recall great, too many FPs.
2. h2 base & ((2,3) theirs or last_col==3): F1 0.756 (P .780 R .734) AUROC .864.
3. h3 base & not((2,3),(1,3) both mine): F1 0.667. Rejected; last-move-in-center matters more than below-color.
4. h5 h2 or ((1,3) theirs & ply<=14): F1 0.779 (P .721 R .847).
5. h6 h2 or ply<=14: F1 0.777 (P .685 R .897) AUROC .942; sim 1.04. Simplest good one -> chosen.
6. h7 points system (+2 (2,3)T, +2 last3, +1 (1,3)T, +1 ply<=14, -1 ply>=24, fire >=2): F1 0.781, sim 1.02. Marginal gain, more complex.
7. h8 h7 + col-4 height terms, threshold 3: F1 0.753. Col-4 suppression (seen in act: 2 stones in col 4 drop 4.1->1.6) does not generalize.

## Extra act findings
- Stones in column 4 (not 2, 5, 6, 1) suppress; their stone at (0,0) and my stones at (0,1)/(0,5)/(0,6) mildly boost.
- Activation decays mildly with ply (4.1 at ply 5 -> 2.5 at ply 17 for same center column).
- Max: their three stacked at rows 1-3 of center (vertical threat at (4,3)), just played: ~9.1.

## Steer
- 3,3,3,0,3 max: changes <=5 pts; 3,3,3,3,0,0 max: col1 -17, col3 +7; 4,0,6,3,3,1,2,3,5,3 zero: col2 +6. Small, no consistent direction.

## Synthesis (act): 1,0,1,0,3,3,5,3,6,3 9.156; 1,0,3,3,5,3,6,3 9.145; 1,0,3,3,6,3,5,3 9.095; 1,0,6,0,3,3,1,3,5,3 9.046; 6,0,3,3,1,3,5,3 8.975 (all below dev max 9.552).
