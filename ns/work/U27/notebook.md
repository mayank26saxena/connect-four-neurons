# U27 notebook (layer 0, pole +, threshold 0.715, dev max 4.71)

## Examples
- Band 9 (top): nearly all have last move in column 0 and column 0 full or nearly full (height 5-6), often last two moves 0,0.
- Lower firing bands mix: many still last col 0 with tall col 0; others are tall col 0 with last move elsewhere; a few early-game oddities (0,4 -> 1.05; first move 4 -> 0.715 exactly at threshold).

## Hypotheses
H1: column 0 tall (>=5 stones). H2: last move in column 0 landing high (row>=4). H3: count of the mover's own stones in column 0 (layer-0 token-count feature).

## act tests
- 0x6 sequence: 0.66 (h3), 1.19 (h4), 2.43 (h5), 2.93 (h6). Full col 0 then a move elsewhere stays ~3.0-3.3.
- 3x6, 1x6, 2x6, 6x6: ~0 -> it is column 0 specifically.
- 0,0,0,0,0,3,0 (full, top stone theirs) 1.70 vs 0x6,3 (top stone mine) 3.28: color/order matters.
- Game traces: last-move-into-col0 at row 3 by player making a vertical three gave -1.25; next move on top (row4) gave 1.77. Activation oscillates with parity after col 0 is full (higher when mover owns more col-0 stones).

## More act tests
- Same board, different move order at ply 10: 2.68-2.88 (order barely matters in short games). At ply 24 the same board gave 1.09 (col-0 moves first) vs 2.91 (col-0 moves last): some recency / long-game dilution.
- Filler columns before 0x6 (ply 12): 3,4-alternating 2.54; 5,6 1.64; 1,2 0.87; 2,1 0.22; 1x6 0.05. Stones in column 1 suppress (theirs in col 1 most).
- Ownership of column 0: full col 0 with mover owning 4 stones 3.4-4.0; 3 stones 2.9-3.3; 2 stones 1.2-1.7.
- A move elsewhere right after filling col 0 drops activation (e.g. 3.38 -> 1.18 as ownership flips and last move leaves col 0).
- Long filler games (30+ ply) with col 0 filled last: ~0 to 0.3. Strong long-game penalty.

## Dev metric log (note: calls 1 and 4 were accidental duplicate runs of p1/p2)
- p1 (h0>=5 and last move col 0): F1 0.316, P 0.28, R 0.36, sim share 0.01.
- p2 (h0>=5 and h1<=2): F1 0.371, P 0.31, R 0.47, sim 0.04.
- p3 (linear score: height, ownership, last-col-0, -h1, -ply): F1 0.414, P 0.68, R 0.30, sim 0.13.
- p4 (re-weighted ownership, threshold 0.9): F1 0.456, P 0.57, R 0.38, sim 0.11.
- p5 (+ extra penalty past ply 26, thr 0.75): F1 0.536, P 0.78, R 0.41, sim 0.15.
- p6 (= p5 with threshold 0.45): F1 0.628, P 0.70, R 0.57, AUROC 0.78, sim 0.15. FINAL.
Histogram of ~160 firing examples: nearly all have column 0 with >=4 stones (mostly full); exceptions are a handful of 1-3 ply openings.

## Steer
Six positions (col 0 full or 5 high): changes <= 2 points; with col 0 at 5 stones, forcing max lowers column 0 by ~2 points. Effect essentially none.

## Synthesis
5,0,4,0,0,0,4,0,0 -> 4.787 (beats dev max 4.71). 4,0,4,0,0,0,5,0,0 4.70; 4,0,4,0,0,0,4,0,0 4.67; 3,0,4,0,0,0,4,0,0 4.64; 2,0,4,0,0,0,4,0,0 4.65.
Recipe: short game, column 0 full, mover owns 4 of its 6 stones, opponent just played the top stone, column 1 empty.
