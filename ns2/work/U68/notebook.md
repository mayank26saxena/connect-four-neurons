# U68 notebook (layer 4, pole -, threshold 1.480, dev max 10.1)

## Observations (examples, 40+ across bands, plus cell histograms by band)
- Firing positions: (1,3) is almost never O (0-6% vs ~35% baseline), (2,2) almost never O, (3,1) often X (51% band 9).
- ~25% of firing is in very early positions (ply 4-7), e.g. 4,5,2,6 (5.7). Fragile: adding two stones anywhere kills it.
- Unit is "me"-relative: in a game it fires after alternate moves.
- Steer: effects are small (<= ~0.16 prob), mostly col 4 / col 2 shifts. 

## Hypotheses
H1: I have >=2 stones, opponent none, in a 4-window on the anti-diagonal through (2,2) [(4,0),(3,1),(2,2),(1,3),(0,4)].
H2: more generally, "2+ of my stones on an open down-right diagonal window with unfilled gaps".
H3: early-opening pattern (col 3 empty, my stone on (0,4)) - possibly separate.

## Minimal pairs
- 6,3,3,1,1,1,1,5 (X at (1,3),(3,1), (2,2) gap): 1.77 fires. Remove X(3,1) -> -0.01; remove X(1,3) -> -0.02. O at (0,4) -> 0.75.
- Add X(0,4) -> 2.34. O at (0,2) (col 2 height 1) strongly suppresses (0.14 / 0.48). X stones in col 0 also suppress.
- 2,1,0,5,... (6.6): replacing X(3,1) with X(0,4) still 3.6 (2 stones in window); replacing with X elsewhere -> 0.65.
- Making 3-in-window with (2,2) playable (immediate win) -> 0.7 (low).
- Band 7 sample: 11/14 midgame firing have the (0,4)-(3,1) or (1,3)-(4,0) window with 2+ X, no O.

## Score log
- s1 p1 (>=2 mine, 0 theirs in a window on the (4,0)-(0,4) anti-diagonal; no immediate win): F1 0.163 (P 0.099 R 0.458) AUROC 0.667, sim share 0.08.
- s2 p2 (same, lines r+c=4 and 5): F1 0.100 (P 0.055, R 0.54). Too broad.
- s3 p3 (anchor X at (1,3) + another X on the diagonal): F1 0.144.
- Found: early-game firing needs my stones on both sides of an EMPTY (0,3) in row 0 (4,5,2,6; 1,0,4,6; 2,6,4,5); same pairs not straddling col 3 give ~0. Row-1 analog does not fire.
- Found: "split" pairs (empty cell between my two stones) on the diagonal matter most.
- s4 p4 (split pair on (4,0)-(0,4) diagonal, no O in window; OR row-0 pair straddling empty (0,3)): F1 0.211 (P 0.171 R 0.273) AUROC 0.617, sim 0.07. BEST.
- s5 p5 (p4 + col 2 low, col 0 low, early part only ply<=8): F1 0.185.
- s6 p6 (split pairs on ANY down-right diagonal): F1 0.078. So it is specific to the (4,0)-(0,4) line.
- Many near-identical boards differ a lot (55001 vs 5742), and the same board via different move order differs (2,4,2,6 1.25 vs 2,6,2,4 -0.09; 4,5,2,6 5.7 vs 4,6,2,5 3.9). Unit depends on move order/last move; no clean board rule found. Possibly a mixture or random direction.

## Steer
- Mostly small (<0.16). In 107252 / 96916 zeroing lowers col 4 (the move that adds a 3rd stone to the (0,4)-(3,1) diagonal); in the synth position zeroing lowers col 0 by 0.23 (landing (4,0) adds a 3rd stone to the (4,0)-(1,3) diagonal) and raises col 4 by 0.27.

## Synthesis
- Local search from dev pos 82037 (10.1): single-move substitutions give 11.61, 11.53, 10.50, 10.46, 10.33 (all beat dev max).
