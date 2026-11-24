# U28 notebook (layer 5, pole -, threshold 0.637, dev max 7.394)

## Examples (~200 viewed across bands 0-9)
- Firing positions are earlier (mean ply ~14 vs ~20 in bands 0-2), cols 2/3/5 filled, cols 1/4 lower.
- Cell tallies (plain single-cell histograms by band): opponent stone at (0,2) 63% in band 9 vs 30% in band 0; (0,5) rarely empty in band 9.
- Many top boards have opponent horizontal pairs/split twos on low rows (e.g. X.O.O.X, .OO...X, ..O.OOX), but not all.

## Hypotheses
H1 either side has a move creating a double threat (open three with two playable ends). Minimal pairs on bottom row looked
   supportive at first (X.O.O.X 3.47 vs X.O.OX. 0.08; .OO...X 1.26 vs XOO...X 0.02), but strongly asymmetric:
   X.OO... (X stack in col 0) = -0.05 while ..OO..X (X stack in col 6) = 0.77; X.O.O.. with X in col 0 = -0.39, ..O.O.X = 1.02.
H2 opponent has a live horizontal 4-window (>=2 stones, empties playable).
H3 cell pattern: opponent stone at (0,2), low ply, cols 1/4 low.

## Edit scans (replace each move by every other column, read final activation)
- In 4 of 5 top games the opponent stone at (0,2) is critical (every alternative kills firing). Column-6 stones and the
  stones of column 2 above row 0 also matter, in a context-dependent way (X on (1,2) raises in one game, lowers in another).
- Nearly every stone matters in some scans: no compact local pattern found.

## Dev metric
- p1 (H1, double-threat move for either side): F1 0.054, P 0.031, R 0.22, AUROC 0.501, sim -0.01. Chance.
- p2 (H2, live horizontal windows for opponent): F1 0.075, AUROC 0.533, sim -0.02.
- p3 (H3, (0,2) theirs, (0,3) not theirs, ply<=20, h1<=2, h4<=2): F1 0.102, P 0.072, R 0.178, AUROC 0.553, sim -0.02.
Stopped scoring: three genuinely different hypotheses all near chance; further rules would be overfitting.

## Effect (steer to max on 6 non-firing positions)
Consistently lowers column 2 (by 0.09-0.33) and shifts a little mass to columns 5/6 (+0.03 to +0.19). Zeroing it in firing
positions changes nothing (those are usually forced/decided positions). In firing positions the model almost never plays col 2.

## Synthesis
Best valid: 2,3,3,0,3,2,1,6,2,2,2,4,5,3,5 (5.68), 2,3,3,0,3,2,1,6,2,2,0,4,5,0,5 (5.33), 4,6,2,6,4 (5.20),
6,3,2,5,3,2,3,1,5,2,2 (5.11), 6,2,2,1,6,6 (4.74). None beats dev max 7.394 (an 8.09 variant was a finished game).

## Conclusion
Low confidence. Looks like a distributed/mixed direction keyed loosely to early-middlegame low-row configurations with an
opponent stone at the bottom of column 2; no clean concept.
