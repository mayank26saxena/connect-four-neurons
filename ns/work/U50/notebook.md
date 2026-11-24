# U50 notebook (layer 1, pole -, threshold 0.686, dev rate 3.0%, dev max 3.660)

## Examples
Bands 5-9 are almost all openings: ply 2-8, mostly even ply (I moved first). Bands 0-4 are midgames.
Only a couple of firing examples past ply 10.

## Hypotheses
H1: opening (ply <= ~8) position where the opponent's last stone is in col 0, 3, 5 or 6 (not 1/2).
H2: additive "column token" detector: opponent stones in col 1 (strongly) and col 2 suppress; stones in col 0/3/5/6 and
    tall stacks (5,5,5 / 0,0,0) boost; decays with ply.
H3: just "early game" (ply small).

## Minimal pairs (act)
Ply-2 sweep (row = my 1st move, col = opponent reply):
0: 1.51 -3.81 -1.43 0.80 0.33 0.45 1.40
1: 0.26 -0.06 -1.47 0.22 -0.12 0.07 0.63
2: 0.89 -3.03 0.03 0.73 0.18 0.48 1.28
3: 1.18 -2.31 -0.66 1.69 0.60 0.86 1.66
4: 1.33 -3.03 -1.08 1.06 0.61 0.59 1.49
5: 1.83 -1.84 -0.03 1.71 0.99 1.57 1.89
6: 1.39 -2.58 -0.61 1.40 0.90 0.88 0.46
-> opponent's last col: 0/3/6 best, 5 good, 4 medium, 2 bad, 1 very bad. My col 1 lowers; my col 5 raises.
Ply 3/4 sweeps after 5,6 and 3,3: odd ply (my stone last) mostly < 0.7; ply 4 same last-col pattern
(last col 1 negative, 0/3/6 high), my 3rd-ply stone in col 5 raises, col 1 lowers.
Odd ply exceptions: 0,0,0 (1.78), 5,5,5 (1.03), 0,0,5, 0,0,3 fire. Later: 5,5,5,0,5,2 (ply 6) 2.37; 3x6 stacked in col 3 (ply 6) 1.65.
Activation after each move in a normal game drops below 0.4 after ply ~6.

## Score calls
- call 1 and 2 (p1, same program twice by mistake): last col in {0,3,5,6}, even ply 2-8. F1 0.453 (P 0.33 R 0.72), AUROC 0.837, sim share 0.10.
  FPs had stones in cols 1/2/4 elsewhere -> contributions are additive over all stones.
- Minimal pairs at ply 4 (X5,O?,X5,O0): earlier opp stone col 1 -> 0.81 vs col 5 -> 3.42; (X?,O6,X5,O0): my col 1 -> 0.40.
  My stone in col 1 flattens everything toward 0 (ply-2 row 1 all ~0).
- call 3 (p2): additive score: col-1 stones -0.8/-1.0, opp col 2 -0.4, col 4 -0.15, col 0/5 +0.3, last-col bonus on even ply,
  -0.15/ply, cap if my stone in col 1. F1 0.682 (P 0.68 R 0.69), AUROC 0.839, sim 0.11.
  Misses: odd plies with col-5 / col-0 three-stacks (0,5,5,5,2 = 1.37 vs 0,5,5,3,2 = 0.11).
- call 4 (p3): + height>=3 bonus in col 0/5, odd-ply -0.5, band-mapped level. F1 0.606, sim 0.06. Worse: height bonus
  gave late-ply FPs (activation collapses after ply 6-8 regardless).
- call 5 (p4): height bonus only ply<=5, odd-ply last-col weights (my last stone in col 4/2/1 negative), extra -0.25/ply after ply 6.
  F1 0.735 (P 0.725 R 0.746), AUROC 0.869, sim 0.16.
- call 6 (p5): same fires, level = 2 + 2.5*score (neutral 2 for midgame, 0 for strongly negative col-1 openings). F1 0.735, sim 0.18. FINAL.

## Steer
5,6 / 3,3 / 5,5,5,0 (firing, -> max or zero): all column changes <= 1 point. Midgame 3,3,4,2,4,3,2,5,1,1 -> max: col 3 -4, col 4 +4.
Opposite pole (0,1): -> max raises col 1 +6, col 3 -3. Effect essentially none on the move.

## Synthesis
5,0,5,0,0,0 = 3.854 (beats dev max 3.660); 5,0,0,0,5,0 = 3.666 (beats). Recipe: me in col 5, opponent stacking col 0.

## Interpretation
Layer-1 opening feature: a weighted tally over the first few move tokens. Not a tactical concept. Mixture of column
preferences (col 1 strongly anti, col 0/5 pro), mostly when I moved first and it is my turn on an even ply.
