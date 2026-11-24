# U90 notebook (layer 2, pole +, threshold 1.279, dev max 9.934)

## Examples
- All firing examples are late-game, nearly full boards (ply 31-41). Band 9 = ply 41 (a single empty cell).
- Pos 115327 (ply 36, act 6.45): only column 1 open but column 1 completely empty -> not about #empty cells.
- Act trace on game 129790: ply 39 (2 open cols) 1.2, ply 40 (1 open col) 4.4, ply 41 (1 cell) 7.6.

## Hypotheses
- H1: fires when only one column is still legal (all others full); stronger as more columns are full.
- H2: fires with <=2 legal columns (count of full columns drives it).
- H3: driven by ply / number of empty cells.

## Score 1 (p1: only one legal column): F1 0.665 (P 0.72, R 0.62), AUROC 0.81, sim share 0.04
## Score 2 (p2: <=2 legal columns): F1 0.484 (P 0.34, R 0.87)
- FPs of p1 are odd ply (me = second player); misses are even ply with 2-3 legal columns.
- Minimal pairs on 115327 prefix (ply 34, legal 0,1,6): every 2-move continuation (ply 36) fires 1.9-6.5;
  every 1- or 3-move continuation (ply 35/37) does not (-0.4..0.2). Filling col 1 further: 38 fires 5.3, 39 0.9, 40 6.2, 41 5.6.
- Parity is key: fires when me = first player (even ply) late in the game; ply 41 (last cell) also fires.
- Artificial column-filling sequences (3,3,3,3,3,3,0,0,...) with 4 full columns at ply 24: no firing -> needs late game.
- Game 129790: ply 36/38 with 3 legal columns do not fire; ply 40 with 2 legal fires 4.4.
- Effect via steer --to zero: ~0 change on 2 positions.
H5: (me_first and <=2 legal columns) or ply 41.

## Score 3 (p3: (me_first and <=2 legal) or ply 41): F1 0.550 (P 0.47, R 0.66). Worse.
- FPs: even ply 32-34 with 2 legal columns but many empty cells (not late enough).
- Misses: odd ply 37/39 with one legal column (1.3-1.5), even ply with 3 legal.
- Ply histogram by band (examples, seeds 11-13): bands 7-8 are almost all even ply 36/38/40 or ply 41; band 5 mixes odd 37/39.
H6: pure ply rule: even ply >= 36 or ply 41.

## Score 4 (p4: even ply >= 36, or ply 41): F1 0.631 (P 0.59, R 0.68), AUROC 0.83, sim -0.02
- Pure ply rule nearly matches the legal-count rule; FPs are even ply 36/38 with 2-4 open columns (act 0.3-1.0),
  misses odd ply 37/39 with 1-2 open columns, and some even ply 32-34.
- Teacher scores of FPs/misses show no consistent win/loss pattern -> not an outcome feature.
H7: combine: ply 41; even ply >= 38; even ply 34-37 with <=2 open cols; odd ply >= 37 with one open col.

## Score 5 (p5 combined): F1 0.612 (P 0.50, R 0.80), AUROC 0.89, sim 0.06. Recall up, precision down.
- Act traces of 4 band-8/9 games, plies 28-41: odd plies strongly negative (down to -3.7), even plies 34-38 around 0-1,
  ply 40 = 2.9-5.0, ply 41 = 4.8-8.6. So it ramps sharply at the last 2 empty cells, with odd plies suppressed before that.
H8: ply >= 40 (<=2 empty cells), or me_first with a single open column, or me_first ply>=38 with <=2 open columns.

## Score 6 (p6): F1 0.663 (P 0.81, R 0.56), AUROC 0.78, sim 0.07.
- FPs are mostly ply 38-40 with act 0.8-1.2 (just under threshold). Misses: even ply 34-36 with 2 open cols (act 1.4-3.2), odd ply 39.
H9: ply>=40, or (me_first, ply>=34, <=2 open cols), or (ply 39 with one open col).

## Score 7 (p7: ply>=40 or me_first ply>=34 <=2 open, or ply>=39 one open): F1 0.600 (P 0.51, R 0.73). Worse.
Best: p1 (F1 0.665, sim 0.04) and p6 (F1 0.663, P 0.81, sim 0.07). Submit p6 (encodes the parity effect seen in minimal pairs).

## Steer (--to max / --to zero): changes <= 0.06 on endgame positions, up to 0.10 on an early open position (ply 6: col 2 -0.10, col 1 +0.05). Effect negligible.

## Synthesis: enumerated ply-35 -> ply-41 completions of band-9 games with synth.
- 4505 prefix + 6,6,5,6,6,4 -> 10.565; 6,6,6,5,6,4 -> 10.763; 6,6,6,6,5,4 -> 10.483 (all beat dev max 9.934).
- 145386 prefix best 9.794 (below).
