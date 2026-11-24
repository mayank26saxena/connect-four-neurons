# U25 notebook (layer 5, pole -; threshold 5.735, dev max 14.83, rate 3%)

## Observations (examples, ~80 viewed)
- Top bands (>11): almost all late game (ply 30-40), with 1-2 columns still open, usually a central column (2/3/4)
  nearly or fully empty while the rest are full ("deep well").
- A small early-game cluster (ply 5-7): open three on the bottom row with both ends open (double threat, either side).
- facts: most firing positions are decided (teacher score ~ +-960..990: forced win/loss), but a draw with one legal
  move also fired (41107, 6.55), and single-move wins with an immediate win were low (141278, 3.08).
- My immediate wins seem to suppress (several 4.5-4.7 non-firers have my_playable_wins).
- Activation oscillates ply-to-ply within a game in the endgame (who is to move matters).

## Hypotheses
H1: late game (ply>=28) with few legal columns (<=3), not having an immediate win.
H2: position is decided (forced win/loss), approximated by endgame + threats.
H3: deep well: one open column with many empty cells, others full.

## Score calls
1-2. h1 (ply>=28, <=3 legal, no immediate win; early double threats). (Accidentally ran twice: calls 1 and 2.)
     F1 0.359 (P 0.22, R 0.91), AUROC 0.909, sim share 0.35. Endgame-ness ranks well; too broad.
3. h4 "every legal move hands opponent an immediate win (poisoned columns)": F1 0.420, AUROC 0.673, sim 0.16.
   Mid-game poisoned positions do NOT fire -> it is an endgame feature.
4. h5 exact solver (<=12 empty), fire if lost: F1 0.430 (P 0.31 R 0.69), sim 0.33. Lost positions with many legal
   columns don't fire.
5. h6 legal<=3 and (lost, or draw with 1 legal column), solver up to 16 empty: F1 0.507 (P 0.37 R 0.80), AUROC 0.878, sim 0.38.
6. h7 >=4 full columns, <=3 legal, not won: F1 0.431. Worse.
7. h8 legal<=2 & not all moves win, or 3 legal lost ply>=31: F1 0.451. Worse (ply-41 single-cell draws are FPs).
8. h9 = h6 but 3-legal losses require ply>=31: F1 0.539 (P 0.42 R 0.75), AUROC 0.858, sim share 0.38. FINAL.

## Minimal pairs (act)
- Neutral constructed fills (stack columns 0,1,6,5 alternately): 4 full cols -> 4.9; adding column 2 full -> 12.5;
  then col 4 x2 -> 12.5, x4 -> 13.5. So the core driver is "board mostly full, few open columns", not threats.
- A new partial column lowers it (first stone into col 2: 4.9 -> 2.0); odd/even ply oscillation of ~3-5 within a game.
- Column identity matters somewhat (B2+3,3 = 6.7 vs B2+4,4 = 4.0).
- Value of the game correlates (lost positions high, won positions mostly low, e.g. 65642 all-win 1.5) but is not the cause:
  neutral filled boards fire too.

## Steer
Zeroing in firing endgames: no change (moves forced). Forcing max: small reshuffles (590: col2 -0.22, col4 +0.18;
30086: col3 -0.15, col4 +0.14; 87438-type midgame +0.05 col1). No consistent column. Effect weak.

## Synthesis
Best constructed 13.59 (< dev max 14.83).
