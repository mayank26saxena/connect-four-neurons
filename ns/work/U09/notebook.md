# U09 notebook (layer 4, pole -, threshold 0.909, dev max 14.55)

## Observations (examples bands 0-9, ~60 boards)
- Top band: opponent (O) threats in left/center: O row-1 three pointing at (1,4) over empty (0,4); must-blocks at (3,1), (0,4), (3,2).
- Column 4 is empty in most top examples; (0,4) is almost never mine in the top band.
- Last move often in col 1 (row 2) at the top.
- Mid firing band: often no threat at all; col 4 empty common.

## Minimal pairs (act)
- Vertical O three: col2 -> 4.7, col0 -> 1.3-2.1, col1 0-2, col3 ~0.85, col4/5/6 ~0. Strong left/col-2 bias.
- 2,0,2,0,2 = 5.48; same with my stone at (0,4) -> 0.44; O stone at (0,4) -> 5.8. My stone at (0,4) inhibits strongly.
- Horizontal O three row0 at 1,2,3 (threat (0,4)) fires 1.54; at 0,1,2 (threat (0,3)) -0.22; at 4,5,6 (threat (0,3)) -0.26.
- 142409 (14.2): last move O at (2,1) creates second "upper" threat (3,0) next to (1,4) threat; other last moves give ~2.

## Hypotheses
H1: fires when O has a threat cell in cols 0-4 and (0,4) not mine.
H2: fires when col 4 is empty/low and O stones next to it (cols 2-3) -> "col 4 well".
H3: weighted map of O threat cells ((0,4),(1,4),(3,1),(3,2),(3,0)) gated by (0,4) not mine.

## score #1 (v1: any O threat in cols 0-4, (0,4) not mine): F1 0.109, P 0.06, R 0.53. Dead end. (Note: accidentally ran score twice; v1 used calls 1-2.)

## Cell-occupancy histogram (bands 0-2 vs 6-9, ~200 boards each)
- theirs (2,2) 66% vs 26%; theirs (1,3) 61% vs 36%; theirs (3,1) 31% vs 16%; mine (0,4) 21% vs 45%; mine (2,2) 8%; mine (1,3) 12%.
- => H5: anti-diagonal (0,4)-(1,3)-(2,2)-(3,1)-(4,0): O stones on it, none of mine.

## score #2 (v2: >=2 O on anti-diagonal (0,4)-(4,0) window free of mine): F1 0.173 (P 0.105 R 0.48). FP: 6651 O has (0,4),(1,3),(2,2) and unit is -2.5. Line-count idea wrong.
## Histogram of last-move cell by band: top band 9: (2,1) 17/60, (2,2) 16/60, (3,1) 8/60; band 0-2 spread out. -> H6: the opponent's last stone landed at (2,1)/(2,2)/(3,1).

## score #3 (v3: last stone at (2,1)/(2,2)/(3,1)... + O neighbours): F1 0.145, AUROC 0.56. Worse.
## Teacher check: top band positions usually have 5-7 losing moves for me (forced/lost); band 1 usually 0.
## score #4 (v4: number of columns that lose at once (must-block elsewhere / play-under-threat) >= 4): F1 0.136. Tactics proxy fails.
## Minimal pairs on tiny positions:
- 0,1,0,2 fires 1.44 but 0,1,6,2 0.22 and 0,1,6,3 -0.6: my stacked pair in col 0 matters.
- 0,1,0,2,6,1 = 7.5 (O at (0,1),(0,2),(1,1), me at (0,0),(1,0),(0,6)); 0,1,6,2,6,1 = 6.3; mine at (0,4) -> 1.5, at (0,3) -> 2.7.
- 5,1,5,2 = 2.3, 0,2,0,3 = 1.1.
- Row-window [1-4] idea fails (0,1,0,2 vs 0,1,6,2 identical windows).
- Steer effects small and inconsistent (max: +0.04..0.07 col 0, +0.02..0.05 col 4, -0.02..-0.09 col 3; in another position +0.15 col 5; 3,4,5 +0.14 col 3).
## H8: hand-weighted cell score from the single-cell histograms (O on (2,2),(1,3),(1,2),(2,1),(3,1),(0,1),(0,2); mine at (0,0); mine on (0,4),(1,3),(2,2),(3,1) negative; last stone at (2,1)/(2,2)/(3,1)).

## score #5 (v5: hand-weighted cell score, threshold 8): F1 0.157 (P 0.43, R 0.10).
## score #6 (v6: same, threshold 6): F1 0.223 (P 0.17, R 0.31), AUROC 0.63, simulation share 0.01. Best. Kept as final; 1 call unused.
## Steer: effects small (<= 0.15 prob). Max/zero comparisons: firing lowers col 1 in two positions (6459: -0.13; synth: zeroing gives +0.12 col 1), raises col 5 / col 0 / col 4 slightly elsewhere. Inconsistent.
## Synthesis: extending dev top 142409 (O builds a lower-left cluster: row-1 three (1,1)-(1,3), (2,1),(2,2),(3,1), cols 4 empty) reaches 18.3 (beats 14.55).
## Conclusion: no clean concept found. Fires around an opponent stone cluster in the lower-left/center ((1,2),(1,3),(2,1),(2,2),(3,1)), with col 4 empty and no stone of mine at (0,4)/(1,3)/(2,2); strongly positionally modulated, and tactics (threats, forced moves) only correlate. Looks like a mixture or near-random direction. Confidence low.
