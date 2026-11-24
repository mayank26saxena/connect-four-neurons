# U87 notebook (layer 5, pole -)
## Examples
Bands 7-9: nearly all = opponent just played col 0 completing a vertical three in column 0, must-block on top of col 0.
Bands 5-6: weaker, often last move col 0 but no must-block; mixed.
## Hypotheses
H1: opponent has vertical three in col 0 with empty cell above (vertical must-block in col 0).
H2: any vertical must-block (any column).  -> rejected by act: same pattern in col 1/2/3/6 gives -2 to -5.
H3: any must-block in col 0 (horizontal). -> 1,0,2,0,4,0,3 (horizontal O row0 1-4?) not firing.
## act tests
3,0,3,0,4,0 1.17; 1,0,1,0,5,0 7.9; col6/col1/col3/col2 versions -2..-5 (no fire). Threat persists when not last move: 1,0,1,0,5,0,6,4 = 7.0.
Strength lower when my stones sit in center cols 3/4 (3,0,4,0,6,0 = 0.56; 1,0,1,0,6,0 = 7.0).
## score log
s1 (p1: opp vertical three in col 0 with empty cell above): F1 0.448 (P 0.912, R 0.297), AUROC 0.648, sim share 0.24.
s2 (p2: + heights<=4, ply<=34): F1 0.378 -- cutoff hurt recall; reverted.
s3 (p3: p1 fires, level graded by ply, late game weaker): F1 0.448, sim share 0.26. Best.
## remaining firing
~70% of firing is low (0.335-1.0) and diffuse: tested horizontal must-blocks near col 0 (0.4 or below), O pairs on bottom-left (no), vertical threats in other columns (strongly negative). No clean second pattern found.
Late-game (ply>30) col-0 vertical threats often do not fire (FPs). Blocking the three kills it (-0.1 to -0.2). My own vertical three in col 0 does not fire.
## steer
Zeroing on saturated must-block positions: no change (col 0 already ~1.0). Max on non-firing positions: changes <=0.10 (e.g. col 3 -0.10). Effect essentially none measurable.
## synthesis
Best ~9.5 (0,1,5,4,0,5,3,4,0); could not beat dev max 11.485.
