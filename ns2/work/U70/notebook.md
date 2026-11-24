# U70 notebook (layer 4, pole -)
## Observations (examples, ~60 positions)
- Nearly every firing position has column 4 EMPTY.
- Top band: opponent (O) has a three that completes at cell (1,4) (row 1, col 4), i.e. the cell directly above the empty bottom of col 4. Playing col 4 would hand them the win.
## Hypotheses
H1: fires when (1,4) in their_wins and heights[4]==0.
H2: more general: cell above landing in col 4 is a their_win (any height).
H3: just col 4 empty + board crowded (heights of cols 3,5).
## Minimal pairs (act)
- Base 6,3,2,3,6,2,3,1,2,1 (O three in row 1 cols 1-3, col 4 empty): 10.2. Mirror (threat at (1,2)/(1,6)): 0.09 -> column-4 specific.
- +4,4 (X fills (0,4), O blocks (1,4)): 0.24. +0,4 (O fills (0,4) so (1,4) becomes a must-block): -8.2 (opposite pole).
- Adding stones elsewhere (0,5,2,3,6 pairs) keeps it 4-9: robust.
- Threat at (2,4) with col 4 height 1: 0.3 (no fire). Threat at (2,4) with col4 empty: -0.8. So specifically cell (1,4).
- Partial O lines (2 O, no X) through (1,4) sometimes give 1.7-3 (weak fires), but many such positions do not.
## Scores
- s1 H1 (heights[4]==0 and (1,4) in their_wins): F1 0.709 P 0.837 R 0.615 AUROC 0.806, sim share 0.75.
- s2 H1 OR "every legal move loses immediately": F1 0.510 (lost positions are not the trigger). Dropped.
- s3 H1 OR poisoned column elsewhere when col 4 full: F1 0.222. Dropped.
- s4 H1, level 2 for col4 empty + X-free 2-O window through (1,4): F1 0.709, sim share 0.78. Final.
## Steer: tiny effects (a few points), slight push away from col 4 where col 4 had mass (-4 pts) else redistribution.
## Synth: best 14.07 (dev game 30305 itself), local search did not beat 14.18.
