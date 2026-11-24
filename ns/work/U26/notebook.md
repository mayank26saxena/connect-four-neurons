# U26 notebook (layer 4, pole -)

## Exploration
- Top examples mostly early-game (ply 2-15), me usually first player (85/120 firing samples even ply).
- Cell frequency firing vs non-firing (240 vs 240 example boards): O at (0,4) 57% vs 30%; X at (0,2) 55% vs 37%; O at (1,3) 50% vs 30%;
  col 4 above row 0 nearly empty in firing; cols 5,6 sparse.
- Minimal pairs (act): 2,2,2,3 = 7.7 (X(0,2),O(1,2),X(2,2),O(0,3)); mirrored 4,4,4,2 = -0.1; shifted 3,3,3,4 = 0.4 -> not translation/mirror invariant.
  2,2,2,c for O's col c: 3:7.7 4:4.7 2:3.1 5:1.5 6:1.2 1:0.7 0:0.15.
  Two-stone grid: O at col 4 is the main driver (0,4 = 2.06); X at col 3 next to O kills (3,4 = -1.5; 0,4,3,6 = -1.3).
  0,4,6,4 (O stacked twice in col 4) = 4.3.

## Hypotheses
H1: opponent stones on the bottom of cols 3/4 (center/right-center), with me holding the bottom of col 2 and me NOT in col 3/4 low cells; early game.
H2: an engine-value feature (bad position for me) -- teacher scores do not support cleanly.
H3: weighted mixture of cell features (distributed, low confidence).

## Score calls
1. p1 cell weights, binary fires: F1 0.102 P0.23 R0.07 AUROC 0.53, sim share 0.06.
2. p2 center-column O count: F1 0.101, AUROC 0.54, sim 0.03.
3. p3 even ply 4-14, me not on (0,3), O on (0,3)/(0,4): F1 0.169 P0.12 R0.31 AUROC 0.62, sim 0.03.
4. p4 graded cell weights + left-column/ply penalties: F1 0.177 AUROC 0.66 sim 0.06.
5. p5 = p4 + bonus if last move in col 3/4: F1 0.180 P0.16 R0.21 AUROC 0.68 sim 0.06. (best; submitted)

## More minimal pairs
- Opening grids (ply 4, a,b,c,d): base 2,2 fires widely when O's 2nd stone is col 3/4 and my 2nd is not col 3; base 3,3 / 3,4 / 3,2 (me on centre bottom) never fires.
- Left-side stacks: 0,0,0,4 = 4.3, 1,1,1,3 = 2.8; right-side mirrors (4,4,4,2 / 5,5,5,4 / 6,6,6,4) ~0. Strongly asymmetric.
- Adding stones in cols 0-1 kills it (2,2,2,3,6,6 = 7.5 -> +0,0 = 2.1 -> +1,1 = -0.1).
- Same board different order: 2,2,6,3 = 6.4 vs 6,3,2,2 = 3.8 (last move into centre adds).
- Mid-game firings (about half of firing) share no clear board pattern I could find.

## Steer
Effects tiny (<0.1 prob). 2,2,2,3: unit on shifts ~0.05 from col 3 to col 5. 2,2,2,4: from col 3 to col 5/4. 5,3,2,2,2,4: raises col 4 by 0.10, lowers col 5. 49974: raises col 4, lowers col 5. 0,4: none.

## Synthesis
Best 2,2,2,3 = 7.73 (dev max 8.07); 2,2,2,4,5,3 = 7.71; 2,2,5,4,2,3 = 7.66; 2,2,2,3,6,6 = 7.55. Deeper games drop. None beat dev max.

## Conclusion
Low confidence: early-opening feature (me first, on left col 2, opponent on centre bottom), mid-game firing unexplained; possibly a mixture / partly random direction.
