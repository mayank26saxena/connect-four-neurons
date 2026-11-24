# U41 notebook (layer 5, pole +, threshold 1.405, dev max 31.76)

## Examples
Top bands (7-9) almost all: last move col 1, must-block at top of column 1, opponent has 3 stacked vertically in col 1.
Band 6: also must-block in col 2 (vertical three in col 2, ~4), horizontal threats at (1,1)/(2,1), some no-threat positions.

## Hypotheses
H1: opponent has an immediate (playable) win in column 1 (must-block at landing(1)); strongest for vertical three.
H2: also vertical three in column 2 (weaker, ~4).
H3: generic "must-block" (rejected by act: col 0/3/4/5/6 vertical threes ~0-0.8).

## act tests
- 1,3,1,4,1 -> 21.9 ; same with col0 0.84, col2 3.7, col3 0.08, col4 -0.1, col5 0.18, col6 0.21
- vertical three in col1 blocked (extra stone on top) -> -0.1; my own vertical three col1 -> 0.25
- not last move (they played elsewhere after) still 10-11 -> not about last_col
- horizontal row-0 threat at (0,1) (O at 0,2,3 or 2,3,0) -> ~0.1 (does NOT fire)
- horizontal row-1 threat at (1,1) (pos 140571, O at (1,0),(1,2),(1,3)) -> 6.3-8.3 fires regardless of which stone was last
- same but O at (1,2),(1,3),(1,4) => double threat (1,1)+(1,5) -> 0.09 (!)

## Scores
- p1 (col-1 must-block row>=1 OR vertical three col 2): F1 0.530 (P .53 R .53). FPs: double threats, my own win available, high-row diagonal threats; col-2 vertical unreliable.
- p2 (col-1 must-block row>=1, no my immediate win; non-vertical only if single threat): F1 0.582 (P .755 R .473)
- p3 (+ their win directly above landing(1)): F1 0.422 (P .30) -> too broad, dropped
- p4 (p2 + non-vertical only rows 1-3 and no their-win above the block cell): F1 0.604 (P .880 R .460) AUROC .73  <- BEST
- p5 (p4 + their drop in col 1 would create >=2 / unstoppable threats): F1 0.520 -> dropped
- p6 (p4 + single must-blocks in cols 0/2 at level 2): F1 0.439 -> dropped
Simulation share reported as nan (ablation damage tiny/negative; unit's effect is redundant when the block is already chosen).

## Misses
~half of firing is diffuse near threshold (1.4-2.5): positions where their threats are in/near column 1 but not
immediately playable, col 0/2 must-blocks, "col 1 is the only safe move" by search. Not capturable simply.

## Steer
- 3,3,4,2 (act -0.2): max -> col 1 +0.60 (col 3 -0.48)
- 5,0,2,3,2,4,0,1,4 (act 7.4): max -> col 1 +0.46
- 1,3,1,4,1 / 6,4,3,1,3,1,0,1: zero -> no change (model already blocks with prob 1.00)
Effect: pushes the model toward column 1; ablating it does not stop the block (redundant).

## Synthesis
6,4,3,1,3,1,0,1 = 29.78; 3,4,6,1,3,1,0,1 = 29.73; 3,4,3,1,6,1,0,1 = 29.46; 6,4,3,1,3,1,4,1 = 29.2; 3,1,0,1,6,1 = 24.5 (all below dev max 31.76)
