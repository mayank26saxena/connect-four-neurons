# U15 notebook (layer 5, pole +, threshold 0.860, dev max 44.4)

## Examples (40 across bands + band 9 extra)
- Bands 7-9: essentially all are "opponent just played col 6 and has 3 stacked on top of column 6, must-block at top of col 6".
- Bands 5-6: vertical threes in col 0, col 5, col 4; one horizontal must-block (pos 13180).
- Below threshold: mostly no must-block, or must-block elsewhere (pos 46432: vertical three col 3, act -0.06!).

## Hypotheses
H1: fires when opponent has a vertical three in column 6 (top 3 of col 6 theirs, cell above empty).
H2: fires for any must-block on column 6 (incl. horizontal/diagonal).
H3: graded by column: col 6 strongest, edge columns (0,5) weaker, centre none.

## Minimal pairs (act)
- 3,6,3,6,4,6 (O vertical three col 6): 28.4. Same in col 0: 5.5; col 1 -0.4; col 2 0.9; col 3 0.0; col 4 0.35; col 5 -0.2 (but 5,3,5,1,5 = 3.0). Middle columns erratic near threshold.
- X's own vertical three col 6 (6,3,6,3,6,4): -0.3 -> only the OPPONENT's threat.
- Horizontal threat at (0,6) (2,3,2,4,0,5): 0.08; double threat (0,2)+(0,6): -6.6. Horizontal threat at (0,3) made by playing col 6: -0.6.
- Horizontal threat at (1,6) (3,4,5,3,0,4,3,5,4,6): 23.3; same with last move elsewhere (..6,1): 21.0 -> not about last move; about a must-block cell in column 6 above row 0.
- Vertical col-6 threat persisting after both sides ignore it: 3-5 (still fires, weaker).

## Score 1 (p1: vertical three col 6 or col 0): F1 0.558 P 0.708 R 0.461. Simulation nan (perfect reader -19.7%, so simulation is uninformative for this unit).
FP: only-legal-move col 6 position (-0.5); several col-0 threats not firing.
## Score 2 (p2: vertical three any column, >1 legal): F1 0.433 P 0.328 R 0.638. Middle columns too noisy -> drop.
Miss 16746 (11.9): diagonal must-block at (1,6) -> H5: must-block cell in column 6 (any direction).
- Row-0 col-6 threats (column 6 empty) never fire (1,3,2,4,1,5: -0.09; 2,3,2,4,0,5,3,3: 0.59).
- Double threat (1,2)+(1,6): 12.5 vs single 23.3 -> still fires, weaker.

## Score 3 (p3: opponent playable win in col 6 at row>=1, >1 legal): F1 0.567 P 0.793 R 0.441.
Misses: weak (0.9-4) firing on must-blocks in other columns, esp. col 0 verticals; one where col 6 was the only non-losing move without an immediate threat.
## Score 4 (p4: single must-block in col 6 (row>=1) or col 0 any direction): F1 0.550 P 0.522 R 0.582. Col-0 non-vertical threats are noise (one FP at -14.7).
## Score 5 (p5: col-6 must-block row>=1 (no legal restriction) OR opponent just stacked a vertical three in col 0): F1 0.626 P 0.666 R 0.590. BEST.
Remaining misses: near-threshold (0.9-2) firing on vertical must-blocks in cols 1-5 and some positions with no must-block; middle-column vertical threes are erratic under act (-0.4 to 3.4), so not included.

## Steer
- 3,6,3,6,4,6 (28.4) -> zero: col 6 stays 0.99 (redundant with other circuitry).
- 3,3,4,2,4 (0.06) -> max: col 6 0.00 -> 0.88, cols 3/4 lose 0.43 each.
- 1,4,2,1,6,3,4 (0.23) -> max: col 6 0.00 -> 0.97, col 3 0.77 -> 0.03.
- 2,2,3,4,3,0,3 (must-block col 3) -> max: no change (col 3 stays 1.00).
Effect: a "play column 6 (block there)" push; overridden by a real must-block elsewhere.

## Synthesis: hill-climb single-move edits of top dev game 33520 (44.4) via act: 48.2, 47.8, 46.9, 46.9 all beat dev max.
