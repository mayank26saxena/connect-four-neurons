# U24 notebook (layer 5, + pole, thr 0.576, dev max 6.99)

## Observations (examples, 160+ positions)
- Top band dominated by must-block at (5,3) (top cell of col 3) right after the opponent played col 3 (up to 6.8).
- Many fires with must-block in other columns ((3,0),(5,0),(5,2),(4,2),(3,1)), and many with col 3 full.
- Steer: forcing high raises column 3 (+0.05 to +0.21); no effect when col 3 full or already ~1.0.
- Position just before the 6.8 one (col 3 poisoned: their threat at (5,3) above landing (4,3)) = -5.55, so the
  negative side is "col 3 is a blunder", the positive side "col 3 is the move".
- 5,4,4,2,2,1,3 (2.70): no immediate threats, but col 3 is the only non-losing move (teacher: all others -989).
- Constructed vertical must-block in col 3 (0,3,0,3,1,3) does NOT fire (-0.10); vertical in col 2 fires 0.87.
- col3 height histogram among fires: mostly 5 or 6 (full), also 1.

## Hypotheses
H1: fires when the opponent has an immediate threat I must block (any column).
H2: fires when there is exactly one non-losing move (forced move), computed by a 2-ply search.
H3: col 3 specific: fires when col 3 is the forced move (block or only-move), plus col-3-full cases.

## Minimal pairs
- Constructed must-blocks in col 3 (vertical at (3,3), vertical at (5,3), horizontal at (0,3)) do NOT fire (-0.24..0.05).
- Row-0 must-blocks in other columns drive it negative (-1.0 to -3.7).
- Col 3 height alone (stacking 0..6 stones in col 3) does nothing (|act| < 0.6).
- 6,4,6,3,5,2,1,x: fires for x in {0,1,2,4,5} but not 3 or 6; 99656 family fires for every legal last move; 39395 family
  stops firing when I get an immediate win. No single board rule found that explains these.
- Natural high cases: opponent's move in col 3 creates a non-vertical threat at the top cell (5,3) (4.7-6.8).

## Dev metric
1. p1 any must-block: F1 0.117 (P 0.07 R 0.34) AUROC 0.60, sim share -0.85
2. p2 col 3 is the forced move (block in col 3 or only safe move by 2-ply search): F1 0.098, AUROC 0.53, sim -0.65
3. p3 any forced move (1 safe move): F1 0.090, sim -0.56
4. p4 non-vertical must-block in rows 4-5: F1 0.043, sim -0.12
5. p5 must-block on col-3 landing: F1 0.110 (P 0.16), sim -0.65
6. p6 must-block and no own win, graded level: F1 0.121, AUROC 0.60, sim -0.88
Single-cell occupancy histograms by band: no cell gives P(fire) above ~0.09. Firing is diffuse.

## Steer
Forcing high raises column 3 (+0.06, +0.21, +0.20, +0.21 on four positions); zeroing lowers col 3 by 0.06-0.11.
No effect when col 3 is full or already at ~1.0.

## Conclusion
No clean concept. Strongest pattern: forced block on the top cell of column 3; overall a diffuse, mixture-like unit
whose output nudges toward column 3. Confidence low.
