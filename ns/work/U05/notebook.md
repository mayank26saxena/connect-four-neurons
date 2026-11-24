# U05 notebook (layer 0, negative pole; threshold 0.004, dev max 0.012)

## Examples (40, bands 0-9 + extra band 4/5 seeds)
Every top-band example (bands 6-9) is the position after exactly ONE move (ply 1).
Band 5 is mostly ply 1 (cols 2/3, act 0.005) plus a few later positions at 0.004-0.005, most with last move in column 0.

Hypotheses:
H1: fires iff exactly one stone is on the board (ply 1), strength depends on which column.
H2: H1 except column 6 (act at ply 1 col 6 = 0.002, no fire).
H3: weak tail: later positions whose last move was in column 0.

## act tests (ply 1 by column; layer 0, so deterministic)
col0 0.009, col1 0.005, col2 0.005, col3 0.005, col4 0.008, col5 0.012, col6 0.002 (no fire).
Empty board -0.002, ply 2 ~0.000, ply 3 ~-0.001..-0.003. So: one-stone opening detector, col 6 excluded.

## score 1 (p1: ply==1 and last_col!=6; level by column)
F1 0.910 (P 1.000, R 0.835), AUROC 0.918. Simulation recovers 78.3% of zero-ablation damage; perfect reader -75.1%, share nan
(ablation damage is tiny, ceiling ill-defined). Misses (339): scattered later positions at 0.004-0.006, mostly last move in
column 0 (plies 7-22), ply 41 (last stone of the game), and last move col 4 at plies 25-31.
Sampled ~60 band-5/6 non-ply-1 firings: last col 0 most common, then ply 41, then col 4 late.

## score 2 (p2: + ply 41 + last col 0 at ply 15-22)
F1 0.652 (P 0.501, R 0.934). Column-0 rule far too broad: most col-0 moves do not fire. Dropped.

## score 3 (p3: + ply 41 only)
F1 0.888 (P 0.908, R 0.869). Ply 41 fires only part of the time. Worse than p1. Keep p1.

## steer
Positions [5], [3], [6], [3,3,4], to max and zero: change 0.00 on every column. No measurable effect (activation scale ~0.01).

## synth
[5] = 0.012 equals the dev maximum (deterministic first-move position); [0] 0.009, [4] 0.008; later positions 0.005.
Nothing tried beats the dev max; the dev max IS the single-stone-in-column-5 position.

## Conclusion
Opening-move detector: fires after exactly one stone (the opponent's first move), unless it was in column 6.
Strength by column: 5 > 0 > 4 > 1,2,3 (just above threshold); col 6 below threshold. Weak, sparse tail elsewhere
(mostly opponent just played column 0, and the 41st move) that I could not capture without many false positives.
