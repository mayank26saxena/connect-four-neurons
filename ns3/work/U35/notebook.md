# U35 notebook (layer 5, pole -, thr 0.667, dev max 5.54)

## Observations (examples bands 0-9, ~90 positions)
- Bands 8-9 almost all: late game, board nearly full, exactly ONE (or two) open column(s), typically with 3-5 empty cells, all other columns full.
- Band 5-6: mixed midgame positions with no obvious shared pattern (low/empty columns next to tall ones, sometimes).
- Two early-game band-8 cases: 2,5,0,6,3 (horizontal must-block with gap, O.OO) and 6,3,6,3,5,2.

## Hypotheses
H1: fires when only one column is still playable (all others full).
H2: fires at the moment the opponent's move fills a column, leaving exactly one (sometimes two) playable columns.
H3: well/deep-empty-column hypothesis (low column flanked by tall ones) for midgame cases.

## act tests
- 3 dev games traced (fillinfo.py helper prints which moves filled a column): filling a column with 3-6 legal columns left: no firing (-0.8..0.4).
  Fill leaving 1 legal column: 3.85, 3.51, 2.54 (fires). Fill leaving 2 legal: 2.32 once, -0.69/-0.82 twice.
- After the forced position, playing in the last column (no fill): drops to -0.8/-1.8 in two games, 1.31 in one (101472).
- Early-game wells (2,2,2,2,4,4,4,4: col 3 empty between towers): no firing (0.2). H3 rejected in simple form.
- Early horizontal must-block 2,5,0,6,3 -> 2.19 fires; changing last to 4 (no threat) -> -0.36. 2,4,2,4,2,4,4 -> 0.73 fires; vertical must-blocks (2,4,2,4,2,5) do not.
- steer max/zero on 5 positions (forced and midgame): changes <= 0.02 in any column. Effect: none measurable.

## Score 1 (p1: exactly one legal column AND last move filled a column)
F1 0.253 (P 0.498, R 0.169), AUROC 0.58; sim share -0.94 (perfect 10-level reader only recovers 37%).
Firing is much broader than the forced-endgame case. FPs: lone-column positions at -0.7..-0.9.

## More act tests
- Forced lone-column outcome check: most firing lone-column cases are "my forced move lands directly under their threat" but two
  non-firing cases have the same structure (N-0.72, N0.10). Pos 50843: lone empty col 3, same structure as a +3.6 case, act -3.6.
  => in endgames the activation swings hugely in both directions (min pole value -131), not a clean predicate.
- Early-game band 7-8 cases: bottom-row pair patterns. Extremely idiosyncratic: 3,5,2,6 F(2.98), 3,6,2,5 F(3.69), 3,5,2,5 F,
  but 3,6,2,6 no (0.25); 3,3,1,5 F(1.2), 3,3,1,6 no, 3,3,5,1 (mirror) no; 3,3,3,3,2 F but 3,3,3,3,4 no; 6,2,6,3 F, 6,3,6,4 no,
  0,2,0,3 no. Depends on exact stones, not a mirror-symmetric threat concept. Teacher scores show these are "critical" positions
  (few non-losing moves or one winning move), but several equally critical variants do not fire.
- Midgame threshold band (5-6): no shared pattern found; ply histogram of bands: bands 7-9 almost all ply>=29 (plus ply 4-9 cases),
  bands 3-6 spread over ply 5-40.
- steer on 10 positions (endgame forced, early critical, midgame): max change 0.02 in any column. Effect: none measurable.

## Score 2 (p2: ply>=28, <=3 legal, last move filled a column, a central col 2-4 with >=3 empties)
F1 0.262 (P 0.27, R 0.26), sim -0.85. Central-column idea did not help.
## Score 3 (p3: one legal column, or two legal columns with the last move filling a column at ply>=30)
F1 0.336 (P 0.29, R 0.40), AUROC 0.69, sim -0.94. Best.
## Score 4 (p4: p3 + any 2-legal at ply>=30 + 3-legal with fill)
F1 0.259 (P 0.17, R 0.52), AUROC 0.72. More recall, worse F1.

Conclusion so far: the only reliable regularity is "very late endgame with 1-2 playable columns, especially right after a column
is filled"; within that, sign and size vary wildly. Mid-game and early firing look idiosyncratic. Steering does nothing.
This looks like a random direction (or heavily mixed); confidence low.

## Synthesis
Hill-climb by swapping same-player moves in dev endgames (variants.py), checked with synth. Best so far 4.90 (< dev max 5.54).
Final synthesis: best 5.16 (still below dev max 5.54). Submitted final.json with p3, confidence low.
