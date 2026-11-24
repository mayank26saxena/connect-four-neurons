# U67 notebook (layer 0, pole -; threshold 2.439, dev max 4.430)

## Observations (examples, ~250 positions in bands 2-9)
- Band 9: 52/52 have last move in column 1 landing at row 5 (i.e. the move that fills column 1).
- Bands 6-8: (last_col=1,row=5) dominates (34/60, 41/60, 47/60); rest are late-game moves high in edge columns 0/6 or row 4 in others.
- Band 5: mixed, (1,5) 13/60, (0,3) 11/60, other late-game moves.
- Strongly late-game (ply mostly 20-41).
- act: 1,1,1,1,1,1 rises 1.2,1.7,2.4 with stack height; same stack in cols 0,2-6 stays ~0.5. Column 1 specific.
- act: in a game, col-1 stones at rows 3/4/5 gave 0.18/1.65/3.77; last move elsewhere drops it to ~0.5-1.0.

## Hypotheses
H1: fires when the opponent's last move filled column 1 (last_col==1, last_row==5).
H2: H1 plus late-game high-landing moves in edge columns (0/6) at row>=3.
H3: activation = f(last move col 1, its row) + general late-ply bump.

## Tests (act minimal pairs)
- Fill move strength grows with ply: 1x6 at ply 6 -> 2.38; after 8-stone prefix -> 2.65; after 18-stone prefix -> 4.36.
- Last col-1 stone at row 3/4/5 -> 0.18/1.65/3.77 in same game. Stacking other columns to the top: ~0.5 flat.
- After column 1 is full, later moves stay on an elevated plateau (~1.5-2.8) that rises with ply, so many late-game positions (ply 30-41) with column 1 full fire without the last move being in column 1.
- Plateau: higher when the top stone of column 1 is the opponent's (parity effect, seen in 3 games), and when the last move is in column 0/2/6 vs 3/4/5 (~0.4 higher, minimal pair at fixed position).
- Recency since the fill did NOT help (p3).

## Dev metric
- p1 (fill move only): F1 0.617 P 0.773 R 0.513 AUROC 0.754, sim share 0.15.
- p2 (fill ply>=12 OR col1 full & ply>=34): F1 0.505 P .348 R .923 AUROC .935, sim .46.
- p3 (recency since fill): F1 0.362 - wrong, misses were ply-41 positions long after fill.
- p4 (fill ply>=12 OR col1 full & ply>=37): F1 0.627 P .506 R .824 AUROC .900, sim .47.
- p5 (p4 + theirs-top bonus, looser): F1 0.530 AUROC .939, sim .47.
- p6 (p4 + theirs-top and last-col 0/2/6 bonuses): F1 0.645 P .525 R .838 AUROC .907, sim .47.  <- final
## Steer
- 5 positions (fill positions and a low position steered to max/zero): change <= 0.03 in any column. None measurable (column 1 is already full when it fires).
## Synthesis
- Random valid ~20-28 stone prefixes avoiding col 1, then six consecutive col-1 moves: up to 4.487 (> dev max 4.430). At ply 42 (board full) only ~1.7.
