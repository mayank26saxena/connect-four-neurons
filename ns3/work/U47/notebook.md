# U47 notebook (layer 5, pole +, threshold 0.886, dev max 26.47)

## Observations (examples, 60+ positions)
- Top band almost all: side to move ("me") has a threat cell (cell completing four) in COLUMN 0,
  often playable (immediate win at col 0) or one above landing. Many also have other threats.
- Mirror of top example (26.4) -> 0.62: strongly column-0 specific.
- Within one game, activation alternates: fires only on plies where me has the col-0 threat.
- Steer to zero: lowers column 0 probability (-0.39, -0.15).
- A few firings with threat at (1,3) over empty col 3 (69730, 27019) and none-threat openings (22844, 2.0).

## Hypotheses
H1: me has any threat cell in column 0 (my_wins with c==0). Level by proximity to landing / count.
H2: me has playable win in column 0 only.
H3: teacher/model wants column 0 (more general "col 0 is the move").

## Minimal pairs (act)
- Bottom-row X three cols1-3, single win at (0,0): 3.5 fires; same three shifted, single win at (0,1): 0.02; opponent fills (0,0): -0.6.
- Open bottom three with two playable wins (any columns): 3.8-5.6 (double threat fires regardless of side).
- Row-2 three cols1-3 with (2,0) threat: d=2 (col0 empty) 2.7; d=1 6-8; playable 12.1; mirror of playable 1.2.
- 20455 game: (3,0) d=2 -> 5.0; (3,0)+(3,4) d=1 -> 10-17 for all 5 opponent last moves; final (2,0) playable + (3,0),(4,0) -> 26.4; mirror 0.6.
- But d=1 col-0 threats often negative (31420 -7.3, 66350 -3.1, 38460 -2.2): when col 0 is not a winning move per engine.
- Creating a threat by playing col 0 (no existing col-0 win cell): ~0. Opponent vertical threes: weak/inconsistent (0.0-0.8 simple, 1-3 in some middlegames).
- Mid band (0.9-3) is diffuse: many must-block positions, left-side 2x2 X blocks (13726 3.3 vs mirror 1.06), openings. No clean rule found.

## Score log
- p1 any my win cell in col 0: F1 0.197 (P .146 R .304), sim share 0.28.
- p2 col-0 win cell with d<=1: F1 0.215 (P .193 R .243), sim 0.39.
- p3 col-0 line windows (2- and 3-stone) + double threats: F1 0.169 (P .10 R .49), sim 0.32. Too broad, dropped.
- p4 col-0 immediate win, or d=1 col-0 threat on my good-parity row, or >=2 immediate wins: F1 0.287 (P .33 R .25), sim 0.53. BEST.
- p5 p4 + require opponent has no threat cells for d=1: F1 0.265 (P .50 R .18), sim 0.51.
- p6 p4 with d=1 allowed also when I have >=3 threats: F1 0.288, sim 0.45.
Final = p4. ~70% of firing is in the diffuse low band not captured.

## Steer
- Zeroing at 26.4: col0 0.76->0.38; at 17.1: col0 0.56->0.14; at 11.6: col0 0.23->0.09; at 5.0: 0.58->0.38.
- Max on 13726: col0 +0.17; 158070: +0.22; forced positions: no change.
## Synthesis: 20455 game + 6,6 -> 26.481 beats dev max 26.467.
