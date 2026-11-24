# U38 notebook (layer 2, pole +, threshold 0.525, dev max 16.75)

## Examples
- Bands 7-9 (act 4-12): almost all have the opponent with 3 stacked at the top of column 0, cell above empty (must-block at col 0), usually last move col 0.
- Bands 5-6 (0.5-2.5): mixed; many have opponent stones at the top of column 0 (two stacked), some unclear.

## Hypotheses
H1: opponent's vertical three on top of column 0, open above (vertical must-block in col 0).
H2: weaker firing from opponent two-stack on top of col 0, esp. when the last move was col 0.
H3: generic "vertical threat anywhere" -- rejected by act (same threat in cols 1,3,6 gives ~0).

## Minimal pairs (act)
- 5,0,4,0,2,0 -> 8.7 ; mirror threat in col 6: 0.08 ; col 3: 0.24 ; col 1: -0.01. Column-0 specific.
- 5,0,4,0,2,0,6,3 (threat still open, last move elsewhere) -> 10.3. Last move not required for 3-run.
- 5,0,4,0,2,0,0,6 (threat blocked) -> 0.42.
- 3,0,0,4,0,5,0 (3-run at rows 1-3) -> 13.1 (higher run, higher act).
- 3,0,4,0 (two-run, last move col0) -> 0.90 fires; 3,0,4,0,2,6 (two-run, last move elsewhere) -> 0.08.
- my own 3-run in col 0 (5,0,4,0,2 from mover's view) -> -2.

## Score 1 (p1: 3-run OR 2-run with last move col0): F1 0.418 P 0.366 R 0.489, sim share 1.45
## Score 2 (p2: 3-run only): F1 0.492 P 0.995 R 0.327, sim share 1.45. Three-run is nearly perfect precision; the rest of firing is weak (0.5-3).
Weak band probes: opponent two-stack on top of col 0 depends on its ROW:
- rows 2-3 (landing row 4): 2.86, 1.0, 2.3, 1.9, 1.4 (fires even when last move elsewhere)
- rows 0-1: 0.9, 0.07, 0.6 (mixed)
- rows 1-2: -0.76, -0.89 ; rows 3-4: -1.6, -3.0 (suppressed)
- single O at r3: ~0.
Dev FPs from p1 fit this (r1-r2 and r3-r4 two-runs were negative).

## Score 3 (p3: 3-run OR their two-run at rows 2-3 with h0==4): F1 0.682 P 0.904 R 0.547, sim 1.52
FPs mostly late-game (30+ stones). Probe: same r2-r3 pair in col0 through a long game: fires for BOTH colours
(when the pair is MINE, ~0.7-0.96; when theirs, 1.4-2.5), declining with ply. Miss 43008 = my own pair at r2-r3.
Next: p4 = 3-run OR (h0==4 and grid[2][0]==grid[3][0] nonzero).

## Score 4 (p4: also my own r2-r3 pair): F1 0.654 P 0.739 R 0.587 -> own pairs cost more precision than they add. Drop.
Long-game probe: their r2-r3 pair act by ply: 8:1.0 10:2.3 12:2.5 14:2.0 16:2.0 18:1.7 20:1.45 22:0.81 24:0.42 26:0.21 -> decays late.
Misses include early r0-r1 their pair just played (5,0,3,0: 0.69; 3,0,3,0: 1.19).
Next p5: 3-run OR (their r2-r3 pair, h0==4, ply<=22) OR (their r0-r1 pair, h0==2, last move col0).

## Score 5 (p5: p3 + ply<=22 on pair + r0-r1 just-played pair): F1 0.428 -- both additions bad (ply cap removed many true late pairs; r0-r1 pairs mostly FP). Revert to p3 (best, F1 0.682).

## Steer
- 4,0,0,6,0,6,3,3,6,6,0 (act 19.9): zero -> col0 block 1.00 -> 0.75 (+0.11 col1, +0.12 col2).
- dev 108191 (1,3,6,0,3,3,0,5,4,1,3,6,5,5,0,3,0): zero -> col0 1.00 -> 0.57, col6 +0.35.
- 5,2,0,0,...: zero -> col0 0.99 (no change). Positions with immediate own wins: no change.
- max on non-threat positions: small inconsistent shifts (+0.18 col3 / +0.22 col6 / ~0), never raises col0.
Effect: helps the model block the vertical threat in column 0; ablating it drops the block by 0-43 points.

## Synthesis (all beat dev max 16.75)
4,0,0,6,0,6,3,3,6,6,0 = 19.9; 4,0,0,6,0,6,3,3,6,6,2,2,0 = 18.7; 4,0,0,6,0,6,6,6,0 = 17.6; 4,0,0,6,0,6,3,3,0 = 17.6; 3,0,0,6,0,6,6,6,3,3,0 = 17.5
Pattern: my stone at col0 row0, their three at rows 1-3, just played; few other stones.
