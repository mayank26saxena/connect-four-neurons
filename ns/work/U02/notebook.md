# U02 notebook (layer 1, pole -, threshold 0.696, dev rate 2.7%, dev max 1.607)

## Observations from examples (bands 0-9, ~100 positions)
- Very top dominated by ply-1 positions: opening 3 -> 1.330, 0 -> 0.873, 6 -> 0.728 (fire); 1 0.687, 2 0.676, 5 0.696, 4 0.264 (not).
- 6,6,6 -> 1.607 (dev max).
- Later firing examples: last move often in col 1 (row 0 early or row 5 = filling column), col 6 (rows 1-5), col 4 (rows 3-5), col 3 row 2.
  Layer 1 => probably a lookup on the last-move cell (column x height) plus a little context.

## Hypotheses
H1: fires depending mainly on the cell of the last (opponent) stone: a set of "hot" cells.
H2: opening position after 3 (ply 1) is a separate strong case.
H3: something about the column being filled (last_row==5) for cols 1/4/6.

## Tests
- Ply-1 openings (act): 3 1.330, 0 0.873, 6 0.728 fire; 1 0.687, 5 0.696 (just below), 2 0.676, 4 0.264.
- Random-game tally of activation by last-stone cell (act on 200 random games): no cell fires >20% of the time -> last cell alone is not the rule.
- Minimal pairs at ply 4 (5,4,4,1 = 1.155): changing any earlier stone moves it by 0.3-0.9; same board through different move orders gives nearly the same value (board-based, not order-based), but the dependence on the other stones has no clean pattern.
- Ply-2 grid of all 49 openings: only 6,6 fires (0.813). Column-6 stacking early is strongest (6,6,6 = 1.607 = dev max; 6,6,6,6 1.272), but 6,6,6,6,6 drops to 0.357.
- Late-game firings: concentrated on the last stone topping cols 6/1/4/0 (row 4-5), with even ply favoured, but graded and not separable.

## Dev metric
1. p1 ply==1 and last col in {0,3,6}: F1 0.644 (P 1.00, R 0.475), AUROC 0.738, sim share 0.00.
2. p2 + broad early/late hot-cell lookup: F1 0.193 (P 0.108, R 0.877). Far too broad.
3. p3 = p1 + late (ply>=20, even, row 5, cols 1/4/6): F1 0.490 (P 0.416). Added rule ~12% precision.
4. p4 = p1 + early col-6 stacking (rows 1-3, ply<=10) + col1 row0 ply<=7: F1 0.502 (P 0.437). Added rules also low precision.
=> Only the ply-1 component is clean; the remaining ~half of firing is spread thinly over many positions with no rule I could find. Keep p1.

## Steering
zero on 3,4,5,...,6,4 (col-4 fill), zero on opening 3, zero on 6,6,6, max on 5,4,4,1 and 2,4,6,4: all changes <= 0.01. No measurable effect.

## Synthesis
Local search with act (mutating sequences) could not beat 6,6,6 (1.607 = dev max). Best others: 0,3,6,6,6 1.548; 0,6,6,6 1.529; 6,0,6,3,6 1.483.

## Conclusion
Low confidence. Fires reliably right after the first move of the game when it is in col 3 (strongest), 0 or 6. The rest of the firing looks like a diffuse mix (early stacking of column 6, late moves that top off cols 6/1/4/0) with no clean rule. Steering does nothing. Could be a random direction.
