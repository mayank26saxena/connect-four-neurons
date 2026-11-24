# U51 notebook (layer 2, pole -, threshold 0.789, dev rate 3.0%, dev max 6.241)

## Observations
- Ply-1 positions (single opponent stone) dominate bands 6-8: col6 1.861, col0 1.459, col1 1.306, col3 0.929 fire; col2 0.525, col5 0.480, col4 0.451 do not.
- Ply-2/3 almost never fire (343-sequence scan in ply3.txt; only 3,0,3 / 3,4,3 / 1,0,6 / 5,0,6 cross threshold).
- Mid-game firing (73 of 160 sampled firing examples) is heterogeneous: last move col 6 / col 3 / col 4 common, top-row last moves common; both parities.
- Top mid-game case 4.046 (6,6,1,4,6,0,6,4,6,6,0,3,3,1,1,0,3): almost any opponent last move fires there (0.44-4.05); col 3 (O on O) highest.
- 141554 (4,6,4,3,5,1,5,6,0,3): O vertical pair in col3 next to X 2x2 block at cols 4-5 -> ~2.0; other last moves ~0.3.
- steer: no measurable effect on move probabilities in 5 positions (max change ~0.05).

## Hypotheses
H1: ply-1 opponent stone in col 0,1,3,6.
H2: opponent's last move stacks a vertical pair (O on O) -- tested: 0,1,0 / 3,1,3 etc. do NOT fire, so not by itself.
H3: random-direction mixture (no clean concept beyond the opening).

## Score calls
1. p1.py (ply1 & last_col in {0,1,3,6}): F1 0.720 (P 1.00, R 0.563), AUROC 0.781, sim share 0.01.
2. p2.py (+ top-row last move in corner col 0/6): F1 0.476 (P 0.38, R 0.63). Rejected, too many FPs.
3. p3.py (p1 fires; level adds weak mid-game grading by last row 5 / col 6): F1 0.720, sim share 0.03.

## Mid-game notes
- Mid-game firing depends on the whole board, not the last move: in the 4.046 board nearly every opponent last move fires; in game 1,2,2,6,...(ply 34) all X last moves to cols 0-2 fire.
- Within a game the activation alternates with parity and builds up slowly over many plies (e.g. 0.27, 0.30, 0.38, 0.70, 0.55, 1.09 on even plies, ~0 on odd), so it looks like an accumulated, diffuse board sum, with no single tactic behind it.
- Last-move stats, firing mid-game vs a band-1 baseline: last col 6 0.30 vs 0.14, last row 5 0.26 vs 0.07, cols 2/5 depleted. These are weak enrichments, and a rule built on them failed (call 2).
- Teacher evaluation, threats and must-blocks do not track it.
- steer max/zero: change <= 0.06 in every probe position (5 positions).
- Conclusion: the clean part is the opening-stone response. The mid-game part looks like a mixture, so it may be a random direction.
- Synthesis: greedy 2-ply extension from the 4.046 game reached 6.373 (beats dev max 6.241). Submitted p3 as final.
