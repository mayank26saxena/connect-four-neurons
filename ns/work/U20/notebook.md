# U20 notebook (layer 5, pole +, thr 1.106, dev firing 1.7%, max 7.12)

Empty board sits exactly at threshold (1.106), does not fire.
Steering (max) has ~no effect on move probabilities (<=0.02) in 4 top positions.

## Observations from examples (bands 7-9, ~60 boards)
- Mostly early/middle game (ply 4-28). Last move by O usually lands directly on top of one of my stones (common but not specific).
- Several top cases: O's last move kills the remaining windows of a horizontal pair/three of mine in rows 0-1
  (e.g. 1,6,4,6,2,3 X X O X -> 3.85; 1,6,6,6,2,3 -> 4.16; 6,2,6,2,1,2,2,5,1,4,3,3,5 -> 4.67).

## Hypotheses
H1: O's last move blocks (enters) a 4-window holding >=2 of my stones and none of theirs.
H2: O's last move lands on top of my stone (cell below last is mine).
H3: unit is a mixture / random direction.

## Minimal pairs
- Bottom-row block XX_X with O filling: fires for cols 1,2,_,4 (2.4-3.8 in many contexts) but NOT for cols 0,1,_,3 / 2,3,_,5 / 3,4,_,6 / X_XX (all < 0.3). Highly position specific.
- 3,0,3,0,3,3 (vertical block of three): 0.31. 1,1,2,2,3,4 (horizontal three blocked): 0.26. So H1 in general is false.
- 1,2,2,2,1 = 4.24 but 1,2,2,0,1 = 0.11 (moving my X from (2,2) to (0,0)). 1,2,2,2,1 stacked on O, not on X -> H2 not required.

## Dev metric
1. p1 (O's last stone lands on top of my stone, ply<=24): F1 0.054, P 0.028, R 0.52, AUROC 0.61, sim share -0.09.
2. p2 (H1: last move enters a horizontal window with >=2 mine, 0 theirs): F1 0.033, AUROC 0.51. H1 dead.
3. p3 (last move kills the last open horizontal window of my pair, favouring cols 1-3): F1 0.039, AUROC 0.51.
4. p4 (>=3 of my stones around last move, no immediate win): F1 0.050, AUROC 0.54.
5. p5 (p1 restricted to last col 1-4, ply 5-24, no immediate win for me): F1 0.063, AUROC 0.60. Best, still near chance.

## Other tests
- Single-feature histograms of 320 firing examples: last col spread (peak col 2), ply 5-24 mostly, last row spread,
  parity even; never fires when I have an immediate win (0/320).
- Very configuration-specific: 1,5,2 fires (1.47), 1,4,2 does not (-0.02), 1,6,2 0.82; XX_X bottom fill fires only at cols 1,2,_,4.
- Activation persists after neutral move pairs in some positions (6015 + 6,6 still 6.4), so it is not purely a last-move detector.
- Steering: max/zero change move probs by <=0.04; pushing to 15 at 1,2,2,2,1 lowers column 1 by 0.20. Zeroing raises col 1 by ~0.04.
- Teacher score of column 1 does not track firing.

## Synthesis
Single-move substitution search from dev max (pos 6015): 2,6,4,5,5,4,4,1,5,5,3,0,4,1,3,3,3,3,5,4 = 8.30 (beats 7.12);
0,6,4,5,5,4,4,1,5,5,3,2,4,1,3,3,3,3,5,4 = 7.42 (beats).

## Conclusion
No simple board concept found; looks like a mixture or random direction. Confidence low.
